import abc

from typing import Optional

from pydantic import BaseModel

from .models import AWSCredentials, AzureCredentials, GCLOUDCredentials


class CloudCredentials(BaseModel):
    aws_credentials: Optional[AWSCredentials] = None
    gcloud_credentials: Optional[GCLOUDCredentials] = None
    azure_credentials: Optional[AzureCredentials] = None

    # @model_validator
    # def validate_credentials(self):
    #     if (
    #         self.aws_credentials is None
    #         and self.gcloud_credentials is None
    #         and self.azure_credentials is None
    #     ):
    #         raise ValueError(
    #             "Atleast one of the cloud credentials should be provided."
    #         )


class BaseCloudStorage(abc.ABC):
    def __init__(self, cloud_credentials: CloudCredentials, folder_name: str) -> None:
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
    def delete(self):
        raise NotImplementedError
