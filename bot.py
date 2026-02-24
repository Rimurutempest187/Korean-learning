"""
Language Learning Ecosystem Telegram Bot
Main Entry Point
"""
import os
import logging
import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from handlers.start_handler import StartHandler
from handlers.lesson_handler import LessonHandler
from handlers.quiz_handler import QuizHandler
from handlers.profile_handler import ProfileHandler
from handlers.leaderboard_handler import LeaderboardHandler
from handlers.admin_handler import AdminHandler
from managers.database_manager import DatabaseManager
from managers.user_manager import UserManager
from managers.notification_manager import NotificationManager
from utils.error_handler import error_handler
from config import Config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class LanguageLearningBot:
    """Main bot class orchestrating all components"""
    
    def __init__(self):
        self.config = Config()
        self.db_manager = None
        self.user_manager = None
        self.notification_manager = None
        
    async def initialize(self):
        """Initialize database and managers"""
        self.db_manager = DatabaseManager(self.config.DB_PATH)
        await self.db_manager.initialize()
        
        self.user_manager = UserManager(self.db_manager)
        self.notification_manager = NotificationManager(self.user_manager)
        
        logger.info("✅ Bot initialized successfully")
    
    async def setup_handlers(self, application: Application):
        """Register all command and callback handlers"""
        
        # Initialize handlers
        start_handler = StartHandler(self.user_manager)
        lesson_handler = LessonHandler(self.user_manager)
        quiz_handler = QuizHandler(self.user_manager)
        profile_handler = ProfileHandler(self.user_manager)
        leaderboard_handler = LeaderboardHandler(self.user_manager)
        admin_handler = AdminHandler(self.user_manager, self.config)
        
        # Command handlers
        application.add_handler(CommandHandler("start", start_handler.start))
        application.add_handler(CommandHandler("help", start_handler.help_command))
        application.add_handler(CommandHandler("learn", lesson_handler.learn_menu))
        application.add_handler(CommandHandler("profile", profile_handler.show_profile))
        application.add_handler(CommandHandler("top", leaderboard_handler.show_leaderboard))
        application.add_handler(CommandHandler("backup", admin_handler.backup_db))
        application.add_handler(CommandHandler("restore", admin_handler.restore_db))
        
        # Callback query handlers
        application.add_handler(CallbackQueryHandler(
            lesson_handler.handle_language_selection,
            pattern="^lang_"
        ))
        application.add_handler(CallbackQueryHandler(
            lesson_handler.handle_unit_selection,
            pattern="^unit_"
        ))
        application.add_handler(CallbackQueryHandler(
            lesson_handler.handle_lesson_selection,
            pattern="^lesson_"
        ))
        application.add_handler(CallbackQueryHandler(
            quiz_handler.handle_quiz_start,
            pattern="^quiz_"
        ))
        application.add_handler(CallbackQueryHandler(
            quiz_handler.handle_answer,
            pattern="^answer_"
        ))
        application.add_handler(CallbackQueryHandler(
            profile_handler.handle_profile_actions,
            pattern="^profile_"
        ))
        application.add_handler(CallbackQueryHandler(
            start_handler.handle_main_menu,
            pattern="^menu_"
        ))
        
        # Message handler for text input (translation practice)
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            quiz_handler.handle_text_answer
        ))
        
        # Error handler
        application.add_error_handler(error_handler)
        
        logger.info("✅ All handlers registered")
    
    async def setup_jobs(self, application: Application):
        """Setup periodic jobs for notifications and maintenance"""
        job_queue = application.job_queue
        
        # Check for inactive users every hour
        job_queue.run_repeating(
            self.notification_manager.check_inactive_users,
            interval=timedelta(hours=1),
            first=timedelta(seconds=10)
        )
        
        # Daily cleanup job (midnight UTC)
        job_queue.run_daily(
            self.daily_maintenance,
            time=datetime.strptime("00:00", "%H:%M").time()
        )
        
        logger.info("✅ Job queue configured")
    
    async def daily_maintenance(self, context: ContextTypes.DEFAULT_TYPE):
        """Daily maintenance tasks"""
        try:
            # Reset daily challenges, update streaks, etc.
            await self.user_manager.reset_hearts_for_all()
            logger.info("✅ Daily maintenance completed")
        except Exception as e:
            logger.error(f"❌ Daily maintenance failed: {e}")
    
    async def run(self):
        """Start the bot"""
        try:
            # Initialize bot components
            await self.initialize()
            
            # Build application
            application = (
                Application.builder()
                .token(self.config.BOT_TOKEN)
                .build()
            )
            
            # Setup handlers and jobs
            await self.setup_handlers(application)
            await self.setup_jobs(application)
            
            # Start bot
            logger.info("🚀 Starting Language Learning Bot...")
            await application.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
            raise


def main():
    """Entry point"""
    bot = LanguageLearningBot()
    asyncio.run(bot.run())


if __name__ == "__main__":
    main()
