"""
Module to deal with various document processing tasks.
"""

__all__ = [
    "Collector",
    "CollectorConfiguration",
    "DownloadManager",
    "DownloadConfig",
    "DownloadOutputConfig",
    "ConfigurationSettings",
    "CloudProvider",
    "ExtractionConfig",
    "DocumentLoader",
    "DocumentConfig",
    "DocumentType",
    "DatabaseConfig",
    "DatabaseConnectionConfig",
    "DatabaseManager",
    "DatabaseType",
    "HTMLConfigurer",
    "StorageConfiguration",
    "StorageManager",
    "StorageType",
    "__version__",
]

from .__version__ import version

__version__ = version

from .fetch import (
    Collector,
    CollectorConfiguration,
    DownloadConfig,
    DownloadManager,
    DownloadOutputConfig,
)
from .ingest.cloud_storage import StorageConfiguration, StorageManager, StorageType
from .ingest.database import (
    DatabaseConfig,
    DatabaseConnectionConfig,
    DatabaseManager,
    DatabaseType,
)

from .store_configs import (
    CloudProvider,
    ConfigurationSettings,
    ExtractionConfig,
    HTMLConfigurer,
)

from .transform import DocumentConfig, DocumentLoader, DocumentType
