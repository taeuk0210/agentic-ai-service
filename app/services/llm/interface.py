from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseLLMService(ABC):
    @abstractmethod
    def route_user_intent(
        self,
        user_input: str,
        accessible_collections: List[str],
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def request_user_input(
        self,
        user_input: str,
        tool_contexts: List[Dict[str, Any]],
    ) -> str:
        pass
