<#
.SYNOPSIS
    Add GitHub Actions CI/CD workflows to all service repositories

.DESCRIPTION
    This script adds standardized GitHub Actions workflows for CI/CD to all 52 service repositories.
    
    Workflows included:
    - ci.yml: Run tests, linting, type checking on every push/PR
    - cd.yml: Deploy to production on main branch push
    - dependency-update.yml: Automated dependency updates

.PARAMETER OrgName
    GitHub Organization name (default: Shakour-Data)

.PARAMETER WorkflowType
    Type of workflow to add: CI, CD, Both (default: Both)

.PARAMETER DryRun
    Run in dry-run mode without making actual changes

.EXAMPLE
    .\Add-GitHubActionsWorkflows.ps1
    
.EXAMPLE
    .\Add-GitHubActionsWorkflows.ps1 -DryRun
    
.EXAMPLE
    .\Add-GitHubActionsWorkflows.ps1 -WorkflowType CI
#>

param(
  [string]$Owner = "Shakour-Data",
  [ValidateSet("CI", "CD", "Both")]
  [string]$WorkflowType = "Both",
  [switch]$DryRun
)

# Colors
$ColorInfo = "Cyan"
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"

Write-Host "`n╔════════════════════════════════════════════════════════╗" -ForegroundColor $ColorInfo
Write-Host "║     GITHUB ACTIONS WORKFLOWS SETUP SCRIPT             ║" -ForegroundColor $ColorInfo
Write-Host "╚════════════════════════════════════════════════════════╝`n" -ForegroundColor $ColorInfo

Write-Host "📋 Configuration:" -ForegroundColor $ColorInfo
Write-Host "  Organization   : $Owner" -ForegroundColor White
Write-Host "  Workflow Type  : $WorkflowType" -ForegroundColor White
Write-Host "  Dry Run        : $DryRun" -ForegroundColor White
Write-Host ""

# CI Workflow Template
$ciWorkflow = @'
name: CI Pipeline

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
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .
        pip install pytest pytest-cov pytest-asyncio black isort mypy bandit safety
    
    - name: Run linting
      run: |
        black --check app/ tests/
        isort --check-only app/ tests/
        mypy app/
    
    - name: Run security checks
      run: |
        bandit -r app/ -ll
        safety check --json
    
    - name: Run tests with coverage
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379/0
        SECRET_KEY: test-secret-key-for-ci
      run: |
        pytest tests/ -v --cov=app --cov-report=xml --cov-report=term
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
    
    - name: Check test coverage threshold
      run: |
        coverage report --fail-under=80
'@

# CD Workflow Template
$cdWorkflow = @'
name: CD Pipeline

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
          ${{ secrets.DOCKER_USERNAME }}/${{ github.event.repository.name }}:${{ github.sha }}
        cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/${{ github.event.repository.name }}:buildcache
        cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/${{ github.event.repository.name }}:buildcache,mode=max

    - name: Deploy to production (placeholder)
      run: |
        echo "Deployment steps would go here"
        echo "Examples:"
        echo "  - kubectl apply -f k8s/"
        echo "  - helm upgrade --install service ./helm-chart"
        echo "  - docker-compose pull && docker-compose up -d"
'@

# List of all services
$services = @(
  "01-common-library",
  "02-service-discovery",
  "03-api-gateway",
  "04-config-service",
  "05-auth-service",
  "06-user-service",
  "07-notification-service",
  "08-email-service",
  "09-sms-service",
  "10-file-storage-service",
  "11-permission-service",
  "12-session-service",
  "13-audit-log-service",
  "14-cache-service",
  "15-payment-service",
  "16-order-service",
  "17-product-service",
  "18-cart-service",
  "19-search-service",
  "20-recommendation-service",
  "21-review-service",
  "22-wishlist-service",
  "23-analytics-service",
  "24-reporting-service",
  "25-inventory-service",
  "26-shipping-service",
  "27-invoice-service",
  "28-chat-service",
  "29-video-call-service",
  "30-geolocation-service",
  "31-subscription-service",
  "32-loyalty-service",
  "33-coupon-service",
  "34-referral-service",
  "35-translation-service",
  "36-cms-service",
  "37-feedback-service",
  "38-monitoring-service",
  "39-logging-service",
  "40-scheduler-service",
  "41-webhook-service",
  "42-export-service",
  "43-import-service",
  "44-backup-service",
  "45-rate-limiter-service",
  "46-ab-testing-service",
  "47-feature-flag-service",
  "48-tax-service",
  "49-fraud-detection-service",
  "50-kyc-service",
  "51-gamification-service",
  "52-social-media-service"
)

# Function to add workflow to repository
function Add-WorkflowToRepo {
  param(
    [string]$RepoName,
    [string]$WorkflowContent,
    [string]$WorkflowFileName
  )
    
  if ($DryRun) {
    Write-Host "    🔍 [DRY RUN] Would create: .github/workflows/$WorkflowFileName" -ForegroundColor $ColorWarning
    return $true
  }
    
  try {
    # Clone repository to temp directory
    $tempDir = Join-Path $env:TEMP "github-workflow-setup-$(Get-Random)"
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
        
    Write-Host "    📥 Cloning repository..." -ForegroundColor Gray
    $cloneResult = gh repo clone "$Owner/$RepoName" $tempDir 2>&1
        
    if ($LASTEXITCODE -ne 0) {
      throw "Failed to clone repository: $cloneResult"
    }
        
    # Create .github/workflows directory
    $workflowDir = Join-Path $tempDir ".github\workflows"
    New-Item -ItemType Directory -Path $workflowDir -Force | Out-Null
        
    # Write workflow file
    $workflowPath = Join-Path $workflowDir $WorkflowFileName
    $WorkflowContent | Out-File -FilePath $workflowPath -Encoding UTF8
        
    # Git operations
    Push-Location $tempDir
        
    git add .github/workflows/$WorkflowFileName
    git commit -m "ci: add $WorkflowFileName GitHub Actions workflow"
    git push origin main
        
    Pop-Location
        
    # Cleanup
    Remove-Item -Path $tempDir -Recurse -Force
        
    return $true
  }
  catch {
    Write-Host "    ❌ Error: $_" -ForegroundColor $ColorError
        
    # Cleanup on error
    if (Test-Path $tempDir) {
      Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
        
    return $false
  }
}

# Statistics
$successCount = 0
$failedCount = 0
$failedRepos = @()

Write-Host "`n▶ Adding workflows to $($services.Count) repositories...`n" -ForegroundColor $ColorInfo

foreach ($service in $services) {
  $repoFullName = "$Owner/$service"
    
  Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
  Write-Host "Repository: $repoFullName" -ForegroundColor White
  Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    
  $repoSuccess = $true
    
  try {
    # Check if repository exists
    Write-Host "  ℹ️  Checking repository..." -ForegroundColor Gray
    gh repo view $repoFullName --json name 2>&1 | Out-Null

    if ($LASTEXITCODE -ne 0) {
      Write-Host "  ⚠️  Repository not found" -ForegroundColor $ColorWarning
      continue
    }
        
    # Add CI workflow
    if ($WorkflowType -eq "CI" -or $WorkflowType -eq "Both") {
      Write-Host "  📄 Adding CI workflow..." -ForegroundColor Gray
      $ciSuccess = Add-WorkflowToRepo -RepoName $service -WorkflowContent $ciWorkflow -WorkflowFileName "ci.yml"
            
      if ($ciSuccess) {
        Write-Host "    ✅ CI workflow added" -ForegroundColor $ColorSuccess
      }
      else {
        $repoSuccess = $false
      }
    }
        
    # Add CD workflow
    if ($WorkflowType -eq "CD" -or $WorkflowType -eq "Both") {
      Write-Host "  📄 Adding CD workflow..." -ForegroundColor Gray
      $cdSuccess = Add-WorkflowToRepo -RepoName $service -WorkflowContent $cdWorkflow -WorkflowFileName "cd.yml"
            
      if ($cdSuccess) {
        Write-Host "    ✅ CD workflow added" -ForegroundColor $ColorSuccess
      }
      else {
        $repoSuccess = $false
      }
    }
        
    if ($repoSuccess) {
      $successCount++
    }
    else {
      $failedCount++
      $failedRepos += $repoFullName
    }
  }
  catch {
    Write-Host "  ❌ Error: $_" -ForegroundColor $ColorError
    $failedCount++
    $failedRepos += $repoFullName
  }
    
  Write-Host ""
}

# Final Report
Write-Host "`n╔════════════════════════════════════════════════════════╗" -ForegroundColor $ColorInfo
Write-Host "║              WORKFLOW SETUP COMPLETE                   ║" -ForegroundColor $ColorInfo
Write-Host "╚════════════════════════════════════════════════════════╝`n" -ForegroundColor $ColorInfo

Write-Host "Results:" -ForegroundColor White
Write-Host "  ✅ Successful    : $successCount/$($services.Count)" -ForegroundColor $ColorSuccess
Write-Host "  ❌ Failed        : $failedCount/$($services.Count)" -ForegroundColor $(if ($failedCount -gt 0) { $ColorError } else { $ColorSuccess })

if ($failedRepos.Count -gt 0) {
  Write-Host "`n❌ Failed repositories:" -ForegroundColor $ColorError
  foreach ($repo in $failedRepos) {
    Write-Host "   - $repo" -ForegroundColor $ColorError
  }
}

if ($DryRun) {
  Write-Host "`n⚠️  This was a DRY RUN. No changes were made." -ForegroundColor $ColorWarning
  Write-Host "   Remove -DryRun parameter to apply changes." -ForegroundColor $ColorWarning
}

Write-Host "`n✨ Script execution completed!`n" -ForegroundColor $ColorSuccess

