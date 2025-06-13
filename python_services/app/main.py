"""
Main FastAPI application for Chief-of-Flow services.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
import structlog
import os

from app.core.config import settings
from app.core.database import get_database_session, get_supabase_client
from app.api.v1.api import api_router

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# DIAGNOSTIC: Print configuration values at startup
print("=" * 60)
print("DIAGNOSTIC: Configuration Values at Startup")
print("=" * 60)
print(f"DATABASE_URL from os.environ: {os.environ.get('DATABASE_URL', 'NOT SET')}")
print(f"DATABASE_URL from settings: {settings.database_url}")
print(f"SUPABASE_URL from settings: {settings.supabase_url}")
print(f"SUPABASE_ANON_KEY from settings: {settings.supabase_anon_key[:20]}..." if settings.supabase_anon_key else "NOT SET")
print(f"SUPABASE_SERVICE_ROLE_KEY from settings: {settings.supabase_service_role_key[:20]}..." if settings.supabase_service_role_key else "NOT SET")
print(f"Debug mode: {settings.debug}")
print("=" * 60)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered personal task management and scheduling system",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("Starting Chief-of-Flow API", version=settings.app_version)


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Shutting down Chief-of-Flow API")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Chief-of-Flow API",
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
async def health_check(
    db=Depends(get_database_session),
    supabase=Depends(get_supabase_client)
):
    """Health check endpoint."""
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
        
        # Test Supabase connection
        if supabase:
            supabase.table("projects").select("id").limit(1).execute()
            supabase_status = "connected"
        else:
            supabase_status = "not configured"
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "database": "connected",
                "supabase": supabase_status,
                "timestamp": structlog.stdlib.get_logger().info("health_check_passed")
            }
        )
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": structlog.stdlib.get_logger().error("health_check_failed")
            }
        )


# Include API routers
app.include_router(api_router, prefix=settings.api_v1_str)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 