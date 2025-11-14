"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : test_registry_service.py
Description  : Comprehensive unit tests for ServiceRegistryService.
Language     : English (UK)
Framework    : pytest 8.4.2, Python 3.13+

================================================================================
AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
================================================================================
Primary Author    : GitHub Copilot (AI Assistant)
Contributors      : Team Gravity
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TEST COVERAGE TARGET
================================================================================
File Under Test   : app/services/registry_service.py
Current Coverage  : 27% (31 of 115 statements)
Target Coverage   : 95%+ (110+ of 115 statements)
Missing Lines     : 84 lines

================================================================================
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, UTC
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.registry_service import ServiceRegistryService
from app.schemas.service import (
    ServiceRegister,
    ServiceDiscoveryRequest,
    LoadBalancingStrategy,
    HealthCheckCreate,
)
from app.models.service import Service, ServiceEvent
from app.core.consul_client import ServiceInstance, HealthCheck


@pytest.fixture
def mock_db_session():
    """Mock database session."""
    session = AsyncMock(spec=AsyncSession)
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    return session


@pytest.fixture
def registry_service(mock_db_session):
    """Create ServiceRegistryService instance with mocked DB."""
    return ServiceRegistryService(db=mock_db_session)


@pytest.fixture
def sample_service_register():
    """Sample service registration data."""
    return ServiceRegister(
        service_id="test-service-1",
        service_name="test-service",
        address="127.0.0.1",
        port=8080,
        tags=["api", "v1"],
        meta={"version": "1.0.0"},
        weight=10,
        datacenter="dc1",
        region="us-east-1",
        zone="zone-a",
        health_check=HealthCheckCreate(
            check_type="http",
            interval="10s",
            timeout="5s",
            http_endpoint="/health"
        )
    )


@pytest.fixture
def sample_service_model():
    """Sample service database model."""
    service = Service(
        service_id="test-service-1",
        service_name="test-service",
        address="127.0.0.1",
        port=8080,
        tags=["api", "v1"],
        meta={"version": "1.0.0"},
        health_status="passing",
        health_check_type="http",
        health_check_endpoint="/health",
        weight=10,
        datacenter="dc1",
        region="us-east-1",
        zone="zone-a",
        is_active=True
    )
    service.id = 1
    service.created_at = datetime.now(UTC)
    service.updated_at = datetime.now(UTC)
    return service


@pytest.fixture
def sample_service_instances():
    """Sample service instances from Consul."""
    return [
        ServiceInstance(
            service_id="test-service-1",
            service_name="test-service",
            address="127.0.0.1",
            port=8080,
            tags=["api", "v1"],
            meta={"version": "1.0.0"},
            health_status="passing"
        ),
        ServiceInstance(
            service_id="test-service-2",
            service_name="test-service",
            address="127.0.0.2",
            port=8081,
            tags=["api", "v2"],
            meta={"version": "2.0.0"},
            health_status="passing"
        )
    ]


class TestRegisterService:
    """Tests for register_service method."""

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    @patch("app.services.registry_service.redis_client")
    async def test_register_service_success(
        self,
        mock_redis,
        mock_consul,
        registry_service,
        mock_db_session,
        sample_service_register,
        sample_service_model
    ):
        """Test successful service registration."""
        # Arrange
        mock_consul.register_service = AsyncMock(return_value=True)
        mock_redis.delete = AsyncMock()
        
        # Mock database session refresh to set attributes
        async def mock_refresh(obj):
            obj.id = 1
            obj.created_at = datetime.now(UTC)
            obj.updated_at = datetime.now(UTC)
        
        mock_db_session.refresh.side_effect = mock_refresh
        
        # Act
        result = await registry_service.register_service(sample_service_register)
        
        # Assert
        assert result is not None
        mock_consul.register_service.assert_called_once()
        # Note: add() called twice - once for Service, once for ServiceEvent in _log_event
        assert mock_db_session.add.call_count == 2
        mock_db_session.commit.assert_called()
        mock_redis.delete.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    async def test_register_service_consul_failure(
        self,
        mock_consul,
        registry_service,
        sample_service_register
    ):
        """Test service registration when Consul fails."""
        # Arrange
        mock_consul.register_service = AsyncMock(return_value=False)
        
        # Act & Assert
        with pytest.raises(Exception, match="Failed to register service with Consul"):
            await registry_service.register_service(sample_service_register)

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    @patch("app.services.registry_service.redis_client")
    async def test_register_service_duplicate_updates(
        self,
        mock_redis,
        mock_consul,
        registry_service,
        mock_db_session,
        sample_service_register
    ):
        """Test service registration with duplicate (triggers update)."""
        # Arrange
        mock_consul.register_service = AsyncMock(return_value=True)
        mock_redis.delete = AsyncMock()
        
        # Simulate IntegrityError on first commit (duplicate), then success on update path
        mock_db_session.commit.side_effect = [
            IntegrityError("", "", ""),  # First commit fails
            None,  # _log_event commit in _update_existing_service
            None   # _log_event commit after update
        ]
        
        # Mock execute for UPDATE statement
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = Service(
            service_id=sample_service_register.service_id,
            service_name=sample_service_register.service_name,
            address=sample_service_register.address,
            port=sample_service_register.port,
            is_active=True
        )
        mock_db_session.execute.return_value = mock_result
        
        # Act
        result = await registry_service.register_service(sample_service_register)
        
        # Assert
        assert result is not None
        assert result.service_id == sample_service_register.service_id
        mock_db_session.rollback.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    async def test_register_service_database_error_rollback(
        self,
        mock_consul,
        registry_service,
        mock_db_session,
        sample_service_register
    ):
        """Test service registration database error triggers Consul deregistration."""
        # Arrange
        mock_consul.register_service = AsyncMock(return_value=True)
        mock_consul.deregister_service = AsyncMock(return_value=True)  # Make it AsyncMock
        
        # Simulate database error that's not IntegrityError
        mock_db_session.commit.side_effect = Exception("Database connection lost")
        
        # Act & Assert
        with pytest.raises(Exception, match="Database connection lost"):
            await registry_service.register_service(sample_service_register)
        
        mock_db_session.rollback.assert_called_once()
        mock_consul.deregister_service.assert_called_once_with(sample_service_register.service_id)

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    @patch("app.services.registry_service.redis_client")
    async def test_register_service_without_health_check(
        self,
        mock_redis,
        mock_consul,
        registry_service,
        mock_db_session
    ):
        """Test service registration without health check."""
        # Arrange
        service_data = ServiceRegister(
            service_id="test-service-no-hc",
            service_name="test-service",
            address="127.0.0.1",
            port=8080,
            health_check=None
        )
        
        mock_consul.register_service = AsyncMock(return_value=True)
        mock_redis.delete = AsyncMock()
        
        async def mock_refresh(obj):
            obj.id = 1
        
        mock_db_session.refresh.side_effect = mock_refresh
        
        # Act
        result = await registry_service.register_service(service_data)
        
        # Assert
        assert result is not None
        # Verify consul_client.register_service was called with health_check=None
        call_args = mock_consul.register_service.call_args
        assert call_args.kwargs.get("health_check") is None


class TestDeregisterService:
    """Tests for deregister_service method."""

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    @patch("app.services.registry_service.redis_client")
    async def test_deregister_service_success(
        self,
        mock_redis,
        mock_consul,
        registry_service,
        mock_db_session,
        sample_service_model
    ):
        """Test successful service deregistration."""
        # Arrange
        mock_consul.deregister_service = AsyncMock(return_value=True)
        mock_redis.delete = AsyncMock()
        
        # Mock SELECT query
        mock_select_result = MagicMock()
        mock_select_result.scalar_one_or_none.return_value = sample_service_model
        
        # Mock UPDATE query
        mock_update_result = MagicMock()
        
        mock_db_session.execute.side_effect = [mock_select_result, mock_update_result, MagicMock()]
        
        # Act
        result = await registry_service.deregister_service("test-service-1")
        
        # Assert
        assert result is True
        mock_consul.deregister_service.assert_called_once_with("test-service-1")
        mock_redis.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_deregister_service_not_found(
        self,
        registry_service,
        mock_db_session
    ):
        """Test deregistering non-existent service."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        # Act
        result = await registry_service.deregister_service("non-existent")
        
        # Assert
        assert result is False


class TestDiscoverService:
    """Tests for discover_service method."""

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    @patch("app.services.registry_service.redis_client")
    @patch("app.services.registry_service.LoadBalancerFactory")
    @patch("app.services.registry_service.settings")
    async def test_discover_service_success(
        self,
        mock_settings,
        mock_lb_factory,
        mock_redis,
        mock_consul,
        registry_service,
        sample_service_instances
    ):
        """Test successful service discovery with load balancing."""
        # Arrange
        mock_settings.CACHE_ENABLED = True
        mock_settings.CACHE_TTL = 60
        
        mock_redis.get = AsyncMock(return_value=None)  # Cache miss
        mock_redis.set = AsyncMock()
        
        mock_consul.discover_service = AsyncMock(return_value=sample_service_instances)
        
        mock_lb = AsyncMock()
        mock_lb.select_instance = AsyncMock(return_value=sample_service_instances[0])
        mock_lb_factory.get_load_balancer.return_value = mock_lb
        
        request = ServiceDiscoveryRequest(
            service_name="test-service",
            passing_only=True,
            lb_strategy=LoadBalancingStrategy.ROUND_ROBIN
        )
        
        # Act
        result = await registry_service.discover_service(request)
        
        # Assert
        assert result is not None
        assert result.service_id == "test-service-1"
        mock_consul.discover_service.assert_called_once()
        mock_lb.select_instance.assert_called_once()
        mock_redis.set.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    @patch("app.services.registry_service.settings")
    async def test_discover_service_no_instances(
        self,
        mock_settings,
        mock_consul,
        registry_service
    ):
        """Test service discovery when no instances found."""
        # Arrange
        mock_settings.CACHE_ENABLED = False
        mock_consul.discover_service = AsyncMock(return_value=[])
        
        request = ServiceDiscoveryRequest(
            service_name="non-existent-service",
            passing_only=True
        )
        
        # Act
        result = await registry_service.discover_service(request)
        
        # Assert
        assert result is None

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    @patch("app.services.registry_service.redis_client")
    @patch("app.services.registry_service.LoadBalancerFactory")
    @patch("app.services.registry_service.settings")
    async def test_discover_service_with_cache_hit(
        self,
        mock_settings,
        mock_lb_factory,
        mock_redis,
        mock_consul,
        registry_service,
        sample_service_instances
    ):
        """Test service discovery with cache hit."""
        # Arrange
        mock_settings.CACHE_ENABLED = True
        mock_redis.get = AsyncMock(return_value={"some": "cached_data"})
        mock_redis.set = AsyncMock()  # Make it AsyncMock
        mock_consul.discover_service = AsyncMock(return_value=sample_service_instances)
        
        mock_lb = AsyncMock()
        mock_lb.select_instance = AsyncMock(return_value=sample_service_instances[0])
        mock_lb_factory.get_load_balancer.return_value = mock_lb
        
        request = ServiceDiscoveryRequest(
            service_name="test-service",
            passing_only=True
        )
        
        # Act
        result = await registry_service.discover_service(request)
        
        # Assert
        assert result is not None
        # Note: Current implementation still calls Consul even on cache hit
        mock_redis.get.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    @patch("app.services.registry_service.LoadBalancerFactory")
    @patch("app.services.registry_service.settings")
    async def test_discover_service_with_filters(
        self,
        mock_settings,
        mock_lb_factory,
        mock_consul,
        registry_service,
        sample_service_instances
    ):
        """Test service discovery with tag, datacenter filters."""
        # Arrange
        mock_settings.CACHE_ENABLED = False
        mock_consul.discover_service = AsyncMock(return_value=sample_service_instances)
        
        mock_lb = AsyncMock()
        mock_lb.select_instance = AsyncMock(return_value=sample_service_instances[0])
        mock_lb_factory.get_load_balancer.return_value = mock_lb
        
        request = ServiceDiscoveryRequest(
            service_name="test-service",
            passing_only=True,
            tag="api",
            datacenter="dc1",
            client_region="us-east-1",
            client_zone="zone-a"
        )
        
        # Act
        result = await registry_service.discover_service(request)
        
        # Assert
        assert result is not None
        mock_consul.discover_service.assert_called_once_with(
            service_name="test-service",
            passing_only=True,
            tag="api",
            datacenter="dc1"
        )
        mock_lb.select_instance.assert_called_once_with(
            sample_service_instances,
            client_region="us-east-1",
            client_zone="zone-a"
        )


class TestGetAllInstances:
    """Tests for get_all_instances method."""

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    async def test_get_all_instances_success(
        self,
        mock_consul,
        registry_service,
        sample_service_instances
    ):
        """Test getting all service instances."""
        # Arrange
        mock_consul.discover_service = AsyncMock(return_value=sample_service_instances)
        
        request = ServiceDiscoveryRequest(
            service_name="test-service",
            passing_only=True
        )
        
        # Act
        result = await registry_service.get_all_instances(request)
        
        # Assert
        assert len(result) == 2
        assert result[0].service_id == "test-service-1"
        assert result[1].service_id == "test-service-2"


class TestGetAllServices:
    """Tests for get_all_services method."""

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    async def test_get_all_services_success(
        self,
        mock_consul,
        registry_service
    ):
        """Test getting all registered services."""
        # Arrange
        expected_services = {
            "service-a": ["api", "v1"],
            "service-b": ["db", "postgresql"],
            "service-c": ["cache", "redis"]
        }
        mock_consul.get_all_services = AsyncMock(return_value=expected_services)
        
        # Act
        result = await registry_service.get_all_services()
        
        # Assert
        assert result == expected_services
        assert "service-a" in result
        assert len(result) == 3


class TestUpdateHealthCheck:
    """Tests for update_health_check method."""

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    async def test_update_health_check_success(
        self,
        mock_consul,
        registry_service
    ):
        """Test successful health check update."""
        # Arrange
        mock_consul.update_health_check = AsyncMock(return_value=True)
        
        # Act
        result = await registry_service.update_health_check(
            check_id="service:test-service-1:1",
            status="pass",
            output="All systems operational"
        )
        
        # Assert
        assert result is True
        mock_consul.update_health_check.assert_called_once_with(
            "service:test-service-1:1",
            "pass",
            "All systems operational"
        )

    @pytest.mark.asyncio
    @patch("app.services.registry_service.consul_client")
    async def test_update_health_check_failure(
        self,
        mock_consul,
        registry_service
    ):
        """Test health check update failure."""
        # Arrange
        mock_consul.update_health_check = AsyncMock(return_value=False)
        
        # Act
        result = await registry_service.update_health_check(
            check_id="service:invalid:1",
            status="fail"
        )
        
        # Assert
        assert result is False


class TestGetServiceEvents:
    """Tests for get_service_events method."""

    @pytest.mark.asyncio
    async def test_get_service_events_all(
        self,
        registry_service,
        mock_db_session
    ):
        """Test getting all service events."""
        # Arrange
        mock_events = [
            ServiceEvent(
                id=1,
                service_id="test-service-1",
                service_name="test-service",
                event_type="registered",
                created_at=datetime.now(UTC)
            ),
            ServiceEvent(
                id=2,
                service_id="test-service-2",
                service_name="test-service",
                event_type="deregistered",
                created_at=datetime.now(UTC)
            )
        ]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_events
        mock_db_session.execute.return_value = mock_result
        
        # Act
        result = await registry_service.get_service_events()
        
        # Assert
        assert len(result) == 2
        assert result[0].event_type == "registered"
        assert result[1].event_type == "deregistered"

    @pytest.mark.asyncio
    async def test_get_service_events_filtered(
        self,
        registry_service,
        mock_db_session
    ):
        """Test getting service events filtered by service_id."""
        # Arrange
        mock_events = [
            ServiceEvent(
                id=1,
                service_id="test-service-1",
                service_name="test-service",
                event_type="registered",
                created_at=datetime.now(UTC)
            )
        ]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_events
        mock_db_session.execute.return_value = mock_result
        
        # Act
        result = await registry_service.get_service_events(service_id="test-service-1")
        
        # Assert
        assert len(result) == 1
        assert result[0].service_id == "test-service-1"

    @pytest.mark.asyncio
    async def test_get_service_events_with_limit(
        self,
        registry_service,
        mock_db_session
    ):
        """Test getting service events with custom limit."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute.return_value = mock_result
        
        # Act
        result = await registry_service.get_service_events(limit=50)
        
        # Assert
        assert len(result) == 0
        mock_db_session.execute.assert_called_once()


class TestPrivateMethods:
    """Tests for private helper methods."""

    @pytest.mark.asyncio
    async def test_log_event(
        self,
        registry_service,
        mock_db_session
    ):
        """Test _log_event creates ServiceEvent."""
        # Act
        await registry_service._log_event(
            service_id="test-service-1",
            service_name="test-service",
            event_type="registered",
            old_status=None,
            new_status="passing",
            details={"version": "1.0.0"}
        )
        
        # Assert
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.services.registry_service.redis_client")
    @patch("app.services.registry_service.settings")
    async def test_invalidate_cache_enabled(
        self,
        mock_settings,
        mock_redis,
        registry_service
    ):
        """Test cache invalidation when caching is enabled."""
        # Arrange
        mock_settings.CACHE_ENABLED = True
        mock_redis.delete = AsyncMock()
        
        # Act
        await registry_service._invalidate_cache("test-service")
        
        # Assert
        mock_redis.delete.assert_called_once_with("service:test-service")

    @pytest.mark.asyncio
    @patch("app.services.registry_service.redis_client")
    @patch("app.services.registry_service.settings")
    async def test_invalidate_cache_disabled(
        self,
        mock_settings,
        mock_redis,
        registry_service
    ):
        """Test cache invalidation when caching is disabled."""
        # Arrange
        mock_settings.CACHE_ENABLED = False
        mock_redis.delete = AsyncMock()
        
        # Act
        await registry_service._invalidate_cache("test-service")
        
        # Assert
        mock_redis.delete.assert_not_called()

    @pytest.mark.asyncio
    @patch("app.services.registry_service.redis_client")
    @patch("app.services.registry_service.settings")
    async def test_cache_service_instances(
        self,
        mock_settings,
        mock_redis,
        registry_service,
        sample_service_instances
    ):
        """Test caching service instances."""
        # Arrange
        mock_settings.CACHE_TTL = 60
        mock_redis.set = AsyncMock()
        
        # Act
        await registry_service._cache_service_instances("test-service", sample_service_instances)
        
        # Assert
        mock_redis.set.assert_called_once()
        call_args = mock_redis.set.call_args
        assert call_args[0][0] == "service:test-service"
        assert len(call_args[0][1]) == 2  # 2 instances
        assert call_args.kwargs["expire"] == 60
