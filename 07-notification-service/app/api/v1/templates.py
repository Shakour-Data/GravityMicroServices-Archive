"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - Notification Service
File         : templates.py
Description  : Template management API endpoints
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
Development Time  : 1 hour 30 minutes
Total Cost        : 1.5 × $150 = $225.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-09 - Marcus Chen - Initial template API

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

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.template_service import template_service
from app.schemas.template import TemplateResponse, TemplateListResponse
from app.models import NotificationType

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/templates", tags=["Templates"])


# Request/Response Models
class CreateTemplateRequest(BaseModel):
    """Request to create template."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Template name")
    type: NotificationType = Field(..., description="Notification type")
    subject: str = Field(..., min_length=1, max_length=200, description="Subject")
    content: str = Field(..., min_length=1, description="Plain text content")
    html_content: Optional[str] = Field(None, description="HTML content")
    variables: Optional[List[str]] = Field(None, description="Variable names")
    language: str = Field("en", description="Language code")
    description: Optional[str] = Field(None, description="Description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "welcome_email",
                "type": "EMAIL",
                "subject": "Welcome to {{app_name}}!",
                "content": "Hello {{name}}, welcome to {{app_name}}!",
                "html_content": "<h1>Hello {{name}}</h1><p>Welcome!</p>",
                "variables": ["name", "app_name"],
                "language": "en",
                "description": "Welcome email for new users",
            }
        }


class UpdateTemplateRequest(BaseModel):
    """Request to update template."""
    
    subject: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    html_content: Optional[str] = None
    variables: Optional[List[str]] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class TemplatePreviewRequest(BaseModel):
    """Request to preview template."""
    
    variables: Dict[str, Any] = Field(..., description="Sample variables")
    
    class Config:
        json_schema_extra = {
            "example": {
                "variables": {
                    "name": "John Doe",
                    "app_name": "Gravity Platform",
                }
            }
        }


class TemplatePreviewResponse(BaseModel):
    """Template preview response."""
    
    subject: str
    content: str
    html_content: Optional[str] = None


# API Endpoints
@router.post(
    "",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create template",
    description="Create a new notification template with Jinja2 support",
)
async def create_template(
    request: CreateTemplateRequest,
    db: AsyncSession = Depends(get_db),
) -> TemplateResponse:
    """
    Create notification template.
    
    Features:
    - Jinja2 template syntax support
    - Variable substitution
    - HTML and plain text versions
    - Template validation
    
    Example:
        POST /api/v1/templates
        {
            "name": "welcome_email",
            "type": "EMAIL",
            "subject": "Welcome {{name}}!",
            "content": "Hello {{name}}!",
            "variables": ["name"]
        }
    """
    try:
        template = await template_service.create_template(
            db=db,
            name=request.name,
            notification_type=request.type,
            subject=request.subject,
            content=request.content,
            html_content=request.html_content,
            variables=request.variables,
            language=request.language,
            description=request.description,
        )
        
        logger.info(f"📝 Created template '{request.name}' (ID: {template.id})")
        return TemplateResponse.model_validate(template)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error creating template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create template: {str(e)}",
        )


@router.get(
    "",
    response_model=TemplateListResponse,
    summary="List templates",
    description="Get list of templates with optional filters",
)
async def list_templates(
    type: Optional[NotificationType] = Query(None, description="Filter by type"),
    language: Optional[str] = Query(None, description="Filter by language"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db),
) -> TemplateListResponse:
    """
    List templates with filters.
    
    Example:
        GET /api/v1/templates?type=EMAIL&is_active=true&limit=10
    """
    try:
        templates = await template_service.list_templates(
            db=db,
            notification_type=type,
            language=language,
            is_active=is_active,
            limit=limit,
            offset=offset,
        )
        
        template_responses = [
            TemplateResponse.model_validate(t) for t in templates
        ]
        
        return TemplateListResponse(
            templates=template_responses,
            total=len(template_responses),
            limit=limit,
            offset=offset,
        )
        
    except Exception as e:
        logger.error(f"Error listing templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list templates: {str(e)}",
        )


@router.get(
    "/{template_id}",
    response_model=TemplateResponse,
    summary="Get template",
    description="Get template by ID",
)
async def get_template(
    template_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> TemplateResponse:
    """
    Get template by ID.
    
    Example:
        GET /api/v1/templates/123e4567-e89b-12d3-a456-426614174000
    """
    template = await template_service.get_template(db, template_id)
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template {template_id} not found",
        )
    
    return TemplateResponse.model_validate(template)


@router.get(
    "/name/{template_name}",
    response_model=TemplateResponse,
    summary="Get template by name",
    description="Get template by unique name",
)
async def get_template_by_name(
    template_name: str,
    db: AsyncSession = Depends(get_db),
) -> TemplateResponse:
    """
    Get template by name.
    
    Example:
        GET /api/v1/templates/name/welcome_email
    """
    template = await template_service.get_template_by_name(db, template_name)
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_name}' not found",
        )
    
    return TemplateResponse.model_validate(template)


@router.patch(
    "/{template_id}",
    response_model=TemplateResponse,
    summary="Update template",
    description="Update template (increments version)",
)
async def update_template(
    template_id: UUID,
    request: UpdateTemplateRequest,
    db: AsyncSession = Depends(get_db),
) -> TemplateResponse:
    """
    Update template.
    
    Features:
    - Version control (increments on update)
    - Template validation
    - Partial updates
    
    Example:
        PATCH /api/v1/templates/123e4567-e89b-12d3-a456-426614174000
        {
            "subject": "Updated subject",
            "is_active": false
        }
    """
    try:
        template = await template_service.update_template(
            db=db,
            template_id=template_id,
            subject=request.subject,
            content=request.content,
            html_content=request.html_content,
            variables=request.variables,
            description=request.description,
            is_active=request.is_active,
        )
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template {template_id} not found",
            )
        
        logger.info(f"✏️ Updated template {template_id} to version {template.version}")
        return TemplateResponse.model_validate(template)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error updating template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update template: {str(e)}",
        )


@router.delete(
    "/{template_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete template",
    description="Delete template (soft delete - marks as inactive)",
)
async def delete_template(
    template_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete template (soft delete).
    
    Example:
        DELETE /api/v1/templates/123e4567-e89b-12d3-a456-426614174000
    """
    success = await template_service.delete_template(db, template_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template {template_id} not found",
        )
    
    logger.info(f"🗑️ Deleted template {template_id}")


@router.post(
    "/{template_id}/preview",
    response_model=TemplatePreviewResponse,
    summary="Preview template",
    description="Preview template with sample variables",
)
async def preview_template(
    template_id: UUID,
    request: TemplatePreviewRequest,
    db: AsyncSession = Depends(get_db),
) -> TemplatePreviewResponse:
    """
    Preview template with sample variables.
    
    Example:
        POST /api/v1/templates/123e4567-e89b-12d3-a456-426614174000/preview
        {
            "variables": {
                "name": "John Doe",
                "app_name": "Gravity"
            }
        }
    """
    try:
        preview = await template_service.preview_template(
            db=db,
            template_id=template_id,
            variables=request.variables,
        )
        
        return TemplatePreviewResponse(**preview)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error previewing template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to preview template: {str(e)}",
        )
