"""
Profile Handler - Manages user profile and statistics
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from managers.user_manager import UserManager
from config import Config
from utils.formatter import escape_markdown

logger = logging.getLogger(__name__)


class ProfileHandler:
    """Handles user profile display and actions"""
    
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
        self.config = Config()
    
    async def show_profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Display user profile"""
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = update.effective_user.id
        else:
            user_id = update.effective_user.id
        
        # Get user data
        user = await self.user_manager.get_or_create_user(user_id)
        heart_info = await self.user_manager.update_hearts(user_id)
        
        # Get achievements
        achievements = await self.user_manager.get_achievements(user_id)
        achievement_text = ""
        if achievements:
            for ach_id in achievements[:5]:  # Show first 5
                if ach_id in self.config.ACHIEVEMENTS:
                    ach = self.config.ACHIEVEMENTS[ach_id]
                    achievement_text += f"{ach['name']}\n"
        else:
            achievement_text = "_No achievements yet_"
        
        # Get progress stats
        total_lessons = await self.user_manager.db.fetch_one(
            "SELECT COUNT(*) as count FROM progress WHERE user_id = ? AND completed = 1",
            (user_id,)
        )
        
        # Calculate level based on XP
        level = (user['xp'] // 100) + 1
        xp_for_next = ((level * 100) - user['xp'])
        
        hearts_display = "❤️" * heart_info['hearts'] + "🖤" * (self.config.MAX_HEARTS - heart_info['hearts'])
        
        text = (
            f"👤 *Profile: {escape_markdown(user['first_name'] or 'User')}*\n\n"
            f"🎚 Level: {level}\n"
            f"⭐️ XP: {user['xp']} \\({xp_for_next} to next level\\)\n"
            f"{hearts_display} Hearts: {heart_info['hearts']}/{self.config.MAX_HEARTS}\n"
            f"🔥 Streak: {user['streak']} days\n"
            f"📚 Lessons Completed: {total_lessons['count']}\n\n"
            f"*🏆 Achievements:*\n{achievement_text}"
        )
        
        keyboard = [
            [InlineKeyboardButton(
                f"🔔 Notifications: {'ON' if user['notification_enabled'] else 'OFF'}",
                callback_data="profile_toggle_notif"
            )],
            [InlineKeyboardButton("📊 Detailed Stats", callback_data="profile_stats")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")]
        ]
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="MarkdownV2"
            )
        else:
            await update.message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="MarkdownV2"
            )
    
    async def handle_profile_actions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle profile-related actions"""
        query = update.callback_query
        await query.answer()
        
        action = query.data.split("_", 1)[1]
        user_id = update.effective_user.id
        
        if action == "toggle_notif":
            # Toggle notifications
            user = await self.user_manager.get_or_create_user(user_id)
            new_state = 0 if user['notification_enabled'] else 1
            
            await self.user_manager.db.execute(
                "UPDATE users SET notification_enabled = ? WHERE user_id = ?",
                (new_state, user_id)
            )
            
            await query.answer(
                f"🔔 Notifications {'enabled' if new_state else 'disabled'}!",
                show_alert=True
            )
            
            # Refresh profile
            await self.show_profile(update, context)
        
        elif action == "stats":
            # Show detailed statistics
            await self._show_detailed_stats(query, user_id)
    
    async def _show_detailed_stats(self, query, user_id: int):
        """Show detailed user statistics"""
        user = await self.user_manager.get_or_create_user(user_id)
        
        # Get progress by language
        languages_data = []
        for lang_code in self.config.LANGUAGES.keys():
            progress = await self.user_manager.get_user_progress(user_id, lang_code)
            if progress['total_lessons'] > 0:
                lang_name = self.config.LANGUAGES[lang_code]['name']
                languages_data.append(
                    f"{lang_name}: {progress['total_lessons']} lessons"
                )
        
        lang_text = "\n".join(languages_data) if languages_data else "_No lessons completed_"
        
        # Get recent lessons
        recent = await self.user_manager.db.fetch_all(
            """SELECT language, lesson_id, score, completed_at 
               FROM progress WHERE user_id = ? AND completed = 1
               ORDER BY completed_at DESC LIMIT 5""",
            (user_id,)
        )
        
        recent_text = ""
        for item in recent:
            recent_text += f"• {item['lesson_id']}: {item['score']}%\n"
        
        if not recent_text:
            recent_text = "_No recent activity_"
        
        text = (
            f"📊 *Detailed Statistics*\n\n"
            f"*Progress by Language:*\n{lang_text}\n\n"
            f"*Recent Activity:*\n{recent_text}\n\n"
            f"*Account Info:*\n"
            f"Joined: {escape_markdown(user['created_at'][:10])}\n"
            f"Username: @{escape_markdown(user['username'] or 'N/A')}"
        )
        
        keyboard = [[InlineKeyboardButton("← Back to Profile", callback_data="menu_profile")]]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="MarkdownV2"
        )
