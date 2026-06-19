from typing import List, Any

import weaviate

from weaviate.classes.config import Configure, VectorDistances
from weaviate.classes.query import MetadataQuery, Filter

from app.config import config
from app.logger import logger
from app.schemas import VectorCollection, VectorItem
from app.infra.vdb.interface import BaseVectorDBClient


class WeaviateVectorDBClient(BaseVectorDBClient):
    def __init__(self):
        self.client = weaviate.connect_to_local(
            host=config.WEAVIATE_HOST,
            port=config.WEAVIATE_PORT,
            # grpc_port=config.WEAVIATE_GRPC_PORT,
        )
        logger.info(f"WeaviateVectorDBClient is initialized.")

    def create_collection(self, vector_collection: VectorCollection) -> bool:
        try:
            is_exist = self.client.collections.exists(name=vector_collection.collection)
            if is_exist:
                logger.error(
                    f"WeaviateVectorDBClient.create_collection() error: {vector_collection.collection} is already exist"
                )
                return False

            metric_type = vector_collection.metric_type.lower()
            if metric_type == "l2":
                metric_type = "l2-squared"

            metric_type = VectorDistances[metric_type.upper()]

            self.client.collections.create(
                name=vector_collection.collection,
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
                f"WeaviateVectorDBClient.create_collection() error ({vector_collection.collection}): {e}"
            )
            return False

    def delete_collection(self, collection: str) -> bool:
        try:
            self.client.collections.delete(name=collection)
            return True

        except Exception as e:
            logger.error(
                f"WeaviateVectorDBClient.delete_collection() error ({collection}): {e}"
            )
            return False

    def upsert_vectors(self, collection: str, items: List[VectorItem]) -> bool:
        try:
            collection = self.client.collections.get(collection)
            with collection.batch.dynamic() as batch:
                for item in items:
                    batch.add_object(
                        uuid=item.uuid,
                        vector=item.vector,
                        properties=item.properties,
                    )
            return True

        except Exception as e:
            logger.error(
                f"WeaviateVectorDBClient.upsert_vector() error ({collection}): {e}"
            )
            return False

    def query_vectors(
        self, collection: str, items: List[VectorItem], top_k: int = 5
    ) -> List[VectorItem]:
        try:
            vc = self.client.collections.get(collection)
            all_objects = []
            for item in items:
                all_objects.extend(
                    vc.query.near_vector(
                        near_vector=item.vector,
                        limit=top_k,
                        return_properties=True,
                        return_metadata=MetadataQuery(distance=True),
                    ).objects
                )
            unique_objects = {}
            for obj in all_objects:
                unique_objects[obj.uuid] = obj

            return [
                VectorItem(
                    uuid=obj.uuid,
                    vector=[],
                    properties=obj.properties,
                )
                for obj in list(unique_objects.values())[:top_k]
            ]

        except Exception as e:
            logger.error(
                f"WeaviateVectorDBClient.query_vectors() error ({collection}): {e}"
            )
            return []

    def delete_vectors(self, collection: str, ids: List[Any]) -> bool:
        try:
            collection = self.client.collections.get(collection)

            if len(ids) == 1:
                delete_filter = Filter.by_id().equal(ids[0])
            else:
                delete_filter = Filter.by_id().contains_any(ids)

            collection.data.delete_many(where=delete_filter)
            return True

        except Exception as e:
            logger.error(
                f"WeaviateVectorDBClient.upsert_vector() error ({collection}): {e}"
            )
            return False


weaviate_client = WeaviateVectorDBClient()
