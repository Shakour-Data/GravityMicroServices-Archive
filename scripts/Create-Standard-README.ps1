#Requires -Version 7.0

<#
.SYNOPSIS
    Create standardized README.md files for all Gravity MicroServices
.DESCRIPTION
    Generates comprehensive README.md documentation for each service including:
    - Service description and features
    - Prerequisites and installation instructions
    - Environment configuration
    - Running the service (standalone and Docker)
    - API documentation
    - Testing instructions
    - Contributing guidelines
.PARAMETER StartFrom
    Service number to start from (default: 4)
.PARAMETER EndAt
    Service number to end at (default: 52)
.PARAMETER DryRun
    If specified, only shows what would be done without creating files
.EXAMPLE
    .\Create-Standard-README.ps1
    .\Create-Standard-README.ps1 -StartFrom 4 -EndAt 10
    .\Create-Standard-README.ps1 -DryRun
#>

[CmdletBinding()]
param(
    [Parameter()]
    [int]$StartFrom = 4,
    
    [Parameter()]
    [int]$EndAt = 52,
    
    [Parameter()]
    [switch]$DryRun
)

# Service metadata
$services = @{
    4  = @{ Name = "config-service"; Port = 8004; Description = "Configuration Management Service"; Features = "Centralized configuration management, environment-based configs, dynamic configuration updates, configuration versioning" }
    5  = @{ Name = "auth-service"; Port = 8005; Description = "Authentication & Authorization Service"; Features = "OAuth2 authentication, JWT tokens, role-based access control (RBAC), refresh tokens, password hashing" }
    6  = @{ Name = "user-service"; Port = 8006; Description = "User Management Service"; Features = "User profiles, user registration, profile management, user preferences, avatar management" }
    7  = @{ Name = "notification-service"; Port = 8007; Description = "Notification Service"; Features = "Multi-channel notifications (Email, SMS, Push), notification templates, delivery tracking, notification preferences" }
    8  = @{ Name = "email-service"; Port = 8008; Description = "Email Service"; Features = "Email sending (SMTP/SendGrid), email templates, attachment support, email tracking, bounce handling" }
    9  = @{ Name = "sms-service"; Port = 8009; Description = "SMS Service"; Features = "SMS sending, SMS templates, delivery reports, multi-provider support, rate limiting" }
    10 = @{ Name = "file-storage-service"; Port = 8010; Description = "File Storage Service"; Features = "File upload/download, S3 storage, file versioning, access control, metadata management" }
    11 = @{ Name = "permission-service"; Port = 8011; Description = "Permission Management Service"; Features = "Permission definitions, role management, permission assignment, access control, permission inheritance" }
    12 = @{ Name = "session-service"; Port = 8012; Description = "Session Management Service"; Features = "Session creation, session validation, session expiry, multi-device sessions, session revocation" }
    13 = @{ Name = "audit-log-service"; Port = 8013; Description = "Audit Logging Service"; Features = "Activity logging, audit trails, compliance tracking, log retention, searchable logs" }
    14 = @{ Name = "cache-service"; Port = 8014; Description = "Distributed Cache Service"; Features = "Redis caching, cache invalidation, cache warming, TTL management, cache statistics" }
    15 = @{ Name = "payment-service"; Port = 8015; Description = "Payment Processing Service"; Features = "Payment gateway integration, payment processing, refunds, payment history, multi-currency support" }
    16 = @{ Name = "order-service"; Port = 8016; Description = "Order Management Service"; Features = "Order creation, order tracking, order status management, order history, cancellation handling" }
    17 = @{ Name = "product-service"; Port = 8017; Description = "Product Catalog Service"; Features = "Product management, categories, attributes, pricing, inventory tracking, product search" }
    18 = @{ Name = "cart-service"; Port = 8018; Description = "Shopping Cart Service"; Features = "Cart management, add/remove items, cart persistence, cart calculations, abandoned cart handling" }
    19 = @{ Name = "search-service"; Port = 8019; Description = "Search Service"; Features = "Elasticsearch integration, full-text search, faceted search, search suggestions, relevance ranking" }
    20 = @{ Name = "recommendation-service"; Port = 8020; Description = "Recommendation Engine Service"; Features = "ML-based recommendations, collaborative filtering, content-based filtering, personalization, A/B testing" }
    21 = @{ Name = "review-service"; Port = 8021; Description = "Review & Rating Service"; Features = "Product reviews, ratings, review moderation, helpful votes, review replies, verified purchases" }
    22 = @{ Name = "wishlist-service"; Port = 8022; Description = "Wishlist Service"; Features = "Wishlist management, add/remove items, share wishlists, price alerts, stock notifications" }
    23 = @{ Name = "analytics-service"; Port = 8023; Description = "Analytics Service"; Features = "User analytics, event tracking, funnel analysis, cohort analysis, custom reports, real-time dashboards" }
    24 = @{ Name = "reporting-service"; Port = 8024; Description = "Reporting Service"; Features = "Report generation, PDF/Excel exports, scheduled reports, custom reports, report templates" }
    25 = @{ Name = "inventory-service"; Port = 8025; Description = "Inventory Management Service"; Features = "Stock management, inventory tracking, low stock alerts, batch operations, inventory history" }
    26 = @{ Name = "shipping-service"; Port = 8026; Description = "Shipping Service"; Features = "Shipping calculation, carrier integration, tracking, delivery estimates, shipping labels" }
    27 = @{ Name = "invoice-service"; Port = 8027; Description = "Invoice Management Service"; Features = "Invoice generation, invoice templates, payment tracking, invoice history, PDF export" }
    28 = @{ Name = "chat-service"; Port = 8028; Description = "Real-time Chat Service"; Features = "WebSocket chat, message history, typing indicators, read receipts, file sharing, chat rooms" }
    29 = @{ Name = "video-call-service"; Port = 8029; Description = "Video Call Service"; Features = "WebRTC video calls, screen sharing, call recording, call history, multi-party calls" }
    30 = @{ Name = "geolocation-service"; Port = 8030; Description = "Geolocation Service"; Features = "Location tracking, geocoding, reverse geocoding, distance calculation, location-based search" }
    31 = @{ Name = "subscription-service"; Port = 8031; Description = "Subscription Management Service"; Features = "Subscription plans, recurring billing, trial periods, plan upgrades/downgrades, cancellation" }
    32 = @{ Name = "loyalty-service"; Port = 8032; Description = "Loyalty Program Service"; Features = "Points management, reward tiers, point redemption, loyalty history, bonus campaigns" }
    33 = @{ Name = "coupon-service"; Port = 8033; Description = "Coupon Management Service"; Features = "Coupon creation, validation, usage tracking, expiry management, discount rules" }
    34 = @{ Name = "referral-service"; Port = 8034; Description = "Referral Program Service"; Features = "Referral tracking, referral rewards, referral codes, conversion tracking, referral analytics" }
    35 = @{ Name = "translation-service"; Port = 8035; Description = "Translation & i18n Service"; Features = "Multi-language support, translation management, locale handling, fallback languages, translation caching" }
    36 = @{ Name = "cms-service"; Port = 8036; Description = "Content Management Service"; Features = "Content creation, versioning, publishing workflow, media library, SEO optimization" }
    37 = @{ Name = "feedback-service"; Port = 8037; Description = "Feedback Collection Service"; Features = "Feedback forms, sentiment analysis, feedback categorization, feedback analytics, response management" }
    38 = @{ Name = "monitoring-service"; Port = 8038; Description = "Monitoring Service"; Features = "Service health checks, performance monitoring, uptime tracking, alerting, metric collection" }
    39 = @{ Name = "logging-service"; Port = 8039; Description = "Centralized Logging Service"; Features = "Log aggregation, log search, log retention, structured logging, log visualization" }
    40 = @{ Name = "scheduler-service"; Port = 8040; Description = "Job Scheduling Service"; Features = "Cron jobs, scheduled tasks, job history, job retry, job monitoring, distributed scheduling" }
    41 = @{ Name = "webhook-service"; Port = 8041; Description = "Webhook Management Service"; Features = "Webhook registration, event delivery, retry logic, webhook verification, delivery logs" }
    42 = @{ Name = "export-service"; Port = 8042; Description = "Data Export Service"; Features = "Export to CSV/Excel/JSON, scheduled exports, large dataset handling, export templates" }
    43 = @{ Name = "import-service"; Port = 8043; Description = "Data Import Service"; Features = "Import from CSV/Excel/JSON, data validation, batch processing, import history, error handling" }
    44 = @{ Name = "backup-service"; Port = 8044; Description = "Backup Service"; Features = "Automated backups, backup scheduling, backup retention, restore functionality, backup verification" }
    45 = @{ Name = "rate-limiter-service"; Port = 8045; Description = "Rate Limiting Service"; Features = "API rate limiting, throttling, quota management, rate limit rules, bypass rules" }
    46 = @{ Name = "ab-testing-service"; Port = 8046; Description = "A/B Testing Service"; Features = "Experiment creation, variant management, traffic splitting, result tracking, statistical analysis" }
    47 = @{ Name = "feature-flag-service"; Port = 8047; Description = "Feature Flag Service"; Features = "Feature toggles, gradual rollouts, targeting rules, flag history, flag analytics" }
    48 = @{ Name = "tax-service"; Port = 8048; Description = "Tax Calculation Service"; Features = "Tax calculation, multi-region support, tax rules, tax reporting, tax rate updates" }
    49 = @{ Name = "fraud-detection-service"; Port = 8049; Description = "Fraud Detection Service"; Features = "Transaction monitoring, risk scoring, rule-based detection, ML-based detection, fraud alerts" }
    50 = @{ Name = "kyc-service"; Port = 8050; Description = "KYC (Know Your Customer) Service"; Features = "Identity verification, document upload, verification workflow, compliance checks, audit trail" }
    51 = @{ Name = "gamification-service"; Port = 8051; Description = "Gamification Service"; Features = "Achievement system, badges, leaderboards, challenges, progress tracking, reward system" }
    52 = @{ Name = "social-media-service"; Port = 8052; Description = "Social Media Integration Service"; Features = "Social login, social sharing, post integration, profile sync, social analytics" }
}

function New-ReadmeContent {
    param(
        [string]$ServiceName,
        [int]$Port,
        [string]$Description,
        [string]$Features
    )
    
    $featureList = $Features -split ", " | ForEach-Object { "- $_" }
    $featureString = $featureList -join "`n"
    
    $displayName = ($ServiceName -split "-" | ForEach-Object { (Get-Culture).TextInfo.ToTitleCase($_) }) -join " "
    $pythonPackageName = $ServiceName -replace "-", "_"
    
    return @"
# $displayName

$Description for the Gravity MicroServices Platform.

[![CI/CD](https://github.com/Shakour-Data/$ServiceName/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakour-Data/$ServiceName/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## 📋 Overview

This microservice is part of the Gravity MicroServices Platform, a comprehensive collection of independent, reusable microservices designed for enterprise applications.

**Key Features:**
$featureString

## 🎯 Service Independence

This service follows the **5 Golden Principles** of microservices:
- ✅ **One Repository = One Service** - Independent Git repository
- ✅ **One Service = One Database** - Dedicated PostgreSQL database
- ✅ **Communication via API Only** - REST API communication
- ✅ **Infrastructure as Code** - Complete Docker setup
- ✅ **Independent Deployment** - Can be deployed standalone

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- Poetry (for dependency management)

### Installation

1. **Clone the repository:**
``````bash
git clone https://github.com/Shakour-Data/$ServiceName.git
cd $ServiceName
``````

2. **Install dependencies:**
``````bash
poetry install
``````

3. **Create environment file:**
``````bash
cp .env.example .env
# Edit .env with your configuration
``````

4. **Start the service:**
``````bash
poetry run python -m app.main
``````

The service will be available at `http://localhost:$Port`

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

``````bash
# Start service with all dependencies
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
``````

### Using Docker Only

``````bash
# Build image
docker build -t $ServiceName:latest .

# Run container
docker run -d \\
  --name $ServiceName \\
  -p ${Port}:${Port} \\
  --env-file .env \\
  $ServiceName:latest
``````

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

``````bash
# Service Configuration
SERVICE_NAME=$ServiceName
SERVICE_PORT=$Port
ENVIRONMENT=development

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/${pythonPackageName}_db

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# API Configuration
API_V1_PREFIX=/api/v1
CORS_ORIGINS=["http://localhost:3000"]

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging
LOG_LEVEL=INFO
``````

### Database Setup

The service uses PostgreSQL with automatic migrations:

``````bash
# Run migrations
poetry run alembic upgrade head

# Create new migration
poetry run alembic revision --autogenerate -m "Description"
``````

## 📚 API Documentation

Once the service is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:$Port/docs
- **ReDoc**: http://localhost:$Port/redoc
- **OpenAPI JSON**: http://localhost:$Port/openapi.json

### Main Endpoints

``````
GET    /health              - Health check endpoint
GET    /api/v1/...          - Service-specific endpoints
POST   /api/v1/...          - Create operations
PUT    /api/v1/...          - Update operations
DELETE /api/v1/...          - Delete operations
``````

## 🧪 Testing

### Run All Tests

``````bash
poetry run pytest tests/ -v
``````

### Run with Coverage

``````bash
poetry run pytest tests/ -v --cov=app --cov-report=html
``````

### Run Specific Test Files

``````bash
poetry run pytest tests/test_main.py -v
``````

### Test Coverage Requirements

- Minimum coverage: **95%**
- All tests must pass before deployment
- Integration tests included

## 🔧 Development

### Project Structure

``````
$ServiceName/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── api/
│   │   └── v1/              # API endpoints
│   ├── core/
│   │   ├── database.py      # Database connection
│   │   ├── redis_client.py  # Redis client
│   │   └── security.py      # Security utilities
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic
├── tests/
│   ├── conftest.py          # Test fixtures
│   └── test_*.py            # Test files
├── alembic/                 # Database migrations
├── docker-compose.yml       # Local infrastructure
├── Dockerfile               # Container image
├── pyproject.toml           # Dependencies
└── README.md                # This file
``````

### Code Quality Standards

``````bash
# Format code
poetry run black app/ tests/
poetry run isort app/ tests/

# Type checking
poetry run mypy app/

# Linting
poetry run ruff check app/ tests/

# Security scanning
poetry run bandit -r app/
poetry run safety check
``````

## 🔐 Security

- **Authentication**: OAuth2 with JWT tokens
- **Authorization**: Role-Based Access Control (RBAC)
- **Data Encryption**: TLS 1.3 for transport
- **Secret Management**: Environment variables (never hardcoded)
- **Input Validation**: Pydantic models
- **SQL Injection Prevention**: Parametrized queries
- **Rate Limiting**: Built-in rate limiting support

## 📊 Monitoring

### Health Check

``````bash
curl http://localhost:$Port/health
``````

Response:
``````json
{
  "status": "healthy",
  "service": "$ServiceName",
  "version": "1.0.0",
  "timestamp": "2025-11-12T10:00:00Z"
}
``````

### Metrics

Prometheus metrics available at:
``````
GET /metrics
``````

## 🚀 Deployment

### Production Deployment

1. **Set environment variables:**
``````bash
export ENVIRONMENT=production
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=your-production-database-url
``````

2. **Run migrations:**
``````bash
poetry run alembic upgrade head
``````

3. **Start with production settings:**
``````bash
poetry run gunicorn app.main:app \\
  --workers 4 \\
  --worker-class uvicorn.workers.UvicornWorker \\
  --bind 0.0.0.0:$Port
``````

### Kubernetes Deployment

Kubernetes manifests are available in the `k8s/` directory:

``````bash
kubectl apply -f k8s/
``````

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

``````
feat: add new feature
fix: resolve bug
refactor: restructure code
docs: update documentation
test: add tests
chore: update dependencies
``````

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Services

Part of the Gravity MicroServices Platform:
- [API Gateway](https://github.com/Shakour-Data/api-gateway)
- [Service Discovery](https://github.com/Shakour-Data/service-discovery)
- [Common Library](https://github.com/Shakour-Data/common-library)

## 📧 Support

For support, please open an issue on GitHub or contact the development team.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Poetry](https://python-poetry.org/) - Dependency management
- [Docker](https://www.docker.com/) - Containerization

---

**Made with ❤️ by the Gravity MicroServices Team**
"@
}

# Main script execution
Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  README.md Generation for Gravity MicroServices" -ForegroundColor Cyan
Write-Host "  Range: Service $StartFrom to $EndAt" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

$updated = 0
$skipped = 0
$errors = 0

for ($i = $StartFrom; $i -le $EndAt; $i++) {
    if (-not $services.ContainsKey($i)) {
        Write-Host "[$i/$EndAt] Service $i not found in metadata - Skipping" -ForegroundColor Yellow
        $skipped++
        continue
    }
    
    $service = $services[$i]
    $serviceName = $service.Name
    $serviceNumber = $i.ToString("D2")
    $serviceDir = "$serviceNumber-$serviceName"
    $servicePath = Join-Path $PSScriptRoot ".." $serviceDir
    $readmePath = Join-Path $servicePath "README.md"
    
    Write-Host "[$i/$EndAt] $serviceDir " -NoNewline
    
    if (-not (Test-Path $servicePath)) {
        Write-Host "❌ Service directory not found" -ForegroundColor Red
        $errors++
        continue
    }
    
    if ($DryRun) {
        Write-Host "🔍 Would create README.md" -ForegroundColor Yellow
        $updated++
        continue
    }
    
    try {
        $readmeContent = New-ReadmeContent `
            -ServiceName $serviceName `
            -Port $service.Port `
            -Description $service.Description `
            -Features $service.Features
        
        $readmeContent | Out-File -FilePath $readmePath -Encoding UTF8
        Write-Host "✅ README.md created" -ForegroundColor Green
        $updated++
    }
    catch {
        Write-Host "❌ Error: $_" -ForegroundColor Red
        $errors++
    }
}

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Created: $updated" -ForegroundColor Green
Write-Host "  Skipped: $skipped" -ForegroundColor Yellow
Write-Host "  Errors:  $errors" -ForegroundColor $(if ($errors -gt 0) { "Red" } else { "Green" })

if ($DryRun) {
    Write-Host "`nℹ️  This was a DRY RUN. Use without -DryRun to create files." -ForegroundColor Yellow
}

Write-Host "================================================================`n" -ForegroundColor Cyan
