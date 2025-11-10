"""
Example Schemas
Replace with your actual schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ExampleBase(BaseModel):
    """Base example schema"""

    title: str = Field(..., min_length=1, max_length=255, description="Example title")
    description: Optional[str] = Field(None, description="Example description")
    is_active: bool = Field(default=True, description="Whether the example is active")


class ExampleCreate(ExampleBase):
    """Schema for creating an example"""

    pass


class ExampleUpdate(BaseModel):
    """Schema for updating an example"""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ExampleResponse(ExampleBase):
    """Schema for example response"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
