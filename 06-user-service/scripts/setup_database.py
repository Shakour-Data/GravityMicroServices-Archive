#!/usr/bin/env python3
"""
Database Setup Script for User Service

This script creates the required database and user for the User Service.
Run this script once before starting the service for the first time.

Usage:
    python scripts/setup_database.py

Environment Variables Required:
    POSTGRES_HOST: PostgreSQL host (default: localhost)
    POSTGRES_PORT: PostgreSQL port (default: 5432)
    POSTGRES_ADMIN_USER: Admin user (default: postgres)
    POSTGRES_ADMIN_PASSWORD: Admin password (required)
    
    DB_NAME: Database name to create (default: user_service_db)
    DB_USER: Database user to create (default: user_service)
    DB_PASSWORD: Database user password (required)

Example:
    export POSTGRES_ADMIN_PASSWORD=admin123
    export DB_PASSWORD=userservice456
    python scripts/setup_database.py
"""

import os
import sys
from typing import Optional

try:
    import psycopg2
    from psycopg2 import sql
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
except ImportError:
    print("❌ Error: psycopg2 is not installed")
    print("Install it with: pip install psycopg2-binary")
    sys.exit(1)


class DatabaseSetup:
    """Setup database and user for User Service."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        # PostgreSQL admin connection
        self.pg_host = os.getenv("POSTGRES_HOST", "localhost")
        self.pg_port = int(os.getenv("POSTGRES_PORT", "5432"))
        self.pg_admin_user = os.getenv("POSTGRES_ADMIN_USER", "postgres")
        self.pg_admin_password = os.getenv("POSTGRES_ADMIN_PASSWORD")
        
        # Database to create
        self.db_name = os.getenv("DB_NAME", "user_service_db")
        self.db_user = os.getenv("DB_USER", "user_service")
        self.db_password = os.getenv("DB_PASSWORD")
        
        # Validation
        if not self.pg_admin_password:
            print("❌ Error: POSTGRES_ADMIN_PASSWORD is required")
            print("Set it with: export POSTGRES_ADMIN_PASSWORD=your_password")
            sys.exit(1)
        
        if not self.db_password:
            print("❌ Error: DB_PASSWORD is required")
            print("Set it with: export DB_PASSWORD=your_password")
            sys.exit(1)
    
    def connect_admin(self):
        """Connect to PostgreSQL with admin credentials."""
        try:
            conn = psycopg2.connect(
                host=self.pg_host,
                port=self.pg_port,
                user=self.pg_admin_user,
                password=self.pg_admin_password,
                database="postgres"
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            return conn
        except psycopg2.Error as e:
            print(f"❌ Failed to connect to PostgreSQL: {e}")
            sys.exit(1)
    
    def database_exists(self, cursor, db_name: str) -> bool:
        """Check if database exists."""
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        return cursor.fetchone() is not None
    
    def user_exists(self, cursor, username: str) -> bool:
        """Check if user exists."""
        cursor.execute(
            "SELECT 1 FROM pg_roles WHERE rolname = %s",
            (username,)
        )
        return cursor.fetchone() is not None
    
    def create_database(self, cursor):
        """Create database if it doesn't exist."""
        if self.database_exists(cursor, self.db_name):
            print(f"✅ Database '{self.db_name}' already exists")
            return False
        
        print(f"📦 Creating database '{self.db_name}'...")
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(self.db_name)
            )
        )
        print(f"✅ Database '{self.db_name}' created successfully")
        return True
    
    def create_user(self, cursor):
        """Create user if it doesn't exist."""
        if self.user_exists(cursor, self.db_user):
            print(f"✅ User '{self.db_user}' already exists")
            # Update password anyway
            print(f"🔄 Updating password for user '{self.db_user}'...")
            cursor.execute(
                sql.SQL("ALTER USER {} WITH PASSWORD %s").format(
                    sql.Identifier(self.db_user)
                ),
                (self.db_password,)
            )
            print(f"✅ Password updated for user '{self.db_user}'")
            return False
        
        print(f"👤 Creating user '{self.db_user}'...")
        cursor.execute(
            sql.SQL("CREATE USER {} WITH PASSWORD %s").format(
                sql.Identifier(self.db_user)
            ),
            (self.db_password,)
        )
        print(f"✅ User '{self.db_user}' created successfully")
        return True
    
    def grant_privileges(self, cursor):
        """Grant all privileges on database to user."""
        print(f"🔐 Granting privileges on '{self.db_name}' to '{self.db_user}'...")
        
        # Grant database privileges
        cursor.execute(
            sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                sql.Identifier(self.db_name),
                sql.Identifier(self.db_user)
            )
        )
        
        print(f"✅ Privileges granted successfully")
    
    def setup_extensions(self):
        """Setup required PostgreSQL extensions."""
        print(f"🔌 Setting up extensions in '{self.db_name}'...")
        
        try:
            # Connect to the new database
            conn = psycopg2.connect(
                host=self.pg_host,
                port=self.pg_port,
                user=self.pg_admin_user,
                password=self.pg_admin_password,
                database=self.db_name
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Create uuid-ossp extension
            cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
            print("  ✅ uuid-ossp extension enabled")
            
            # Grant schema privileges
            cursor.execute(
                sql.SQL("GRANT ALL ON SCHEMA public TO {}").format(
                    sql.Identifier(self.db_user)
                )
            )
            
            # Grant default privileges for future tables
            cursor.execute(
                sql.SQL(
                    "ALTER DEFAULT PRIVILEGES IN SCHEMA public "
                    "GRANT ALL ON TABLES TO {}"
                ).format(sql.Identifier(self.db_user))
            )
            
            cursor.execute(
                sql.SQL(
                    "ALTER DEFAULT PRIVILEGES IN SCHEMA public "
                    "GRANT ALL ON SEQUENCES TO {}"
                ).format(sql.Identifier(self.db_user))
            )
            
            print("  ✅ Schema privileges configured")
            
            cursor.close()
            conn.close()
            
        except psycopg2.Error as e:
            print(f"⚠️  Warning: Could not setup extensions: {e}")
    
    def print_connection_string(self):
        """Print the DATABASE_URL for the service."""
        database_url = (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.pg_host}:{self.pg_port}/{self.db_name}"
        )
        
        print("\n" + "="*60)
        print("🎉 Database setup completed successfully!")
        print("="*60)
        print("\n📝 Add this to your .env file:\n")
        print(f"DATABASE_URL={database_url}")
        print("\n🚀 Next steps:")
        print("1. Copy the DATABASE_URL above to your .env file")
        print("2. Run migrations: alembic upgrade head")
        print("3. Start the service: uvicorn app.main:app --reload")
        print("="*60 + "\n")
    
    def run(self):
        """Execute the database setup."""
        print("\n" + "="*60)
        print("🚀 User Service Database Setup")
        print("="*60 + "\n")
        
        print(f"Configuration:")
        print(f"  PostgreSQL Host: {self.pg_host}:{self.pg_port}")
        print(f"  Admin User: {self.pg_admin_user}")
        print(f"  Database Name: {self.db_name}")
        print(f"  Database User: {self.db_user}")
        print()
        
        # Connect to PostgreSQL
        print("🔌 Connecting to PostgreSQL...")
        conn = self.connect_admin()
        cursor = conn.cursor()
        print("✅ Connected successfully\n")
        
        # Create user
        self.create_user(cursor)
        print()
        
        # Create database
        db_created = self.create_database(cursor)
        print()
        
        # Grant privileges
        self.grant_privileges(cursor)
        print()
        
        # Close admin connection
        cursor.close()
        conn.close()
        
        # Setup extensions (needs separate connection to new db)
        if db_created:
            self.setup_extensions()
            print()
        
        # Print connection string
        self.print_connection_string()


def main():
    """Main entry point."""
    try:
        setup = DatabaseSetup()
        setup.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
