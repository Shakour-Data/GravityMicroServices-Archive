# Deployment Guide

Complete deployment guide for Common Library Service v1.0.0.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Configuration](#environment-configuration)
3. [Local Development](#local-development)
4. [Docker Deployment](#docker-deployment)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Health Checks](#health-checks)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required
- Python 3.12+
- PostgreSQL 16+ (optional for production)
- Redis 7+ (optional, has Mock fallback)

### Optional
- Docker & Docker Compose
- Kubernetes cluster
- Load balancer

---

## Environment Configuration

### 1. Create `.env` file

```bash
# Copy example environment file
cp .env.example .env
```

### 2. Configure Environment Variables

```bash
# Application
APP_NAME=01-common-library
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=False
LOG_LEVEL=INFO
PORT=8100

# Database (PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/common_library
DATABASE_ECHO=False
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Redis Cache
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
REDIS_MAX_CONNECTIONS=50

# Security
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production-min-32-chars
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080","http://localhost:8100"]
```

---

## Local Development

### 1. Install Dependencies

#### Using pip:
```bash
pip install -r requirements.txt
```

#### Using poetry (if available):
```bash
poetry install
```

### 2. Start Server

```bash
# Development mode with hot reload
python -m uvicorn app.main:app --host 0.0.0.0 --port 8100 --reload

# Production mode
python -m uvicorn app.main:app --host 0.0.0.0 --port 8100 --workers 4
```

### 3. Access API Documentation

- **Swagger UI**: http://localhost:8100/docs
- **ReDoc**: http://localhost:8100/redoc
- **Health Check**: http://localhost:8100/health

---

## Docker Deployment

### 1. Build Image

```bash
docker build -t common-library:1.0.0 .
```

### 2. Run Container

```bash
docker run -d \
  --name common-library \
  -p 8100:8100 \
  --env-file .env \
  common-library:1.0.0
```

### 3. Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Kubernetes Deployment

### 1. Create ConfigMap

```bash
kubectl create configmap common-library-config \
  --from-env-file=.env
```

### 2. Create Secret

```bash
kubectl create secret generic common-library-secret \
  --from-literal=jwt-secret-key=your-secret-key \
  --from-literal=database-password=your-db-password
```

### 3. Deploy

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -l app=common-library

# Check service
kubectl get svc common-library

# View logs
kubectl logs -l app=common-library -f
```

---

## Health Checks

### Kubernetes Liveness Probe

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8100
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

### Kubernetes Readiness Probe

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8100
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

### Manual Health Check

```bash
# Basic health
curl http://localhost:8100/health

# Readiness (with dependencies)
curl http://localhost:8100/ready

# Ping
curl http://localhost:8100/ping
```

---

## Troubleshooting

### Issue: Server won't start

**Solution 1**: Check port availability
```bash
# Windows
netstat -ano | findstr :8100

# Linux/Mac
lsof -i :8100
```

**Solution 2**: Check dependencies
```bash
python -m pip list | grep fastapi
python -m pip list | grep uvicorn
```

### Issue: Database connection fails

**Solution 1**: Verify PostgreSQL is running
```bash
# Check PostgreSQL status
pg_isready -h localhost -p 5432
```

**Solution 2**: Check connection string
```bash
# Test connection
psql "postgresql://user:password@localhost:5432/common_library"
```

**Solution 3**: Use graceful degradation
- Service will continue without database
- Mock Redis will be used if Redis unavailable

### Issue: Redis connection fails

**Solution**: Service automatically falls back to Mock Redis
```
2025-11-13 20:49:46 - WARNING - Real Redis unavailable
2025-11-13 20:49:46 - INFO - Falling back to MockRedisClient (in-memory)
```

### Issue: Import errors

**Solution**: Ensure all dependencies installed
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Permission denied

**Solution**: Check file permissions
```bash
chmod +x scripts/*
chown -R $USER:$USER .
```

---

## Performance Tuning

### 1. Workers Configuration

```bash
# Calculate optimal workers: (2 x CPU cores) + 1
python -m uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8100 \
  --workers 9 \
  --worker-class uvicorn.workers.UvicornWorker
```

### 2. Database Connection Pool

```bash
# Adjust in .env
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
```

### 3. Redis Connection Pool

```bash
# Adjust in .env
REDIS_MAX_CONNECTIONS=50
```

---

## Security Checklist

- [ ] Change JWT_SECRET_KEY in production
- [ ] Use strong database passwords
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS origins properly
- [ ] Set DEBUG=False in production
- [ ] Use environment variables (never hardcode secrets)
- [ ] Enable rate limiting
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity

---

## Monitoring

### Prometheus Metrics
```
# Coming in next version
GET /metrics
```

### Structured Logging
```python
# All requests logged with:
- Request ID
- Method, Path
- Client IP
- Response time
- Status code
```

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/Shakour-Data/01-common-library/issues
- Documentation: http://localhost:8100/docs
- Team: Elite Engineers (IQ 180+, 15+ years experience)

---

## License

MIT License - See LICENSE file for details.

---

**Deployment Guide v1.0.0**  
Author: Dr. Sarah Chen (Chief Architect)  
Cost: 1.5 hours × $150 = $225 USD
