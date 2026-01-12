#!/usr/bin/env python3
"""
Free Video Generator Module - Memory Optimized for Render Free Tier (512MB)
Uses gTTS and aggressive memory management
"""

import os
import gc
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx.all import fadein, fadeout
from gtts import gTTS
from typing import Dict, List, Optional
from logger import get_logger

logger = get_logger(__name__)

class FreeVideoGenerator:
    """Free video generator optimized for low memory"""
    
    def __init__(self):
        self.temp_dir = "temp"
        self.output_dir = "output"
        self._setup_directories()
        logger.info("Free video generator initialized (memory-optimized)")
    
    def _setup_directories(self):
        """Create necessary directories"""
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_audio(self, text: str, output_path: str) -> bool:
        """Generate narration audio using gTTS"""
        try:
            base, ext = os.path.splitext(output_path)
            if ext.lower() != ".mp3":
                output_path = base + ".mp3"
            
            tts = gTTS(text=text, lang="en", slow=False)
            tts.save(output_path)
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                logger.info(f"Audio generated: {os.path.basename(output_path)}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            return False
    
    def create_background_image(self, text: str, size: tuple = (1280, 720),  # Reduced from 1920x1080
                              bg_color: tuple = (30, 30, 30)) -> Image.Image:
        """Create background image with text overlay (reduced resolution to save memory)"""
        try:
            img = Image.new('RGB', size, bg_color)
            draw = ImageDraw.Draw(img)
            
            # Use default font to save memory
            try:
                font_size = 40  # Reduced from 60
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
            
            # Split text into lines
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
            
            # Draw text (simplified, no shadows to save memory)
            y_position = size[1] // 2 - (len(lines) * 50) // 2
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x_position = (size[0] - text_width) // 2
                
                # Single text layer (no shadow)
                draw.text((x_position, y_position), line, font=font, fill=(255, 255, 255))
                y_position += 50
            
            return img
            
        except Exception as e:
            logger.error(f"Error creating image: {e}")
            return Image.new('RGB', size, bg_color)
    
    def create_video_segment(self, text: str, audio_path: str, duration: int, 
                           bg_color: tuple = (30, 30, 30)) -> Optional[ImageClip]:
        """Create a video segment with aggressive memory management"""
        try:
            # Create and save image
            img = self.create_background_image(text, bg_color=bg_color)
            temp_img_path = os.path.join(self.temp_dir, f"seg_{hash(text) % 1000}.png")
            img.save(temp_img_path, optimize=True)
            del img  # Free memory immediately
            gc.collect()
            
            # Create video clip
            if os.path.exists(audio_path):
                audio_clip = AudioFileClip(audio_path)
                actual_duration = audio_clip.duration
                video_clip = ImageClip(temp_img_path, duration=actual_duration)
                video_clip = video_clip.set_audio(audio_clip)
                audio_clip.close()  # Close audio immediately
            else:
                video_clip = ImageClip(temp_img_path, duration=duration)
            
            # Simple fade (reduced duration to save processing)
            video_clip = fadein(video_clip, 0.3)
            video_clip = fadeout(video_clip, 0.3)
            
            logger.info(f"Segment created: {text[:30]}...")
            return video_clip
            
        except Exception as e:
            logger.error(f"Error creating segment: {e}")
            return None
    
    def create_short_form_video(self, script: Dict, output_path: str, 
                              background_music: Optional[str] = None) -> bool:
        """Create video with aggressive memory optimization"""
        try:
            logger.info("Creating video (memory-optimized)...")
            
            video_clips = []
            temp_audio_files = []
            
            # Limit segments to prevent memory issues
            max_segments = 3  # Reduced from unlimited
            segment_count = 0
            
            # Hook
            if 'hook' in script and segment_count < max_segments:
                hook = script['hook']
                audio_path = os.path.join(self.temp_dir, f"hook_{hash(str(hook)) % 1000}.mp3")
                temp_audio_files.append(audio_path)
                
                if self.generate_audio(hook['text'], audio_path):
                    clip = self.create_video_segment(
                        hook['text'], audio_path, hook.get('duration', 5),
                        bg_color=(40, 60, 120)
                    )
                    if clip:
                        video_clips.append(clip)
                        segment_count += 1
                        gc.collect()  # Force garbage collection
            
            # Main segments (limit to 2)
            for i, segment in enumerate(script.get('segments', [])[:2]):  # Max 2 segments
                if segment_count >= max_segments:
                    break
                    
                audio_path = os.path.join(self.temp_dir, f"seg_{i}_{hash(str(segment)) % 1000}.mp3")
                temp_audio_files.append(audio_path)
                
                if self.generate_audio(segment['text'], audio_path):
                    clip = self.create_video_segment(
                        segment['text'], audio_path, segment.get('duration', 10)
                    )
                    if clip:
                        video_clips.append(clip)
                        segment_count += 1
                        gc.collect()
            
            # Combine clips
            if video_clips:
                logger.info(f"Combining {len(video_clips)} clips...")
                final_video = concatenate_videoclips(video_clips, method="compose")
                
                # Export with lower settings to save memory
                final_video.write_videofile(
                    output_path,
                    fps=24,
                    codec='libx264',
                    audio_codec='aac',
                    bitrate="500k",  # Lower bitrate
                    temp_audiofile=os.path.join(self.temp_dir, 'temp_audio.m4a'),
                    remove_temp=True,
                    threads=1,  # Single thread to reduce memory
                    logger=None
                )
                
                # Cleanup
                final_video.close()
                for clip in video_clips:
                    try:
                        clip.close()
                    except:
                        pass
                del video_clips
                
                # Remove temp files
                for audio_file in temp_audio_files:
                    try:
                        if os.path.exists(audio_file):
                            os.remove(audio_file)
                    except:
                        pass
                
                # Clean temp images
                for f in os.listdir(self.temp_dir):
                    if f.startswith('seg_') and f.endswith('.png'):
                        try:
                            os.remove(os.path.join(self.temp_dir, f))
                        except:
                            pass
                
                gc.collect()  # Final cleanup
                logger.info(f"Video created: {output_path}")
                return True
            else:
                logger.error("No clips created")
                return False
                
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def generate_video_from_script(self, script: Dict, output_filename: str = None) -> Optional[str]:
        """Main method to generate video"""
        try:
            if not output_filename:
                output_filename = f"video_{hash(str(script)) % 1000}.mp4"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            if self.create_short_form_video(script, output_path):
                logger.info(f"Video generated: {output_path}")
                return output_path
            else:
                logger.error("Failed to generate video")
                return None
                
        except Exception as e:
            logger.error(f"Error in video generation: {e}")
            return None