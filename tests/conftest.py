"""Test configuration module."""

import os
import sys
import pytest

# Add project root to Python path for test imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@pytest.fixture(autouse=True)
def mock_env():
    """Mock environment variables for testing"""
    test_env = {
        "BOOTSTRAP_SERVERS": "localhost:9092",
        "INPUT_TOPIC": "test-input",
        "OUTPUT_TOPIC": "test-output",
        "METRICS_PORT": "8000"  # Add metrics port for Prometheus
    }
    # Set environment variables
    for key, value in test_env.items():
        os.environ[key] = value
    yield
    # Cleanup
    for key in test_env.keys():
        os.environ.pop(key, None)


@pytest.fixture(autouse=True)
def mock_metrics():
    """Mock metrics server for testing."""
    from unittest.mock import patch
    with patch(
        'prometheus_client.start_http_server'
    ):
        yield
