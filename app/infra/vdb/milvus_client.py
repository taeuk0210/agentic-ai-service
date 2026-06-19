from typing import List, Any

from pymilvus import MilvusClient

from app.config import config
from app.logger import logger
from app.schemas import VectorItem, VectorCollection
from app.infra.vdb.interface import BaseVectorDBClient


class MilvusVectorDBClient(BaseVectorDBClient):
    def __init__(self):
        self.client = MilvusClient(
            uri=f"http://{config.MILVUS_HOST}:{config.MILVUS_PORT}",
        )

    def create_collection(self, vector_collection: VectorCollection) -> bool:
        try:
            self.client.create_collection(
                collection_name=vector_collection.collection,
                dimension=vector_collection.dimension,
                metric_type=vector_collection.metric_type,
                auto_id=False,
                consistency_level="Strong",
            )
            return True

        except Exception as e:
            logger.error(
                f"MilvusVectorDBClient.create_collection() error ({vector_collection.collection}): {e}"
            )
            return False

    def delete_collection(self, collection: str) -> bool:
        try:
            self.client.drop_collection(collection_name=collection)
            return True

        except Exception as e:
            logger.error(
                f"MilvusVectorDBClient.delete_collection() error ({collection}): {e}"
            )
            return False

    def upsert_vectors(self, collection: str, items: List[VectorItem]) -> bool:
        try:
            data = []
            for item in items:
                record = {"id": item.uuid, "vector": item.vector}
                if item.properties:
                    record.update(item.properties)
                data.append(record)

            self.client.insert(collection_name=collection, data=data)
            return True

        except Exception as e:
            logger.error(
                f"MilvusVectorDBClient.upsert_vector() error ({collection}): {e}"
            )
            return False

    def query_vectors(
        self, collection: str, items: List[VectorItem], top_k: int = 5
    ) -> List[VectorItem]:
        try:
            response = self.client.search(
                collection_name=collection,
                data=[item.model_dump() for item in items],
                limit=top_k,
                output_fields=["*"],
            )

            results = []
            if response and len(response) > 0:
                for hit in response[0]:
                    results.append(VectorItem(uuid=str(hit.get("id"))))
            return results

        except Exception as e:
            logger.error(
                f"MilvusVectorDBClient.query_similarity() error ({collection}): {e}"
            )
            return []

    def delete_vectors(self, collection: str, ids: List[Any]) -> bool:
        try:
            self.client.delete(collection_name=collection, pks=ids)
            return True

        except Exception as e:
            logger.error(
                f"MilvusVectorDBClient.delete_vectors_by_ids() error ({collection}): {e}"
            )
            return False


milvus_client = MilvusVectorDBClient()
