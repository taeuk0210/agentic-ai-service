from abc import ABC, abstractmethod
from typing import Any


class BaseStorageClient(ABC):
    @abstractmethod
    def create_bucket(self, bucket: str) -> bool:
        pass

    @abstractmethod
    def delete_bucket(self, bucket: str) -> bool:
        pass

    @abstractmethod
    def upload_file(self, fileobj: Any, bucket: str, key: str) -> bool:
        pass

    @abstractmethod
    def download_file(self, bucket: str, key: str, download_path: str) -> bool:
        pass

    @abstractmethod
    def delete_file(self, bucket: str, key: str) -> bool:
        pass
