"""
Pytest Configuration and Fixtures
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings
from app.core.database import Base, get_db
from app.main import app

# Test database URL
TEST_DATABASE_URL = settings.TEST_DATABASE_URL


# Event loop fixture for async tests
@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Test database engine
@pytest_asyncio.fixture(scope="function")
async def test_db_engine():
    """Create test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


# Test database session
@pytest_asyncio.fixture(scope="function")
async def test_db(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session"""
    async_session = sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with async_session() as session:
        yield session
        await session.rollback()


# Override database dependency
@pytest.fixture(scope="function")
def override_get_db(test_db):
    """Override get_db dependency"""

    async def _override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


# HTTP client fixture
@pytest_asyncio.fixture(scope="function")
async def client(override_get_db) -> AsyncGenerator[AsyncClient, None]:
    """Create HTTP client for testing"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# Mock user fixture
@pytest.fixture
def mock_user():
    """Create mock authenticated user"""
    return {
        "sub": "123",
        "username": "testuser",
        "email": "test@example.com",
        "role": "user",
        "disabled": False,
    }


# Mock admin user fixture
@pytest.fixture
def mock_admin_user():
    """Create mock admin user"""
    return {
        "sub": "456",
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin",
        "disabled": False,
    }


# Auth token fixture
@pytest.fixture
def auth_token(mock_user):
    """Create authentication token for mock user"""
    from app.core.security import create_access_token

    return create_access_token(data=mock_user)


# Admin auth token fixture
@pytest.fixture
def admin_auth_token(mock_admin_user):
    """Create authentication token for mock admin"""
    from app.core.security import create_access_token

    return create_access_token(data=mock_admin_user)
