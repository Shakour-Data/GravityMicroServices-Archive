"""
Main FastAPI Application
"""

import inspect
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.config import settings
from app.core.database import engine, init_db
from app.core.exceptions import GravityException
from app.core.logging_config import setup_logging
from app.core.redis_client import get_redis_client, init_redis

# Setup logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("Starting application", service=settings.SERVICE_NAME)

    try:
        # Initialize database
        await init_db()
        logger.info("Database initialized")

        # Initialize Redis
        await init_redis()
        logger.info("Redis initialized")

        # Register with service discovery
        # await register_service()

        logger.info("Application started successfully")

        yield

    except Exception as e:
        logger.error("Failed to start application", error=str(e))
        raise

    finally:
        # Shutdown
        logger.info("Shutting down application")

        # Close database connections
        await engine.dispose()
        logger.info("Database connections closed")

        # Close Redis connections
        redis_client = await get_redis_client()
        await redis_client.close()
        logger.info("Redis connections closed")

        # Deregister from service discovery
        # await deregister_service()

        logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=f"Gravity {settings.SERVICE_NAME.title()} Service",
    description=f"Microservice for {settings.SERVICE_NAME}",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# Exception handlers
@app.exception_handler(GravityException)
async def gravity_exception_handler(request, exc: GravityException):
    """Handle custom Gravity exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": exc.error_code},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle general exceptions"""
    logger.error("Unhandled exception", error=str(exc), path=str(request.url))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error_code": "INTERNAL_ERROR"},
    )


# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "service": settings.SERVICE_NAME}


@app.get("/health/detailed", tags=["Health"])
async def detailed_health_check():
    """Detailed health check with dependencies"""
    health_status = {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": "1.0.0",
        "dependencies": {},
    }

    # Check database
    try:
        from app.core.database import get_db
        async for db in get_db():
            await db.execute(text("SELECT 1"))
            health_status["dependencies"]["database"] = "healthy"
            break
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        health_status["dependencies"]["database"] = "unhealthy"
        health_status["status"] = "degraded"

    # Check Redis
    try:
        redis = await get_redis_client()
        ping_result = redis.ping()
        if inspect.isawaitable(ping_result):
            await ping_result
        elif not ping_result:
            raise RuntimeError("Redis ping failed")
        health_status["dependencies"]["redis"] = "healthy"
    except Exception as e:
        logger.error("Redis health check failed", error=str(e))
        health_status["dependencies"]["redis"] = "unhealthy"
        health_status["status"] = "degraded"

    return health_status


# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to Gravity {settings.SERVICE_NAME.title()} Service",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.SERVICE_PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
