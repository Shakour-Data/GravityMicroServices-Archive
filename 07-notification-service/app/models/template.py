"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - Notification Service
File         : template.py
Description  : Template model for notification templates
Language     : Python 3.11+

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
================================================================================
"""

from sqlalchemy import Column, String, Text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB, ENUM
from app.core.database import Base
from app.models.base import BaseModel
from app.models.notification import NotificationType


class Template(Base, BaseModel):
    """
    Template model for reusable notification templates.
    
    Attributes:
        id: Unique template ID
        name: Template name (unique)
        type: Template type (email, sms, push)
        subject: Email subject or notification title template
        content: Plain text content template
        html_content: HTML content template (for emails)
        variables: Available variables (JSONB array)
        language: Template language code (en, fa, etc.)
        is_active: Whether template is active
        version: Template version number
        created_by: User ID who created the template
    """
    
    __tablename__ = "templates"
    
    name = Column(String(100), nullable=False, unique=True, index=True)
    type = Column(
        ENUM(NotificationType, name="notification_type"),
        nullable=False,
        index=True
    )
    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    html_content = Column(Text, nullable=True)
    variables = Column(JSONB, nullable=True, default=[])
    language = Column(String(10), default="en", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    
    def __repr__(self) -> str:
        return f"<Template {self.name} ({self.type})>"
