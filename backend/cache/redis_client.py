from redis.asyncio.client import Redis

from config.settings import REDIS_HOST, REDIS_PASSWORD


cache_client = Redis(
    host=REDIS_HOST,
    password=REDIS_PASSWORD
)