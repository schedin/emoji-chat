#!/usr/bin/env python3
"""Startup script for the emoji chat backend."""

import uvicorn
from config import settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=False,  # Set to False for production
        log_level="info"
    )
