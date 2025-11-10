"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - Notification Service
File         : test_email_provider.py
Description  : Email provider tests
Language     : English (UK)
Framework    : pytest / pytest-asyncio

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Marcus Chen (Backend & Integration Lead)
Contributors      : Dr. Sarah Chen (Chief Architect)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-09
Development Time  : 1 hour
Total Cost        : 1.0 × $150 = $150.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-09 - Marcus Chen - Initial email provider tests

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
================================================================================
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock

from app.providers.email_provider import EmailProvider


class TestEmailProvider:
    """Test suite for EmailProvider."""
    
    @pytest.fixture
    def email_provider(self):
        """Create email provider instance for testing."""
        return EmailProvider()
    
    def test_validate_email_address_valid(self, email_provider):
        """Test email validation with valid addresses."""
        assert email_provider.validate_email_address("user@example.com")
        assert email_provider.validate_email_address("test.user@subdomain.example.com")
        assert email_provider.validate_email_address("user+tag@example.com")
    
    def test_validate_email_address_invalid(self, email_provider):
        """Test email validation with invalid addresses."""
        assert not email_provider.validate_email_address("invalid")
        assert not email_provider.validate_email_address("@example.com")
        assert not email_provider.validate_email_address("user@")
        assert not email_provider.validate_email_address("")
    
    def test_create_message_plain_text(self, email_provider):
        """Test creating plain text email message."""
        message = email_provider.create_message(
            to="recipient@example.com",
            subject="Test Subject",
            content="Test content",
        )
        
        assert message["To"] == "recipient@example.com"
        assert message["Subject"] == "Test Subject"
        assert "Test content" in str(message)
    
    def test_create_message_html(self, email_provider):
        """Test creating HTML email message."""
        message = email_provider.create_message(
            to="recipient@example.com",
            subject="Test Subject",
            content="Plain text",
            html_content="<h1>HTML content</h1>",
        )
        
        assert message["To"] == "recipient@example.com"
        assert "<h1>HTML content</h1>" in str(message)
    
    def test_create_message_with_reply_to(self, email_provider):
        """Test creating message with reply-to header."""
        message = email_provider.create_message(
            to="recipient@example.com",
            subject="Test",
            content="Content",
            reply_to="reply@example.com",
        )
        
        assert message["Reply-To"] == "reply@example.com"
    
    @pytest.mark.asyncio
    async def test_send_email_success(self, email_provider):
        """Test successful email sending."""
        with patch("app.providers.email_provider.aiosmtplib.SMTP") as mock_smtp:
            # Setup mock
            mock_instance = AsyncMock()
            mock_smtp.return_value.__aenter__.return_value = mock_instance
            
            # Test
            result = await email_provider.send_email(
                to="test@example.com",
                subject="Test",
                content="Content",
            )
            
            assert result is True
            mock_instance.send_message.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_email_invalid_address(self, email_provider):
        """Test sending email to invalid address."""
        result = await email_provider.send_email(
            to="invalid-email",
            subject="Test",
            content="Content",
        )
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_send_email_smtp_error(self, email_provider):
        """Test email sending with SMTP error."""
        with patch("app.providers.email_provider.aiosmtplib.SMTP") as mock_smtp:
            # Setup mock to raise error
            mock_smtp.return_value.__aenter__.side_effect = Exception("SMTP error")
            
            # Test
            result = await email_provider.send_email(
                to="test@example.com",
                subject="Test",
                content="Content",
            )
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_send_bulk_emails_success(self, email_provider):
        """Test sending bulk emails successfully."""
        with patch.object(email_provider, "send_email") as mock_send:
            mock_send.return_value = True
            
            result = await email_provider.send_bulk_emails(
                recipients=["user1@example.com", "user2@example.com"],
                subject="Test",
                content="Content",
            )
            
            assert result["total"] == 2
            assert result["success"] == 2
            assert result["failed"] == 0
            assert len(result["failed_recipients"]) == 0
    
    @pytest.mark.asyncio
    async def test_send_bulk_emails_partial_failure(self, email_provider):
        """Test bulk sending with some failures."""
        with patch.object(email_provider, "send_email") as mock_send:
            # First succeeds, second fails
            mock_send.side_effect = [True, False]
            
            result = await email_provider.send_bulk_emails(
                recipients=["user1@example.com", "user2@example.com"],
                subject="Test",
                content="Content",
            )
            
            assert result["total"] == 2
            assert result["success"] == 1
            assert result["failed"] == 1
            assert "user2@example.com" in result["failed_recipients"]
    
    def test_render_template(self, email_provider):
        """Test template rendering."""
        # Mock Jinja2 environment
        with patch.object(email_provider, "jinja_env") as mock_env:
            mock_template = Mock()
            mock_template.render.return_value = "Rendered content"
            mock_env.get_template.return_value = mock_template
            
            result = email_provider.render_template(
                template_name="test.html",
                variables={"name": "John"},
            )
            
            assert result == "Rendered content"
            mock_env.get_template.assert_called_once_with("test.html")
            mock_template.render.assert_called_once_with(name="John")
    
    def test_render_template_not_initialized(self, email_provider):
        """Test rendering when template environment not initialized."""
        email_provider.jinja_env = None
        
        with pytest.raises(ValueError, match="Template environment not initialized"):
            email_provider.render_template("test.html", {})


class TestEmailProviderIntegration:
    """Integration tests for EmailProvider (requires SMTP server)."""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_send_real_email(self):
        """Test sending real email (skipped in CI)."""
        # This test requires actual SMTP credentials
        # Skip in CI/CD pipeline
        pytest.skip("Integration test requires SMTP server")
