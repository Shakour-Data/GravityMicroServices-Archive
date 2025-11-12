#!/usr/bin/env pwsh
param([int]$Start = 1)

$services = 1..52 | ForEach-Object { "{0:D2}-{1}" -f $_, @(
        "common-library", "service-discovery", "api-gateway", "config-service",
        "auth-service", "user-service", "notification-service", "email-service",
        "sms-service", "file-storage-service", "permission-service", "session-service",
        "audit-log-service", "cache-service", "payment-service", "order-service",
        "product-service", "cart-service", "search-service", "recommendation-service",
        "review-service", "wishlist-service", "analytics-service", "reporting-service",
        "inventory-service", "shipping-service", "invoice-service", "chat-service",
        "video-call-service", "geolocation-service", "subscription-service", "loyalty-service",
        "coupon-service", "referral-service", "translation-service", "cms-service",
        "feedback-service", "monitoring-service", "logging-service", "scheduler-service",
        "webhook-service", "export-service", "import-service", "backup-service",
        "rate-limiter-service", "ab-testing-service", "feature-flag-service", "tax-service",
        "fraud-detection-service", "kyc-service", "gamification-service", "social-media-service"
    )[$_ - 1] }

$ci = @'
name: CI
on: [push, pull_request]
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
        ports: [5432:5432]
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports: [6379:6379]
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with: { python-version: '3.12' }
    - run: |
        python -m pip install --upgrade pip
        if [ -f pyproject.toml ]; then pip install -e .[dev]; fi
    - run: pytest tests/ -v --cov --cov-report=xml
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379
    - uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
        token: ${{ secrets.CODECOV_TOKEN }}
'@

$cd = @'
name: CD
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: docker/setup-buildx-action@v3
    - uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    - uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
          ${{ secrets.DOCKER_USERNAME }}/${{ github.event.repository.name }}:${{ github.sha }}
'@

Write-Host "`n🚀 WORKFLOW DEPLOYMENT - Starting from #$Start" -ForegroundColor Cyan
$ok = 0; $fail = 0

foreach ($svc in $services[($Start - 1)..51]) {
    Write-Host "`n  Processing $svc..." -ForegroundColor Cyan
    try {
        # Skip if has workflows
        $check = gh api "repos/Shakour-Data/$svc/contents/.github/workflows" -silent 2>&1
        if ($check -match '"name"') {
            Write-Host "  ✓ $svc (skip - already has workflows)" -ForegroundColor Gray
            $ok++; continue
        }
    }
    catch {}
    
    try {
        $tmp = Join-Path $env:TEMP "wf$(Get-Random)"
        gh repo clone "Shakour-Data/$svc" $tmp 2>&1 | Out-Null
        
        $wfDir = Join-Path $tmp ".github\workflows"
        New-Item -Path $wfDir -ItemType Directory -Force | Out-Null
        $ci | Out-File -FilePath "$wfDir\ci.yml" -Encoding UTF8
        $cd | Out-File -FilePath "$wfDir\cd.yml" -Encoding UTF8
        
        Push-Location $tmp
        git add .github 2>&1 | Out-Null
        git commit -m "ci: add workflows" 2>&1 | Out-Null
        $pushOutput = git push origin main 2>&1 | Out-String
        $pushOK = ($pushOutput -notmatch "fatal|error") -and ($pushOutput -match "main -> main")
        Pop-Location
        
        Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
        
        if ($pushOK) {
            Write-Host "  ✅ $svc" -ForegroundColor Green
            $ok++
        }
        else {
            Write-Host "  ⚠️ $svc (push failed)" -ForegroundColor Yellow
            $fail++
        }
    }
    catch {
        Write-Host "  ❌ $svc : $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "     Stack: $($_.ScriptStackTrace)" -ForegroundColor DarkGray
        $fail++
    }
}

Write-Host "`n📊 Results: ✅ $ok | ❌ $fail`n" -ForegroundColor $(if ($fail -eq 0) { 'Green' }else { 'Yellow' })
