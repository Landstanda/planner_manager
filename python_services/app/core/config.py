"""
Core application configuration using Pydantic settings.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = Field(default="Chief-of-Flow", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")
    secret_key: str = Field(default="dev-secret-key-change-in-production", alias="SECRET_KEY")
    
    # API
    api_v1_str: str = Field(default="/api/v1", alias="API_V1_STR")
    cors_origins: List[str] = Field(
        default=["http://localhost:3000"], 
        alias="CORS_ORIGINS"
    )
    
    # Database - Supabase (defaults for development)
    supabase_url: str = Field(default="https://your-project.supabase.co", alias="SUPABASE_URL")
    supabase_anon_key: str = Field(default="your-anon-key", alias="SUPABASE_ANON_KEY")
    supabase_service_role_key: str = Field(default="your-service-role-key", alias="SUPABASE_SERVICE_ROLE_KEY")
    database_url: str = Field(default="postgresql+asyncpg://user:password@localhost:5432/chief_of_flow", alias="DATABASE_URL")
    
    # AI Configuration
    openai_api_key: str = Field(default="your-openai-api-key", alias="OPENAI_API_KEY")
    
    # Google Drive
    google_drive_credentials_json: Optional[str] = Field(
        default=None, 
        alias="GOOGLE_DRIVE_CREDENTIALS_JSON"
    )
    google_drive_folder_id: Optional[str] = Field(
        default=None, 
        alias="GOOGLE_DRIVE_FOLDER_ID"
    )
    
    # Background Tasks
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    class Config:
        env_file = ".env"
        case_sensitive = False
        # Allow extra fields for flexibility
        extra = "allow"


# Global settings instance
settings = Settings() 