from enum import Enum

from pydantic import BaseModel

from .provider import ConnectionConfiguration


class StorageType(str, Enum):
    LOCAL = "local"
    AWS = "aws"
    GCLOUD = "gcloud"
    AZURE = "azure"


class StorageConfiguration(BaseModel):
    storage_type: StorageType
    folder_name: str
    storage_connection_config: ConnectionConfiguration
