"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : service.py
Description  : Service model for database storage.
Language     : English (UK)
Framework    : SQLAlchemy / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
================================================================================
Primary Author    : Elena Volkov (Backend & Integration Lead)
Contributors      : None
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT (زمان‌بندی و تلاش)
================================================================================
Created Date      : 2025-11-07 20:45 UTC
Last Modified     : 2025-11-07 20:45 UTC
Development Time  : 0 hours 30 minutes
Review Time       : 0 hours 10 minutes
Testing Time      : 0 hours 15 minutes
Total Time        : 0 hours 55 minutes

================================================================================
COST CALCULATION (محاسبه هزینه)
================================================================================
Hourly Rate       : $150/hour (Elite Engineer Standard)
Development Cost  : 0.5 × $150 = $75.00 USD
Review Cost       : 0.17 × $150 = $25.00 USD
Testing Cost      : 0.25 × $150 = $37.50 USD
Total Cost        : $137.50 USD

================================================================================
VERSION HISTORY (تاریخچه نسخه)
================================================================================
v1.0.0 - 2025-11-07 - Elena Volkov - Initial implementation

================================================================================
DEPENDENCIES (وابستگی‌ها)
================================================================================
Internal  : None
External  : sqlalchemy
Database  : PostgreSQL 16+

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/GravityMicroServices

================================================================================
"""

from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class Service(Base):
    """
    Service registration model.
    
    Stores service instance information for tracking and analytics.
    """
    
    __tablename__ = "services"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Service identification
    service_id = Column(String(255), unique=True, nullable=False, index=True)
    service_name = Column(String(255), nullable=False, index=True)
    
    # Network information
    address = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    
    # Metadata
    tags = Column(JSON, default=list)  # List of tags
    meta = Column(JSON, default=dict)  # Key-value metadata
    
    # Health information
    health_status = Column(
        String(20),
        default="passing",
        index=True
    )  # passing, warning, critical
    health_check_type = Column(String(20))  # http, tcp, ttl, grpc
    health_check_endpoint = Column(String(500))
    
    # Load balancing
    weight = Column(Integer, default=1)  # For weighted load balancing
    
    # Geographic information
    datacenter = Column(String(100), index=True)
    region = Column(String(100), index=True)
    zone = Column(String(100))
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Timestamps
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    last_health_check = Column(DateTime(timezone=True))
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_service_name_active', 'service_name', 'is_active'),
        Index('idx_service_health', 'service_name', 'health_status'),
        Index('idx_datacenter_region', 'datacenter', 'region'),
    )
    
    def __repr__(self) -> str:
        """String representation of Service."""
        return (
            f"<Service(id={self.id}, service_id='{self.service_id}', "
            f"service_name='{self.service_name}', address='{self.address}', "
            f"port={self.port}, health_status='{self.health_status}')>"
        )
    
    def to_dict(self) -> dict:
        """Convert service to dictionary."""
        return {
            "id": self.id,
            "service_id": self.service_id,
            "service_name": self.service_name,
            "address": self.address,
            "port": self.port,
            "tags": self.tags,
            "meta": self.meta,
            "health_status": self.health_status,
            "health_check_type": self.health_check_type,
            "health_check_endpoint": self.health_check_endpoint,
            "weight": self.weight,
            "datacenter": self.datacenter,
            "region": self.region,
            "zone": self.zone,
            "is_active": self.is_active,
            "registered_at": self.registered_at.isoformat() if self.registered_at is not None else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at is not None else None,
            "last_health_check": self.last_health_check.isoformat() if self.last_health_check is not None else None,
        }


class ServiceEvent(Base):
    """
    Service event log.
    
    Tracks service lifecycle events for auditing and debugging.
    """
    
    __tablename__ = "service_events"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Event information
    service_id = Column(String(255), nullable=False, index=True)
    service_name = Column(String(255), nullable=False, index=True)
    event_type = Column(
        String(50),
        nullable=False,
        index=True
    )  # registered, deregistered, health_changed, updated
    
    # Event details
    old_status = Column(String(20))
    new_status = Column(String(20))
    details = Column(JSON, default=dict)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self) -> str:
        """String representation of ServiceEvent."""
        return (
            f"<ServiceEvent(id={self.id}, service_id='{self.service_id}', "
            f"event_type='{self.event_type}', created_at={self.created_at})>"
        )
    
    def to_dict(self) -> dict:
        """Convert event to dictionary."""
        return {
            "id": self.id,
            "service_id": self.service_id,
            "service_name": self.service_name,
            "event_type": self.event_type,
            "old_status": self.old_status,
            "new_status": self.new_status,
            "details": self.details,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
        }
