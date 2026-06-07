import os
from typing import Any

import boto3
from botocore.exceptions import ClientError

from app.config import config
from app.logger import logger
from app.infra.obj.interface import BaseStorageClient


class MinIOStorageClient(BaseStorageClient):
    def __init__(self):
        self.client = boto3.client(
            service_name="s3",
            endpoint_url=f"http://{config.MINIO_HOST}:{config.MINIO_PORT}",
            aws_access_key_id=config.MINIO_ACCESS_KEY,
            aws_secret_access_key=config.MINIO_SECRET_KEY,
            region_name="us-east-1",
        )

    def create_bucket(self, bucket_name: str) -> bool:
        try:
            try:
                self.client.head_bucket(Bucket=bucket_name)
                return True
            except ClientError:
                pass

            self.client.create_bucket(Bucket=bucket_name)
            return True

        except Exception as e:
            logger.error(
                f"MinIOStorageClient.create_bucket() error ({bucket_name}): {e}"
            )
            return False

    def delete_bucket(self, bucket_name: str) -> bool:
        try:
            self.client.delete_bucket(Bucket=bucket_name)
            return True

        except Exception as e:
            logger.error(
                f"MinIOStorageClient.delete_bucket() error ({bucket_name}): {e}"
            )
            return False

    def upload_file(
        self, local_file_path: str, bucket_name: str, object_name: str
    ) -> bool:
        try:
            if not os.path.exists(local_file_path):
                return False

            self.client.upload_file(
                Filename=local_file_path, Bucket=bucket_name, Key=object_name
            )
            return True

        except Exception as e:
            logger.error(f"MinIOStorageClient.upload_file() error ({object_name}): {e}")
            return False

    def upload_fileobj(self, file_obj: Any, bucket_name: str, object_name: str) -> bool:
        try:
            self.client.upload_fileobj(
                Fileobj=file_obj, Bucket=bucket_name, Key=object_name
            )
            return True

        except Exception as e:
            logger.error(
                f"MinIOStorageClient.upload_fileobj() error ({object_name}): {e}"
            )
            return False

    def download_file(
        self, bucket_name: str, object_name: str, local_download_path: str
    ) -> bool:
        try:
            local_dir = os.path.dirname(local_download_path)
            if local_dir and not os.path.exists(local_dir):
                os.makedirs(local_dir, exist_ok=True)

            self.client.download_file(
                Bucket=bucket_name, Key=object_name, Filename=local_download_path
            )
            return True

        except Exception as e:
            logger.error(
                f"MinIOStorageClient.download_file() error ({object_name}): {e}"
            )
            return False

    def delete_file(self, bucket_name: str, object_name: str) -> bool:
        try:
            self.client.delete_object(Bucket=bucket_name, Key=object_name)
            return True

        except Exception as e:
            logger.error(f"MinIOStorageClient.delete_file() error ({object_name}): {e}")
            return False


minio_client = MinIOStorageClient()
