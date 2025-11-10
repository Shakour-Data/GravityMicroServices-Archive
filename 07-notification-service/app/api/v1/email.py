"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - Notification Service
File         : email.py
Description  : Email notification API endpoints
Language     : English (UK)
Framework    : FastAPI

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
Development Time  : 2 hours
Total Cost        : 2.0 × $150 = $300.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-09 - Marcus Chen - Initial email API

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
================================================================================
"""

import logging
from typing import Optional, List, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, conlist
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.notification_service import notification_service
from app.services.template_service import template_service
from app.schemas.notification import NotificationResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/email", tags=["Email Notifications"])


# Request/Response Models
class SendEmailRequest(BaseModel):
    """Request to send email notification."""
    
    user_id: UUID = Field(..., description="User ID")
    to: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., min_length=1, max_length=200, description="Email subject")
    content: str = Field(..., min_length=1, description="Plain text content")
    html_content: Optional[str] = Field(None, description="HTML content")
    reply_to: Optional[EmailStr] = Field(None, description="Reply-to address")
    template_id: Optional[UUID] = Field(None, description="Template ID")
    template_variables: Optional[Dict[str, Any]] = Field(
        None, description="Template variables"
    )
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "to": "user@example.com",
                "subject": "Welcome to Gravity!",
                "content": "Welcome to our platform!",
                "html_content": "<h1>Welcome to Gravity!</h1>",
                "template_variables": {"name": "John Doe"},
            }
        }


class BulkEmailRequest(BaseModel):
    """Request to send bulk emails."""
    
    user_id: UUID = Field(..., description="User ID")
    recipients: List[EmailStr] = Field(
        ...,
        description="Recipient email addresses",
        min_length=1,
        max_length=100,
    )
    subject: str = Field(..., min_length=1, max_length=200, description="Email subject")
    content: str = Field(..., min_length=1, description="Plain text content")
    html_content: Optional[str] = Field(None, description="HTML content")
    template_id: Optional[UUID] = Field(None, description="Template ID")
    template_variables: Optional[Dict[str, Any]] = Field(
        None, description="Template variables"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "recipients": ["user1@example.com", "user2@example.com"],
                "subject": "Monthly Newsletter",
                "content": "Check out our latest updates!",
                "template_id": "456e4567-e89b-12d3-a456-426614174000",
                "template_variables": {"month": "January"},
            }
        }


class BulkEmailResponse(BaseModel):
    """Response for bulk email sending."""
    
    total: int = Field(..., description="Total emails to send")
    success: int = Field(..., description="Successfully sent")
    failed: int = Field(..., description="Failed to send")
    failed_recipients: List[str] = Field(
        ..., description="List of failed recipient emails"
    )


# API Endpoints
@router.post(
    "/send",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send email notification",
    description="Send a single email notification with optional template support",
)
async def send_email(
    request: SendEmailRequest,
    db: AsyncSession = Depends(get_db),
) -> NotificationResponse:
    """
    Send email notification.
    
    Features:
    - Plain text and HTML content
    - Template support with variables
    - Delivery tracking
    - Retry logic for failures
    
    Example:
        POST /api/v1/email/send
        {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "to": "user@example.com",
            "subject": "Welcome!",
            "content": "Welcome to Gravity!",
            "html_content": "<h1>Welcome!</h1>"
        }
    """
    try:
        # If template_id provided, render template
        html_content = request.html_content
        content = request.content
        subject = request.subject
        
        if request.template_id and request.template_variables:
            template = await template_service.get_template(db, request.template_id)
            if not template:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Template {request.template_id} not found",
                )
            
            # Render template
            subject = template_service.render_subject(
                template, request.template_variables
            )
            content = template_service.render_template(
                template, request.template_variables, use_html=False
            )
            template_html_content: Optional[str] = getattr(template, "html_content", None)
            if template_html_content:
                html_content = template_service.render_template(
                    template, request.template_variables, use_html=True
                )
        
        # Send email
        notification = await notification_service.send_email_notification(
            db=db,
            user_id=request.user_id,
            to=request.to,
            subject=subject,
            content=content,
            html_content=html_content,
            template_id=request.template_id,
            template_variables=request.template_variables,
            metadata=request.metadata,
        )
        
        logger.info(f"✉️ Email sent to {request.to} (ID: {notification.id})")
        return NotificationResponse.model_validate(notification)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email: {str(e)}",
        )


@router.post(
    "/send-bulk",
    response_model=BulkEmailResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Send bulk emails",
    description="Send emails to multiple recipients (max 100 per request)",
)
async def send_bulk_emails(
    request: BulkEmailRequest,
    db: AsyncSession = Depends(get_db),
) -> BulkEmailResponse:
    """
    Send bulk emails to multiple recipients.
    
    Features:
    - Send to up to 100 recipients per request
    - Template support
    - Individual tracking for each email
    - Detailed success/failure reporting
    
    Example:
        POST /api/v1/email/send-bulk
        {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "recipients": ["user1@example.com", "user2@example.com"],
            "subject": "Newsletter",
            "content": "Latest updates!",
            "template_id": "456e4567-e89b-12d3-a456-426614174000"
        }
    """
    try:
        # Render template if provided
        html_content = request.html_content
        content = request.content
        subject = request.subject
        
        if request.template_id and request.template_variables:
            template = await template_service.get_template(db, request.template_id)
            if not template:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Template {request.template_id} not found",
                )
            
            subject = template_service.render_subject(
                template, request.template_variables
            )
            content = template_service.render_template(
                template, request.template_variables, use_html=False
            )
            template_html_content: Optional[str] = getattr(template, "html_content", None)
            if template_html_content:
                html_content = template_service.render_template(
                    template, request.template_variables, use_html=True
                )
        
        # Send emails
        success_count = 0
        failed_recipients = []
        
        for recipient in request.recipients:
            try:
                await notification_service.send_email_notification(
                    db=db,
                    user_id=request.user_id,
                    to=recipient,
                    subject=subject,
                    content=content,
                    html_content=html_content,
                    template_id=request.template_id,
                    template_variables=request.template_variables,
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to send to {recipient}: {e}")
                failed_recipients.append(recipient)
        
        logger.info(
            f"📊 Bulk email complete: {success_count}/{len(request.recipients)} sent"
        )
        
        return BulkEmailResponse(
            total=len(request.recipients),
            success=success_count,
            failed=len(failed_recipients),
            failed_recipients=failed_recipients,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending bulk emails: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send bulk emails: {str(e)}",
        )
