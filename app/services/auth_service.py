from abc import ABC, abstractmethod
from typing import List, Dict, Any

from app.schemas import LLMChat


@abstractmethod
def validate_user(self, session_id: str) -> Dict[str, Any]:
    pass


@abstractmethod
def validate_content(self, content: str) -> bool:
    pass
