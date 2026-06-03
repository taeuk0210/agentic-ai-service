from abc import ABC, abstractmethod
from typing import Tuple

class BaseGuardrailService(ABC):
    @abstractmethod
    def validate_input(self, user_query: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def validate_output(self, llm_response: str) -> Tuple[bool, str]:
        pass