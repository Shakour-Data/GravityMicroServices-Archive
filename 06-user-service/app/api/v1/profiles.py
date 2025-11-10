"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : profiles.py
Description  : User profile API endpoints
Language     : English (UK)
Framework    : FastAPI / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Elena Volkov (Backend & Integration Lead)
Contributors      : Dr. Sarah Chen (Chief Architect)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-08 16:15 UTC
Last Modified     : 2025-11-08 16:15 UTC
Development Time  : 2 hours 0 minutes
Total Cost        : 2.0 × $150 = $300.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial endpoint implementation

================================================================================
DEPENDENCIES
================================================================================
Internal  : core, services, schemas
External  : fastapi
Database  : PostgreSQL 16+

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

from typing import cast
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db
from app.core.security import get_current_user, CurrentUser
from app.core.exceptions import ForbiddenException
from app.services import ProfileService
from app.schemas import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserProfileWithPreferences
)
from app.config import settings


router = APIRouter(prefix="/users", tags=["User Profiles"])


@router.post(
    "",
    response_model=UserProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create user profile",
    description="Create a new user profile. Requires authentication."
)
async def create_profile(
    profile_data: UserProfileCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserProfileResponse:
    """Create a new user profile."""
    # Ensure user can only create their own profile
    if profile_data.user_id != current_user.user_id:
        raise ForbiddenException("Cannot create profile for another user")
    
    service = ProfileService(db)
    return await service.create_profile(profile_data)


@router.get(
    "/me",
    response_model=UserProfileWithPreferences,
    summary="Get current user profile",
    description="Get the authenticated user's profile with preferences."
)
async def get_my_profile(
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserProfileWithPreferences:
    """Get current user's profile."""
    service = ProfileService(db)
    profile = cast(
        UserProfileWithPreferences,
        await service.get_profile_by_user_id(
            current_user.user_id,
            include_preferences=True
        )
    )
    
    # Update last login
    await service.update_last_login(profile.id)
    
    return profile


@router.get(
    "/{profile_id}",
    response_model=UserProfileResponse,
    summary="Get user profile by ID",
    description="Get a specific user profile by ID. Public endpoint."
)
async def get_profile(
    profile_id: str,
    db: AsyncSession = Depends(get_db)
) -> UserProfileResponse:
    """Get user profile by ID."""
    service = ProfileService(db)
    return await service.get_profile_by_id(profile_id)


@router.patch(
    "/{profile_id}",
    response_model=UserProfileResponse,
    summary="Update user profile",
    description="Update user profile. Users can only update their own profile."
)
async def update_profile(
    profile_id: str,
    profile_data: UserProfileUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserProfileResponse:
    """Update user profile."""
    service = ProfileService(db)
    
    # Verify ownership
    profile = await service.get_profile_by_id(profile_id)
    if profile.user_id != current_user.user_id:
        raise ForbiddenException("Cannot update another user's profile")
    
    return await service.update_profile(profile_id, profile_data)


@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user profile",
    description="Delete user profile. Users can only delete their own profile."
)
async def delete_profile(
    profile_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete user profile."""
    service = ProfileService(db)
    
    # Verify ownership
    profile = await service.get_profile_by_id(profile_id)
    if profile.user_id != current_user.user_id:
        raise ForbiddenException("Cannot delete another user's profile")
    
    await service.delete_profile(profile_id)


@router.get(
    "",
    response_model=dict,
    summary="List user profiles",
    description="List all user profiles with pagination. Public endpoint."
)
async def list_profiles(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Number of records to return"
    ),
    is_active: bool = Query(None, description="Filter by active status"),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """List user profiles with pagination."""
    service = ProfileService(db)
    profiles, total = await service.list_profiles(skip, limit, is_active)
    
    return {
        "items": profiles,
        "total": total,
        "skip": skip,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get(
    "/search/",
    response_model=dict,
    summary="Search user profiles",
    description="Search user profiles by display name or location. Public endpoint."
)
async def search_profiles(
    q: str = Query(..., min_length=2, description="Search query"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Number of records to return"
    ),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Search user profiles."""
    service = ProfileService(db)
    profiles, total = await service.search_profiles(q, skip, limit)
    
    return {
        "items": profiles,
        "total": total,
        "skip": skip,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
        "query": q
    }
