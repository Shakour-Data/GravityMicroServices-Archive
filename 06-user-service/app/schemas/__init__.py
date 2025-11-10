"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : __init__.py
Description  : Schemas package initialization
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
Created Date      : 2025-11-08 12:15 UTC
Last Modified     : 2025-11-08 12:15 UTC
Development Time  : 0 hours 15 minutes
Total Cost        : 0.25 × $150 = $37.50 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial package setup

================================================================================
DEPENDENCIES
================================================================================
Internal  : user_profile, user_preference, user_session
External  : None

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

from .user_profile import (
    UserProfileBase,
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserProfileWithPreferences,
)
from .user_preference import (
    UserPreferenceBase,
    UserPreferenceCreate,
    UserPreferenceUpdate,
    UserPreferenceResponse,
)
from .user_session import (
    UserSessionBase,
    UserSessionCreate,
    UserSessionResponse,
)

__all__ = [
    # User Profile
    "UserProfileBase",
    "UserProfileCreate",
    "UserProfileUpdate",
    "UserProfileResponse",
    "UserProfileWithPreferences",
    # User Preference
    "UserPreferenceBase",
    "UserPreferenceCreate",
    "UserPreferenceUpdate",
    "UserPreferenceResponse",
    # User Session
    "UserSessionBase",
    "UserSessionCreate",
    "UserSessionResponse",
]
