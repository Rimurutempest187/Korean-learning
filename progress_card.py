#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Progress Card Generator for SUPER LEARNING BOT
Generates visual progress cards for users
"""

import io
import logging
from datetime import datetime, timedelta
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

logger = logging.getLogger(__name__)


class ProgressCardGenerator:
    """Generates progress cards and visualizations"""
    
    def __init__(self):
        self.width = 800
        self.height = 600
        self.background_color = (45, 52, 94)  # Dark blue
        self.accent_color = (88, 166, 255)  # Light blue
        self.text_color = (255, 255, 255)  # White
    
    def generate_card(self, user_id: int) -> Optional[bytes]:
        """Generate progress card for user"""
        
        try:
            # This is a simplified version
            # In production, would fetch real data and create detailed graphics
            
            # Create image
            img = Image.new('RGB', (self.width, self.height), self.background_color)
            draw = ImageDraw.Draw(img)
            
            # Load fonts (using default if custom not available)
            try:
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
                text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            # Draw title
            title = "📊 Learning Progress"
            draw.text((50, 50), title, fill=self.text_color, font=title_font)
            
            # Draw progress info (sample data)
            y_pos = 150
            stats = [
                "🔥 Streak: 15 days",
                "⭐ XP: 1,250",
                "📚 Lessons: 25",
                "🎯 Accuracy: 85%",
                "🏆 Level: 5"
            ]
            
            for stat in stats:
                draw.text((50, y_pos), stat, fill=self.text_color, font=text_font)
                y_pos += 50
            
            # Add footer
            footer = "SUPER LEARNING BOT • Create by: PINLON-YOUTH"
            draw.text((50, self.height - 50), footer, fill=self.accent_color, font=text_font)
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            return img_byte_arr.getvalue()
            
        except Exception as e:
            logger.error(f"Error generating progress card: {e}")
            return None
    
    def generate_weekly_chart(self, user_id: int) -> Optional[bytes]:
        """Generate weekly activity chart"""
        
        try:
            # Create sample data (would fetch from database in production)
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            minutes = [20, 30, 15, 25, 40, 10, 35]
            
            # Create chart
            plt.figure(figsize=(10, 6))
            plt.bar(days, minutes, color='#58A6FF')
            plt.xlabel('Day of Week')
            plt.ylabel('Minutes Studied')
            plt.title('Weekly Study Activity')
            plt.ylim(0, max(minutes) + 10)
            
            # Add value labels on bars
            for i, v in enumerate(minutes):
                plt.text(i, v + 1, str(v), ha='center')
            
            # Save to bytes
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            plt.close()
            
            return buf.getvalue()
            
        except Exception as e:
            logger.error(f"Error generating weekly chart: {e}")
            return None
    
    def generate_streak_calendar(self, user_id: int) -> Optional[bytes]:
        """Generate calendar showing streak"""
        
        try:
            # Would create a GitHub-style contribution calendar
            # Showing daily activity over past months
            
            # This is a placeholder
            return None
            
        except Exception as e:
            logger.error(f"Error generating streak calendar: {e}")
            return None
    
    def generate_badge_showcase(self, user_id: int) -> Optional[bytes]:
        """Generate image showing earned badges"""
        
        try:
            # Create image with badge collection
            img = Image.new('RGB', (800, 400), self.background_color)
            draw = ImageDraw.Draw(img)
            
            # Draw title
            title = "🏆 Your Badges"
            try:
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            except:
                title_font = ImageFont.load_default()
            
            draw.text((50, 30), title, fill=self.text_color, font=title_font)
            
            # Draw sample badges (would fetch from database)
            badges = ['👣', '🔥', '📚', '💬', '🎯']
            x_pos = 50
            y_pos = 120
            
            for badge in badges:
                draw.text((x_pos, y_pos), badge, font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60))
                x_pos += 120
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            return img_byte_arr.getvalue()
            
        except Exception as e:
            logger.error(f"Error generating badge showcase: {e}")
            return None
    
    def generate_level_progress(self, current_xp: int, next_level_xp: int) -> Optional[bytes]:
        """Generate level progress visualization"""
        
        try:
            # Create progress bar image
            img = Image.new('RGB', (600, 150), self.background_color)
            draw = ImageDraw.Draw(img)
            
            # Calculate progress
            if next_level_xp > 0:
                progress = (current_xp / next_level_xp) * 100
            else:
                progress = 100
            
            # Draw progress bar background
            bar_width = 500
            bar_height = 40
            bar_x = 50
            bar_y = 70
            
            draw.rectangle(
                [(bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height)],
                outline=self.text_color,
                width=2
            )
            
            # Draw progress fill
            fill_width = int((progress / 100) * bar_width)
            draw.rectangle(
                [(bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height)],
                fill=self.accent_color
            )
            
            # Draw text
            try:
                text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            except:
                text_font = ImageFont.load_default()
            
            text = f"{current_xp} / {next_level_xp} XP ({progress:.1f}%)"
            draw.text((bar_x, bar_y - 40), text, fill=self.text_color, font=text_font)
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            return img_byte_arr.getvalue()
            
        except Exception as e:
            logger.error(f"Error generating level progress: {e}")
            return None
