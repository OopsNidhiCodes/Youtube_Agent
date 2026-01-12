#!/usr/bin/env python3
"""
Test script for YouTube Tech Video Agent
Tests all components without actually uploading to YouTube
"""

import os
import sys
from datetime import datetime
from config import Config
from logger import get_logger
from content_research import ContentResearcher
from video_generator import VideoGenerator

logger = get_logger(__name__)

def test_content_research():
    """Test content research functionality"""
    logger.info("Testing content research...")
    
    try:
        researcher = ContentResearcher()
        
        # Test trending topics
        logger.info("Testing trending topics retrieval...")
        topics = researcher.get_trending_tech_topics(limit=2)
        logger.info(f"Found {len(topics)} trending topics")
        
        for topic in topics:
            logger.info(f"Topic: {topic}")
        
        # Test script generation
        if topics:
            logger.info("Testing script generation...")
            script = researcher.generate_video_script(topics[0], duration_seconds=30)
            logger.info(f"Generated script title: {script['title']}")
            logger.info(f"Script hook: {script['hook']}")
            logger.info(f"Script length: {len(script['script'])} characters")
            
            return script
        
        return None
        
    except Exception as e:
        logger.error(f"Content research test failed: {e}")
        return None

def test_video_generation(script_data):
    """Test video generation functionality"""
    logger.info("Testing video generation...")
    
    try:
        generator = VideoGenerator()
        
        # Create test video
        test_filename = f"test_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        video_path = generator.create_short_video(script_data, test_filename)
        
        if video_path and os.path.exists(video_path):
            file_size = os.path.getsize(video_path)
            logger.info(f"Test video created successfully: {video_path}")
            logger.info(f"Video file size: {file_size / 1024 / 1024:.2f} MB")
            
            # Clean up test video
            os.remove(video_path)
            logger.info("Test video cleaned up")
            
            return True
        else:
            logger.error("Video generation failed")
            return False
            
    except Exception as e:
        logger.error(f"Video generation test failed: {e}")
        return False

def test_configuration():
    """Test configuration and environment"""
    logger.info("Testing configuration...")
    
    try:
        # Test directories
        logger.info(f"Output directory: {Config.OUTPUT_DIR}")
        logger.info(f"Temp directory: {Config.TEMP_DIR}")
        
        # Test API keys
        logger.info(f"OpenAI API key configured: {'Yes' if Config.OPENAI_API_KEY else 'No'}")
        logger.info(f"YouTube credentials configured: {'Yes' if Config.YOUTUBE_CLIENT_ID else 'No'}")
        
        # Test video settings
        logger.info(f"Video length: {Config.VIDEO_LENGTH} seconds")
        logger.info(f"Upload schedule: {Config.UPLOAD_SCHEDULE}")
        logger.info(f"Upload time: {Config.VIDEO_UPLOAD_TIME}")
        
        return True
        
    except Exception as e:
        logger.error(f"Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("=== Starting YouTube Tech Video Agent Tests ===")
    
    # Test configuration
    logger.info("\n1. Testing Configuration...")
    config_ok = test_configuration()
    
    if not config_ok:
        logger.error("Configuration test failed - please check your .env file")
        return False
    
    # Test content research
    logger.info("\n2. Testing Content Research...")
    script = test_content_research()
    
    if not script:
        logger.error("Content research test failed")
        return False
    
    # Test video generation
    logger.info("\n3. Testing Video Generation...")
    video_ok = test_video_generation(script)
    
    if not video_ok:
        logger.error("Video generation test failed")
        return False
    
    logger.info("\n=== All Tests Passed! ===")
    logger.info("Your YouTube Tech Video Agent is ready to use!")
    logger.info("Run 'python main.py --mode once' to create your first video")
    logger.info("Run 'python main.py --mode automated' to start automated uploads")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)