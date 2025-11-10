"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : __init__.py
Description  : Core package initialization
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
Created Date      : 2025-11-08 12:20 UTC
Last Modified     : 2025-11-08 12:20 UTC
Development Time  : 0 hours 10 minutes
Total Cost        : 0.17 × $150 = $25.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial package setup

================================================================================
DEPENDENCIES
================================================================================
Internal  : database
External  : None

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

from .database import get_db, init_db, close_db, engine, AsyncSessionLocal

__all__ = [
    "get_db",
    "init_db",
    "close_db",
    "engine",
    "AsyncSessionLocal",
]
