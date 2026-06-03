from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseIntentService(ABC):
    @abstractmethod
    def route_request(self, user_query: str, allowed_sources: List[str]) -> Dict[str, Any]:
        pass