import time
import unittest

from app.infra.cache.redis_client import redis_client


class TestRedisCacheClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = redis_client

    def test_set_get_delete(self) -> None:
        # given
        testkey = "testkey:setandget"
        testvalue = "{'user_id': '12345', 'role': 'user'}"

        # when
        is_set_success = self.client.set(testkey, testvalue)
        cached_value = self.client.get(testkey)
        is_delete_success = self.client.delete(testkey)
        deleted_value = self.client.get(testkey)

        # then
        self.assertTrue(is_set_success)
        self.assertEqual(cached_value, testvalue)
        self.assertTrue(is_delete_success)
        self.assertIsNone(deleted_value)

    def test_ttl_expiration(self) -> None:
        # given
        ttl_key = "testkey:ttl"
        ttl_value = "temporary_value"

        # when
        self.client.set(ttl_key, ttl_value, ttl_seconds=2)
        unexpired_value = self.client.get(ttl_key)
        time.sleep(3)
        expired_value = self.client.get(ttl_key)

        # then
        self.assertEqual(unexpired_value, ttl_value)
        self.assertIsNone(expired_value)


if __name__ == "__main__":
    unittest.main()
