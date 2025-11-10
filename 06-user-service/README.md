# Gravity User Service

**Portable, database-agnostic user profile and preference management microservice.**

## ⚠️ Important: Database Setup Required

**This microservice does NOT include a database.** It provides:
- ✅ Database schema definitions (SQLAlchemy models)
- ✅ Database migrations (Alembic)
- ✅ API endpoints and business logic

**Your project must:**
- Create the database (PostgreSQL, MySQL, etc.)
- Configure DATABASE_URL environment variable
- Run migrations: `alembic upgrade head`

See [Database Setup](#database-setup) section below.

---

## Overview

The User Service provides comprehensive user profile management, including:
- User profiles (display name, bio, avatar, location, website)
- User preferences (language, timezone, theme, notifications)
- Session management (active sessions, device tracking)
- Avatar upload/management (integrates with File Service)

## Features

- ✅ User profile CRUD operations
- ✅ User preference management
- ✅ Active session tracking
- ✅ Avatar upload/download
- ✅ Search users by display name
- ✅ JWT authentication via Auth Service
- ✅ PostgreSQL database per service
- ✅ Redis caching for sessions
- ✅ Prometheus metrics
- ✅ Docker support
- ✅ 95%+ test coverage

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Database**: PostgreSQL 16
- **Cache**: Redis 7
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Validation**: Pydantic 2.0
- **Testing**: pytest, pytest-asyncio
- **Monitoring**: Prometheus, Grafana

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 16+ (or MySQL 8+, MariaDB 10.6+)
- Python package manager (pip or Poetry)
- Redis 7+ (optional, for caching)
- Poetry 1.7+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/GravityWavesMl/user-service.git
cd user-service
```

2. Install dependencies:
```bash
poetry install
```

3. **Setup database** (ONE command):
```bash
# Set credentials
export POSTGRES_ADMIN_PASSWORD=your_admin_password
export DB_PASSWORD=your_service_password

# Run setup script (choose one):
python scripts/setup_database.py           # Python (cross-platform)
./scripts/setup_database.sh                # Bash (Linux/macOS)
.\scripts\setup_database.ps1               # PowerShell (Windows)
```

This creates:
- Database: `user_service_db`
- User: `user_service` with password
- Required extensions (uuid-ossp)
- Correct privileges

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your database URL
```

5. Run database migrations:
```bash
poetry run alembic upgrade head
```

6. Start the service:
```bash
poetry run uvicorn app.main:app --reload --port 8082
```

### Docker (Example Only)

⚠️ **Note:** The included `docker-compose.yml` is an **example** for development/testing.  
Your production project should create its own Docker setup.

```bash
docker-compose up --build
```

This example creates a PostgreSQL database automatically. In production, use your project's database infrastructure.

## API Endpoints

### Health Check
- `GET /health` - Service health status
- `GET /` - Service information

### User Profiles
- `GET /api/v1/users` - List users (paginated)
- `GET /api/v1/users/me` - Get current user profile
- `GET /api/v1/users/{id}` - Get user profile by ID
- `POST /api/v1/users` - Create user profile
- `PATCH /api/v1/users/{id}` - Update user profile
- `DELETE /api/v1/users/{id}` - Delete user profile

### User Preferences
- `GET /api/v1/users/{id}/preferences` - Get user preferences
- `PATCH /api/v1/users/{id}/preferences` - Update user preferences

### User Sessions
- `GET /api/v1/users/{id}/sessions` - Get active sessions
- `DELETE /api/v1/users/{id}/sessions/{session_id}` - Revoke session

### Avatar Management
- `POST /api/v1/users/{id}/avatar` - Upload avatar
- `DELETE /api/v1/users/{id}/avatar` - Delete avatar

### Search
- `GET /api/v1/users/search?q={query}` - Search users

## Database Setup

### 🎯 One-Command Setup (Recommended)

**Set credentials and run:**
```bash
# Set your credentials
export POSTGRES_ADMIN_PASSWORD=your_postgres_password
export DB_PASSWORD=your_service_password

# Run setup script (choose one)
python scripts/setup_database.py           # Python (recommended)
./scripts/setup_database.sh                # Bash (Linux/macOS)
.\scripts\setup_database.ps1               # PowerShell (Windows)
```

**Or use Makefile:**
```bash
make setup-db  # Runs Python script
```

The script automatically:
- ✅ Creates database `user_service_db`
- ✅ Creates user `user_service` with your password
- ✅ Grants all necessary privileges
- ✅ Enables required extensions (uuid-ossp)
- ✅ Prints DATABASE_URL for your .env file

**See [SETUP.md](SETUP.md) for detailed guide.**

### Requirements

**Database Type:** PostgreSQL 16+ (recommended) or MySQL 8+  
**Required Extensions:** `uuid-ossp` (PostgreSQL only)  
**Required Permissions:** CREATE, SELECT, INSERT, UPDATE, DELETE  
**Estimated Size:** 100MB initial, ~1GB/year growth  

### Setup Steps

1. **Create Database:**
```sql
-- PostgreSQL
CREATE DATABASE user_service_db;

-- MySQL
CREATE DATABASE user_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. **Create User & Grant Permissions:**
```sql
-- PostgreSQL
CREATE USER user_svc WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE user_service_db TO user_svc;

-- MySQL
CREATE USER 'user_svc'@'%' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON user_service_db.* TO 'user_svc'@'%';
```

3. **Configure Environment:**
```env
# PostgreSQL
DATABASE_URL=postgresql+asyncpg://user_svc:secure_password@localhost:5432/user_service_db

# MySQL
DATABASE_URL=mysql+aiomysql://user_svc:secure_password@localhost:3306/user_service_db
```

4. **Run Migrations:**
```bash
poetry run alembic upgrade head
```

### Deployment Topologies

#### Option 1: Single Database (Small Projects)
```
project_db/
├── user_profiles (user-service)
├── auth_users (auth-service)
└── payments (payment-service)
```
All services share one database with different tables.

#### Option 2: Database-per-Service (Microservices Best Practice)
```
├── user_service_db (isolated)
├── auth_service_db (isolated)
└── payment_service_db (isolated)
```
Each service has its own database.

#### Option 3: Multi-Tenant
```
Tenant A: user_service_tenant_a_db
Tenant B: user_service_tenant_b_db
```

Choose based on your project requirements!

---

## Database Schema

### user_profiles
- id (UUID, PK)
- user_id (UUID, FK to auth-service)
- display_name (varchar)
- bio (text)
- avatar_url (varchar)
- location (varchar)
- website (varchar)
- phone_number (varchar)
- is_verified (boolean)
- is_active (boolean)
- created_at (timestamp)
- updated_at (timestamp)
- last_login_at (timestamp)

### user_preferences
- id (UUID, PK)
- profile_id (UUID, FK)
- language (varchar)
- timezone (varchar)
- theme (varchar)
- date_format (varchar)
- time_format (varchar)
- email_notifications (boolean)
- push_notifications (boolean)
- sms_notifications (boolean)
- newsletter (boolean)
- marketing (boolean)
- custom_settings (json)
- created_at (timestamp)
- updated_at (timestamp)

### user_sessions
- id (UUID, PK)
- profile_id (UUID, FK)
- session_token (varchar)
- device_type (varchar)
- device_name (varchar)
- os (varchar)
- ip_address (varchar)
- user_agent (text)
- is_active (boolean)
- created_at (timestamp)
- last_activity_at (timestamp)
- expires_at (timestamp)
- logout_at (timestamp)

## Testing

Run tests:
```bash
poetry run pytest
```

Run tests with coverage:
```bash
poetry run pytest --cov=app --cov-report=html
```

## Development

### Code Quality

Format code:
```bash
poetry run black app tests
poetry run isort app tests
```

Lint code:
```bash
poetry run ruff app tests
poetry run mypy app
```

### Database Migrations

Create migration:
```bash
poetry run alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
poetry run alembic upgrade head
```

Rollback migration:
```bash
poetry run alembic downgrade -1
```

## Configuration

Key environment variables:

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `AUTH_SERVICE_URL` - Auth service URL
- `FILE_SERVICE_URL` - File service URL
- `JWT_SECRET_KEY` - JWT secret key
- `MAX_AVATAR_SIZE` - Maximum avatar size (bytes)
- `MAX_ACTIVE_SESSIONS` - Max active sessions per user

See `.env.example` for full configuration options.

## Documentation

- [API Documentation](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Testing Guide](docs/TESTING.md)

## Contributing

1. Follow conventional commits
2. Maintain 95%+ test coverage
3. Use type hints everywhere
4. Format code with black/isort
5. Lint with ruff/mypy

## License

MIT License - see LICENSE file

## Authors

- Elena Volkov (Backend & Integration Lead)
- Dr. Sarah Chen (Chief Architect)

## Support

For issues and questions, please open a GitHub issue.
