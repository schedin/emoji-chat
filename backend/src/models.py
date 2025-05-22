"""Pydantic models for request and response validation."""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from config import settings


class MessageRequest(BaseModel):
    """Request model for emoji generation."""

    message: str = Field(
        ...,
        min_length=settings.min_message_length,
        max_length=settings.max_message_length,
        description="The user message to generate emojis for"
    )

    @validator('message')
    def validate_message(cls, v):
        """Validate message content."""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty or only whitespace")

        # Basic validation for reasonable content
        if len(v.strip()) < settings.min_message_length:
            raise ValueError(f"Message too short. Minimum length: {settings.min_message_length}")

        return v.strip()


class EmojiResponse(BaseModel):
    """Response model for emoji generation."""

    emojis: List[str] = Field(
        ...,
        description="List of emojis that correspond to the user message"
    )
    message: str = Field(
        ...,
        description="The original user message"
    )
    moderation_passed: Optional[bool] = Field(
        None,
        description="Whether the message passed content moderation (if enabled)"
    )


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")


class SampleResponse(BaseModel):
    """Response model for sample sentence generation."""

    sample: str = Field(
        ...,
        description="A short inspirational sentence to use as inspiration"
    )


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Service status")
    llm_url: str = Field(..., description="Configured LLM URL")
    llm_model: str = Field(..., description="Configured LLM model")
    content_moderation_enabled: bool = Field(..., description="Whether content moderation is enabled")
    moderation_model: Optional[str] = Field(None, description="Model used for content moderation")
