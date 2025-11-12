"""
Redis Client Configuration
"""

from typing import Optional

from redis.asyncio import Redis

from app.config import settings

# Global Redis client instance
_redis_client: Optional[Redis] = None


async def init_redis() -> Redis:
    """
    Initialize Redis client

    Returns:
        Redis client instance
    """
    global _redis_client

    _redis_client = Redis.from_url(
        settings.REDIS_URL,
        max_connections=settings.REDIS_MAX_CONNECTIONS,
        socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
        socket_connect_timeout=settings.REDIS_SOCKET_TIMEOUT,
        decode_responses=True,
        encoding="utf-8",
    )

    # Test connection
    await _redis_client.execute_command("PING")

    return _redis_client


async def get_redis_client() -> Redis:
    """
    Get Redis client instance

    Returns:
        Redis client

    Raises:
        RuntimeError: If Redis client is not initialized
    """
    if _redis_client is None:
        raise RuntimeError("Redis client is not initialized. Call init_redis() first.")
    return _redis_client


async def close_redis() -> None:
    """Close Redis connection"""
    if _redis_client:
        await _redis_client.close()


# Cache decorator
def cache(ttl: int = settings.CACHE_TTL):
    """
    Decorator to cache function results in Redis

    Args:
        ttl: Time to live in seconds

    Example:
        @cache(ttl=300)
        async def get_user(user_id: int):
            return await db.get(User, user_id)
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            if not settings.CACHE_ENABLED:
                return await func(*args, **kwargs)

            # Generate cache key
            cache_key = f"{func.__name__}:{args}:{kwargs}"

            # Try to get from cache
            redis_client = await get_redis_client()
            cached_value = await redis_client.get(cache_key)

            if cached_value:
                import json

                return json.loads(cached_value)

            # Call function and cache result
            result = await func(*args, **kwargs)

            import json

            await redis_client.setex(cache_key, ttl, json.dumps(result))

            return result

        return wrapper

    return decorator


async def invalidate_cache(pattern: str) -> int:
    """
    Invalidate cache keys matching pattern

    Args:
        pattern: Redis key pattern (e.g., "user:*")

    Returns:
        Number of keys deleted
    """
    redis_client = await get_redis_client()
    keys = await redis_client.keys(pattern)

    if keys:
        return await redis_client.delete(*keys)

    return 0
