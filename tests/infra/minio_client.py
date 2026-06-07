import io
import os
import unittest

from app.infra.obj.minio_client import minio_client


class TestMinIOStorageClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = minio_client
        cls.test_bucket = "test-bucket-lifecycle"
        cls.local_test_file = "local_test_sample.txt"
        cls.local_download_file = "local_downloaded_sample.txt"

        with open(cls.local_test_file, "w", encoding="utf-8") as f:
            f.write("이 파일은 MinIO 스토리지 클라이언트 테스트용 파일입니다.")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.local_test_file):
            os.remove(cls.local_test_file)
        if os.path.exists(cls.local_download_file):
            os.remove(cls.local_download_file)

    def setUp(self):
        if self.client.create_bucket(self.test_bucket):
            self.client.delete_file(self.test_bucket, "test_file.txt")
            self.client.delete_file(self.test_bucket, "test_fileobj.txt")

    def tearDown(self):
        self.client.delete_file(self.test_bucket, "test_file.txt")
        self.client.delete_file(self.test_bucket, "test_fileobj.txt")

        try:
            self.client.delete_bucket(bucket_name=self.test_bucket)
        except Exception:
            pass

    def test_create_bucket_lifecycle(self) -> None:
        # given
        temp_bucket_name = "temporary-empty-bucket"

        # when
        first_create = self.client.create_bucket(temp_bucket_name)
        second_create = self.client.create_bucket(temp_bucket_name)
        deleted = self.client.delete_bucket(bucket_name=temp_bucket_name)

        # then
        self.assertTrue(first_create)
        self.assertTrue(second_create)
        self.assertTrue(deleted)

    def test_upload_and_download_file(self) -> None:
        # given
        object_name = "test_file.txt"
        if os.path.exists(self.local_download_file):
            os.remove(self.local_download_file)

        # when
        upload_success = self.client.upload_file(
            local_file_path=self.local_test_file,
            bucket_name=self.test_bucket,
            object_name=object_name,
        )
        download_success = self.client.download_file(
            bucket_name=self.test_bucket,
            object_name=object_name,
            local_download_path=self.local_download_file,
        )
        with open(self.local_download_file, "r", encoding="utf-8") as f:
            downloaded_content = f.read()

        # then
        self.assertTrue(upload_success)
        self.assertTrue(download_success)
        self.assertTrue(os.path.exists(self.local_download_file))
        self.assertIn("MinIO 스토리지 클라이언트 테스트용", downloaded_content)

    def test_upload_fileobj(self) -> None:
        # given
        object_name = "test_fileobj.txt"
        mock_file_stream = io.BytesIO(
            b"Hello MinIO, this is an in-memory stream object data."
        )

        # when
        upload_success = self.client.upload_fileobj(
            file_obj=mock_file_stream,
            bucket_name=self.test_bucket,
            object_name=object_name,
        )

        # then
        self.assertTrue(upload_success)

    def test_delete_file(self) -> None:
        # given
        object_name = "test_file.txt"
        self.client.upload_file(
            local_file_path=self.local_test_file,
            bucket_name=self.test_bucket,
            object_name=object_name,
        )

        # when
        delete_success = self.client.delete_file(
            bucket_name=self.test_bucket, object_name=object_name
        )

        # then
        self.assertTrue(delete_success)


if __name__ == "__main__":
    unittest.main()
