"""
Integration tests for API Gateway
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Test health endpoint"""
    response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert "service" in data
    assert data["service"] == "api-gateway"


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint"""
    response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["service"] == "api-gateway"
    assert "version" in data
    assert "status" in data


@pytest.mark.asyncio
async def test_services_endpoint(client: AsyncClient):
    """Test services listing endpoint"""
    response = await client.get("/services")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "services" in data
    assert "healthy_services" in data


@pytest.mark.asyncio
async def test_circuit_breakers_endpoint(client: AsyncClient):
    """Test circuit breakers listing endpoint"""
    response = await client.get("/circuit-breakers")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "circuit_breakers" in data


@pytest.mark.asyncio
async def test_metrics_endpoint(client: AsyncClient):
    """Test Prometheus metrics endpoint"""
    response = await client.get("/metrics")
    
    # Metrics should return plain text
    assert response.status_code == 200
    assert "text/plain" in response.headers.get("content-type", "")
