from abc import ABC, abstractmethod
from typing import List

from app.schemas import LLMChat


class BaseLLMClient(ABC):
    @abstractmethod
    def chat_completion(
        self,
        system_prompt: str,
        chat_histories: List[LLMChat],
        user_prompt: str,
    ) -> str:
        pass
