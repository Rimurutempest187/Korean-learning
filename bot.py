#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUPER LEARNING BOT - Universal Language Learning Telegram Bot
Create by: PINLON-YOUTH
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import json
import random

from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode

# Database imports
from database import Database
from models import User, Lesson, Vocabulary, Quiz, Progress
from ai_tutor import AITutor
from content_manager import ContentManager
from gamification import GamificationEngine
from progress_card import ProgressCardGenerator
from scheduler import DailyScheduler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
SELECTING_LANGUAGE, LEVEL_TEST, GOAL_SETTING = range(3)

# Available languages
AVAILABLE_LANGUAGES = {
    'en': '🇺🇸 English',
    'ko': '🇰🇷 Korean',
    'ja': '🇯🇵 Japanese',
    'zh': '🇨🇳 Chinese',
    'es': '🇪🇸 Spanish',
    'fr': '🇫🇷 French',
    'de': '🇩🇪 German',
    'th': '🇹🇭 Thai',
    'my': '🇲🇲 Myanmar'
}

# Proficiency levels
LEVELS = ['Beginner', 'Elementary', 'Intermediate', 'Upper-Intermediate', 'Advanced']

# Initialize components
db = Database()
ai_tutor = AITutor()
content_manager = ContentManager()
gamification = GamificationEngine()
progress_card_gen = ProgressCardGenerator()
scheduler = DailyScheduler()


class SuperLearningBot:
    """Main bot class"""
    
    def __init__(self):
        self.db = db
        self.ai_tutor = ai_tutor
        self.content_manager = content_manager
        self.gamification = gamification
        
    # ==================== MAIN MENU ====================
    
    def get_main_menu_keyboard(self, user_id: int) -> ReplyKeyboardMarkup:
        """Generate main menu keyboard"""
        keyboard = [
            ['📚 Learn', '🧠 Review'],
            ['💬 AI Tutor', '📊 Progress'],
            ['🎯 Quiz', '📖 Vocabulary'],
            ['⚙️ Settings', '❓ Help']
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command - Onboarding"""
        user_id = update.effective_user.id
        username = update.effective_user.first_name
        
        # Check if user exists
        user = self.db.get_user(user_id)
        
        if user:
            # Returning user
            await update.message.reply_text(
                f"Welcome back, {username}! 🎉\n\n"
                f"Ready to continue your learning journey?\n"
                f"Current streak: {user['streak']} days 🔥",
                reply_markup=self.get_main_menu_keyboard(user_id)
            )
        else:
            # New user - Start onboarding
            welcome_text = (
                "🌍 *SUPER LEARNING BOT*\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "Welcome to your personal language learning assistant! 🚀\n\n"
                "I'll help you:\n"
                "✅ Learn languages effectively\n"
                "✅ Practice daily with AI tutor\n"
                "✅ Track your progress\n"
                "✅ Achieve your goals\n\n"
                "Let's start by choosing your learning language:\n\n"
                "_Create by: PINLON-YOUTH_"
            )
            
            # Language selection keyboard
            keyboard = []
            lang_items = list(AVAILABLE_LANGUAGES.items())
            for i in range(0, len(lang_items), 2):
                row = []
                for j in range(2):
                    if i + j < len(lang_items):
                        code, name = lang_items[i + j]
                        row.append(InlineKeyboardButton(name, callback_data=f"lang_{code}"))
                keyboard.append(row)
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                welcome_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            
            return SELECTING_LANGUAGE
    
    async def language_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle language selection"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        username = query.from_user.first_name
        lang_code = query.data.split('_')[1]
        
        # Save to context
        context.user_data['learning_language'] = lang_code
        
        # Ask for level
        level_text = (
            f"Great choice! You're learning {AVAILABLE_LANGUAGES[lang_code]} 🎯\n\n"
            "What's your current level?"
        )
        
        keyboard = []
        for level in LEVELS:
            keyboard.append([InlineKeyboardButton(level, callback_data=f"level_{level}")])
        keyboard.append([InlineKeyboardButton("📝 Take Level Test", callback_data="level_test")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            level_text,
            reply_markup=reply_markup
        )
        
        return LEVEL_TEST
    
    async def level_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle level selection"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        data = query.data
        
        if data == "level_test":
            # Start level test
            await query.edit_message_text("📝 Level test feature coming soon!")
            level = "Beginner"
        else:
            level = data.split('_')[1]
        
        context.user_data['level'] = level
        
        # Ask for daily goal
        goal_text = (
            "Perfect! 🎯\n\n"
            "How much time can you dedicate daily?"
        )
        
        keyboard = [
            [InlineKeyboardButton("5 minutes", callback_data="goal_5")],
            [InlineKeyboardButton("10 minutes", callback_data="goal_10")],
            [InlineKeyboardButton("20 minutes", callback_data="goal_20")],
            [InlineKeyboardButton("30 minutes", callback_data="goal_30")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            goal_text,
            reply_markup=reply_markup
        )
        
        return GOAL_SETTING
    
    async def goal_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle goal setting and complete onboarding"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        username = query.from_user.first_name
        goal_minutes = int(query.data.split('_')[1])
        
        # Create user in database
        user_data = {
            'user_id': user_id,
            'username': username,
            'learning_language': context.user_data['learning_language'],
            'level': context.user_data['level'],
            'daily_goal_minutes': goal_minutes,
            'xp': 0,
            'streak': 0,
            'total_lessons': 0
        }
        
        self.db.create_user(user_data)
        
        # Send welcome message
        welcome_complete = (
            "🎉 *Setup Complete!*\n\n"
            f"Learning: {AVAILABLE_LANGUAGES[context.user_data['learning_language']]}\n"
            f"Level: {context.user_data['level']}\n"
            f"Daily Goal: {goal_minutes} minutes\n\n"
            "🚀 You're all set! Let's start learning!\n\n"
            "Use the menu below to navigate:\n"
            "📚 Learn - Start today's lesson\n"
            "🧠 Review - Review previous content\n"
            "💬 AI Tutor - Practice conversation\n"
            "📊 Progress - Check your stats\n\n"
            "_Create by: PINLON-YOUTH_"
        )
        
        await query.edit_message_text(
            welcome_complete,
            parse_mode=ParseMode.MARKDOWN
        )
        
        await context.bot.send_message(
            chat_id=user_id,
            text="Choose an option:",
            reply_markup=self.get_main_menu_keyboard(user_id)
        )
        
        return ConversationHandler.END
    
    # ==================== USER COMMANDS ====================
    
    async def lang_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /lang command - Change learning language"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        
        if not user:
            await update.message.reply_text("Please use /start first!")
            return
        
        # Show current language and options
        current_lang = user['learning_language']
        text = f"Current learning language: {AVAILABLE_LANGUAGES.get(current_lang, 'Unknown')}\n\nSelect new language:"
        
        keyboard = []
        lang_items = list(AVAILABLE_LANGUAGES.items())
        for i in range(0, len(lang_items), 2):
            row = []
            for j in range(2):
                if i + j < len(lang_items):
                    code, name = lang_items[i + j]
                    row.append(InlineKeyboardButton(name, callback_data=f"changelang_{code}"))
            keyboard.append(row)
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup)
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command - Show user profile"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        
        if not user:
            await update.message.reply_text("Please use /start first!")
            return
        
        # Get user stats
        stats = self.db.get_user_stats(user_id)
        
        profile_text = (
            f"👤 *Your Profile*\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"📚 Language: {AVAILABLE_LANGUAGES.get(user['learning_language'], 'Unknown')}\n"
            f"📊 Level: {user['level']}\n"
            f"⭐ XP: {user['xp']}\n"
            f"🔥 Streak: {user['streak']} days\n"
            f"📖 Lessons Completed: {user['total_lessons']}\n"
            f"🎯 Accuracy: {stats['accuracy']}%\n"
            f"🏆 Badges: {stats['badge_count']}\n\n"
            f"_Keep learning to unlock more achievements!_"
        )
        
        keyboard = [
            [InlineKeyboardButton("📊 Detailed Stats", callback_data="detailed_stats")],
            [InlineKeyboardButton("🏆 Badges", callback_data="show_badges")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            profile_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def learn_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /learn command - Start daily lesson"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        
        if not user:
            await update.message.reply_text("Please use /start first!")
            return
        
        # Generate daily lesson
        lesson = self.content_manager.generate_daily_lesson(
            user['learning_language'],
            user['level']
        )
        
        lesson_text = (
            f"📚 *Today's Lesson*\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"*Topic:* {lesson['topic']}\n"
            f"*Level:* {lesson['level']}\n\n"
            f"Ready to start? This lesson includes:\n"
            f"• 5 new vocabulary words\n"
            f"• 1 grammar point\n"
            f"• Listening exercise\n"
            f"• Practice quiz\n\n"
            f"Estimated time: 10 minutes ⏱️"
        )
        
        keyboard = [
            [InlineKeyboardButton("🚀 Start Lesson", callback_data=f"start_lesson_{lesson['id']}")],
            [InlineKeyboardButton("📋 Choose Different Topic", callback_data="browse_lessons")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            lesson_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def vocab_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /vocab command - Show daily vocabulary"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        
        if not user:
            await update.message.reply_text("Please use /start first!")
            return
        
        # Get today's vocabulary
        vocab_list = self.content_manager.get_daily_vocabulary(
            user['learning_language'],
            user['level'],
            count=5
        )
        
        vocab_text = "📖 *Today's Vocabulary*\n━━━━━━━━━━━━━━━━━━\n\n"
        
        for idx, word in enumerate(vocab_list, 1):
            vocab_text += (
                f"{idx}. *{word['word']}* ({word['pronunciation']})\n"
                f"   _{word['translation']}_\n"
                f"   Example: {word['example']}\n\n"
            )
        
        keyboard = [
            [InlineKeyboardButton("🔊 Practice Pronunciation", callback_data="practice_pronunciation")],
            [InlineKeyboardButton("📝 Take Vocab Quiz", callback_data="vocab_quiz")],
            [InlineKeyboardButton("💾 Save to My Deck", callback_data="save_vocab")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            vocab_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def tutor_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /tutor command - Start AI conversation"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        
        if not user:
            await update.message.reply_text("Please use /start first!")
            return
        
        tutor_text = (
            "💬 *AI Tutor Mode*\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "I'm your personal language tutor! 🤖\n\n"
            "You can:\n"
            "• Have a conversation in your learning language\n"
            "• Ask me to correct your sentences\n"
            "• Practice specific scenarios\n"
            "• Get grammar explanations\n\n"
            "Just start typing, or choose a scenario below:"
        )
        
        keyboard = [
            [InlineKeyboardButton("🍕 Restaurant", callback_data="roleplay_restaurant")],
            [InlineKeyboardButton("✈️ Airport", callback_data="roleplay_airport")],
            [InlineKeyboardButton("🛒 Shopping", callback_data="roleplay_shopping")],
            [InlineKeyboardButton("💼 Job Interview", callback_data="roleplay_interview")],
            [InlineKeyboardButton("💬 Free Conversation", callback_data="roleplay_free")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Enable tutor mode
        context.user_data['tutor_mode'] = True
        
        await update.message.reply_text(
            tutor_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def quiz_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quiz command - Start quiz"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        
        if not user:
            await update.message.reply_text("Please use /start first!")
            return
        
        quiz_text = (
            "🎯 *Quiz Time!*\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "Test your knowledge and earn XP! 🌟\n\n"
            "Choose a quiz type:"
        )
        
        keyboard = [
            [InlineKeyboardButton("⚡ Quick Quiz (5 questions)", callback_data="quiz_quick")],
            [InlineKeyboardButton("🎓 Standard Quiz (10 questions)", callback_data="quiz_standard")],
            [InlineKeyboardButton("🔥 Challenge Mode (Timed)", callback_data="quiz_challenge")],
            [InlineKeyboardButton("📊 Level Test", callback_data="quiz_level_test")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            quiz_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def progress_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /progress command - Show progress"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        
        if not user:
            await update.message.reply_text("Please use /start first!")
            return
        
        # Generate progress card
        progress_image = progress_card_gen.generate_card(user_id)
        
        progress_text = (
            "📊 *Your Learning Progress*\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"Week: {user['weekly_lessons']} lessons\n"
            f"Month: {user['monthly_lessons']} lessons\n"
            f"Total Study Time: {user['total_minutes']} minutes\n\n"
            "Keep up the great work! 🌟"
        )
        
        keyboard = [
            [InlineKeyboardButton("📈 Detailed Analytics", callback_data="detailed_analytics")],
            [InlineKeyboardButton("🏆 Leaderboard", callback_data="show_leaderboard")],
            [InlineKeyboardButton("📤 Share Progress", callback_data="share_progress")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if progress_image:
            await update.message.reply_photo(
                photo=progress_image,
                caption=progress_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                progress_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = (
            "❓ *SUPER LEARNING BOT - Help*\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "*📚 Learning Commands:*\n"
            "/learn - Start daily lesson\n"
            "/vocab - Today's vocabulary\n"
            "/review - Review previous content\n"
            "/path - Learning roadmap\n\n"
            "*💬 Practice Commands:*\n"
            "/tutor - AI conversation practice\n"
            "/roleplay - Scenario practice\n"
            "/correct - Grammar correction\n\n"
            "*🎯 Quiz Commands:*\n"
            "/quiz - Take a quiz\n"
            "/challenge - Timed challenge\n"
            "/exam - Level test\n\n"
            "*📊 Progress Commands:*\n"
            "/profile - Your profile\n"
            "/progress - Progress stats\n"
            "/streak - Streak info\n"
            "/badges - Your achievements\n\n"
            "*⚙️ Settings:*\n"
            "/lang - Change language\n"
            "/goal - Set daily goal\n\n"
            "_Create by: PINLON-YOUTH_"
        )
        
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN
        )
    
    # ==================== ADMIN COMMANDS ====================
    
    async def admin_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command - Admin statistics"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            await update.message.reply_text("⛔ Admin access required!")
            return
        
        stats = self.db.get_platform_stats()
        
        stats_text = (
            "📊 *Platform Statistics*\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"👥 Total Users: {stats['total_users']}\n"
            f"✅ Active Today: {stats['active_today']}\n"
            f"📚 Lessons Completed: {stats['total_lessons']}\n"
            f"🎯 Quizzes Taken: {stats['total_quizzes']}\n"
            f"💬 AI Conversations: {stats['total_conversations']}\n"
            f"📈 Retention Rate: {stats['retention_rate']}%\n"
        )
        
        await update.message.reply_text(
            stats_text,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /broadcast command - Send message to all users"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            await update.message.reply_text("⛔ Admin access required!")
            return
        
        if not context.args:
            await update.message.reply_text(
                "Usage: /broadcast <message>\n"
                "Send a message to all users."
            )
            return
        
        message = ' '.join(context.args)
        users = self.db.get_all_users()
        
        success_count = 0
        for user in users:
            try:
                await context.bot.send_message(
                    chat_id=user['user_id'],
                    text=f"📢 *Announcement*\n\n{message}",
                    parse_mode=ParseMode.MARKDOWN
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to send to {user['user_id']}: {e}")
        
        await update.message.reply_text(
            f"✅ Broadcast sent to {success_count}/{len(users)} users"
        )
    
    # ==================== CALLBACK HANDLERS ====================
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all button callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = query.from_user.id
        
        # Route to appropriate handler
        if data.startswith('start_lesson_'):
            await self.handle_start_lesson(query, context)
        elif data.startswith('quiz_'):
            await self.handle_quiz_start(query, context)
        elif data.startswith('roleplay_'):
            await self.handle_roleplay(query, context)
        # Add more handlers as needed
    
    async def handle_start_lesson(self, query, context):
        """Handle lesson start"""
        lesson_id = query.data.split('_')[2]
        # Implementation for starting lesson
        await query.edit_message_text("Starting lesson... 📚")
    
    async def handle_quiz_start(self, query, context):
        """Handle quiz start"""
        quiz_type = query.data.split('_')[1]
        # Implementation for starting quiz
        await query.edit_message_text("Starting quiz... 🎯")
    
    async def handle_roleplay(self, query, context):
        """Handle roleplay scenario"""
        scenario = query.data.split('_')[1]
        # Implementation for roleplay
        await query.edit_message_text(f"Starting {scenario} roleplay... 💬")
    
    # ==================== MESSAGE HANDLERS ====================
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        user_id = update.effective_user.id
        text = update.message.text
        
        # Check if in tutor mode
        if context.user_data.get('tutor_mode'):
            response = await self.ai_tutor.get_response(user_id, text)
            await update.message.reply_text(response)
        else:
            # Handle menu button presses
            if text == '📚 Learn':
                await self.learn_command(update, context)
            elif text == '🧠 Review':
                await update.message.reply_text("Review feature coming soon! 🎯")
            elif text == '💬 AI Tutor':
                await self.tutor_command(update, context)
            elif text == '📊 Progress':
                await self.progress_command(update, context)
            elif text == '🎯 Quiz':
                await self.quiz_command(update, context)
            elif text == '📖 Vocabulary':
                await self.vocab_command(update, context)
            elif text == '❓ Help':
                await self.help_command(update, context)


def main():
    """Start the bot"""
    # Get token from environment
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment!")
        return
    
    # Create bot instance
    bot = SuperLearningBot()
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Conversation handler for onboarding
    onboarding_handler = ConversationHandler(
        entry_points=[CommandHandler('start', bot.start_command)],
        states={
            SELECTING_LANGUAGE: [CallbackQueryHandler(bot.language_selected, pattern='^lang_')],
            LEVEL_TEST: [CallbackQueryHandler(bot.level_selected, pattern='^level_')],
            GOAL_SETTING: [CallbackQueryHandler(bot.goal_selected, pattern='^goal_')],
        },
        fallbacks=[CommandHandler('start', bot.start_command)],
    )
    
    # Add handlers
    application.add_handler(onboarding_handler)
    application.add_handler(CommandHandler('lang', bot.lang_command))
    application.add_handler(CommandHandler('profile', bot.profile_command))
    application.add_handler(CommandHandler('learn', bot.learn_command))
    application.add_handler(CommandHandler('vocab', bot.vocab_command))
    application.add_handler(CommandHandler('tutor', bot.tutor_command))
    application.add_handler(CommandHandler('quiz', bot.quiz_command))
    application.add_handler(CommandHandler('progress', bot.progress_command))
    application.add_handler(CommandHandler('help', bot.help_command))
    
    # Admin commands
    application.add_handler(CommandHandler('stats', bot.admin_stats_command))
    application.add_handler(CommandHandler('broadcast', bot.broadcast_command))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Start scheduler for daily reminders
    scheduler.start(application)
    
    # Start bot
    logger.info("🚀 SUPER LEARNING BOT is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
