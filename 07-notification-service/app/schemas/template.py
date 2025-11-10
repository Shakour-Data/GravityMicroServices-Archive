"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - Notification Service
File         : template.py
Description  : Template Pydantic schemas
Language     : English (UK)
Framework    : Pydantic

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Marcus Chen (Backend & Integration Lead)
Contributors      : Dr. Sarah Chen (Chief Architect)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-09
Development Time  : 30 minutes
Total Cost        : 0.5 × $150 = $75.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-09 - Marcus Chen - Initial template schemas

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
================================================================================
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.models import NotificationType


class TemplateResponse(BaseModel):
    """Template response schema."""
    
    id: UUID
    name: str
    type: NotificationType
    subject: str
    content: str
    html_content: Optional[str] = None
    variables: List[str]
    language: str
    description: Optional[str] = None
    version: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TemplateListResponse(BaseModel):
    """List of templates response."""
    
    templates: List[TemplateResponse]
    total: int
    limit: int
    offset: int
