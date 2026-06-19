from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTool(ABC):
    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        pass
