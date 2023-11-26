"""
Module to deal with various document processing tasks.
"""

__all__ = [
    "URLCollector",
    "URLConfig",
    "DownloadManager",
    "DownloadConfig",
    "DownloadOutputConfig",
    "ConfigurationSettings",
    "CloudProvider",
    "ExtractionConfig",
    "DocumentLoader",
    "DocumentConfig",
    "DocumentType",
    "CloudConfig",
    "CloudStorageManager",
    "CloudType",
    "CloudCredentials",
    "DatabaseConfig",
    "DatabaseConnectionConfig",
    "DatabaseManager",
    "DatabaseType",
    "HTMLConfigurer",
]


from .cloud_storage import CloudConfig, CloudCredentials, CloudStorageManager, CloudType
from .database import (
    DatabaseConfig,
    DatabaseConnectionConfig,
    DatabaseManager,
    DatabaseType,
)
from .fetch import (
    DownloadConfig,
    DownloadManager,
    DownloadOutputConfig,
    URLCollector,
    URLConfig,
)

from .store_configs import (
    CloudProvider,
    ConfigurationSettings,
    ExtractionConfig,
    HTMLConfigurer,
)

from .transform import DocumentConfig, DocumentLoader, DocumentType
