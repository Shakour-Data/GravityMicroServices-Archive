<#
.SYNOPSIS
    Execute a command across all Gravity repositories

.DESCRIPTION
    Runs a git command or script across all 52 repositories

.PARAMETER RepositoriesDirectory
    Directory containing all cloned repositories

.PARAMETER Command
    Command to execute (e.g., "git status", "npm test")

.EXAMPLE
    .\Execute-CommandAcrossRepos.ps1 -RepositoriesDirectory "C:\Projects\Gravity" -Command "git status"

.EXAMPLE
    .\Execute-CommandAcrossRepos.ps1 -RepositoriesDirectory "." -Command "poetry install"

.NOTES
    Author: Gravity Elite Engineering Team
    Version: 1.0.0
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$RepositoriesDirectory,

    [Parameter(Mandatory = $true)]
    [string]$Command
)

$ErrorActionPreference = "Continue"

function Write-Info { param($Message) Write-Host "ℹ $Message" -ForegroundColor Cyan }

Write-Info "Executing command across all repositories: $Command"

# Find all gravity-* directories
$Repositories = Get-ChildItem -Path $RepositoriesDirectory -Directory -Filter "gravity-*"

Write-Info "Found $($Repositories.Count) repositories"

foreach ($repo in $Repositories) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host " Repository: $($repo.Name)" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    
    Push-Location $repo.FullName
    
    try {
        Invoke-Expression $Command
    }
    catch {
        Write-Host "Error in $($repo.Name): $_" -ForegroundColor Red
    }
    
    Pop-Location
}

Write-Host ""
Write-Info "Command execution completed!"
