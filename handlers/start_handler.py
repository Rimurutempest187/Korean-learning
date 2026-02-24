"""
Start Handler - Handles /start and /help commands
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from managers.user_manager import UserManager
from utils.formatter import escape_markdown

logger = logging.getLogger(__name__)


class StartHandler:
    """Handles bot initialization and main menu"""
    
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        await self.user_manager.get_or_create_user(
            user.id, user.username, user.first_name
        )
        
        # Update hearts
        heart_info = await self.user_manager.update_hearts(user.id)
        
        welcome_text = (
            f"🌟 *Welcome to Language Learning Bot\\!*\n\n"
            f"Learn English 🇬🇧, Japanese 🇯🇵, or Korean 🇰🇷 "
            f"translated to Myanmar 🇲🇲\n\n"
            f"*Your Stats:*\n"
            f"❤️ Hearts: {heart_info['hearts']}/5\n"
            f"⭐️ XP: 0\n"
            f"🔥 Streak: 0 days\n\n"
            f"Ready to start your learning journey?"
        )
        
        keyboard = [
            [InlineKeyboardButton("📚 Start Learning", callback_data="menu_learn")],
            [InlineKeyboardButton("👤 My Profile", callback_data="menu_profile")],
            [InlineKeyboardButton("🏆 Leaderboard", callback_data="menu_leaderboard")],
            [InlineKeyboardButton("❓ Help", callback_data="menu_help")]
        ]
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="MarkdownV2"
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = (
            "*📖 How to Use This Bot*\n\n"
            "*Commands:*\n"
            "`/start` \\- Start the bot\n"
            "`/learn` \\- Browse lessons\n"
            "`/profile` \\- View your profile\n"
            "`/top` \\- View leaderboard\n\n"
            "*Game Mechanics:*\n"
            "❤️ *Hearts:* You have 5 hearts\\. Wrong answers cost 1 heart\\. "
            "Hearts refill every 4 hours\\.\n\n"
            "⭐️ *XP:* Earn XP by completing lessons and quizzes\\. "
            "Correct answers: \\+10 XP, Lesson complete: \\+50 XP\\.\n\n"
            "🔥 *Streak:* Practice daily to maintain your streak\\. "
            "We'll remind you if you miss a day\\!\n\n"
            "🏆 *Achievements:* Unlock badges by reaching milestones\\.\n\n"
            "*Tips:*\n"
            "• Complete easier lessons first to build XP\n"
            "• Don't lose all your hearts \\- practice carefully\\!\n"
            "• Maintain your streak for bonus XP\n"
            "• Compete with friends on the leaderboard\\!"
        )
        
        keyboard = [[InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")]]
        
        await update.message.reply_text(
            help_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="MarkdownV2"
        )
    
    async def handle_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle main menu callbacks"""
        query = update.callback_query
        await query.answer()
        
        action = query.data.split("_")[1]
        
        if action == "learn":
            from handlers.lesson_handler import LessonHandler
            handler = LessonHandler(self.user_manager)
            await handler.learn_menu(update, context)
        
        elif action == "profile":
            from handlers.profile_handler import ProfileHandler
            handler = ProfileHandler(self.user_manager)
            await handler.show_profile(update, context)
        
        elif action == "leaderboard":
            from handlers.leaderboard_handler import LeaderboardHandler
            handler = LeaderboardHandler(self.user_manager)
            await handler.show_leaderboard(update, context)
        
        elif action == "help":
            help_text = (
                "*📖 Bot Guide*\n\n"
                "Use inline buttons to navigate through lessons\\. "
                "Answer quiz questions to earn XP and progress\\.\n\n"
                "Good luck with your learning\\! 🚀"
            )
            keyboard = [[InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")]]
            await query.edit_message_text(
                help_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="MarkdownV2"
            )
        
        elif action == "main":
            user = update.effective_user
            user_data = await self.user_manager.get_or_create_user(user.id)
            heart_info = await self.user_manager.update_hearts(user.id)
            
            welcome_text = (
                f"🌟 *Language Learning Bot*\n\n"
                f"*Your Stats:*\n"
                f"❤️ Hearts: {heart_info['hearts']}/5\n"
                f"⭐️ XP: {user_data['xp']}\n"
                f"🔥 Streak: {user_data['streak']} days\n\n"
                f"What would you like to do?"
            )
            
            keyboard = [
                [InlineKeyboardButton("📚 Start Learning", callback_data="menu_learn")],
                [InlineKeyboardButton("👤 My Profile", callback_data="menu_profile")],
                [InlineKeyboardButton("🏆 Leaderboard", callback_data="menu_leaderboard")]
            ]
            
            await query.edit_message_text(
                welcome_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="MarkdownV2"
            )
