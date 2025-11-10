"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : user_preference.py
Description  : User preference Pydantic schemas
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
Created Date      : 2025-11-08 11:30 UTC
Last Modified     : 2025-11-08 11:30 UTC
Development Time  : 0 hours 30 minutes
Total Cost        : 0.5 × $150 = $75.00 USD

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
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class UserPreferenceBase(BaseModel):
    """Base user preference schema with common fields."""
    
    language: str = Field(default="en", description="Preferred language (ISO 639-1)")
    timezone: str = Field(default="UTC", description="User timezone (IANA timezone)")
    theme: str = Field(default="auto", description="UI theme (light/dark/auto)")
    date_format: str = Field(default="YYYY-MM-DD", description="Date format preference")
    time_format: str = Field(default="24h", description="Time format (12h/24h)")
    email_notifications: bool = Field(default=True, description="Enable email notifications")
    push_notifications: bool = Field(default=True, description="Enable push notifications")
    sms_notifications: bool = Field(default=False, description="Enable SMS notifications")
    newsletter: bool = Field(default=False, description="Subscribe to newsletter")
    marketing: bool = Field(default=False, description="Subscribe to marketing emails")
    custom_settings: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional custom settings"
    )


class UserPreferenceCreate(UserPreferenceBase):
    """Schema for creating user preference."""
    
    profile_id: str = Field(..., description="Profile ID")


class UserPreferenceUpdate(BaseModel):
    """Schema for updating user preference (all fields optional)."""
    
    language: Optional[str] = Field(None, description="Preferred language")
    timezone: Optional[str] = Field(None, description="User timezone")
    theme: Optional[str] = Field(None, description="UI theme")
    date_format: Optional[str] = Field(None, description="Date format preference")
    time_format: Optional[str] = Field(None, description="Time format")
    email_notifications: Optional[bool] = Field(None, description="Enable email notifications")
    push_notifications: Optional[bool] = Field(None, description="Enable push notifications")
    sms_notifications: Optional[bool] = Field(None, description="Enable SMS notifications")
    newsletter: Optional[bool] = Field(None, description="Subscribe to newsletter")
    marketing: Optional[bool] = Field(None, description="Subscribe to marketing emails")
    custom_settings: Optional[Dict[str, Any]] = Field(None, description="Custom settings")


class UserPreferenceResponse(UserPreferenceBase):
    """Schema for user preference response."""
    
    id: str = Field(..., description="Preference ID")
    profile_id: str = Field(..., description="Profile ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
    
    model_config = {"from_attributes": True}
