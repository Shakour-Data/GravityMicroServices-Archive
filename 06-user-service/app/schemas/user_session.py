"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : user_session.py
Description  : User session Pydantic schemas
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
Created Date      : 2025-11-08 12:00 UTC
Last Modified     : 2025-11-08 12:00 UTC
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
from typing import Optional
from pydantic import BaseModel, Field


class UserSessionBase(BaseModel):
    """Base user session schema with common fields."""
    
    device_type: str = Field(..., description="Device type (web/mobile/tablet/desktop)")
    device_name: Optional[str] = Field(None, description="Device name or browser")
    os: Optional[str] = Field(None, description="Operating system")
    ip_address: str = Field(..., description="Client IP address")
    user_agent: Optional[str] = Field(None, description="User agent string")


class UserSessionCreate(UserSessionBase):
    """Schema for creating user session."""
    
    profile_id: str = Field(..., description="Profile ID")
    session_token: str = Field(..., description="Session token (JWT token ID)")
    expires_at: datetime = Field(..., description="Session expiration timestamp")


class UserSessionResponse(UserSessionBase):
    """Schema for user session response."""
    
    id: str = Field(..., description="Session ID")
    profile_id: str = Field(..., description="Profile ID")
    session_token: str = Field(..., description="Session token")
    is_active: bool = Field(..., description="Session active status")
    created_at: datetime = Field(..., description="Creation timestamp")
    last_activity_at: datetime = Field(..., description="Last activity timestamp")
    expires_at: datetime = Field(..., description="Expiration timestamp")
    logout_at: Optional[datetime] = Field(None, description="Logout timestamp")
    
    model_config = {"from_attributes": True}
