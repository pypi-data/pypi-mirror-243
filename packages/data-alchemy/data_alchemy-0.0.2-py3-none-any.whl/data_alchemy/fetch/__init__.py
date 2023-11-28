"""
Module for fetching content from the web and storing it.
"""

__all__ = [
    "Collector",
    "CollectorConfiguration",
    "CollectorOptions",
    "DownloadManager",
    "DownloadConfig",
    "DownloadOutputConfig",
]

from .collector import Collector, CollectorConfiguration, CollectorOptions
from .downloader import DownloadConfig, DownloadManager, DownloadOutputConfig
