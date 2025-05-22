"""FastAPI backend server for emoji chat application."""

import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from config import settings
from models import MessageRequest, EmojiResponse, ErrorResponse, HealthResponse
from llm_client import llm_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Emoji Chat Backend",
    description="A FastAPI backend that generates emojis based on user messages using an LLM",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail="An unexpected error occurred"
        ).dict()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        llm_url=settings.llm_url,
        content_moderation_enabled=settings.enable_content_moderation
    )


@app.post("/api/emojis", response_model=EmojiResponse)
async def generate_emojis(request: MessageRequest):
    """
    Generate emojis for a given message.
    
    This endpoint:
    1. Validates the message parameter for reasonable size
    2. Optionally checks content moderation (if enabled)
    3. Generates appropriate emojis using the LLM
    """
    try:
        message = request.message
        logger.info(f"Processing message: {message[:50]}...")
        
        # Content moderation (if enabled)
        moderation_passed = None
        if settings.enable_content_moderation:
            is_safe, reason = await llm_client.moderate_content(message)
            moderation_passed = is_safe
            
            if not is_safe:
                logger.warning(f"Message failed moderation: {reason}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Message failed content moderation: {reason}"
                )
        
        # Generate emojis
        emojis = await llm_client.generate_emojis(message)
        
        if not emojis:
            logger.warning("No emojis generated, using fallback")
            emojis = ["😊", "👍"]
        
        logger.info(f"Generated emojis: {emojis}")
        
        return EmojiResponse(
            emojis=emojis,
            message=message,
            moderation_passed=moderation_passed
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate emojis"
        )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Emoji Chat Backend API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "generate_emojis": "/api/emojis"
        }
    }


if __name__ == "__main__":
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    logger.info(f"LLM URL: {settings.llm_url}")
    logger.info(f"Content moderation enabled: {settings.enable_content_moderation}")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level="info"
    )
