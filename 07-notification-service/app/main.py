"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - Notification Service
File         : main.py
Description  : FastAPI application entry point
Language     : English (UK)
Framework    : FastAPI 0.104+

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Dr. Sarah Chen (Chief Architect)
Contributors      : Marcus Chen (Backend Lead)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-09
Development Time  : 1 hours 0 minutes
Total Cost        : 1.0 × $150 = $150.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-09 - Dr. Sarah Chen - Initial application setup

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
================================================================================
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import settings
from app.core.database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events:
    - Initialize database connection
    - Register with service discovery
    - Setup monitoring
    """
    # Startup
    print("🚀 Starting Notification Service...")
    
    # Initialize database
    await init_db()
    print("✅ Database initialized")
    
    # TODO: Register with Consul
    # await register_service()
    # print(f"✅ Registered with Consul: {settings.SERVICE_NAME}")
    
    yield
    
    # Shutdown
    print("⏹️  Shutting down Notification Service...")
    
    # Close database
    await close_db()
    print("✅ Database connections closed")
    
    # TODO: Deregister from Consul
    # await deregister_service()
    # print("✅ Deregistered from Consul")


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Prometheus metrics
if settings.PROMETHEUS_ENABLED:
    Instrumentator().instrument(app).expose(app)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> JSONResponse:
    """
    Health check endpoint.
    
    Returns:
        Service health status
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "service": settings.SERVICE_NAME,
            "version": settings.API_VERSION,
            "port": settings.PORT,
        },
        status_code=200,
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root() -> JSONResponse:
    """
    Root endpoint with service information.
    
    Returns:
        Service information
    """
    return JSONResponse(
        content={
            "service": settings.APP_NAME,
            "version": settings.API_VERSION,
            "status": "running",
            "docs": f"http://{settings.HOST}:{settings.PORT}/docs",
            "features": {
                "email": True,
                "sms": settings.TWILIO_ENABLED,
                "push": settings.FIREBASE_ENABLED,
            },
        }
    )


# Include API routers
from app.api.v1 import email, templates, history, analytics

app.include_router(email.router, prefix=settings.API_V1_PREFIX)
app.include_router(templates.router, prefix=settings.API_V1_PREFIX)
app.include_router(history.router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics.router, prefix=settings.API_V1_PREFIX)

# TODO: Add remaining routers
# from app.api.v1 import sms, push
# app.include_router(sms.router, prefix=settings.API_V1_PREFIX, tags=["SMS"])
# app.include_router(push.router, prefix=settings.API_V1_PREFIX, tags=["Push"])


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
