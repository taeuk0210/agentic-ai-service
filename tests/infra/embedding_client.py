import unittest

from app.infra.embed.st_client import st_client


class TestEmbeddingClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = st_client

    def test_embedding(self) -> None:
        # given
        test_text = "this is test sentence."

        # when
        embedding = self.client.embedding(test_text)

        # then
        self.assertGreater(len(embedding), 0)

    def test_embedding_batch(self) -> None:
        # given
        test_texts = [
            "this is test sentence1.",
            "this is test sentence2.",
            "this is test sentence3.",
        ]

        # when
        embeddings = self.client.embedding(test_texts)

        # then
        self.assertEqual(len(test_texts), len(embeddings))


if __name__ == "__main__":
    unittest.main()
