from abc import ABC, abstractmethod
from typing import List

class BaseAuthService(ABC):
    @abstractmethod
    def verify_access(self, user_id: str, required_permission: str) -> bool:
        pass

    @abstractmethod
    def get_accessible_knowledge_sources(self, user_id: str) -> List[str]:
        pass