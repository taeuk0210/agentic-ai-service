from abc import ABC, abstractmethod

from app.schemas import UserRequest, UserResponse


class BaseChatService(ABC):
    @abstractmethod
    def chat(self, req: UserRequest) -> UserResponse:
        pass
