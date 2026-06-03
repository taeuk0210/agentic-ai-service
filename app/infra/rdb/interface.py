from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseRepository(ABC):
    @abstractmethod
    def save(self, entity_id: Optional[Any], data: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: Any) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def query(self, filters: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
        pass