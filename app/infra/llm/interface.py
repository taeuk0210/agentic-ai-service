from abc import ABC, abstractmethod


from app.schemas import LLMRequest, LLMResponse


class BaseLLMClient(ABC):
    @abstractmethod
    def generate(
        self,
        req: LLMRequest,
    ) -> LLMResponse:
        pass
