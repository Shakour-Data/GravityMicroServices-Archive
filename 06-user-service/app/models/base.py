"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : base.py
Description  : SQLAlchemy declarative base
Language     : English (UK)
Framework    : SQLAlchemy 2.0+ / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Elena Volkov (Backend & Integration Lead)
Contributors      : Dr. Sarah Chen (Chief Architect)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-08 08:30 UTC
Last Modified     : 2025-11-08 08:30 UTC
Development Time  : 0 hours 15 minutes
Total Cost        : 0.25 × $150 = $37.50 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial base implementation

================================================================================
DEPENDENCIES
================================================================================
Internal  : None
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

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    SQLAlchemy declarative base for all models.
    
    All database models inherit from this base class.
    Uses SQLAlchemy 2.0 declarative mapping style with type annotations.
    """
    pass
