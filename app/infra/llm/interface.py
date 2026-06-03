from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseLLMClient(ABC):
    @abstractmethod
    def chat_completion(self):
        pass