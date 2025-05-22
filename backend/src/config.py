"""Configuration settings for the emoji chat backend."""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # LLM Configuration
    llm_url: str = os.getenv("LLM_URL", "http://llm-server:8000")
    
    # Content moderation settings
    enable_content_moderation: bool = os.getenv("ENABLE_CONTENT_MODERATION", "true").lower() == "true"
    
    # Message validation settings
    max_message_length: int = int(os.getenv("MAX_MESSAGE_LENGTH", "1000"))
    min_message_length: int = int(os.getenv("MIN_MESSAGE_LENGTH", "1"))
    
    # Server settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # API settings
    api_timeout: int = int(os.getenv("API_TIMEOUT", "30"))
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
