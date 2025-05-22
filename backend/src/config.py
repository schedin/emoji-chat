"""Configuration settings for the emoji chat backend."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Configuration
    llm_url: str = os.getenv("LLM_URL", "http://llm-server:11434")
    llm_model: str = os.getenv("LLM_MODEL", "gemma3:1b-it-qat")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    llm_max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "100"))

    # Content moderation settings
    enable_content_moderation: bool = os.getenv("ENABLE_CONTENT_MODERATION", "true").lower() == "true"
    moderation_model: str = os.getenv("MODERATION_MODEL", "")  # Use same model as main if empty

    # Message validation settings
    max_message_length: int = int(os.getenv("MAX_MESSAGE_LENGTH", "1000"))
    min_message_length: int = int(os.getenv("MIN_MESSAGE_LENGTH", "1"))

    # Server settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    # API settings
    api_timeout: int = int(os.getenv("API_TIMEOUT", "30"))

    # Development settings
    development_mode: bool = os.getenv("DEVELOPMENT_MODE", "false").lower() == "true"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
