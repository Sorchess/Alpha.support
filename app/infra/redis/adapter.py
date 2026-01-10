import json
from dataclasses import dataclass
from redis.asyncio import Redis


@dataclass
class RedisAdapter:
    redis: Redis
    namespace: str

    async def hset(self, key: str, values: any, expire: int | None = None):
        await self.redis.hset(
            name=f"{self.namespace}:{key}",
            mapping=values,
        )
        await self.redis.expire(
            name=f"{self.namespace}:{key}",
            time=expire,
        )

    async def hget(self, key: str, attr: str):
        await self.redis.hget(
            name=f"{self.namespace}:{key}",
            key=attr,
        )

    async def hgetall(self, key: str):
        data = await self.redis.hgetall(
            name=f"{self.namespace}:{key}",
        )
        return data

    async def set(self, key: str, value: any, expire: int | None = None):
        await self.redis.set(
            name=f"{self.namespace}:{key}",
            value=json.dumps(value),
            ex=expire,
        )

    async def decr(self, key: str):
        await self.redis.decr(
            name=f"{self.namespace}:{key}",
        )

    async def get(self, key: str):
        data = await self.redis.get(
            name=f"{self.namespace}:{key}",
        )
        return json.loads(data) if data else None

    async def delete(self, key: str):
        await self.redis.delete(
            f"{self.namespace}:{key}",
        )

    async def exists(self, key: str) -> bool:
        return await self.redis.exists(
            f"{self.namespace}:{key}",
        )
