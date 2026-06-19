from typing import List, Dict, Any

from app.schemas import Message


class MessageService:
    def __init__(self):
        pass

    def get_message(message_key: str) -> List[Message]:
        pass

    def set_message(message_key: str, messages: List[Message]) -> bool:
        pass


history_service = MessageService()
