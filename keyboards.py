"""
SUPER LEARNING BOT — Inline Keyboards & Menus
==============================================
Centralised UI button builder. Keeps handlers clean.
"""
from telegram import InlineKeyboardButton as Btn, InlineKeyboardMarkup as Markup
from config import SUPPORTED_LANGS, CEFR_LEVELS

# ─────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────
def main_menu():
    return Markup([
        [Btn("📚 Learn",     callback_data="menu_learn"),
         Btn("🧠 Review",    callback_data="menu_review")],
        [Btn("💬 Tutor",     callback_data="menu_tutor"),
         Btn("📊 Progress",  callback_data="menu_progress")],
        [Btn("🔤 Vocabulary",callback_data="menu_vocab"),
         Btn("🧪 Quiz",      callback_data="menu_quiz")],
        [Btn("🤝 Social",    callback_data="menu_social"),
         Btn("⚙️ Settings",  callback_data="menu_settings")],
    ])

# ─────────────────────────────────────────
#  LANGUAGE PICKER
# ─────────────────────────────────────────
def lang_picker(prefix: str = "setlang"):
    buttons = []
    items   = list(SUPPORTED_LANGS.items())
    for i in range(0, len(items), 2):
        row = []
        for key, info in items[i:i+2]:
            row.append(Btn(info["name"], callback_data=f"{prefix}:{key}"))
        buttons.append(row)
    return Markup(buttons)

# ─────────────────────────────────────────
#  LEVEL PICKER
# ─────────────────────────────────────────
def level_picker(prefix: str = "setlevel"):
    labels = {"A1": "🌱 A1 Beginner", "A2": "🌿 A2 Elementary",
              "B1": "⭐ B1 Intermediate", "B2": "🌟 B2 Upper-Int",
              "C1": "💫 C1 Advanced", "C2": "👑 C2 Mastery"}
    rows = []
    for i in range(0, len(CEFR_LEVELS), 2):
        row = []
        for lv in CEFR_LEVELS[i:i+2]:
            row.append(Btn(labels.get(lv, lv), callback_data=f"{prefix}:{lv}"))
        rows.append(row)
    return Markup(rows)

# ─────────────────────────────────────────
#  QUIZ OPTION BUTTONS
# ─────────────────────────────────────────
def quiz_options(options: list[str], session_id: int, q_index: int):
    labels = ["🅐", "🅑", "🅒", "🅓"]
    return Markup([
        [Btn(f"{labels[i]} {opt}", callback_data=f"quiz:{session_id}:{q_index}:{i}")]
        for i, opt in enumerate(options)
    ])

# ─────────────────────────────────────────
#  YES / NO
# ─────────────────────────────────────────
def yes_no(yes_data: str, no_data: str):
    return Markup([[Btn("✅ Yes", callback_data=yes_data), Btn("❌ No", callback_data=no_data)]])

# ─────────────────────────────────────────
#  BACK BUTTON
# ─────────────────────────────────────────
def back_btn(target: str = "menu_main"):
    return Markup([[Btn("◀️ Back to Menu", callback_data=target)]])

# ─────────────────────────────────────────
#  LEARN MENU
# ─────────────────────────────────────────
def learn_menu():
    return Markup([
        [Btn("📅 Daily Lesson", callback_data="learn_daily"),
         Btn("🗺️ Learning Path", callback_data="learn_path")],
        [Btn("🎧 Listening", callback_data="learn_listen"),
         Btn("🔄 Review",    callback_data="learn_review")],
        [Btn("◀️ Menu",      callback_data="menu_main")],
    ])

# ─────────────────────────────────────────
#  VOCAB MENU
# ─────────────────────────────────────────
def vocab_menu():
    return Markup([
        [Btn("📖 Daily Words",   callback_data="vocab_daily"),
         Btn("🗂️ My Deck",       callback_data="vocab_deck")],
        [Btn("🃏 Flashcards",    callback_data="vocab_flash"),
         Btn("📥 Review Due",    callback_data="vocab_review")],
        [Btn("◀️ Menu",          callback_data="menu_main")],
    ])

# ─────────────────────────────────────────
#  QUIZ MENU
# ─────────────────────────────────────────
def quiz_menu():
    return Markup([
        [Btn("🎲 Random Quiz",   callback_data="quiz_random"),
         Btn("⚡ Challenge",      callback_data="quiz_challenge")],
        [Btn("📝 Level Exam",    callback_data="quiz_exam"),
         Btn("🏆 Leaderboard",   callback_data="quiz_tops")],
        [Btn("◀️ Menu",          callback_data="menu_main")],
    ])

# ─────────────────────────────────────────
#  SOCIAL MENU
# ─────────────────────────────────────────
def social_menu():
    return Markup([
        [Btn("👥 Study Groups",  callback_data="social_groups"),
         Btn("⚔️ Duel",          callback_data="social_duel")],
        [Btn("🃏 Share Card",    callback_data="social_share"),
         Btn("◀️ Menu",          callback_data="menu_main")],
    ])

# ─────────────────────────────────────────
#  SETTINGS MENU
# ─────────────────────────────────────────
def settings_menu():
    return Markup([
        [Btn("🌍 Change Language", callback_data="settings_lang"),
         Btn("🎯 Daily Goal",      callback_data="settings_goal")],
        [Btn("👤 Profile",         callback_data="settings_profile"),
         Btn("◀️ Menu",            callback_data="menu_main")],
    ])

# ─────────────────────────────────────────
#  TUTOR MENU
# ─────────────────────────────────────────
def tutor_menu():
    return Markup([
        [Btn("💬 Free Chat",       callback_data="tutor_chat"),
         Btn("🎭 Roleplay",        callback_data="tutor_roleplay")],
        [Btn("✏️ Grammar Check",   callback_data="tutor_grammar"),
         Btn("🔁 Shadowing",       callback_data="tutor_shadow")],
        [Btn("◀️ Menu",            callback_data="menu_main")],
    ])

# ─────────────────────────────────────────
#  ROLEPLAY SCENARIO PICKER
# ─────────────────────────────────────────
def roleplay_picker():
    from lessons_data import ROLEPLAY_SCENARIOS
    rows = []
    items = list(ROLEPLAY_SCENARIOS.items())
    for i in range(0, len(items), 2):
        row = []
        for key, info in items[i:i+2]:
            row.append(Btn(info["title"], callback_data=f"roleplay:{key}"))
        rows.append(row)
    rows.append([Btn("◀️ Back", callback_data="menu_tutor")])
    return Markup(rows)

# ─────────────────────────────────────────
#  GOAL PICKER
# ─────────────────────────────────────────
def goal_picker():
    options = [5, 10, 15, 20, 30, 45, 60]
    rows = []
    for i in range(0, len(options), 3):
        row = [Btn(f"⏱ {m} min", callback_data=f"goal:{m}") for m in options[i:i+3]]
        rows.append(row)
    rows.append([Btn("◀️ Back", callback_data="menu_settings")])
    return Markup(rows)

# ─────────────────────────────────────────
#  FLASHCARD BUTTONS
# ─────────────────────────────────────────
def flashcard_rating(vocab_id: int):
    return Markup([[
        Btn("😰 Hard (1)",  callback_data=f"fc:{vocab_id}:1"),
        Btn("🤔 OK (3)",    callback_data=f"fc:{vocab_id}:3"),
        Btn("😄 Easy (5)",  callback_data=f"fc:{vocab_id}:5"),
    ]])

# ─────────────────────────────────────────
#  DUEL ACCEPT/DECLINE
# ─────────────────────────────────────────
def duel_invite(duel_id: int):
    return Markup([[
        Btn("⚔️ Accept", callback_data=f"duel_accept:{duel_id}"),
        Btn("❌ Decline", callback_data=f"duel_decline:{duel_id}"),
    ]])#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gamification Engine for SUPER LEARNING BOT
Handles XP, levels, badges, and achievements
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from database import Database

logger = logging.getLogger(__name__)


class GamificationEngine:
    """Manages gamification features"""
    
    def __init__(self):
        self.db = Database()
        
        # XP requirements for each level
        self.level_thresholds = {
            1: 0,
            2: 100,
            3: 250,
            4: 500,
            5: 1000,
            6: 1500,
            7: 2500,
            8: 4000,
            9: 6000,
            10: 10000
        }
        
        # Badge definitions
        self.badges = {
            'first_lesson': {
                'name': 'First Steps',
                'icon': '👣',
                'description': 'Complete your first lesson',
                'requirement': 'complete_1_lesson'
            },
            'week_streak': {
                'name': 'Week Warrior',
                'icon': '🔥',
                'description': 'Maintain a 7-day streak',
                'requirement': 'streak_7'
            },
            'month_streak': {
                'name': 'Monthly Master',
                'icon': '🎯',
                'description': 'Maintain a 30-day streak',
                'requirement': 'streak_30'
            },
            'vocabulary_master': {
                'name': 'Word Wizard',
                'icon': '📚',
                'description': 'Learn 100 vocabulary words',
                'requirement': 'vocab_100'
            },
            'quiz_ace': {
                'name': 'Quiz Champion',
                'icon': '🏆',
                'description': 'Score 100% on 10 quizzes',
                'requirement': 'perfect_quizzes_10'
            },
            'conversation_pro': {
                'name': 'Conversation Pro',
                'icon': '💬',
                'description': 'Have 50 AI tutor conversations',
                'requirement': 'conversations_50'
            },
            'early_bird': {
                'name': 'Early Bird',
                'icon': '🌅',
                'description': 'Complete 10 morning lessons',
                'requirement': 'morning_lessons_10'
            },
            'night_owl': {
                'name': 'Night Owl',
                'icon': '🦉',
                'description': 'Complete 10 evening lessons',
                'requirement': 'evening_lessons_10'
            },
            'speed_demon': {
                'name': 'Speed Demon',
                'icon': '⚡',
                'description': 'Complete 5 lessons in one day',
                'requirement': 'daily_lessons_5'
            },
            'perfectionist': {
                'name': 'Perfectionist',
                'icon': '💯',
                'description': 'Complete 20 lessons with 100% accuracy',
                'requirement': 'perfect_lessons_20'
            }
        }
    
    def calculate_xp_reward(self, activity_type: str, performance: Dict) -> int:
        """Calculate XP reward for an activity"""
        
        base_xp = {
            'lesson_complete': 50,
            'quiz_complete': 30,
            'vocabulary_learned': 5,
            'conversation': 20,
            'daily_goal': 25,
            'streak_bonus': 10
        }
        
        xp = base_xp.get(activity_type, 10)
        
        # Bonus for high performance
        if activity_type in ['quiz_complete', 'lesson_complete']:
            accuracy = performance.get('accuracy', 0)
            if accuracy >= 90:
                xp += 20
            elif accuracy >= 80:
                xp += 10
            elif accuracy >= 70:
                xp += 5
        
        # Streak bonus
        streak = performance.get('streak', 0)
        if streak >= 7:
            xp += streak * 2
        
        return xp
    
    def award_xp(self, user_id: int, xp: int, reason: str = "") -> Dict:
        """Award XP to user and check for level up"""
        
        # Get current user
        user = self.db.get_user(user_id)
        if not user:
            return {'success': False, 'message': 'User not found'}
        
        # Add XP
        new_xp = self.db.add_xp(user_id, xp)
        
        # Check for level up
        old_level = self.get_user_level(user['xp'])
        new_level = self.get_user_level(new_xp)
        
        result = {
            'success': True,
            'xp_gained': xp,
            'total_xp': new_xp,
            'old_level': old_level,
            'new_level': new_level,
            'leveled_up': new_level > old_level,
            'reason': reason
        }
        
        if result['leveled_up']:
            logger.info(f"User {user_id} leveled up to {new_level}!")
        
        return result
    
    def get_user_level(self, xp: int) -> int:
        """Calculate user level from XP"""
        
        level = 1
        for lvl, threshold in sorted(self.level_thresholds.items()):
            if xp >= threshold:
                level = lvl
            else:
                break
        
        return level
    
    def get_level_progress(self, xp: int) -> Dict:
        """Get progress to next level"""
        
        current_level = self.get_user_level(xp)
        
        if current_level >= max(self.level_thresholds.keys()):
            return {
                'level': current_level,
                'current_xp': xp,
                'next_level_xp': None,
                'progress_percentage': 100,
                'xp_to_next_level': 0
            }
        
        current_threshold = self.level_thresholds[current_level]
        next_threshold = self.level_thresholds[current_level + 1]
        
        xp_in_level = xp - current_threshold
        xp_needed = next_threshold - current_threshold
        progress_percentage = (xp_in_level / xp_needed * 100) if xp_needed > 0 else 100
        
        return {
            'level': current_level,
            'current_xp': xp,
            'next_level_xp': next_threshold,
            'progress_percentage': round(progress_percentage, 1),
            'xp_to_next_level': next_threshold - xp
        }
    
    def check_badge_eligibility(self, user_id: int, activity: str, stats: Dict) -> List[str]:
        """Check if user earned any badges"""
        
        earned_badges = []
        
        # Check each badge requirement
        if activity == 'lesson_complete' and stats.get('total_lessons', 0) >= 1:
            if not self.has_badge(user_id, 'first_lesson'):
                self.award_badge(user_id, 'first_lesson')
                earned_badges.append('first_lesson')
        
        if activity == 'streak_update':
            streak = stats.get('streak', 0)
            if streak >= 7 and not self.has_badge(user_id, 'week_streak'):
                self.award_badge(user_id, 'week_streak')
                earned_badges.append('week_streak')
            if streak >= 30 and not self.has_badge(user_id, 'month_streak'):
                self.award_badge(user_id, 'month_streak')
                earned_badges.append('month_streak')
        
        # Add more badge checks...
        
        return earned_badges
    
    def has_badge(self, user_id: int, badge_id: str) -> bool:
        """Check if user has a badge"""
        # Would query database
        return False
    
    def award_badge(self, user_id: int, badge_id: str) -> bool:
        """Award a badge to user"""
        try:
            # Would insert into database
            logger.info(f"Awarded badge {badge_id} to user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error awarding badge: {e}")
            return False
    
    def get_user_badges(self, user_id: int) -> List[Dict]:
        """Get all badges earned by user"""
        # Would query from database
        return []
    
    def get_leaderboard(self, timeframe: str = 'all', limit: int = 10) -> List[Dict]:
        """Get leaderboard data"""
        
        # Would query from database
        # For now, return sample data
        return [
            {'rank': 1, 'username': 'User1', 'xp': 5000, 'streak': 30},
            {'rank': 2, 'username': 'User2', 'xp': 4500, 'streak': 25},
            {'rank': 3, 'username': 'User3', 'xp': 4000, 'streak': 20},
        ]
    
    def format_badge_message(self, badge_id: str) -> str:
        """Format badge earned message"""
        
        badge = self.badges.get(badge_id)
        if not badge:
            return "You earned a new badge!"
        
        return f"""🎉 *New Badge Earned!*

{badge['icon']} *{badge['name']}*
{badge['description']}

Keep up the great work!"""
    
    def format_level_up_message(self, old_level: int, new_level: int, xp: int) -> str:
        """Format level up message"""
        
        return f"""🎊 *LEVEL UP!*

You've reached Level {new_level}! 🚀

Previous Level: {old_level}
New Level: {new_level}
Total XP: {xp}

You're making amazing progress!"""
    
    def get_daily_challenge(self, user_id: int) -> Dict:
        """Get daily challenge for user"""
        
        challenges = [
            {'type': 'lessons', 'goal': 3, 'reward_xp': 50, 
             'description': 'Complete 3 lessons today'},
            {'type': 'vocabulary', 'goal': 10, 'reward_xp': 30, 
             'description': 'Learn 10 new words'},
            {'type': 'quiz', 'goal': 2, 'reward_xp': 40, 
             'description': 'Take 2 quizzes'},
            {'type': 'conversation', 'goal': 5, 'reward_xp': 35, 
             'description': 'Have 5 minutes of AI conversation'},
        ]
        
        # Return random challenge (in production, would be user-specific)
        import random
        return random.choice(challenges)
    
    def calculate_streak_bonus(self, streak: int) -> Dict:
        """Calculate streak bonus rewards"""
        
        bonuses = {
            3: {'xp': 20, 'message': '3-day streak! Keep going!'},
            7: {'xp': 50, 'message': '1 week streak! Amazing!'},
            14: {'xp': 100, 'message': '2 weeks! You\'re on fire! 🔥'},
            30: {'xp': 250, 'message': '1 month streak! Incredible dedication!'},
            100: {'xp': 1000, 'message': '100 days! You\'re a legend! 🏆'},
        }
        
        if streak in bonuses:
            return bonuses[streak]
        
        return None
