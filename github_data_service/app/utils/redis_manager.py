import redis

from config import REDIS_HOST, REDIS_PORT
from app_logging import logger

def create_redis_client():
    """
    Creates a redis client and returns it.
    
    Returns:
        redis.Redis: A redis client.
    """
    try:
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

        return redis_client
    except Exception as e:
        logger.error(f"Failed to create redis client. Error: {e}")

        return None
