from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddingClient(ABC):
    @abstractmethod
    def embedding(self, text: str | List[str]) -> List[float] | List[List[float]]:
        pass
