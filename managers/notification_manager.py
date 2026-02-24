"""
Notification Manager - Handles user notifications
"""
import logging
from datetime import datetime
from telegram import Bot
from telegram.ext import ContextTypes
from managers.user_manager import UserManager
from config import Config

logger = logging.getLogger(__name__)


class NotificationManager:
    """Manages notifications and reminders"""
    
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
        self.config = Config()
    
    async def check_inactive_users(self, context: ContextTypes.DEFAULT_TYPE):
        """Check for inactive users and send reminders"""
        try:
            inactive_users = await self.user_manager.get_inactive_users(
                self.config.STREAK_NOTIFICATION_HOURS
            )
            
            for user_id in inactive_users:
                try:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text="🔥 *Don't break your streak\\!*\n\n"
                             "You haven't practiced today\\. "
                             "Keep your learning momentum going\\! 💪\n\n"
                             "Tap /learn to continue your journey\\.",
                        parse_mode="MarkdownV2"
                    )
                    logger.info(f"✅ Sent reminder to user {user_id}")
                except Exception as e:
                    logger.error(f"❌ Failed to send reminder to {user_id}: {e}")
            
            if inactive_users:
                logger.info(f"📬 Sent {len(inactive_users)} streak reminders")
        
        except Exception as e:
            logger.error(f"❌ Error in check_inactive_users: {e}")
    
    async def send_achievement_notification(self, context: ContextTypes.DEFAULT_TYPE, 
                                           user_id: int, achievement_id: str):
        """Send achievement unlock notification"""
        try:
            achievement = self.config.ACHIEVEMENTS.get(achievement_id)
            if achievement:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"🎉 *Achievement Unlocked\\!*\n\n"
                         f"{achievement['name']}\n"
                         f"\\+{achievement['xp']} XP\n\n"
                         f"Keep up the great work\\!",
                    parse_mode="MarkdownV2"
                )
        except Exception as e:
            logger.error(f"❌ Failed to send achievement notification: {e}")
