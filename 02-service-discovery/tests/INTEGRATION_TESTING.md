# Integration Testing Guide

## Prerequisites

Integration tests require real instances of:
- PostgreSQL 16+
- Redis 7+
- Consul 1.17+

## Quick Start with Docker Compose

The easiest way to run integration tests is using Docker Compose:

```bash
# Start all required services
docker-compose up -d postgres redis consul

# Wait for services to be ready (about 30 seconds)
docker-compose ps

# Run integration tests
pytest tests/test_integration.py -v

# Cleanup
docker-compose down
```

## Manual Setup

### 1. Start PostgreSQL

```bash
docker run -d \
  --name test-postgres \
  -e POSTGRES_DB=service_discovery_test \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres_password_change_in_production \
  -p 5432:5432 \
  postgres:16-alpine
```

### 2. Start Redis

```bash
docker run -d \
  --name test-redis \
  -p 6379:6379 \
  redis:7-alpine redis-server --requirepass redis_password_change_in_production
```

### 3. Start Consul

```bash
docker run -d \
  --name test-consul \
  -p 8500:8500 \
  consul:1.17 agent -server -ui -bootstrap-expect=1 -client=0.0.0.0
```

### 4. Run Tests

```bash
# All integration tests
pytest tests/test_integration.py -v

# Specific test class
pytest tests/test_integration.py::TestServiceRegistrationIntegration -v

# Specific test
pytest tests/test_integration.py::TestServiceRegistrationIntegration::test_register_service_end_to_end -v

# With coverage
pytest tests/test_integration.py --cov=app --cov-report=html
```

## Test Categories

### 1. Service Registration Integration
- End-to-end registration flow
- Load balancing across multiple instances
- Service deregistration

### 2. Health Monitoring Integration
- TTL health check updates
- Health status filtering
- Automatic health check registration

### 3. Caching Integration
- Redis caching for service discovery
- Cache invalidation on deregistration
- Cache hit/miss scenarios

### 4. Database Persistence Integration
- Service events storage
- Metadata persistence
- Event history tracking

### 5. End-to-End Scenarios
- Complete microservice lifecycle
- Multi-service interactions

### 6. Performance Integration
- Concurrent registrations (10 services)
- High-volume discovery (100 requests)
- Load testing scenarios

## Expected Results

```
======================== test session starts =========================
collected 15 items

tests/test_integration.py::TestServiceRegistrationIntegration::test_register_service_end_to_end PASSED
tests/test_integration.py::TestServiceRegistrationIntegration::test_discover_service_with_load_balancing PASSED
tests/test_integration.py::TestServiceRegistrationIntegration::test_deregister_service_end_to_end PASSED
tests/test_integration.py::TestHealthMonitoringIntegration::test_health_check_ttl_update PASSED
tests/test_integration.py::TestHealthMonitoringIntegration::test_health_check_filtering PASSED
tests/test_integration.py::TestCachingIntegration::test_service_discovery_caching PASSED
tests/test_integration.py::TestCachingIntegration::test_cache_invalidation_on_deregister PASSED
tests/test_integration.py::TestDatabasePersistenceIntegration::test_service_events_stored PASSED
tests/test_integration.py::TestDatabasePersistenceIntegration::test_service_metadata_persistence PASSED
tests/test_integration.py::TestEndToEndScenarios::test_complete_microservice_lifecycle PASSED
tests/test_integration.py::TestPerformanceIntegration::test_concurrent_registrations PASSED
tests/test_integration.py::TestPerformanceIntegration::test_high_volume_discovery PASSED

======================== 15 passed in 45.23s =========================
```

## Troubleshooting

### Consul Not Available

```bash
# Check if Consul is running
curl http://localhost:8500/v1/status/leader

# View Consul logs
docker logs test-consul
```

### PostgreSQL Connection Issues

```bash
# Test connection
docker exec -it test-postgres psql -U postgres -d service_discovery_test

# Check logs
docker logs test-postgres
```

### Redis Connection Issues

```bash
# Test connection
docker exec -it test-redis redis-cli -a redis_password_change_in_production ping

# Check logs
docker logs test-redis
```

### Tests Skipped

If you see:
```
tests/test_integration.py::TestServiceRegistrationIntegration::test_register_service_end_to_end SKIPPED
```

This means required services are not running. Start them with Docker Compose.

## CI/CD Integration

For GitHub Actions, see `.github/workflows/integration-tests.yml` (Task 19).

## Performance Benchmarks

Expected performance on standard development machine:

- Service Registration: <100ms per request
- Service Discovery: <50ms per request (cached: <10ms)
- Concurrent Registrations (10): <2 seconds total
- High Volume Discovery (100): <5 seconds total

## Cleanup

```bash
# Stop and remove all test containers
docker-compose down -v

# Or manually:
docker stop test-postgres test-redis test-consul
docker rm test-postgres test-redis test-consul
```

## Next Steps

After integration tests pass:
1. Run full test suite: `pytest tests/ -v`
2. Check combined coverage: `pytest --cov=app`
3. Proceed to Performance Testing (Task 17)
4. Set up CI/CD Pipeline (Task 19)
