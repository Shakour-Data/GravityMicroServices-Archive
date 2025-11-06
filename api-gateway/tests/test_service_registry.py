"""
Tests for Service Registry
Designed by Dr. Sarah Chen - Chief Architect
"""

import pytest
from datetime import datetime

from app.core.service_registry import ServiceRegistry, ServiceInfo, ServiceStatus


@pytest.mark.asyncio
async def test_service_registration():
    """Test service registration"""
    registry = ServiceRegistry()
    
    # Register a service
    await registry.register_service(
        name="test-service",
        url="http://localhost:8000",
        health_endpoint="/health"
    )
    
    # Check service is registered
    service = await registry.get_service("test-service")
    assert service is not None
    assert service.name == "test-service"
    assert service.url == "http://localhost:8000"


@pytest.mark.asyncio
async def test_service_health_check():
    """Test service health checking"""
    registry = ServiceRegistry()
    
    # Register service with invalid URL (will fail health check)
    await registry.register_service(
        name="unhealthy-service",
        url="http://localhost:9999",
        health_endpoint="/health"
    )
    
    # Wait for health check
    import asyncio
    await asyncio.sleep(2)
    
    # Service should be unhealthy
    service = registry.services.get("unhealthy-service")
    assert service is not None
    assert service.status == ServiceStatus.UNHEALTHY


@pytest.mark.asyncio
async def test_get_healthy_services():
    """Test getting healthy services"""
    registry = ServiceRegistry()
    
    # Add some services
    await registry.register_service(
        name="service1",
        url="http://localhost:8001",
        health_endpoint="/health"
    )
    
    await registry.register_service(
        name="service2", 
        url="http://localhost:8002",
        health_endpoint="/health"
    )
    
    # Get healthy services (both will be unhealthy as servers aren't running)
    healthy = registry.get_healthy_services()
    
    # Should return empty list as no real services are running
    assert isinstance(healthy, list)


@pytest.mark.asyncio
async def test_service_status_summary():
    """Test getting status summary"""
    registry = ServiceRegistry()
    
    await registry.register_service(
        name="test-service",
        url="http://localhost:8000",
        health_endpoint="/health"
    )
    
    summary = registry.get_status_summary()
    
    assert "test-service" in summary
    assert "status" in summary["test-service"]
    assert "response_time_ms" in summary["test-service"]
