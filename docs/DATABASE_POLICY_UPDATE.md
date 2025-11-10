# ⚠️ CRITICAL UPDATE: Database Architecture Changed

## Date: November 8, 2025

---

## 🎯 Major Policy Change: Database-Agnostic Design

### What Changed?

Previously, microservices included database configurations and assumed databases existed.

**NOW:** Microservices are **completely database-agnostic** and **portable**.

---

## New Architecture Principles

### ✅ Microservice Responsibility:
1. **Define schemas** (SQLAlchemy models)
2. **Provide migrations** (Alembic scripts)
3. **Accept DATABASE_URL** from environment
4. **Document requirements** (DB type, permissions, extensions)

### ✅ Project Responsibility:
1. **Create databases** (PostgreSQL, MySQL, etc.)
2. **Set up credentials** (users, passwords, permissions)
3. **Configure environment** (DATABASE_URL variable)
4. **Execute migrations** (`alembic upgrade head`)
5. **Choose topology** (single DB, DB-per-service, multi-tenant, etc.)

---

## What This Means

### For Microservices:
- ❌ **DO NOT** include docker-compose with databases
- ❌ **DO NOT** create databases in code
- ❌ **DO NOT** hardcode database connections
- ✅ **DO** define models and migrations
- ✅ **DO** accept DATABASE_URL from environment
- ✅ **DO** document database requirements

### For Projects Using Microservices:
- ✅ **You create** the database(s)
- ✅ **You configure** DATABASE_URL
- ✅ **You run** migrations
- ✅ **You choose** topology (single DB vs multiple)
- ✅ **You control** database technology (PostgreSQL, MySQL, etc.)

---

## Example Scenarios

### Scenario 1: Small Project (1 Database)
```
project_db/
├── user_profiles (from user-service)
├── auth_users (from auth-service)
├── payments (from payment-service)
└── logs (from log-service)
```

**All services share one database.**

```env
USER_SERVICE_DATABASE_URL=postgresql://user@host/project_db
AUTH_SERVICE_DATABASE_URL=postgresql://user@host/project_db
PAYMENT_SERVICE_DATABASE_URL=postgresql://user@host/project_db
```

### Scenario 2: Enterprise (Database-per-Service)
```
├── user_service_db (isolated)
├── auth_service_db (isolated)
├── payment_service_db (isolated)
└── log_service_db (isolated)
```

**Each service has dedicated database.**

```env
USER_SERVICE_DATABASE_URL=postgresql://user_svc@host/user_service_db
AUTH_SERVICE_DATABASE_URL=postgresql://auth_svc@host/auth_service_db
PAYMENT_SERVICE_DATABASE_URL=postgresql://pay_svc@host/payment_service_db
```

### Scenario 3: Multi-Tenant
```
Tenant A: user_svc_tenant_a, auth_svc_tenant_a
Tenant B: user_svc_tenant_b, auth_svc_tenant_b
```

**Complete isolation per tenant.**

---

## Benefits of This Approach

### 🚀 Portability
- Deploy anywhere (cloud, on-premise, hybrid)
- Use any database (PostgreSQL, MySQL, MongoDB)
- Mix technologies (PostgreSQL + MongoDB + Redis)

### 💰 Cost Efficiency
- Small projects: 1 database for all services
- Large projects: Scale as needed
- No forced database multiplication

### 🔒 Security
- Project controls credentials
- Custom isolation levels
- Flexible backup strategies

### ⚡ Flexibility
- Choose DB per workload
- Scale independently
- Multi-tenant support

---

## Documentation Updates

### New Documents Created:
1. **`docs/DATABASE_ARCHITECTURE.md`** - Complete architecture guide
2. **`user-service/DATABASE.md`** - User Service database setup guide

### Updated Documents:
1. **`docs/TEAM_PROMPT.md`** - Added database policy section
2. **`user-service/README.md`** - Updated with database setup instructions
3. **`user-service/docker-compose.yml`** - Marked as example only

---

## User Service Updates

### ✅ What's Complete:
- Database models (3 tables)
- Alembic migrations
- Environment-based configuration
- API endpoints (15 total)
- Service layer
- Documentation

### 📝 Documentation Added:
- Database requirements
- Setup instructions (PostgreSQL, MySQL)
- Topology examples (single DB, DB-per-service, multi-tenant)
- Docker examples
- Kubernetes examples
- Cloud database examples (AWS, GCP, Azure)
- Backup & recovery procedures
- Troubleshooting guide

### ⚠️ Important Notes:
- `docker-compose.yml` is **example only**
- Projects must create databases
- DATABASE_URL **must** be configured
- Migrations **must** be executed by project

---

## Migration Guide for Existing Projects

If you already deployed user-service with included database:

### Step 1: Extract Database
```bash
# Backup current data
docker exec user-postgres pg_dump -U user_service user_db > backup.sql
```

### Step 2: Move to Project Infrastructure
```bash
# Create database in your project's PostgreSQL
psql -U postgres -c "CREATE DATABASE user_service_db;"

# Restore data
psql -U postgres user_service_db < backup.sql
```

### Step 3: Update Configuration
```env
# Remove docker-compose database
# Update .env to point to project database
DATABASE_URL=postgresql+asyncpg://user@host/user_service_db
```

### Step 4: Restart Service
```bash
docker-compose up -d user-service  # Only service, no database
```

---

## Quick Reference

### Microservice Provides:
```python
# models/user_profile.py
class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(String(36), primary_key=True)
    # ... schema definition
```

```python
# alembic/versions/001_initial.py
def upgrade():
    op.create_table('user_profiles', ...)
```

### Project Provides:
```sql
-- Project creates database
CREATE DATABASE user_service_db;
CREATE USER user_svc WITH PASSWORD 'secure';
GRANT ALL PRIVILEGES ON DATABASE user_service_db TO user_svc;
```

```env
# Project configures environment
DATABASE_URL=postgresql+asyncpg://user_svc:secure@host/user_service_db
```

```bash
# Project runs migrations
cd user-service && alembic upgrade head
```

---

## Impact on Other Services

### Services to Update:
- [ ] auth-service
- [ ] api-gateway (no database needed)
- [ ] service-discovery (uses Consul)
- [ ] common-library (utilities only)
- [x] user-service (COMPLETE)

### Services in Development:
All future services will follow this pattern from day 1.

---

## Summary

| Before | After |
|--------|-------|
| Microservice includes database | Microservice defines schema only |
| docker-compose creates DB | Project creates DB |
| Hardcoded connections | Environment-based |
| One topology (DB-per-service) | Flexible topology |
| PostgreSQL only | Any compatible DB |

---

## Questions?

**Q: Do I need to create separate databases for each service?**  
A: No! You can use one database for all services (small projects) or separate databases (large projects). Your choice!

**Q: Can I use MySQL instead of PostgreSQL?**  
A: Yes! Just change DATABASE_URL and ensure compatible SQLAlchemy driver.

**Q: What about the example docker-compose.yml?**  
A: It's for development/testing only. Create your own for production.

**Q: Who runs migrations?**  
A: Your project runs migrations: `alembic upgrade head`

**Q: Can I use cloud databases (AWS RDS, etc.)?**  
A: Absolutely! Just configure DATABASE_URL to point to your cloud database.

---

**See Full Documentation:**
- `docs/DATABASE_ARCHITECTURE.md` - Architecture philosophy
- `user-service/DATABASE.md` - Setup guide with examples
- `docs/TEAM_PROMPT.md` - Team standards

---

**Status:** ✅ IMPLEMENTED  
**Date:** November 8, 2025  
**Author:** Dr. Sarah Chen + Elena Volkov  
**Impact:** ALL MICROSERVICES (current and future)
