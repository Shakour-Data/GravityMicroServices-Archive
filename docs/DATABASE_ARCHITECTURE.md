# Database Architecture - Gravity MicroServices

## Philosophy: Database-Agnostic Design

### Core Principle
**Microservices do NOT come with databases. They are portable, reusable components that adapt to the target project's database infrastructure.**

---

## Key Concepts

### 1. No Pre-Configured Databases
- Microservices **define** database schemas (via models)
- Microservices **do not create** databases
- Each deployment project sets up its own databases
- Database choice is project-specific (PostgreSQL, MySQL, MongoDB, etc.)

### 2. Portable Schema Definition
```python
# ✅ Good: Define schema, let project create database
class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(String(36), primary_key=True)
    # ... fields

# ❌ Bad: Hardcode database connection
engine = create_engine("postgresql://localhost/mydb")
```

### 3. Environment-Based Configuration
```python
# config.py - Database URL from environment
DATABASE_URL: str = Field(
    ...,  # Required, no default
    description="Database connection URL (provided by deployment)"
)
```

---

## Implementation Pattern

### Service Responsibility
Each microservice provides:

1. **Database Models** (SQLAlchemy)
   - Table definitions
   - Relationships
   - Indexes
   - Constraints

2. **Alembic Migrations**
   - Schema versioning
   - Migration scripts
   - Upgrade/downgrade paths

3. **Configuration Interface**
   - Environment variable specification
   - Connection parameter requirements
   - Database feature requirements

### Project Responsibility
The deployment project handles:

1. **Database Creation**
   ```sql
   CREATE DATABASE user_service_db;
   CREATE DATABASE auth_service_db;
   CREATE DATABASE payment_service_db;
   ```

2. **User & Permissions**
   ```sql
   CREATE USER service_user WITH PASSWORD 'xxx';
   GRANT ALL PRIVILEGES ON DATABASE user_service_db TO service_user;
   ```

3. **Environment Configuration**
   ```env
   USER_SERVICE_DATABASE_URL=postgresql://service_user:xxx@localhost/user_service_db
   AUTH_SERVICE_DATABASE_URL=postgresql://service_user:xxx@localhost/auth_service_db
   ```

4. **Migration Execution**
   ```bash
   cd user-service && alembic upgrade head
   cd auth-service && alembic upgrade head
   ```

---

## Deployment Scenarios

### Scenario 1: Single Database (Small Project)
```
Project Database: app_db
├── user_profiles (user-service tables)
├── auth_users (auth-service tables)
├── payments (payment-service tables)
└── notifications (notification-service tables)
```

All services connect to same database with different table prefixes.

### Scenario 2: Database-per-Service (Medium Project)
```
├── user_service_db (user-service)
├── auth_service_db (auth-service)
├── payment_service_db (payment-service)
└── notification_service_db (notification-service)
```

Each service has isolated database (microservices best practice).

### Scenario 3: Database-per-Tenant (Enterprise)
```
Tenant A:
├── tenant_a_user_db
├── tenant_a_auth_db
└── tenant_a_payment_db

Tenant B:
├── tenant_b_user_db
├── tenant_b_auth_db
└── tenant_b_payment_db
```

Multi-tenant deployment with database isolation.

### Scenario 4: Mixed Databases (Hybrid)
```
├── PostgreSQL: auth_service, user_service
├── MySQL: payment_service, order_service
├── MongoDB: log_service, analytics_service
└── Redis: cache, sessions (all services)
```

Different database technologies for different services.

---

## Docker Compose Example

### Development (Single Database)
```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: gravity_dev
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_pass
    volumes:
      - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql

  user-service:
    build: ./user-service
    environment:
      DATABASE_URL: postgresql+asyncpg://dev_user:dev_pass@postgres/gravity_dev
    depends_on:
      - postgres

  auth-service:
    build: ./auth-service
    environment:
      DATABASE_URL: postgresql+asyncpg://dev_user:dev_pass@postgres/gravity_dev
    depends_on:
      - postgres
```

### Production (Database-per-Service)
```yaml
services:
  user-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: user_service
      POSTGRES_USER: user_svc
      POSTGRES_PASSWORD: ${USER_DB_PASS}

  auth-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: auth_service
      POSTGRES_USER: auth_svc
      POSTGRES_PASSWORD: ${AUTH_DB_PASS}

  user-service:
    build: ./user-service
    environment:
      DATABASE_URL: postgresql+asyncpg://user_svc:${USER_DB_PASS}@user-db/user_service
    depends_on:
      - user-db

  auth-service:
    build: ./auth-service
    environment:
      DATABASE_URL: postgresql+asyncpg://auth_svc:${AUTH_DB_PASS}@auth-db/auth_service
    depends_on:
      - auth-db
```

---

## Migration Management

### Service Provides Migrations
```bash
user-service/
└── alembic/
    └── versions/
        ├── 001_initial.py
        ├── 002_add_avatar.py
        └── 003_add_sessions.py
```

### Project Executes Migrations
```bash
# Option 1: Manual
cd user-service
alembic upgrade head

# Option 2: Docker entrypoint
docker-compose run user-service alembic upgrade head

# Option 3: Init container (Kubernetes)
initContainers:
  - name: migrations
    image: user-service:latest
    command: ["alembic", "upgrade", "head"]
```

---

## Database Configuration Interface

### Service README Must Specify

#### Required Environment Variables
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/dbname
# OR
DB_HOST=localhost
DB_PORT=5432
DB_NAME=user_service
DB_USER=service_user
DB_PASSWORD=secret
```

#### Database Requirements
- PostgreSQL 16+ (or alternative)
- Required extensions: uuid-ossp, pg_trgm
- Required permissions: CREATE, SELECT, INSERT, UPDATE, DELETE
- Estimated size: 100MB initial, 1GB/year growth

#### Schema Information
- Tables: 3 (user_profiles, user_preferences, user_sessions)
- Indexes: 15
- Foreign keys: 2
- Functions/Triggers: 0

---

## Benefits of This Approach

### ✅ Portability
- Deploy to any infrastructure
- Use any compatible database
- Mix database technologies

### ✅ Flexibility
- Single database for small projects
- Multiple databases for scaling
- Multi-tenant deployments

### ✅ Security
- Project controls credentials
- Isolated databases possible
- Custom encryption/backup

### ✅ Cost Efficiency
- Small projects: 1 database for all services
- Large projects: Database-per-service
- No forced database multiplication

### ✅ Technology Freedom
- PostgreSQL, MySQL, MariaDB
- MongoDB for document services
- SQLite for testing
- Cloud databases (RDS, Cloud SQL)

---

## Anti-Patterns (Avoid)

### ❌ Hardcoded Database
```python
# BAD: Hardcoded connection
engine = create_engine("postgresql://localhost/mydb")
```

### ❌ Database Creation in Code
```python
# BAD: Service creates database
def init_db():
    conn = psycopg2.connect(host="localhost")
    conn.cursor().execute("CREATE DATABASE user_service")
```

### ❌ Assuming Database Exists
```python
# BAD: No error handling for missing DB
app.on_startup(init_database_tables)  # Fails if DB doesn't exist
```

### ✅ Correct Pattern
```python
# GOOD: Environment-based, fails gracefully
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not configured")

engine = create_async_engine(DATABASE_URL)

# Provide clear migration instructions in README
```

---

## Documentation Requirements

Every microservice must include:

### 1. DATABASE.md
```markdown
# Database Setup

## Requirements
- PostgreSQL 16+ (or MySQL 8+)
- Required extensions: uuid-ossp
- Minimum permissions: CREATE, SELECT, INSERT, UPDATE, DELETE

## Setup Steps
1. Create database: `CREATE DATABASE service_name;`
2. Configure URL: `DATABASE_URL=postgresql://...`
3. Run migrations: `alembic upgrade head`

## Schema Overview
- Tables: 3
- Estimated size: 100MB
- Growth rate: ~1GB/year
```

### 2. docker-compose.yml (Example Only)
```yaml
# EXAMPLE: Not for production use
# Projects should create their own docker-compose
services:
  db:
    image: postgres:16-alpine
    # ... example configuration

  service:
    build: .
    environment:
      DATABASE_URL: postgresql://...
```

Mark clearly: **"This is an example. Configure for your project."**

---

## Summary

| Aspect | Microservice Provides | Project Provides |
|--------|----------------------|------------------|
| **Models** | ✅ Table definitions | ❌ |
| **Migrations** | ✅ Alembic scripts | ❌ |
| **Database** | ❌ | ✅ Creates database |
| **Credentials** | ❌ | ✅ Sets credentials |
| **Connection** | ✅ Uses from env | ✅ Provides via env |
| **Backup** | ❌ | ✅ Project responsibility |
| **Scaling** | ❌ | ✅ Project decision |

---

**Key Takeaway**: Microservices are like **blueprints**. Projects are **construction sites** that build according to blueprints.

🏗️ **Service = Blueprint (schema)**  
🏢 **Project = Building (actual database)**

---

**Document Version**: 1.0.0  
**Last Updated**: November 8, 2025  
**Author**: Dr. Sarah Chen (Chief Architect)
