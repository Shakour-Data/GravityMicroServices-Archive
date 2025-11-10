"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : user_profile.py
Description  : User profile database model
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
Created Date      : 2025-11-08 08:30 UTC
Last Modified     : 2025-11-08 08:30 UTC
Development Time  : 1 hour 0 minutes
Total Cost        : 1.0 × $150 = $150.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial model implementation

================================================================================
DEPENDENCIES
================================================================================
Internal  : None
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
from sqlalchemy import String, Text, DateTime, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base

if TYPE_CHECKING:
    from .user_preference import UserPreference
    from .user_session import UserSession


class UserProfile(Base):
    """
    User profile model storing extended user information.
    
    Links to auth-service user via user_id. Contains display preferences,
    bio, avatar, and other profile information. Each user has exactly one profile.
    
    Attributes:
        id: Primary key (UUID v4)
        user_id: Foreign key to auth-service user (UUID v4)
        display_name: User's display name (max 100 chars)
        bio: User biography (max 500 chars)
        avatar_url: URL to avatar image in file-service
        location: User location (max 100 chars)
        website: User website URL (max 255 chars)
        phone_number: User phone (max 20 chars)
        is_verified: Email verification status
        is_active: Account active status
        created_at: Record creation timestamp (UTC)
        updated_at: Record update timestamp (UTC)
        last_login_at: Last login timestamp (UTC)
    """
    
    __tablename__ = "user_profiles"
    
    # Primary Key
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    
    # Foreign Key to auth-service (not enforced in DB)
    user_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
        comment="User ID from auth-service"
    )
    
    # Profile Information
    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="User display name"
    )
    
    bio: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="User biography (max 500 chars)"
    )
    
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Avatar image URL from file-service"
    )
    
    location: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="User location"
    )
    
    website: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="User website URL"
    )
    
    phone_number: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="User phone number"
    )
    
    # Status Flags
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        comment="Email verification status"
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        comment="Account active status"
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
    
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Last login timestamp (UTC)"
    )
    
    # Relationships
    preferences: Mapped["UserPreference"] = relationship(
        "UserPreference",
        back_populates="profile",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession",
        back_populates="profile",
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_user_profiles_user_id", "user_id"),
        Index("idx_user_profiles_display_name", "display_name"),
        Index("idx_user_profiles_is_active", "is_active"),
        Index("idx_user_profiles_is_verified", "is_verified"),
        Index("idx_user_profiles_created_at", "created_at"),
        {"comment": "User profile information table"}
    )
    
    def __repr__(self) -> str:
        return f"<UserProfile(id={self.id}, user_id={self.user_id}, display_name={self.display_name})>"
