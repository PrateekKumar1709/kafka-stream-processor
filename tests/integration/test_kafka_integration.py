"""Integration tests for Kafka utilities."""

from unittest.mock import Mock, patch
import pytest

from src.consumer.utils.kafka_utils import ensure_topic_exists


@pytest.fixture
def mock_kafka_admin():
    """Fixture for mocking KafkaAdminClient."""
    with patch(
        'src.consumer.utils.kafka_utils.KafkaAdminClient',
        autospec=True
    ) as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        mock_instance.list_topics.return_value = []
        yield mock_instance


@pytest.fixture(autouse=True)
def mock_bootstrap_servers():
    """Mock bootstrap servers environment variable."""
    with patch.dict('os.environ', {'BOOTSTRAP_SERVERS': 'localhost:9092'}):
        yield


def test_topic_creation(mock_kafka_admin):  # pylint: disable=W0621
    """Test topic creation functionality."""
    test_topic = "test-topic"
    ensure_topic_exists(test_topic)

    mock_kafka_admin.create_topics.assert_called_once()
    called_args = mock_kafka_admin.create_topics.call_args[0][0]
    assert len(called_args) == 1
    assert called_args[0].name == test_topic
