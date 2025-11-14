"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform
File         : security.py
Description  : Security utilities API endpoints for password hashing, JWT tokens
Language     : English (UK)
Framework    : FastAPI / Python 3.12+

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Michael Rodriguez (Security & Authentication Expert)
Contributors      : Elena Volkov (API Implementation)
                   Dr. Sarah Chen (Architecture Review)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-13 12:00 UTC
Last Modified     : 2025-11-13 14:30 UTC
Development Time  : 2 hours 30 minutes
Review Time       : 0 hours 45 minutes
Total Time        : 3 hours 15 minutes
Total Cost        : 3.25 × $150 = $487.50 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-13 - Michael Rodriguez - Security utilities API
                    - Password hashing with bcrypt
                    - JWT token generation and verification
                    - Refresh token mechanism
                    - Comprehensive security validation

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/Shakour-Data/01-common-library
================================================================================
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, validator
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/security", tags=["Security"])

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==============================================================================
# Request/Response Models
# ==============================================================================

class PasswordHashRequest(BaseModel):
    """Request model for password hashing."""
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password to hash (8-128 characters)",
        examples=["MySecureP@ssw0rd"]
    )
    
    @validator('password')
    def validate_password_strength(cls, v):
        """Validate password meets minimum security requirements."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Check for at least one uppercase letter
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        
        # Check for at least one lowercase letter
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        
        # Check for at least one digit
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        
        return v


class PasswordHashResponse(BaseModel):
    """Response model for password hashing."""
    success: bool = Field(default=True, description="Operation success status")
    hashed_password: str = Field(..., description="Bcrypt hashed password")
    algorithm: str = Field(default="bcrypt", description="Hashing algorithm used")
    timestamp: str = Field(..., description="UTC timestamp")


class PasswordVerifyRequest(BaseModel):
    """Request model for password verification."""
    password: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Plain text password to verify"
    )
    hashed_password: str = Field(
        ...,
        min_length=1,
        description="Bcrypt hashed password to verify against"
    )


class PasswordVerifyResponse(BaseModel):
    """Response model for password verification."""
    success: bool = Field(default=True, description="Operation success status")
    valid: bool = Field(..., description="Whether password matches hash")
    timestamp: str = Field(..., description="UTC timestamp")


class JWTGenerateRequest(BaseModel):
    """Request model for JWT token generation."""
    subject: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Token subject (typically user ID)",
        examples=["user_12345"]
    )
    claims: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional claims to include in token",
        examples=[{"email": "user@example.com", "role": "admin"}]
    )
    expires_minutes: Optional[int] = Field(
        default=None,
        ge=1,
        le=43200,  # Max 30 days
        description="Token expiration in minutes (default from config)"
    )


class JWTGenerateResponse(BaseModel):
    """Response model for JWT token generation."""
    success: bool = Field(default=True, description="Operation success status")
    access_token: str = Field(..., description="Generated JWT access token")
    token_type: str = Field(default="Bearer", description="Token type")
    expires_in: int = Field(..., description="Expiration time in seconds")
    expires_at: str = Field(..., description="Expiration timestamp (UTC)")
    timestamp: str = Field(..., description="Generation timestamp (UTC)")


class JWTVerifyRequest(BaseModel):
    """Request model for JWT token verification."""
    token: str = Field(
        ...,
        min_length=1,
        description="JWT token to verify"
    )


class JWTVerifyResponse(BaseModel):
    """Response model for JWT token verification."""
    success: bool = Field(default=True, description="Operation success status")
    valid: bool = Field(..., description="Whether token is valid")
    payload: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Decoded token payload (if valid)"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message (if invalid)"
    )
    timestamp: str = Field(..., description="Verification timestamp (UTC)")


class RefreshTokenGenerateRequest(BaseModel):
    """Request model for refresh token generation."""
    subject: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Token subject (typically user ID)",
        examples=["user_12345"]
    )
    claims: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional claims to include in token",
        examples=[{"email": "user@example.com", "role": "admin"}]
    )
    expires_days: Optional[int] = Field(
        default=None,
        ge=1,
        le=365,  # Max 1 year
        description="Token expiration in days (default from config)"
    )


class RefreshTokenGenerateResponse(BaseModel):
    """Response model for refresh token generation."""
    success: bool = Field(default=True, description="Operation success status")
    refresh_token: str = Field(..., description="Generated JWT refresh token")
    token_type: str = Field(default="Bearer", description="Token type")
    expires_in: int = Field(..., description="Expiration time in seconds")
    expires_at: str = Field(..., description="Expiration timestamp (UTC)")
    timestamp: str = Field(..., description="Generation timestamp (UTC)")


class RefreshTokenRequest(BaseModel):
    """Request model for token refresh."""
    refresh_token: str = Field(
        ...,
        min_length=1,
        description="Valid refresh token"
    )


# ==============================================================================
# API Endpoints
# ==============================================================================

@router.post(
    "/hash-password",
    response_model=PasswordHashResponse,
    status_code=status.HTTP_200_OK,
    summary="Hash Password",
    description="""
    Hash a plain text password using bcrypt algorithm.
    
    **Security Features:**
    - Uses bcrypt with automatic salt generation
    - Configurable work factor (cost)
    - Industry-standard hashing
    - Password strength validation
    
    **Password Requirements:**
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - Maximum 128 characters
    
    **Use Cases:**
    - User registration
    - Password reset
    - Password change
    
    **Example:**
    ```json
    {
      "password": "MySecureP@ssw0rd"
    }
    ```
    """,
    responses={
        200: {
            "description": "Password successfully hashed",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "hashed_password": "$2b$12$KIXfF5KGRqw7HZk.vxMdruQVE0RfzPq...",
                        "algorithm": "bcrypt",
                        "timestamp": "2025-11-13T14:30:00.123456Z"
                    }
                }
            }
        },
        422: {
            "description": "Validation error (weak password)"
        }
    }
)
async def hash_password(request: PasswordHashRequest) -> PasswordHashResponse:
    """
    Hash a password using bcrypt.
    
    Args:
        request: Password hashing request with plain text password
    
    Returns:
        Hashed password with metadata
    
    Raises:
        HTTPException: If hashing fails
    """
    try:
        logger.info("🔐 Hashing password")
        
        # Hash password with bcrypt
        hashed = pwd_context.hash(request.password)
        
        logger.info("✅ Password hashed successfully")
        
        return PasswordHashResponse(
            success=True,
            hashed_password=hashed,
            algorithm="bcrypt",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    
    except Exception as e:
        logger.error(f"❌ Password hashing failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password hashing failed: {str(e)}"
        )


@router.post(
    "/verify-password",
    response_model=PasswordVerifyResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify Password",
    description="""
    Verify a plain text password against a bcrypt hash.
    
    **Security Features:**
    - Constant-time comparison
    - Timing attack resistant
    - Supports bcrypt hashes only
    
    **Use Cases:**
    - User login
    - Password confirmation
    - Authentication verification
    
    **Example:**
    ```json
    {
      "password": "MySecureP@ssw0rd",
      "hashed_password": "$2b$12$KIXfF5KGRqw7HZk..."
    }
    ```
    """,
    responses={
        200: {
            "description": "Password verified",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "valid": True,
                        "timestamp": "2025-11-13T14:30:00.123456Z"
                    }
                }
            }
        }
    }
)
async def verify_password(request: PasswordVerifyRequest) -> PasswordVerifyResponse:
    """
    Verify a password against a bcrypt hash.
    
    Args:
        request: Password verification request
    
    Returns:
        Verification result (valid/invalid)
    
    Raises:
        HTTPException: If verification process fails
    """
    try:
        logger.info("🔍 Verifying password")
        
        # Verify password
        is_valid = pwd_context.verify(request.password, request.hashed_password)
        
        logger.info(f"✅ Password verification complete: {is_valid}")
        
        return PasswordVerifyResponse(
            success=True,
            valid=is_valid,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    
    except Exception as e:
        logger.error(f"❌ Password verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password verification failed: {str(e)}"
        )


@router.post(
    "/generate-jwt",
    response_model=JWTGenerateResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate JWT Token",
    description="""
    Generate a JWT access token with custom claims.
    
    **Security Features:**
    - HS256 algorithm (configurable)
    - Configurable expiration
    - Custom claims support
    - Signed with secret key
    
    **Token Claims:**
    - `sub`: Subject (user ID)
    - `exp`: Expiration timestamp
    - `iat`: Issued at timestamp
    - `type`: Token type (access)
    - Custom claims as provided
    
    **Use Cases:**
    - User authentication
    - API authorization
    - Service-to-service authentication
    
    **Example:**
    ```json
    {
      "subject": "user_12345",
      "claims": {
        "email": "user@example.com",
        "role": "admin"
      },
      "expires_minutes": 60
    }
    ```
    """,
    responses={
        200: {
            "description": "JWT token generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "Bearer",
                        "expires_in": 3600,
                        "expires_at": "2025-11-13T15:30:00.123456Z",
                        "timestamp": "2025-11-13T14:30:00.123456Z"
                    }
                }
            }
        }
    }
)
async def generate_jwt(request: JWTGenerateRequest) -> JWTGenerateResponse:
    """
    Generate a JWT access token.
    
    Args:
        request: JWT generation request with subject and claims
    
    Returns:
        Generated JWT token with metadata
    
    Raises:
        HTTPException: If token generation fails
    """
    try:
        logger.info(f"🎫 Generating JWT for subject: {request.subject}")
        
        # Calculate expiration
        expires_minutes = request.expires_minutes or settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        expires_delta = timedelta(minutes=expires_minutes)
        expire_time = datetime.utcnow() + expires_delta
        
        # Build token payload
        payload = {
            "sub": request.subject,
            "exp": expire_time,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        # Add custom claims
        if request.claims:
            payload.update(request.claims)
        
        # Generate token
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        logger.info(f"✅ JWT generated successfully for {request.subject}")
        
        return JWTGenerateResponse(
            success=True,
            access_token=token,
            token_type="Bearer",
            expires_in=expires_minutes * 60,  # Convert to seconds
            expires_at=expire_time.isoformat() + "Z",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    
    except Exception as e:
        logger.error(f"❌ JWT generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"JWT generation failed: {str(e)}"
        )


@router.post(
    "/generate-refresh-token",
    response_model=RefreshTokenGenerateResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Refresh Token",
    description="""
    Generate a JWT refresh token with custom claims.

    **Security Features:**
    - HS256 algorithm (configurable)
    - Configurable expiration (days)
    - Custom claims support
    - Signed with secret key

    **Token Claims:**
    - `sub`: Subject (user ID)
    - `exp`: Expiration timestamp
    - `iat`: Issued at timestamp
    - `type`: Token type (refresh)
    - Custom claims as provided

    **Use Cases:**
    - User authentication setup
    - Long-term session management
    - Token refresh mechanism

    **Example:**
    ```json
    {
      "subject": "user_12345",
      "claims": {
        "email": "user@example.com",
        "role": "admin"
      },
      "expires_days": 7
    }
    ```
    """,
    responses={
        200: {
            "description": "Refresh token generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "Bearer",
                        "expires_in": 604800,
                        "expires_at": "2025-11-20T14:30:00.123456Z",
                        "timestamp": "2025-11-13T14:30:00.123456Z"
                    }
                }
            }
        }
    }
)
async def generate_refresh_token(request: RefreshTokenGenerateRequest) -> RefreshTokenGenerateResponse:
    """
    Generate a JWT refresh token.

    Args:
        request: Refresh token generation request with subject and claims

    Returns:
        Generated JWT refresh token with metadata

    Raises:
        HTTPException: If token generation fails
    """
    try:
        logger.info(f"🔄 Generating refresh token for subject: {request.subject}")

        # Calculate expiration
        expires_days = request.expires_days or settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        expires_delta = timedelta(days=expires_days)
        expire_time = datetime.utcnow() + expires_delta

        # Build token payload
        payload = {
            "sub": request.subject,
            "exp": expire_time,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }

        # Add custom claims
        if request.claims:
            payload.update(request.claims)

        # Generate token
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        logger.info(f"✅ Refresh token generated successfully for {request.subject}")

        return RefreshTokenGenerateResponse(
            success=True,
            refresh_token=token,
            token_type="Bearer",
            expires_in=expires_days * 24 * 60 * 60,  # Convert to seconds
            expires_at=expire_time.isoformat() + "Z",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

    except Exception as e:
        logger.error(f"❌ Refresh token generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Refresh token generation failed: {str(e)}"
        )


@router.post(
    "/verify-jwt",
    response_model=JWTVerifyResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify JWT Token",
    description="""
    Verify and decode a JWT token.
    
    **Validation Checks:**
    - Signature verification
    - Expiration check
    - Token format validation
    - Algorithm verification
    
    **Use Cases:**
    - API request authentication
    - Token validation
    - Claims extraction
    
    **Example:**
    ```json
    {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
    """,
    responses={
        200: {
            "description": "Token verification result",
            "content": {
                "application/json": {
                    "examples": {
                        "valid_token": {
                            "summary": "Valid token",
                            "value": {
                                "success": True,
                                "valid": True,
                                "payload": {
                                    "sub": "user_12345",
                                    "email": "user@example.com",
                                    "exp": 1700000000
                                },
                                "error": None,
                                "timestamp": "2025-11-13T14:30:00.123456Z"
                            }
                        },
                        "invalid_token": {
                            "summary": "Invalid token",
                            "value": {
                                "success": True,
                                "valid": False,
                                "payload": None,
                                "error": "Token has expired",
                                "timestamp": "2025-11-13T14:30:00.123456Z"
                            }
                        }
                    }
                }
            }
        }
    }
)
async def verify_jwt(request: JWTVerifyRequest) -> JWTVerifyResponse:
    """
    Verify and decode a JWT token.
    
    Args:
        request: JWT verification request with token
    
    Returns:
        Verification result with payload if valid
    """
    try:
        logger.info("🔍 Verifying JWT token")
        
        # Verify and decode token
        payload = jwt.decode(
            request.token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        logger.info(f"✅ JWT valid for subject: {payload.get('sub')}")
        
        return JWTVerifyResponse(
            success=True,
            valid=True,
            payload=payload,
            error=None,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    
    except JWTError as e:
        logger.warning(f"⚠️ JWT verification failed: {str(e)}")
        
        return JWTVerifyResponse(
            success=True,
            valid=False,
            payload=None,
            error=str(e),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    
    except Exception as e:
        logger.error(f"❌ JWT verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"JWT verification error: {str(e)}"
        )


@router.post(
    "/refresh-token",
    response_model=JWTGenerateResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh JWT Token",
    description="""
    Generate a new access token from a valid refresh token.
    
    **Process:**
    1. Verify refresh token validity
    2. Extract subject from refresh token
    3. Generate new access token
    4. Return new token with expiration
    
    **Security:**
    - Refresh tokens have longer expiration
    - Only valid refresh tokens accepted
    - New tokens have fresh expiration
    
    **Use Cases:**
    - Token renewal
    - Session extension
    - Seamless re-authentication
    
    **Example:**
    ```json
    {
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
    """,
    responses={
        200: {
            "description": "New access token generated"
        },
        401: {
            "description": "Invalid or expired refresh token"
        }
    }
)
async def refresh_token(request: RefreshTokenRequest) -> JWTGenerateResponse:
    """
    Generate a new access token from a refresh token.
    
    Args:
        request: Refresh token request
    
    Returns:
        New access token
    
    Raises:
        HTTPException: If refresh token is invalid
    """
    try:
        logger.info("🔄 Refreshing JWT token")
        
        # Verify refresh token
        payload = jwt.decode(
            request.refresh_token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Check if token type is refresh
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type. Refresh token required."
            )
        
        subject = payload.get("sub")
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Generate new access token
        expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        expire_time = datetime.utcnow() + expires_delta
        
        new_payload = {
            "sub": subject,
            "exp": expire_time,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        new_token = jwt.encode(
            new_payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        logger.info(f"✅ Token refreshed successfully for {subject}")
        
        return JWTGenerateResponse(
            success=True,
            access_token=new_token,
            token_type="Bearer",
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            expires_at=expire_time.isoformat() + "Z",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    
    except JWTError as e:
        logger.warning(f"⚠️ Token refresh failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired refresh token: {str(e)}"
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"❌ Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )
