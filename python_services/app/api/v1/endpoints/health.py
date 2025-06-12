"""
Health check API endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import structlog

from app.core.database import get_database_session, get_supabase_client
from app.services.ai_service import AIService

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "service": "Chief-of-Flow API",
        "message": "Service is running"
    }


@router.get("/detailed")
async def detailed_health_check(
    db: AsyncSession = Depends(get_database_session)
):
    """Detailed health check including dependencies."""
    health_status = {
        "status": "healthy",
        "service": "Chief-of-Flow API",
        "checks": {}
    }
    
    # Check database connection
    try:
        await db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = "connected"
    except Exception as e:
        health_status["checks"]["database"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check Supabase connection
    try:
        supabase = get_supabase_client()
        if supabase:
            # Try a simple query
            supabase.table("projects").select("id").limit(1).execute()
            health_status["checks"]["supabase"] = "connected"
        else:
            health_status["checks"]["supabase"] = "not configured"
    except Exception as e:
        health_status["checks"]["supabase"] = f"error: {str(e)}"
    
    # Check AI service
    try:
        ai_service = AIService()
        health_status["checks"]["ai_service"] = {
            "openai_available": ai_service.client is not None,
            "status": "ready"
        }
    except Exception as e:
        health_status["checks"]["ai_service"] = f"error: {str(e)}"
    
    return health_status 