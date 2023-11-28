import os
from pathlib import Path
from typing import Union

from ._base_storage import BaseStorage
from .models import ConnectionConfiguration


class LocalStorage(BaseStorage):
    def __init__(
        self, cloud_credentials: ConnectionConfiguration, folder_name: str
    ) -> None:
        super().__init__(cloud_credentials, folder_name)
        self.folder_name = folder_name

    def create_bucket(self, bucket_name: str = None):
        if bucket_name is None:
            bucket_name = self.folder_name

        if not os.path.exists(bucket_name):
            os.makedirs(bucket_name)
        return True

    def bucket_exists(self, bucket_name: str = None):
        if bucket_name is None:
            bucket_name = self.folder_name

        return os.path.exists(bucket_name)

    def file_exists(self, key: str, bucket_name: Union[str, None] = None):
        if bucket_name is None:
            bucket_name = self.folder_name

        file_path = Path(bucket_name) / key

        return os.path.exists(file_path)

    def put(
        self,
        file_path: str,
        bucket_name: Union[str, None] = None,
        key: Union[str, None] = None,
    ):
        if bucket_name is None:
            bucket_name = self.folder_name

        if key is None:
            raise ValueError("Key cannot be None")

        assert key is not None

        file_path = Path(bucket_name) / key

        with open(file_path, "wb") as f:
            f.write(file_path)
        return True

    def get(self, key: str, bucket_name: Union[str, None] = None):
        if bucket_name is None:
            bucket_name = self.folder_name

        file_path = Path(bucket_name) / key

        with open(file_path, "rb") as f:
            return f.read()

    def delete(self, key: str, bucket_name: Union[str, None] = None):
        if bucket_name is None:
            bucket_name = self.folder_name

        file_path = Path(bucket_name) / key

        os.remove(file_path)
        return True
