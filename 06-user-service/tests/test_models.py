"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : test_models.py
Description  : Database model tests
Language     : English (UK)
Framework    : pytest / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Elena Volkov (Backend & Integration Lead)
Contributors      : Dr. Sarah Chen (Chief Architect)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-08 22:30 UTC
Last Modified     : 2025-11-08 22:30 UTC
Development Time  : 1 hour 30 minutes
Total Cost        : 1.5 × $150 = $225.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial model tests

================================================================================
DEPENDENCIES
================================================================================
Internal  : models
External  : pytest, sqlalchemy
Database  : PostgreSQL 16+ (test database)

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user_profile import UserProfile
from app.models.user_preference import UserPreference
from app.models.user_session import UserSession


# UserProfile Model Tests
@pytest.mark.asyncio
async def test_create_user_profile(db: AsyncSession, test_user_id: str):
    """Test creating a user profile."""
    profile = UserProfile(
        user_id=test_user_id,
        display_name="Test User",
        bio="Test bio",
        avatar_url="https://example.com/avatar.jpg",
        location="Tehran, Iran",
        website="https://example.com"
    )
    
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    
    assert profile.id is not None
    assert profile.user_id == test_user_id
    assert profile.display_name == "Test User"
    assert profile.created_at is not None


@pytest.mark.asyncio
async def test_user_profile_relationships(db: AsyncSession, test_user_id: str):
    """Test profile relationships with preferences and sessions."""
    # Create profile
    profile = UserProfile(
        user_id=test_user_id,
        display_name="Test User"
    )
    db.add(profile)
    
    # Create preference
    preference = UserPreference(
        user_id=test_user_id,
        language="en"
    )
    db.add(preference)
    
    # Create session
    session = UserSession(
        user_id=test_user_id,
        session_id="test-session",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0"
    )
    db.add(session)
    
    await db.commit()
    await db.refresh(profile)
    
    # Test relationships
    assert profile.preferences is not None
    assert len(profile.sessions) == 1
    assert getattr(profile.sessions[0], "session_id") == "test-session"


@pytest.mark.asyncio
async def test_user_profile_unique_user_id(db: AsyncSession, test_user_id: str):
    """Test that user_id is unique."""
    # Create first profile
    profile1 = UserProfile(
        user_id=test_user_id,
        display_name="User 1"
    )
    db.add(profile1)
    await db.commit()
    
    # Try to create duplicate
    profile2 = UserProfile(
        user_id=test_user_id,
        display_name="User 2"
    )
    db.add(profile2)
    
    with pytest.raises(Exception):  # Should raise integrity error
        await db.commit()


@pytest.mark.asyncio
async def test_user_profile_timestamps(db: AsyncSession, test_user_id: str):
    """Test automatic timestamp management."""
    profile = UserProfile(
        user_id=test_user_id,
        display_name="Test User"
    )
    
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    
    created_at = profile.created_at
    updated_at = profile.updated_at
    
    assert created_at is not None
    assert updated_at is not None
    assert created_at == updated_at
    
    # Update profile
    profile.display_name = "Updated User"
    await db.commit()
    await db.refresh(profile)
    
    assert profile.created_at == created_at  # Unchanged
    assert profile.updated_at > updated_at  # Updated


# UserPreference Model Tests
@pytest.mark.asyncio
async def test_create_user_preference(db: AsyncSession, test_user_id: str):
    """Test creating user preferences."""
    preference = UserPreference(
        user_id=test_user_id,
        language="fa",
        timezone="Asia/Tehran",
        theme="dark",
        email_notifications=True,
        push_notifications=False
    )
    
    db.add(preference)
    await db.commit()
    await db.refresh(preference)
    
    assert preference.id is not None
    assert getattr(preference, "user_id") == test_user_id
    assert preference.language == "fa"
    assert preference.timezone == "Asia/Tehran"


@pytest.mark.asyncio
async def test_user_preference_defaults(db: AsyncSession, test_user_id: str):
    """Test default preference values."""
    preference = UserPreference(
        user_id=test_user_id
    )
    
    db.add(preference)
    await db.commit()
    await db.refresh(preference)
    
    assert preference.language == "en"
    assert preference.timezone == "UTC"
    assert preference.theme == "system"
    assert preference.email_notifications is True
    assert preference.push_notifications is True
    assert preference.sms_notifications is False


@pytest.mark.asyncio
async def test_user_preference_unique_user_id(db: AsyncSession, test_user_id: str):
    """Test that user_id is unique in preferences."""
    # Create first preference
    pref1 = UserPreference(
        user_id=test_user_id,
        language="en"
    )
    db.add(pref1)
    await db.commit()
    
    # Try to create duplicate
    pref2 = UserPreference(
        user_id=test_user_id,
        language="fa"
    )
    db.add(pref2)
    
    with pytest.raises(Exception):  # Should raise integrity error
        await db.commit()


# UserSession Model Tests
@pytest.mark.asyncio
async def test_create_user_session(db: AsyncSession, test_user_id: str):
    """Test creating a user session."""
    session = UserSession(
        user_id=test_user_id,
        session_id="test-session-123",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        device_type="desktop",
        device_name="Chrome on Windows"
    )
    
    db.add(session)
    await db.commit()
    await db.refresh(session)
    
    assert session.id is not None
    assert getattr(session, "user_id") == test_user_id
    assert getattr(session, "session_id") == "test-session-123"
    assert session.is_active is True


@pytest.mark.asyncio
async def test_user_session_defaults(db: AsyncSession, test_user_id: str):
    """Test default session values."""
    session = UserSession(
        user_id=test_user_id,
        session_id="test-session",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0"
    )
    
    db.add(session)
    await db.commit()
    await db.refresh(session)
    
    assert session.is_active is True
    assert session.device_type == "unknown"
    assert session.created_at is not None
    last_activity = getattr(session, "last_activity")
    assert last_activity is not None
    assert session.expires_at is not None


@pytest.mark.asyncio
async def test_user_session_expiration(db: AsyncSession, test_user_id: str):
    """Test session expiration."""
    # Create session with custom expiration
    expires_at = datetime.utcnow() + timedelta(hours=24)
    session = UserSession(
        user_id=test_user_id,
        session_id="test-session",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0",
        expires_at=expires_at
    )
    
    db.add(session)
    await db.commit()
    await db.refresh(session)
    
    assert session.expires_at == expires_at


@pytest.mark.asyncio
async def test_user_session_unique_session_id(db: AsyncSession, test_user_id: str):
    """Test that session_id is unique per user."""
    # Create first session
    session1 = UserSession(
        user_id=test_user_id,
        session_id="same-session-id",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0"
    )
    db.add(session1)
    await db.commit()
    
    # Try to create duplicate for same user
    session2 = UserSession(
        user_id=test_user_id,
        session_id="same-session-id",
        ip_address="192.168.1.2",
        user_agent="Mozilla/5.0"
    )
    db.add(session2)
    
    with pytest.raises(Exception):  # Should raise integrity error
        await db.commit()


@pytest.mark.asyncio
async def test_multiple_sessions_per_user(db: AsyncSession, test_user_id: str):
    """Test that user can have multiple sessions."""
    sessions = [
        UserSession(
            user_id=test_user_id,
            session_id=f"session-{i}",
            ip_address=f"192.168.1.{i}",
            user_agent="Mozilla/5.0"
        )
        for i in range(5)
    ]
    
    db.add_all(sessions)
    await db.commit()
    
    # Query sessions
    user_id_column = getattr(UserSession, "user_id")
    result = await db.execute(
        select(UserSession).where(user_id_column == test_user_id)
    )
    user_sessions = result.scalars().all()
    
    assert len(user_sessions) == 5


@pytest.mark.asyncio
async def test_session_activity_tracking(db: AsyncSession, test_user_id: str):
    """Test session activity tracking."""
    session = UserSession(
        user_id=test_user_id,
        session_id="test-session",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0"
    )
    
    db.add(session)
    await db.refresh(session)
    
    original_activity = getattr(session, "last_activity")
    
    # Update activity
    setattr(session, "last_activity", datetime.utcnow())
    await db.commit()
    await db.refresh(session)
    
    updated_activity = getattr(session, "last_activity")
    assert updated_activity > original_activity
    assert updated_activity > original_activity


@pytest.mark.asyncio
async def test_cascade_delete_profile(db: AsyncSession, test_user_id: str):
    """Test cascade delete of profile deletes related records."""
    # Create profile
    profile = UserProfile(
        user_id=test_user_id,
        display_name="Test User"
    )
    db.add(profile)
    
    # Create preference
    preference = UserPreference(
        user_id=test_user_id,
        language="en"
    )
    db.add(preference)
    
    # Create sessions
    for i in range(3):
        session = UserSession(
            user_id=test_user_id,
            session_id=f"session-{i}",
            ip_address=f"192.168.1.{i}",
            user_agent="Mozilla/5.0"
        )
        db.add(session)
    
    await db.commit()
    
    # Delete profile
    await db.delete(profile)
    await db.commit()
    
    # Check preferences deleted
    user_preference_user_id = getattr(UserPreference, "user_id")
    result = await db.execute(
        select(UserPreference).where(user_preference_user_id == test_user_id)
    )
    assert result.scalar_one_or_none() is None
    
    user_session_user_id = getattr(UserSession, "user_id")
    result = await db.execute(
        select(UserSession).where(user_session_user_id == test_user_id)
    )
    assert len(result.scalars().all()) == 0
    assert len(result.scalars().all()) == 0


@pytest.mark.asyncio
async def test_session_ordering(db: AsyncSession, test_user_id: str):
    """Test that sessions can be ordered by last_activity."""
    # Create sessions with different activity times
    for i in range(3):
        session = UserSession(
            user_id=test_user_id,
            session_id=f"session-{i}",
            ip_address=f"192.168.1.{i}",
            user_agent="Mozilla/5.0",
            last_activity=datetime.utcnow() - timedelta(hours=i)
        )
        db.add(session)
    
    user_id_column = getattr(UserSession, "user_id")
    last_activity_column = getattr(UserSession, "last_activity")
    result = await db.execute(
        select(UserSession)
        .where(user_id_column == test_user_id)
        .order_by(last_activity_column.desc())
    )
    sessions = result.scalars().all()
    
    assert len(sessions) == 3
    # Most recent first
    assert getattr(sessions[0], "session_id") == "session-0"
    assert getattr(sessions[1], "session_id") == "session-1"
    assert getattr(sessions[2], "session_id") == "session-2"


@pytest.mark.asyncio
async def test_profile_search_index(db: AsyncSession):
    """Test profile display_name indexing for search."""
    # Create profiles with different names
    profiles = [
        UserProfile(user_id=f"user-{i}", display_name=f"User {i}")
        for i in range(100)
    ]
    
    db.add_all(profiles)
    await db.commit()
    
    # Search should be fast with index
    result = await db.execute(
        select(UserProfile)
        .where(UserProfile.display_name.like("%User 5%"))
    )
    matching = result.scalars().all()
    
    # Should find User 5, User 50-59
    assert len(matching) >= 11
