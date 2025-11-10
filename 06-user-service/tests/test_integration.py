"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : test_integration.py
Description  : Integration tests for complete workflows
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
Created Date      : 2025-11-08 23:00 UTC
Last Modified     : 2025-11-08 23:00 UTC
Development Time  : 2 hours 30 minutes
Total Cost        : 2.5 × $150 = $375.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial integration tests

================================================================================
DEPENDENCIES
================================================================================
Internal  : conftest, all services
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


@pytest.mark.asyncio
async def test_complete_user_lifecycle(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test complete user lifecycle from creation to deletion."""
    
    # 1. Create user profile
    profile_data = {
        "user_id": test_user_id,
        "display_name": "Integration Test User",
        "bio": "Testing the complete lifecycle",
        "location": "Tehran, Iran"
    }
    
    response = await client.post(
        "/api/v1/users",
        headers=auth_headers,
        json=profile_data
    )
    assert response.status_code == 201
    profile = response.json()
    profile_id = profile["id"]
    
    # 2. Get own profile
    response = await client.get(
        "/api/v1/users/me",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["id"] == profile_id
    
    # 3. Update profile
    update_data = {
        "display_name": "Updated Test User",
        "bio": "Updated bio"
    }
    response = await client.patch(
        f"/api/v1/users/{profile_id}",
        headers=auth_headers,
        json=update_data
    )
    assert response.status_code == 200
    assert response.json()["display_name"] == "Updated Test User"
    
    # 4. Update preferences
    pref_data = {
        "language": "fa",
        "timezone": "Asia/Tehran",
        "theme": "dark"
    }
    response = await client.patch(
        f"/api/v1/users/{test_user_id}/preferences",
        headers=auth_headers,
        json=pref_data
    )
    assert response.status_code == 200
    assert response.json()["language"] == "fa"
    
    # 5. Get preferences
    response = await client.get(
        f"/api/v1/users/{test_user_id}/preferences",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["language"] == "fa"
    
    # 6. Create sessions (simulated)
    # In real scenario, sessions are created during login
    # Here we test the session endpoints
    
    # 7. Get active sessions
    response = await client.get(
        f"/api/v1/users/{test_user_id}/sessions",
        headers=auth_headers
    )
    assert response.status_code == 200
    sessions = response.json()
    assert isinstance(sessions, list)
    
    # 8. Search for user
    response = await client.get(
        f"/api/v1/users/search?q=Updated Test User"
    )
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert any(u["id"] == profile_id for u in results)
    
    # 9. List users
    response = await client.get("/api/v1/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert any(u["id"] == profile_id for u in users)
    
    # 10. Delete profile
    response = await client.delete(
        f"/api/v1/users/{profile_id}",
        headers=auth_headers
    )
    assert response.status_code == 204
    
    # 11. Verify deletion
    response = await client.get(f"/api/v1/users/{profile_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_multi_user_interaction(
    client: AsyncClient,
    auth_headers: dict
):
    """Test interactions between multiple users."""
    
    # Create first user
    user1_data = {
        "user_id": "user-1",
        "display_name": "Alice Johnson"
    }
    response = await client.post(
        "/api/v1/users",
        headers=auth_headers,
        json=user1_data
    )
    assert response.status_code == 201
    user1 = response.json()
    
    # Create second user
    user2_data = {
        "user_id": "user-2",
        "display_name": "Bob Smith"
    }
    response = await client.post(
        "/api/v1/users",
        headers=auth_headers,
        json=user2_data
    )
    assert response.status_code == 201
    user2 = response.json()
    
    # List all users
    response = await client.get("/api/v1/users")
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 2
    
    # Search for specific user
    response = await client.get("/api/v1/users/search?q=Alice")
    assert response.status_code == 200
    results = response.json()
    assert len(results) >= 1
    assert results[0]["display_name"] == "Alice Johnson"
    
    # Get user1 profile (public)
    response = await client.get(f"/api/v1/users/{user1['id']}")
    assert response.status_code == 200
    assert response.json()["display_name"] == "Alice Johnson"


@pytest.mark.asyncio
async def test_preference_persistence(
    client: AsyncClient,
    test_user_id: str,
    auth_headers: dict
):
    """Test that preferences persist across updates."""
    
    # Set initial preferences
    initial_prefs = {
        "language": "en",
        "timezone": "UTC",
        "theme": "light",
        "email_notifications": True,
        "push_notifications": True
    }
    response = await client.patch(
        f"/api/v1/users/{test_user_id}/preferences",
        headers=auth_headers,
        json=initial_prefs
    )
    assert response.status_code == 200
    
    # Update only language
    response = await client.patch(
        f"/api/v1/users/{test_user_id}/preferences",
        headers=auth_headers,
        json={"language": "fa"}
    )
    assert response.status_code == 200
    
    # Get preferences and verify all values
    response = await client.get(
        f"/api/v1/users/{test_user_id}/preferences",
        headers=auth_headers
    )
    assert response.status_code == 200
    prefs = response.json()
    
    assert prefs["language"] == "fa"  # Updated
    assert prefs["timezone"] == "UTC"  # Unchanged
    assert prefs["theme"] == "light"  # Unchanged
    assert prefs["email_notifications"] is True  # Unchanged


@pytest.mark.asyncio
async def test_session_management_workflow(
    client: AsyncClient,
    db: AsyncSession,
    test_user_id: str,
    auth_headers: dict
):
    """Test complete session management workflow."""
    
    # Create multiple sessions manually for testing
    from app.models.user_session import UserSession
    from datetime import datetime, timedelta
    
    sessions = [
        UserSession(
            user_id=test_user_id,
            session_id=f"session-{i}",
            ip_address=f"192.168.1.{i}",
            user_agent="Mozilla/5.0",
            device_type="desktop",
            is_active=True,
            expires_at=datetime.utcnow() + timedelta(days=1)
        )
        for i in range(3)
    ]
    
    db.add_all(sessions)
    await db.commit()
    
    # 1. Get all active sessions
    response = await client.get(
        f"/api/v1/users/{test_user_id}/sessions",
        headers=auth_headers
    )
    assert response.status_code == 200
    active_sessions = response.json()
    assert len(active_sessions) == 3
    
    # 2. Revoke specific session
    response = await client.delete(
        f"/api/v1/users/{test_user_id}/sessions/session-0",
        headers=auth_headers
    )
    assert response.status_code == 204
    
    # 3. Verify session revoked
    response = await client.get(
        f"/api/v1/users/{test_user_id}/sessions",
        headers=auth_headers
    )
    assert response.status_code == 200
    active_sessions = response.json()
    assert len(active_sessions) == 2
    assert not any(s["session_id"] == "session-0" for s in active_sessions)
    
    # 4. Revoke all remaining sessions
    response = await client.delete(
        f"/api/v1/users/{test_user_id}/sessions",
        headers=auth_headers
    )
    assert response.status_code == 204
    
    # 5. Verify all sessions revoked
    response = await client.get(
        f"/api/v1/users/{test_user_id}/sessions",
        headers=auth_headers
    )
    assert response.status_code == 200
    active_sessions = response.json()
    assert len(active_sessions) == 0


@pytest.mark.asyncio
async def test_pagination_workflow(client: AsyncClient, auth_headers: dict):
    """Test pagination across multiple pages."""
    
    # Create 25 users
    for i in range(25):
        user_data = {
            "user_id": f"pagination-user-{i}",
            "display_name": f"Pagination User {i}"
        }
        response = await client.post(
            "/api/v1/users",
            headers=auth_headers,
            json=user_data
        )
        assert response.status_code == 201
    
    # Get first page (default limit 20)
    response = await client.get("/api/v1/users?skip=0&limit=10")
    assert response.status_code == 200
    page1 = response.json()
    assert len(page1) == 10
    
    # Get second page
    response = await client.get("/api/v1/users?skip=10&limit=10")
    assert response.status_code == 200
    page2 = response.json()
    assert len(page2) == 10
    
    # Get third page
    response = await client.get("/api/v1/users?skip=20&limit=10")
    assert response.status_code == 200
    page3 = response.json()
    assert len(page3) >= 5
    
    # Verify no duplicates across pages
    all_ids = (
        [u["id"] for u in page1] +
        [u["id"] for u in page2] +
        [u["id"] for u in page3]
    )
    assert len(all_ids) == len(set(all_ids))  # All unique


@pytest.mark.asyncio
async def test_error_handling_workflow(
    client: AsyncClient,
    test_user_id: str,
    auth_headers: dict
):
    """Test error handling in various scenarios."""
    
    # 1. Try to get non-existent profile
    response = await client.get("/api/v1/users/non-existent-id")
    assert response.status_code == 404
    
    # 2. Try to create duplicate profile
    profile_data = {
        "user_id": test_user_id,
        "display_name": "Test User"
    }
    response = await client.post(
        "/api/v1/users",
        headers=auth_headers,
        json=profile_data
    )
    assert response.status_code == 201
    
    # Try duplicate
    response = await client.post(
        "/api/v1/users",
        headers=auth_headers,
        json=profile_data
    )
    assert response.status_code == 400
    
    # 3. Try to update with invalid data
    response = await client.patch(
        f"/api/v1/users/{test_user_id}/preferences",
        headers=auth_headers,
        json={"timezone": "Invalid/Timezone"}
    )
    assert response.status_code == 422
    
    # 4. Try to access without authentication
    response = await client.get(
        f"/api/v1/users/{test_user_id}/preferences"
    )
    assert response.status_code == 401
    
    # 5. Try to access another user's private data
    response = await client.patch(
        "/api/v1/users/other-user-id/preferences",
        headers=auth_headers,
        json={"language": "fa"}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_search_functionality(client: AsyncClient, auth_headers: dict):
    """Test search with various queries."""
    
    # Create users with different names
    users_data = [
        ("search-1", "Alice Johnson"),
        ("search-2", "Alice Cooper"),
        ("search-3", "Bob Johnson"),
        ("search-4", "Charlie Brown")
    ]
    
    for user_id, name in users_data:
        response = await client.post(
            "/api/v1/users",
            headers=auth_headers,
            json={"user_id": user_id, "display_name": name}
        )
        assert response.status_code == 201
    
    # Search for "Alice"
    response = await client.get("/api/v1/users/search?q=Alice")
    assert response.status_code == 200
    results = response.json()
    assert len(results) >= 2
    assert all("Alice" in r["display_name"] for r in results)
    
    # Search for "Johnson"
    response = await client.get("/api/v1/users/search?q=Johnson")
    assert response.status_code == 200
    results = response.json()
    assert len(results) >= 2
    assert all("Johnson" in r["display_name"] for r in results)
    
    # Search with no results
    response = await client.get("/api/v1/users/search?q=NonExistentUser")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 0


@pytest.mark.asyncio
async def test_concurrent_updates(
    client: AsyncClient,
    test_user_id: str,
    auth_headers: dict
):
    """Test handling of concurrent preference updates."""
    
    # Create initial preferences
    response = await client.patch(
        f"/api/v1/users/{test_user_id}/preferences",
        headers=auth_headers,
        json={"language": "en", "theme": "light"}
    )
    assert response.status_code == 200
    
    # Simulate concurrent updates
    import asyncio
    
    async def update_language():
        return await client.patch(
            f"/api/v1/users/{test_user_id}/preferences",
            headers=auth_headers,
            json={"language": "fa"}
        )
    
    async def update_theme():
        return await client.patch(
            f"/api/v1/users/{test_user_id}/preferences",
            headers=auth_headers,
            json={"theme": "dark"}
        )
    
    # Execute concurrently
    results = await asyncio.gather(
        update_language(),
        update_theme()
    )
    
    # Both should succeed
    assert all(r.status_code == 200 for r in results)
    
    # Get final state
    response = await client.get(
        f"/api/v1/users/{test_user_id}/preferences",
        headers=auth_headers
    )
    assert response.status_code == 200
    prefs = response.json()
    
    # Both updates should be applied
    assert prefs["language"] == "fa"
    assert prefs["theme"] == "dark"
