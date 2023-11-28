from datetime import datetime
from uuid import NAMESPACE_URL, uuid5


def fetch_unique_id(url: str) -> str:
    """
    Fetch a unique ID for a given URL.
    This method will be used to create a unique ID for each URL.
    """
    date_str = datetime.now().strftime("%Y_%m_%d")
    uid = uuid5(NAMESPACE_URL, url).hex
    return f"{uid}_{date_str}"


def is_valid_url(url: str) -> bool:
    """
    Check if a given URL is valid.
    """
    return url.startswith("http") or url.startswith("https")
