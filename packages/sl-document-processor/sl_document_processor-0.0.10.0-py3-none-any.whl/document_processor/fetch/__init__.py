"""
Module for fetching content from the web and storing it.
"""

__all__ = [
    "URLCollector",
    "URLConfig",
    "DownloadManager",
    "DownloadConfig",
    "DownloadOutputConfig",
]

from .collector import URLCollector, URLConfig
from .downloader import DownloadConfig, DownloadManager, DownloadOutputConfig
