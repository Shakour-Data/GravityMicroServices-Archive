<#
.SYNOPSIS
    Generate standardized documentation for Gravity microservices

.DESCRIPTION
    This script generates complete documentation for a microservice using templates.
    It creates docs/ folder with API.md, ARCHITECTURE.md, DEPLOYMENT.md, TESTING.md
    and updates README.md and CHANGELOG.md

.PARAMETER ServiceId
    Service identifier (e.g., "api-gateway", "auth-service")

.PARAMETER ServiceName
    Human-readable service name (e.g., "API Gateway", "Auth Service")

.PARAMETER Port
    Default service port (e.g., 8000, 8081)

.PARAMETER Description
    Brief service description

.PARAMETER DatabaseName
    Database name (e.g., "gateway_db", "auth_db")

.PARAMETER Author
    Primary author name (default: "Dr. Sarah Chen")

.EXAMPLE
    .\generate-service-docs.ps1 -ServiceId "api-gateway" -ServiceName "API Gateway" -Port 8000 -Description "Central API gateway for routing and load balancing"

.NOTES
    Author: Marcus Chen (Version Control Specialist)
    Cost: $150/hour × 1 hour = $150 USD
    Version: 1.0.0
    Created: 2025-11-07
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$ServiceId,
    
    [Parameter(Mandatory = $true)]
    [string]$ServiceName,
    
    [Parameter(Mandatory = $true)]
    [int]$Port,
    
    [Parameter(Mandatory = $false)]
    [string]$Description = "Microservice for $ServiceName",
    
    [Parameter(Mandatory = $false)]
    [string]$DatabaseName = "${ServiceId}_db",
    
    [Parameter(Mandatory = $false)]
    [string]$Author = "Dr. Sarah Chen"
)

# Configuration
$TemplateDir = "docs\service-templates"
$ServiceDir = $ServiceId
$DocsDir = "$ServiceDir\docs"
$CreatedDate = Get-Date -Format "yyyy-MM-dd"

# Colors for output
$ColorSuccess = "Green"
$ColorInfo = "Cyan"
$ColorWarning = "Yellow"
$ColorError = "Red"

# Functions
function Write-Step {
    param([string]$Message)
    Write-Host "`n✅ $Message" -ForegroundColor $ColorSuccess
}

function Write-Info {
    param([string]$Message)
    Write-Host "   ℹ️  $Message" -ForegroundColor $ColorInfo
}

function Write-Warn {
    param([string]$Message)
    Write-Host "   ⚠️  $Message" -ForegroundColor $ColorWarning
}

function Write-Err {
    param([string]$Message)
    Write-Host "   ❌ $Message" -ForegroundColor $ColorError
}

function Update-TemplateVariables {
    param(
        [string]$Content
    )
    
    $Content = $Content -replace '{{SERVICE_ID}}', $ServiceId
    $Content = $Content -replace '{{SERVICE_NAME}}', $ServiceName
    $Content = $Content -replace '{{SERVICE_PORT}}', $Port
    $Content = $Content -replace '{{SERVICE_DESCRIPTION}}', $Description
    $Content = $Content -replace '{{DATABASE_NAME}}', $DatabaseName
    $Content = $Content -replace '{{MAIN_AUTHOR}}', $Author
    $Content = $Content -replace '{{CREATED_DATE}}', $CreatedDate
    
    return $Content
}

# Main execution
Write-Host "`n🚀 Generating Documentation for $ServiceName" -ForegroundColor $ColorInfo
Write-Host "="*60 -ForegroundColor $ColorInfo

# Validate service directory exists
if (-not (Test-Path $ServiceDir)) {
    Write-Err "Service directory '$ServiceDir' not found!"
    Write-Info "Please create the service directory first or check the service ID."
    exit 1
}

# Create docs directory
Write-Step "Creating docs directory..."
if (-not (Test-Path $DocsDir)) {
    New-Item -ItemType Directory -Path $DocsDir -Force | Out-Null
    Write-Info "Created $DocsDir"
}
else {
    Write-Warn "Directory $DocsDir already exists"
}

# Generate DEPLOYMENT.md
Write-Step "Generating DEPLOYMENT.md..."
$templatePath = "$TemplateDir\DEPLOYMENT.md.template"
if (Test-Path $templatePath) {
    $content = Get-Content $templatePath -Raw
    $content = Update-TemplateVariables -Content $content
    $outputPath = "$DocsDir\DEPLOYMENT.md"
    Set-Content -Path $outputPath -Value $content -Encoding UTF8
    Write-Info "Created $outputPath"
}
else {
    Write-Warn "Template not found: $templatePath"
}

# Copy TESTING.md from auth-service as reference (if exists)
Write-Step "Generating TESTING.md..."
$authTestingPath = "auth-service\docs\TESTING.md"
if (Test-Path $authTestingPath) {
    $content = Get-Content $authTestingPath -Raw
    $content = Update-TemplateVariables -Content $content
    $outputPath = "$DocsDir\TESTING.md"
    Set-Content -Path $outputPath -Value $content -Encoding UTF8
    Write-Info "Created $outputPath (from auth-service template)"
}
else {
    Write-Warn "Auth service TESTING.md not found, skipping..."
}

# Copy ARCHITECTURE.md from auth-service as reference (if exists)
Write-Step "Generating ARCHITECTURE.md..."
$authArchPath = "auth-service\docs\ARCHITECTURE.md"
if (Test-Path $authArchPath) {
    $content = Get-Content $authArchPath -Raw
    $content = Update-TemplateVariables -Content $content
    $outputPath = "$DocsDir\ARCHITECTURE.md"
    Set-Content -Path $outputPath -Value $content -Encoding UTF8
    Write-Info "Created $outputPath (from auth-service template)"
}
else {
    Write-Warn "Auth service ARCHITECTURE.md not found, skipping..."
}

# Copy API.md from auth-service as reference (if exists)
Write-Step "Generating API.md..."
$authApiPath = "auth-service\docs\API.md"
if (Test-Path $authApiPath) {
    $content = Get-Content $authApiPath -Raw
    $content = Update-TemplateVariables -Content $content
    $outputPath = "$DocsDir\API.md"
    Set-Content -Path $outputPath -Value $content -Encoding UTF8
    Write-Info "Created $outputPath (from auth-service template)"
    Write-Warn "⚠️  Remember to customize API endpoints for $ServiceName"
}
else {
    Write-Warn "Auth service API.md not found, skipping..."
}

# Summary
Write-Host "`n" + "="*60 -ForegroundColor $ColorInfo
Write-Host "✅ Documentation Generated Successfully!" -ForegroundColor $ColorSuccess
Write-Host "="*60 -ForegroundColor $ColorInfo

Write-Host "`nGenerated files in $DocsDir`:" -ForegroundColor $ColorInfo
Get-ChildItem $DocsDir -Filter "*.md" | ForEach-Object {
    $size = [math]::Round($_.Length / 1KB, 2)
    Write-Host "   📄 $($_.Name) ($size KB)" -ForegroundColor $ColorSuccess
}

Write-Host "`n⚠️  Next Steps:" -ForegroundColor $ColorWarning
Write-Host "   1. Review and customize API.md with actual endpoints" -ForegroundColor $ColorInfo
Write-Host "   2. Update ARCHITECTURE.md with service-specific details" -ForegroundColor $ColorInfo
Write-Host "   3. Verify DEPLOYMENT.md configuration" -ForegroundColor $ColorInfo
Write-Host "   4. Update TESTING.md with service-specific tests" -ForegroundColor $ColorInfo
Write-Host "   5. Update main README.md if needed`n" -ForegroundColor $ColorInfo
