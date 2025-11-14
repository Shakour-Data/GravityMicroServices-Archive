"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform
File         : test_utilities.py
Description  : Test suite for utility endpoints
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
v1.0.0 - 2025-11-12 - João Silva - Initial test suite for utility endpoints

================================================================================
DEPENDENCIES
================================================================================
Internal  : app.api.v1.utilities
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


class TestUUIDGeneration:
    """Test cases for UUID generation."""
    
    def test_generate_uuid_v4(self, client: TestClient):
        """Test UUID v4 generation."""
        response = client.get("/api/v1/utilities/uuid?version=4")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "uuid" in data
        assert data["version"] == 4
        assert len(data["uuid"]) == 36  # UUID format: 8-4-4-4-12
    
    def test_generate_uuid_v1(self, client: TestClient):
        """Test UUID v1 generation."""
        response = client.get("/api/v1/utilities/uuid?version=1")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["version"] == 1


class TestDateFormatting:
    """Test cases for date formatting."""
    
    def test_format_current_date(self, client: TestClient):
        """Test formatting current date."""
        response = client.post("/api/v1/utilities/date/format", json={
            "format": "%Y-%m-%d"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "formatted" in data
        assert "timestamp" in data
        assert "iso" in data
    
    def test_format_specific_timestamp(self, client: TestClient):
        """Test formatting specific timestamp."""
        response = client.post("/api/v1/utilities/date/format", json={
            "timestamp": 1700000000,
            "format": "%Y-%m-%d %H:%M:%S"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["timestamp"] == 1700000000


class TestBase64Encoding:
    """Test cases for Base64 encoding/decoding."""
    
    def test_encode_base64(self, client: TestClient):
        """Test Base64 encoding."""
        response = client.post("/api/v1/utilities/base64/encode", json={
            "text": "Hello World"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["encoded"] == "SGVsbG8gV29ybGQ="
        assert data["original_length"] == 11
    
    def test_decode_base64(self, client: TestClient):
        """Test Base64 decoding."""
        response = client.post("/api/v1/utilities/base64/decode", json={
            "encoded": "SGVsbG8gV29ybGQ="
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["decoded"] == "Hello World"
    
    def test_encode_decode_round_trip(self, client: TestClient):
        """Test encode/decode round trip."""
        original_text = "Test Message 123"
        
        # Encode
        encode_response = client.post("/api/v1/utilities/base64/encode", json={
            "text": original_text
        })
        encoded = encode_response.json()["encoded"]
        
        # Decode
        decode_response = client.post("/api/v1/utilities/base64/decode", json={
            "encoded": encoded
        })
        decoded = decode_response.json()["decoded"]
        
        assert decoded == original_text


class TestHashGeneration:
    """Test cases for hash generation."""
    
    def test_generate_sha256_hash(self, client: TestClient):
        """Test SHA256 hash generation."""
        response = client.post("/api/v1/utilities/hash", json={
            "text": "Hello World",
            "algorithm": "sha256"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["algorithm"] == "sha256"
        assert len(data["hash"]) == 64  # SHA256 produces 64 hex characters
    
    def test_generate_md5_hash(self, client: TestClient):
        """Test MD5 hash generation."""
        response = client.post("/api/v1/utilities/hash", json={
            "text": "Hello World",
            "algorithm": "md5"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["algorithm"] == "md5"
        assert len(data["hash"]) == 32  # MD5 produces 32 hex characters
