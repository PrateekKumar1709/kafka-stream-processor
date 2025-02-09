"""Metrics configuration for Prometheus monitoring."""
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Message processing metrics
MESSAGES_PROCESSED = Counter(
    'kafka_consumer_messages_processed_total',
    'Total number of messages processed'
)

PROCESSING_TIME = Gauge(
    'kafka_consumer_processing_time_seconds',
    'Time taken to process messages'
)

RISK_SCORES = Counter(
    'kafka_consumer_risk_scores_total',
    'Risk scores distribution',
    ['risk_level']
)

MESSAGE_PROCESSING_TIME = Histogram(
    'kafka_consumer_message_processing_seconds',
    'Time taken to process each message',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

ERROR_COUNTER = Counter(
    'kafka_consumer_errors_total',
    'Total number of errors by type',
    ['error_type']
)

RISK_LEVEL_GAUGE = Gauge(
    'kafka_consumer_risk_level',
    'Current risk level by category',
    ['risk_level']
)


def setup_metrics(port=8000):
    """Start metrics HTTP server."""
    start_http_server(port, addr='0.0.0.0')
