"""
Standard Response Schemas
"""

from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    """
    Standard API response wrapper

    Example:
        {
            "success": true,
            "message": "Operation successful",
            "data": {...}
        }
    """

    success: bool = Field(default=True, description="Whether the operation was successful")
    message: str = Field(default="Success", description="Response message")
    data: Optional[T] = Field(default=None, description="Response data")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Paginated response wrapper

    Example:
        {
            "items": [...],
            "total": 100,
            "skip": 0,
            "limit": 10,
            "has_more": true
        }
    """

    items: List[T] = Field(default_factory=list, description="List of items")
    total: int = Field(..., description="Total number of items")
    skip: int = Field(default=0, description="Number of skipped items")
    limit: int = Field(default=100, description="Maximum items returned")

    @property
    def has_more(self) -> bool:
        """Check if there are more items"""
        return self.skip + len(self.items) < self.total


class ErrorResponse(BaseModel):
    """
    Error response schema

    Example:
        {
            "detail": "Error message",
            "error_code": "ERROR_CODE",
            "extra": {...}
        }
    """

    detail: str = Field(..., description="Error detail message")
    error_code: str = Field(..., description="Error code")
    extra: Optional[dict[str, Any]] = Field(default=None, description="Additional error information")
