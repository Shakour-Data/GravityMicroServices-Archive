"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : test_rate_limiter.py
Description  : Tests for Rate Limiter
Language     : English (UK)
Framework    : FastAPI / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
================================================================================
Primary Author    : João Silva (QA & Testing Lead)
Contributors      : Lars Björkman, Elena Volkov
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT (زمان‌بندی و تلاش)
================================================================================
Created Date      : 2025-11-05 14:00 UTC
Last Modified     : 2025-11-06 16:45 UTC
Development Time  : 2 hours 30 minutes
Review Time       : 0 hours 45 minutes
Testing Time      : 2 hours 0 minutes
Total Time        : 5 hours 15 minutes

================================================================================
COST CALCULATION (محاسبه هزینه)
================================================================================
Hourly Rate       : $150/hour (Elite Engineer Standard)
Development Cost  : 2.5 × $150 = $375.00 USD
Review Cost       : 0.75 × $150 = $112.50 USD
Testing Cost      : 2.0 × $150 = $300.00 USD
Total Cost        : $787.50 USD

================================================================================
VERSION HISTORY (تاریخچه نسخه)
================================================================================
v1.0.0 - 2025-11-05 - João Silva - Initial implementation
v1.0.1 - 2025-11-06 - João Silva - Added file header standard

================================================================================
DEPENDENCIES (وابستگی‌ها)
================================================================================
Internal  : gravity_common (where applicable)
External  : FastAPI, SQLAlchemy, Pydantic (as needed)
Database  : PostgreSQL 16+, Redis 7 (as needed)

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/GravityMicroServices

================================================================================
"""

import pytest
from datetime import datetime
from redis.asyncio import Redis

from app.core.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_rate_limiter_allow_request():
    """Test rate limiter allows requests within limit"""
    # Create Redis client for testing
    redis = Redis.from_url("redis://localhost:6379/1", decode_responses=True)
    
    limiter = RateLimiter(redis, requests_per_minute=10)
    
    # First request should be allowed
    allowed = await limiter.is_allowed("test-key")
    assert allowed is True
    
    # Cleanup
    await redis.close()


@pytest.mark.asyncio
async def test_rate_limiter_blocks_excessive_requests():
    """Test rate limiter blocks requests exceeding limit"""
    redis = Redis.from_url("redis://localhost:6379/1", decode_responses=True)
    
    # Low limit for testing
    limiter = RateLimiter(redis, requests_per_minute=3)
    
    # Make requests up to limit
    for i in range(3):
        allowed = await limiter.is_allowed("test-key-block")
        assert allowed is True
    
    # Next request should be blocked
    allowed = await limiter.is_allowed("test-key-block")
    assert allowed is False
    
    # Cleanup
    await redis.aclose()


@pytest.mark.asyncio
async def test_rate_limiter_different_keys():
    """Test rate limiter handles different keys independently"""
    redis = Redis.from_url("redis://localhost:6379/1", decode_responses=True)
    
    limiter = RateLimiter(redis, requests_per_minute=5)
    
    # Requests with different keys should be independent
    allowed1 = await limiter.is_allowed("key1")
    allowed2 = await limiter.is_allowed("key2")
    
    assert allowed1 is True
    assert allowed2 is True
    
    await redis.aclose()


@pytest.mark.asyncio
async def test_get_rate_limit_info():
    """Test getting rate limit information"""
    redis = Redis.from_url("redis://localhost:6379/1", decode_responses=True)
    
    limiter = RateLimiter(redis, requests_per_minute=10)
    
    # Make a request
    await limiter.is_allowed("info-key")
    
    # Get info
    info = await limiter.get_rate_limit_info("info-key")
    
    assert info["limit"] == 10
    assert info["remaining"] == 9
    assert "reset_at" in info
    
    await redis.aclose()
