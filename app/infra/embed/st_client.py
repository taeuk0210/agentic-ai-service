from typing import List

from sentence_transformers import SentenceTransformer

from app.config import config
from app.logger import logger
from app.infra.embed.interface import BaseEmbeddingClient


class StEmbeddingClient(BaseEmbeddingClient):
    def __init__(self):
        self.model = SentenceTransformer(
            model_name_or_path=config.EMBEDDING_MODEL,
            device=config.EMBEDDING_DEVICE,
        )
        logger.info(f"StEmbeddingClient() is initialized.")

    def embedding(self, text: str | List[str]) -> List[float] | List[List[float]]:
        try:
            if isinstance(text, List):
                return self.model.encode(
                    inputs=text, convert_to_numpy=True, normalize_embeddings=True
                )

            return self.model.encode_document(
                inputs=text,
                batch_size=config.EMBEDDING_BATCH,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True,
            ).tolist()

        except Exception as e:
            logger.error(f"StEmbeddingClient.embedding() error: {e}")
            return []


st_client = StEmbeddingClient()
