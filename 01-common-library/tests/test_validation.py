"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform
File         : test_validation.py
Description  : Test suite for validation endpoints
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
Development Time  : 1 hour 0 minutes
Total Cost        : 1.0 × $150 = $150.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-12 - João Silva - Initial test suite for validation endpoints

================================================================================
DEPENDENCIES
================================================================================
Internal  : app.api.v1.validation
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


class TestEmailValidation:
    """Test cases for email validation."""
    
    def test_valid_email(self, client: TestClient):
        """Test valid email address."""
        response = client.post("/api/v1/validation/email", json={
            "email": "test@example.com"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_valid"] is True
        assert data["email"] == "test@example.com"
        assert data["error"] is None
    
    def test_invalid_email_format(self, client: TestClient):
        """Test invalid email format."""
        response = client.post("/api/v1/validation/email", json={
            "email": "invalid-email"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_valid"] is False
        assert data["error"] is not None


class TestPhoneValidation:
    """Test cases for phone validation."""
    
    def test_valid_phone(self, client: TestClient):
        """Test valid phone number."""
        response = client.post("/api/v1/validation/phone", json={
            "phone": "+1234567890"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_valid"] is True
    
    def test_invalid_phone(self, client: TestClient):
        """Test invalid phone number."""
        response = client.post("/api/v1/validation/phone", json={
            "phone": "abc"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_valid"] is False


class TestURLValidation:
    """Test cases for URL validation."""
    
    def test_valid_url(self, client: TestClient):
        """Test valid URL."""
        response = client.post("/api/v1/validation/url", json={
            "url": "https://example.com",
            "require_https": False
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_valid"] is True
        assert data["scheme"] == "https"
        assert data["domain"] == "example.com"
    
    def test_invalid_url(self, client: TestClient):
        """Test invalid URL."""
        response = client.post("/api/v1/validation/url", json={
            "url": "not-a-url"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_valid"] is False


class TestDateValidation:
    """Test cases for date validation."""
    
    def test_valid_date(self, client: TestClient):
        """Test valid date string."""
        response = client.post("/api/v1/validation/date", json={
            "date_string": "2025-11-13",
            "format": "%Y-%m-%d"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_valid"] is True
        assert data["parsed_date"] is not None
    
    def test_invalid_date_format(self, client: TestClient):
        """Test invalid date format."""
        response = client.post("/api/v1/validation/date", json={
            "date_string": "2025-13-45",  # Invalid month/day
            "format": "%Y-%m-%d"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_valid"] is False
