"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform
File         : mock_redis.py
Description  : Mock Redis client for development/testing without Docker
Language     : English (UK)
Framework    : Python 3.12+

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Lars Björkman (DevOps & Cloud Infrastructure Lead)
Contributors      : Takeshi Yamamoto (Performance)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-13 17:30 UTC
Last Modified     : 2025-11-13 18:00 UTC
Development Time  : 0 hours 30 minutes
Total Cost        : 0.5 × $150 = $75.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-13 - Lars Björkman - Mock Redis for testing without Docker

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/Shakour-Data/01-common-library
================================================================================
"""

import logging
import time
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class MockRedisClient:
    """
    Mock Redis client for development/testing without Docker.
    
    This is an in-memory implementation that mimics basic Redis operations.
    Use for development when Docker is not available.
    
    Features:
        - In-memory key-value storage
        - TTL support (simulated)
        - Same API as real RedisClient
        - Health checks
    
    Warning:
        - Data is lost on restart
        - Not thread-safe
        - No persistence
        - For development only!
    """
    
    def __init__(self):
        """Initialize mock Redis client."""
        self._store: Dict[str, Any] = {}
        self._ttls: Dict[str, float] = {}  # key -> expiration timestamp
        self._connected: bool = False
        
        logger.info("📦 MockRedisClient initialized (in-memory)")
    
    async def connect(self) -> None:
        """Simulate connection to Redis."""
        if self._connected:
            logger.warning("⚠️ Mock Redis already connected")
            return
        
        logger.info("🔌 Mock Redis connecting (in-memory mode)")
        self._connected = True
        logger.info("✅ Mock Redis connected (in-memory)")
    
    async def close(self) -> None:
        """Simulate closing Redis connection."""
        if not self._connected:
            return
        
        logger.info("🔌 Closing Mock Redis connection")
        self._connected = False
        logger.info("✅ Mock Redis connection closed")
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check."""
        if not self._connected:
            return {
                "status": "unhealthy",
                "error": "Not connected to Mock Redis"
            }
        
        return {
            "status": "healthy",
            "latency_ms": 0.1,
            "version": "mock-1.0.0",
            "connected_clients": 1,
            "used_memory_human": f"{len(self._store)} keys",
            "uptime_in_seconds": 0
        }
    
    def _cleanup_expired(self):
        """Remove expired keys."""
        current_time = time.time()
        expired_keys = [
            key for key, expiration in self._ttls.items()
            if expiration < current_time
        ]
        
        for key in expired_keys:
            if key in self._store:
                del self._store[key]
            del self._ttls[key]
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Set a value with optional TTL."""
        if not self._connected:
            raise ConnectionError("Not connected to Mock Redis")
        
        self._cleanup_expired()
        
        self._store[key] = str(value)
        
        if ttl:
            self._ttls[key] = time.time() + ttl
        elif key in self._ttls:
            del self._ttls[key]
        
        logger.debug(f"✅ Mock Redis SET: key='{key}', ttl={ttl}")
        return True
    
    async def get(self, key: str) -> Optional[str]:
        """Get a value."""
        if not self._connected:
            raise ConnectionError("Not connected to Mock Redis")
        
        self._cleanup_expired()
        
        value = self._store.get(key)
        logger.debug(f"✅ Mock Redis GET: key='{key}', found={value is not None}")
        return value
    
    async def delete(self, *keys: str) -> int:
        """Delete one or more keys."""
        if not self._connected:
            raise ConnectionError("Not connected to Mock Redis")
        
        self._cleanup_expired()
        
        count = 0
        for key in keys:
            if key in self._store:
                del self._store[key]
                count += 1
            if key in self._ttls:
                del self._ttls[key]
        
        logger.debug(f"✅ Mock Redis DELETE: deleted {count} key(s)")
        return count
    
    async def exists(self, *keys: str) -> int:
        """Check if keys exist."""
        if not self._connected:
            raise ConnectionError("Not connected to Mock Redis")
        
        self._cleanup_expired()
        
        count = sum(1 for key in keys if key in self._store)
        return count
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set TTL on a key."""
        if not self._connected:
            raise ConnectionError("Not connected to Mock Redis")
        
        self._cleanup_expired()
        
        if key not in self._store:
            return False
        
        self._ttls[key] = time.time() + seconds
        logger.debug(f"✅ Mock Redis EXPIRE: key='{key}', seconds={seconds}")
        return True
    
    async def ttl(self, key: str) -> int:
        """Get remaining TTL of a key."""
        if not self._connected:
            raise ConnectionError("Not connected to Mock Redis")
        
        self._cleanup_expired()
        
        if key not in self._store:
            return -2  # Key doesn't exist
        
        if key not in self._ttls:
            return -1  # Key exists but has no TTL
        
        remaining = int(self._ttls[key] - time.time())
        return max(0, remaining)
    
    async def keys(self, pattern: str = "*") -> list:
        """Get all keys matching a pattern."""
        if not self._connected:
            raise ConnectionError("Not connected to Mock Redis")
        
        self._cleanup_expired()
        
        # Simple pattern matching (* and ?)
        import fnmatch
        
        matching_keys = [
            key for key in self._store.keys()
            if fnmatch.fnmatch(key, pattern)
        ]
        
        logger.debug(f"✅ Mock Redis KEYS: pattern='{pattern}', found={len(matching_keys)}")
        return matching_keys
    
    async def flushdb(self) -> bool:
        """Delete all keys."""
        if not self._connected:
            raise ConnectionError("Not connected to Mock Redis")
        
        logger.warning("⚠️ Mock Redis FLUSHDB")
        self._store.clear()
        self._ttls.clear()
        return True
    
    async def incr(self, key: str, amount: int = 1) -> int:
        """Increment a key's value."""
        if not self._connected:
            raise ConnectionError("Not connected to Mock Redis")
        
        self._cleanup_expired()
        
        current = int(self._store.get(key, 0))
        new_value = current + amount
        self._store[key] = str(new_value)
        
        logger.debug(f"✅ Mock Redis INCR: key='{key}', amount={amount}, new_value={new_value}")
        return new_value
    
    async def decr(self, key: str, amount: int = 1) -> int:
        """Decrement a key's value."""
        if not self._connected:
            raise ConnectionError("Not connected to Mock Redis")
        
        self._cleanup_expired()
        
        current = int(self._store.get(key, 0))
        new_value = current - amount
        self._store[key] = str(new_value)
        
        logger.debug(f"✅ Mock Redis DECR: key='{key}', amount={amount}, new_value={new_value}")
        return new_value
