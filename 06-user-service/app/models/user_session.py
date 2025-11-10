"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : user_session.py
Description  : User session database model
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
Created Date      : 2025-11-08 09:30 UTC
Last Modified     : 2025-11-08 09:30 UTC
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
from sqlalchemy import String, DateTime, Boolean, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base

if TYPE_CHECKING:
    from .user_profile import UserProfile


class UserSession(Base):
    """
    User session model for tracking active user sessions.
    
    Stores session information including device details, IP address,
    and login/logout timestamps. Used for session management and security.
    
    Attributes:
        id: Primary key (UUID v4)
        profile_id: Foreign key to user_profiles
        session_token: Session token (JWT token ID)
        device_type: Device type (web/mobile/tablet/desktop)
        device_name: Device name/browser
        os: Operating system
        ip_address: Client IP address
        user_agent: Full user agent string
        is_active: Session active status
        created_at: Session creation timestamp (UTC)
        last_activity_at: Last activity timestamp (UTC)
        expires_at: Session expiration timestamp (UTC)
        logout_at: Logout timestamp (UTC)
    """
    
    __tablename__ = "user_sessions"
    
    # Primary Key
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    
    # Foreign Key
    profile_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key to user_profiles"
    )
    
    # Session Information
    session_token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Session token (JWT token ID)"
    )
    
    # Device Information
    device_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Device type (web/mobile/tablet/desktop)"
    )
    
    device_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Device name or browser"
    )
    
    os: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Operating system"
    )
    
    # Network Information
    ip_address: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
        index=True,
        comment="Client IP address (IPv4/IPv6)"
    )
    
    user_agent: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Full user agent string"
    )
    
    # Session Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        comment="Session active status"
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Session creation timestamp (UTC)"
    )
    
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Last activity timestamp (UTC)"
    )
    
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Session expiration timestamp (UTC)"
    )
    
    logout_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Logout timestamp (UTC)"
    )
    
    # Relationships
    profile: Mapped["UserProfile"] = relationship(
        "UserProfile",
        back_populates="sessions"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_user_sessions_profile_id", "profile_id"),
        Index("idx_user_sessions_session_token", "session_token"),
        Index("idx_user_sessions_is_active", "is_active"),
        Index("idx_user_sessions_expires_at", "expires_at"),
        Index("idx_user_sessions_ip_address", "ip_address"),
        Index("idx_user_sessions_device_type", "device_type"),
        Index("idx_user_sessions_profile_active", "profile_id", "is_active"),
        {"comment": "User session tracking table"}
    )
    
    def __repr__(self) -> str:
        return f"<UserSession(id={self.id}, profile_id={self.profile_id}, device_type={self.device_type})>"
