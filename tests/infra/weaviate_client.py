import uuid
import unittest

from app.schemas import VectorCreateRequest, VectorQueryResponse
from app.infra.vdb.weaviate_client import weaviate_client


class TestWeaviateVectorDBClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = weaviate_client
        cls.test_collection_name = "testcollection"

    def setUp(self):
        if self.client.has_collection(self.test_collection_name):
            self.client.delete_collection(self.test_collection_name)

        self.client.create_collection(collection_name=self.test_collection_name)

    def tearDown(self):
        if self.client.has_collection(self.test_collection_name):
            self.client.delete_collection(self.test_collection_name)

    def test_collection_lifecycle(self) -> None:
        # given
        temp_collection = "tempcollection"
        if self.client.has_collection(temp_collection):
            self.client.delete_collection(temp_collection)

        # when
        create_success = self.client.create_collection(temp_collection)
        is_created = self.client.has_collection(temp_collection)
        delete_success = self.client.delete_collection(temp_collection)
        is_lived = self.client.has_collection(temp_collection)

        # then
        self.assertTrue(create_success)
        self.assertTrue(is_created)
        self.assertTrue(delete_success)
        self.assertFalse(is_lived)

    def test_upsert_and_query_similarity(self) -> None:
        # given
        mock_vector_1 = [0.1] * 1024
        mock_vector_2 = [-0.1] * 1024
        target_uuid_1 = uuid.uuid4()
        target_uuid_2 = uuid.uuid4()
        items = [
            VectorCreateRequest(uuid=target_uuid_1, vector=mock_vector_1),
            VectorCreateRequest(uuid=target_uuid_2, vector=mock_vector_2),
        ]

        # when (1): 데이터 적재(Upsert)
        upsert_success = self.client.upsert_vectors(self.test_collection_name, items)
        query_results = self.client.query_similarity(
            collection_name=self.test_collection_name, vector=mock_vector_1, top_k=2
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
            VectorCreateRequest(uuid=target_uuid_1, vector=mock_vector),
            VectorCreateRequest(uuid=target_uuid_2, vector=mock_vector),
        ]
        self.client.upsert_vectors(self.test_collection_name, items)

        # when
        delete_success = self.client.delete_vectors_by_ids(
            self.test_collection_name, [target_uuid_1, target_uuid_2]
        )
        remain_results = self.client.query_similarity(
            self.test_collection_name, mock_vector, top_k=2
        )

        # then
        self.assertTrue(delete_success)
        self.assertEqual(len(remain_results), 0)


if __name__ == "__main__":
    unittest.main()
