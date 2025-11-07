# Service Discovery - Gravity MicroServices Platform

**Version:** 1.0.0  
**Status:** In Development 🚧  
**Author:** Elena Volkov (Backend & Integration Lead)

## 🎯 Overview

Service Discovery microservice provides dynamic service registration, health monitoring, and load balancing for the Gravity platform using HashiCorp Consul.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -e ".[dev,test]"

# Start infrastructure
docker-compose up -d consul postgres redis

# Run migrations
alembic upgrade head

# Start service
uvicorn app.main:app --host 0.0.0.0 --port 8761 --reload
```

## 📋 Features

- ✅ Service registration and deregistration
- ✅ Health monitoring (HTTP, TCP, TTL, gRPC)
- ✅ Load balancing (round-robin, least-connections, weighted, geographic)
- ✅ Dynamic configuration management
- ✅ Real-time updates via WebSocket
- ✅ Prometheus metrics
- ✅ OpenAPI documentation

## 🏗️ Architecture

See [docs/SERVICE_DISCOVERY_ARCHITECTURE.md](../docs/SERVICE_DISCOVERY_ARCHITECTURE.md) for complete architecture design.

## 📡 API Endpoints

### Service Registration

- `POST /api/v1/register` - Register service instance
- `DELETE /api/v1/deregister/{service_id}` - Deregister service
- `GET /api/v1/services` - List all services
- `GET /api/v1/services/{name}/instance` - Get instance (load balanced)

### Health Monitoring

- `GET /api/v1/health/{service_id}` - Get health status
- `POST /api/v1/health/{service_id}/check` - Manual health check

### Configuration

- `GET /api/v1/config/{service_name}` - Get configuration
- `PUT /api/v1/config/{service_name}` - Update configuration
- `WS /api/v1/config/watch/{service_name}` - Watch config changes

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test
pytest tests/test_registration.py -v
```

## 📊 Performance Targets

- **Registration:** < 100ms
- **Discovery:** < 50ms
- **Throughput:** 10,000+ req/sec
- **Availability:** 99.99%

## 🔧 Configuration

Environment variables:

```env
CONSUL_HOST=localhost
CONSUL_PORT=8500
DATABASE_URL=postgresql://user:pass@localhost:5432/service_discovery
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
```

## 📈 Monitoring

- **Metrics:** http://localhost:8761/metrics
- **Health:** http://localhost:8761/health
- **Docs:** http://localhost:8761/docs

## 👥 Development Team

- **Backend Lead:** Elena Volkov
- **Architecture:** Dr. Fatima Al-Mansouri  
- **DevOps:** Lars Björkman

---

**Cost:** $2,250 (15 hours estimated)  
**Status:** Phase 1 & 2 in progress
