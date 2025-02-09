from src.consumer.utils.analysis_utils import get_ip_type
from src.consumer.utils.analysis_utils import get_app_version_category


def test_ip_type():
    assert get_ip_type("192.168.1.1") == "Private"
    assert get_ip_type("8.8.8.8") == "Public"
    assert get_ip_type("invalid-ip") == "Invalid"


def test_app_version_category():
    assert get_app_version_category("2.0.0") == "Current"
    assert get_app_version_category("1.9.0") == "Legacy"
    assert get_app_version_category("invalid") == "Unknown"
