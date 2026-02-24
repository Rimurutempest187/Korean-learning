"""
Leaderboard Handler - Displays top users
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from managers.user_manager import UserManager
from utils.formatter import escape_markdown

logger = logging.getLogger(__name__)


class LeaderboardHandler:
    """Handles leaderboard display"""
    
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
    
    async def show_leaderboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Display top 10 users"""
        if update.callback_query:
            query = update.callback_query
            await query.answer()
        
        # Get top users
        top_users = await self.user_manager.get_leaderboard(10)
        
        if not top_users:
            text = "🏆 *Leaderboard*\n\nNo users yet\\. Be the first\\!"
        else:
            text = "🏆 *Top 10 Learners*\n\n"
            
            medals = ["🥇", "🥈", "🥉"]
            
            for idx, user in enumerate(top_users, 1):
                medal = medals[idx - 1] if idx <= 3 else f"{idx}\\."
                name = escape_markdown(user['first_name'] or user['username'] or 'User')
                xp = user['xp']
                streak = user['streak']
                
                text += f"{medal} {name}\n"
                text += f"   ⭐️ {xp} XP • 🔥 {streak} days\n\n"
            
            # Show current user's rank
            user_id = update.effective_user.id
            user = await self.user_manager.get_or_create_user(user_id)
            
            # Calculate user's rank
            all_users = await self.user_manager.db.fetch_all(
                "SELECT user_id FROM users ORDER BY xp DESC"
            )
            user_rank = next((i + 1 for i, u in enumerate(all_users) if u['user_id'] == user_id), None)
            
            if user_rank:
                text += f"*Your Rank:* #{user_rank}\n"
                text += f"Your XP: {user['xp']}"
        
        keyboard = [[InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")]]
        
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
