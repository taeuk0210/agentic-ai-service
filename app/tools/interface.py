from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseToolService(ABC):
    @property
    @abstractmethod
    def tool_name(self) -> str:
        pass

    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> str:
        pass