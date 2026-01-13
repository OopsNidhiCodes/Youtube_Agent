#!/usr/bin/env python3
"""
Free Video Generator - With gTTS retry logic for rate limits
"""

import os
import gc
import time
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx.all import fadein, fadeout
from gtts import gTTS
from typing import Dict, List, Optional
from logger import get_logger

logger = get_logger(__name__)

class FreeVideoGenerator:
    """Free video generator with rate limit handling"""
    
    def __init__(self):
        self.temp_dir = "temp"
        self.output_dir = "output"
        self._setup_directories()
        logger.info("Free video generator initialized")
    
    def _setup_directories(self):
        """Create necessary directories"""
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_audio(self, text: str, output_path: str, max_retries: int = 3) -> bool:
        """Generate audio with retry logic for rate limits"""
        base, ext = os.path.splitext(output_path)
        if ext.lower() != ".mp3":
            output_path = base + ".mp3"
        
        for attempt in range(max_retries):
            try:
                # Add delay between requests to avoid rate limits
                if attempt > 0:
                    wait_time = (2 ** attempt) * 2  # Exponential backoff: 4s, 8s, 16s
                    logger.info(f"Rate limit hit, waiting {wait_time}s...")
                    time.sleep(wait_time)
                
                tts = gTTS(text=text, lang="en", slow=False)
                tts.save(output_path)
                
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    logger.info(f"Audio: {os.path.basename(output_path)}")
                    # Small delay to be nice to Google's API
                    time.sleep(1)
                    return True
                    
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "Too Many Requests" in error_msg:
                    logger.warning(f"Rate limited (attempt {attempt + 1}/{max_retries})")
                    if attempt == max_retries - 1:
                        logger.error("Max retries reached, skipping audio")
                        return False
                else:
                    logger.error(f"Audio error: {e}")
                    return False
        
        return False
    
    def create_background_image(self, text: str, size: tuple = (1280, 720),
                              bg_color: tuple = (30, 30, 30)) -> Image.Image:
        """Create background image (720p)"""
        try:
            img = Image.new('RGB', size, bg_color)
            draw = ImageDraw.Draw(img)
            
            # Font
            try:
                font_size = 40
                font_paths = [
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                ]
                
                font = None
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        try:
                            font = ImageFont.truetype(font_path, font_size)
                            break
                        except:
                            continue
                
                if font is None:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
            
            # Text wrapping
            max_chars = 35
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > max_chars:
                    current_line.pop()
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw
            y_position = size[1] // 2 - (len(lines) * 50) // 2
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x_position = (size[0] - text_width) // 2
                draw.text((x_position, y_position), line, font=font, fill=(255, 255, 255))
                y_position += 50
            
            return img
            
        except Exception as e:
            logger.error(f"Image error: {e}")
            return Image.new('RGB', size, bg_color)
    
    def create_video_segment(self, text: str, audio_path: str, duration: int, 
                           bg_color: tuple = (30, 30, 30)) -> Optional[ImageClip]:
        """Create video segment"""
        try:
            # Image
            img = self.create_background_image(text, bg_color=bg_color)
            temp_img_path = os.path.join(self.temp_dir, f"img_{hash(text) % 1000}.png")
            img.save(temp_img_path, optimize=True)
            del img
            gc.collect()
            
            # Video with audio
            if os.path.exists(audio_path):
                try:
                    audio_clip = AudioFileClip(audio_path)
                    actual_duration = audio_clip.duration
                    video_clip = ImageClip(temp_img_path, duration=actual_duration)
                    video_clip = video_clip.set_audio(audio_clip)
                except Exception as audio_error:
                    logger.warning(f"Audio load failed, using silent: {audio_error}")
                    video_clip = ImageClip(temp_img_path, duration=duration)
            else:
                # No audio file - create silent video
                logger.warning(f"No audio file, creating silent segment")
                video_clip = ImageClip(temp_img_path, duration=duration)
            
            # Fades
            video_clip = fadein(video_clip, 0.3)
            video_clip = fadeout(video_clip, 0.3)
            
            logger.info(f"Segment: {text[:25]}...")
            return video_clip
            
        except Exception as e:
            logger.error(f"Segment error: {e}")
            return None
    
    def create_short_form_video(self, script: Dict, output_path: str, 
                              background_music: Optional[str] = None) -> bool:
        """Create video"""
        video_clips = []
        temp_files = []
        
        try:
            logger.info("Creating video...")
            
            # Limit segments
            max_segments = 3
            segment_count = 0
            
            # Hook
            if 'hook' in script and segment_count < max_segments:
                hook = script['hook']
                audio_path = os.path.join(self.temp_dir, f"h_{segment_count}.mp3")
                temp_files.append(audio_path)
                
                # Try to generate audio, but continue even if it fails
                self.generate_audio(hook['text'], audio_path)
                
                clip = self.create_video_segment(
                    hook['text'], audio_path, hook.get('duration', 5),
                    bg_color=(40, 60, 120)
                )
                if clip:
                    video_clips.append(clip)
                    segment_count += 1
            
            # Main segments
            for i, segment in enumerate(script.get('segments', [])[:2]):
                if segment_count >= max_segments:
                    break
                    
                audio_path = os.path.join(self.temp_dir, f"s_{i}.mp3")
                temp_files.append(audio_path)
                
                # Try to generate audio, but continue even if it fails
                self.generate_audio(segment['text'], audio_path)
                
                clip = self.create_video_segment(
                    segment['text'], audio_path, segment.get('duration', 10)
                )
                if clip:
                    video_clips.append(clip)
                    segment_count += 1
            
            # Export
            if video_clips:
                logger.info(f"Combining {len(video_clips)} clips...")
                final_video = concatenate_videoclips(video_clips, method="compose")
                
                logger.info("Exporting...")
                final_video.write_videofile(
                    output_path,
                    fps=24,
                    codec='libx264',
                    audio_codec='aac',
                    bitrate="500k",
                    preset='ultrafast',
                    threads=1,
                    logger=None,
                    verbose=False
                )
                
                # Cleanup
                logger.info("Cleanup...")
                final_video.close()
                for clip in video_clips:
                    try:
                        clip.close()
                    except:
                        pass
                
                # Remove temp files
                for f in temp_files:
                    try:
                        if os.path.exists(f):
                            os.remove(f)
                    except:
                        pass
                
                # Remove temp images
                for f in os.listdir(self.temp_dir):
                    if f.startswith('img_') and f.endswith('.png'):
                        try:
                            os.remove(os.path.join(self.temp_dir, f))
                        except:
                            pass
                
                gc.collect()
                logger.info(f"✅ Video: {output_path}")
                return True
            else:
                logger.error("No clips")
                return False
                
        except Exception as e:
            logger.error(f"Video error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            
            for clip in video_clips:
                try:
                    clip.close()
                except:
                    pass
            
            return False
    
    def generate_video_from_script(self, script: Dict, output_filename: str = None) -> Optional[str]:
        """Generate video"""
        try:
            if not output_filename:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"video_{timestamp}.mp4"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            if self.create_short_form_video(script, output_path):
                logger.info(f"Done: {output_path}")
                return output_path
            else:
                logger.error("Failed")
                return None
                
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return None