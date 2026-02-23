#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database module for SUPER LEARNING BOT
Handles all database operations using SQLite
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class Database:
    """Database handler class"""
    
    def __init__(self, db_path='superlearning.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                learning_language TEXT,
                level TEXT,
                daily_goal_minutes INTEGER DEFAULT 10,
                xp INTEGER DEFAULT 0,
                streak INTEGER DEFAULT 0,
                last_activity DATE,
                total_lessons INTEGER DEFAULT 0,
                total_minutes INTEGER DEFAULT 0,
                weekly_lessons INTEGER DEFAULT 0,
                monthly_lessons INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Lessons table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language TEXT,
                level TEXT,
                topic TEXT,
                content TEXT,
                vocabulary TEXT,
                grammar TEXT,
                audio_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                lesson_id INTEGER,
                completed BOOLEAN DEFAULT 0,
                score INTEGER,
                time_spent INTEGER,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (lesson_id) REFERENCES lessons(id)
            )
        ''')
        
        # Vocabulary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language TEXT,
                level TEXT,
                word TEXT,
                translation TEXT,
                pronunciation TEXT,
                example TEXT,
                audio_url TEXT
            )
        ''')
        
        # User vocabulary (saved words)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_vocabulary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                vocab_id INTEGER,
                mastery_level INTEGER DEFAULT 0,
                last_reviewed DATE,
                next_review DATE,
                review_count INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (vocab_id) REFERENCES vocabulary(id)
            )
        ''')
        
        # Quizzes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language TEXT,
                level TEXT,
                quiz_type TEXT,
                questions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Quiz results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                quiz_id INTEGER,
                score INTEGER,
                total_questions INTEGER,
                time_taken INTEGER,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
            )
        ''')
        
        # Badges/Achievements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS badges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                icon TEXT,
                requirement TEXT
            )
        ''')
        
        # User badges
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_badges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                badge_id INTEGER,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (badge_id) REFERENCES badges(id)
            )
        ''')
        
        # AI conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                scenario TEXT,
                messages TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Admin users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                user_id INTEGER PRIMARY KEY,
                role TEXT DEFAULT 'admin',
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Database initialized successfully")
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, user_data: Dict) -> bool:
        """Create new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (user_id, username, learning_language, level, daily_goal_minutes)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                user_data['user_id'],
                user_data['username'],
                user_data['learning_language'],
                user_data['level'],
                user_data['daily_goal_minutes']
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return dict(row)
            return None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def update_user(self, user_id: int, updates: Dict) -> bool:
        """Update user data"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
            values = list(updates.values()) + [user_id]
            
            cursor.execute(f'''
                UPDATE users 
                SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', values)
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return False
    
    def update_streak(self, user_id: int) -> int:
        """Update user streak"""
        user = self.get_user(user_id)
        if not user:
            return 0
        
        last_activity = user.get('last_activity')
        today = datetime.now().date()
        
        if last_activity:
            last_date = datetime.strptime(last_activity, '%Y-%m-%d').date()
            days_diff = (today - last_date).days
            
            if days_diff == 0:
                # Already active today
                return user['streak']
            elif days_diff == 1:
                # Consecutive day
                new_streak = user['streak'] + 1
            else:
                # Streak broken
                new_streak = 1
        else:
            new_streak = 1
        
        self.update_user(user_id, {
            'streak': new_streak,
            'last_activity': today.isoformat()
        })
        
        return new_streak
    
    def add_xp(self, user_id: int, xp: int) -> int:
        """Add XP to user"""
        user = self.get_user(user_id)
        if not user:
            return 0
        
        new_xp = user['xp'] + xp
        self.update_user(user_id, {'xp': new_xp})
        
        return new_xp
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get user statistics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get quiz accuracy
            cursor.execute('''
                SELECT AVG(CAST(score AS FLOAT) / total_questions * 100) as accuracy
                FROM quiz_results
                WHERE user_id = ?
            ''', (user_id,))
            
            accuracy_row = cursor.fetchone()
            accuracy = round(accuracy_row['accuracy'], 2) if accuracy_row['accuracy'] else 0
            
            # Get badge count
            cursor.execute('''
                SELECT COUNT(*) as badge_count
                FROM user_badges
                WHERE user_id = ?
            ''', (user_id,))
            
            badge_row = cursor.fetchone()
            badge_count = badge_row['badge_count']
            
            conn.close()
            
            return {
                'accuracy': accuracy,
                'badge_count': badge_count
            }
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {'accuracy': 0, 'badge_count': 0}
    
    # ==================== LESSON OPERATIONS ====================
    
    def create_lesson(self, lesson_data: Dict) -> Optional[int]:
        """Create new lesson"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO lessons (language, level, topic, content, vocabulary, grammar, audio_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                lesson_data['language'],
                lesson_data['level'],
                lesson_data['topic'],
                json.dumps(lesson_data['content']),
                json.dumps(lesson_data['vocabulary']),
                json.dumps(lesson_data['grammar']),
                lesson_data.get('audio_url', '')
            ))
            
            lesson_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            return lesson_id
        except Exception as e:
            logger.error(f"Error creating lesson: {e}")
            return None
    
    def get_lesson(self, lesson_id: int) -> Optional[Dict]:
        """Get lesson by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                lesson = dict(row)
                lesson['content'] = json.loads(lesson['content'])
                lesson['vocabulary'] = json.loads(lesson['vocabulary'])
                lesson['grammar'] = json.loads(lesson['grammar'])
                return lesson
            return None
        except Exception as e:
            logger.error(f"Error getting lesson: {e}")
            return None
    
    def get_lessons_by_level(self, language: str, level: str, limit: int = 10) -> List[Dict]:
        """Get lessons by language and level"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM lessons 
                WHERE language = ? AND level = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (language, level, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            lessons = []
            for row in rows:
                lesson = dict(row)
                lesson['content'] = json.loads(lesson['content'])
                lesson['vocabulary'] = json.loads(lesson['vocabulary'])
                lesson['grammar'] = json.loads(lesson['grammar'])
                lessons.append(lesson)
            
            return lessons
        except Exception as e:
            logger.error(f"Error getting lessons: {e}")
            return []
    
    # ==================== VOCABULARY OPERATIONS ====================
    
    def add_vocabulary(self, vocab_data: Dict) -> Optional[int]:
        """Add vocabulary word"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO vocabulary (language, level, word, translation, pronunciation, example, audio_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                vocab_data['language'],
                vocab_data['level'],
                vocab_data['word'],
                vocab_data['translation'],
                vocab_data['pronunciation'],
                vocab_data['example'],
                vocab_data.get('audio_url', '')
            ))
            
            vocab_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            return vocab_id
        except Exception as e:
            logger.error(f"Error adding vocabulary: {e}")
            return None
    
    def get_vocabulary(self, language: str, level: str, limit: int = 10) -> List[Dict]:
        """Get vocabulary words"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM vocabulary 
                WHERE language = ? AND level = ?
                ORDER BY RANDOM()
                LIMIT ?
            ''', (language, level, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting vocabulary: {e}")
            return []
    
    def save_user_vocabulary(self, user_id: int, vocab_id: int) -> bool:
        """Save vocabulary to user's deck"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if already saved
            cursor.execute('''
                SELECT id FROM user_vocabulary 
                WHERE user_id = ? AND vocab_id = ?
            ''', (user_id, vocab_id))
            
            if cursor.fetchone():
                conn.close()
                return True
            
            # Calculate next review date (1 day from now)
            next_review = (datetime.now() + timedelta(days=1)).date().isoformat()
            
            cursor.execute('''
                INSERT INTO user_vocabulary (user_id, vocab_id, next_review)
                VALUES (?, ?, ?)
            ''', (user_id, vocab_id, next_review))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            logger.error(f"Error saving user vocabulary: {e}")
            return False
    
    # ==================== QUIZ OPERATIONS ====================
    
    def create_quiz(self, quiz_data: Dict) -> Optional[int]:
        """Create new quiz"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO quizzes (language, level, quiz_type, questions)
                VALUES (?, ?, ?, ?)
            ''', (
                quiz_data['language'],
                quiz_data['level'],
                quiz_data['quiz_type'],
                json.dumps(quiz_data['questions'])
            ))
            
            quiz_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            return quiz_id
        except Exception as e:
            logger.error(f"Error creating quiz: {e}")
            return None
    
    def save_quiz_result(self, user_id: int, quiz_id: int, score: int, total: int, time_taken: int) -> bool:
        """Save quiz result"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO quiz_results (user_id, quiz_id, score, total_questions, time_taken)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, quiz_id, score, total, time_taken))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            logger.error(f"Error saving quiz result: {e}")
            return False
    
    # ==================== ADMIN OPERATIONS ====================
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT user_id FROM admins WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            
            conn.close()
            
            return result is not None
        except Exception as e:
            logger.error(f"Error checking admin: {e}")
            return False
    
    def get_platform_stats(self) -> Dict:
        """Get platform-wide statistics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Total users
            cursor.execute('SELECT COUNT(*) as total FROM users')
            total_users = cursor.fetchone()['total']
            
            # Active today
            today = datetime.now().date().isoformat()
            cursor.execute('SELECT COUNT(*) as active FROM users WHERE last_activity = ?', (today,))
            active_today = cursor.fetchone()['active']
            
            # Total lessons completed
            cursor.execute('SELECT COUNT(*) as total FROM user_progress WHERE completed = 1')
            total_lessons = cursor.fetchone()['total']
            
            # Total quizzes
            cursor.execute('SELECT COUNT(*) as total FROM quiz_results')
            total_quizzes = cursor.fetchone()['total']
            
            # Total conversations
            cursor.execute('SELECT COUNT(*) as total FROM conversations')
            total_conversations = cursor.fetchone()['total']
            
            # Calculate retention (users active in last 7 days)
            week_ago = (datetime.now() - timedelta(days=7)).date().isoformat()
            cursor.execute('SELECT COUNT(*) as active FROM users WHERE last_activity >= ?', (week_ago,))
            active_week = cursor.fetchone()['active']
            
            retention_rate = round((active_week / total_users * 100), 2) if total_users > 0 else 0
            
            conn.close()
            
            return {
                'total_users': total_users,
                'active_today': active_today,
                'total_lessons': total_lessons,
                'total_quizzes': total_quizzes,
                'total_conversations': total_conversations,
                'retention_rate': retention_rate
            }
        except Exception as e:
            logger.error(f"Error getting platform stats: {e}")
            return {}
    
    def get_all_users(self) -> List[Dict]:
        """Get all users (for broadcasting)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT user_id, username FROM users')
            rows = cursor.fetchall()
            
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []
