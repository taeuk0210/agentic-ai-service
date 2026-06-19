import os
from typing import Any

import boto3

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
        logger.info(f"MinIOStorageClient is initialized.")

    def create_bucket(self, bucket: str) -> bool:
        try:
            self.client.create_bucket(Bucket=bucket)
            return True

        except Exception as e:
            logger.error(f"MinIOStorageClient.create_bucket() error ({bucket}): {e}")
            return False

    def delete_bucket(self, bucket: str) -> bool:
        try:
            self.client.delete_bucket(Bucket=bucket)
            return True

        except Exception as e:
            logger.error(f"MinIOStorageClient.delete_bucket() error ({bucket}): {e}")
            return False

    def upload_file(self, bucket: str, key: str, fileobj: Any) -> bool:
        try:
            self.client.upload_fileobj(Fileobj=fileobj, Bucket=bucket, Key=key)
            return True

        except Exception as e:
            logger.error(f"MinIOStorageClient.upload_file() error ({key}): {e}")
            return False

    def download_file(self, bucket: str, key: str, download_path: str) -> bool:
        try:
            local_dir = os.path.dirname(download_path)
            if local_dir and not os.path.exists(local_dir):
                os.makedirs(local_dir, exist_ok=True)

            self.client.download_file(Bucket=bucket, Key=key, Filename=download_path)
            return True

        except Exception as e:
            logger.error(f"MinIOStorageClient.download_file() error ({key}): {e}")
            return False

    def delete_file(self, bucket: str, key: str) -> bool:
        try:
            self.client.delete_object(Bucket=bucket, Key=key)
            return True

        except Exception as e:
            logger.error(f"MinIOStorageClient.delete_file() error ({key}): {e}")
            return False


minio_client = MinIOStorageClient()
