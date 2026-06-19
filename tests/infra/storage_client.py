import os
import io

import unittest

from app.infra.obj.minio_client import minio_client


class TestStorageClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = minio_client

    def test_bucket(self) -> None:
        # given
        bucket = "test-bucket-1"

        # when
        created = self.client.create_bucket(bucket=bucket)
        deleted = self.client.delete_bucket(bucket=bucket)

        # then
        self.assertTrue(created)
        self.assertTrue(deleted)

    def test_file(self) -> None:
        # given
        bucket = "test-bucket-2"
        key = "test-file.txt"
        path = "local-file.txt"
        fileobj = io.BytesIO(b"Hello MinIO, this is an in-memory stream object data.")
        self.client.create_bucket(bucket=bucket)

        # when
        uploaded = self.client.upload_file(bucket=bucket, key=key, fileobj=fileobj)
        downloaded = self.client.download_file(
            bucket=bucket, key=key, download_path=path
        )
        deleted = self.client.delete_file(bucket=bucket, key=key)
        os.remove(path=path)
        self.client.delete_bucket(bucket=bucket)

        # then
        self.assertTrue(uploaded)
        self.assertTrue(downloaded)
        self.assertTrue(deleted)


if __name__ == "__main__":
    unittest.main()
