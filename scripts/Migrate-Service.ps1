<#
.SYNOPSIS
    Migrate a single service from monorepo to its own GitHub repository

.DESCRIPTION
    This script extracts a service from the monorepo and creates a new independent
    GitHub repository with full CI/CD, following the multi-repo strategy.

.PARAMETER ServiceNumber
    The service number (01-52)

.PARAMETER ServiceName
    The service name (e.g., "common-library", "auth-service")

.PARAMETER GitHubOrg
    GitHub organization name (default: "GravityMicroServices")

.PARAMETER GitHubToken
    GitHub Personal Access Token with repo permissions

.PARAMETER DryRun
    If set, shows what would be done without making changes

.EXAMPLE
    .\Migrate-Service.ps1 -ServiceNumber "01" -ServiceName "common-library" -GitHubToken "ghp_xxx"

.NOTES
    Author: Gravity Elite Engineering Team
    Version: 1.0.0
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$ServiceNumber,

    [Parameter(Mandatory = $true)]
    [string]$ServiceName,

    [Parameter(Mandatory = $false)]
    [string]$GitHubOrg = "GravityMicroServices",

    [Parameter(Mandatory = $true)]
    [string]$GitHubToken,

    [Parameter(Mandatory = $false)]
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# Colors for output
function Write-Success { param($Message) Write-Host "✓ $Message" -ForegroundColor Green }
function Write-Info { param($Message) Write-Host "ℹ $Message" -ForegroundColor Cyan }
function Write-Warning { param($Message) Write-Host "⚠ $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "✗ $Message" -ForegroundColor Red }

# Configuration
$ServiceFolderName = "$ServiceNumber-$ServiceName"
$RepositoryName = "gravity-$ServiceName"
$MonorepoPath = $PSScriptRoot
$TempPath = Join-Path $env:TEMP "gravity-migration-$ServiceFolderName"
$TemplatePath = Join-Path $MonorepoPath "gravity-template-service"

Write-Info "================================================"
Write-Info "  Gravity Service Migration Tool"
Write-Info "================================================"
Write-Info ""
Write-Info "Service: $ServiceFolderName"
Write-Info "Repository: $RepositoryName"
Write-Info "Organization: $GitHubOrg"
Write-Info "Dry Run: $DryRun"
Write-Info ""

# Step 1: Validate service exists
Write-Info "[Step 1/10] Validating service..."
$ServicePath = Join-Path $MonorepoPath $ServiceFolderName
if (-not (Test-Path $ServicePath)) {
    Write-Error "Service folder not found: $ServicePath"
    exit 1
}
Write-Success "Service folder found: $ServicePath"

# Step 2: Validate template exists
Write-Info "[Step 2/10] Validating template..."
if (-not (Test-Path $TemplatePath)) {
    Write-Error "Template folder not found: $TemplatePath"
    exit 1
}
Write-Success "Template found: $TemplatePath"

# Step 3: Create temporary working directory
Write-Info "[Step 3/10] Creating temporary directory..."
if (Test-Path $TempPath) {
    Remove-Item $TempPath -Recurse -Force
}
New-Item -ItemType Directory -Path $TempPath -Force | Out-Null
Write-Success "Temporary directory created: $TempPath"

# Step 4: Copy template to temporary directory
Write-Info "[Step 4/10] Copying template..."
Copy-Item -Path "$TemplatePath\*" -Destination $TempPath -Recurse -Force
Write-Success "Template copied to temporary directory"

# Step 5: Copy service files
Write-Info "[Step 5/10] Copying service files..."

# Copy app/ directory if exists
if (Test-Path "$ServicePath\app") {
    Write-Info "  Copying app/ directory..."
    Remove-Item "$TempPath\app" -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item "$ServicePath\app" -Destination "$TempPath\app" -Recurse -Force
}

# Copy tests/ directory if exists
if (Test-Path "$ServicePath\tests") {
    Write-Info "  Copying tests/ directory..."
    Remove-Item "$TempPath\tests" -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item "$ServicePath\tests" -Destination "$TempPath\tests" -Recurse -Force
}

# Copy alembic/ directory if exists
if (Test-Path "$ServicePath\alembic") {
    Write-Info "  Copying alembic/ directory..."
    Remove-Item "$TempPath\alembic" -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item "$ServicePath\alembic" -Destination "$TempPath\alembic" -Recurse -Force
}

# Copy k8s/ directory if exists
if (Test-Path "$ServicePath\k8s") {
    Write-Info "  Copying k8s/ directory..."
    Remove-Item "$TempPath\k8s" -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item "$ServicePath\k8s" -Destination "$TempPath\k8s" -Recurse -Force
}

# Copy scripts/ directory if exists
if (Test-Path "$ServicePath\scripts") {
    Write-Info "  Copying scripts/ directory..."
    Remove-Item "$TempPath\scripts" -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item "$ServicePath\scripts" -Destination "$TempPath\scripts" -Recurse -Force
}

# Copy configuration files if they exist
$ConfigFiles = @(
    "pyproject.toml",
    "alembic.ini",
    "pytest.ini",
    "docker-compose.yml",
    "Dockerfile",
    ".env.example",
    "README.md",
    "DEPLOYMENT.md",
    "IMPLEMENTATION_SUMMARY.md"
)

foreach ($file in $ConfigFiles) {
    if (Test-Path "$ServicePath\$file") {
        Write-Info "  Copying $file..."
        Copy-Item "$ServicePath\$file" -Destination "$TempPath\$file" -Force
    }
}

Write-Success "Service files copied"

# Step 6: Update placeholders in files
Write-Info "[Step 6/10] Updating placeholders..."

# Determine service port (8000 + service number)
$ServicePort = 8000 + [int]$ServiceNumber

# Files to update
$FilesToUpdate = Get-ChildItem -Path $TempPath -Recurse -File -Include @(
    "*.py", "*.md", "*.yml", "*.yaml", "*.toml", "*.ini", "*.example"
)

foreach ($file in $FilesToUpdate) {
    $content = Get-Content $file.FullName -Raw
    
    # Replace placeholders
    $content = $content -replace 'template-service', $ServiceName
    $content = $content -replace 'SERVICE_NAME', $ServiceName
    $content = $content -replace 'SERVICE_PORT', $ServicePort
    $content = $content -replace 'gravity-template-service', $RepositoryName
    
    Set-Content -Path $file.FullName -Value $content -NoNewline
}

Write-Success "Placeholders updated"

# Step 7: Initialize git repository
Write-Info "[Step 7/10] Initializing git repository..."

if (-not $DryRun) {
    Push-Location $TempPath
    
    git init | Out-Null
    git add . | Out-Null
    git commit -m "Initial commit from monorepo migration" | Out-Null
    
    Pop-Location
    Write-Success "Git repository initialized"
}
else {
    Write-Warning "Dry run: Skipping git initialization"
}

# Step 8: Create GitHub repository
Write-Info "[Step 8/10] Creating GitHub repository..."

$Headers = @{
    "Authorization" = "token $GitHubToken"
    "Accept"        = "application/vnd.github.v3+json"
    "Content-Type"  = "application/json"
}

if (-not $DryRun) {
    try {
        # Check if repository exists
        $CheckUrl = "https://api.github.com/repos/$GitHubOrg/$RepositoryName"
        try {
            $ExistingRepo = Invoke-RestMethod -Uri $CheckUrl -Headers $Headers -Method Get
            Write-Warning "Repository already exists: $RepositoryName"
        }
        catch {
            # Repository doesn't exist, create it
            $CreateUrl = "https://api.github.com/orgs/$GitHubOrg/repos"
            $Body = @{
                name         = $RepositoryName
                description  = "Gravity $ServiceName Service - Part of GravityMicroServices Platform"
                private      = $false
                has_issues   = $true
                has_projects = $true
                has_wiki     = $true
                auto_init    = $false
            } | ConvertTo-Json

            $NewRepo = Invoke-RestMethod -Uri $CreateUrl -Headers $Headers -Method Post -Body $Body
            Write-Success "Repository created: $RepositoryName"
        }
    }
    catch {
        Write-Error "Failed to create repository: $_"
        exit 1
    }
}
else {
    Write-Warning "Dry run: Skipping repository creation"
}

# Step 9: Push to GitHub
Write-Info "[Step 9/10] Pushing to GitHub..."

if (-not $DryRun) {
    Push-Location $TempPath
    
    $RemoteUrl = "https://$($GitHubToken)@github.com/$GitHubOrg/$RepositoryName.git"
    
    git remote add origin $RemoteUrl | Out-Null
    git branch -M main | Out-Null
    git push -u origin main | Out-Null
    
    Pop-Location
    Write-Success "Pushed to GitHub: https://github.com/$GitHubOrg/$RepositoryName"
}
else {
    Write-Warning "Dry run: Skipping push to GitHub"
}

# Step 10: Apply labels and settings
Write-Info "[Step 10/10] Applying labels and settings..."

if (-not $DryRun) {
    try {
        # Load organization config
        $ConfigPath = Join-Path $MonorepoPath "migration\organization-config.json"
        if (Test-Path $ConfigPath) {
            $OrgConfig = Get-Content $ConfigPath | ConvertFrom-Json
            
            # Apply labels
            Write-Info "  Applying labels..."
            foreach ($label in $OrgConfig.labels) {
                $LabelUrl = "https://api.github.com/repos/$GitHubOrg/$RepositoryName/labels"
                $LabelBody = @{
                    name        = $label.name
                    color       = $label.color
                    description = $label.description
                } | ConvertTo-Json

                try {
                    Invoke-RestMethod -Uri $LabelUrl -Headers $Headers -Method Post -Body $LabelBody | Out-Null
                }
                catch {
                    Write-Warning "Label already exists: $($label.name)"
                }
            }

            # Apply branch protection
            Write-Info "  Applying branch protection..."
            $ProtectionUrl = "https://api.github.com/repos/$GitHubOrg/$RepositoryName/branches/main/protection"
            $ProtectionBody = $OrgConfig.branch_protection | ConvertTo-Json -Depth 10

            try {
                Invoke-RestMethod -Uri $ProtectionUrl -Headers $Headers -Method Put -Body $ProtectionBody | Out-Null
                Write-Success "Branch protection applied"
            }
            catch {
                Write-Warning "Could not apply branch protection: $_"
            }
        }
    }
    catch {
        Write-Warning "Could not apply all settings: $_"
    }
}
else {
    Write-Warning "Dry run: Skipping labels and settings"
}

# Cleanup
Write-Info "Cleaning up..."
if (-not $DryRun) {
    Remove-Item $TempPath -Recurse -Force
}

Write-Success "================================================"
Write-Success "  Migration completed successfully!"
Write-Success "================================================"
Write-Info ""
Write-Info "Repository URL: https://github.com/$GitHubOrg/$RepositoryName"
Write-Info "Clone command: git clone https://github.com/$GitHubOrg/$RepositoryName.git"
Write-Info ""

# Generate migration log
$LogPath = Join-Path $MonorepoPath "migration\migration-log.txt"
$LogEntry = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Migrated $ServiceFolderName to $RepositoryName`n"
Add-Content -Path $LogPath -Value $LogEntry

Write-Success "Migration log updated: $LogPath"
