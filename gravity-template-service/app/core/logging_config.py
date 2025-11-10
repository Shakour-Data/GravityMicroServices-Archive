"""
Structured Logging Configuration
Uses structlog for structured logging
"""

import logging
import sys
from pathlib import Path
from typing import Any

import structlog

from app.config import settings


def setup_logging() -> Any:
    """
    Setup structured logging with structlog

    Returns:
        Configured logger
    """
    # Create logs directory if it doesn't exist
    log_file = Path(settings.LOG_FILE_PATH)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Configure structlog processors
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # Add JSON or console renderer based on format
    if settings.LOG_FORMAT == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL),
    )

    # Configure file handler with rotation
    if not settings.is_development:
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(
            settings.LOG_FILE_PATH,
            maxBytes=settings.LOG_FILE_MAX_SIZE,
            backupCount=settings.LOG_FILE_BACKUP_COUNT,
        )
        file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
        logging.root.addHandler(file_handler)

    # Get logger
    logger = structlog.get_logger(settings.SERVICE_NAME)

    return logger


# Create default logger
logger = setup_logging()
