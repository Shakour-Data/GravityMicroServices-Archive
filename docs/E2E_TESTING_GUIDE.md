# End-to-End Testing Guide

## Overview

This guide walks you through complete end-to-end testing of User Service integration with Auth Service.

**Estimated Time:** 30-60 minutes  
**Cost:** $75-$150 USD

---

## Prerequisites

### Required Software:
- ✅ Docker Desktop (running)
- ✅ Python 3.11+
- ✅ PowerShell 7+

### Check Prerequisites:
```powershell
# Check Docker
docker --version
docker ps

# Check Python
python --version

# Check PowerShell
$PSVersionTable.PSVersion
```

---

## Phase 1: Infrastructure Setup (10 minutes)

### Step 1: Start Infrastructure Services

```powershell
# Navigate to project root
cd E:\Shakour\GravityMicroServices

# Start PostgreSQL, Redis, Consul
docker-compose -f docker-compose.e2e.yml up -d

# Wait for services to be healthy (30 seconds)
Start-Sleep -Seconds 30

# Verify services are running
docker ps --filter "name=gravity-"
```

**Expected Output:**
```
CONTAINER ID   IMAGE              STATUS         PORTS
xxxxx          postgres:16        Up 30 seconds  0.0.0.0:5432->5432/tcp
xxxxx          redis:7            Up 30 seconds  0.0.0.0:6379->6379/tcp
xxxxx          consul:1.17        Up 30 seconds  0.0.0.0:8500->8500/tcp
```

### Step 2: Verify Service Health

```powershell
# Check PostgreSQL
docker exec gravity-postgres-e2e pg_isready -U gravity

# Check Redis
docker exec gravity-redis-e2e redis-cli -a redis_secret_2025 ping

# Check Consul UI
Start-Process "http://localhost:8500"
```

---

## Phase 2: Database Setup (10 minutes)

### Auth Service Database

```powershell
cd E:\Shakour\GravityMicroServices\auth-service

# Setup database
.\scripts\setup_database.ps1

# Run migrations
alembic upgrade head
```

**Expected Output:**
```
✅ Database 'auth_db' created successfully
✅ User 'auth_service' created successfully
✅ Privileges granted
✅ Extension 'uuid-ossp' enabled
```

### User Service Database

```powershell
cd E:\Shakour\GravityMicroServices\user-service

# Setup database
.\scripts\setup_database.ps1

# Run migrations (if applicable)
# alembic upgrade head
```

**Expected Output:**
```
✅ Database 'user_db' created successfully
✅ User 'user_service' created successfully
✅ Privileges granted
✅ Extension 'uuid-ossp' enabled
```

---

## Phase 3: Start Services (5 minutes)

### Terminal 1: Start Auth Service

```powershell
cd E:\Shakour\GravityMicroServices\auth-service

# Activate virtual environment (if using)
# .\.venv\Scripts\Activate.ps1

# Start Auth Service
uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8081
INFO:     Application startup complete
✅ Registered with Consul: auth-service
```

### Terminal 2: Start User Service

```powershell
cd E:\Shakour\GravityMicroServices\user-service

# Activate virtual environment (if using)
# .\.venv\Scripts\Activate.ps1

# Start User Service
uvicorn app.main:app --host 0.0.0.0 --port 8082 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8082
INFO:     Application startup complete
✅ Registered with Consul: user-service
```

---

## Phase 4: Verify Service Registration (2 minutes)

### Check Consul Service Discovery

1. Open Consul UI: http://localhost:8500
2. Navigate to "Services"
3. Verify both services are registered:
   - ✅ `auth-service` (healthy, port 8081)
   - ✅ `user-service` (healthy, port 8082)

### Check Service Health Endpoints

```powershell
# Auth Service health
curl http://localhost:8081/health

# User Service health
curl http://localhost:8082/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "user-service",
  "version": "1.0.0",
  "timestamp": "2025-11-08T20:00:00Z",
  "service_discovery": {
    "consul_available": true,
    "registered": true
  }
}
```

---

## Phase 5: Integration Testing (15-20 minutes)

### Test 1: Create Test User in Auth Service

```powershell
# Create a test user
$body = @{
    username = "testuser"
    email = "test@example.com"
    password = "TestPassword123!"
    full_name = "Test User"
} | ConvertTo-Json

curl -X POST http://localhost:8081/api/v1/auth/register `
  -H "Content-Type: application/json" `
  -d $body
```

**Expected Response:**
```json
{
  "id": "user-123-456",
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "is_active": true,
  "created_at": "2025-11-08T20:00:00Z"
}
```

### Test 2: Login and Get JWT Token

```powershell
# Login
$loginBody = @{
    username = "testuser"
    password = "TestPassword123!"
} | ConvertTo-Json

$response = curl -X POST http://localhost:8081/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d $loginBody | ConvertFrom-Json

$token = $response.access_token
Write-Host "Token: $token"
```

**Expected Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Test 3: Create User Profile in User Service

```powershell
# Create profile using JWT token
$profileBody = @{
    user_id = "user-123-456"
    display_name = "Test User"
    bio = "This is a test user"
    avatar_url = "https://example.com/avatar.jpg"
} | ConvertTo-Json

curl -X POST http://localhost:8082/api/v1/profiles `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer $token" `
  -d $profileBody
```

**Expected Response:**
```json
{
  "id": "profile-789",
  "user_id": "user-123-456",
  "display_name": "Test User",
  "bio": "This is a test user",
  "avatar_url": "https://example.com/avatar.jpg",
  "created_at": "2025-11-08T20:00:00Z"
}
```

### Test 4: Get User Profile (Verify Token Validation)

```powershell
# Get profile - this will validate token with Auth Service
curl http://localhost:8082/api/v1/profiles/me `
  -H "Authorization: Bearer $token"
```

**Expected:** ✅ Profile returned successfully (token validated via Auth Service)

### Test 5: Test Fallback - Stop Auth Service

```powershell
# In Terminal 1, stop Auth Service (Ctrl+C)

# Try to get profile again
curl http://localhost:8082/api/v1/profiles/me `
  -H "Authorization: Bearer $token"
```

**Expected:** ✅ Profile still returned (local JWT validation fallback activated)

**Check User Service logs for:**
```
WARNING: ⚠️ Using local token validation (Auth Service unavailable)
```

### Test 6: Restart Auth Service

```powershell
# Restart Auth Service in Terminal 1
uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload

# Try to get profile again
curl http://localhost:8082/api/v1/profiles/me `
  -H "Authorization: Bearer $token"
```

**Expected:** ✅ Profile returned (Auth Service validation restored)

---

## Phase 6: Automated Tests (10 minutes)

### Run Auth Integration Tests

```powershell
cd E:\Shakour\GravityMicroServices\user-service

# Run integration tests
pytest tests/test_auth_integration.py -v

# Expected: All 11 tests PASSED
```

### Run Full Test Suite (Optional)

```powershell
# Run all tests with coverage
pytest tests/ -v --cov=app --cov-report=html

# Open coverage report
Start-Process htmlcov/index.html
```

---

## Phase 7: Cleanup (2 minutes)

### Stop Services

```powershell
# Stop Auth Service (Ctrl+C in Terminal 1)
# Stop User Service (Ctrl+C in Terminal 2)

# Stop infrastructure
cd E:\Shakour\GravityMicroServices
docker-compose -f docker-compose.e2e.yml down

# Optional: Remove volumes
docker-compose -f docker-compose.e2e.yml down -v
```

---

## Expected Results

### ✅ Success Criteria:

1. **Infrastructure:**
   - ✅ PostgreSQL, Redis, Consul running
   - ✅ All services healthy

2. **Service Registration:**
   - ✅ Auth Service registered in Consul
   - ✅ User Service registered in Consul
   - ✅ Health checks passing

3. **Token Validation:**
   - ✅ User Service validates tokens with Auth Service
   - ✅ Fallback to local validation works
   - ✅ No errors in logs

4. **Integration Tests:**
   - ✅ All 11 Auth integration tests pass
   - ✅ Token validation tests pass
   - ✅ Service discovery tests pass

---

## Troubleshooting

### Issue: Docker services not starting

**Solution:**
```powershell
# Check Docker Desktop is running
docker ps

# Restart Docker Desktop
# Open Docker Desktop app → Restart
```

### Issue: Port already in use

**Solution:**
```powershell
# Check what's using the port
Get-NetTCPConnection -LocalPort 8081,8082,5432,6379,8500

# Stop conflicting services
Stop-Service <service-name>
```

### Issue: Database connection failed

**Solution:**
```powershell
# Verify PostgreSQL is running
docker exec gravity-postgres-e2e pg_isready -U gravity

# Check database exists
docker exec -it gravity-postgres-e2e psql -U gravity -c "\l"

# Re-run setup script
cd user-service
.\scripts\setup_database.ps1
```

### Issue: Service not registering with Consul

**Solution:**
```powershell
# Check Consul is running
curl http://localhost:8500/v1/status/leader

# Check service logs for errors
# Look for "Registered with Consul" message

# Verify SERVICE_DISCOVERY_URL in .env
# Should be: http://localhost:8500
```

---

## Next Steps

After successful E2E testing:

1. ✅ Document findings in `E2E_TEST_RESULTS.md`
2. ✅ Fix any issues discovered
3. 🚀 Proceed to build Notification Service

---

**Last Updated:** November 8, 2025  
**Version:** 1.0.0  
**Author:** GitHub Copilot (Elite Engineers Team)
