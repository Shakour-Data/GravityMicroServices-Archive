"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : test_preferences.py
Description  : User preferences API endpoint tests
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
Created Date      : 2025-11-08 21:00 UTC
Last Modified     : 2025-11-08 21:00 UTC
Development Time  : 1 hour 30 minutes
Total Cost        : 1.5 × $150 = $225.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial preference tests

================================================================================
DEPENDENCIES
================================================================================
Internal  : conftest
External  : pytest, httpx
Database  : PostgreSQL 16+ (test database)

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_preference import UserPreference


@pytest.mark.asyncio
async def test_get_preferences(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test getting user preferences."""
    # Create preferences first
    preference = UserPreference(
        user_id=test_user_id,
        language="en",
        timezone="UTC",
        theme="light",
        email_notifications=True,
        push_notifications=False,
        sms_notifications=False
    )
    db.add(preference)
    await db.commit()
    
    # Get preferences
    response = await client.get(
        f"/api/v1/users/{test_user_id}/preferences",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == test_user_id
    assert data["language"] == "en"
    assert data["timezone"] == "UTC"
    assert data["theme"] == "light"
    assert data["email_notifications"] is True
    assert data["push_notifications"] is False


@pytest.mark.asyncio
async def test_get_preferences_not_found(
    client: AsyncClient,
    test_user_id: str,
    auth_headers: dict
):
    """Test getting preferences for user without preferences."""
    # Try to get non-existent preferences
    response = await client.get(
        f"/api/v1/users/{test_user_id}/preferences",
        headers=auth_headers
    )
    
    # Should return default preferences
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == test_user_id
    assert data["language"] == "en"
    assert data["timezone"] == "UTC"
    assert data["theme"] == "system"


@pytest.mark.asyncio
async def test_update_preferences(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test updating user preferences."""
    # Create initial preferences
    preference = UserPreference(
        user_id=test_user_id,
        language="en",
        timezone="UTC"
    )
    db.add(preference)
    await db.commit()
    
    # Update preferences
    update_data = {
        "language": "fa",
        "timezone": "Asia/Tehran",
        "theme": "dark",
        "email_notifications": False
    }
    
    response = await client.patch(
        f"/api/v1/users/{test_user_id}/preferences",
        headers=auth_headers,
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "fa"
    assert data["timezone"] == "Asia/Tehran"
    assert data["theme"] == "dark"
    assert data["email_notifications"] is False


@pytest.mark.asyncio
async def test_update_preferences_partial(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test partial update of preferences."""
    # Create initial preferences
    preference = UserPreference(
        user_id=test_user_id,
        language="en",
        timezone="UTC",
        theme="light"
    )
    db.add(preference)
    await db.commit()
    
    # Update only language
    update_data = {
        "language": "fr"
    }
    
    response = await client.patch(
        f"/api/v1/users/{test_user_id}/preferences",
        headers=auth_headers,
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "fr"
    assert data["timezone"] == "UTC"  # Unchanged
    assert data["theme"] == "light"  # Unchanged


@pytest.mark.asyncio
async def test_update_preferences_invalid_timezone(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test updating preferences with invalid timezone."""
    # Create initial preferences
    preference = UserPreference(
        user_id=test_user_id,
        language="en",
        timezone="UTC"
    )
    db.add(preference)
    await db.commit()
    
    # Try to update with invalid timezone
    update_data = {
        "timezone": "Invalid/Timezone"
    }
    
    response = await client.patch(
        f"/api/v1/users/{test_user_id}/preferences",
        headers=auth_headers,
        json=update_data
    )
    
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_update_preferences_unauthorized(
    client: AsyncClient,
    test_user_id: str
):
    """Test updating preferences without authentication."""
    update_data = {
        "language": "fa"
    }
    
    response = await client.patch(
        f"/api/v1/users/{test_user_id}/preferences",
        json=update_data
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_preferences_forbidden(
    client: AsyncClient,
    auth_headers: dict
):
    """Test updating another user's preferences."""
    other_user_id = "other-user-123"
    update_data = {
        "language": "fa"
    }
    
    response = await client.patch(
        f"/api/v1/users/{other_user_id}/preferences",
        headers=auth_headers,
        json=update_data
    )
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_preferences_unauthorized(
    client: AsyncClient,
    test_user_id: str
):
    """Test getting preferences without authentication."""
    response = await client.get(
        f"/api/v1/users/{test_user_id}/preferences"
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_preferences_language_validation(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test language code validation."""
    preference = UserPreference(
        user_id=test_user_id,
        language="en",
        timezone="UTC"
    )
    db.add(preference)
    await db.commit()
    
    # Valid language codes
    for lang in ["en", "fa", "ar", "fr", "de", "es", "ja", "zh"]:
        response = await client.patch(
            f"/api/v1/users/{test_user_id}/preferences",
            headers=auth_headers,
            json={"language": lang}
        )
        assert response.status_code == 200
        assert response.json()["language"] == lang


@pytest.mark.asyncio
async def test_preferences_theme_validation(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test theme validation."""
    preference = UserPreference(
        user_id=test_user_id,
        language="en",
        timezone="UTC"
    )
    db.add(preference)
    await db.commit()
    
    # Valid themes
    for theme in ["light", "dark", "system"]:
        response = await client.patch(
            f"/api/v1/users/{test_user_id}/preferences",
            headers=auth_headers,
            json={"theme": theme}
        )
        assert response.status_code == 200
        assert response.json()["theme"] == theme
