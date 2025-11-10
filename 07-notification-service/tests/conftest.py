"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - Notification Service
File         : conftest.py
Description  : Pytest configuration and fixtures
Language     : English (UK)
Framework    : pytest / pytest-asyncio

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Marcus Chen (Backend & Integration Lead)
Contributors      : Dr. Sarah Chen (Chief Architect)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-09
Development Time  : 30 minutes
Total Cost        : 0.5 × $150 = $75.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-09 - Marcus Chen - Initial test configuration

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
================================================================================
"""

import asyncio
from typing import AsyncGenerator, Generator
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.core.database import Base
from app.config import settings


# Test database URL (using different database)
TEST_DATABASE_URL = settings.DATABASE_URL.replace("/notification_db", "/notification_test_db")


# Async test configuration
@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Database fixtures
@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
        echo=False,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


# Test data fixtures
@pytest.fixture
def sample_user_id():
    """Sample user ID for testing."""
    from uuid import uuid4
    return uuid4()


@pytest.fixture
def sample_email_data():
    """Sample email data for testing."""
    return {
        "to": "test@example.com",
        "subject": "Test Subject",
        "content": "Test content",
        "html_content": "<p>Test HTML content</p>",
    }


@pytest.fixture
def sample_template_data():
    """Sample template data for testing."""
    return {
        "name": "test_template",
        "type": "EMAIL",
        "subject": "Hello {{ name }}",
        "content": "Hello {{ name }}, this is a test.",
        "html_content": "<h1>Hello {{ name }}</h1>",
        "variables": ["name"],
        "language": "en",
    }
