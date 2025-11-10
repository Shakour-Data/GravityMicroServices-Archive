"""
Custom Exceptions
"""

from typing import Any, Optional


class GravityException(Exception):
    """Base exception for Gravity services"""

    def __init__(
        self,
        detail: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        extra: Optional[dict[str, Any]] = None,
    ):
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        self.extra = extra or {}
        super().__init__(detail)


class NotFoundException(GravityException):
    """Resource not found exception"""

    def __init__(self, detail: str = "Resource not found", **kwargs: Any):
        super().__init__(
            detail=detail,
            status_code=404,
            error_code="NOT_FOUND",
            **kwargs,
        )


class BadRequestException(GravityException):
    """Bad request exception"""

    def __init__(self, detail: str = "Bad request", **kwargs: Any):
        super().__init__(
            detail=detail,
            status_code=400,
            error_code="BAD_REQUEST",
            **kwargs,
        )


class UnauthorizedException(GravityException):
    """Unauthorized exception"""

    def __init__(self, detail: str = "Unauthorized", **kwargs: Any):
        super().__init__(
            detail=detail,
            status_code=401,
            error_code="UNAUTHORIZED",
            **kwargs,
        )


class ForbiddenException(GravityException):
    """Forbidden exception"""

    def __init__(self, detail: str = "Forbidden", **kwargs: Any):
        super().__init__(
            detail=detail,
            status_code=403,
            error_code="FORBIDDEN",
            **kwargs,
        )


class ConflictException(GravityException):
    """Conflict exception"""

    def __init__(self, detail: str = "Conflict", **kwargs: Any):
        super().__init__(
            detail=detail,
            status_code=409,
            error_code="CONFLICT",
            **kwargs,
        )


class ValidationException(GravityException):
    """Validation exception"""

    def __init__(self, detail: str = "Validation error", **kwargs: Any):
        super().__init__(
            detail=detail,
            status_code=422,
            error_code="VALIDATION_ERROR",
            **kwargs,
        )


class ServiceUnavailableException(GravityException):
    """Service unavailable exception"""

    def __init__(self, detail: str = "Service temporarily unavailable", **kwargs: Any):
        super().__init__(
            detail=detail,
            status_code=503,
            error_code="SERVICE_UNAVAILABLE",
            **kwargs,
        )


class DatabaseException(GravityException):
    """Database operation exception"""

    def __init__(self, detail: str = "Database error", **kwargs: Any):
        super().__init__(
            detail=detail,
            status_code=500,
            error_code="DATABASE_ERROR",
            **kwargs,
        )


class CacheException(GravityException):
    """Cache operation exception"""

    def __init__(self, detail: str = "Cache error", **kwargs: Any):
        super().__init__(
            detail=detail,
            status_code=500,
            error_code="CACHE_ERROR",
            **kwargs,
        )


class ExternalServiceException(GravityException):
    """External service call exception"""

    def __init__(self, detail: str = "External service error", **kwargs: Any):
        super().__init__(
            detail=detail,
            status_code=502,
            error_code="EXTERNAL_SERVICE_ERROR",
            **kwargs,
        )


class RateLimitException(GravityException):
    """Rate limit exceeded exception"""

    def __init__(self, detail: str = "Rate limit exceeded", **kwargs: Any):
        super().__init__(
            detail=detail,
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
            **kwargs,
        )
