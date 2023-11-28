from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class Element(BaseModel):
    name: str
    selector: str


class ExtractionConfig(BaseModel):
    website: str
    elements: List[Element]


class CloudProvider(str, Enum):
    AWS = "AWS"
    AZURE = "AZURE"
    GCP = "GCP"


class ConfigurationSettings(BaseModel):
    url: str
    yaml_file_name: str
    cloud_provider: CloudProvider
    processed: Optional[bool] = False


class HTML(BaseModel):
    url: str
