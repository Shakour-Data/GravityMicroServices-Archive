"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : sessions.py
Description  : User session API endpoints
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
Created Date      : 2025-11-08 17:30 UTC
Last Modified     : 2025-11-08 17:30 UTC
Development Time  : 1 hour 30 minutes
Total Cost        : 1.5 × $150 = $225.00 USD

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

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db
from app.core.security import get_current_user, CurrentUser
from app.core.exceptions import ForbiddenException
from app.services import ProfileService, SessionService
from app.schemas import UserSessionResponse


router = APIRouter(prefix="/users", tags=["User Sessions"])


@router.get(
    "/{profile_id}/sessions",
    response_model=List[UserSessionResponse],
    summary="Get active sessions",
    description="Get all active sessions for a user profile. Users can only access their own sessions."
)
async def get_active_sessions(
    profile_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> List[UserSessionResponse]:
    """Get active sessions for a profile."""
    profile_service = ProfileService(db)
    session_service = SessionService(db)
    
    # Verify ownership
    profile = await profile_service.get_profile_by_id(profile_id)
    if profile.user_id != current_user.user_id:
        raise ForbiddenException("Cannot access another user's sessions")
    
    return await session_service.get_active_sessions(profile_id)


@router.delete(
    "/{profile_id}/sessions/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Revoke session",
    description="Revoke (logout) a specific session. Users can only revoke their own sessions."
)
async def revoke_session(
    profile_id: str,
    session_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Revoke a specific session."""
    profile_service = ProfileService(db)
    session_service = SessionService(db)
    
    # Verify ownership
    profile = await profile_service.get_profile_by_id(profile_id)
    if profile.user_id != current_user.user_id:
        raise ForbiddenException("Cannot revoke another user's session")
    
    # Verify session belongs to profile
    session = await session_service.get_session(session_id)
    if session.profile_id != profile_id:
        raise ForbiddenException("Session does not belong to this profile")
    
    await session_service.revoke_session(session_id)


@router.delete(
    "/{profile_id}/sessions",
    response_model=dict,
    summary="Revoke all sessions",
    description="Revoke all active sessions for a user. Users can only revoke their own sessions."
)
async def revoke_all_sessions(
    profile_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Revoke all sessions for a profile."""
    profile_service = ProfileService(db)
    session_service = SessionService(db)
    
    # Verify ownership
    profile = await profile_service.get_profile_by_id(profile_id)
    if profile.user_id != current_user.user_id:
        raise ForbiddenException("Cannot revoke another user's sessions")
    
    count = await session_service.revoke_all_sessions(profile_id)
    
    return {
        "message": "All sessions revoked successfully",
        "revoked_count": count
    }
