from abc import ABC, abstractmethod
from typing import Any


class BaseStorageClient(ABC):
    @abstractmethod
    def create_bucket(self, bucket_name: str) -> bool:
        pass

    @abstractmethod
    def delete_bucket(self, bucket_name: str) -> bool:
        pass

    @abstractmethod
    def upload_file(
        self, local_file_path: str, bucket_name: str, object_name: str
    ) -> bool:
        pass

    @abstractmethod
    def upload_fileobj(self, file_obj: Any, bucket_name: str, object_name: str) -> bool:
        pass

    @abstractmethod
    def download_file(
        self, bucket_name: str, object_name: str, local_download_path: str
    ) -> bool:
        pass

    @abstractmethod
    def delete_file(self, bucket_name: str, object_name: str) -> bool:
        pass
