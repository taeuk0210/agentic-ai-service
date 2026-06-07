from typing import List

from sentence_transformers import SentenceTransformer

from app.config import config
from app.logger import logger
from app.infra.embed.interface import BaseEmbeddingClient


class SentenceTransformersEmbeddingClient(BaseEmbeddingClient):
    def __init__(self):
        self.model = SentenceTransformer(
            model_name_or_path=config.EMBEDDING_MODEL,
            device=config.EMBEDDING_DEVICE,
        )
        logger.info(f"SentenceTransformersEmbeddingClient() is initialized.")

    def embedding(self, text: str) -> List[float]:
        try:
            embedding = self.model.encode(
                inputs=text, convert_to_numpy=True, normalize_embeddings=True
            )
            return embedding.tolist()
        except Exception as e:
            logger.error(f"SentenceTransformersEmbeddingClient.embedding() error: {e}")
            return []

    def batch_embedding(self, texts: List[str]) -> List[List[float]]:
        try:
            embeddings = self.model.encode_document(
                inputs=texts,
                batch_size=config.EMBEDDING_BATCH,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True,
            )
            return embeddings.tolist()
        except Exception as e:
            logger.error(
                f"SentenceTransformersEmbeddingClient.batch_embedding() error: {e}"
            )
            return []


st_client = SentenceTransformersEmbeddingClient()
