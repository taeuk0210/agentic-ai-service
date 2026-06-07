from abc import ABC, abstractmethod
from typing import List, Dict, Any

from app.schema import LLMChat


class BaseChatService(ABC):
    @abstractmethod
    def validate_user(self, session_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def validate_content(self, content: str) -> bool:
        pass

    @abstractmethod
    def get_chat_histories(session_id: str) -> List[LLMChat]:
        pass

    @abstractmethod
    def set_chat_histories(session_id: str, chats: List[LLMChat]) -> bool:
        pass
