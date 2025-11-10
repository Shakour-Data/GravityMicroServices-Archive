"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : test_profiles.py
Description  : User profile API endpoint tests
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
Created Date      : 2025-11-08 19:00 UTC
Last Modified     : 2025-11-08 19:00 UTC
Development Time  : 2 hours 0 minutes
Total Cost        : 2.0 × $150 = $300.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial profile tests

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


@pytest.mark.asyncio
class TestUserProfiles:
    """Test user profile endpoints."""
    
    async def test_create_profile(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_user_id: str
    ) -> None:
        """Test creating a user profile."""
        profile_data = {
            "user_id": test_user_id,
            "display_name": "Test User",
            "bio": "This is a test bio",
            "location": "Test City",
            "website": "https://test.com",
            "phone_number": "+1234567890"
        }
        
        response = await client.post(
            "/api/v1/users",
            json=profile_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == test_user_id
        assert data["display_name"] == "Test User"
        assert data["bio"] == "This is a test bio"
        assert data["is_active"] is True
        assert data["is_verified"] is False
    
    async def test_create_profile_duplicate(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_user_id: str
    ) -> None:
        """Test creating duplicate profile returns 409."""
        profile_data = {
            "user_id": test_user_id,
            "display_name": "Test User"
        }
        
        # Create first profile
        await client.post(
            "/api/v1/users",
            json=profile_data,
            headers=auth_headers
        )
        
        # Try to create duplicate
        response = await client.post(
            "/api/v1/users",
            json=profile_data,
            headers=auth_headers
        )
        
        assert response.status_code == 409
    
    async def test_get_my_profile(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_user_id: str
    ) -> None:
        """Test getting current user's profile."""
        # Create profile
        profile_data = {
            "user_id": test_user_id,
            "display_name": "Test User"
        }
        await client.post(
            "/api/v1/users",
            json=profile_data,
            headers=auth_headers
        )
        
        # Get my profile
        response = await client.get(
            "/api/v1/users/me",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == test_user_id
        assert "preferences" in data
    
    async def test_get_profile_by_id(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_user_id: str
    ) -> None:
        """Test getting profile by ID."""
        # Create profile
        profile_data = {
            "user_id": test_user_id,
            "display_name": "Test User"
        }
        create_response = await client.post(
            "/api/v1/users",
            json=profile_data,
            headers=auth_headers
        )
        profile_id = create_response.json()["id"]
        
        # Get profile
        response = await client.get(f"/api/v1/users/{profile_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == profile_id
    
    async def test_update_profile(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_user_id: str
    ) -> None:
        """Test updating profile."""
        # Create profile
        profile_data = {
            "user_id": test_user_id,
            "display_name": "Test User"
        }
        create_response = await client.post(
            "/api/v1/users",
            json=profile_data,
            headers=auth_headers
        )
        profile_id = create_response.json()["id"]
        
        # Update profile
        update_data = {
            "display_name": "Updated User",
            "bio": "Updated bio"
        }
        response = await client.patch(
            f"/api/v1/users/{profile_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["display_name"] == "Updated User"
        assert data["bio"] == "Updated bio"
    
    async def test_delete_profile(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_user_id: str
    ) -> None:
        """Test deleting profile."""
        # Create profile
        profile_data = {
            "user_id": test_user_id,
            "display_name": "Test User"
        }
        create_response = await client.post(
            "/api/v1/users",
            json=profile_data,
            headers=auth_headers
        )
        profile_id = create_response.json()["id"]
        
        # Delete profile
        response = await client.delete(
            f"/api/v1/users/{profile_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify deleted
        get_response = await client.get(f"/api/v1/users/{profile_id}")
        assert get_response.status_code == 404
    
    async def test_list_profiles(
        self,
        client: AsyncClient
    ) -> None:
        """Test listing profiles."""
        response = await client.get("/api/v1/users")
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data
    
    async def test_search_profiles(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_user_id: str
    ) -> None:
        """Test searching profiles."""
        # Create profile
        profile_data = {
            "user_id": test_user_id,
            "display_name": "Searchable User"
        }
        await client.post(
            "/api/v1/users",
            json=profile_data,
            headers=auth_headers
        )
        
        # Search
        response = await client.get(
            "/api/v1/users/search/?q=Searchable"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert data["query"] == "Searchable"
