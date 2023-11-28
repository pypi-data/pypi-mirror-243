import abc

from typing import Optional

from .models import ConnectionConfiguration


class BaseStorage(abc.ABC):
    def __init__(
        self, cloud_credentials: ConnectionConfiguration, folder_name: str
    ) -> None:
        self.cloud_credentials = cloud_credentials
        self.folder_name = folder_name

    @abc.abstractmethod
    def put(
        self,
        file_path: str,
        bucket_name: Optional[str] = None,
        key: Optional[str] = None,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, key: str, bucket_name: Optional[str] = None):
        raise NotImplementedError

    @abc.abstractmethod
    def file_exists(self, key: str, bucket_name: Optional[str] = None):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, key: str, bucket_name: Optional[str] = None):
        raise NotImplementedError
