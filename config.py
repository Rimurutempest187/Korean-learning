"""
Configuration Management
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Centralized configuration"""
    
    # Bot Configuration
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
    
    # Database Configuration
    DB_PATH = os.getenv("DB_PATH", "language_bot.db")
    
    # Game Configuration
    MAX_HEARTS = 5
    HEART_REFILL_HOURS = 4
    XP_PER_CORRECT_ANSWER = 10
    XP_PER_LESSON_COMPLETE = 50
    STREAK_NOTIFICATION_HOURS = 24
    
    # Lesson Configuration
    LANGUAGES = {
        "english": {
            "name": "English 🇬🇧",
            "code": "en",
            "target": "my"
        },
        "japanese": {
            "name": "Japanese 🇯🇵",
            "code": "ja",
            "target": "my"
        },
        "korean": {
            "name": "Korean 🇰🇷",
            "code": "ko",
            "target": "my"
        }
    }
    
    UNITS = ["beginner", "intermediate", "advanced"]
    
    # Achievements
    ACHIEVEMENTS = {
        "first_lesson": {"name": "🎓 First Steps", "xp": 100, "requirement": 1},
        "streak_7": {"name": "🔥 Week Warrior", "xp": 200, "requirement": 7},
        "streak_30": {"name": "🏆 Monthly Master", "xp": 500, "requirement": 30},
        "lessons_10": {"name": "📚 Bookworm", "xp": 300, "requirement": 10},
        "lessons_50": {"name": "🌟 Scholar", "xp": 1000, "requirement": 50},
        "perfect_quiz": {"name": "💯 Perfect Score", "xp": 150, "requirement": 1}
    }
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN environment variable is required")
        if cls.ADMIN_ID == 0:
            raise ValueError("ADMIN_ID environment variable is required")
