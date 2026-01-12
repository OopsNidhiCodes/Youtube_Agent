#!/usr/bin/env python3
"""
Free Video Generator Module
Uses local resources and free alternatives instead of paid services
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from moviepy.video.fx.all import fadein, fadeout
from gtts import gTTS
import tempfile
from typing import Dict, List, Optional
from logger import get_logger

logger = get_logger(__name__)

class FreeVideoGenerator:
    """Free video generator using local resources"""
    
    def __init__(self):
        self.temp_dir = "temp"
        self.output_dir = "output"
        self._setup_directories()
        # gTTS requires no system TTS engine; no initialization needed
    
    def _setup_directories(self):
        """Create necessary directories"""
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _setup_tts_engine(self):
        """Deprecated: pyttsx3 setup removed; using gTTS instead."""
        pass
    
    def generate_audio(self, text: str, output_path: str) -> bool:
        """Generate narration audio using gTTS (no system TTS required)."""
        try:
            # Ensure MP3 extension for gTTS
            base, ext = os.path.splitext(output_path)
            if ext.lower() != ".mp3":
                output_path = base + ".mp3"
            tts = gTTS(text=text, lang="en")
            tts.save(output_path)
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                logger.info(f"Audio generated successfully: {output_path}")
                return True
            logger.error("Audio file was not created properly")
            return False
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            return False
    
    def create_background_image(self, text: str, size: tuple = (1920, 1080), 
                              bg_color: tuple = (30, 30, 30)) -> Image.Image:
        """Create background image with text overlay"""
        try:
            # Create base image
            img = Image.new('RGB', size, bg_color)
            draw = ImageDraw.Draw(img)
            
            # Try to use a better font
            try:
                # Try system fonts
                font_paths = [
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                    "/System/Library/Fonts/Helvetica.ttc",
                    "C:\\Windows\\Fonts\\arial.ttf"
                ]
                
                font = None
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        try:
                            font = ImageFont.truetype(font_path, 60)
                            break
                        except:
                            continue
                
                if font is None:
                    font = ImageFont.load_default()
                    
            except:
                font = ImageFont.load_default()
            
            # Split text into multiple lines
            max_chars_per_line = 40
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > max_chars_per_line:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw text
            y_position = size[1] // 2 - (len(lines) * 80) // 2
            
            for line in lines:
                # Get text bounding box
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # Center text
                x_position = (size[0] - text_width) // 2
                
                # Add text shadow
                draw.text((x_position + 3, y_position + 3), line, 
                         font=font, fill=(0, 0, 0))
                
                # Add main text
                draw.text((x_position, y_position), line, 
                         font=font, fill=(255, 255, 255))
                
                y_position += text_height + 20
            
            # Add decorative elements
            self._add_decorative_elements(draw, size)
            
            logger.info("Background image created successfully")
            return img
            
        except Exception as e:
            logger.error(f"Error creating background image: {e}")
            # Return a simple colored image
            return Image.new('RGB', size, bg_color)
    
    def _add_decorative_elements(self, draw: ImageDraw.Draw, size: tuple):
        """Add decorative elements to the image"""
        try:
            # Add top and bottom borders
            border_color = (60, 60, 60)
            draw.rectangle([0, 0, size[0], 10], fill=border_color)
            draw.rectangle([0, size[1]-10, size[0], size[1]], fill=border_color)
            
            # Add corner decorations
            corner_size = 50
            corner_color = (100, 100, 100)
            
            # Top-left corner
            draw.rectangle([20, 20, 20+corner_size, 20+corner_size//4], fill=corner_color)
            draw.rectangle([20, 20, 20+corner_size//4, 20+corner_size], fill=corner_color)
            
            # Top-right corner
            draw.rectangle([size[0]-20-corner_size, 20, size[0]-20, 20+corner_size//4], fill=corner_color)
            draw.rectangle([size[0]-20-corner_size//4, 20, size[0]-20, 20+corner_size], fill=corner_color)
            
            # Bottom-left corner
            draw.rectangle([20, size[1]-20-corner_size//4, 20+corner_size, size[1]-20], fill=corner_color)
            draw.rectangle([20, size[1]-20-corner_size, 20+corner_size//4, size[1]-20], fill=corner_color)
            
            # Bottom-right corner
            draw.rectangle([size[0]-20-corner_size, size[1]-20-corner_size//4, size[0]-20, size[1]-20], fill=corner_color)
            draw.rectangle([size[0]-20-corner_size//4, size[1]-20-corner_size, size[0]-20, size[1]-20], fill=corner_color)
            
        except Exception as e:
            logger.warning(f"Could not add decorative elements: {e}")
    
    def create_video_segment(self, text: str, audio_path: str, duration: int, 
                           bg_color: tuple = (30, 30, 30)) -> Optional[ImageClip]:
        """Create a video segment with text and audio"""
        try:
            # Create background image
            img = self.create_background_image(text, bg_color=bg_color)
            
            # Save temporary image
            temp_img_path = os.path.join(self.temp_dir, f"temp_segment_{hash(text) % 10000}.png")
            img.save(temp_img_path)
            
            # Create video clip
            if os.path.exists(audio_path):
                # Use audio duration if available
                audio_clip = AudioFileClip(audio_path)
                actual_duration = audio_clip.duration
                
                video_clip = ImageClip(temp_img_path, duration=actual_duration)
                video_clip = video_clip.set_audio(audio_clip)
            else:
                # Use estimated duration
                video_clip = ImageClip(temp_img_path, duration=duration)
            
            # Add fade effects
            video_clip = fadein(video_clip, 0.5)
            video_clip = fadeout(video_clip, 0.5)
            
            # Clean up temporary image
            try:
                os.remove(temp_img_path)
            except:
                pass
            
            logger.info(f"Video segment created: {text[:50]}...")
            return video_clip
            
        except Exception as e:
            logger.error(f"Error creating video segment: {e}")
            return None
    
    def create_short_form_video(self, script: Dict, output_path: str, 
                              background_music: Optional[str] = None) -> bool:
        """Create short-form video using free resources"""
        try:
            logger.info("Creating free short-form video...")
            
            video_clips = []
            temp_audio_files = []
            
            # Generate hook segment
            if 'hook' in script:
                hook = script['hook']
                audio_path = os.path.join(self.temp_dir, f"hook_{hash(str(hook)) % 10000}.mp3")
                temp_audio_files.append(audio_path)
                
                if self.generate_audio(hook['text'], audio_path):
                    clip = self.create_video_segment(
                        hook['text'], 
                        audio_path, 
                        hook.get('duration', 5),
                        bg_color=(40, 60, 120)  # Different color for hook
                    )
                    if clip:
                        video_clips.append(clip)
            
            # Generate main content segments
            for i, segment in enumerate(script.get('segments', [])):
                audio_path = os.path.join(self.temp_dir, f"segment_{i}_{hash(str(segment)) % 10000}.mp3")
                temp_audio_files.append(audio_path)
                
                if self.generate_audio(segment['text'], audio_path):
                    clip = self.create_video_segment(
                        segment['text'],
                        audio_path,
                        segment.get('duration', 10)
                    )
                    if clip:
                        video_clips.append(clip)
            
            # Generate call-to-action segment
            if 'call_to_action' in script:
                cta = script['call_to_action']
                audio_path = os.path.join(self.temp_dir, f"cta_{hash(str(cta)) % 10000}.mp3")
                temp_audio_files.append(audio_path)
                
                if self.generate_audio(cta['text'], audio_path):
                    clip = self.create_video_segment(
                        cta['text'],
                        audio_path,
                        cta.get('duration', 5),
                        bg_color=(120, 60, 40)  # Different color for CTA
                    )
                    if clip:
                        video_clips.append(clip)
            
            # Combine all clips
            if video_clips:
                final_video = concatenate_videoclips(video_clips, method="compose")
                
                # Add background music if provided
                if background_music and os.path.exists(background_music):
                    try:
                        music = AudioFileClip(background_music).volumex(0.3)  # Lower volume
                        final_video = final_video.set_audio(
                            CompositeVideoClip([final_video.audio, music])
                        )
                    except Exception as e:
                        logger.warning(f"Could not add background music: {e}")
                
                # Export video
                final_video.write_videofile(
                    output_path,
                    fps=24,
                    codec='libx264',
                    audio_codec='aac',
                    temp_audiofile=os.path.join(self.temp_dir, 'temp_audio.m4a'),
                    remove_temp=True,
                    logger=None  # Suppress moviepy logs
                )
                
                # Clean up
                final_video.close()
                for clip in video_clips:
                    clip.close()
                
                # Clean up temporary audio files
                for audio_file in temp_audio_files:
                    try:
                        os.remove(audio_file)
                    except:
                        pass
                
                logger.info(f"Free video created successfully: {output_path}")
                return True
            else:
                logger.error("No video clips were created")
                return False
                
        except Exception as e:
            logger.error(f"Error creating free video: {e}")
            return False
    
    def add_subtitles_to_video(self, video_path: str, script: Dict, output_path: str) -> bool:
        """Add subtitles to video using OpenCV (free)"""
        try:
            logger.info("Adding subtitles to video...")
            
            # For now, return True as subtitles are complex with OpenCV
            # This is a placeholder for future implementation
            logger.info("Subtitles feature coming soon - video created without subtitles")
            
            # Copy video to output path
            import shutil
            shutil.copy2(video_path, output_path)
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding subtitles: {e}")
            return False
    
    def generate_video_from_script(self, script: Dict, output_filename: str = None) -> Optional[str]:
        """Main method to generate video from script"""
        try:
            if not output_filename:
                output_filename = f"video_{hash(str(script)) % 10000}.mp4"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Create video
            if self.create_short_form_video(script, output_path):
                logger.info(f"Video generated successfully: {output_path}")
                return output_path
            else:
                logger.error("Failed to generate video")
                return None
                
        except Exception as e:
            logger.error(f"Error in video generation: {e}")
            return None

# Test the free video generator
if __name__ == "__main__":
    generator = FreeVideoGenerator()
    
    # Test script
    test_script = {
        "hook": {"text": "Welcome to our tech channel! Today we're discussing Python programming tips.", "duration": 5},
        "segments": [
            {"text": "Python is one of the most popular programming languages today.", "duration": 8},
            {"text": "Here are three tips to improve your Python coding skills.", "duration": 10},
            {"text": "First, always use meaningful variable names for better code readability.", "duration": 12}
        ],
        "call_to_action": {"text": "Thanks for watching! Subscribe for more programming tips.", "duration": 5}
    }
    
    video_path = generator.generate_video_from_script(test_script)
    if video_path:
        print(f"Test video created: {video_path}")
    else:
        print("Failed to create test video")