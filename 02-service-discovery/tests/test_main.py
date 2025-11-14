"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : test_main.py
Description  : Comprehensive unit tests for main.py FastAPI application.
Language     : English (UK)
Framework    : pytest 8.4.2, Python 3.13+

================================================================================
TEST COVERAGE TARGET
================================================================================
File Under Test   : app/main.py
Current Coverage  : 45% (29 of 64 statements)
Target Coverage   : 95%+ (60+ of 64 statements)
Missing Lines     : 35 lines (90-123, 171-190, 210-211, 218)

================================================================================
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text

from app.main import app, lifespan, health_check, welcome, root


@pytest.fixture
def client():
    """Test client for synchronous endpoints."""
    return TestClient(app)


class TestLifespan:
    """Tests for lifespan context manager."""

    @pytest.mark.asyncio
    @patch("app.main.db_manager")
    @patch("app.main.redis_client")
    @patch("app.main.consul_client")
    async def test_lifespan_startup_success(
        self,
        mock_consul,
        mock_redis,
        mock_db_manager
    ):
        """Test successful application startup."""
        # Arrange
        mock_conn = AsyncMock()
        mock_conn.run_sync = AsyncMock()
        
        # Create proper async context manager for engine.begin()
        class MockAsyncContextManager:
            async def __aenter__(self):
                return mock_conn
            
            async def __aexit__(self, exc_type, exc_val, exc_tb):
                pass
        
        mock_engine = AsyncMock()
        mock_engine.begin = MagicMock(return_value=MockAsyncContextManager())
        
        mock_db_manager.engine = mock_engine
        mock_db_manager.init = MagicMock()
        mock_db_manager.close = AsyncMock()
        
        mock_redis.connect = AsyncMock()
        mock_redis.disconnect = AsyncMock()
        
        mock_consul.health_check = AsyncMock(return_value=True)
        
        # Act
        async with lifespan(app):
            pass  # Lifespan runs startup
        
        # Assert
        mock_db_manager.init.assert_called_once()
        mock_redis.connect.assert_called_once()
        mock_consul.health_check.assert_called_once()
        mock_redis.disconnect.assert_called_once()
        mock_db_manager.close.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.main.db_manager")
    @patch("app.main.redis_client")
    @patch("app.main.consul_client")
    async def test_lifespan_consul_unhealthy_warning(
        self,
        mock_consul,
        mock_redis,
        mock_db_manager
    ):
        """Test startup when Consul is unhealthy."""
        # Arrange
        mock_conn = AsyncMock()
        mock_conn.run_sync = AsyncMock()
        
        # Create proper async context manager for engine.begin()
        class MockAsyncContextManager:
            async def __aenter__(self):
                return mock_conn
            
            async def __aexit__(self, exc_type, exc_val, exc_tb):
                pass
        
        mock_engine = AsyncMock()
        mock_engine.begin = MagicMock(return_value=MockAsyncContextManager())
        
        mock_db_manager.engine = mock_engine
        mock_db_manager.init = MagicMock()
        mock_db_manager.close = AsyncMock()
        
        mock_redis.connect = AsyncMock()
        mock_redis.disconnect = AsyncMock()
        
        mock_consul.health_check = AsyncMock(return_value=False)  # Consul unhealthy
        
        # Act (should not raise, just warn)
        async with lifespan(app):
            pass
        
        # Assert
        mock_consul.health_check.assert_called_once()
        # Application should continue despite Consul being unhealthy

    @pytest.mark.asyncio
    @patch("app.main.db_manager")
    async def test_lifespan_engine_not_initialized_raises(
        self,
        mock_db_manager
    ):
        """Test lifespan raises RuntimeError if DB engine not initialized."""
        # Arrange
        mock_db_manager.engine = None
        mock_db_manager.init = MagicMock()  # init called but doesn't set engine
        
        # Act & Assert
        with pytest.raises(RuntimeError, match="Database engine is not initialized"):
            async with lifespan(app):
                pass


class TestHealthCheckEndpoint:
    """Tests for /health endpoint."""

    @pytest.mark.asyncio
    @patch("app.main.get_db")
    @patch("app.main.redis_client")
    @patch("app.main.consul_client")
    async def test_health_check_all_healthy(
        self,
        mock_consul,
        mock_redis,
        mock_get_db
    ):
        """Test health check when all dependencies are healthy."""
        # Arrange
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock()
        mock_session.close = AsyncMock()
        
        async def mock_db_generator():
            yield mock_session
        
        mock_get_db.return_value = mock_db_generator()
        
        mock_redis.health_check = AsyncMock(return_value=True)
        mock_consul.health_check = AsyncMock(return_value=True)
        
        # Act
        result = await health_check()
        
        # Assert
        assert result["status"] == "healthy"
        assert result["dependencies"]["database"] == "healthy"
        assert result["dependencies"]["redis"] == "healthy"
        assert result["dependencies"]["consul"] == "healthy"
        mock_session.execute.assert_called_once()
        mock_session.close.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.main.get_db")
    @patch("app.main.redis_client")
    @patch("app.main.consul_client")
    async def test_health_check_database_unhealthy(
        self,
        mock_consul,
        mock_redis,
        mock_get_db
    ):
        """Test health check when database is unhealthy."""
        # Arrange
        async def mock_db_generator():
            raise Exception("Database connection failed")
            yield  # pragma: no cover
        
        mock_get_db.return_value = mock_db_generator()
        
        mock_redis.health_check = AsyncMock(return_value=True)
        mock_consul.health_check = AsyncMock(return_value=True)
        
        # Act
        result = await health_check()
        
        # Assert
        assert result["status"] == "unhealthy"
        assert result["dependencies"]["database"] == "unhealthy"
        assert result["dependencies"]["redis"] == "healthy"
        assert result["dependencies"]["consul"] == "healthy"

    @pytest.mark.asyncio
    @patch("app.main.get_db")
    @patch("app.main.redis_client")
    @patch("app.main.consul_client")
    async def test_health_check_redis_unhealthy(
        self,
        mock_consul,
        mock_redis,
        mock_get_db
    ):
        """Test health check when Redis is unhealthy."""
        # Arrange
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock()
        mock_session.close = AsyncMock()
        
        async def mock_db_generator():
            yield mock_session
        
        mock_get_db.return_value = mock_db_generator()
        
        mock_redis.health_check = AsyncMock(return_value=False)
        mock_consul.health_check = AsyncMock(return_value=True)
        
        # Act
        result = await health_check()
        
        # Assert
        assert result["status"] == "unhealthy"
        assert result["dependencies"]["redis"] == "unhealthy"

    @pytest.mark.asyncio
    @patch("app.main.get_db")
    @patch("app.main.redis_client")
    @patch("app.main.consul_client")
    async def test_health_check_consul_unhealthy(
        self,
        mock_consul,
        mock_redis,
        mock_get_db
    ):
        """Test health check when Consul is unhealthy."""
        # Arrange
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock()
        mock_session.close = AsyncMock()
        
        async def mock_db_generator():
            yield mock_session
        
        mock_get_db.return_value = mock_db_generator()
        
        mock_redis.health_check = AsyncMock(return_value=True)
        mock_consul.health_check = AsyncMock(return_value=False)
        
        # Act
        result = await health_check()
        
        # Assert
        assert result["status"] == "unhealthy"
        assert result["dependencies"]["consul"] == "unhealthy"


class TestWelcomeEndpoint:
    """Tests for /welcome endpoint."""

    @pytest.mark.asyncio
    async def test_welcome(self):
        """Test /welcome endpoint returns welcome message."""
        # Arrange - use async client
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            # Act
            response = await ac.get("/welcome")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Welcome to the Service Discovery API!"


class TestRootEndpoint:
    """Tests for / endpoint."""

    @pytest.mark.asyncio
    @patch("app.main.settings")
    async def test_root(self, mock_settings):
        """Test / endpoint returns service information."""
        # Arrange
        mock_settings.APP_NAME = "Test Service"
        mock_settings.API_VERSION = "1.0.0"
        
        # Act
        result = await root()
        
        # Assert
        assert result["service"] == "Test Service"
        assert result["version"] == "1.0.0"


class TestAppConfiguration:
    """Tests for FastAPI app configuration."""

    def test_app_has_cors_middleware(self):
        """Test CORS middleware is configured."""
        # Assert
        middlewares = [m.cls.__name__ for m in app.user_middleware]
        assert "CORSMiddleware" in middlewares

    def test_app_includes_services_router(self):
        """Test services router is included."""
        # Assert
        routes = [r.path for r in app.routes]
        # Check if any route starts with /api/v1/services
        assert any("/api/v1/services" in route for route in routes)

    def test_app_has_health_endpoint(self):
        """Test health endpoint is registered."""
        # Assert
        routes = [r.path for r in app.routes]
        assert "/health" in routes

    def test_app_has_docs_endpoint(self):
        """Test OpenAPI docs endpoint is available."""
        # Assert
        assert app.docs_url == "/docs"
        assert app.redoc_url == "/redoc"
        assert app.openapi_url == "/openapi.json"


class TestHealthEndpointIntegration:
    """Integration tests for /health endpoint using TestClient."""

    @pytest.mark.asyncio
    @patch("app.main.get_db")
    @patch("app.main.redis_client")
    @patch("app.main.consul_client")
    async def test_health_endpoint_returns_200(
        self,
        mock_consul,
        mock_redis,
        mock_get_db
    ):
        """Test /health endpoint returns 200 status."""
        # Arrange
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock()
        mock_session.close = AsyncMock()
        
        async def mock_db_generator():
            yield mock_session
        
        mock_get_db.return_value = mock_db_generator()
        
        mock_redis.health_check = AsyncMock(return_value=True)
        mock_consul.health_check = AsyncMock(return_value=True)
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            # Act
            response = await ac.get("/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "dependencies" in data
