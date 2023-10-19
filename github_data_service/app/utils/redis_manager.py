import redis
import json
from redis.exceptions import RedisError, ConnectionError

from app.config import REDIS_HOST, REDIS_PORT
from app.app_logging import logger

def create_redis_client():
    """
    Create Redis client instance.
    
    Returns:
        redis.Redis or None: Redis client instance if connection is successful, otherwise None.
    """
    try:
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

        # Check if client can connect
        redis_client.ping()
    except (ConnectionError, ConnectionRefusedError) as e:
        logger.error(f"Failed to connect to Redis server. Error: {e}")

        return None
    except RedisError as e:
        logger.error(f"Failed to create Redis client. Error: {e}")

        return None

def get_from_cache(client, key):
    """
    Retrieve data from Redis cache.

    Args:
        client (redis.Redis): Redis client instance.
        key (str): Key to retrieve data from Redis cache.

    Returns:
        dict or None: Decoded JSON data if key exists in cache, otherwise None.
    """
    try:
        cached_data = client.get(key)

        if cached_data:
            return json.loads(cached_data)
        else:
            return None
    except RedisError as e:
        logger.error(f"Failed to get data from cache. Error: {e}")

        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode cached data. Error: {e}")

        return None
    
def set_in_cache(client, key, data, ex):
    """
    Set data in Redis cache.
    
    Args:
        client (redis.Redis): Redis client instance.
        key (str): Key to set data in Redis cache.
        data (dict): Data to set in Redis cache.
        ex (int): Expiration time in seconds.
    """
    try:
        serialized_data = json.dumps(data)
        client.set(key,serialized_data, ex=ex)
    except RedisError as e:
        logger.error(f"Failed to set data in cache. Error: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to encode data to cache. Error: {e}")

def close_redis_client(client):
    """
    Close Redis client connection.
    
    Args:
        client (redis.Redis): Redis client instance.
    """
    try:
        client.close()
    except Exception as e:
        logger.error(f"Failed to close Redis client connection. Error: {e}")