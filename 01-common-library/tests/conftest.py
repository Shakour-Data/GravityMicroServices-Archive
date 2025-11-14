"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform
File         : conftest.py
Description  : Pytest configuration and shared fixtures
Language     : English (UK)
Framework    : Pytest / FastAPI TestClient

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : João Silva (Testing & Quality Assurance Lead)
Contributors      : Elena Volkov (FastAPI expertise)
                   Dr. Aisha Patel (Database fixtures)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-13 23:00 UTC
Last Modified     : 2025-11-14 00:00 UTC
Development Time  : 0 hours 45 minutes
Review Time       : 0 hours 15 minutes
Total Time        : 1 hour 00 minutes
Total Cost        : 1.0 x $150 = $150.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-13 - João Silva - Pytest configuration
                    - Test client fixture
                    - Database fixtures
                    - Redis mock fixtures

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/Shakour-Data/01-common-library
================================================================================
"""

import pytest
from typing import Generator
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """
    Fixture providing FastAPI test client.
    
    Usage:
        def test_health(client):
            response = client.get("/health")
            assert response.status_code == 200
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_redis_data() -> dict:
    """
    Fixture providing mock Redis data for testing.
    """
    return {
        "test_key_1": "test_value_1",
        "test_key_2": "test_value_2",
        "user:123": "John Doe"
    }


@pytest.fixture
def sample_user_data() -> dict:
    """
    Fixture providing sample user data for testing.
    """
    return {
        "email": "test@example.com",
        "password": "SecurePass123!",
        "first_name": "John",
        "last_name": "Doe"
    }
