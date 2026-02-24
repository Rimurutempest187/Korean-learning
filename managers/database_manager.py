"""
Database Manager - Handles all database operations
"""
import aiosqlite
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db: Optional[aiosqlite.Connection] = None
    
    async def initialize(self):
        """Initialize database and create tables"""
        self.db = await aiosqlite.connect(self.db_path)
        self.db.row_factory = aiosqlite.Row
        await self._create_tables()
        logger.info(f"✅ Database initialized: {self.db_path}")
    
    async def _create_tables(self):
        """Create all required tables"""
        async with self.db.cursor() as cursor:
            # Users table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    xp INTEGER DEFAULT 0,
                    hearts INTEGER DEFAULT 5,
                    streak INTEGER DEFAULT 0,
                    last_active TEXT,
                    last_heart_refill TEXT,
                    notification_enabled INTEGER DEFAULT 1,
                    current_language TEXT DEFAULT 'english',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Progress table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    language TEXT,
                    unit TEXT,
                    lesson_id TEXT,
                    completed INTEGER DEFAULT 0,
                    score INTEGER DEFAULT 0,
                    completed_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    UNIQUE(user_id, language, unit, lesson_id)
                )
            """)
            
            # Achievements table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    achievement_id TEXT,
                    unlocked_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    UNIQUE(user_id, achievement_id)
                )
            """)
            
            # Quiz sessions table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS quiz_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    language TEXT,
                    lesson_id TEXT,
                    current_question INTEGER DEFAULT 0,
                    correct_answers INTEGER DEFAULT 0,
                    total_questions INTEGER,
                    session_data TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            await self.db.commit()
    
    async def execute(self, query: str, params: tuple = ()) -> aiosqlite.Cursor:
        """Execute a query with parameters"""
        async with self.db.cursor() as cursor:
            await cursor.execute(query, params)
            await self.db.commit()
            return cursor
    
    async def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """Fetch a single row"""
        async with self.db.cursor() as cursor:
            await cursor.execute(query, params)
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def fetch_all(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Fetch all rows"""
        async with self.db.cursor() as cursor:
            await cursor.execute(query, params)
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def close(self):
        """Close database connection"""
        if self.db:
            await self.db.close()
            logger.info("Database connection closed")
