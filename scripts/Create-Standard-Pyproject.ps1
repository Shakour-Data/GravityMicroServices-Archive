# ============================================================================
# Script: Create-Standard-Pyproject.ps1
# Purpose: Generate standardized pyproject.toml files for all microservices
# Author: Gravity Elite Team
# Date: 2024
# ============================================================================

param(
    [int]$StartFrom = 1,
    [int]$EndAt = 52
)

$ErrorActionPreference = "Stop"

# Service metadata
$services = @{
    "04-config-service" = @{
        name = "config-service"
        description = "Centralized Configuration Management Service - Manage application configs across all services"
        app_port = 8004
    }
    "05-auth-service" = @{
        name = "auth-service"
        description = "Independent Authentication & Authorization Microservice - Reusable across unlimited projects"
        app_port = 8005
    }
    "06-user-service" = @{
        name = "user-service"
        description = "User Profile & Management Service - Handle user data, profiles, and preferences"
        app_port = 8006
    }
    "07-notification-service" = @{
        name = "notification-service"
        description = "Multi-Channel Notification Service - Email, SMS, Push notifications orchestration"
        app_port = 8007
    }
    "08-email-service" = @{
        name = "email-service"
        description = "Email Delivery Service - SMTP/SendGrid integration for email dispatch"
        app_port = 8008
    }
    "09-sms-service" = @{
        name = "sms-service"
        description = "SMS Delivery Service - Twilio/AWS SNS integration for SMS dispatch"
        app_port = 8009
    }
    "10-file-storage-service" = @{
        name = "file-storage-service"
        description = "File Storage & Management Service - S3/MinIO integration for file handling"
        app_port = 8010
    }
    "11-permission-service" = @{
        name = "permission-service"
        description = "RBAC Permissions Service - Role-based access control and permissions"
        app_port = 8011
    }
    "12-session-service" = @{
        name = "session-service"
        description = "User Session Management Service - Handle active sessions and tokens"
        app_port = 8012
    }
    "13-audit-log-service" = @{
        name = "audit-log-service"
        description = "Audit & Activity Logging Service - Track all system activities"
        app_port = 8013
    }
    "14-cache-service" = @{
        name = "cache-service"
        description = "Distributed Cache Service - Redis-based caching layer"
        app_port = 8014
    }
    "15-payment-service" = @{
        name = "payment-service"
        description = "Payment Processing Service - Stripe/PayPal integration"
        app_port = 8015
    }
    "16-order-service" = @{
        name = "order-service"
        description = "Order Management Service - Handle orders lifecycle"
        app_port = 8016
    }
    "17-product-service" = @{
        name = "product-service"
        description = "Product Catalog Service - Manage products and inventory"
        app_port = 8017
    }
    "18-cart-service" = @{
        name = "cart-service"
        description = "Shopping Cart Service - Handle shopping cart operations"
        app_port = 8018
    }
    "19-search-service" = @{
        name = "search-service"
        description = "Search & Indexing Service - Elasticsearch integration"
        app_port = 8019
    }
    "20-recommendation-service" = @{
        name = "recommendation-service"
        description = "AI Recommendation Engine - ML-based product recommendations"
        app_port = 8020
    }
    "21-review-service" = @{
        name = "review-service"
        description = "Product Review & Rating Service - Handle user reviews"
        app_port = 8021
    }
    "22-wishlist-service" = @{
        name = "wishlist-service"
        description = "Wishlist Management Service - User wishlists and favorites"
        app_port = 8022
    }
    "23-analytics-service" = @{
        name = "analytics-service"
        description = "Analytics & Metrics Service - Business intelligence and metrics"
        app_port = 8023
    }
    "24-reporting-service" = @{
        name = "reporting-service"
        description = "Report Generation Service - Generate business reports"
        app_port = 8024
    }
    "25-inventory-service" = @{
        name = "inventory-service"
        description = "Inventory Management Service - Stock tracking and management"
        app_port = 8025
    }
    "26-shipping-service" = @{
        name = "shipping-service"
        description = "Shipping & Logistics Service - Handle shipping operations"
        app_port = 8026
    }
    "27-invoice-service" = @{
        name = "invoice-service"
        description = "Invoice Generation Service - Create and manage invoices"
        app_port = 8027
    }
    "28-chat-service" = @{
        name = "chat-service"
        description = "Real-time Chat Service - WebSocket-based messaging"
        app_port = 8028
    }
    "29-video-call-service" = @{
        name = "video-call-service"
        description = "Video Call Service - WebRTC integration"
        app_port = 8029
    }
    "30-geolocation-service" = @{
        name = "geolocation-service"
        description = "Geolocation Service - Location-based features"
        app_port = 8030
    }
    "31-subscription-service" = @{
        name = "subscription-service"
        description = "Subscription Management Service - Handle subscriptions"
        app_port = 8031
    }
    "32-loyalty-service" = @{
        name = "loyalty-service"
        description = "Loyalty Program Service - Points and rewards"
        app_port = 8032
    }
    "33-coupon-service" = @{
        name = "coupon-service"
        description = "Coupon & Discount Service - Manage promotional codes"
        app_port = 8033
    }
    "34-referral-service" = @{
        name = "referral-service"
        description = "Referral Program Service - Referral tracking and rewards"
        app_port = 8034
    }
    "35-translation-service" = @{
        name = "translation-service"
        description = "i18n Translation Service - Multi-language support"
        app_port = 8035
    }
    "36-cms-service" = @{
        name = "cms-service"
        description = "Content Management Service - Manage content and pages"
        app_port = 8036
    }
    "37-feedback-service" = @{
        name = "feedback-service"
        description = "Feedback & Survey Service - Collect user feedback"
        app_port = 8037
    }
    "38-monitoring-service" = @{
        name = "monitoring-service"
        description = "System Monitoring Service - Prometheus/Grafana integration"
        app_port = 8038
    }
    "39-logging-service" = @{
        name = "logging-service"
        description = "Centralized Logging Service - ELK stack integration"
        app_port = 8039
    }
    "40-scheduler-service" = @{
        name = "scheduler-service"
        description = "Task Scheduler Service - Celery/APScheduler integration"
        app_port = 8040
    }
    "41-webhook-service" = @{
        name = "webhook-service"
        description = "Webhook Management Service - Handle webhooks"
        app_port = 8041
    }
    "42-export-service" = @{
        name = "export-service"
        description = "Data Export Service - Export data to various formats"
        app_port = 8042
    }
    "43-import-service" = @{
        name = "import-service"
        description = "Data Import Service - Import data from various sources"
        app_port = 8043
    }
    "44-backup-service" = @{
        name = "backup-service"
        description = "Backup & Restore Service - Database backup automation"
        app_port = 8044
    }
    "45-rate-limiter-service" = @{
        name = "rate-limiter-service"
        description = "Rate Limiting Service - API rate limiting"
        app_port = 8045
    }
    "46-ab-testing-service" = @{
        name = "ab-testing-service"
        description = "A/B Testing Service - Feature experimentation"
        app_port = 8046
    }
    "47-feature-flag-service" = @{
        name = "feature-flag-service"
        description = "Feature Flag Service - Toggle features dynamically"
        app_port = 8047
    }
    "48-tax-service" = @{
        name = "tax-service"
        description = "Tax Calculation Service - Handle tax calculations"
        app_port = 8048
    }
    "49-fraud-detection-service" = @{
        name = "fraud-detection-service"
        description = "Fraud Detection Service - ML-based fraud detection"
        app_port = 8049
    }
    "50-kyc-service" = @{
        name = "kyc-service"
        description = "KYC Verification Service - Identity verification"
        app_port = 8050
    }
    "51-gamification-service" = @{
        name = "gamification-service"
        description = "Gamification Service - Badges, achievements, leaderboards"
        app_port = 8051
    }
    "52-social-media-service" = @{
        name = "social-media-service"
        description = "Social Media Integration Service - Social login and sharing"
        app_port = 8052
    }
}

function Get-PyprojectContent {
    param(
        [string]$ServiceName,
        [string]$Description,
        [int]$AppPort
    )

    return @"
# ============================================================================
# File: pyproject.toml
# Project: Gravity Microservices Platform
# Service: $ServiceName
# Purpose: Poetry dependency management and build configuration
# Author: Gravity Elite Team
# Date: 2024
# License: MIT
# ============================================================================

[tool.poetry]
name = "$ServiceName"
version = "1.0.0"
description = "$Description"
authors = ["Gravity Elite Team <team@gravity.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "~3.12.10"

# Web Framework
fastapi = "^0.104.1"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
pydantic = {extras = ["email"], version = "^2.5.0"}
pydantic-settings = "^2.1.0"

# Database - PostgreSQL
sqlalchemy = {extras = ["asyncio"], version = "^2.0.23"}
asyncpg = "^0.29.0"
alembic = "^1.13.0"

# Security
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
python-multipart = "^0.0.6"
bcrypt = "^4.1.2"

# Redis for caching and sessions
redis = {extras = ["hiredis"], version = "^5.0.1"}

# HTTP Client
httpx = "^0.25.2"

# Utilities
python-dotenv = "^1.0.0"
python-json-logger = "^2.0.7"

# Monitoring & Observability
prometheus-fastapi-instrumentator = "^6.1.0"

# Common library from GitHub
gravity-common = {git = "https://github.com/Shakour-Data/gravity-common.git", tag = "v1.0.2"}

[tool.poetry.group.dev.dependencies]
# Testing
pytest = "^7.4.3"
pytest-asyncio = "^0.23.2"
pytest-cov = "^4.1.0"
pytest-mock = "^3.12.0"

# Code Quality
black = "^23.12.1"
mypy = "^1.7.1"
ruff = "^0.1.9"
isort = "^5.13.2"

# HTTP Client for testing
httpx = "^0.25.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

# ============================================================================
# Testing Configuration
# ============================================================================
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
    "--cov=app",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
    "--cov-fail-under=80"
]
markers = [
    "asyncio: mark test as async",
    "integration: mark test as integration test",
    "unit: mark test as unit test",
    "slow: mark test as slow running"
]

# ============================================================================
# Coverage Configuration
# ============================================================================
[tool.coverage.run]
source = ["app"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/.venv/*",
    "*/migrations/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "def __str__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
    "@abc.abstractmethod"
]

# ============================================================================
# Black Configuration (Code Formatting)
# ============================================================================
[tool.black]
line-length = 100
target-version = ['py312']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
  | migrations
)/
'''

# ============================================================================
# MyPy Configuration (Type Checking)
# ============================================================================
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
strict_equality = true
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

# ============================================================================
# Ruff Configuration (Linting)
# ============================================================================
[tool.ruff]
line-length = 100
target-version = "py312"
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "C",  # flake8-comprehensions
    "B",  # flake8-bugbear
    "UP", # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by black)
    "B008",  # do not perform function calls in argument defaults
    "C901",  # too complex
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # unused imports
"tests/*" = ["S101"]      # use of assert

# ============================================================================
# Isort Configuration (Import Sorting)
# ============================================================================
[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
skip_gitignore = true
known_first_party = ["app", "gravity_common"]
"@
}

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Creating standardized pyproject.toml files" -ForegroundColor Cyan
Write-Host "  Range: Service $StartFrom to $EndAt" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

$created = 0
$skipped = 0
$errors = 0

foreach ($key in $services.Keys | Sort-Object) {
    $number = [int]($key -replace '\D')
    
    if ($number -lt $StartFrom -or $number -gt $EndAt) {
        continue
    }

    $serviceInfo = $services[$key]
    $servicePath = Join-Path $PSScriptRoot "..\$key"
    $tomlPath = Join-Path $servicePath "pyproject.toml"

    Write-Host "[$number/52] $key" -ForegroundColor Yellow -NoNewline
    
    try {
        if (-not (Test-Path $servicePath)) {
            Write-Host " - Service directory not found!" -ForegroundColor Red
            $errors++
            continue
        }

        $content = Get-PyprojectContent `
            -ServiceName $serviceInfo.name `
            -Description $serviceInfo.description `
            -AppPort $serviceInfo.app_port

        # Write the file
        $content | Out-File -FilePath $tomlPath -Encoding UTF8 -NoNewline
        
        Write-Host " ✅ Created" -ForegroundColor Green
        $created++
    }
    catch {
        Write-Host " ❌ Error: $_" -ForegroundColor Red
        $errors++
    }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Created: $created" -ForegroundColor Green
Write-Host "  Skipped: $skipped" -ForegroundColor Yellow
Write-Host "  Errors:  $errors" -ForegroundColor $(if ($errors -gt 0) { "Red" } else { "Green" })
Write-Host "================================================================" -ForegroundColor Cyan
