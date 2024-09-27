import aioredis

from src.config import REDIS_URL


redis_client = aioredis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=1)


async def get_redis_client():
    try:
        await redis_client.ping()
        return redis_client
    except:
        return None