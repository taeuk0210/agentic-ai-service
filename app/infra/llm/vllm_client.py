from typing import List

from openai import OpenAI

from app.config import config
from app.logger import logger
from app.infra.llm.interface import BaseLLMClient
from app.schemas import LLMChat


class VLLMClient(BaseLLMClient):
    def __init__(self):
        self.client = OpenAI(
            base_url=f"http://{config.VLLM_HOST}:{config.VLLM_PORT}/v1",
            api_key=config.VLLM_API_KEY,
            timeout=config.VLLM_TIMEOUT,
        )

    def chat_completion(
        self,
        system_prompt: str,
        chat_histories: List[LLMChat],
        user_prompt: str,
    ) -> str:
        try:
            response = self.client.chat.completions.create(
                model=config.VLLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *[h.model_dump() for h in chat_histories],
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
            )
            return response.choices[0].message

        except Exception as e:
            logger.error(f"VLLMClient.chat_completion() error: {e}")
        return


vllm_client = VLLMClient()
