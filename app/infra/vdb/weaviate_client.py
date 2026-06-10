from typing import List, Any

import weaviate

from weaviate.classes.config import Configure, VectorDistances
from weaviate.classes.query import MetadataQuery, Filter

from app.config import config
from app.logger import logger
from app.schemas import VectorCreateRequest, VectorQueryResponse
from app.infra.vdb.interface import BaseVectorDBClient


class WeaviateVectorDBClient(BaseVectorDBClient):
    def __init__(self):
        self.client = weaviate.connect_to_local(
            host=config.WEAVIATE_HOST,
            port=config.WEAVIATE_PORT,
            # grpc_port=config.WEAVIATE_GRPC_PORT,
        )

    def has_collection(self, collection_name: str) -> bool:
        try:
            return self.client.collections.exists(name=collection_name)

        except Exception as e:
            logger.error(
                f"WeaviateVectorDBClient.has_collection() error ({collection_name}): {e}"
            )
            return False

    def create_collection(
        self, collection_name: str, dimension: int = 1024, metric_type: str = "COSINE"
    ) -> bool:
        try:
            metric_type = metric_type.lower()
            if metric_type == "l2":
                metric_type = "l2-squared"

            metric_type = VectorDistances[metric_type.upper()]

            self.client.collections.create(
                name=collection_name,
                vector_config=[
                    Configure.Vectors.self_provided(
                        name="custom_vector",
                        vector_index_config=Configure.VectorIndex.hnsw(),
                    ),
                ],
            )
            return True

        except Exception as e:
            logger.error(
                f"WeaviateVectorDBClient.create_collection() error ({collection_name}): {e}"
            )
            return False

    def delete_collection(self, collection_name: str) -> bool:
        try:
            self.client.collections.delete(name=collection_name)
            return True

        except Exception as e:
            logger.error(
                f"WeaviateVectorDBClient.delete_collection() error ({collection_name}): {e}"
            )
            return False

    def query_similarity(
        self, collection_name: str, vector: List[float], top_k: int = 5
    ) -> List[VectorQueryResponse]:
        try:
            collection = self.client.collections.get(collection_name)
            response = collection.query.near_vector(
                near_vector=vector,
                limit=top_k,
                return_metadata=MetadataQuery(distance=True),
            )
            return [VectorQueryResponse(uuid=obj.uuid) for obj in response.objects]

        except Exception as e:
            logger.error(
                f"WeaviateVectorDBClient.query_similarity() error ({collection_name}): {e}"
            )
            return []

    def upsert_vectors(
        self, collection_name: str, items: List[VectorCreateRequest]
    ) -> bool:
        try:
            collection = self.client.collections.get(collection_name)
            with collection.batch.dynamic() as batch:
                for item in items:
                    batch.add_object(
                        properties=item.properties,
                        vector=item.vector,
                        uuid=item.uuid,
                    )
            return True

        except Exception as e:
            logger.error(
                f"WeaviateVectorDBClient.upsert_vector() error ({collection_name}): {e}"
            )
            return False

    def delete_vectors_by_ids(self, collection_name: str, ids: List[Any]) -> bool:
        try:
            collection = self.client.collections.get(collection_name)

            if len(ids) == 1:
                delete_filter = Filter.by_id().equal(ids[0])
            else:
                delete_filter = Filter.by_id().contains_any(ids)

            collection.data.delete_many(where=delete_filter)
            return True

        except Exception as e:
            logger.error(
                f"WeaviateVectorDBClient.upsert_vector() error ({collection_name}): {e}"
            )
            return False


weaviate_client = WeaviateVectorDBClient()
