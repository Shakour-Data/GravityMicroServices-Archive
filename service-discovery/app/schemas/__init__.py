"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : __init__.py
Description  : Schemas package initialization.
Language     : English (UK)
Framework    : Pydantic / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
================================================================================
Primary Author    : Elena Volkov (Backend & Integration Lead)
Contributors      : None
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT (زمان‌بندی و تلاش)
================================================================================
Created Date      : 2025-11-07 21:00 UTC
Last Modified     : 2025-11-07 21:00 UTC
Development Time  : 0 hours 2 minutes
Review Time       : 0 hours 0 minutes
Testing Time      : 0 hours 0 minutes
Total Time        : 0 hours 2 minutes

================================================================================
COST CALCULATION (محاسبه هزینه)
================================================================================
Hourly Rate       : $150/hour (Elite Engineer Standard)
Development Cost  : 0.033 × $150 = $5.00 USD
Review Cost       : 0.0 × $150 = $0.00 USD
Testing Cost      : 0.0 × $150 = $0.00 USD
Total Cost        : $5.00 USD

================================================================================
VERSION HISTORY (تاریخچه نسخه)
================================================================================
v1.0.0 - 2025-11-07 - Elena Volkov - Initial implementation

================================================================================
DEPENDENCIES (وابستگی‌ها)
================================================================================
Internal  : app.schemas.service
External  : None
Database  : N/A

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/GravityMicroServices

================================================================================
"""

from app.schemas.service import (
    HealthCheckType,
    HealthStatus,
    LoadBalancingStrategy,
    HealthCheckCreate,
    ServiceRegister,
    ServiceResponse,
    ServiceDiscoveryRequest,
    ServiceInstanceResponse,
    ServiceListResponse,
    ServiceDeregister,
    HealthCheckUpdate,
    ServiceEventResponse,
    AllServicesResponse,
)

__all__ = [
    "HealthCheckType",
    "HealthStatus",
    "LoadBalancingStrategy",
    "HealthCheckCreate",
    "ServiceRegister",
    "ServiceResponse",
    "ServiceDiscoveryRequest",
    "ServiceInstanceResponse",
    "ServiceListResponse",
    "ServiceDeregister",
    "HealthCheckUpdate",
    "ServiceEventResponse",
    "AllServicesResponse",
]
