import schedule
import time
from datetime import datetime, timedelta
import threading
from typing import Callable, Optional
import os
from logger import get_logger

logger = get_logger(__name__)

class VideoScheduler:
    def __init__(self):
        # Read scheduler configuration from environment variables with sensible defaults
        self.upload_time = os.getenv("VIDEO_UPLOAD_TIME", "09:00")
        self.schedule_type = os.getenv("UPLOAD_SCHEDULE", "daily").lower()
        self.running = False
        self.thread = None
        logger.info(f"Scheduler initialized with {self.schedule_type} uploads at {self.upload_time}")
    
    def schedule_upload(self, upload_function: Callable):
        """Schedule the upload function based on configuration"""
        logger.info(f"Setting up {self.schedule_type} schedule for uploads at {self.upload_time}")
        
        if self.schedule_type == 'daily':
            schedule.every().day.at(self.upload_time).do(upload_function)
        elif self.schedule_type == 'weekly':
            schedule.every().week.at(self.upload_time).do(upload_function)
        elif self.schedule_type == 'monthly':
            # For monthly, we'll schedule for the 1st of each month
            schedule.every(30).days.at(self.upload_time).do(upload_function)
        else:
            logger.error(f"Invalid schedule type: {self.schedule_type}")
            return False
        
        return True

    def schedule_daily(self, upload_function: Callable, time_str: Optional[str] = None) -> bool:
        """Schedule a daily job at the specified time (HH:MM)."""
        if time_str:
            self.upload_time = time_str
        self.schedule_type = 'daily'
        logger.info(f"Setting up daily schedule at {self.upload_time}")
        try:
            schedule.every().day.at(self.upload_time).do(upload_function)
            return True
        except Exception as e:
            logger.error(f"Failed to schedule daily job: {e}")
            return False
    
    def start(self):
        """Start the scheduler in a background thread"""
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        logger.info("Scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Scheduler stopped")

    def is_running(self) -> bool:
        """Return whether the scheduler is currently running."""
        return self.running
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        logger.info("Scheduler loop started")
        
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)  # Wait a minute before retrying
    
    def get_next_run_time(self) -> Optional[datetime]:
        """Get the next scheduled run time"""
        if not schedule.jobs:
            return None
        
        # Get the next run time from the first job
        next_run = schedule.jobs[0].next_run
        return next_run
    
    def get_schedule_info(self) -> dict:
        """Get current schedule information"""
        next_run = self.get_next_run_time()
        
        return {
            'schedule_type': self.schedule_type,
            'upload_time': self.upload_time,
            'running': self.running,
            'next_upload': next_run.strftime('%Y-%m-%d %H:%M:%S') if next_run else 'Not scheduled',
            'jobs_count': len(schedule.jobs)
        }
    
    def run_now(self, upload_function: Callable):
        """Manually trigger an upload"""
        logger.info("Manually triggering upload...")
        try:
            upload_function()
            logger.info("Manual upload completed")
        except Exception as e:
            logger.error(f"Manual upload failed: {e}")
    
    def clear_schedule(self):
        """Clear all scheduled jobs"""
        schedule.clear()
        logger.info("All scheduled jobs cleared")
    
    def add_custom_schedule(self, interval: int, unit: str, upload_function: Callable):
        """Add a custom schedule (for testing or flexibility)"""
        logger.info(f"Adding custom schedule: every {interval} {unit}")
        
        if unit == 'minutes':
            schedule.every(interval).minutes.do(upload_function)
        elif unit == 'hours':
            schedule.every(interval).hours.do(upload_function)
        elif unit == 'days':
            schedule.every(interval).days.do(upload_function)
        else:
            logger.error(f"Invalid unit: {unit}")
            return False
        
        return True

# Global scheduler instance
scheduler = VideoScheduler()

def schedule_video_upload(upload_function: Callable):
    """Convenience function to schedule video uploads"""
    return scheduler.schedule_upload(upload_function)

def start_scheduler():
    """Convenience function to start the scheduler"""
    scheduler.start()

def stop_scheduler():
    """Convenience function to stop the scheduler"""
    scheduler.stop()

def get_schedule_status():
    """Convenience function to get schedule status"""
    return scheduler.get_schedule_info()