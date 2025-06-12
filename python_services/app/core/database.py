"""
Database configuration and session management for Supabase PostgreSQL.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import structlog
from app.core.config import settings

logger = structlog.get_logger(__name__)

# SQLAlchemy setup
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)

# Async session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for SQLAlchemy models
Base = declarative_base()

# Lazy-loaded Supabase clients
_supabase_client = None
_supabase_admin_client = None


def _create_supabase_client():
    """Create Supabase client with error handling."""
    try:
        # Only create if we have real credentials
        if (settings.supabase_url != "https://your-project.supabase.co" and 
            settings.supabase_anon_key != "your-anon-key"):
            from supabase import create_client
            return create_client(settings.supabase_url, settings.supabase_anon_key)
        else:
            logger.warning("Supabase credentials not configured - using mock client")
            return None
    except Exception as e:
        logger.error("Failed to create Supabase client", error=str(e))
        return None


def _create_supabase_admin_client():
    """Create Supabase admin client with error handling."""
    try:
        # Only create if we have real credentials
        if (settings.supabase_url != "https://your-project.supabase.co" and 
            settings.supabase_service_role_key != "your-service-role-key"):
            from supabase import create_client
            return create_client(settings.supabase_url, settings.supabase_service_role_key)
        else:
            logger.warning("Supabase admin credentials not configured - using mock client")
            return None
    except Exception as e:
        logger.error("Failed to create Supabase admin client", error=str(e))
        return None


async def get_database_session() -> AsyncSession:
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Alias for FastAPI dependency injection
get_db = get_database_session


def get_supabase_client():
    """Dependency to get Supabase client."""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = _create_supabase_client()
    return _supabase_client


def get_supabase_admin_client():
    """Dependency to get Supabase admin client."""
    global _supabase_admin_client
    if _supabase_admin_client is None:
        _supabase_admin_client = _create_supabase_admin_client()
    return _supabase_admin_client 