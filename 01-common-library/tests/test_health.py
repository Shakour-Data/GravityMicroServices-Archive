"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform
File         : test_health.py
Description  : Test suite for health check endpoints
Language     : English (UK)
Framework    : FastAPI / Python 3.12+ / Pytest

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : João Silva (Testing & QA Lead)
Contributors      : Elite Engineering Team
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-12 00:00 UTC
Last Modified     : 2025-11-12 00:00 UTC
Development Time  : 0 hours 30 minutes
Total Cost        : 0.5 × $150 = $75.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-12 - João Silva - Initial test suite for health endpoints

================================================================================
DEPENDENCIES
================================================================================
Internal  : app.main
External  : pytest>=7.4.0, httpx>=0.24.1, fastapi>=0.100.0
Database  : N/A

================================================================================
LICENSE & COPYRIGHT
================================================================================
License      : MIT License
Copyright    : © 2025 Gravity MicroServices Platform. All rights reserved.
================================================================================
"""

import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test basic health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "healthy"
    assert data["service"] == "01-common-library"
    assert "version" in data
    assert "timestamp" in data


def test_ping(client: TestClient):
    """Test ping endpoint."""
    response = client.get("/ping")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["ping"] == "pong"


def test_readiness_check(client: TestClient):
    """Test readiness probe endpoint."""
    response = client.get("/ready")
    
    # Should return 200 or 503
    assert response.status_code in [200, 503]
    data = response.json()
    
    assert "status" in data
    assert "checks" in data
    assert "redis" in data["checks"]
