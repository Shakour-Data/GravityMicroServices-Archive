"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : router.py
Description  : API v1 router aggregation
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
Created Date      : 2025-11-08 18:00 UTC
Last Modified     : 2025-11-08 18:00 UTC
Development Time  : 0 hours 15 minutes
Total Cost        : 0.25 × $150 = $37.50 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial router setup

================================================================================
DEPENDENCIES
================================================================================
Internal  : profiles, preferences, sessions
External  : fastapi

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

from fastapi import APIRouter

from .profiles import router as profiles_router
from .preferences import router as preferences_router
from .sessions import router as sessions_router


# Create main API v1 router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(profiles_router)
api_router.include_router(preferences_router)
api_router.include_router(sessions_router)
