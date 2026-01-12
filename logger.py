from loguru import logger
import sys
import os

"""Logger setup that reads configuration from environment variables.

Environment variables:
- LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR). Defaults to INFO.
"""

# Ensure logs directory exists before adding file handler
os.makedirs("logs", exist_ok=True)

# Read log level from environment (default INFO)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logging
logger.remove()  # Remove default handler

# Add console handler with custom format
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=LOG_LEVEL,
    colorize=True
)

# Add file handler
logger.add(
    "logs/youtube_agent.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=LOG_LEVEL,
    rotation="10 MB",
    retention="10 days",
    compression="zip"
)

def get_logger(name: str):
    """Get logger instance for a specific module"""
    return logger.bind(name=name)

__all__ = ['logger', 'get_logger']