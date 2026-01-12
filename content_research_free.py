#!/usr/bin/env python3
"""
Free Content Research Module
Uses Hugging Face models and RSS feeds instead of OpenAI API
"""

import json
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import feedparser
from bs4 import BeautifulSoup
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from logger import get_logger

logger = get_logger(__name__)

class FreeContentResearcher:
    """Free content research using Hugging Face models and RSS feeds"""
    
    def __init__(self):
        self.device = "cpu"  # Use CPU for free deployment
        self.tokenizer = None
        self.model = None
        self.text_generator = None
        self._setup_models()
    
    def _setup_models(self):
        """Setup free Hugging Face models"""
        try:
            # Use a smaller, faster model for text generation
            model_name = "microsoft/DialoGPT-medium"  # Free and fast
            
            logger.info("Loading free Hugging Face model...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float32,  # CPU compatible
                device_map="cpu"
            )
            
            # Setup text generation pipeline
            self.text_generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1  # CPU
            )
            
            logger.info("Free AI models loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load free AI models: {e}")
            # Fallback to rule-based content generation
            logger.info("Using fallback rule-based content generation")
    
    def get_trending_tech_topics(self) -> List[str]:
        """Get trending tech topics from free RSS feeds"""
        topics = []
        
        try:
            # Free tech RSS feeds
            feeds = [
                "https://feeds.feedburner.com/oreilly/radar",
                "https://techcrunch.com/feed/",
                "https://www.wired.com/feed/rss",
                "https://feeds.arstechnica.com/arstechnica/index",
                "https://www.theverge.com/rss/index.xml"
            ]
            
            logger.info("Fetching trending topics from RSS feeds...")
            
            for feed_url in feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:5]:  # Top 5 from each feed
                        # Extract keywords from title
                        title = entry.title.lower()
                        if any(tech_word in title for tech_word in [
                            'ai', 'artificial intelligence', 'machine learning', 'ml',
                            'python', 'programming', 'coding', 'software',
                            'technology', 'tech', 'startup', 'innovation',
                            'blockchain', 'crypto', 'cybersecurity', 'cloud'
                        ]):
                            topics.append(entry.title)
                            
                except Exception as e:
                    logger.warning(f"Failed to parse feed {feed_url}: {e}")
                    continue
            
            # Remove duplicates and limit to top 10
            unique_topics = list(set(topics))[:10]
            logger.info(f"Found {len(unique_topics)} trending tech topics")
            
            return unique_topics if unique_topics else self._get_fallback_topics()
            
        except Exception as e:
            logger.error(f"Error fetching trending topics: {e}")
            return self._get_fallback_topics()
    
    def _get_fallback_topics(self) -> List[str]:
        """Fallback topics if RSS feeds fail"""
        return [
            "Python Programming Tips for Beginners",
            "Machine Learning Basics Explained",
            "How to Start Coding in 2024",
            "Best Programming Languages to Learn",
            "Understanding Artificial Intelligence",
            "Web Development Fundamentals",
            "Cybersecurity Best Practices",
            "Cloud Computing Explained Simply",
            "Mobile App Development Trends",
            "Data Science Career Guide"
        ]
    
    def generate_video_script(self, topic: str, video_length: int = 60) -> Dict:
        """Generate video script using free Hugging Face models"""
        try:
            if self.text_generator:
                # Generate script using AI
                prompt = f"""Create a {video_length}-second video script about: {topic}
                
Include:
1. Hook/introduction (5-10 seconds)
2. Main content points (40-50 seconds)
3. Call to action (5-10 seconds)

Format with timestamps and visual cues."""

                response = self.text_generator(
                    prompt,
                    max_length=500,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True
                )
                
                script_content = response[0]['generated_text']
                
            else:
                # Fallback rule-based generation
                script_content = self._generate_rule_based_script(topic, video_length)
            
            # Parse script into structured format
            script = self._parse_script(script_content, topic)
            
            logger.info(f"Generated script for topic: {topic}")
            return script
            
        except Exception as e:
            logger.error(f"Error generating script: {e}")
            return self._generate_fallback_script(topic, video_length)
    
    def _generate_rule_based_script(self, topic: str, video_length: int) -> str:
        """Generate script using templates and rules"""
        templates = {
            "introduction": [
                f"Welcome to our tech channel! Today we're discussing: {topic}",
                f"Hey tech enthusiasts! Let's explore {topic}",
                f"In this video, we'll dive into {topic}"
            ],
            "main_points": [
                "First, let's understand the basics...",
                "Here are the key points you need to know...",
                "The most important aspects include..."
            ],
            "conclusion": [
                "Thanks for watching! Don't forget to subscribe for more tech content.",
                "I hope you learned something new today. See you in the next video!",
                "If you found this helpful, please like and subscribe!"
            ]
        }
        
        script = f"""0:00 - {self._get_random_item(templates['introduction'])}
0:05 - {self._get_random_item(templates['main_points'])}
0:30 - Key insights and practical tips
0:50 - {self._get_random_item(templates['conclusion'])}"""
        
        return script
    
    def _parse_script(self, script_content: str, topic: str) -> Dict:
        """Parse script content into structured format"""
        lines = script_content.split('\n')
        segments = []
        
        current_time = 0
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Try to extract timestamp
                if ':' in line and line[0].isdigit():
                    # Line has timestamp
                    parts = line.split(' - ', 1)
                    if len(parts) == 2:
                        time_str = parts[0].strip()
                        content = parts[1].strip()
                        
                        # Convert time to seconds
                        try:
                            if ':' in time_str:
                                minutes, seconds = map(int, time_str.split(':'))
                                current_time = minutes * 60 + seconds
                        except:
                            current_time += 10  # Default 10 second segments
                        
                        segments.append({
                            "timestamp": current_time,
                            "text": content,
                            "duration": 10,
                            "visual_cue": self._get_visual_cue(content)
                        })
                else:
                    # No timestamp, add with estimated time
                    segments.append({
                        "timestamp": current_time,
                        "text": line,
                        "duration": 8,
                        "visual_cue": self._get_visual_cue(line)
                    })
                    current_time += 8
        
        return {
            "title": topic,
            "hook": segments[0] if segments else {"text": topic, "duration": 5},
            "segments": segments[1:] if len(segments) > 1 else [],
            "call_to_action": segments[-1] if segments else {"text": "Thanks for watching!", "duration": 5},
            "total_duration": sum(seg["duration"] for seg in segments) if segments else 60
        }
    
    def _get_visual_cue(self, text: str) -> str:
        """Generate visual cues based on text content"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['introduce', 'welcome', 'hey', 'hello']):
            return "animated_text"
        elif any(word in text_lower for word in ['show', 'demonstrate', 'example']):
            return "code_example"
        elif any(word in text_lower for word in ['tip', 'trick', 'secret']):
            return "highlight_text"
        elif any(word in text_lower for word in ['subscribe', 'like', 'follow']):
            return "call_to_action"
        else:
            return "simple_text"
    
    def _get_random_item(self, items: List[str]) -> str:
        """Get random item from list"""
        import random
        return random.choice(items)
    
    def _generate_fallback_script(self, topic: str, video_length: int) -> Dict:
        """Generate fallback script"""
        return {
            "title": topic,
            "hook": {"text": f"Today we're discussing {topic}", "duration": 5},
            "segments": [
                {"text": "Let's start with the basics", "duration": 10, "visual_cue": "simple_text"},
                {"text": "Here are the key points", "duration": 15, "visual_cue": "highlight_text"},
                {"text": "Important tips to remember", "duration": 10, "visual_cue": "tip_text"}
            ],
            "call_to_action": {"text": "Thanks for watching! Subscribe for more tech content.", "duration": 5},
            "total_duration": 45
        }
    
    def generate_video_idea(self) -> Dict:
        """Generate a complete video idea using free methods"""
        logger.info("Generating free video idea...")
        
        # Get trending topics
        topics = self.get_trending_tech_topics()
        if not topics:
            topics = self._get_fallback_topics()
        
        # Select random topic
        import random
        selected_topic = random.choice(topics)
        
        # Generate script
        script = self.generate_video_script(selected_topic)
        
        return {
            "topic": selected_topic,
            "script": script,
            "keywords": self._extract_keywords(selected_topic),
            "tags": self._generate_tags(selected_topic),
            "description": self._generate_description(selected_topic, script)
        }
    
    def _extract_keywords(self, topic: str) -> List[str]:
        """Extract keywords from topic"""
        # Simple keyword extraction
        words = topic.lower().split()
        keywords = [word.strip('.,!?') for word in words if len(word) > 3]
        return keywords[:5]  # Top 5 keywords
    
    def _generate_tags(self, topic: str) -> List[str]:
        """Generate YouTube tags"""
        base_tags = ["technology", "tech", "programming", "coding", "tutorial"]
        topic_tags = self._extract_keywords(topic)
        return base_tags + topic_tags[:5]
    
    def _generate_description(self, topic: str, script: Dict) -> str:
        """Generate video description"""
        description = f"In this video, we explore {topic}. "
        
        if script and 'segments' in script:
            description += "We cover key concepts and practical insights. "
        
        description += "\n\n🎯 Key Topics Covered:\n"
        description += f"• {topic}\n"
        description += "• Technology insights\n"
        description += "• Practical applications\n\n"
        
        description += "🔔 Don't forget to subscribe for more tech content!\n"
        description += "💬 Let us know your thoughts in the comments.\n\n"
        
        description += "#technology #tech #programming #coding #tutorial"
        
        return description

# Test the free content researcher
if __name__ == "__main__":
    researcher = FreeContentResearcher()
    idea = researcher.generate_video_idea()
    print(json.dumps(idea, indent=2))