from abc import ABC, abstractmethod
from typing import List, Any

from app.schemas import VectorCollection, VectorItem


class BaseVectorDBClient(ABC):
    @abstractmethod
    def create_collection(self, vector_collection: VectorCollection) -> bool:
        pass

    @abstractmethod
    def delete_collection(self, collection: str) -> bool:
        pass

    @abstractmethod
    def upsert_vectors(self, collection: str, items: List[VectorItem]) -> bool:
        pass

    @abstractmethod
    def query_vectors(
        self, collection: str, items: List[VectorItem], top_k: int
    ) -> List[VectorItem]:
        pass

    @abstractmethod
    def delete_vectors(self, collection: str, ids: List[Any]) -> bool:
        pass
