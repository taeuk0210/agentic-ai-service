from typing import List, Dict, Any

from app.schemas import LLMChat


class HistoryService:
    def __init__(self):
        pass

    def get_histories(session_id: str) -> List[LLMChat]:
        pass

    def set_histories(session_id: str, chats: List[LLMChat]) -> bool:
        pass


history_service = HistoryService()
