import ipaddress


def get_ip_type(ip):
    """Determine if IP is private or public"""
    try:
        ip_addr = ipaddress.ip_address(ip)
        return "Private" if ip_addr.is_private else "Public"
    except ValueError:
        return "Invalid"


def get_app_version_category(version):
    """Categorize app version"""
    try:
        major_version = float(version.split(".")[0])
        return "Current" if major_version >= 2 else "Legacy"
    except ValueError:
        return "Unknown"
