import json
from typing import Any

from aioredis import Redis

from core.config import settings


class CacheService:

    def __init__(self, redis: Redis):
        self._redis = redis

    async def set_value(self, key: str, data: Any):
        json_data = json.dumps(data)
        return await self._redis.set(
            key=key,
            value=json_data,
            expire=settings.EXPIRE,
        )

    async def get_value(self, key_name: str) -> Any:
        if cache := await self._redis.get(key_name):
            return json.loads(cache)
        return None
