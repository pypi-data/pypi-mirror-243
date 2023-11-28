"""
Module to download content from the web.
"""

from .main import DownloadManager
from .models import (
    DownloadConfig,
    DownloadOutputConfig,
    DownloadProvider,
    URLInformation,
)


__all__ = [
    "DownloadManager",
    "DownloadConfig",
    "DownloadOutputConfig",
    "URLInformation",
    "DownloadProvider",
]
