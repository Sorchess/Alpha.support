from dataclasses import dataclass

from pydantic import RedisDsn
from redis.asyncio import Redis


@dataclass
class RedisClientFactory:
    url: RedisDsn

    def get_client(self, db_index: int) -> Redis:
        base_url = str(self.url).rstrip("/0123456789")
        return Redis.from_url(
            url=f"{base_url}/{db_index}",
            decode_responses=True,
        )
