"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - Notification Service
File         : template_service.py
Description  : Template management service
Language     : English (UK)
Framework    : SQLAlchemy 2.0 / Jinja2

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
v1.0.0 - 2025-11-09 - Marcus Chen - Initial template service

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
================================================================================
"""

import logging
from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from jinja2 import Template as Jinja2Template, TemplateSyntaxError

from app.models import Template, NotificationType

logger = logging.getLogger(__name__)


class TemplateService:
    """
    Service for managing notification templates.
    
    Handles:
    - CRUD operations for templates
    - Template rendering with Jinja2
    - Template versioning
    - Template validation
    """
    
    async def create_template(
        self,
        db: AsyncSession,
        name: str,
        notification_type: NotificationType,
        subject: str,
        content: str,
        html_content: Optional[str] = None,
        variables: Optional[List[str]] = None,
        language: str = "en",
        description: Optional[str] = None,
    ) -> Template:
        """
        Create a new notification template.
        
        Args:
            db: Database session
            name: Template name (unique)
            notification_type: Type of notification
            subject: Template subject
            content: Plain text template
            html_content: HTML template
            variables: List of variable names
            language: Template language
            description: Template description
            
        Returns:
            Created template
            
        Raises:
            ValueError: If template already exists or validation fails
        """
        # Check if template exists
        existing = await self.get_template_by_name(db, name)
        if existing:
            raise ValueError(f"Template '{name}' already exists")
        
        # Validate template syntax
        self._validate_template_syntax(content)
        if html_content:
            self._validate_template_syntax(html_content)
        
        # Create template
        template = Template(
            name=name,
            type=notification_type,
            subject=subject,
            content=content,
            html_content=html_content,
            variables=variables or [],
            language=language,
            description=description,
            version=1,
            is_active=True,
        )
        
        db.add(template)
        await db.commit()
        await db.refresh(template)
        
        logger.info(f"📝 Created template '{name}' (ID: {template.id})")
        return template
    
    def _validate_template_syntax(self, template_content: str) -> None:
        """
        Validate Jinja2 template syntax.
        
        Args:
            template_content: Template content to validate
            
        Raises:
            ValueError: If template syntax is invalid
        """
        try:
            Jinja2Template(template_content)
        except TemplateSyntaxError as e:
            raise ValueError(f"Invalid template syntax: {e}")
    
    async def get_template(
        self,
        db: AsyncSession,
        template_id: UUID,
    ) -> Optional[Template]:
        """
        Get template by ID.
        
        Args:
            db: Database session
            template_id: Template ID
            
        Returns:
            Template or None
        """
        result = await db.execute(
            select(Template).where(Template.id == template_id)
        )
        return result.scalar_one_or_none()
    
    async def get_template_by_name(
        self,
        db: AsyncSession,
        name: str,
    ) -> Optional[Template]:
        """
        Get template by name.
        
        Args:
            db: Database session
            name: Template name
            
        Returns:
            Template or None
        """
        result = await db.execute(
            select(Template).where(Template.name == name)
        )
        return result.scalar_one_or_none()
    
    async def list_templates(
        self,
        db: AsyncSession,
        notification_type: Optional[NotificationType] = None,
        language: Optional[str] = None,
        is_active: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Template]:
        """
        List templates with filters.
        
        Args:
            db: Database session
            notification_type: Filter by type
            language: Filter by language
            is_active: Filter by active status
            limit: Maximum results
            offset: Pagination offset
            
        Returns:
            List of templates
        """
        query = select(Template)
        
        if notification_type:
            query = query.where(Template.type == notification_type)
        
        if language:
            query = query.where(Template.language == language)
        
        if is_active is not None:
            query = query.where(Template.is_active == is_active)
        
        query = query.order_by(Template.created_at.desc())
        query = query.limit(limit).offset(offset)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def update_template(
        self,
        db: AsyncSession,
        template_id: UUID,
        subject: Optional[str] = None,
        content: Optional[str] = None,
        html_content: Optional[str] = None,
        variables: Optional[List[str]] = None,
        description: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Optional[Template]:
        """
        Update template.
        
        Args:
            db: Database session
            template_id: Template ID
            subject: New subject
            content: New plain text content
            html_content: New HTML content
            variables: New variables list
            description: New description
            is_active: New active status
            
        Returns:
            Updated template or None
        """
        template = await self.get_template(db, template_id)
        if not template:
            return None
        
        # Validate new template content
        if content:
            self._validate_template_syntax(content)
            template.content = content
        
        if html_content:
            self._validate_template_syntax(html_content)
            template.html_content = html_content
        
        # Update other fields
        if subject is not None:
            template.subject = subject
        
        if variables is not None:
            template.variables = variables
        
        if description is not None:
            template.description = description
        
        if is_active is not None:
            template.is_active = is_active
        
        # Increment version
        template.version += 1
        
        await db.commit()
        await db.refresh(template)
        
        logger.info(f"✏️ Updated template {template_id} to version {template.version}")
        return template
    
    async def delete_template(
        self,
        db: AsyncSession,
        template_id: UUID,
    ) -> bool:
        """
        Delete template (soft delete by marking inactive).
        
        Args:
            db: Database session
            template_id: Template ID
            
        Returns:
            True if deleted, False if not found
        """
        template = await self.get_template(db, template_id)
        if not template:
            return False
        
        template.is_active = False
        await db.commit()
        
        logger.info(f"🗑️ Deactivated template {template_id}")
        return True
    
    def render_template(
        self,
        template: Template,
        variables: Dict[str, Any],
        use_html: bool = False,
    ) -> str:
        """
        Render template with variables.
        
        Args:
            template: Template to render
            variables: Variables to substitute
            use_html: Use HTML content instead of plain text
            
        Returns:
            Rendered template content
            
        Example:
            template = await service.get_template(db, template_id)
            rendered = service.render_template(
                template,
                {"name": "John", "url": "https://example.com"}
            )
        """
        content = template.html_content if use_html else template.content
        
        if not content:
            content = template.content  # Fallback to plain text
        
        try:
            jinja_template = Jinja2Template(content)
            return jinja_template.render(**variables)
        except Exception as e:
            logger.error(f"Error rendering template {template.id}: {e}")
            raise
    
    def render_subject(
        self,
        template: Template,
        variables: Dict[str, Any],
    ) -> str:
        """
        Render template subject with variables.
        
        Args:
            template: Template
            variables: Variables to substitute
            
        Returns:
            Rendered subject
        """
        try:
            jinja_template = Jinja2Template(template.subject)
            return jinja_template.render(**variables)
        except Exception as e:
            logger.error(f"Error rendering template subject {template.id}: {e}")
            raise
    
    async def preview_template(
        self,
        db: AsyncSession,
        template_id: UUID,
        variables: Dict[str, Any],
    ) -> Dict[str, str]:
        """
        Preview template with sample variables.
        
        Args:
            db: Database session
            template_id: Template ID
            variables: Sample variables
            
        Returns:
            Dict with rendered subject, content, and html_content
        """
        template = await self.get_template(db, template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        preview = {
            "subject": self.render_subject(template, variables),
            "content": self.render_template(template, variables, use_html=False),
        }
        
        if template.html_content:
            preview["html_content"] = self.render_template(
                template, variables, use_html=True
            )
        
        return preview


# Create global instance
template_service = TemplateService()
