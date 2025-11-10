"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : tests/test_auth_integration.py
Description  : Auth Service integration tests
Language     : English (UK)
Framework    : pytest / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : GitHub Copilot
Contributors      : Testing Team
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-08
Development Time  : 30 minutes
Total Cost        : 0.5 × $150 = $75.00 USD

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

import pytest
from unittest.mock import AsyncMock, patch
from app.core.security import (
    validate_token_with_auth_service,
    validate_token_locally,
    get_current_user,
    CurrentUser
)
from app.core.exceptions import UnauthorizedException


@pytest.mark.asyncio
async def test_validate_token_with_auth_service_success():
    """Test successful token validation with Auth Service."""
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(return_value={
        "sub": "user-123",
        "email": "test@example.com",
        "username": "testuser",
        "jti": "token-456"
    })
    
    with patch("httpx.AsyncClient.post", return_value=mock_response):
        payload = await validate_token_with_auth_service("fake-token")
        
        assert payload["sub"] == "user-123"
        assert payload["email"] == "test@example.com"
        assert payload["username"] == "testuser"


@pytest.mark.asyncio
async def test_validate_token_with_auth_service_unauthorized():
    """Test token validation with unauthorized response."""
    mock_response = AsyncMock()
    mock_response.status_code = 401
    
    with patch("httpx.AsyncClient.post", return_value=mock_response):
        with pytest.raises(UnauthorizedException) as exc_info:
            await validate_token_with_auth_service("invalid-token")
        
        assert "Invalid or expired token" in str(exc_info.value)


@pytest.mark.asyncio
async def test_validate_token_with_auth_service_timeout_fallback():
    """Test fallback to local validation on Auth Service timeout."""
    from httpx import TimeoutException
    
    # Mock timeout
    with patch("httpx.AsyncClient.post", side_effect=TimeoutException("Timeout")):
        # Mock local validation
        with patch("app.core.security.validate_token_locally") as mock_local:
            mock_local.return_value = {
                "sub": "user-123",
                "email": "test@example.com"
            }
            
            payload = await validate_token_with_auth_service("fake-token")
            
            assert payload["sub"] == "user-123"
            assert mock_local.called


def test_validate_token_locally_success():
    """Test local token validation with valid token."""
    from jose import jwt
    from datetime import datetime, timedelta, timezone
    from app.config import settings
    
    # Create valid token
    payload = {
        "sub": "user-123",
        "email": "test@example.com",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    # Validate
    result = validate_token_locally(token)
    
    assert result["sub"] == "user-123"
    assert result["email"] == "test@example.com"


def test_validate_token_locally_expired():
    """Test local token validation with expired token."""
    from jose import jwt
    from datetime import datetime, timedelta, timezone
    from app.config import settings
    
    # Create expired token
    payload = {
        "sub": "user-123",
        "email": "test@example.com",
        "exp": datetime.now(timezone.utc) - timedelta(hours=1),  # Expired
        "iat": datetime.now(timezone.utc) - timedelta(hours=2)
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    # Validate
    with pytest.raises(UnauthorizedException) as exc_info:
        validate_token_locally(token)
    
    assert "expired" in str(exc_info.value).lower()


def test_validate_token_locally_invalid():
    """Test local token validation with invalid token."""
    with pytest.raises(UnauthorizedException):
        validate_token_locally("invalid-token-format")


@pytest.mark.asyncio
async def test_get_current_user_success():
    """Test getting current user with valid token."""
    mock_payload = {
        "sub": "user-123",
        "email": "test@example.com",
        "username": "testuser",
        "jti": "token-456"
    }
    
    with patch("app.core.security.validate_token_with_auth_service", return_value=mock_payload):
        user = await get_current_user("Bearer fake-token")
        
        assert isinstance(user, CurrentUser)
        assert user.user_id == "user-123"
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.token_id == "token-456"


@pytest.mark.asyncio
async def test_get_current_user_invalid_header():
    """Test getting current user with invalid authorization header."""
    with pytest.raises(UnauthorizedException) as exc_info:
        await get_current_user("InvalidFormat token")
    
    assert "Invalid authorization header" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_current_user_missing_data():
    """Test getting current user with incomplete token payload."""
    mock_payload = {
        "sub": "user-123"
        # Missing email
    }
    
    with patch("app.core.security.validate_token_with_auth_service", return_value=mock_payload):
        with pytest.raises(UnauthorizedException) as exc_info:
            await get_current_user("Bearer fake-token")
        
        assert "missing user_id or email" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_get_current_user_with_user_id_field():
    """Test getting current user when payload uses 'user_id' instead of 'sub'."""
    mock_payload = {
        "user_id": "user-123",  # Alternative field name
        "email": "test@example.com"
    }
    
    with patch("app.core.security.validate_token_with_auth_service", return_value=mock_payload):
        user = await get_current_user("Bearer fake-token")
        
        assert user.user_id == "user-123"
        assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_service_discovery_integration():
    """Test that Auth Service URL is retrieved from service discovery."""
    from app.core.service_discovery import get_auth_service_url
    
    # This will use actual service discovery or fallback to config
    url = await get_auth_service_url()
    
    assert url is not None
    assert url.startswith("http://") or url.startswith("https://")
    assert "auth" in url.lower() or "8081" in url
