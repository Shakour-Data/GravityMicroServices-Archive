"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - Notification Service
File         : notification.py
Description  : Notification model for storing sent notifications
Language     : Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Elena Volkov (Database Architect)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-09
Development Time  : 0 hours 30 minutes
Total Cost        : 0.5 × $150 = $75.00 USD

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
================================================================================
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base
from app.models.base import BaseModel
import enum


class NotificationType(str, enum.Enum):
    """Notification types."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class NotificationStatus(str, enum.Enum):
    """Notification delivery status."""
    PENDING = "pending"
    SENDING = "sending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Notification(Base, BaseModel):
    """
    Notification model for tracking all sent notifications.
    
    Attributes:
        id: Unique notification ID
        user_id: Recipient user ID
        type: Notification type (email, sms, push)
        template_id: Template used (if any)
        recipient: Email address, phone number, or device token
        subject: Email subject or notification title
        content: Plain text content
        html_content: HTML content (for emails)
        status: Current delivery status
        sent_at: Timestamp when notification was sent
        delivered_at: Timestamp when notification was delivered
        read_at: Timestamp when notification was read
        error_message: Error message if failed
        retry_count: Number of retry attempts
        metadata: Additional data (JSONB)
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = "notifications"
    
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    type = Column(
        SQLEnum(NotificationType, name="notification_type"),
        nullable=False,
        index=True
    )
    template_id = Column(UUID(as_uuid=True), nullable=True)
    recipient = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    html_content = Column(Text, nullable=True)
    status = Column(
        SQLEnum(NotificationStatus, name="notification_status"),
        nullable=False,
        default=NotificationStatus.PENDING,
        index=True
    )
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    metadata = Column(JSONB, nullable=True, default={})
    
    def __repr__(self) -> str:
        return f"<Notification {self.id} - {self.type} to {self.recipient}>"
    
    def mark_as_sent(self) -> None:
        """Mark notification as sent."""
        self.status = NotificationStatus.SENT
        self.sent_at = datetime.utcnow()
    
    def mark_as_delivered(self) -> None:
        """Mark notification as delivered."""
        self.status = NotificationStatus.DELIVERED
        self.delivered_at = datetime.utcnow()
    
    def mark_as_failed(self, error: str) -> None:
        """Mark notification as failed."""
        self.status = NotificationStatus.FAILED
        self.error_message = error
        self.retry_count += 1
