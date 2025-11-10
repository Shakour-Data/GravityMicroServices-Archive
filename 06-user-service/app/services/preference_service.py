"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : preference_service.py
Description  : User preference service layer
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
Created Date      : 2025-11-08 15:00 UTC
Last Modified     : 2025-11-08 15:00 UTC
Development Time  : 1 hour 0 minutes
Total Cost        : 1.0 × $150 = $150.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial service implementation

================================================================================
DEPENDENCIES
================================================================================
Internal  : models, schemas, exceptions
External  : sqlalchemy
Database  : PostgreSQL 16+

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserPreference
from app.schemas import UserPreferenceUpdate, UserPreferenceResponse
from app.core.exceptions import PreferenceNotFoundException


class PreferenceService:
    """Service for managing user preferences."""
    
    def __init__(self, db: AsyncSession) -> None:
        """Initialize preference service."""
        self.db = db
    
    async def get_preferences(self, profile_id: str) -> UserPreferenceResponse:
        """
        Get user preferences by profile ID.
        
        Args:
            profile_id: Profile ID
            
        Returns:
            UserPreferenceResponse: User preferences
            
        Raises:
            PreferenceNotFoundException: If preferences not found
        """
        result = await self.db.execute(
            select(UserPreference).where(UserPreference.profile_id == profile_id)
        )
        preference = result.scalar_one_or_none()
        
        if not preference:
            raise PreferenceNotFoundException(profile_id)
        
        return UserPreferenceResponse.model_validate(preference)
    
    async def update_preferences(
        self,
        profile_id: str,
        preference_data: UserPreferenceUpdate
    ) -> UserPreferenceResponse:
        """
        Update user preferences.
        
        Args:
            profile_id: Profile ID
            preference_data: Preference update data
            
        Returns:
            UserPreferenceResponse: Updated preferences
            
        Raises:
            PreferenceNotFoundException: If preferences not found
        """
        result = await self.db.execute(
            select(UserPreference).where(UserPreference.profile_id == profile_id)
        )
        preference = result.scalar_one_or_none()
        
        if not preference:
            raise PreferenceNotFoundException(profile_id)
        
        # Update fields
        update_data = preference_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(preference, field, value)
        
        await self.db.commit()
        await self.db.refresh(preference)
        
        return UserPreferenceResponse.model_validate(preference)
