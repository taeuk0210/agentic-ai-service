from typing import Optional

import redis

from app.config import config
from app.logger import logger
from app.infra.cache.interface import BaseCacheClient


class RedisCacheClient(BaseCacheClient):
    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            password=config.REDIS_PASSWORD,
            decode_responses=True,
        )
        self.client = redis.Redis(connection_pool=self.pool)
        logger.info(f"RedisCacheClient() is initialized.")

    def get(self, key: str) -> Optional[str]:
        try:
            value = self.client.get(key)
            return value
        except redis.RedisError as e:
            logger.error(f"RedisCacheClient.get() error (key: {key}): {e}")
            return None

    def set(self, key: str, value: str, ttl_seconds: Optional[int] = None) -> bool:
        try:
            if ttl_seconds:
                self.client.set(name=key, value=value, ex=ttl_seconds)
            else:
                self.client.set(name=key, value=value)
            return True
        except redis.RedisError as e:
            logger.error(f"RedisCacheClient.set() error (key: {key}): {e}")
            return False

    def delete(self, key: str) -> bool:
        try:
            result = self.client.delete(key)
            return result > 0
        except redis.RedisError as e:
            logger.error(f"RedisCacheClient.delete() error (key: {key}): {e}")
            return False


redis_client = RedisCacheClient()
