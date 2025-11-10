"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : exceptions.py
Description  : Custom exceptions for user service
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
Created Date      : 2025-11-08 13:30 UTC
Last Modified     : 2025-11-08 13:30 UTC
Development Time  : 0 hours 30 minutes
Total Cost        : 0.5 × $150 = $75.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial exceptions

================================================================================
DEPENDENCIES
================================================================================
Internal  : None
External  : fastapi

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

from typing import Any, Optional
from fastapi import HTTPException, status


class UserServiceException(HTTPException):
    """Base exception for user service."""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[dict[str, Any]] = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class UserNotFoundException(UserServiceException):
    """Exception raised when user is not found."""
    
    def __init__(self, user_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' not found"
        )


class ProfileNotFoundException(UserServiceException):
    """Exception raised when profile is not found."""
    
    def __init__(self, profile_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with ID '{profile_id}' not found"
        )


class PreferenceNotFoundException(UserServiceException):
    """Exception raised when preference is not found."""
    
    def __init__(self, profile_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Preferences for profile '{profile_id}' not found"
        )


class SessionNotFoundException(UserServiceException):
    """Exception raised when session is not found."""
    
    def __init__(self, session_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID '{session_id}' not found"
        )


class ProfileAlreadyExistsException(UserServiceException):
    """Exception raised when profile already exists for user."""
    
    def __init__(self, user_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Profile already exists for user '{user_id}'"
        )


class UnauthorizedException(UserServiceException):
    """Exception raised when user is unauthorized."""
    
    def __init__(self, detail: str = "Unauthorized") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class ForbiddenException(UserServiceException):
    """Exception raised when access is forbidden."""
    
    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class InvalidAvatarException(UserServiceException):
    """Exception raised when avatar is invalid."""
    
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class MaxSessionsExceededException(UserServiceException):
    """Exception raised when max active sessions exceeded."""
    
    def __init__(self, max_sessions: int) -> None:
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Maximum active sessions ({max_sessions}) exceeded"
        )
