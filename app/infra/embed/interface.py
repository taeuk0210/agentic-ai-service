from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddingClient(ABC):
    @abstractmethod
    def embedding(self, text: str) -> List[float]:
        pass

    @abstractmethod
    def batch_embedding(self, texts: List[str]) -> List[List[float]]:
        pass
