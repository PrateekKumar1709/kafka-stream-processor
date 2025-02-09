"""Consumer module for processing Kafka messages."""

import os
import logging
import time
from datetime import datetime
from kafka.errors import KafkaError
from .utils.analysis_utils import get_ip_type
from .utils.analysis_utils import get_app_version_category
from .utils.kafka_utils import (
    ensure_topic_exists,
    create_consumer,
    create_producer
)
from .utils.metrics import (
    setup_metrics,
    MESSAGES_PROCESSED,
    RISK_SCORES,
    MESSAGE_PROCESSING_TIME,
    ERROR_COUNTER,
    RISK_LEVEL_GAUGE
)

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Environment variables
BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "kafka:9092")
INPUT_TOPIC = os.getenv("INPUT_TOPIC", "user-login")
OUTPUT_TOPIC = os.getenv("OUTPUT_TOPIC", "processed-logins")
GROUP_ID = os.getenv("GROUP_ID", "my-consumer-group")
METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))

# Region mapping
REGION_MAPPING = {
    "US": "North America",
    "CA": "North America",
    "MX": "North America",
    "GB": "Europe",
    "FR": "Europe",
    "DE": "Europe",
    "IT": "Europe",
    "CN": "Asia",
    "JP": "Asia",
    "IN": "Asia",
}


def _get_day_segment(hour):
    """Get the day segment based on hour."""
    if 5 <= hour < 12:
        return "Morning"
    if 12 <= hour < 17:
        return "Afternoon"
    if 17 <= hour < 22:
        return "Evening"
    return "Night"


def _get_platform_info(device_type):
    """Get platform information."""
    device_type_lower = device_type.lower()
    is_ios = device_type_lower == "ios"
    is_android = device_type_lower == "android"
    os_family = (
        "iOS" if is_ios
        else "Android" if is_android
        else "Desktop"
    )
    return {
        "type": device_type.upper(),
        "is_mobile": device_type_lower in ["ios", "android"],
        "os_family": os_family
    }


def _get_app_status(app_version):
    """Get application status information."""
    version_category = get_app_version_category(app_version)
    return {
        "version": app_version,
        "version_category": version_category,
        "needs_update": version_category == "Legacy"
    }


def _get_security_analysis(data):
    """Get security analysis information."""
    return {
        "ip_type": get_ip_type(data["ip"]),
        "ip_address": data["ip"],
        "device_id_present": bool(data.get("device_id"))
    }


def _calc_risk_factors(data, login_time):
    """Calculate risk factors for the login attempt."""
    app_version_status = get_app_version_category(data["app_version"])
    ip_type = get_ip_type(data["ip"])
    return {
        "using_legacy_version": app_version_status == "Legacy",
        "private_ip_login": ip_type == "Private",
        "odd_hour_login": not (9 <= login_time.hour <= 17),
        "weekend_login": login_time.weekday() >= 5
    }


def _calc_risk_assessment(risk_factors):
    """Calculate risk assessment based on risk factors."""
    risk_score = sum(1 for factor in risk_factors.values() if factor)
    risk_level = (
        "High" if risk_score >= 3
        else "Medium" if risk_score >= 2
        else "Low"
    )
    return {
        "risk_score": risk_score,
        "risk_level": risk_level
    }


def process_message(data):
    """Process and transform the input message with specific insights."""
    try:
        logger.info(
            "Processing message: %s",
            data
        )
        required_fields = [
            "user_id",
            "app_version",
            "locale",
            "device_type",
            "timestamp",
            "ip"
        ]
        if not all(field in data for field in required_fields):
            logger.warning("Message missing required fields: %s", data)
            ERROR_COUNTER.labels(error_type="missing_fields").inc()
            return False

        with MESSAGE_PROCESSING_TIME.time():
            login_time = datetime.fromtimestamp(data["timestamp"])
            insights = {
                "event_id": data["user_id"],
                "timestamp": data["timestamp"],
                "analysis_timestamp": int(time.time()),
                "login_hour": login_time.hour,
                "login_day": login_time.strftime("%A"),
                "is_weekend": login_time.weekday() >= 5,
                "day_segment": _get_day_segment(login_time.hour),
                "region": REGION_MAPPING.get(data["locale"], "Other"),
                "country_code": data["locale"],
                "platform": _get_platform_info(data["device_type"]),
                "app_status": _get_app_status(data["app_version"]),
                "security_analysis": _get_security_analysis(data)
            }

            risk_factors = _calc_risk_factors(data, login_time)
            insights["risk_factors"] = risk_factors
            insights["risk_assessment"] = _calc_risk_assessment(risk_factors)

            MESSAGES_PROCESSED.inc()
            RISK_SCORES.labels(
                risk_level=insights["risk_assessment"]["risk_level"]
            ).inc()
            RISK_LEVEL_GAUGE.labels(
                risk_level=insights["risk_assessment"]["risk_level"]
            ).set(insights["risk_assessment"]["risk_score"])

            logger.info("Generated insights: %s", insights)
            return insights

    except (ValueError, KeyError, TypeError) as e:
        logger.error("Error processing message: %s", e)
        ERROR_COUNTER.labels(error_type="processing_error").inc()
        return False


def main():
    """Main function to run the consumer."""
    logger.info("Starting consumer application")
    setup_metrics(port=METRICS_PORT)
    ensure_topic_exists(OUTPUT_TOPIC)

    try:
        consumer = create_consumer()
        producer = create_producer()
        logger.info("Starting message processing loop...")

        for message in consumer:
            try:
                data = message.value
                processed_data = process_message(data)
                if processed_data:
                    future = producer.send(OUTPUT_TOPIC, value=processed_data)
                    record_metadata = future.get(timeout=10)
                    logger.info(
                        "Insights sent to topic %s",
                        record_metadata.topic
                    )
                else:
                    logger.info("Message skipped due to processing rules")
                producer.flush()
            except KafkaError as ke:
                logger.error("Kafka error processing message: %s", ke)
                ERROR_COUNTER.labels(error_type="kafka_error").inc()
            except (ValueError, KeyError) as e:
                logger.error("Data processing error: %s", e)
                ERROR_COUNTER.labels(error_type="data_error").inc()

    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except KafkaError as ke:
        logger.error("Critical Kafka error: %s", ke)
        ERROR_COUNTER.labels(error_type="critical_kafka_error").inc()
    finally:
        logger.info("Cleaning up resources...")
        try:
            consumer.close()
            producer.close()
        except KafkaError as ke:
            logger.error("Error during cleanup: %s", ke)
            ERROR_COUNTER.labels(error_type="cleanup_error").inc()


if __name__ == "__main__":
    main()
