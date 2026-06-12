from typing import List, Dict, Any

from app.schemas import LLMChat


class AuthService:
    def __init__(self):
        pass

    def validate_user(self, session_id: str) -> Dict[str, Any]:
        pass


auth_service = AuthService()
