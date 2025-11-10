#!/bin/bash
#
# Database Setup Script for User Service (Bash)
#
# This script creates the required database and user for the User Service.
# Run this script once before starting the service for the first time.
#
# Usage:
#     ./scripts/setup_database.sh
#
# Or with custom values:
#     POSTGRES_HOST=localhost \
#     POSTGRES_ADMIN_PASSWORD=admin123 \
#     DB_PASSWORD=userservice456 \
#     ./scripts/setup_database.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration with defaults
POSTGRES_HOST="${POSTGRES_HOST:-localhost}"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"
POSTGRES_ADMIN_USER="${POSTGRES_ADMIN_USER:-postgres}"
POSTGRES_ADMIN_PASSWORD="${POSTGRES_ADMIN_PASSWORD}"

DB_NAME="${DB_NAME:-user_service_db}"
DB_USER="${DB_USER:-user_service}"
DB_PASSWORD="${DB_PASSWORD}"

# Functions
print_header() {
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}📝 $1${NC}"
}

check_requirements() {
    # Check if psql is installed
    if ! command -v psql &> /dev/null; then
        print_error "psql is not installed"
        print_info "Install PostgreSQL client:"
        print_info "  Ubuntu/Debian: sudo apt-get install postgresql-client"
        print_info "  macOS: brew install postgresql"
        print_info "  Windows: Use setup_database.ps1 instead"
        exit 1
    fi
    
    # Check if required environment variables are set
    if [ -z "$POSTGRES_ADMIN_PASSWORD" ]; then
        print_error "POSTGRES_ADMIN_PASSWORD is required"
        print_info "Set it with: export POSTGRES_ADMIN_PASSWORD=your_password"
        exit 1
    fi
    
    if [ -z "$DB_PASSWORD" ]; then
        print_error "DB_PASSWORD is required"
        print_info "Set it with: export DB_PASSWORD=your_password"
        exit 1
    fi
}

test_connection() {
    print_info "Testing PostgreSQL connection..."
    
    if PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" psql \
        -h "$POSTGRES_HOST" \
        -p "$POSTGRES_PORT" \
        -U "$POSTGRES_ADMIN_USER" \
        -d postgres \
        -c "SELECT version();" > /dev/null 2>&1; then
        print_success "Connected to PostgreSQL successfully"
        return 0
    else
        print_error "Failed to connect to PostgreSQL"
        print_info "Check your credentials and ensure PostgreSQL is running"
        exit 1
    fi
}

create_user() {
    print_info "Creating user '$DB_USER'..."
    
    # Check if user exists
    USER_EXISTS=$(PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" psql \
        -h "$POSTGRES_HOST" \
        -p "$POSTGRES_PORT" \
        -U "$POSTGRES_ADMIN_USER" \
        -d postgres \
        -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'")
    
    if [ "$USER_EXISTS" = "1" ]; then
        print_success "User '$DB_USER' already exists"
        print_info "Updating password..."
        PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" psql \
            -h "$POSTGRES_HOST" \
            -p "$POSTGRES_PORT" \
            -U "$POSTGRES_ADMIN_USER" \
            -d postgres \
            -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" > /dev/null
        print_success "Password updated"
    else
        PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" psql \
            -h "$POSTGRES_HOST" \
            -p "$POSTGRES_PORT" \
            -U "$POSTGRES_ADMIN_USER" \
            -d postgres \
            -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" > /dev/null
        print_success "User '$DB_USER' created"
    fi
}

create_database() {
    print_info "Creating database '$DB_NAME'..."
    
    # Check if database exists
    DB_EXISTS=$(PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" psql \
        -h "$POSTGRES_HOST" \
        -p "$POSTGRES_PORT" \
        -U "$POSTGRES_ADMIN_USER" \
        -d postgres \
        -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")
    
    if [ "$DB_EXISTS" = "1" ]; then
        print_success "Database '$DB_NAME' already exists"
    else
        PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" psql \
            -h "$POSTGRES_HOST" \
            -p "$POSTGRES_PORT" \
            -U "$POSTGRES_ADMIN_USER" \
            -d postgres \
            -c "CREATE DATABASE $DB_NAME;" > /dev/null
        print_success "Database '$DB_NAME' created"
    fi
}

grant_privileges() {
    print_info "Granting privileges..."
    
    PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" psql \
        -h "$POSTGRES_HOST" \
        -p "$POSTGRES_PORT" \
        -U "$POSTGRES_ADMIN_USER" \
        -d postgres \
        -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" > /dev/null
    
    print_success "Privileges granted"
}

setup_extensions() {
    print_info "Setting up extensions..."
    
    PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" psql \
        -h "$POSTGRES_HOST" \
        -p "$POSTGRES_PORT" \
        -U "$POSTGRES_ADMIN_USER" \
        -d "$DB_NAME" \
        -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";" > /dev/null
    
    print_success "Extension 'uuid-ossp' enabled"
    
    # Grant schema privileges
    PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" psql \
        -h "$POSTGRES_HOST" \
        -p "$POSTGRES_PORT" \
        -U "$POSTGRES_ADMIN_USER" \
        -d "$DB_NAME" \
        -c "GRANT ALL ON SCHEMA public TO $DB_USER;" > /dev/null
    
    # Grant default privileges
    PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" psql \
        -h "$POSTGRES_HOST" \
        -p "$POSTGRES_PORT" \
        -U "$POSTGRES_ADMIN_USER" \
        -d "$DB_NAME" \
        -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;" > /dev/null
    
    PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" psql \
        -h "$POSTGRES_HOST" \
        -p "$POSTGRES_PORT" \
        -U "$POSTGRES_ADMIN_USER" \
        -d "$DB_NAME" \
        -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;" > /dev/null
    
    print_success "Schema privileges configured"
}

print_connection_info() {
    DATABASE_URL="postgresql+asyncpg://$DB_USER:$DB_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$DB_NAME"
    
    echo
    print_header "🎉 Database Setup Completed Successfully!"
    echo
    print_info "Add this to your .env file:"
    echo
    echo "DATABASE_URL=$DATABASE_URL"
    echo
    print_info "Next steps:"
    echo "1. Copy the DATABASE_URL above to your .env file"
    echo "2. Run migrations: alembic upgrade head"
    echo "3. Start the service: uvicorn app.main:app --reload"
    echo
    echo -e "${BLUE}============================================================${NC}"
}

# Main execution
main() {
    print_header "🚀 User Service Database Setup"
    
    echo "Configuration:"
    echo "  PostgreSQL Host: $POSTGRES_HOST:$POSTGRES_PORT"
    echo "  Admin User: $POSTGRES_ADMIN_USER"
    echo "  Database Name: $DB_NAME"
    echo "  Database User: $DB_USER"
    echo
    
    check_requirements
    test_connection
    echo
    
    create_user
    echo
    
    create_database
    echo
    
    grant_privileges
    echo
    
    setup_extensions
    echo
    
    print_connection_info
}

# Run main function
main
