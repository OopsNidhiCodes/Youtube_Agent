#!/usr/bin/env python3
"""
🆓 FREE YouTube Tech Video Agent
Completely free version - no paid APIs, no costs!
"""

import os
import sys
import time
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional

# Import free modules
from content_research_free import FreeContentResearcher
from video_generator_free import FreeVideoGenerator
from logger import get_logger
from scheduler import VideoScheduler
from free_uploader import upload_to_transfer_sh

logger = get_logger(__name__)

class FreeYouTubeTechAgent:
    """Free YouTube video agent using only free resources"""
    
    def __init__(self):
        self.content_researcher = FreeContentResearcher()
        self.video_generator = FreeVideoGenerator()
        self.scheduler = VideoScheduler()
        self.output_dir = "output"
        self.videos_dir = "videos"
        self._setup_directories()
    
    def _setup_directories(self):
        """Create necessary directories"""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.videos_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        os.makedirs("temp", exist_ok=True)
    
    def create_video(self, topic: Optional[str] = None, video_length: int = 60) -> Optional[str]:
        """Create a complete video using only free resources"""
        try:
            logger.info("🆓 Starting FREE video creation process...")
            
            # Step 1: Research trending topics (RSS feeds)
            logger.info("📰 Researching trending topics...")
            trending_topics = self.content_researcher.get_trending_tech_topics()
            
            if not trending_topics:
                logger.error("❌ No trending topics found")
                return None
            
            logger.info(f"✅ Found {len(trending_topics)} trending topics")
            
            # Step 2: Generate video script
            logger.info("🤖 Generating video script...")
            chosen_topic = topic if topic else trending_topics[0]
            script = self.content_researcher.generate_video_script(chosen_topic, video_length)
            
            if not script:
                logger.error("❌ Script generation failed")
                return None
            
            logger.info("✅ Script generated successfully")
            # logger.info(f"📝 Script preview: {script[:100]}...")
            
            # Step 3: Create video
            logger.info("🎬 Creating video...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_filename = f"free_tech_video_{timestamp}.mp4"
            video_path = self.video_generator.generate_video_from_script(script, video_filename)
            
            if not video_path or not os.path.exists(video_path):
                logger.error("❌ Video creation failed")
                return None
            
            logger.info(f"✅ Video created: {video_path}")
            
            # Step 4: Generate upload instructions (manual upload)
            logger.info("📋 Generating upload instructions...")
            video_idea = {
                "topic": chosen_topic,
                "script": script,
                "keywords": self.content_researcher._extract_keywords(chosen_topic),
                "tags": self.content_researcher._generate_tags(chosen_topic),
                "description": self.content_researcher._generate_description(chosen_topic, script)
            }
            instructions_path = self.generate_upload_instructions(video_path, video_idea)
            
            logger.info(f"✅ Upload instructions created: {instructions_path}")

            # Optional: deliver via transfer.sh if persistent disk is unavailable
            delivery_method = os.getenv("OUTPUT_DELIVERY", "local").lower()
            if delivery_method == "transfer_sh":
                logger.info("🚚 Delivering files via transfer.sh (no disk required)...")
                video_url = upload_to_transfer_sh(video_path)
                instr_url = upload_to_transfer_sh(instructions_path)

                # Save a small delivery manifest next to files
                manifest = {
                    "video_file": os.path.basename(video_path),
                    "video_url": video_url,
                    "instructions_file": os.path.basename(instructions_path),
                    "instructions_url": instr_url,
                    "created_at": datetime.now().isoformat(),
                }
                manifest_path = video_path.replace('.mp4', '_delivery.json')
                with open(manifest_path, 'w', encoding='utf-8') as mf:
                    json.dump(manifest, mf, indent=2)
                logger.info(f"📦 Delivery manifest saved: {manifest_path}")
                if video_url:
                    logger.info(f"🔗 Video download URL: {video_url}")
                if instr_url:
                    logger.info(f"🔗 Instructions download URL: {instr_url}")
            
            # Step 5: Cleanup old files
            self._cleanup_old_files()
            
            logger.info("🎉 FREE video creation completed!")
            logger.info(f"📹 Video ready for manual upload: {video_path}")
            logger.info(f"📖 Instructions: {instructions_path}")
            
            return video_path
            
        except Exception as e:
            logger.error(f"❌ Video creation failed: {str(e)}")
            return None
    
    def generate_upload_instructions(self, video_path: str, metadata: Dict) -> str:
        """Generate instructions for manual YouTube upload"""
        instructions = f"""
🎬 VIDEO READY FOR UPLOAD!

📁 Video File: {video_path}
📋 Metadata File: {video_path.replace('.mp4', '_metadata.json')}

📤 UPLOAD INSTRUCTIONS:

1. **Go to YouTube Studio** (studio.youtube.com)
2. **Click "Create" → "Upload videos"**
3. **Select the video file:** {os.path.basename(video_path)}

📋 COPY-PASTE THIS INFORMATION:

📝 **Title:** {metadata.get('topic', 'Tech Video')}

📝 **Description:**
{metadata.get('description', 'Check out this tech video!')}

🏷️ **Tags:** {', '.join(metadata.get('tags', []))}

🔍 **Keywords:** {', '.join(metadata.get('keywords', []))}

⚙️ **UPLOAD SETTINGS:**
- **Visibility:** Public (or schedule as desired)
- **Category:** Science & Technology
- **Made for kids:** No
- **License:** Standard YouTube License

⏰ **SCHEDULE RECOMMENDATION:**
Upload at 9:00 AM for best engagement

📊 **AFTER UPLOAD:**
1. Add to relevant playlists
2. Create a custom thumbnail
3. Add end screens and cards
4. Share on social media

🔄 **AUTOMATION NOTE:**
This video was generated automatically using free tools.
Next video will be generated and prepared for upload soon!

---
Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        # Save instructions to file
        instructions_path = video_path.replace('.mp4', '_upload_instructions.txt')
        with open(instructions_path, 'w', encoding='utf-8') as f:
            f.write(instructions.strip())
        
        logger.info(f"Upload instructions saved: {instructions_path}")
        return instructions_path
    
    def run_automated_mode(self):
        """Run in automated mode (creates videos but doesn't upload)"""
        logger.info("Starting free automated mode...")
        
        def create_and_prepare_video():
            try:
                logger.info("Creating new video...")
                video_path = self.create_video()
                
                if video_path:
                    # Load metadata
                    metadata_path = video_path.replace('.mp4', '_metadata.json')
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    # Generate upload instructions
                    instructions_path = self.generate_upload_instructions(video_path, metadata)
                    
                    logger.info("🎉 VIDEO READY FOR MANUAL UPLOAD!")
                    logger.info(f"📁 Video: {video_path}")
                    logger.info(f"📋 Instructions: {instructions_path}")
                    delivery_method = os.getenv("OUTPUT_DELIVERY", "local").lower()
                    if delivery_method == "transfer_sh":
                        manifest_path = video_path.replace('.mp4', '_delivery.json')
                        if os.path.exists(manifest_path):
                            with open(manifest_path, 'r', encoding='utf-8') as mf:
                                manifest = json.load(mf)
                            logger.info("🔗 Delivery URLs (no disk):")
                            logger.info(f"   Video: {manifest.get('video_url')}")
                            logger.info(f"   Instructions: {manifest.get('instructions_url')}")
                    logger.info("🔄 Next video will be created at the next scheduled time")
                    
                    # Clean up old files (keep last 5 videos)
                    self._cleanup_old_files()
                    
                else:
                    logger.error("Failed to create video")
                    
            except Exception as e:
                logger.error(f"Error in automated video creation: {e}")
        
        # Schedule daily video creation
        schedule_time = os.getenv('VIDEO_UPLOAD_TIME', '09:00')
        logger.info(f"Scheduling daily video creation at {schedule_time}")
        
        self.scheduler.schedule_daily(create_and_prepare_video, schedule_time)
        
        # Create first video immediately
        logger.info("Creating first video immediately...")
        create_and_prepare_video()
        
        logger.info("Free automated mode started successfully!")
        logger.info("The agent will create videos daily and prepare them for manual upload.")
        logger.info("Check the output folder for new videos and upload instructions.")
        
        # Keep the scheduler running
        try:
            self.scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping free automated mode...")
            self.scheduler.stop()
    
    def _cleanup_old_files(self, keep_count: int = 5):
        """Clean up old video files to save space"""
        try:
            # Get all video files
            video_files = []
            for ext in ['*.mp4', '*.avi', '*.mov']:
                video_files.extend(Path(self.output_dir).glob(ext))
            
            # Sort by modification time
            video_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remove old files
            if len(video_files) > keep_count:
                for old_file in video_files[keep_count:]:
                    old_file.unlink()
                    # Also remove metadata and instructions
                    for suffix in ['.json', '_metadata.json', '_upload_instructions.txt']:
                        meta_file = old_file.with_suffix(suffix)
                        if meta_file.exists():
                            meta_file.unlink()
                    
                    logger.info(f"Cleaned up old file: {old_file}")
                    
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")
    
    def get_status(self) -> Dict:
        """Get agent status"""
        video_files = list(Path(self.output_dir).glob("*.mp4"))
        
        return {
            "status": "running",
            "mode": "free",
            "videos_created": len(video_files),
            "latest_video": str(video_files[0]) if video_files else None,
            "scheduler_active": self.scheduler.is_running(),
            "next_run": self.scheduler.get_next_run_time(),
            "free_features": {
                "content_research": "RSS feeds + Hugging Face",
                "video_generation": "Local TTS + OpenCV",
                "upload_method": "Manual (YouTube Studio)",
                "cost": "Completely Free"
            }
        }

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Free YouTube Tech Video Agent")
    parser.add_argument("--mode", choices=["create", "automated", "status"], 
                       default="create", help="Operation mode")
    parser.add_argument("--topic", type=str, help="Video topic (optional)")
    parser.add_argument("--length", type=int, default=60, help="Video length in seconds")
    
    args = parser.parse_args()
    
    agent = FreeYouTubeTechAgent()
    
    if args.mode == "create":
        # Create single video
        video_path = agent.create_video(args.topic, args.length)
        if video_path:
            # Load metadata and generate instructions
            metadata_path = video_path.replace('.mp4', '_metadata.json')
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            instructions_path = agent.generate_upload_instructions(video_path, metadata)
            
            print(f"\n🎉 VIDEO CREATED SUCCESSFULLY!")
            print(f"📁 Video file: {video_path}")
            print(f"📋 Upload instructions: {instructions_path}")
            print("\n🔄 Next steps:")
            print("1. Read the upload instructions file")
            print("2. Manually upload to YouTube Studio")
            print("3. Use the provided title, description, and tags")
        else:
            print("❌ Failed to create video")
            sys.exit(1)
    
    elif args.mode == "automated":
        # Run automated mode
        print("🚀 Starting FREE automated YouTube video agent...")
        print("This version creates videos but requires manual upload to YouTube.")
        print("Check the output folder for new videos and upload instructions.")
        print("Press Ctrl+C to stop\n")
        
        agent.run_automated_mode()
    
    elif args.mode == "status":
        # Show status
        status = agent.get_status()
        print("\n📊 FREE YOUTUBE TECH VIDEO AGENT STATUS")
        print("=" * 50)
        print(f"Status: {status['status']}")
        print(f"Mode: {status['mode']}")
        print(f"Videos Created: {status['videos_created']}")
        print(f"Scheduler Active: {status['scheduler_active']}")
        if status['next_run']:
            print(f"Next Scheduled Run: {status['next_run']}")
        if status['latest_video']:
            print(f"Latest Video: {status['latest_video']}")
        
        print("\n🆓 FREE FEATURES:")
        for feature, description in status['free_features'].items():
            print(f"  {feature.replace('_', ' ').title()}: {description}")

if __name__ == "__main__":
    main()