"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : security.py
Description  : Security utilities (JWT validation, authentication)
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
Created Date      : 2025-11-08 13:45 UTC
Last Modified     : 2025-11-08 15:30 UTC
Development Time  : 2 hours 0 minutes
Total Cost        : 2.0 × $150 = $300.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial security implementation
v1.1.0 - 2025-11-08 - GitHub Copilot - Auth Service integration

================================================================================
DEPENDENCIES
================================================================================
Internal  : config, exceptions, service_discovery
External  : fastapi, jose, pydantic, httpx

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

from typing import Optional
from datetime import datetime, timezone
import logging
from fastapi import Depends, Header
from jose import JWTError, jwt
from pydantic import BaseModel
import httpx

from app.config import settings
from app.core.exceptions import UnauthorizedException
from app.core.service_discovery import get_auth_service_url

logger = logging.getLogger(__name__)


class TokenData(BaseModel):
    """JWT token data."""
    
    user_id: str
    email: str
    exp: datetime
    iat: datetime
    jti: Optional[str] = None


class CurrentUser(BaseModel):
    """Current authenticated user."""
    
    user_id: str
    email: str
    username: Optional[str] = None
    token_id: Optional[str] = None


async def validate_token_with_auth_service(token: str) -> dict:
    """
    Validate JWT token with Auth Service.
    
    Args:
        token: JWT token to validate
        
    Returns:
        dict: Token payload from Auth Service
        
    Raises:
        UnauthorizedException: If token is invalid
    """
    try:
        auth_service_url = await get_auth_service_url()
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{auth_service_url}/api/v1/auth/validate",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                return await response.json()
            elif response.status_code == 401:
                raise UnauthorizedException("Token validation failed: Invalid or expired token")
            else:
                logger.error(f"Auth Service returned {response.status_code}: {response.text}")
                raise UnauthorizedException("Token validation failed")
                
    except httpx.TimeoutException:
        logger.error("Auth Service timeout")
        # Fallback to local validation if Auth Service is unavailable
        return validate_token_locally(token)
    except httpx.RequestError as e:
        logger.error(f"Auth Service request error: {e}")
        # Fallback to local validation
        return validate_token_locally(token)


def validate_token_locally(token: str) -> dict:
    """
    Validate JWT token locally (fallback).
    
    Args:
        token: JWT token to validate
        
    Returns:
        dict: Token payload
        
    Raises:
        UnauthorizedException: If token is invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Check expiration
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise UnauthorizedException("Token has expired")
        
        logger.warning("⚠️ Using local token validation (Auth Service unavailable)")
        return payload
        
    except JWTError as e:
        raise UnauthorizedException(f"Could not validate credentials: {str(e)}")


async def get_current_user(
    authorization: str = Header(..., description="Bearer token")
) -> CurrentUser:
    """
    Get current authenticated user from JWT token.
    
    Validates token with Auth Service, falls back to local validation if unavailable.
    
    Args:
        authorization: Authorization header with Bearer token
        
    Returns:
        CurrentUser: Current user information
        
    Raises:
        UnauthorizedException: If token is invalid or expired
    """
    # Extract token from Authorization header
    if not authorization.startswith("Bearer "):
        raise UnauthorizedException("Invalid authorization header format")
    
    token = authorization.replace("Bearer ", "")
    
    try:
        # Validate with Auth Service (with fallback)
        payload = await validate_token_with_auth_service(token)
        
        # Extract user data
        user_id = payload.get("sub") or payload.get("user_id")
        email = payload.get("email")
        username = payload.get("username")
        jti = payload.get("jti")
        
        if not user_id or not email:
            raise UnauthorizedException("Invalid token payload: missing user_id or email")
        
        return CurrentUser(
            user_id=str(user_id),
            email=str(email),
            username=str(username) if username else None,
            token_id=str(jti) if jti else None
        )
        
    except UnauthorizedException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during token validation: {e}")
        raise UnauthorizedException("Could not validate credentials")


async def get_optional_user(
    authorization: Optional[str] = Header(None, description="Bearer token")
) -> Optional[CurrentUser]:
    """
    Get current user if authenticated, otherwise return None.
    
    Args:
        authorization: Optional authorization header
        
    Returns:
        Optional[CurrentUser]: Current user or None
    """
    if not authorization:
        return None
    
    try:
        return await get_current_user(authorization)
    except UnauthorizedException:
        return None
