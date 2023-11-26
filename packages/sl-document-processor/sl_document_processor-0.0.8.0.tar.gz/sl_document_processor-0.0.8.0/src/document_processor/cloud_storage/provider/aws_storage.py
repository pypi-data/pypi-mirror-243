import logging
from typing import Any, Callable, Optional, ParamSpec, TypeVar

import boto3
from botocore.exceptions import ClientError

from ._base_storage import BaseCloudStorage, CloudCredentials

F = TypeVar("F", bound=Callable[..., Any])

P = ParamSpec("P")
T = TypeVar("T")


def client_required(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(self: "AWSCloudStorage", *args: P.args, **kwargs: P.kwargs):
        if self.is_client_set():
            response = func(self, *args, **kwargs)
            return response

        raise ValueError(
            f"Client is not instantiated. Please set it before using the function - {func.__name__}"
        )

    return wrapper


class AWSCloudStorage(BaseCloudStorage):
    client = None

    def __init__(self, cloud_credentials: CloudCredentials, folder_name: str) -> None:
        super().__init__(cloud_credentials, folder_name)

        if cloud_credentials.aws_credentials is not None:
            if cloud_credentials.aws_credentials.region_name is None:
                print("AWS region not specified. Using default region - us-east-1")
                self.client = boto3.client(
                    "s3",
                    aws_access_key_id=cloud_credentials.aws_credentials.aws_access_key_id,
                    aws_secret_access_key=cloud_credentials.aws_credentials.aws_secret_access_key,
                )
            else:
                print(
                    f"AWS region specified - {cloud_credentials.aws_credentials.region_name}"
                )
                self.client = boto3.client(
                    "s3",
                    aws_access_key_id=cloud_credentials.aws_credentials.aws_access_key_id,
                    aws_secret_access_key=cloud_credentials.aws_credentials.aws_secret_access_key,
                    region_name=cloud_credentials.aws_credentials.region_name,
                )

    def is_client_set(self):
        return self.client is not None

    @client_required
    def create_bucket(self, bucket_name: str = None):
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).

        :param bucket_name: Bucket to create
        :return: True if bucket created, else False
        """

        if bucket_name is None:
            bucket_name = self.folder_name

        # Create bucket
        try:
            if self.cloud_credentials.aws_credentials.region_name is None:
                self.client.create_bucket(Bucket=bucket_name)
            else:
                location = {
                    "LocationConstraint": self.cloud_credentials.aws_credentials.region_name
                }
                self.client.create_bucket(
                    Bucket=bucket_name, CreateBucketConfiguration=location
                )
        except ClientError as e:
            logging.error(e)
            return False
        return True

    @client_required
    def bucket_exists(self, bucket_name: str = None):
        """Determine whether bucket_name exists and the user has permission to access it

        :param bucket_name: string
        :return: True if the referenced bucket_name exists, otherwise False
        """

        if bucket_name is None:
            bucket_name = self.folder_name

        # Retrieve the list_buckets results and check for the presence of our bucket
        try:
            self.client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            logging.debug(e)
            return False
        return True

    @client_required
    def file_exists(self, key: str, bucket_name: Optional[str] = None):
        """Determine whether an object with the specified key exists in the specified bucket

        :param bucket_name: string
        :param key: string
        :return: True if the object exists, otherwise False
        """

        if bucket_name is None:
            bucket_name = self.folder_name

        # Retrieve the list_buckets results and check for the presence of our bucket
        try:
            self.client.head_object(Bucket=bucket_name, Key=key)
        except ClientError as e:
            logging.debug(e)
            return False
        return True

    @client_required
    def put(
        self,
        file_path: str,
        bucket_name: Optional[str] = None,
        key: Optional[str] = None,
    ):
        """Uploads a file to a S3 bucket"""

        if bucket_name is None:
            bucket_name = self.folder_name

        # If bucket doesn't exist, create it
        if not self.bucket_exists(bucket_name):
            logging.info("Bucket %s doesn't exist. Creating it...", bucket_name)
            self.create_bucket(bucket_name)

        # If S3 object_name was not specified, use file_name
        if key is None:
            key = file_path

        try:
            self.client.upload_file(file_path, bucket_name, key)
        except ClientError as e:
            logging.error(e)
            return False

        return True

    def get(self, key: str, bucket_name: Optional[str] = None):
        """
        Read an object from an S3 bucket
        """
        if bucket_name is None:
            bucket_name = self.folder_name

        try:
            response = self.client.get_object(Bucket=bucket_name, Key=key)
        except ClientError as e:
            logging.error(e)
            return None

        return response

    def delete(self):
        print("delete")
