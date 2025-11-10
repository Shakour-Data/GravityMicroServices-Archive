"""Initial migration - Create user tables

Revision ID: 001
Revises: 
Create Date: 2025-11-08 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create user_profiles table
    op.create_table(
        'user_profiles',
        sa.Column('id', sa.String(36), primary_key=True, index=True),
        sa.Column('user_id', sa.String(36), nullable=False, unique=True, index=True, 
                  comment='User ID from auth-service'),
        sa.Column('display_name', sa.String(100), nullable=False, index=True, 
                  comment='User display name'),
        sa.Column('bio', sa.Text(), nullable=True, comment='User biography (max 500 chars)'),
        sa.Column('avatar_url', sa.String(255), nullable=True, 
                  comment='Avatar image URL from file-service'),
        sa.Column('location', sa.String(100), nullable=True, comment='User location'),
        sa.Column('website', sa.String(255), nullable=True, comment='User website URL'),
        sa.Column('phone_number', sa.String(20), nullable=True, comment='User phone number'),
        sa.Column('is_verified', sa.Boolean(), default=False, nullable=False, index=True, 
                  comment='Email verification status'),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False, index=True, 
                  comment='Account active status'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), 
                  nullable=False, comment='Record creation timestamp (UTC)'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), 
                  onupdate=sa.func.now(), nullable=False, comment='Record update timestamp (UTC)'),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True, 
                  comment='Last login timestamp (UTC)'),
        comment='User profile information table'
    )
    
    # Create indexes
    op.create_index('idx_user_profiles_user_id', 'user_profiles', ['user_id'])
    op.create_index('idx_user_profiles_display_name', 'user_profiles', ['display_name'])
    op.create_index('idx_user_profiles_is_active', 'user_profiles', ['is_active'])
    op.create_index('idx_user_profiles_is_verified', 'user_profiles', ['is_verified'])
    op.create_index('idx_user_profiles_created_at', 'user_profiles', ['created_at'])
    
    # Create user_preferences table
    op.create_table(
        'user_preferences',
        sa.Column('id', sa.String(36), primary_key=True, index=True),
        sa.Column('profile_id', sa.String(36), sa.ForeignKey('user_profiles.id', ondelete='CASCADE'), 
                  nullable=False, unique=True, index=True, comment='Foreign key to user_profiles'),
        sa.Column('language', sa.String(10), default='en', nullable=False, 
                  comment='Preferred language (ISO 639-1)'),
        sa.Column('timezone', sa.String(50), default='UTC', nullable=False, 
                  comment='User timezone (IANA timezone)'),
        sa.Column('theme', sa.String(20), default='auto', nullable=False, 
                  comment='UI theme (light/dark/auto)'),
        sa.Column('date_format', sa.String(20), default='YYYY-MM-DD', nullable=False, 
                  comment='Date format preference'),
        sa.Column('time_format', sa.String(10), default='24h', nullable=False, 
                  comment='Time format (12h/24h)'),
        sa.Column('email_notifications', sa.Boolean(), default=True, nullable=False, 
                  comment='Enable email notifications'),
        sa.Column('push_notifications', sa.Boolean(), default=True, nullable=False, 
                  comment='Enable push notifications'),
        sa.Column('sms_notifications', sa.Boolean(), default=False, nullable=False, 
                  comment='Enable SMS notifications'),
        sa.Column('newsletter', sa.Boolean(), default=False, nullable=False, 
                  comment='Subscribe to newsletter'),
        sa.Column('marketing', sa.Boolean(), default=False, nullable=False, 
                  comment='Subscribe to marketing emails'),
        sa.Column('custom_settings', sa.JSON(), nullable=True, 
                  comment='Additional custom settings (JSON)'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), 
                  nullable=False, comment='Record creation timestamp (UTC)'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), 
                  onupdate=sa.func.now(), nullable=False, comment='Record update timestamp (UTC)'),
        comment='User preference settings table'
    )
    
    # Create indexes
    op.create_index('idx_user_preferences_profile_id', 'user_preferences', ['profile_id'])
    op.create_index('idx_user_preferences_language', 'user_preferences', ['language'])
    op.create_index('idx_user_preferences_timezone', 'user_preferences', ['timezone'])
    
    # Create user_sessions table
    op.create_table(
        'user_sessions',
        sa.Column('id', sa.String(36), primary_key=True, index=True),
        sa.Column('profile_id', sa.String(36), sa.ForeignKey('user_profiles.id', ondelete='CASCADE'), 
                  nullable=False, index=True, comment='Foreign key to user_profiles'),
        sa.Column('session_token', sa.String(255), nullable=False, unique=True, index=True, 
                  comment='Session token (JWT token ID)'),
        sa.Column('device_type', sa.String(20), nullable=False, 
                  comment='Device type (web/mobile/tablet/desktop)'),
        sa.Column('device_name', sa.String(100), nullable=True, 
                  comment='Device name or browser'),
        sa.Column('os', sa.String(50), nullable=True, comment='Operating system'),
        sa.Column('ip_address', sa.String(45), nullable=False, index=True, 
                  comment='Client IP address (IPv4/IPv6)'),
        sa.Column('user_agent', sa.Text(), nullable=True, comment='Full user agent string'),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False, index=True, 
                  comment='Session active status'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), 
                  nullable=False, comment='Session creation timestamp (UTC)'),
        sa.Column('last_activity_at', sa.DateTime(timezone=True), server_default=sa.func.now(), 
                  onupdate=sa.func.now(), nullable=False, comment='Last activity timestamp (UTC)'),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False, index=True, 
                  comment='Session expiration timestamp (UTC)'),
        sa.Column('logout_at', sa.DateTime(timezone=True), nullable=True, 
                  comment='Logout timestamp (UTC)'),
        comment='User session tracking table'
    )
    
    # Create indexes
    op.create_index('idx_user_sessions_profile_id', 'user_sessions', ['profile_id'])
    op.create_index('idx_user_sessions_session_token', 'user_sessions', ['session_token'])
    op.create_index('idx_user_sessions_is_active', 'user_sessions', ['is_active'])
    op.create_index('idx_user_sessions_expires_at', 'user_sessions', ['expires_at'])
    op.create_index('idx_user_sessions_ip_address', 'user_sessions', ['ip_address'])
    op.create_index('idx_user_sessions_device_type', 'user_sessions', ['device_type'])
    op.create_index('idx_user_sessions_profile_active', 'user_sessions', ['profile_id', 'is_active'])


def downgrade() -> None:
    op.drop_table('user_sessions')
    op.drop_table('user_preferences')
    op.drop_table('user_profiles')
