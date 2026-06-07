from app.infra.obj.interface import BaseStorageClient
from app.infra.obj.minio_client import minio_client

__all__ = [
    "BaseStorageClient",
    "minio_client",
]
