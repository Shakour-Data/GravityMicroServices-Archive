"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : user_profile.py
Description  : User profile Pydantic schemas
Language     : English (UK)
Framework    : Pydantic 2.0+ / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Elena Volkov (Backend & Integration Lead)
Contributors      : Dr. Sarah Chen (Chief Architect)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-08 11:00 UTC
Last Modified     : 2025-11-08 11:00 UTC
Development Time  : 0 hours 45 minutes
Total Cost        : 0.75 × $150 = $112.50 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial schema implementation

================================================================================
DEPENDENCIES
================================================================================
Internal  : None
External  : pydantic
Database  : None

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class UserProfileBase(BaseModel):
    """Base user profile schema with common fields."""
    
    display_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User display name"
    )
    bio: Optional[str] = Field(
        None,
        max_length=500,
        description="User biography"
    )
    location: Optional[str] = Field(
        None,
        max_length=100,
        description="User location"
    )
    website: Optional[str] = Field(
        None,
        max_length=255,
        description="User website URL"
    )
    phone_number: Optional[str] = Field(
        None,
        max_length=20,
        description="User phone number"
    )
    
    @field_validator("bio")
    @classmethod
    def validate_bio(cls, v: Optional[str]) -> Optional[str]:
        """Validate bio length."""
        if v and len(v) > 500:
            raise ValueError("Bio must not exceed 500 characters")
        return v


class UserProfileCreate(UserProfileBase):
    """Schema for creating user profile."""
    
    user_id: str = Field(..., description="User ID from auth-service")


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile (all fields optional)."""
    
    display_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="User display name"
    )
    bio: Optional[str] = Field(None, max_length=500, description="User biography")
    location: Optional[str] = Field(None, max_length=100, description="User location")
    website: Optional[str] = Field(None, max_length=255, description="User website URL")
    phone_number: Optional[str] = Field(None, max_length=20, description="User phone number")


class UserProfileResponse(UserProfileBase):
    """Schema for user profile response."""
    
    id: str = Field(..., description="Profile ID")
    user_id: str = Field(..., description="User ID from auth-service")
    avatar_url: Optional[str] = Field(None, description="Avatar image URL")
    is_verified: bool = Field(..., description="Email verification status")
    is_active: bool = Field(..., description="Account active status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
    last_login_at: Optional[datetime] = Field(None, description="Last login timestamp")
    
    model_config = {"from_attributes": True}


class UserProfileWithPreferences(UserProfileResponse):
    """Schema for user profile with preferences."""
    
    preferences: Optional["UserPreferenceResponse"] = Field(None, description="User preferences")


# Forward reference resolution
from .user_preference import UserPreferenceResponse
UserProfileWithPreferences.model_rebuild()
