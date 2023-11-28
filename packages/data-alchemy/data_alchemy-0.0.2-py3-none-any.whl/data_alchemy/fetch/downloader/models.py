from enum import Enum

from typing import List

from pydantic import BaseModel


class DownloadProvider(str, Enum):
    LOCAL = "local"
    S3 = "s3"
    AZURE = "azure"
    GCP = "gcp"


class DownloadOutputConfig(BaseModel):
    provider: DownloadProvider
    location: str


class URLInformation(BaseModel):
    url: str
    name: str
    url_type: str


class DownloadConfig(BaseModel):
    urls: List[URLInformation]
    output_config: DownloadOutputConfig
