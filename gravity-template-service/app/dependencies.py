"""
FastAPI Dependencies
Common dependencies for dependency injection
"""

from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.redis_client import get_redis_client
from app.core.security import decode_access_token

# Security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Get current authenticated user from JWT token

    Args:
        credentials: HTTP Bearer token

    Returns:
        User information from token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """
    Get current active user (must not be disabled)

    Args:
        current_user: Current user from token

    Returns:
        Active user information

    Raises:
        HTTPException: If user is disabled
    """
    if current_user.get("disabled", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


async def get_current_admin_user(
    current_user: dict = Depends(get_current_active_user),
) -> dict:
    """
    Get current admin user (must have admin role)

    Args:
        current_user: Current active user

    Returns:
        Admin user information

    Raises:
        HTTPException: If user is not admin
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user


class PaginationParams:
    """Pagination parameters"""

    def __init__(
        self,
        skip: int = 0,
        limit: int = 100,
    ):
        self.skip = max(0, skip)
        self.limit = min(1000, max(1, limit))


def get_pagination_params(
    skip: int = 0,
    limit: int = 100,
) -> PaginationParams:
    """
    Get pagination parameters

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        PaginationParams instance
    """
    return PaginationParams(skip=skip, limit=limit)


# Optional dependencies for specific use cases
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session (alias for get_db)"""
    async for session in get_db():
        yield session


async def get_redis() -> AsyncGenerator:
    """Get Redis client"""
    return await get_redis_client()
