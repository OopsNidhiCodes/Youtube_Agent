from loguru import logger
import sys
from config import Config

# Configure logging
logger.remove()  # Remove default handler

# Add console handler with custom format
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=Config.LOG_LEVEL,
    colorize=True
)

# Add file handler
logger.add(
    "logs/youtube_agent.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=Config.LOG_LEVEL,
    rotation="10 MB",
    retention="10 days",
    compression="zip"
)

# Create logs directory
import os
os.makedirs("logs", exist_ok=True)

def get_logger(name: str):
    """Get logger instance for a specific module"""
    return logger.bind(name=name)

__all__ = ['logger', 'get_logger']