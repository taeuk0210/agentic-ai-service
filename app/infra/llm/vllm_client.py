import time

from openai import OpenAI

from app.config import config
from app.logger import logger
from app.infra.llm.interface import BaseLLMClient
from app.schemas import LLMRequest, LLMResponse


class VLLMClient(BaseLLMClient):
    def __init__(self):
        self.client = OpenAI(
            base_url=f"http://{config.VLLM_HOST}:{config.VLLM_PORT}/v1",
            api_key=config.VLLM_API_KEY,
            timeout=config.VLLM_TIMEOUT,
        )

    def generate(self, req: LLMRequest) -> LLMResponse:
        try:
            t0 = time.perf_counter()
            response = self.client.chat.completions.create(
                model=config.VLLM_MODEL,
                messages=[
                    {"role": "system", "content": req.system_prompt},
                    *[h.model_dump() for h in req.messages],
                    {"role": "user", "content": req.user_prompt},
                ],
                temperature=req.temperature,
            )
            t1 = time.perf_counter()
            return LLMResponse(
                message=response.choices[0].message,
                latency=t1 - t0,
                prompt_token=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
            )

        except Exception as e:
            logger.error(f"VLLMClient.generate() error: {e}")
        return


vllm_client = VLLMClient()
