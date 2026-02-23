#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Scheduler for SUPER LEARNING BOT
Handles scheduled reminders and notifications
"""

import os
import logging
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from database import Database

logger = logging.getLogger(__name__)


class DailyScheduler:
    """Manages scheduled tasks and reminders"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.db = Database()
        self.timezone = pytz.timezone(os.getenv('TIMEZONE', 'Asia/Yangon'))
        
        # Get reminder times from environment
        self.morning_time = os.getenv('DAILY_REMINDER_TIME', '09:00')
        self.evening_time = os.getenv('EVENING_REMINDER_TIME', '19:00')
    
    def start(self, application):
        """Start the scheduler"""
        self.application = application
        
        # Schedule daily morning reminder
        morning_hour, morning_minute = map(int, self.morning_time.split(':'))
        self.scheduler.add_job(
            self.send_morning_reminder,
            CronTrigger(hour=morning_hour, minute=morning_minute, timezone=self.timezone),
            id='morning_reminder',
            name='Send morning learning reminder'
        )
        
        # Schedule evening reminder
        evening_hour, evening_minute = map(int, self.evening_time.split(':'))
        self.scheduler.add_job(
            self.send_evening_reminder,
            CronTrigger(hour=evening_hour, minute=evening_minute, timezone=self.timezone),
            id='evening_reminder',
            name='Send evening review reminder'
        )
        
        # Schedule midnight reset (for daily stats)
        self.scheduler.add_job(
            self.midnight_reset,
            CronTrigger(hour=0, minute=0, timezone=self.timezone),
            id='midnight_reset',
            name='Reset daily statistics'
        )
        
        # Schedule weekly report (Sunday 20:00)
        self.scheduler.add_job(
            self.send_weekly_report,
            CronTrigger(day_of_week='sun', hour=20, minute=0, timezone=self.timezone),
            id='weekly_report',
            name='Send weekly progress report'
        )
        
        self.scheduler.start()
        logger.info("Scheduler started successfully")
    
    async def send_morning_reminder(self):
        """Send morning learning reminder to active users"""
        try:
            users = self.db.get_all_users()
            
            for user in users:
                try:
                    # Check if user wants morning reminders (would be in user preferences)
                    user_data = self.db.get_user(user['user_id'])
                    
                    if not user_data:
                        continue
                    
                    # Check last activity - don't spam inactive users
                    if user_data.get('last_activity'):
                        last_active = datetime.strptime(user_data['last_activity'], '%Y-%m-%d').date()
                        days_inactive = (datetime.now().date() - last_active).days
                        
                        if days_inactive > 7:
                            continue  # Skip if inactive for more than a week
                    
                    message = (
                        "🌅 *Good Morning!*\n\n"
                        "Ready to start your learning day? 📚\n\n"
                        f"Your streak: {user_data['streak']} days 🔥\n"
                        f"Daily goal: {user_data['daily_goal_minutes']} minutes\n\n"
                        "Start your lesson now and keep the streak going! 💪\n\n"
                        "Use /learn to begin"
                    )
                    
                    await self.application.bot.send_message(
                        chat_id=user['user_id'],
                        text=message,
                        parse_mode='Markdown'
                    )
                    
                except Exception as e:
                    logger.error(f"Error sending morning reminder to {user['user_id']}: {e}")
            
            logger.info("Morning reminders sent")
            
        except Exception as e:
            logger.error(f"Error in send_morning_reminder: {e}")
    
    async def send_evening_reminder(self):
        """Send evening review reminder"""
        try:
            users = self.db.get_all_users()
            today = datetime.now().date().isoformat()
            
            for user in users:
                try:
                    user_data = self.db.get_user(user['user_id'])
                    
                    if not user_data:
                        continue
                    
                    # Check if user studied today
                    if user_data.get('last_activity') == today:
                        # Send review reminder
                        message = (
                            "🌙 *Evening Review Time!*\n\n"
                            "Great job studying today! 🎉\n\n"
                            "Take a few minutes to review what you learned:\n"
                            "• /review - Review today's content\n"
                            "• /vocab - Practice vocabulary\n"
                            "• /quiz - Test yourself\n\n"
                            "Reviewing helps retention! 🧠"
                        )
                    else:
                        # Send streak warning
                        message = (
                            "⚠️ *Streak Alert!*\n\n"
                            f"You haven't studied today yet!\n"
                            f"Current streak: {user_data['streak']} days 🔥\n\n"
                            "Don't break your streak! It only takes a few minutes:\n"
                            "• /learn - Quick lesson\n"
                            "• /vocab - 5 new words\n\n"
                            "You've got this! 💪"
                        )
                    
                    await self.application.bot.send_message(
                        chat_id=user['user_id'],
                        text=message,
                        parse_mode='Markdown'
                    )
                    
                except Exception as e:
                    logger.error(f"Error sending evening reminder to {user['user_id']}: {e}")
            
            logger.info("Evening reminders sent")
            
        except Exception as e:
            logger.error(f"Error in send_evening_reminder: {e}")
    
    async def midnight_reset(self):
        """Reset daily statistics at midnight"""
        try:
            # Reset daily counters, check streaks, etc.
            # This would update database accordingly
            
            logger.info("Midnight reset completed")
            
        except Exception as e:
            logger.error(f"Error in midnight_reset: {e}")
    
    async def send_weekly_report(self):
        """Send weekly progress report to users"""
        try:
            users = self.db.get_all_users()
            
            for user in users:
                try:
                    user_data = self.db.get_user(user['user_id'])
                    
                    if not user_data:
                        continue
                    
                    # Skip inactive users
                    if user_data.get('last_activity'):
                        last_active = datetime.strptime(user_data['last_activity'], '%Y-%m-%d').date()
                        days_inactive = (datetime.now().date() - last_active).days
                        
                        if days_inactive > 14:
                            continue
                    
                    # Generate weekly report
                    message = (
                        "📊 *Weekly Progress Report*\n"
                        "━━━━━━━━━━━━━━━━━━\n\n"
                        f"This week you:\n"
                        f"📚 Completed {user_data.get('weekly_lessons', 0)} lessons\n"
                        f"🔥 Maintained {user_data['streak']} day streak\n"
                        f"⭐ Earned {user_data.get('weekly_xp', 0)} XP\n"
                        f"🎯 Current level: {user_data.get('level', 'Beginner')}\n\n"
                        "Keep up the amazing work! 🌟\n\n"
                        "Next week's goal: Try to beat this week's record! 💪"
                    )
                    
                    await self.application.bot.send_message(
                        chat_id=user['user_id'],
                        text=message,
                        parse_mode='Markdown'
                    )
                    
                except Exception as e:
                    logger.error(f"Error sending weekly report to {user['user_id']}: {e}")
            
            logger.info("Weekly reports sent")
            
        except Exception as e:
            logger.error(f"Error in send_weekly_report: {e}")
    
    async def send_motivational_quote(self):
        """Send motivational quote"""
        quotes = [
            "💪 'The expert in anything was once a beginner.'",
            "🌟 'Every day is a new chance to learn something amazing!'",
            "🚀 'Progress, not perfection!'",
            "📚 'Learning is a journey, not a destination.'",
            "🎯 'Small steps every day lead to big achievements!'",
            "🔥 'Your only limit is you!'",
            "✨ 'Believe in yourself and keep going!'"
        ]
        
        import random
        quote = random.choice(quotes)
        
        try:
            users = self.db.get_all_users()
            
            for user in users:
                try:
                    await self.application.bot.send_message(
                        chat_id=user['user_id'],
                        text=quote
                    )
                except Exception as e:
                    logger.error(f"Error sending quote to {user['user_id']}: {e}")
            
        except Exception as e:
            logger.error(f"Error in send_motivational_quote: {e}")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")
