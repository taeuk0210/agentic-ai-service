from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseVectorDBClient(ABC):
    @abstractmethod
    def query_similarity(self, collection_name: str, vector: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def upsert_vectors(self, collection_name: str, items: List[Dict[str, Any]]) -> bool:
        pass