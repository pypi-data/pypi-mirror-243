from .models import StorageConfiguration, StorageType
from .provider import AWSCloudStorage


class StorageManager:
    storage = None

    def __init__(self, storage_config: StorageConfiguration) -> None:
        self.storage_type = storage_config.storage_type
        self.storage_config = storage_config

        if self.storage_type == StorageType.AWS:
            self.storage = AWSCloudStorage(
                cloud_credentials=self.storage_config.storage_connection_config,
                folder_name=self.storage_config.folder_name,
            )
        else:
            raise NotImplementedError(
                f"Storage type is not implemented: {self.storage_type}"
            )
