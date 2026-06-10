from abc import ABC, abstractmethod
from typing import List, Dict, Any

from app.schemas import LLMChat


@abstractmethod
def get_chat_histories(session_id: str) -> List[LLMChat]:
    pass


@abstractmethod
def set_chat_histories(session_id: str, chats: List[LLMChat]) -> bool:
    pass
