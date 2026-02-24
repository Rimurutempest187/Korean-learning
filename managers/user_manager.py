"""
User Manager - Handles user-related operations
"""
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from managers.database_manager import DatabaseManager
from config import Config

logger = logging.getLogger(__name__)


class UserManager:
    """Manages user data and game mechanics"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.config = Config()
    
    async def get_or_create_user(self, user_id: int, username: str = None, 
                                 first_name: str = None) -> Dict[str, Any]:
        """Get existing user or create new one"""
        user = await self.db.fetch_one(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        
        if not user:
            await self.db.execute(
                """INSERT INTO users (user_id, username, first_name, last_active, last_heart_refill)
                   VALUES (?, ?, ?, ?, ?)""",
                (user_id, username, first_name, datetime.now().isoformat(), 
                 datetime.now().isoformat())
            )
            user = await self.db.fetch_one(
                "SELECT * FROM users WHERE user_id = ?",
                (user_id,)
            )
            logger.info(f"✅ New user created: {user_id}")
        
        return user
    
    async def update_hearts(self, user_id: int) -> Dict[str, Any]:
        """Check and refill hearts if enough time has passed"""
        user = await self.db.fetch_one(
            "SELECT hearts, last_heart_refill FROM users WHERE user_id = ?",
            (user_id,)
        )
        
        if user['hearts'] < self.config.MAX_HEARTS:
            last_refill = datetime.fromisoformat(user['last_heart_refill'])
            now = datetime.now()
            hours_passed = (now - last_refill).total_seconds() / 3600
            
            if hours_passed >= self.config.HEART_REFILL_HOURS:
                new_hearts = min(self.config.MAX_HEARTS, 
                               user['hearts'] + int(hours_passed / self.config.HEART_REFILL_HOURS))
                await self.db.execute(
                    "UPDATE users SET hearts = ?, last_heart_refill = ? WHERE user_id = ?",
                    (new_hearts, now.isoformat(), user_id)
                )
                return {"hearts": new_hearts, "refilled": True}
        
        return {"hearts": user['hearts'], "refilled": False}
    
    async def lose_heart(self, user_id: int) -> int:
        """Decrease heart count"""
        user = await self.db.fetch_one(
            "SELECT hearts FROM users WHERE user_id = ?",
            (user_id,)
        )
        new_hearts = max(0, user['hearts'] - 1)
        await self.db.execute(
            "UPDATE users SET hearts = ? WHERE user_id = ?",
            (new_hearts, user_id)
        )
        return new_hearts
    
    async def add_xp(self, user_id: int, xp: int) -> int:
        """Add XP to user"""
        user = await self.db.fetch_one(
            "SELECT xp FROM users WHERE user_id = ?",
            (user_id,)
        )
        new_xp = user['xp'] + xp
        await self.db.execute(
            "UPDATE users SET xp = ? WHERE user_id = ?",
            (new_xp, user_id)
        )
        logger.info(f"➕ User {user_id} gained {xp} XP (Total: {new_xp})")
        return new_xp
    
    async def update_streak(self, user_id: int) -> int:
        """Update user's daily streak"""
        user = await self.db.fetch_one(
            "SELECT streak, last_active FROM users WHERE user_id = ?",
            (user_id,)
        )
        
        last_active = datetime.fromisoformat(user['last_active'])
        now = datetime.now()
        days_diff = (now.date() - last_active.date()).days
        
        if days_diff == 0:
            # Same day, no change
            new_streak = user['streak']
        elif days_diff == 1:
            # Consecutive day, increment
            new_streak = user['streak'] + 1
        else:
            # Streak broken
            new_streak = 1
        
        await self.db.execute(
            "UPDATE users SET streak = ?, last_active = ? WHERE user_id = ?",
            (new_streak, now.isoformat(), user_id)
        )
        
        return new_streak
    
    async def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top users by XP"""
        return await self.db.fetch_all(
            """SELECT user_id, username, first_name, xp, streak
               FROM users
               ORDER BY xp DESC
               LIMIT ?""",
            (limit,)
        )
    
    async def complete_lesson(self, user_id: int, language: str, 
                             unit: str, lesson_id: str, score: int):
        """Mark lesson as completed"""
        await self.db.execute(
            """INSERT OR REPLACE INTO progress 
               (user_id, language, unit, lesson_id, completed, score, completed_at)
               VALUES (?, ?, ?, ?, 1, ?, ?)""",
            (user_id, language, unit, lesson_id, score, datetime.now().isoformat())
        )
        
        # Award XP
        await self.add_xp(user_id, self.config.XP_PER_LESSON_COMPLETE)
        
        # Update streak
        await self.update_streak(user_id)
    
    async def get_user_progress(self, user_id: int, language: str) -> Dict[str, Any]:
        """Get user's progress for a language"""
        completed = await self.db.fetch_all(
            """SELECT unit, lesson_id, score, completed_at
               FROM progress
               WHERE user_id = ? AND language = ? AND completed = 1
               ORDER BY completed_at DESC""",
            (user_id, language)
        )
        
        return {
            "total_lessons": len(completed),
            "lessons": completed
        }
    
    async def unlock_achievement(self, user_id: int, achievement_id: str) -> bool:
        """Unlock an achievement for user"""
        try:
            await self.db.execute(
                "INSERT INTO achievements (user_id, achievement_id) VALUES (?, ?)",
                (user_id, achievement_id)
            )
            
            # Award achievement XP
            if achievement_id in self.config.ACHIEVEMENTS:
                xp = self.config.ACHIEVEMENTS[achievement_id]['xp']
                await self.add_xp(user_id, xp)
            
            return True
        except:
            return False  # Already unlocked
    
    async def get_achievements(self, user_id: int) -> List[str]:
        """Get user's unlocked achievements"""
        achievements = await self.db.fetch_all(
            "SELECT achievement_id FROM achievements WHERE user_id = ?",
            (user_id,)
        )
        return [a['achievement_id'] for a in achievements]
    
    async def get_inactive_users(self, hours: int) -> List[int]:
        """Get users inactive for specified hours"""
        threshold = (datetime.now() - timedelta(hours=hours)).isoformat()
        users = await self.db.fetch_all(
            """SELECT user_id FROM users 
               WHERE last_active < ? AND notification_enabled = 1""",
            (threshold,)
        )
        return [u['user_id'] for u in users]
    
    async def reset_hearts_for_all(self):
        """Reset hearts to max for all users (daily maintenance)"""
        await self.db.execute(
            f"UPDATE users SET hearts = {self.config.MAX_HEARTS}, last_heart_refill = ?",
            (datetime.now().isoformat(),)
        )
