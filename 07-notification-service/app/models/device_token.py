"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - Notification Service
File         : device_token.py
Description  : Device token model for push notifications
Language     : Python 3.11+

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
================================================================================
"""

from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base
from app.models.base import BaseModel
import enum


class DevicePlatform(str, enum.Enum):
    """Device platforms for push notifications."""
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"


class DeviceToken(Base, BaseModel):
    """
    Device token model for push notification registration.
    
    Attributes:
        id: Unique device token ID
        user_id: Owner user ID
        token: FCM or APNs device token
        platform: Device platform (ios, android, web)
        device_info: Additional device information (JSONB)
        is_active: Whether token is active
        last_used_at: Last time token was used
    """
    
    __tablename__ = "device_tokens"
    
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    token = Column(String(255), nullable=False, unique=True, index=True)
    platform = Column(
        SQLEnum(DevicePlatform, name="device_platform"),
        nullable=False
    )
    device_info = Column(JSONB, nullable=True, default={})
    is_active = Column(Boolean, default=True, nullable=False)
    last_used_at = Column(DateTime, nullable=True)
    
    def __repr__(self) -> str:
        return f"<DeviceToken {self.token[:20]}... ({self.platform})>"
    
    def update_last_used(self) -> None:
        """Update last used timestamp."""
        self.last_used_at = datetime.utcnow()
