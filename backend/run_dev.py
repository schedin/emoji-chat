#!/usr/bin/env python3
"""Development server runner for emoji chat backend."""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import uvicorn
from config import settings

if __name__ == "__main__":
    print("Starting Emoji Chat Backend in development mode...")
    print(f"Server will run on http://{settings.host}:{settings.port}")
    print(f"LLM URL: {settings.llm_url}")
    print(f"Content moderation enabled: {settings.enable_content_moderation}")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
