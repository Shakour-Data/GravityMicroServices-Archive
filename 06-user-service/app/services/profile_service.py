"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : profile_service.py
Description  : User profile service layer
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
Created Date      : 2025-11-08 14:00 UTC
Last Modified     : 2025-11-08 14:00 UTC
Development Time  : 2 hours 0 minutes
Total Cost        : 2.0 × $150 = $300.00 USD

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

import uuid
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import UserProfile, UserPreference
from app.schemas import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserProfileWithPreferences,
    UserPreferenceCreate
)
from app.core.exceptions import (
    ProfileNotFoundException,
    ProfileAlreadyExistsException
)


class ProfileService:
    """Service for managing user profiles."""
    
    def __init__(self, db: AsyncSession) -> None:
        """Initialize profile service."""
        self.db = db
    
    async def create_profile(
        self,
        profile_data: UserProfileCreate
    ) -> UserProfileResponse:
        """
        Create a new user profile.
        
        Args:
            profile_data: Profile creation data
            
        Returns:
            UserProfileResponse: Created profile
            
        Raises:
            ProfileAlreadyExistsException: If profile already exists for user
        """
        # Check if profile already exists
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.user_id == profile_data.user_id)
        )
        if result.scalar_one_or_none():
            raise ProfileAlreadyExistsException(profile_data.user_id)
        
        # Create profile
        profile = UserProfile(
            id=str(uuid.uuid4()),
            user_id=profile_data.user_id,
            display_name=profile_data.display_name,
            bio=profile_data.bio,
            location=profile_data.location,
            website=profile_data.website,
            phone_number=profile_data.phone_number,
            is_verified=False,
            is_active=True
        )
        
        self.db.add(profile)
        
        # Create default preferences
        preference = UserPreference(
            id=str(uuid.uuid4()),
            profile_id=profile.id
        )
        self.db.add(preference)
        
        await self.db.commit()
        await self.db.refresh(profile)
        
        return UserProfileResponse.model_validate(profile)
    
    async def get_profile_by_id(
        self,
        profile_id: str,
        include_preferences: bool = False
    ) -> UserProfileResponse | UserProfileWithPreferences:
        """
        Get profile by ID.
        
        Args:
            profile_id: Profile ID
            include_preferences: Include preferences in response
            
        Returns:
            UserProfileResponse: Profile data
            
        Raises:
            ProfileNotFoundException: If profile not found
        """
        query = select(UserProfile).where(UserProfile.id == profile_id)
        
        if include_preferences:
            query = query.options(selectinload(UserProfile.preferences))
        
        result = await self.db.execute(query)
        profile = result.scalar_one_or_none()
        
        if not profile:
            raise ProfileNotFoundException(profile_id)
        
        if include_preferences:
            return UserProfileWithPreferences.model_validate(profile)
        return UserProfileResponse.model_validate(profile)
    
    async def get_profile_by_user_id(
        self,
        user_id: str,
        include_preferences: bool = False
    ) -> UserProfileResponse | UserProfileWithPreferences:
        """
        Get profile by user ID.
        
        Args:
            user_id: User ID from auth-service
            include_preferences: Include preferences in response
            
        Returns:
            UserProfileResponse: Profile data
            
        Raises:
            ProfileNotFoundException: If profile not found
        """
        query = select(UserProfile).where(UserProfile.user_id == user_id)
        
        if include_preferences:
            query = query.options(selectinload(UserProfile.preferences))
        
        result = await self.db.execute(query)
        profile = result.scalar_one_or_none()
        
        if not profile:
            raise ProfileNotFoundException(user_id)
        
        if include_preferences:
            return UserProfileWithPreferences.model_validate(profile)
        return UserProfileResponse.model_validate(profile)
    
    async def update_profile(
        self,
        profile_id: str,
        profile_data: UserProfileUpdate
    ) -> UserProfileResponse:
        """
        Update user profile.
        
        Args:
            profile_id: Profile ID
            profile_data: Profile update data
            
        Returns:
            UserProfileResponse: Updated profile
            
        Raises:
            ProfileNotFoundException: If profile not found
        """
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.id == profile_id)
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            raise ProfileNotFoundException(profile_id)
        
        # Update fields
        update_data = profile_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)
        
        await self.db.commit()
        await self.db.refresh(profile)
        
        return UserProfileResponse.model_validate(profile)
    
    async def delete_profile(self, profile_id: str) -> None:
        """
        Delete user profile.
        
        Args:
            profile_id: Profile ID
            
        Raises:
            ProfileNotFoundException: If profile not found
        """
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.id == profile_id)
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            raise ProfileNotFoundException(profile_id)
        
        await self.db.delete(profile)
        await self.db.commit()
    
    async def list_profiles(
        self,
        skip: int = 0,
        limit: int = 20,
        is_active: Optional[bool] = None
    ) -> tuple[List[UserProfileResponse], int]:
        """
        List user profiles with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Number of records to return
            is_active: Filter by active status
            
        Returns:
            tuple: (List of profiles, total count)
        """
        # Build query
        query = select(UserProfile)
        count_query = select(func.count()).select_from(UserProfile)
        
        if is_active is not None:
            query = query.where(UserProfile.is_active == is_active)
            count_query = count_query.where(UserProfile.is_active == is_active)
        
        # Get total count
        count_result = await self.db.execute(count_query)
        total = count_result.scalar_one()
        
        # Get profiles
        query = query.offset(skip).limit(limit).order_by(UserProfile.created_at.desc())
        result = await self.db.execute(query)
        profiles = result.scalars().all()
        
        return (
            [UserProfileResponse.model_validate(p) for p in profiles],
            total
        )
    
    async def search_profiles(
        self,
        query: str,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[UserProfileResponse], int]:
        """
        Search user profiles by display name.
        
        Args:
            query: Search query
            skip: Number of records to skip
            limit: Number of records to return
            
        Returns:
            tuple: (List of profiles, total count)
        """
        search_filter = or_(
            UserProfile.display_name.ilike(f"%{query}%"),
            UserProfile.location.ilike(f"%{query}%")
        )
        
        # Build query
        profile_query = (
            select(UserProfile)
            .where(search_filter)
            .where(UserProfile.is_active == True)
        )
        count_query = (
            select(func.count())
            .select_from(UserProfile)
            .where(search_filter)
            .where(UserProfile.is_active == True)
        )
        
        # Get total count
        count_result = await self.db.execute(count_query)
        total = count_result.scalar_one()
        
        # Get profiles
        profile_query = profile_query.offset(skip).limit(limit)
        result = await self.db.execute(profile_query)
        profiles = result.scalars().all()
        
        return (
            [UserProfileResponse.model_validate(p) for p in profiles],
            total
        )
    
    async def update_last_login(self, profile_id: str) -> None:
        """
        Update last login timestamp.
        
        Args:
            profile_id: Profile ID
        """
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.id == profile_id)
        )
        profile = result.scalar_one_or_none()
        
        if profile:
            profile.last_login_at = datetime.now(timezone.utc)
            await self.db.commit()
