"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : __init__.py
Description  : Services package initialization
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
Created Date      : 2025-11-08 16:00 UTC
Last Modified     : 2025-11-08 16:00 UTC
Development Time  : 0 hours 15 minutes
Total Cost        : 0.25 × $150 = $37.50 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial package setup

================================================================================
DEPENDENCIES
================================================================================
Internal  : profile_service, preference_service, session_service
External  : None

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

from .profile_service import ProfileService
from .preference_service import PreferenceService
from .session_service import SessionService

__all__ = [
    "ProfileService",
    "PreferenceService",
    "SessionService",
]
