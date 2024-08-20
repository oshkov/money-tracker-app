import aioredis
from src.config import REDIS_URL


redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)


async def get_redis_client():
    return redis_client