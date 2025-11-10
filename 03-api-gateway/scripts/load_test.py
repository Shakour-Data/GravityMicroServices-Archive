"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : load_test.py
Description  : Load testing script using Locust
Language     : English (UK)
Framework    : FastAPI / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
================================================================================
Primary Author    : Lars Björkman (DevOps & Infrastructure Lead)
Contributors      : None
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT (زمان‌بندی و تلاش)
================================================================================
Created Date      : 2025-11-05 14:00 UTC
Last Modified     : 2025-11-06 16:45 UTC
Development Time  : 1 hour 0 minutes
Review Time       : 0 hours 15 minutes
Testing Time      : 0 hours 30 minutes
Total Time        : 1 hour 45 minutes

================================================================================
COST CALCULATION (محاسبه هزینه)
================================================================================
Hourly Rate       : $150/hour (Elite Engineer Standard)
Development Cost  : 1.0 × $150 = $150.00 USD
Review Cost       : 0.25 × $150 = $37.50 USD
Testing Cost      : 0.5 × $150 = $75.00 USD
Total Cost        : $262.50 USD

================================================================================
VERSION HISTORY (تاریخچه نسخه)
================================================================================
v1.0.0 - 2025-11-05 - Lars Björkman - Initial implementation
v1.0.1 - 2025-11-06 - Lars Björkman - Added file header standard

================================================================================
DEPENDENCIES (وابستگی‌ها)
================================================================================
Internal  : gravity_common (where applicable)
External  : FastAPI, SQLAlchemy, Pydantic (as needed)
Database  : PostgreSQL 16+, Redis 7 (as needed)

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/GravityMicroServices

================================================================================
"""

from locust import HttpUser, task, between
import random


class APIGatewayUser(HttpUser):
    """Simulated user for load testing API Gateway"""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    @task(3)
    def check_health(self):
        """Test health endpoint (most common)"""
        self.client.get("/health")
    
    @task(2)
    def list_services(self):
        """Test services listing"""
        self.client.get("/services")
    
    @task(1)
    def check_circuit_breakers(self):
        """Test circuit breakers listing"""
        self.client.get("/circuit-breakers")
    
    @task(1)
    def root_endpoint(self):
        """Test root endpoint"""
        self.client.get("/")
    
    @task(2)
    def proxy_auth_request(self):
        """Test proxying to auth service"""
        # Simulate authentication request
        self.client.post(
            "/api/auth/login",
            json={
                "email": f"test{random.randint(1, 100)}@example.com",
                "password": "password123"
            }
        )
    
    def on_start(self):
        """Called when user starts"""
        pass
