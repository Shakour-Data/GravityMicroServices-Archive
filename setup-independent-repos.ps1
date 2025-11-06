#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script to convert monorepo to independent microservice repositories

.DESCRIPTION
    این اسکریپت ساختار monorepo فعلی را به repository های مستقل تبدیل می‌کند.
    هر میکروسرویس به یک Git repository جداگانه با تمام dependency ها تبدیل می‌شود.

.EXAMPLE
    .\setup-independent-repos.ps1
#>

param(
    [string]$BasePath = "E:\Shakour\GravityMicroServices",
    [string]$OutputPath = "E:\Shakour\IndependentServices"
)

Write-Host "🚀 Starting Independent Microservices Setup..." -ForegroundColor Green
Write-Host ""

# ایجاد مسیر خروجی
if (-not (Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
    Write-Host "✅ Created output directory: $OutputPath" -ForegroundColor Green
}

# لیست سرویس‌ها
$services = @(
    @{
        Name = "gravity-common"
        Description = "Shared Python package with common utilities"
        Port = "N/A"
        Database = "N/A"
        Type = "library"
    },
    @{
        Name = "auth-service"
        Description = "Authentication & Authorization service"
        Port = "8001"
        Database = "auth_db"
        Type = "service"
    },
    @{
        Name = "api-gateway"
        Description = "API Gateway for routing and load balancing"
        Port = "8000"
        Database = "api_gateway_db"
        Type = "service"
    },
    @{
        Name = "user-service"
        Description = "User management service"
        Port = "8002"
        Database = "user_db"
        Type = "service"
    },
    @{
        Name = "notification-service"
        Description = "Notification service (Email, SMS, Push)"
        Port = "8003"
        Database = "notification_db"
        Type = "service"
    },
    @{
        Name = "file-storage-service"
        Description = "File storage and management service"
        Port = "8004"
        Database = "file_storage_db"
        Type = "service"
    },
    @{
        Name = "payment-service"
        Description = "Payment processing service"
        Port = "8005"
        Database = "payment_db"
        Type = "service"
    }
)

# تابع ایجاد .gitignore
function New-ServiceGitIgnore {
    param([string]$Path)
    
    $gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# Poetry
poetry.lock

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment variables
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
.coverage.*
.pytest_cache/

# Alembic
alembic/__pycache__/
alembic/versions/__pycache__/
"@
    
    Set-Content -Path "$Path\.gitignore" -Value $gitignoreContent
}

# تابع ایجاد README
function New-ServiceReadme {
    param(
        [string]$Path,
        [hashtable]$Service
    )
    
    $readmeContent = @"
# $($Service.Name)

## 📋 Description
$($Service.Description)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Poetry 1.7+
- Docker & Docker Compose

### Installation

``````bash
# 1. Clone repository
git clone https://github.com/gravity/$($Service.Name).git
cd $($Service.Name)

# 2. Create virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# 3. Install dependencies
poetry install

# 4. Start infrastructure
docker-compose up -d

# 5. Run migrations (if applicable)
poetry run alembic upgrade head

# 6. Start service
poetry run uvicorn app.main:create_app --factory --reload --port $($Service.Port)
``````

## 📚 API Documentation
Once running, access:
- Swagger UI: http://localhost:$($Service.Port)/docs
- ReDoc: http://localhost:$($Service.Port)/redoc

## 🧪 Testing

``````bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html
``````

## 🐳 Docker

``````bash
# Build image
docker build -t $($Service.Name):latest .

# Run container
docker-compose up -d
``````

## 📊 Service Information
- **Port:** $($Service.Port)
- **Database:** $($Service.Database)
- **Language:** Python 3.11+
- **Framework:** FastAPI

## 📝 License
MIT License
"@
    
    Set-Content -Path "$Path\README.md" -Value $readmeContent
}

# تابع ایجاد docker-compose.yml برای هر سرویس
function New-ServiceDockerCompose {
    param(
        [string]$Path,
        [hashtable]$Service
    )
    
    if ($Service.Type -eq "library") {
        return  # Library نیاز به docker-compose ندارد
    }
    
    $dbName = $Service.Database
    $serviceName = $Service.Name
    $port = $Service.Port
    
    $dockerComposeContent = @"
version: '3.8'

services:
  postgres:
    image: postgres:16
    container_name: ${serviceName}-postgres
    environment:
      POSTGRES_DB: ${dbName}
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
    networks:
      - ${serviceName}-network

  redis:
    image: redis:7-alpine
    container_name: ${serviceName}-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - ${serviceName}-network

  ${serviceName}:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ${serviceName}
    ports:
      - "${port}:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@postgres:5432/${dbName}
      REDIS_URL: redis://redis:6379/0
      LOG_LEVEL: INFO
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - ${serviceName}-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  ${serviceName}-network:
    driver: bridge
"@
    
    Set-Content -Path "$Path\docker-compose.yml" -Value $dockerComposeContent
}

# تابع ایجاد GitHub Actions workflow
function New-ServiceGitHubActions {
    param([string]$Path)
    
    $workflowPath = "$Path\.github\workflows"
    New-Item -ItemType Directory -Path $workflowPath -Force | Out-Null
    
    $ciContent = @"
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
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
        python-version: '3.11'
    
    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> `$GITHUB_PATH
    
    - name: Install dependencies
      run: |
        poetry install
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379/0
      run: |
        poetry run pytest --cov=app --cov-report=xml --cov-report=term
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  lint:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> `$GITHUB_PATH
    
    - name: Install dependencies
      run: poetry install
    
    - name: Run linting
      run: |
        poetry run black --check app/ tests/
        poetry run mypy app/

  build:
    runs-on: ubuntu-latest
    needs: [test, lint]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Build Docker image
      run: docker build -t service:latest .
"@
    
    Set-Content -Path "$workflowPath\ci.yml" -Value $ciContent
}

# پردازش هر سرویس
foreach ($service in $services) {
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "📦 Processing: $($service.Name)" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    
    $servicePath = Join-Path $OutputPath $service.Name
    
    # ایجاد مسیر سرویس
    if (-not (Test-Path $servicePath)) {
        New-Item -ItemType Directory -Path $servicePath -Force | Out-Null
        Write-Host "  ✅ Created directory: $servicePath" -ForegroundColor Green
    }
    
    # کپی کردن فایل‌های موجود (اگر وجود دارد)
    $sourcePath = Join-Path $BasePath $service.Name
    if (Test-Path $sourcePath) {
        Write-Host "  📁 Copying existing files..." -ForegroundColor Cyan
        Copy-Item -Path "$sourcePath\*" -Destination $servicePath -Recurse -Force
        Write-Host "  ✅ Files copied" -ForegroundColor Green
    }
    
    # ایجاد Git repository
    Push-Location $servicePath
    if (-not (Test-Path ".git")) {
        git init | Out-Null
        Write-Host "  ✅ Initialized Git repository" -ForegroundColor Green
    }
    Pop-Location
    
    # ایجاد .gitignore
    New-ServiceGitIgnore -Path $servicePath
    Write-Host "  ✅ Created .gitignore" -ForegroundColor Green
    
    # ایجاد README
    New-ServiceReadme -Path $servicePath -Service $service
    Write-Host "  ✅ Created README.md" -ForegroundColor Green
    
    # ایجاد docker-compose
    if ($service.Type -eq "service") {
        New-ServiceDockerCompose -Path $servicePath -Service $service
        Write-Host "  ✅ Created docker-compose.yml" -ForegroundColor Green
    }
    
    # ایجاد GitHub Actions
    New-ServiceGitHubActions -Path $servicePath
    Write-Host "  ✅ Created GitHub Actions workflow" -ForegroundColor Green
    
    Write-Host "  🎉 $($service.Name) setup completed!" -ForegroundColor Green
}

# ایجاد Infrastructure Repository
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🏗️  Creating Infrastructure Repository" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$infraPath = Join-Path $OutputPath "gravity-infrastructure"
New-Item -ItemType Directory -Path $infraPath -Force | Out-Null

# کپی docker-compose اصلی
if (Test-Path "$BasePath\docker-compose.yml") {
    Copy-Item -Path "$BasePath\docker-compose.yml" -Destination "$infraPath\docker-compose.full.yml" -Force
    Write-Host "  ✅ Copied full docker-compose.yml" -ForegroundColor Green
}

# ایجاد README برای infrastructure
$infraReadme = @"
# Gravity Infrastructure

این repository شامل تمام پیکربندی‌های زیرساختی برای پلتفرم میکروسرویس‌های Gravity است.

## محتویات

- **docker-compose.full.yml**: Docker Compose با تمام سرویس‌های مشترک
- **kubernetes/**: Kubernetes manifests برای deployment
- **monitoring/**: پیکربندی Prometheus و Grafana
- **logging/**: پیکربندی ELK Stack

## استفاده

### Development (همه سرویس‌ها با Docker Compose)
``````bash
docker-compose -f docker-compose.full.yml up -d
``````

### Production (Kubernetes)
``````bash
kubectl apply -f kubernetes/
``````
"@

Set-Content -Path "$infraPath\README.md" -Value $infraReadme
Write-Host "  ✅ Created Infrastructure README" -ForegroundColor Green

# خلاصه نهایی
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host "🎉 Independent Microservices Setup Completed!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Summary:" -ForegroundColor Cyan
Write-Host "  • Created $($services.Count) independent repositories" -ForegroundColor White
Write-Host "  • Location: $OutputPath" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Review each service in: $OutputPath" -ForegroundColor White
Write-Host "  2. Create remote repositories on GitHub/GitLab" -ForegroundColor White
Write-Host "  3. Push each service:" -ForegroundColor White
Write-Host "     cd $OutputPath\auth-service" -ForegroundColor Gray
Write-Host "     git remote add origin <your-repo-url>" -ForegroundColor Gray
Write-Host "     git add ." -ForegroundColor Gray
Write-Host "     git commit -m 'Initial commit'" -ForegroundColor Gray
Write-Host "     git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "  • See INDEPENDENT_ARCHITECTURE.md for architecture details" -ForegroundColor White
Write-Host ""
