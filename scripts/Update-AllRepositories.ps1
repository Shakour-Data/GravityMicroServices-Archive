<#
.SYNOPSIS
    Update all Gravity microservice repositories

.DESCRIPTION
    Pulls latest changes from main branch for all 52 repositories

.PARAMETER RepositoriesDirectory
    Directory containing all cloned repositories

.EXAMPLE
    .\Update-AllRepositories.ps1 -RepositoriesDirectory "C:\Projects\Gravity"

.NOTES
    Author: Gravity Elite Engineering Team
    Version: 1.0.0
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$RepositoriesDirectory
)

$ErrorActionPreference = "Continue"

function Write-Success { param($Message) Write-Host "✓ $Message" -ForegroundColor Green }
function Write-Info { param($Message) Write-Host "ℹ $Message" -ForegroundColor Cyan }
function Write-Warning { param($Message) Write-Host "⚠ $Message" -ForegroundColor Yellow }

Write-Info "Updating all repositories in: $RepositoriesDirectory"

# Find all gravity-* directories
$Repositories = Get-ChildItem -Path $RepositoriesDirectory -Directory -Filter "gravity-*"

Write-Info "Found $($Repositories.Count) repositories"

$Stats = @{
    Total     = $Repositories.Count
    Updated   = 0
    Failed    = 0
    NoChanges = 0
}

foreach ($repo in $Repositories) {
    Write-Info "Updating $($repo.Name)..."
    
    Push-Location $repo.FullName
    
    try {
        # Fetch latest
        git fetch origin | Out-Null
        
        # Check current branch
        $CurrentBranch = git branch --show-current
        
        # Pull latest
        $Output = git pull origin $CurrentBranch 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            if ($Output -match "Already up to date") {
                $Stats.NoChanges++
                Write-Info "No changes: $($repo.Name)"
            }
            else {
                $Stats.Updated++
                Write-Success "Updated: $($repo.Name)"
            }
        }
        else {
            $Stats.Failed++
            Write-Warning "Failed to update: $($repo.Name)"
        }
    }
    catch {
        $Stats.Failed++
        Write-Warning "Error updating $($repo.Name): $_"
    }
    
    Pop-Location
}

Write-Host ""
Write-Info "Update Summary:"
Write-Host "  Total: $($Stats.Total)" -ForegroundColor White
Write-Host "  Updated: $($Stats.Updated)" -ForegroundColor Green
Write-Host "  No Changes: $($Stats.NoChanges)" -ForegroundColor Cyan
Write-Host "  Failed: $($Stats.Failed)" -ForegroundColor Red
