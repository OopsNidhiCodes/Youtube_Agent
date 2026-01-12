#!/usr/bin/env python3
"""
Free Configuration Module
Completely free configuration without API keys
"""

import os
from pathlib import Path
from typing import Optional
from logger import get_logger

logger = get_logger(__name__)

class FreeConfig:
    """Configuration for completely free YouTube video agent"""
    
    # Video settings
    VIDEO_UPLOAD_TIME = os.getenv("VIDEO_UPLOAD_TIME", "09:00")
    VIDEO_TOPIC = os.getenv("VIDEO_TOPIC", "technology")
    VIDEO_LENGTH = int(os.getenv("VIDEO_LENGTH", "60"))
    UPLOAD_SCHEDULE = os.getenv("UPLOAD_SCHEDULE", "daily")
    
    # Directory settings
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
    TEMP_DIR = os.getenv("TEMP_DIR", "temp")
    LOGS_DIR = os.getenv("LOGS_DIR", "logs")
    VIDEOS_DIR = os.getenv("VIDEOS_DIR", "videos")
    
    # Free AI model settings
    AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "microsoft/DialoGPT-medium")
    AI_DEVICE = os.getenv("AI_DEVICE", "cpu")  # Use CPU for free deployment
    AI_MAX_LENGTH = int(os.getenv("AI_MAX_LENGTH", "500"))
    AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))
    
    # Free TTS settings
    TTS_RATE = int(os.getenv("TTS_RATE", "150"))
    TTS_VOLUME = float(os.getenv("TTS_VOLUME", "0.9"))
    
    # RSS feed sources (free)
    RSS_FEEDS = [
        "https://feeds.feedburner.com/oreilly/radar",
        "https://techcrunch.com/feed/",
        "https://www.wired.com/feed/rss",
        "https://feeds.arstechnica.com/arstechnica/index",
        "https://www.theverge.com/rss/index.xml",
        "https://www.reddit.com/r/technology/.rss",
        "https://www.reddit.com/r/programming/.rss"
    ]
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Cleanup settings
    KEEP_VIDEO_COUNT = int(os.getenv("KEEP_VIDEO_COUNT", "5"))
    CLEANUP_OLD_FILES = os.getenv("CLEANUP_OLD_FILES", "true").lower() == "true"
    
    # YouTube settings (manual upload)
    YOUTUBE_UPLOAD_METHOD = "manual"  # Always manual for free version
    YOUTUBE_CHANNEL_URL = os.getenv("YOUTUBE_CHANNEL_URL", "")
    
    # Render settings (free tier)
    RENDER_FREE_TIER = os.getenv("RENDER_FREE_TIER", "true").lower() == "true"
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration (no API keys needed)"""
        try:
            # Create necessary directories
            directories = [cls.OUTPUT_DIR, cls.TEMP_DIR, cls.LOGS_DIR, cls.VIDEOS_DIR]
            for directory in directories:
                Path(directory).mkdir(parents=True, exist_ok=True)
            
            logger.info("Free configuration validated successfully")
            logger.info(f"Video settings: {cls.VIDEO_LENGTH}s daily at {cls.VIDEO_UPLOAD_TIME}")
            logger.info(f"AI model: {cls.AI_MODEL_NAME}")
            logger.info(f"Upload method: {cls.YOUTUBE_UPLOAD_METHOD}")
            logger.info(f"Cleanup: {cls.CLEANUP_OLD_FILES} (keep {cls.KEEP_VIDEO_COUNT} videos)")
            
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    @classmethod
    def get_video_schedule_info(cls) -> dict:
        """Get video scheduling information"""
        return {
            "upload_time": cls.VIDEO_UPLOAD_TIME,
            "schedule": cls.UPLOAD_SCHEDULE,
            "topic": cls.VIDEO_TOPIC,
            "length": cls.VIDEO_LENGTH,
            "method": cls.YOUTUBE_UPLOAD_METHOD
        }
    
    @classmethod
    def get_ai_settings(cls) -> dict:
        """Get AI model settings"""
        return {
            "model": cls.AI_MODEL_NAME,
            "device": cls.AI_DEVICE,
            "max_length": cls.AI_MAX_LENGTH,
            "temperature": cls.AI_TEMPERATURE
        }
    
    @classmethod
    def get_cleanup_settings(cls) -> dict:
        """Get cleanup settings"""
        return {
            "enabled": cls.CLEANUP_OLD_FILES,
            "keep_count": cls.KEEP_VIDEO_COUNT
        }
    
    @classmethod
    def get_rss_feeds(cls) -> list:
        """Get RSS feed sources"""
        return cls.RSS_FEEDS
    
    @classmethod
    def is_render_free_tier(cls) -> bool:
        """Check if using Render free tier"""
        return cls.RENDER_FREE_TIER
    
    @classmethod
    def get_directory_paths(cls) -> dict:
        """Get all directory paths"""
        return {
            "output": cls.OUTPUT_DIR,
            "temp": cls.TEMP_DIR,
            "logs": cls.LOGS_DIR,
            "videos": cls.VIDEOS_DIR
        }

# Test configuration
if __name__ == "__main__":
    print("Testing free configuration...")
    
    if FreeConfig.validate_config():
        print("✅ Configuration validated successfully!")
        print(f"📁 Directories: {FreeConfig.get_directory_paths()}")
        print(f"🎬 Video settings: {FreeConfig.get_video_schedule_info()}")
        print(f"🤖 AI settings: {FreeConfig.get_ai_settings()}")
        print(f"🧹 Cleanup settings: {FreeConfig.get_cleanup_settings()}")
        print(f"📡 RSS feeds: {len(FreeConfig.get_rss_feeds())} sources")
    else:
        print("❌ Configuration validation failed!")
        exit(1)