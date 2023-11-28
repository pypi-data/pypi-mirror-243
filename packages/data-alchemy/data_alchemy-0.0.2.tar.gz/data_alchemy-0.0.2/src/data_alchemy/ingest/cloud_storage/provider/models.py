from typing import Optional

from pydantic import BaseModel, model_validator


class AWSCredentials(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: Optional[str] = None
    region_name: str


class GCLOUDCredentials(BaseModel):
    # Credentil required to auithenticate with Google Cloud Storage
    gcloud_credentials: str


class AzureCredentials(BaseModel):
    # authenticate to use blob storage
    azure_storage_account_name: str
    azure_storage_account_key: str
    azure_storage_container_name: str
    azure_storage_blob_name: str
    azure_storage_blob_url: str


class ConnectionConfiguration(BaseModel):
    aws_credentials: Optional[AWSCredentials] = None
    gcloud_credentials: Optional[GCLOUDCredentials] = None
    azure_credentials: Optional[AzureCredentials] = None

    @model_validator(mode="after")
    def validate_credentials(self):
        if (
            self.aws_credentials is None
            and self.gcloud_credentials is None
            and self.azure_credentials is None
        ):
            print("No credentials configured for cloud storage.")
        return self
