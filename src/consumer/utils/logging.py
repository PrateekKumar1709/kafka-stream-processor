"""Logging configuration module."""

import logging


def setup_logger():
    """Setup and return logger with configuration."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)
