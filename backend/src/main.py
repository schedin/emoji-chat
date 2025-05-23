"""FastAPI backend server for emoji chat application."""

import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from config import settings
from models import MessageRequest, EmojiResponse, ErrorResponse, HealthResponse, SampleResponse
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
    logger.error(f"Unhandled exception in {request.method} {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=f"An unexpected error occurred: {str(exc)}"
        ).model_dump()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        llm_url=settings.llm_url,
        llm_model=settings.llm_model,
        content_moderation_enabled=True,  # Always available, controlled by user
        moderation_model=settings.moderation_model or settings.llm_model
    )


@app.post("/api/emojis", response_model=EmojiResponse)
async def generate_emojis(request: MessageRequest):
    """
    Generate emojis for a given message.

    This endpoint:
    1. Validates the message parameter for reasonable size
    2. Optionally checks content moderation (if not disabled by user)
    3. Generates appropriate emojis using the LLM
    """
    try:
        message = request.message
        disable_moderation = request.disable_moderation
        logger.info(f"Processing message: {message[:50]}... (moderation disabled: {disable_moderation})")

        # Content moderation (if not disabled by user)
        moderation_passed = None
        should_moderate = not disable_moderation

        if should_moderate:
            logger.info("Starting content moderation check...")
            try:
                is_safe, reason = await llm_client.moderate_content(message)
                moderation_passed = is_safe
                logger.info(f"Moderation result: safe={is_safe}, reason={reason}")

                if not is_safe:
                    logger.warning(f"Message failed moderation: {reason}")
                    raise HTTPException(
                        status_code=400,
                        detail=f"Message failed content moderation: {reason}"
                    )
                else:
                    logger.info("Message passed content moderation")
            except HTTPException:
                # Re-raise HTTP exceptions (moderation failures)
                raise
            except Exception as e:
                logger.error(f"Error during content moderation: {str(e)}", exc_info=True)
                raise HTTPException(
                    status_code=500,
                    detail=f"Content moderation failed: {str(e)}"
                )
        else:
            logger.info(f"Content moderation skipped (user disabled: {disable_moderation})")

        # Generate emojis
        logger.info("Starting emoji generation...")
        try:
            emojis = await llm_client.generate_emojis(message)
            logger.info(f"LLM returned emojis: {emojis}")

            if not emojis:
                logger.warning("No emojis generated, using fallback")
                emojis = ["😊", "👍"]

            logger.info(f"Final emojis: {emojis}")
        except Exception as e:
            logger.error(f"Error during emoji generation: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Emoji generation failed: {str(e)}"
            )

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


@app.get("/api/sample", response_model=SampleResponse)
async def get_sample():
    """
    Generate a sample inspirational sentence.

    This endpoint generates a short, inspirational sentence that can be used
    as inspiration for users to start conversations or express themselves.
    """
    try:
        logger.info("Generating sample sentence")

        # Generate sample sentence
        sample = await llm_client.generate_sample_sentence()

        logger.info(f"Generated sample: {sample}")

        return SampleResponse(sample=sample)

    except Exception as e:
        logger.error(f"Error generating sample: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate sample sentence"
        )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Emoji Chat Backend API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "generate_emojis": "/api/emojis",
            "sample": "/sample"
        }
    }


def main():
    # Determine mode based on settings
    mode = "development" if settings.development_mode else "production"

    # Log startup information
    logger.info(f"Starting Emoji Chat Backend in {mode} mode...")
    logger.info(f"Server will run on http://{settings.host}:{settings.port}")
    logger.info(f"LLM URL: {settings.llm_url}")
    logger.info(f"LLM Model: {settings.llm_model}")
    logger.info(f"Content moderation: User-controlled (enabled by default)")
    moderation_model = settings.moderation_model or settings.llm_model
    logger.info(f"Moderation model: {moderation_model}")

    if settings.development_mode:
        logger.info("Development mode: Auto-reload enabled")
        logger.info("Press Ctrl+C to stop the server")

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.development_mode,  # Enable reload only in development
        log_level="info"
    )


if __name__ == "__main__":
    main()
