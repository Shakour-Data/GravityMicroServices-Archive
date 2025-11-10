"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : preferences.py
Description  : User preference API endpoints
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
Created Date      : 2025-11-08 17:00 UTC
Last Modified     : 2025-11-08 17:00 UTC
Development Time  : 1 hour 0 minutes
Total Cost        : 1.0 × $150 = $150.00 USD

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

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db
from app.core.security import get_current_user, CurrentUser
from app.core.exceptions import ForbiddenException
from app.services import ProfileService, PreferenceService
from app.schemas import UserPreferenceUpdate, UserPreferenceResponse


router = APIRouter(prefix="/users", tags=["User Preferences"])


@router.get(
    "/{profile_id}/preferences",
    response_model=UserPreferenceResponse,
    summary="Get user preferences",
    description="Get user preferences by profile ID. Users can only access their own preferences."
)
async def get_preferences(
    profile_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserPreferenceResponse:
    """Get user preferences."""
    profile_service = ProfileService(db)
    preference_service = PreferenceService(db)
    
    # Verify ownership
    profile = await profile_service.get_profile_by_id(profile_id)
    if profile.user_id != current_user.user_id:
        raise ForbiddenException("Cannot access another user's preferences")
    
    return await preference_service.get_preferences(profile_id)


@router.patch(
    "/{profile_id}/preferences",
    response_model=UserPreferenceResponse,
    summary="Update user preferences",
    description="Update user preferences. Users can only update their own preferences."
)
async def update_preferences(
    profile_id: str,
    preference_data: UserPreferenceUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserPreferenceResponse:
    """Update user preferences."""
    profile_service = ProfileService(db)
    preference_service = PreferenceService(db)
    
    # Verify ownership
    profile = await profile_service.get_profile_by_id(profile_id)
    if profile.user_id != current_user.user_id:
        raise ForbiddenException("Cannot update another user's preferences")
    
    return await preference_service.update_preferences(profile_id, preference_data)
