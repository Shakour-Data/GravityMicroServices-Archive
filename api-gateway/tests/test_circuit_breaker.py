"""
Tests for Circuit Breaker
Designed by Lars Björkman - DevOps Lead
"""

import pytest
import asyncio
from datetime import datetime

from app.core.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
    CircuitBreakerConfig,
    CircuitBreakerManager,
)
from gravity_common.exceptions import ServiceUnavailableError


@pytest.mark.asyncio
async def test_circuit_breaker_closed_state():
    """Test circuit breaker starts in CLOSED state"""
    breaker = CircuitBreaker("test-service")
    
    assert breaker.state == CircuitState.CLOSED
    assert breaker.failure_count == 0


@pytest.mark.asyncio
async def test_circuit_breaker_opens_on_failures():
    """Test circuit breaker opens after threshold failures"""
    config = CircuitBreakerConfig(failure_threshold=3)
    breaker = CircuitBreaker("test-service", config)
    
    # Simulate failures
    async def failing_func():
        raise Exception("Service error")
    
    # Execute failing calls
    for _ in range(3):
        try:
            await breaker.call(failing_func)
        except Exception:
            pass
    
    # Circuit should be open now
    assert breaker.state == CircuitState.OPEN


@pytest.mark.asyncio
async def test_circuit_breaker_fails_fast_when_open():
    """Test circuit breaker fails fast when open"""
    config = CircuitBreakerConfig(failure_threshold=2)
    breaker = CircuitBreaker("test-service", config)
    
    # Cause failures to open circuit
    async def failing_func():
        raise Exception("Service error")
    
    for _ in range(2):
        try:
            await breaker.call(failing_func)
        except Exception:
            pass
    
    # Circuit is open - should fail fast
    with pytest.raises(ServiceUnavailableError):
        await breaker.call(failing_func)


@pytest.mark.asyncio
async def test_circuit_breaker_half_open_transition():
    """Test circuit breaker transitions to HALF_OPEN after timeout"""
    config = CircuitBreakerConfig(
        failure_threshold=2,
        timeout=1  # 1 second timeout
    )
    breaker = CircuitBreaker("test-service", config)
    
    # Cause failures
    async def failing_func():
        raise Exception("Service error")
    
    for _ in range(2):
        try:
            await breaker.call(failing_func)
        except Exception:
            pass
    
    # Circuit is open
    assert breaker.state == CircuitState.OPEN
    
    # Wait for timeout
    await asyncio.sleep(1.5)
    
    # Check timeout (this should transition to HALF_OPEN)
    await breaker._check_timeout()
    
    assert breaker.state == CircuitState.HALF_OPEN


@pytest.mark.asyncio
async def test_circuit_breaker_closes_on_success():
    """Test circuit breaker closes after successful calls in HALF_OPEN"""
    config = CircuitBreakerConfig(
        failure_threshold=2,
        success_threshold=2,
        timeout=1
    )
    breaker = CircuitBreaker("test-service", config)
    
    # Cause failures
    async def failing_func():
        raise Exception("Service error")
    
    async def success_func():
        return "success"
    
    # Open circuit
    for _ in range(2):
        try:
            await breaker.call(failing_func)
        except Exception:
            pass
    
    assert breaker.state == CircuitState.OPEN
    
    # Wait for timeout
    await asyncio.sleep(1.5)
    await breaker._check_timeout()
    assert breaker.state == CircuitState.HALF_OPEN
    
    # Success calls should close circuit
    for _ in range(2):
        await breaker.call(success_func)
    
    assert breaker.state == CircuitState.CLOSED


@pytest.mark.asyncio
async def test_circuit_breaker_manager():
    """Test circuit breaker manager"""
    manager = CircuitBreakerManager()
    
    # Get breaker for service
    breaker1 = await manager.get_breaker("service1")
    assert breaker1.name == "service1"
    
    # Get same breaker again
    breaker2 = await manager.get_breaker("service1")
    assert breaker1 is breaker2
    
    # Get different breaker
    breaker3 = await manager.get_breaker("service2")
    assert breaker3.name == "service2"
    assert breaker3 is not breaker1


@pytest.mark.asyncio
async def test_circuit_breaker_reset():
    """Test manual circuit breaker reset"""
    config = CircuitBreakerConfig(failure_threshold=2)
    breaker = CircuitBreaker("test-service", config)
    
    # Cause failures
    async def failing_func():
        raise Exception("Service error")
    
    for _ in range(2):
        try:
            await breaker.call(failing_func)
        except Exception:
            pass
    
    assert breaker.state == CircuitState.OPEN
    
    # Reset circuit
    await breaker.reset()
    
    assert breaker.state == CircuitState.CLOSED
    assert breaker.failure_count == 0
