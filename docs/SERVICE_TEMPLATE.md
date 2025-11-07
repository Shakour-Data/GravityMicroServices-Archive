# 🎯 Microservice Template - استاندارد ایجاد میکروسرویس جدید

## 📋 راهنمای ایجاد میکروسرویس جدید

این template استاندارد برای ایجاد هر میکروسرویس **کاملاً مستقل** است.

---

## 🚀 مراحل ایجاد سرویس جدید

### 1. ایجاد Repository

```bash
# ایجاد directory
mkdir my-new-service
cd my-new-service

# مقداردهی Git
git init
git remote add origin https://github.com/gravity/my-new-service.git
```

### 2. ایجاد Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### 3. ایجاد ساختار پروژه

```bash
mkdir -p app/{api/v1,core,models,schemas,services}
mkdir -p tests alembic/versions scripts kubernetes
touch app/__init__.py app/main.py app/config.py
touch tests/__init__.py tests/conftest.py
touch .gitignore .env.example README.md
```

---

## 📁 ساختار استاندارد

```
my-new-service/
├── .git/                           # Git repository ✅
├── .github/
│   └── workflows/
│       └── ci.yml                  # CI/CD pipeline
├── .venv/                          # Virtual environment (gitignored)
│
├── app/                            # کد اصلی application
│   ├── __init__.py
│   ├── main.py                     # FastAPI app factory
│   ├── config.py                   # Pydantic settings
│   ├── dependencies.py             # FastAPI dependencies
│   │
│   ├── core/                       # Core utilities
│   │   ├── __init__.py
│   │   ├── database.py             # Database session
│   │   └── redis_client.py         # Redis client
│   │
│   ├── models/                     # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── entity.py
│   │
│   ├── schemas/                    # Pydantic schemas
│   │   ├── __init__.py
│   │   └── entity.py
│   │
│   ├── services/                   # Business logic
│   │   ├── __init__.py
│   │   └── entity_service.py
│   │
│   └── api/                        # API endpoints
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           └── entity.py
│
├── tests/                          # Tests
│   ├── __init__.py
│   ├── conftest.py                 # Test fixtures
│   ├── test_api.py                 # Integration tests
│   └── test_services.py            # Unit tests
│
├── alembic/                        # Database migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── scripts/                        # Utility scripts
│   ├── __init__.py
│   └── migrate.py
│
├── kubernetes/                     # K8s manifests
│   ├── deployment.yml
│   ├── service.yml
│   └── ingress.yml
│
├── docker-compose.yml              # Infrastructure ✅
├── Dockerfile                      # Container image
├── pyproject.toml                  # Poetry dependencies ✅
├── poetry.lock
├── alembic.ini                     # Alembic config
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore
├── README.md                       # Documentation
├── DEPLOYMENT.md                   # Deployment guide
└── LICENSE                         # License
```

---

## 📝 Template Files

### 1. pyproject.toml

```toml
[tool.poetry]
name = "my-new-service"
version = "1.0.0"
description = "Independent microservice description"
authors = ["Gravity Elite Team <team@gravity.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"

# Web Framework
fastapi = "^0.104.1"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
pydantic = {extras = ["email"], version = "^2.5.0"}
pydantic-settings = "^2.1.0"

# Database - PostgreSQL
sqlalchemy = {extras = ["asyncio"], version = "^2.0.23"}
asyncpg = "^0.29.0"
alembic = "^1.13.0"

# Redis
redis = {extras = ["hiredis"], version = "^5.0.1"}

# Common library
gravity-common = {git = "https://github.com/gravity/gravity-common.git", tag = "v1.0.0"}

# Utilities
python-dotenv = "^1.0.0"
python-json-logger = "^2.0.7"
httpx = "^0.25.2"

# Monitoring
prometheus-fastapi-instrumentator = "^6.1.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.3"
pytest-asyncio = "^0.23.2"
pytest-cov = "^4.1.0"
black = "^23.12.1"
mypy = "^1.7.1"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "--cov=app --cov-report=term-missing --cov-fail-under=80"

[tool.black]
line-length = 100
target-version = ['py311']
```

### 2. docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16
    container_name: my-service-postgres
    environment:
      POSTGRES_DB: my_service_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: my-service-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  my-service:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: my-service
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@postgres:5432/my_service_db
      REDIS_URL: redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### 3. app/main.py

```python
"""
FastAPI application factory.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import settings
from app.core.database import engine
from app.api.v1 import router as api_v1_router
from gravity_common.logging_config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    # Startup
    setup_logging(settings.LOG_LEVEL)
    yield
    # Shutdown
    await engine.dispose()


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        lifespan=lifespan
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Prometheus metrics
    Instrumentator().instrument(app).expose(app)
    
    # Include routers
    app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)
    
    # Health check
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": settings.PROJECT_NAME}
    
    return app
```

### 4. app/config.py

```python
"""
Application configuration using Pydantic settings.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # Project info
    PROJECT_NAME: str = "My Service"
    DESCRIPTION: str = "Independent microservice"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

### 5. Dockerfile

```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

FROM python:3.11-slim as runtime

ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN useradd -m -u 1000 appuser

WORKDIR /app
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --chown=appuser:appuser . .

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
```

### 6. .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.venv/
venv/
ENV/

# Poetry
poetry.lock

# Environment
.env
.env.local

# Database
*.db
*.sqlite

# Logs
*.log
logs/

# Coverage
htmlcov/
.coverage
.pytest_cache/

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

### 7. .env.example

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/my_service_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Application
PROJECT_NAME=My Service
LOG_LEVEL=INFO
ENVIRONMENT=development

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

---

## 🧪 چک‌لیست تکمیل سرویس

### ✅ Structure
- [ ] ساختار فولدرها ایجاد شده
- [ ] Git repository مقداردهی شده
- [ ] Virtual environment ایجاد شده
- [ ] Dependencies نصب شده

### ✅ Configuration
- [ ] pyproject.toml با تمام dependencies
- [ ] docker-compose.yml برای PostgreSQL & Redis
- [ ] Dockerfile برای containerization
- [ ] .env.example برای environment variables
- [ ] alembic.ini برای migrations

### ✅ Core Files
- [ ] app/main.py با FastAPI factory
- [ ] app/config.py با Pydantic settings
- [ ] app/core/database.py
- [ ] app/core/redis_client.py

### ✅ Business Logic
- [ ] Models (SQLAlchemy)
- [ ] Schemas (Pydantic)
- [ ] Services (business logic)
- [ ] API endpoints

### ✅ Database
- [ ] Alembic setup
- [ ] Initial migration
- [ ] Database models

### ✅ Testing
- [ ] tests/conftest.py با fixtures
- [ ] Integration tests
- [ ] Unit tests
- [ ] Coverage > 80%

### ✅ DevOps
- [ ] GitHub Actions CI/CD
- [ ] Docker build تست شده
- [ ] Health check endpoint
- [ ] Prometheus metrics

### ✅ Documentation
- [ ] README.md کامل
- [ ] API documentation (OpenAPI)
- [ ] DEPLOYMENT.md
- [ ] Code comments و docstrings

### ✅ Independence Verification
- [ ] سرویس بدون dependency دیگر اجرا می‌شود
- [ ] Database اختصاصی دارد
- [ ] Docker Compose مستقل دارد
- [ ] Git repository مجزا دارد
- [ ] می‌تواند در پروژه‌های دیگر استفاده شود

---

## 🚀 Quick Start Script

```bash
#!/bin/bash
# create-new-service.sh

SERVICE_NAME=$1

if [ -z "$SERVICE_NAME" ]; then
    echo "Usage: ./create-new-service.sh <service-name>"
    exit 1
fi

echo "🚀 Creating new service: $SERVICE_NAME"

# ایجاد directory
mkdir $SERVICE_NAME
cd $SERVICE_NAME

# Git init
git init

# Virtual environment
python -m venv .venv
source .venv/bin/activate

# ساختار directories
mkdir -p app/{api/v1,core,models,schemas,services}
mkdir -p tests alembic/versions scripts kubernetes

# ایجاد __init__.py files
find app tests scripts -type d -exec touch {}/__init__.py \;

# نصب Poetry و dependencies
pip install poetry
poetry init -n
poetry add fastapi uvicorn sqlalchemy asyncpg alembic redis pydantic-settings

echo "✅ Service $SERVICE_NAME created successfully!"
echo "📝 Next steps:"
echo "  1. Configure pyproject.toml"
echo "  2. Create docker-compose.yml"
echo "  3. Implement business logic"
echo "  4. Write tests"
echo "  5. Push to Git"
```

---

## 📚 مستندات بیشتر

- [INDEPENDENT_ARCHITECTURE.md](INDEPENDENT_ARCHITECTURE.md) - معماری کلی
- [TEAM_PROMPT.md](TEAM_PROMPT.md) - استانداردهای تیم
- Auth Service - مثال کامل پیاده‌سازی

---

**این template تضمین می‌کند هر سرویس جدید کاملاً مستقل و قابل استفاده مجدد باشد! 🎯**
