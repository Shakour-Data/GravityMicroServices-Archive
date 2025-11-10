"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : user_preference.py
Description  : User preference database model
Language     : English (UK)
Framework    : SQLAlchemy 2.0+ / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Elena Volkov (Backend & Integration Lead)
Contributors      : Dr. Sarah Chen (Chief Architect)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-08 09:00 UTC
Last Modified     : 2025-11-08 09:00 UTC
Development Time  : 0 hours 45 minutes
Total Cost        : 0.75 × $150 = $112.50 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial model implementation

================================================================================
DEPENDENCIES
================================================================================
Internal  : user_profile.py
External  : sqlalchemy
Database  : PostgreSQL 16+

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, Boolean, ForeignKey, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base

if TYPE_CHECKING:
    from .user_profile import UserProfile


class UserPreference(Base):
    """
    User preference model storing user settings and preferences.
    
    Each user has exactly one preference record. Contains UI preferences,
    notification settings, and other customization options.
    
    Attributes:
        id: Primary key (UUID v4)
        profile_id: Foreign key to user_profiles
        language: Preferred language (ISO 639-1 code)
        timezone: User timezone (IANA timezone)
        theme: UI theme (light/dark/auto)
        date_format: Date format preference
        time_format: Time format (12h/24h)
        email_notifications: Enable email notifications
        push_notifications: Enable push notifications
        sms_notifications: Enable SMS notifications
        newsletter: Subscribe to newsletter
        marketing: Subscribe to marketing emails
        custom_settings: JSON field for additional settings
        created_at: Record creation timestamp (UTC)
        updated_at: Record update timestamp (UTC)
    """
    
    __tablename__ = "user_preferences"
    
    # Primary Key
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    
    # Foreign Key
    profile_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
        comment="Foreign key to user_profiles"
    )
    
    # Language & Localization
    language: Mapped[str] = mapped_column(
        String(10),
        default="en",
        nullable=False,
        comment="Preferred language (ISO 639-1)"
    )
    
    timezone: Mapped[str] = mapped_column(
        String(50),
        default="UTC",
        nullable=False,
        comment="User timezone (IANA timezone)"
    )
    
    # UI Preferences
    theme: Mapped[str] = mapped_column(
        String(20),
        default="auto",
        nullable=False,
        comment="UI theme (light/dark/auto)"
    )
    
    date_format: Mapped[str] = mapped_column(
        String(20),
        default="YYYY-MM-DD",
        nullable=False,
        comment="Date format preference"
    )
    
    time_format: Mapped[str] = mapped_column(
        String(10),
        default="24h",
        nullable=False,
        comment="Time format (12h/24h)"
    )
    
    # Notification Preferences
    email_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Enable email notifications"
    )
    
    push_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Enable push notifications"
    )
    
    sms_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Enable SMS notifications"
    )
    
    # Marketing Preferences
    newsletter: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Subscribe to newsletter"
    )
    
    marketing: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Subscribe to marketing emails"
    )
    
    # Custom Settings (JSON)
    custom_settings: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        comment="Additional custom settings (JSON)"
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Record creation timestamp (UTC)"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Record update timestamp (UTC)"
    )
    
    # Relationships
    profile: Mapped["UserProfile"] = relationship(
        "UserProfile",
        back_populates="preferences"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_user_preferences_profile_id", "profile_id"),
        Index("idx_user_preferences_language", "language"),
        Index("idx_user_preferences_timezone", "timezone"),
        {"comment": "User preference settings table"}
    )
    
    def __repr__(self) -> str:
        return f"<UserPreference(id={self.id}, profile_id={self.profile_id}, language={self.language})>"
