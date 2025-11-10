"""
Schemas Package
Pydantic schemas for request/response validation
"""

from app.schemas.example import ExampleCreate, ExampleResponse, ExampleUpdate
from app.schemas.response import PaginatedResponse, StandardResponse

__all__ = [
    "ExampleCreate",
    "ExampleUpdate",
    "ExampleResponse",
    "StandardResponse",
    "PaginatedResponse",
]
