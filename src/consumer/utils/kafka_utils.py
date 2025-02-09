"""Kafka utilities module."""

try:
    from kafka.consumer.group import KafkaConsumer
    from kafka.producer.kafka import KafkaProducer
    from kafka.admin import KafkaAdminClient, NewTopic
except ImportError:
    from kafka import KafkaConsumer, KafkaProducer, KafkaAdminClient
    from kafka.admin import NewTopic

import json
import os
import logging

logger = logging.getLogger(__name__)

BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "kafka:9092")
INPUT_TOPIC = os.getenv("INPUT_TOPIC", "user-login")
GROUP_ID = os.getenv("GROUP_ID", "my-consumer-group")


def ensure_topic_exists(topic_name, num_partitions=1, replication_factor=1):
    """Create topic if it doesn't exist."""
    admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
    try:
        topics = admin_client.list_topics()
        if topic_name not in topics:
            logger.info("Attempting to create topic: %s", topic_name)
            new_topic = NewTopic(
                name=topic_name,
                num_partitions=num_partitions,
                replication_factor=replication_factor,
            )
            admin_client.create_topics([new_topic])
            logger.info("Successfully created topic: %s", topic_name)
    except Exception as e:
        logger.error("Error ensuring topic exists: %s", e)
    finally:
        admin_client.close()


def create_consumer():
    """Create and return a Kafka consumer instance."""
    return KafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        api_version=(2, 5, 0),
    )


def create_producer():
    """Create and return a Kafka producer instance."""
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        api_version=(2, 5, 0),
    )
