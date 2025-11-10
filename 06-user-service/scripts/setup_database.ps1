# Database Setup Script for User Service (PowerShell)
#
# This script creates the required database and user for the User Service.
# Run this script once before starting the service for the first time.
#
# Usage:
#     .\scripts\setup_database.ps1
#
# Or with custom values:
#     $env:POSTGRES_HOST = "localhost"
#     $env:POSTGRES_ADMIN_PASSWORD = "admin123"
#     $env:DB_PASSWORD = "userservice456"
#     .\scripts\setup_database.ps1

# Configuration with defaults
$POSTGRES_HOST = if ($env:POSTGRES_HOST) { $env:POSTGRES_HOST } else { "localhost" }
$POSTGRES_PORT = if ($env:POSTGRES_PORT) { $env:POSTGRES_PORT } else { "5432" }
$POSTGRES_ADMIN_USER = if ($env:POSTGRES_ADMIN_USER) { $env:POSTGRES_ADMIN_USER } else { "postgres" }
$POSTGRES_ADMIN_PASSWORD = $env:POSTGRES_ADMIN_PASSWORD

$DB_NAME = if ($env:DB_NAME) { $env:DB_NAME } else { "user_service_db" }
$DB_USER = if ($env:DB_USER) { $env:DB_USER } else { "user_service" }
$DB_PASSWORD = $env:DB_PASSWORD

# Functions
function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Blue
    Write-Host $Message -ForegroundColor Blue
    Write-Host "============================================================" -ForegroundColor Blue
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "📝 $Message" -ForegroundColor Cyan
}

function Test-Requirements {
    # Check if psql is installed
    if (-not (Get-Command psql -ErrorAction SilentlyContinue)) {
        Write-ErrorMsg "psql is not installed"
        Write-Info "Install PostgreSQL from: https://www.postgresql.org/download/windows/"
        Write-Info "Or use the Python script: python scripts/setup_database.py"
        exit 1
    }
    
    # Check if required environment variables are set
    if (-not $POSTGRES_ADMIN_PASSWORD) {
        Write-ErrorMsg "POSTGRES_ADMIN_PASSWORD is required"
        Write-Info "Set it with: `$env:POSTGRES_ADMIN_PASSWORD = 'your_password'"
        exit 1
    }
    
    if (-not $DB_PASSWORD) {
        Write-ErrorMsg "DB_PASSWORD is required"
        Write-Info "Set it with: `$env:DB_PASSWORD = 'your_password'"
        exit 1
    }
}

function Test-Connection {
    Write-Info "Testing PostgreSQL connection..."
    
    $env:PGPASSWORD = $POSTGRES_ADMIN_PASSWORD
    $null = psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_ADMIN_USER -d postgres -c "SELECT version();" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Connected to PostgreSQL successfully"
        return $true
    }
    else {
        Write-ErrorMsg "Failed to connect to PostgreSQL"
        Write-Info "Check your credentials and ensure PostgreSQL is running"
        exit 1
    }
}

function New-DatabaseUser {
    Write-Info "Creating user '$DB_USER'..."
    
    # Check if user exists
    $env:PGPASSWORD = $POSTGRES_ADMIN_PASSWORD
    $userExists = psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_ADMIN_USER -d postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" 2>$null
    
    if ($userExists -eq "1") {
        Write-Success "User '$DB_USER' already exists"
        Write-Info "Updating password..."
        $null = psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_ADMIN_USER -d postgres -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>&1
        Write-Success "Password updated"
    }
    else {
        $null = psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_ADMIN_USER -d postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>&1
        Write-Success "User '$DB_USER' created"
    }
}

function New-Database {
    Write-Info "Creating database '$DB_NAME'..."
    
    # Check if database exists
    $env:PGPASSWORD = $POSTGRES_ADMIN_PASSWORD
    $dbExists = psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_ADMIN_USER -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" 2>$null
    
    if ($dbExists -eq "1") {
        Write-Success "Database '$DB_NAME' already exists"
        return $false
    }
    else {
        $null = psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_ADMIN_USER -d postgres -c "CREATE DATABASE $DB_NAME;" 2>&1
        Write-Success "Database '$DB_NAME' created"
        return $true
    }
}

function Grant-Privileges {
    Write-Info "Granting privileges..."
    
    $env:PGPASSWORD = $POSTGRES_ADMIN_PASSWORD
    $null = psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_ADMIN_USER -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>&1
    
    Write-Success "Privileges granted"
}

function Initialize-Extensions {
    Write-Info "Setting up extensions..."
    
    $env:PGPASSWORD = $POSTGRES_ADMIN_PASSWORD
    
    # Create extension
    $null = psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_ADMIN_USER -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS ""uuid-ossp"";" 2>&1
    Write-Success "Extension 'uuid-ossp' enabled"
    
    # Grant schema privileges
    $null = psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_ADMIN_USER -d $DB_NAME -c "GRANT ALL ON SCHEMA public TO $DB_USER;" 2>&1
    
    # Grant default privileges
    $null = psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_ADMIN_USER -d $DB_NAME -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;" 2>&1
    $null = psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_ADMIN_USER -d $DB_NAME -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;" 2>&1
    
    Write-Success "Schema privileges configured"
}

function Show-ConnectionInfo {
    $DATABASE_URL = "postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${DB_NAME}"
    
    Write-Host ""
    Write-Header "🎉 Database Setup Completed Successfully!"
    
    Write-Info "Add this to your .env file:"
    Write-Host ""
    Write-Host "DATABASE_URL=$DATABASE_URL" -ForegroundColor White
    Write-Host ""
    Write-Info "Next steps:"
    Write-Host "1. Copy the DATABASE_URL above to your .env file"
    Write-Host "2. Run migrations: alembic upgrade head"
    Write-Host "3. Start the service: uvicorn app.main:app --reload"
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Blue
    Write-Host ""
}

# Main execution
function Main {
    Write-Header "🚀 User Service Database Setup"
    
    Write-Host "Configuration:"
    Write-Host "  PostgreSQL Host: ${POSTGRES_HOST}:${POSTGRES_PORT}"
    Write-Host "  Admin User: $POSTGRES_ADMIN_USER"
    Write-Host "  Database Name: $DB_NAME"
    Write-Host "  Database User: $DB_USER"
    Write-Host ""
    
    Test-Requirements
    Test-Connection
    Write-Host ""
    
    New-DatabaseUser
    Write-Host ""
    
    $dbCreated = New-Database
    Write-Host ""
    
    Grant-Privileges
    Write-Host ""
    
    if ($dbCreated) {
        Initialize-Extensions
        Write-Host ""
    }
    
    Show-ConnectionInfo
}

# Run main function
try {
    Main
}
catch {
    Write-ErrorMsg "An error occurred: $_"
    exit 1
}
