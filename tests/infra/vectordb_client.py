import uuid
import unittest

from app.schemas import VectorCollection, VectorItem
from app.infra.vdb.weaviate_client import weaviate_client


class TestVectorDBClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = weaviate_client
        cls.collection = "testcollection"

    def setUp(self):
        self.client.create_collection(
            VectorCollection(
                collection=self.collection, dimension=1024, metric_type="COSINE"
            )
        )

    def tearDown(self):
        self.client.delete_collection(self.collection)

    def test_collection(self) -> None:
        # given
        temp_collection = "tempcollection"

        # when
        created = self.client.create_collection(
            VectorCollection(
                collection=temp_collection, dimension=1024, metric_type="COSINE"
            )
        )
        deleted = self.client.delete_collection(temp_collection)

        # then
        self.assertTrue(created)
        self.assertTrue(deleted)

    def test_vectors(self) -> None:
        # given
        mock_vector_1 = [0.1] * 1024
        mock_vector_2 = [-0.1] * 1024
        target_uuid_1 = uuid.uuid4()
        target_uuid_2 = uuid.uuid4()
        items = [
            VectorItem(uuid=target_uuid_1, vector=mock_vector_1, properties={}),
            VectorItem(uuid=target_uuid_2, vector=mock_vector_2, properties={}),
        ]

        # when
        upsert_success = self.client.upsert_vectors(self.collection, items)
        query_results = self.client.query_vectors(
            collection=self.collection, items=items, top_k=2
        )

        # then
        self.assertTrue(upsert_success)
        self.assertEqual(len(query_results), 2)
        self.assertEqual(query_results[0].uuid, target_uuid_1)

    def test_delete_vectors_by_ids(self) -> None:
        # given
        mock_vector = [0.05] * 1024
        target_uuid_1 = uuid.uuid4()
        target_uuid_2 = uuid.uuid4()
        items = [
            VectorItem(uuid=target_uuid_1, vector=mock_vector, properties={}),
            VectorItem(uuid=target_uuid_2, vector=mock_vector, properties={}),
        ]
        self.client.upsert_vectors(self.collection, items)

        # when
        deleted = self.client.delete_vectors(
            self.collection, [target_uuid_1, target_uuid_2]
        )

        # then
        self.assertTrue(deleted)


if __name__ == "__main__":
    unittest.main()
