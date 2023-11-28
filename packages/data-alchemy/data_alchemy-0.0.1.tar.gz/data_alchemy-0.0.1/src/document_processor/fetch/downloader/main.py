import os
import shutil
from tempfile import mkdtemp

import requests
from tqdm import tqdm

from document_processor.ingest.cloud_storage import StorageConfiguration, StorageManager

from .models import DownloadConfig, DownloadProvider


class DownloadManager:
    def __init__(self, download_config: DownloadConfig):
        self.urls = download_config.urls
        self.output_config = download_config.output_config

    def download(self) -> None:
        for url_information in self.urls:
            response = requests.get(url_information.url, timeout=5)
            if self.output_config.provider == DownloadProvider.LOCAL:
                if not os.path.exists(self.output_config.location):
                    os.makedirs(self.output_config.location)

                name = url_information.name
                file_type = url_information.type

                with open(
                    os.path.join(self.output_config.location, f"{name}.{file_type}"),
                    "wb",
                ) as f:
                    f.write(response.content)

            elif self.output_config.provider == DownloadProvider.S3:
                pass

    def sync_documents_to_cloud(self, cloud_configuration: StorageConfiguration):
        try:
            storage_manager = StorageManager(cloud_configuration)
            tmp_dir = mkdtemp()

            for url_information in tqdm(self.urls, total=len(self.urls)):
                name = url_information.name
                file_type = url_information.url_type

                file_path = os.path.join(tmp_dir, f"{name}.{file_type}")

                response = requests.get(url_information.url, timeout=5)

                with open(file_path, "wb") as f:
                    f.write(response.content)

                storage_manager.storage.put(
                    file_path=file_path,
                    key=f"{name}.{file_type}",
                )

        finally:
            shutil.rmtree(tmp_dir)
