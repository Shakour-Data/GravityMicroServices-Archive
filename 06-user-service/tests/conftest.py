"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : conftest.py
Description  : pytest configuration and fixtures
Language     : English (UK)
Framework    : pytest / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Elena Volkov (Backend & Integration Lead)
Contributors      : Dr. Sarah Chen (Chief Architect)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-08 18:30 UTC
Last Modified     : 2025-11-08 18:30 UTC
Development Time  : 1 hour 30 minutes
Total Cost        : 1.5 × $150 = $225.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial test configuration

================================================================================
DEPENDENCIES
================================================================================
Internal  : app.main, app.core, app.models
External  : pytest, httpx, sqlalchemy
Database  : PostgreSQL 16+ (test database)

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

import asyncio
import uuid
from typing import AsyncGenerator, Generator
from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from jose import jwt

from app.main import app
from app.core import get_db
from app.models import Base
from app.config import settings


# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_pass@localhost:5433/test_user_db"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db() -> AsyncGenerator[AsyncSession, None]:
    """
    Create test database session.
    
    Creates tables before test and drops them after.
    """
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
    
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create test HTTP client.
    
    Overrides database dependency with test database.
    """
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_id() -> str:
    """Generate test user ID."""
    return str(uuid.uuid4())


@pytest.fixture
def test_user_email() -> str:
    """Generate test user email."""
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture
def auth_token(test_user_id: str, test_user_email: str) -> str:
    """
    Create test JWT token.
    
    Args:
        test_user_id: Test user ID
        test_user_email: Test user email
        
    Returns:
        str: JWT token
    """
    payload = {
        "sub": test_user_id,
        "email": test_user_email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc),
        "jti": str(uuid.uuid4())
    }
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


@pytest.fixture
def auth_headers(auth_token: str) -> dict[str, str]:
    """
    Create authorization headers.
    
    Args:
        auth_token: JWT token
        
    Returns:
        dict: Authorization headers
    """
    return {"Authorization": f"Bearer {auth_token}"}
