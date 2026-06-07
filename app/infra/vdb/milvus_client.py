from typing import List, Any

from pymilvus import MilvusClient

from app.config import config
from app.logger import logger
from app.schema import VectorCreateRequest, VectorQueryResponse
from app.infra.vdb.interface import BaseVectorDBClient


class MilvusVectorDBClient(BaseVectorDBClient):
    def __init__(self):
        self.client = MilvusClient(
            uri=f"http://{config.MILVUS_HOST}:{config.MILVUS_PORT}",
        )

    def has_collection(self, collection_name: str) -> bool:
        try:
            return self.client.has_collection(collection_name=collection_name)

        except Exception as e:
            logger.error(
                f"MilvusVectorDBClient.has_collection() error ({collection_name}): {e}"
            )
            return False

    def create_collection(
        self, collection_name: str, dimension: int = 1024, metric_type: str = "COSINE"
    ) -> bool:
        try:
            self.client.create_collection(
                collection_name=collection_name,
                dimension=dimension,
                metric_type=metric_type,
                auto_id=False,
                consistency_level="Strong",
            )
            return True

        except Exception as e:
            logger.error(
                f"MilvusVectorDBClient.create_collection() error ({collection_name}): {e}"
            )
            return False

    def delete_collection(self, collection_name: str) -> bool:
        try:
            self.client.drop_collection(collection_name=collection_name)
            return True

        except Exception as e:
            logger.error(
                f"MilvusVectorDBClient.delete_collection() error ({collection_name}): {e}"
            )
            return False

    def query_similarity(
        self, collection_name: str, vector: List[float], top_k: int = 5
    ) -> List[VectorQueryResponse]:
        try:
            response = self.client.search(
                collection_name=collection_name,
                data=[vector],
                limit=top_k,
                output_fields=["*"],
            )

            results = []
            if response and len(response) > 0:
                for hit in response[0]:
                    results.append(VectorQueryResponse(uuid=str(hit.get("id"))))
            return results

        except Exception as e:
            logger.error(
                f"MilvusVectorDBClient.query_similarity() error ({collection_name}): {e}"
            )
            return []

    def upsert_vectors(
        self, collection_name: str, items: List[VectorCreateRequest]
    ) -> bool:
        try:
            data = []
            for item in items:
                record = {"id": item.uuid, "vector": item.vector}
                if item.properties:
                    record.update(item.properties)
                data.append(record)

            self.client.insert(collection_name=collection_name, data=data)
            return True

        except Exception as e:
            logger.error(
                f"MilvusVectorDBClient.upsert_vector() error ({collection_name}): {e}"
            )
            return False

    def delete_vectors_by_ids(self, collection_name: str, ids: List[Any]) -> bool:
        try:
            self.client.delete(collection_name=collection_name, pks=ids)
            return True

        except Exception as e:
            logger.error(
                f"MilvusVectorDBClient.delete_vectors_by_ids() error ({collection_name}): {e}"
            )
            return False


milvus_client = MilvusVectorDBClient()
