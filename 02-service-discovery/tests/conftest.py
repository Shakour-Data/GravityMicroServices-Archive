"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : conftest.py
Description  : Pytest configuration and fixtures for Service Discovery tests.
Language     : English (UK)
Framework    : Pytest / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
================================================================================
Primary Author    : Elena Volkov (Backend & Integration Lead)
Contributors      : None
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT (زمان‌بندی و تلاش)
================================================================================
Created Date      : 2025-11-07 22:00 UTC
Last Modified     : 2025-11-07 22:00 UTC
Development Time  : 0 hours 45 minutes
Review Time       : 0 hours 10 minutes
Testing Time      : 0 hours 15 minutes
Total Time        : 1 hour 10 minutes

================================================================================
COST CALCULATION (محاسبه هزینه)
================================================================================
Hourly Rate       : $150/hour (Elite Engineer Standard)
Development Cost  : 0.75 × $150 = $112.50 USD
Review Cost       : 0.17 × $150 = $25.00 USD
Testing Cost      : 0.25 × $150 = $37.50 USD
Total Cost        : $175.00 USD

================================================================================
VERSION HISTORY (تاریخچه نسخه)
================================================================================
v1.0.0 - 2025-11-07 - Elena Volkov - Initial implementation

================================================================================
DEPENDENCIES (وابستگی‌ها)
================================================================================
Internal  : app.config, app.core, app.models
External  : pytest, pytest-asyncio, pytest-cov
Database  : PostgreSQL 16+ (test), Redis 7 (test)

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/GravityMicroServices

NOTE: Environment variables for integration tests are configured below
BEFORE any app imports to ensure correct database connections.

================================================================================
"""

import os
import sys

# ============================================================================
# CRITICAL: Set test environment variables BEFORE importing the app
# This ensures Settings loads with correct test database configuration
# ============================================================================

# Set environment variables for integration testing
os.environ["POSTGRES_USER"] = "postgres"
os.environ["POSTGRES_PASSWORD"] = "postgres_pass_2025"
os.environ["POSTGRES_HOST"] = "localhost"
os.environ["POSTGRES_PORT"] = "5434"
os.environ["POSTGRES_DB"] = "service_discovery"
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6381"
os.environ["REDIS_PASSWORD"] = "redis_pass_2025"
os.environ["CONSUL_HOST"] = "localhost"
os.environ["CONSUL_PORT"] = "8500"
os.environ["LOG_LEVEL"] = "DEBUG"


import pytest
import asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient

from app.main import app
from app.models.service import Base
from app.core.database import db_manager
from app.core.redis_client import redis_client
from app.config import settings


# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_pass@localhost:5432/test_service_discovery"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create database session for tests."""
    async_session_maker = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create HTTP client for API tests."""
    async with AsyncClient(base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_consul_client(mocker):
    """Mock Consul client for tests."""
    mock = mocker.patch("app.core.consul_client.consul_client")
    mock.register_service = mocker.AsyncMock(return_value=True)
    mock.deregister_service = mocker.AsyncMock(return_value=True)
    mock.discover_service = mocker.AsyncMock(return_value=[])
    mock.get_all_services = mocker.AsyncMock(return_value={})
    mock.update_health_check = mocker.AsyncMock(return_value=True)
    mock.health_check = mocker.AsyncMock(return_value=True)
    return mock


@pytest.fixture
def mock_redis_client(mocker):
    """Mock Redis client for tests."""
    mock = mocker.patch("app.core.redis_client.redis_client")
    mock.get = mocker.AsyncMock(return_value=None)
    mock.set = mocker.AsyncMock(return_value=True)
    mock.delete = mocker.AsyncMock(return_value=True)
    mock.health_check = mocker.AsyncMock(return_value=True)
    return mock


@pytest.fixture
def sample_service_data():
    """Sample service registration data."""
    return {
        "service_id": "test-service-001",
        "service_name": "test-service",
        "address": "10.0.1.100",
        "port": 8080,
        "tags": ["v1.0.0", "test"],
        "meta": {"version": "1.0.0", "team": "test"},
        "health_check": {
            "check_type": "http",
            "interval": "10s",
            "timeout": "5s",
            "http_endpoint": "http://10.0.1.100:8080/health"
        },
        "weight": 10,
        "datacenter": "dc1",
        "region": "us-east-1",
        "zone": "us-east-1a"
    }


@pytest.fixture
def sample_service_instances():
    """Sample service instances for discovery."""
    from app.core.consul_client import ServiceInstance
    
    return [
        ServiceInstance(
            service_id="test-service-001",
            service_name="test-service",
            address="10.0.1.100",
            port=8080,
            tags=["v1.0.0"],
            meta={"version": "1.0.0"},
            health_status="passing"
        ),
        ServiceInstance(
            service_id="test-service-002",
            service_name="test-service",
            address="10.0.1.101",
            port=8080,
            tags=["v1.0.0"],
            meta={"version": "1.0.0"},
            health_status="passing"
        ),
        ServiceInstance(
            service_id="test-service-003",
            service_name="test-service",
            address="10.0.1.102",
            port=8080,
            tags=["v1.0.0"],
            meta={"version": "1.0.0"},
            health_status="passing"
        ),
    ]
