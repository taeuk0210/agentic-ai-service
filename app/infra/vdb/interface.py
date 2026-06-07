from abc import ABC, abstractmethod
from typing import List, Any

from app.schema import VectorCreateRequest, VectorQueryResponse


class BaseVectorDBClient(ABC):
    @abstractmethod
    def has_collection(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def create_collection(
        self, collection_name: str, dimension: int = 1024, metric_type: str = "COSINE"
    ) -> bool:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def query_similarity(
        self, collection_name: str, vector: List[float], top_k: int = 5
    ) -> List[VectorQueryResponse]:
        pass

    @abstractmethod
    def upsert_vectors(
        self, collection_name: str, items: List[VectorCreateRequest]
    ) -> bool:
        pass

    @abstractmethod
    def delete_vectors_by_ids(self, collection_name: str, ids: List[Any]) -> bool:
        pass
