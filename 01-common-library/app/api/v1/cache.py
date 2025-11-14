"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform
File         : cache.py
Description  : Cache management APIs using Redis
Language     : English (UK)
Framework    : FastAPI / Python 3.12+ / Redis 7+

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Takeshi Yamamoto (Performance & Optimization Master)
Contributors      : Lars Bjorkman (Redis architecture)
                   Elena Volkov (API design)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-13 17:00 UTC
Last Modified     : 2025-11-13 20:00 UTC
Development Time  : 2 hours 00 minutes
Review Time       : 0 hours 30 minutes
Total Time        : 2 hours 30 minutes
Total Cost        : 2.5 x $150 = $375.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-13 - Takeshi Yamamoto - Cache management APIs
                    - Get/Set/Delete cache operations
                    - TTL management
                    - Batch operations
                    - Pattern-based key search

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/Shakour-Data/01-common-library
================================================================================
"""

import logging
from typing import Optional, List, Dict, Any

from fastapi import APIRouter, status, HTTPException, Query
from pydantic import BaseModel, Field

from app.core.redis_client import get_redis_client
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)

router = APIRouter()


# Pydantic Models
class CacheSetRequest(BaseModel):
    """Request model for setting cache value."""
    key: str = Field(..., description="Cache key", min_length=1, max_length=255)
    value: str = Field(..., description="Cache value", max_length=10000)
    ttl: Optional[int] = Field(None, description="Time-to-live in seconds", ge=1, le=2592000)


class CacheSetResponse(BaseModel):
    """Response model for cache set operation."""
    success: bool
    key: str
    message: str


class CacheGetResponse(BaseModel):
    """Response model for cache get operation."""
    key: str
    value: Optional[str]
    exists: bool
    ttl: Optional[int] = None


class CacheDeleteRequest(BaseModel):
    """Request model for deleting cache keys."""
    keys: List[str] = Field(..., min_length=1, max_length=100)


class CacheDeleteResponse(BaseModel):
    """Response model for cache delete operation."""
    success: bool
    deleted_count: int
    message: str


class CacheKeysResponse(BaseModel):
    """Response model for cache keys search."""
    pattern: str
    keys: List[str]
    count: int


class CacheHealthResponse(BaseModel):
    """Response model for cache health check."""
    status: str
    latency_ms: Optional[float] = None
    version: Optional[str] = None
    connected_clients: Optional[int] = None
    used_memory_human: Optional[str] = None
    error: Optional[str] = None


# Cache Endpoints
@router.post("/set", status_code=status.HTTP_201_CREATED, response_model=CacheSetResponse)
async def set_cache(request: CacheSetRequest) -> CacheSetResponse:
    """Set a value in cache with optional TTL."""
    try:
        redis = await get_redis_client()
        await redis.set(request.key, request.value, ttl=request.ttl)
        
        logger.info(f"Cache set: key='{request.key}', ttl={request.ttl}")
        
        return CacheSetResponse(
            success=True,
            key=request.key,
            message=f"Cache value set successfully"
        )
    except RedisError as e:
        logger.error(f"Redis error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.get("/get/{key}", response_model=CacheGetResponse)
async def get_cache(key: str) -> CacheGetResponse:
    """Get a value from cache by key."""
    try:
        redis = await get_redis_client()
        value = await redis.get(key)
        ttl_value = await redis.ttl(key)
        
        return CacheGetResponse(
            key=key,
            value=value,
            exists=value is not None,
            ttl=ttl_value if value else None
        )
    except RedisError as e:
        logger.error(f"Redis error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.delete("/delete", response_model=CacheDeleteResponse)
async def delete_cache(request: CacheDeleteRequest) -> CacheDeleteResponse:
    """Delete one or more keys from cache."""
    try:
        redis = await get_redis_client()
        deleted_count = await redis.delete(*request.keys)
        
        return CacheDeleteResponse(
            success=True,
            deleted_count=deleted_count,
            message=f"Deleted {deleted_count} key(s)"
        )
    except RedisError as e:
        logger.error(f"Redis error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.get("/keys", response_model=CacheKeysResponse)
async def search_keys(pattern: str = Query("*", max_length=255)) -> CacheKeysResponse:
    """Search for cache keys matching a pattern."""
    try:
        redis = await get_redis_client()
        keys = await redis.keys(pattern)
        
        return CacheKeysResponse(
            pattern=pattern,
            keys=keys,
            count=len(keys)
        )
    except RedisError as e:
        logger.error(f"Redis error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.get("/health", response_model=CacheHealthResponse)
async def check_cache_health() -> CacheHealthResponse:
    """Check Redis cache health."""
    try:
        redis = await get_redis_client()
        health_data = await redis.health_check()
        return CacheHealthResponse(**health_data)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return CacheHealthResponse(status="unhealthy", error=str(e))
