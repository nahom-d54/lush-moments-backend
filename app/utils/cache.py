import json
import os
from typing import Any, Optional

import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Global Redis client
redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """Get Redis client instance"""
    global redis_client
    if redis_client is None:
        redis_client = await redis.from_url(REDIS_URL, decode_responses=True)
    return redis_client


async def close_redis():
    """Close Redis connection"""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


async def get_cached(key: str) -> Optional[Any]:
    """
    Get value from cache

    Args:
        key: Cache key

    Returns:
        Cached value or None if not found
    """
    try:
        client = await get_redis()
        value = await client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"Cache get error: {e}")
        return None


async def set_cached(key: str, value: Any, expire: int = 300) -> bool:
    """
    Set value in cache

    Args:
        key: Cache key
        value: Value to cache
        expire: Expiration time in seconds (default: 5 minutes)

    Returns:
        True if successful, False otherwise
    """
    try:
        client = await get_redis()
        await client.setex(key, expire, json.dumps(value))
        return True
    except Exception as e:
        print(f"Cache set error: {e}")
        return False


async def delete_cached(key: str) -> bool:
    """
    Delete value from cache

    Args:
        key: Cache key

    Returns:
        True if successful, False otherwise
    """
    try:
        client = await get_redis()
        await client.delete(key)
        return True
    except Exception as e:
        print(f"Cache delete error: {e}")
        return False


async def clear_pattern(pattern: str) -> bool:
    """
    Clear all keys matching a pattern

    Args:
        pattern: Key pattern (e.g., "packages:*")

    Returns:
        True if successful, False otherwise
    """
    try:
        client = await get_redis()
        keys = await client.keys(pattern)
        if keys:
            await client.delete(*keys)
        return True
    except Exception as e:
        print(f"Cache clear error: {e}")
        return False
