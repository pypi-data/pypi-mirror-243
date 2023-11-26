from enum import Enum

from pydantic import BaseModel

from .provider import AWSCloudStorage, CloudCredentials


class CloudType(str, Enum):
    AWS = "aws"
    GCLOUD = "gcloud"
    AZURE = "azure"


class CloudConfig(BaseModel):
    cloud_type: CloudType
    storage_connection_config: CloudCredentials
    folder_name: str


class CloudStorageManager:
    cloud_storage = None

    def __init__(self, cloud_config: CloudConfig) -> None:
        self.cloud_type = cloud_config.cloud_type
        self.coud_config = cloud_config

        if self.cloud_type == CloudType.AWS:
            self.cloud_storage = AWSCloudStorage(
                cloud_credentials=self.coud_config.storage_connection_config,
                folder_name=self.coud_config.folder_name,
            )
        else:
            raise NotImplementedError(
                f"Cloud Storage for {self.cloud_type} is not implemented."
            )
