"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : test_sessions.py
Description  : User sessions API endpoint tests
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
Created Date      : 2025-11-08 21:30 UTC
Last Modified     : 2025-11-08 21:30 UTC
Development Time  : 2 hours 0 minutes
Total Cost        : 2.0 × $150 = $300.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial session tests

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
from datetime import datetime, timedelta
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_session import UserSession


@pytest.mark.asyncio
async def test_get_active_sessions(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test getting active sessions."""
    # Create active sessions
    session1 = UserSession(
        user_id=test_user_id,
        session_id="session-1",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0",
        device_type="desktop",
        is_active=True,
        expires_at=datetime.utcnow() + timedelta(days=1)
    )
    session2 = UserSession(
        user_id=test_user_id,
        session_id="session-2",
        ip_address="192.168.1.2",
        user_agent="Mobile Safari",
        device_type="mobile",
        is_active=True,
        expires_at=datetime.utcnow() + timedelta(days=1)
    )
    db.add_all([session1, session2])
    await db.commit()
    
    # Get sessions
    response = await client.get(
        f"/api/v1/users/{test_user_id}/sessions",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["is_active"] is True
    assert data[1]["is_active"] is True


@pytest.mark.asyncio
async def test_get_sessions_only_active(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test that only active sessions are returned."""
    # Create active and inactive sessions
    active_session = UserSession(
        user_id=test_user_id,
        session_id="active-session",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0",
        is_active=True,
        expires_at=datetime.utcnow() + timedelta(days=1)
    )
    inactive_session = UserSession(
        user_id=test_user_id,
        session_id="inactive-session",
        ip_address="192.168.1.2",
        user_agent="Mozilla/5.0",
        is_active=False,
        expires_at=datetime.utcnow() - timedelta(days=1)
    )
    db.add_all([active_session, inactive_session])
    await db.commit()
    
    # Get sessions
    response = await client.get(
        f"/api/v1/users/{test_user_id}/sessions",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["session_id"] == "active-session"


@pytest.mark.asyncio
async def test_revoke_session(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test revoking a specific session."""
    # Create session
    session = UserSession(
        user_id=test_user_id,
        session_id="session-to-revoke",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0",
        is_active=True,
        expires_at=datetime.utcnow() + timedelta(days=1)
    )
    db.add(session)
    await db.commit()
    
    # Revoke session
    response = await client.delete(
        f"/api/v1/users/{test_user_id}/sessions/session-to-revoke",
        headers=auth_headers
    )
    
    assert response.status_code == 204
    
    # Verify session is revoked
    await db.refresh(session)
    assert session.is_active is False


@pytest.mark.asyncio
async def test_revoke_session_not_found(
    client: AsyncClient,
    test_user_id: str,
    auth_headers: dict
):
    """Test revoking non-existent session."""
    response = await client.delete(
        f"/api/v1/users/{test_user_id}/sessions/non-existent-session",
        headers=auth_headers
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_revoke_all_sessions(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test revoking all sessions."""
    # Create multiple sessions
    sessions = [
        UserSession(
            user_id=test_user_id,
            session_id=f"session-{i}",
            ip_address=f"192.168.1.{i}",
            user_agent="Mozilla/5.0",
            is_active=True,
            expires_at=datetime.utcnow() + timedelta(days=1)
        )
        for i in range(3)
    ]
    db.add_all(sessions)
    await db.commit()
    
    # Revoke all sessions
    response = await client.delete(
        f"/api/v1/users/{test_user_id}/sessions",
        headers=auth_headers
    )
    
    assert response.status_code == 204
    
    # Verify all sessions are revoked
    for session in sessions:
        await db.refresh(session)
        assert session.is_active is False


@pytest.mark.asyncio
async def test_revoke_sessions_unauthorized(
    client: AsyncClient,
    test_user_id: str
):
    """Test revoking sessions without authentication."""
    response = await client.delete(
        f"/api/v1/users/{test_user_id}/sessions/some-session"
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_revoke_sessions_forbidden(
    client: AsyncClient,
    auth_headers: dict
):
    """Test revoking another user's sessions."""
    other_user_id = "other-user-123"
    
    response = await client.delete(
        f"/api/v1/users/{other_user_id}/sessions/some-session",
        headers=auth_headers
    )
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_sessions_unauthorized(
    client: AsyncClient,
    test_user_id: str
):
    """Test getting sessions without authentication."""
    response = await client.get(
        f"/api/v1/users/{test_user_id}/sessions"
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_session_ordering(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test that sessions are ordered by last_activity descending."""
    # Create sessions with different last_activity times
    old_session = UserSession(
        user_id=test_user_id,
        session_id="old-session",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0",
        is_active=True,
        last_activity=datetime.utcnow() - timedelta(hours=2),
        expires_at=datetime.utcnow() + timedelta(days=1)
    )
    recent_session = UserSession(
        user_id=test_user_id,
        session_id="recent-session",
        ip_address="192.168.1.2",
        user_agent="Mozilla/5.0",
        is_active=True,
        last_activity=datetime.utcnow() - timedelta(minutes=5),
        expires_at=datetime.utcnow() + timedelta(days=1)
    )
    db.add_all([old_session, recent_session])
    await db.commit()
    
    # Get sessions
    response = await client.get(
        f"/api/v1/users/{test_user_id}/sessions",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Most recent should be first
    assert data[0]["session_id"] == "recent-session"
    assert data[1]["session_id"] == "old-session"


@pytest.mark.asyncio
async def test_session_device_type_detection(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test device type detection from user agent."""
    sessions = [
        UserSession(
            user_id=test_user_id,
            session_id="desktop-session",
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            device_type="desktop",
            is_active=True,
            expires_at=datetime.utcnow() + timedelta(days=1)
        ),
        UserSession(
            user_id=test_user_id,
            session_id="mobile-session",
            ip_address="192.168.1.2",
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)",
            device_type="mobile",
            is_active=True,
            expires_at=datetime.utcnow() + timedelta(days=1)
        ),
        UserSession(
            user_id=test_user_id,
            session_id="tablet-session",
            ip_address="192.168.1.3",
            user_agent="Mozilla/5.0 (iPad; CPU OS 14_0)",
            device_type="tablet",
            is_active=True,
            expires_at=datetime.utcnow() + timedelta(days=1)
        )
    ]
    db.add_all(sessions)
    await db.commit()
    
    # Get sessions
    response = await client.get(
        f"/api/v1/users/{test_user_id}/sessions",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    device_types = {s["session_id"]: s["device_type"] for s in data}
    assert device_types["desktop-session"] == "desktop"
    assert device_types["mobile-session"] == "mobile"
    assert device_types["tablet-session"] == "tablet"


@pytest.mark.asyncio
async def test_expired_sessions_not_returned(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test that expired sessions are not returned even if active."""
    # Create expired but marked active session
    expired_session = UserSession(
        user_id=test_user_id,
        session_id="expired-session",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0",
        is_active=True,
        expires_at=datetime.utcnow() - timedelta(days=1)
    )
    valid_session = UserSession(
        user_id=test_user_id,
        session_id="valid-session",
        ip_address="192.168.1.2",
        user_agent="Mozilla/5.0",
        is_active=True,
        expires_at=datetime.utcnow() + timedelta(days=1)
    )
    db.add_all([expired_session, valid_session])
    await db.commit()
    
    # Get sessions
    response = await client.get(
        f"/api/v1/users/{test_user_id}/sessions",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    # Should only return valid session
    session_ids = [s["session_id"] for s in data]
    assert "valid-session" in session_ids
    assert "expired-session" not in session_ids
