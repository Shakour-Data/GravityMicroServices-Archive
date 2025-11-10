# 🗂️ Gravity MicroServices - Repository Management Guide

## 📋 Overview

This document provides a complete guide for managing the 52+ independent repositories that make up the Gravity MicroServices Platform. Each microservice has its own dedicated Git repository to ensure 100% independence.

**Last Updated:** November 10, 2025  
**GitHub Organization:** `https://github.com/GravityWavesMl`  
**Total Repositories:** 52 services + 1 monorepo = 53 repositories

---

## 🎯 Repository Structure

### Main Monorepo (Orchestration Only)
- **Repository:** `GravityMicroServices`
- **URL:** `https://github.com/GravityWavesMl/GravityMicroServices`
- **Purpose:** Documentation, docker-compose orchestration, shared configs
- **Does NOT contain:** Service implementation code

### Individual Service Repositories
- **Pattern:** `gravity-{service-name}-service`
- **Example:** `https://github.com/GravityWavesMl/gravity-auth-service`
- **Purpose:** Complete independent service with own code, database, CI/CD

---

## 📊 Repository Checklist for Each Service

When creating a new service repository, ensure:

### ✅ Repository Setup
- [ ] Repository created with correct naming: `gravity-{service}-service`
- [ ] README.md with service description
- [ ] LICENSE file (MIT)
- [ ] .gitignore (Python)
- [ ] Branch protection enabled on `main`
- [ ] Required reviewers: minimum 2

### ✅ Code Structure
- [ ] `/app` directory with FastAPI application
- [ ] `/tests` directory with 95%+ coverage
- [ ] `/alembic` for database migrations
- [ ] `pyproject.toml` with Python 3.12.10
- [ ] `.python-version` file set to `3.12.10`
- [ ] `Dockerfile` for containerization
- [ ] `docker-compose.yml` for local development

### ✅ Documentation
- [ ] `README.md` with quick start guide
- [ ] `DEPLOYMENT.md` with deployment instructions
- [ ] `CHANGELOG.md` for version history
- [ ] `CONTRIBUTING.md` with contribution guidelines
- [ ] API documentation (Swagger at `/docs`)

### ✅ CI/CD Pipeline
- [ ] `.github/workflows/ci.yml` for continuous integration
- [ ] `.github/workflows/cd.yml` for continuous deployment
- [ ] Automated tests on PR
- [ ] Code coverage reporting
- [ ] Security scanning (Bandit, Safety)
- [ ] Docker image build and push

### ✅ Configuration
- [ ] `.env.example` with all required variables
- [ ] No hardcoded secrets
- [ ] Environment-based configuration
- [ ] Settings from `pydantic-settings`

### ✅ Database
- [ ] Own dedicated database
- [ ] Alembic migration scripts
- [ ] Initial migration created
- [ ] Seed data (if applicable)

### ✅ Monitoring
- [ ] `/health` endpoint
- [ ] `/metrics` endpoint (Prometheus format)
- [ ] Structured logging
- [ ] Error tracking integration

---

## 🏗️ Repository Creation Scripts

### 1. Create Repository on GitHub

```bash
# Using GitHub CLI (gh)
gh repo create GravityWavesMl/gravity-{service}-service \
  --public \
  --description "Gravity MicroServices - {Service} Service" \
  --homepage "https://gravitywavesml.github.io" \
  --license MIT
```

### 2. Initialize Local Repository

```bash
# Clone the empty repository
git clone https://github.com/GravityWavesMl/gravity-{service}-service.git
cd gravity-{service}-service

# Create basic structure
mkdir -p app/{api/v1,core,models,schemas,services}
mkdir -p tests/{unit,integration}
mkdir -p alembic/versions
mkdir -p .github/workflows
mkdir -p scripts

# Create .python-version
echo "3.12.10" > .python-version

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Environment
.env
.env.local

# Database
*.db
*.sqlite

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db
EOF

# Initial commit
git add .
git commit -m "chore: initialize repository structure"
git push origin main
```

### 3. Set Up Branch Protection

```bash
# Enable branch protection on main
gh api repos/GravityWavesMl/gravity-{service}-service/branches/main/protection \
  -X PUT \
  -f required_status_checks='{"strict":true,"contexts":["test","lint"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":2}' \
  -f restrictions=null
```

---

## 📋 Complete Repository List

### PRIORITY 0: Infrastructure (4 repositories)

| # | Repository | URL | Status | Team |
|---|------------|-----|--------|------|
| 1 | `gravity-common` | [Link](https://github.com/GravityWavesMl/gravity-common) | ✅ Published | Core Infra |
| 2 | `gravity-service-discovery` | [Link](https://github.com/GravityWavesMl/gravity-service-discovery) | 🔄 90% | DevOps |
| 3 | `gravity-api-gateway` | [Link](https://github.com/GravityWavesMl/gravity-api-gateway) | 🔄 95% | Backend Infra |
| 4 | `gravity-config-service` | [Create](https://github.com/new) | ⏳ Pending | DevOps |

### PRIORITY 1: Core Services (10 repositories)

| # | Repository | URL | Status | Team |
|---|------------|-----|--------|------|
| 5 | `gravity-auth-service` | [Link](https://github.com/GravityWavesMl/gravity-auth-service) | ✅ Complete | Security |
| 6 | `gravity-user-service` | [Link](https://github.com/GravityWavesMl/gravity-user-service) | ✅ Complete | Backend A |
| 7 | `gravity-permission-service` | [Create](https://github.com/new) | ⏳ Pending | Security |
| 8 | `gravity-session-service` | [Create](https://github.com/new) | ⏳ Pending | Security |
| 9 | `gravity-notification-service` | [Link](https://github.com/GravityWavesMl/gravity-notification-service) | 🔄 42% | Backend B |
| 10 | `gravity-email-service` | [Create](https://github.com/new) | ⏳ Pending | Backend B |
| 11 | `gravity-sms-service` | [Create](https://github.com/new) | ⏳ Pending | Backend B |
| 12 | `gravity-webhook-service` | [Create](https://github.com/new) | ⏳ Pending | Backend C |
| 13 | `gravity-file-storage-service` | [Create](https://github.com/new) | ⏳ Pending | Backend A |
| 14 | `gravity-media-processing-service` | [Create](https://github.com/new) | ⏳ Pending | Backend A |

### PRIORITY 2: Business Services (13 repositories)

| # | Repository | URL | Status | Team |
|---|------------|-----|--------|------|
| 15 | `gravity-payment-service` | [Create](https://github.com/new) | ⏳ Pending | FinTech |
| 16 | `gravity-order-service` | [Create](https://github.com/new) | ⏳ Pending | Backend C |
| 17 | `gravity-product-catalog-service` | [Create](https://github.com/new) | ⏳ Pending | Backend C |
| 18 | `gravity-inventory-service` | [Create](https://github.com/new) | ⏳ Pending | Backend C |
| 19 | `gravity-pricing-service` | [Create](https://github.com/new) | ⏳ Pending | Backend D |
| 20 | `gravity-cart-service` | [Create](https://github.com/new) | ⏳ Pending | Backend D |
| 21 | `gravity-checkout-service` | [Create](https://github.com/new) | ⏳ Pending | FinTech |
| 22 | `gravity-search-service` | [Create](https://github.com/new) | ⏳ Pending | Search Team |
| 23 | `gravity-analytics-service` | [Create](https://github.com/new) | ⏳ Pending | Data Team |
| 24 | `gravity-recommendation-service` | [Create](https://github.com/new) | ⏳ Pending | ML Team |
| 25 | `gravity-review-service` | [Create](https://github.com/new) | ⏳ Pending | Backend E |
| 26 | `gravity-comment-service` | [Create](https://github.com/new) | ⏳ Pending | Backend E |
| 27 | `gravity-cms-service` | [Create](https://github.com/new) | ⏳ Pending | Backend E |

### PRIORITY 3: Advanced Services (10 repositories)

| # | Repository | URL | Status | Team |
|---|------------|-----|--------|------|
| 28 | `gravity-chat-service` | [Create](https://github.com/new) | ⏳ Pending | Real-time |
| 29 | `gravity-video-call-service` | [Create](https://github.com/new) | ⏳ Pending | Real-time |
| 30 | `gravity-notification-center-service` | [Create](https://github.com/new) | ⏳ Pending | Backend F |
| 31 | `gravity-scheduling-service` | [Create](https://github.com/new) | ⏳ Pending | Backend F |
| 32 | `gravity-geolocation-service` | [Create](https://github.com/new) | ⏳ Pending | Backend G |
| 33 | `gravity-translation-service` | [Create](https://github.com/new) | ⏳ Pending | Backend G |
| 34 | `gravity-export-import-service` | [Create](https://github.com/new) | ⏳ Pending | Backend H |
| 35 | `gravity-reporting-service` | [Create](https://github.com/new) | ⏳ Pending | Backend H |
| 36 | `gravity-backup-service` | [Create](https://github.com/new) | ⏳ Pending | DevOps |
| 37 | `gravity-rate-limiting-service` | [Create](https://github.com/new) | ⏳ Pending | Backend I |

### PRIORITY 4: Monitoring & Specialized (15 repositories)

| # | Repository | URL | Status | Team |
|---|------------|-----|--------|------|
| 38 | `gravity-logging-service` | [Create](https://github.com/new) | ⏳ Pending | DevOps |
| 39 | `gravity-monitoring-service` | [Create](https://github.com/new) | ⏳ Pending | DevOps |
| 40 | `gravity-audit-service` | [Create](https://github.com/new) | ⏳ Pending | Security |
| 41 | `gravity-health-check-service` | [Create](https://github.com/new) | ⏳ Pending | DevOps |
| 42 | `gravity-survey-service` | [Create](https://github.com/new) | ⏳ Pending | Backend J |
| 43 | `gravity-quiz-service` | [Create](https://github.com/new) | ⏳ Pending | Backend J |
| 44 | `gravity-gamification-service` | [Create](https://github.com/new) | ⏳ Pending | Backend K |
| 45 | `gravity-loyalty-service` | [Create](https://github.com/new) | ⏳ Pending | Backend K |
| 46 | `gravity-referral-service` | [Create](https://github.com/new) | ⏳ Pending | Backend L |
| 47 | `gravity-subscription-service` | [Create](https://github.com/new) | ⏳ Pending | FinTech |
| 48 | `gravity-fraud-detection-service` | [Create](https://github.com/new) | ⏳ Pending | ML+Security |
| 49 | `gravity-encryption-service` | [Create](https://github.com/new) | ⏳ Pending | Security |

---

## 🚀 Automation Scripts

### Batch Create All Repositories

```bash
#!/bin/bash
# create_all_repos.sh

# Array of service names (without 'gravity-' prefix and '-service' suffix)
services=(
  "config"
  "permission"
  "session"
  "email"
  "sms"
  "webhook"
  "file-storage"
  "media-processing"
  "payment"
  "order"
  "product-catalog"
  "inventory"
  "pricing"
  "cart"
  "checkout"
  "search"
  "analytics"
  "recommendation"
  "review"
  "comment"
  "cms"
  "chat"
  "video-call"
  "notification-center"
  "scheduling"
  "geolocation"
  "translation"
  "export-import"
  "reporting"
  "backup"
  "rate-limiting"
  "logging"
  "monitoring"
  "audit"
  "health-check"
  "survey"
  "quiz"
  "gamification"
  "loyalty"
  "referral"
  "subscription"
  "fraud-detection"
  "encryption"
)

# Create each repository
for service in "${services[@]}"; do
  repo_name="gravity-${service}-service"
  echo "Creating repository: ${repo_name}"
  
  gh repo create "GravityWavesMl/${repo_name}" \
    --public \
    --description "Gravity MicroServices - ${service^} Service" \
    --homepage "https://gravitywavesml.github.io" \
    --license MIT
  
  echo "✅ Created: ${repo_name}"
  sleep 2  # Rate limiting
done

echo "🎉 All repositories created successfully!"
```

### Initialize Service Template

```bash
#!/bin/bash
# init_service.sh <service-name>

SERVICE_NAME=$1
REPO_NAME="gravity-${SERVICE_NAME}-service"

# Clone repository
git clone "https://github.com/GravityWavesMl/${REPO_NAME}.git"
cd "${REPO_NAME}"

# Create directory structure
mkdir -p app/{api/v1,core,models,schemas,services}
mkdir -p tests/{unit,integration}
mkdir -p alembic/versions
mkdir -p .github/workflows
mkdir -p scripts

# Create .python-version
echo "3.12.10" > .python-version

# Create pyproject.toml
cat > pyproject.toml << EOF
[tool.poetry]
name = "${REPO_NAME}"
version = "0.1.0"
description = "Gravity MicroServices - ${SERVICE_NAME^} Service"
authors = ["Gravity Team <team@gravitywaves.ml>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "~3.12.10"
fastapi = "^0.104.1"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
sqlalchemy = {extras = ["asyncio"], version = "^2.0.23"}
asyncpg = "^0.29.0"
pydantic = "^2.5.0"
pydantic-settings = "^2.1.0"
redis = "^5.0.1"
httpx = "^0.25.2"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.3"
pytest-asyncio = "^0.21.1"
pytest-cov = "^4.1.0"
black = "^23.12.0"
isort = "^5.13.0"
mypy = "^1.7.1"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
EOF

# Create README.md template
cat > README.md << EOF
# ${REPO_NAME}

Gravity MicroServices - ${SERVICE_NAME^} Service

## 🚀 Quick Start

\`\`\`bash
# Install dependencies
poetry install

# Copy environment template
cp .env.example .env

# Run database migrations
poetry run alembic upgrade head

# Start service
poetry run uvicorn app.main:app --reload --port 8XXX
\`\`\`

## 📋 Prerequisites

- Python 3.12.10 (Required)
- PostgreSQL 16+
- Redis 7+

## 🔗 API Documentation

- Swagger UI: http://localhost:8XXX/docs
- ReDoc: http://localhost:8XXX/redoc

## ✅ Testing

\`\`\`bash
poetry run pytest tests/ -v --cov=app
\`\`\`

## 📄 License

MIT License - See LICENSE file
EOF

# Create LICENSE
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 Gravity MicroServices Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Create main.py
cat > app/main.py << 'EOF'
"""
${SERVICE_NAME^} Service - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="${SERVICE_NAME^} Service",
    description="Gravity MicroServices - ${SERVICE_NAME^} Service",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "${SERVICE_NAME}"}

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "${SERVICE_NAME}",
        "version": "0.1.0",
        "docs": "/docs"
    }
EOF

# Create config.py
cat > app/config.py << 'EOF'
"""Configuration settings."""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"

settings = Settings()
EOF

# Create .env.example
cat > .env.example << 'EOF'
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/${SERVICE_NAME}_db
REDIS_URL=redis://localhost:6379/0
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
.Python
venv/
.env
.env.local
*.db
.pytest_cache/
.coverage
htmlcov/
.vscode/
.idea/
*.log
EOF

# Commit initial structure
git add .
git commit -m "chore: initialize service structure"
git push origin main

echo "✅ Service ${REPO_NAME} initialized successfully!"
```

---

## 📊 Repository Management Dashboard

### Status Overview

| Status | Count | Services |
|--------|-------|----------|
| ✅ Complete | 3 | auth, user, common |
| 🔄 In Progress | 3 | api-gateway, service-discovery, notification |
| ⏳ Not Started | 46 | All P2, P3, P4 services |
| **TOTAL** | **52** | **All services** |

---

## 🔄 CI/CD Template

Create `.github/workflows/ci.yml` in each repository:

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12.10'
    
    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH
    
    - name: Install dependencies
      run: poetry install
    
    - name: Run linters
      run: |
        poetry run black --check app tests
        poetry run isort --check app tests
        poetry run mypy app
    
    - name: Run tests
      run: poetry run pytest tests/ -v --cov=app --cov-report=xml
      env:
        DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379/0
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## 🎯 Team Assignment

### Infrastructure Team (4 developers)
- P0-02: Service Discovery
- P0-03: API Gateway
- P0-04: Configuration Service
- P3-09: Backup Service
- P4-01: Logging Service
- P4-02: Monitoring Service
- P4-04: Health Check Service

### Security Team (4 developers)
- P1-01: Auth Service ✅
- P1-03: Permission Service
- P1-04: Session Service
- P4-03: Audit Service
- P4-11: Fraud Detection Service
- P4-12: Encryption Service

### Backend Team A (3 developers)
- P1-02: User Service ✅
- P1-09: File Storage Service
- P1-10: Media Processing Service

### Backend Team B (3 developers)
- P1-05: Notification Service 🔄
- P1-06: Email Service
- P1-07: SMS Service

### Backend Team C (3 developers)
- P1-08: Webhook Service
- P2-02: Order Service
- P2-03: Product Catalog Service
- P2-04: Inventory Service

### FinTech Team (3 developers)
- P2-01: Payment Service
- P2-07: Checkout Service
- P4-10: Subscription Service

### And so on...

---

## 📋 Next Steps

1. **Week 1:**
   - ✅ Review this repository management plan
   - ⏳ Create missing P0 repositories
   - ⏳ Set up CI/CD templates
   - ⏳ Assign teams to services

2. **Week 2:**
   - ⏳ Create P1 repositories (10 services)
   - ⏳ Initialize service templates
   - ⏳ Set up branch protection
   - ⏳ Begin P1 development

3. **Week 3-4:**
   - ⏳ Complete P1 services
   - ⏳ Create P2 repositories (13 services)
   - ⏳ Begin P2 development

4. **Ongoing:**
   - Monitor repository health
   - Review PRs across all services
   - Update documentation
   - Track progress dashboard

---

**Document Owner:** Marcus Chen (Version Control Specialist)  
**Last Updated:** November 10, 2025  
**Next Review:** November 17, 2025  
**Status:** ✅ Ready for Implementation
