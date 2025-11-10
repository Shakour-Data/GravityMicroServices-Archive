"""
Main Application Tests
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint"""
    response = await client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint"""
    response = await client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data


@pytest.mark.asyncio
async def test_detailed_health_check(client: AsyncClient):
    """Test detailed health check endpoint"""
    response = await client.get("/health/detailed")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "dependencies" in data
    assert "database" in data["dependencies"]
    assert "redis" in data["dependencies"]


@pytest.mark.asyncio
async def test_openapi_schema(client: AsyncClient):
    """Test OpenAPI schema endpoint"""
    response = await client.get("/openapi.json")

    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data


@pytest.mark.asyncio
async def test_docs_endpoint(client: AsyncClient):
    """Test Swagger UI docs endpoint"""
    response = await client.get("/docs")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@pytest.mark.asyncio
async def test_redoc_endpoint(client: AsyncClient):
    """Test ReDoc endpoint"""
    response = await client.get("/redoc")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@pytest.mark.asyncio
async def test_404_not_found(client: AsyncClient):
    """Test 404 not found"""
    response = await client.get("/nonexistent-endpoint")

    assert response.status_code == 404
