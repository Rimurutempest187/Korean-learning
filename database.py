"""
SUPER LEARNING BOT — SQLite Database Layer
==========================================
Handles all persistent storage: users, vocab,
lessons, quiz scores, streaks, badges, duels.
"""
import sqlite3
import json
import time
from datetime import datetime, date
from config import DB_PATH

# ─────────────────────────────────────────
#  CONNECTION HELPER
# ─────────────────────────────────────────
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

# ─────────────────────────────────────────
#  SCHEMA INIT
# ─────────────────────────────────────────
def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id       INTEGER PRIMARY KEY,
            username      TEXT,
            full_name     TEXT,
            lang          TEXT DEFAULT 'english',
            cefr_level    TEXT DEFAULT 'A1',
            xp            INTEGER DEFAULT 0,
            streak        INTEGER DEFAULT 0,
            last_active   TEXT,
            daily_goal    INTEGER DEFAULT 15,
            joined_at     TEXT,
            is_premium    INTEGER DEFAULT 0,
            total_lessons INTEGER DEFAULT 0,
            total_correct INTEGER DEFAULT 0,
            total_questions INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS vocab (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER,
            word       TEXT,
            meaning    TEXT,
            example    TEXT,
            lang       TEXT,
            next_review TEXT,
            ease       REAL DEFAULT 2.5,
            interval   INTEGER DEFAULT 1,
            reps       INTEGER DEFAULT 0,
            added_at   TEXT,
            UNIQUE(user_id, word, lang)
        );

        CREATE TABLE IF NOT EXISTS lessons (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            lesson_key  TEXT,
            lang        TEXT,
            completed   INTEGER DEFAULT 0,
            score       INTEGER DEFAULT 0,
            completed_at TEXT
        );

        CREATE TABLE IF NOT EXISTS quiz_sessions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER,
            q_json     TEXT,
            ans_json   TEXT,
            score      INTEGER DEFAULT 0,
            total      INTEGER DEFAULT 0,
            mode       TEXT DEFAULT 'quiz',
            started_at TEXT,
            ended_at   TEXT
        );

        CREATE TABLE IF NOT EXISTS badges (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id  INTEGER,
            badge_id TEXT,
            earned_at TEXT,
            UNIQUE(user_id, badge_id)
        );

        CREATE TABLE IF NOT EXISTS duels (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            challenger   INTEGER,
            opponent     INTEGER,
            status       TEXT DEFAULT 'pending',
            winner       INTEGER,
            created_at   TEXT,
            q_json       TEXT,
            c_score      INTEGER DEFAULT 0,
            o_score      INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS study_groups (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT,
            owner_id   INTEGER,
            lang       TEXT,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS group_members (
            group_id INTEGER,
            user_id  INTEGER,
            joined_at TEXT,
            PRIMARY KEY(group_id, user_id)
        );

        CREATE TABLE IF NOT EXISTS custom_lessons (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id   INTEGER,
            lang       TEXT,
            level      TEXT,
            title      TEXT,
            content    TEXT,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS custom_quizzes (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id   INTEGER,
            lang       TEXT,
            q_json     TEXT,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS user_state (
            user_id  INTEGER PRIMARY KEY,
            state    TEXT DEFAULT 'idle',
            data     TEXT DEFAULT '{}'
        );
        """)
    print("✅ Database initialized.")

# ─────────────────────────────────────────
#  USER CRUD
# ─────────────────────────────────────────
def get_user(user_id: int) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
        return dict(row) if row else None

def upsert_user(user_id: int, username: str, full_name: str):
    now = datetime.now().isoformat()
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO users(user_id, username, full_name, joined_at, last_active)
            VALUES(?,?,?,?,?)
            ON CONFLICT(user_id) DO UPDATE SET
                username=excluded.username,
                full_name=excluded.full_name,
                last_active=excluded.last_active
        """, (user_id, username, full_name, now, now))

def update_user(user_id: int, **kwargs):
    if not kwargs:
        return
    fields = ", ".join(f"{k}=?" for k in kwargs)
    vals   = list(kwargs.values()) + [user_id]
    with get_conn() as conn:
        conn.execute(f"UPDATE users SET {fields} WHERE user_id=?", vals)

def add_xp(user_id: int, amount: int):
    with get_conn() as conn:
        conn.execute("UPDATE users SET xp=xp+? WHERE user_id=?", (amount, user_id))

def update_streak(user_id: int):
    user = get_user(user_id)
    if not user:
        return 0
    today = date.today().isoformat()
    last  = user.get("last_active", "")[:10]
    if last == today:
        return user["streak"]
    yesterday = (date.today().replace(day=date.today().day - 1)).isoformat()
    new_streak = (user["streak"] + 1) if last == yesterday else 1
    update_user(user_id, streak=new_streak, last_active=datetime.now().isoformat())
    return new_streak

def get_leaderboard(limit=10) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT user_id, full_name, xp, streak FROM users ORDER BY xp DESC LIMIT ?",
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

def get_all_user_ids() -> list[int]:
    with get_conn() as conn:
        rows = conn.execute("SELECT user_id FROM users").fetchall()
        return [r["user_id"] for r in rows]

# ─────────────────────────────────────────
#  STATE MACHINE
# ─────────────────────────────────────────
def get_state(user_id: int) -> tuple[str, dict]:
    with get_conn() as conn:
        row = conn.execute("SELECT state, data FROM user_state WHERE user_id=?", (user_id,)).fetchone()
        if row:
            return row["state"], json.loads(row["data"])
        return "idle", {}

def set_state(user_id: int, state: str, data: dict = None):
    if data is None:
        data = {}
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO user_state(user_id, state, data) VALUES(?,?,?)
            ON CONFLICT(user_id) DO UPDATE SET state=excluded.state, data=excluded.data
        """, (user_id, state, json.dumps(data)))

def clear_state(user_id: int):
    set_state(user_id, "idle", {})

# ─────────────────────────────────────────
#  VOCAB CRUD
# ─────────────────────────────────────────
def save_vocab(user_id: int, word: str, meaning: str, example: str, lang: str):
    now = datetime.now().isoformat()
    with get_conn() as conn:
        try:
            conn.execute("""
                INSERT INTO vocab(user_id, word, meaning, example, lang, next_review, added_at)
                VALUES(?,?,?,?,?,?,?)
            """, (user_id, word, meaning, example, lang, now, now))
            return True
        except sqlite3.IntegrityError:
            return False

def get_vocab_deck(user_id: int, lang: str = None) -> list[dict]:
    with get_conn() as conn:
        if lang:
            rows = conn.execute(
                "SELECT * FROM vocab WHERE user_id=? AND lang=? ORDER BY added_at DESC",
                (user_id, lang)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM vocab WHERE user_id=? ORDER BY added_at DESC",
                (user_id,)
            ).fetchall()
        return [dict(r) for r in rows]

def get_due_reviews(user_id: int) -> list[dict]:
    now = datetime.now().isoformat()
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM vocab WHERE user_id=? AND next_review<=? ORDER BY next_review LIMIT 20",
            (user_id, now)
        ).fetchall()
        return [dict(r) for r in rows]

def update_vocab_sm2(vocab_id: int, quality: int):
    """SM-2 spaced repetition algorithm."""
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM vocab WHERE id=?", (vocab_id,)).fetchone()
        if not row:
            return
        ease     = row["ease"]
        interval = row["interval"]
        reps     = row["reps"]
        if quality >= 3:
            if reps == 0:   interval = 1
            elif reps == 1: interval = 6
            else:           interval = round(interval * ease)
            ease = ease + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
            ease = max(1.3, ease)
            reps += 1
        else:
            interval = 1
            reps     = 0
        import datetime as dt
        next_rev = (dt.datetime.now() + dt.timedelta(days=interval)).isoformat()
        conn.execute(
            "UPDATE vocab SET ease=?, interval=?, reps=?, next_review=? WHERE id=?",
            (ease, interval, reps, next_rev, vocab_id)
        )

def count_vocab(user_id: int) -> int:
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM vocab WHERE user_id=?", (user_id,)).fetchone()[0]

# ─────────────────────────────────────────
#  LESSON TRACKING
# ─────────────────────────────────────────
def mark_lesson_done(user_id: int, lesson_key: str, lang: str, score: int):
    now = datetime.now().isoformat()
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO lessons(user_id, lesson_key, lang, completed, score, completed_at)
            VALUES(?,?,?,1,?,?)
        """, (user_id, lesson_key, lang, score, now))
        conn.execute("UPDATE users SET total_lessons=total_lessons+1 WHERE user_id=?", (user_id,))

def get_completed_lessons(user_id: int, lang: str) -> list[str]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT lesson_key FROM lessons WHERE user_id=? AND lang=?",
            (user_id, lang)
        ).fetchall()
        return [r["lesson_key"] for r in rows]

# ─────────────────────────────────────────
#  QUIZ SESSION
# ─────────────────────────────────────────
def start_quiz_session(user_id: int, questions: list, mode: str = "quiz") -> int:
    now = datetime.now().isoformat()
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO quiz_sessions(user_id, q_json, ans_json, mode, started_at)
            VALUES(?,?,?,?,?)
        """, (user_id, json.dumps(questions), json.dumps([]), mode, now))
        return cur.lastrowid

def update_quiz_session(session_id: int, score: int, total: int, answers: list):
    now = datetime.now().isoformat()
    with get_conn() as conn:
        conn.execute(
            "UPDATE quiz_sessions SET score=?, total=?, ans_json=?, ended_at=? WHERE id=?",
            (score, total, json.dumps(answers), now, session_id)
        )
        conn.execute(
            "UPDATE users SET total_correct=total_correct+?, total_questions=total_questions+? WHERE user_id=(SELECT user_id FROM quiz_sessions WHERE id=?)",
            (score, total, session_id)
        )

# ─────────────────────────────────────────
#  BADGES
# ─────────────────────────────────────────
def award_badge(user_id: int, badge_id: str) -> bool:
    now = datetime.now().isoformat()
    with get_conn() as conn:
        try:
            conn.execute(
                "INSERT INTO badges(user_id, badge_id, earned_at) VALUES(?,?,?)",
                (user_id, badge_id, now)
            )
            return True
        except sqlite3.IntegrityError:
            return False

def get_user_badges(user_id: int) -> list[str]:
    with get_conn() as conn:
        rows = conn.execute("SELECT badge_id FROM badges WHERE user_id=?", (user_id,)).fetchall()
        return [r["badge_id"] for r in rows]

# ─────────────────────────────────────────
#  DUELS
# ─────────────────────────────────────────
def create_duel(challenger_id: int, opponent_id: int, questions: list) -> int:
    now = datetime.now().isoformat()
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO duels(challenger, opponent, q_json, created_at)
            VALUES(?,?,?,?)
        """, (challenger_id, opponent_id, json.dumps(questions), now))
        return cur.lastrowid

def get_duel(duel_id: int) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM duels WHERE id=?", (duel_id,)).fetchone()
        return dict(row) if row else None

def update_duel_score(duel_id: int, player: str, score: int):
    field = "c_score" if player == "challenger" else "o_score"
    with get_conn() as conn:
        conn.execute(f"UPDATE duels SET {field}=? WHERE id=?", (score, duel_id))

def finish_duel(duel_id: int, winner_id: int):
    with get_conn() as conn:
        conn.execute(
            "UPDATE duels SET status='done', winner=? WHERE id=?",
            (winner_id, duel_id)
        )

# ─────────────────────────────────────────
#  STUDY GROUPS
# ─────────────────────────────────────────
def create_group(name: str, owner_id: int, lang: str) -> int:
    now = datetime.now().isoformat()
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO study_groups(name, owner_id, lang, created_at) VALUES(?,?,?,?)",
            (name, owner_id, lang, now)
        )
        gid = cur.lastrowid
        conn.execute(
            "INSERT INTO group_members(group_id, user_id, joined_at) VALUES(?,?,?)",
            (gid, owner_id, now)
        )
        return gid

def join_group(group_id: int, user_id: int):
    now = datetime.now().isoformat()
    with get_conn() as conn:
        try:
            conn.execute(
                "INSERT INTO group_members(group_id, user_id, joined_at) VALUES(?,?,?)",
                (group_id, user_id, now)
            )
            return True
        except sqlite3.IntegrityError:
            return False

def list_groups() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT g.*, COUNT(m.user_id) as member_count
            FROM study_groups g
            LEFT JOIN group_members m ON g.id=m.group_id
            GROUP BY g.id ORDER BY member_count DESC LIMIT 20
        """).fetchall()
        return [dict(r) for r in rows]

def get_user_groups(user_id: int) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT g.* FROM study_groups g
            JOIN group_members m ON g.id=m.group_id
            WHERE m.user_id=?
        """, (user_id,)).fetchall()
        return [dict(r) for r in rows]

# ─────────────────────────────────────────
#  ADMIN: CUSTOM CONTENT
# ─────────────────────────────────────────
def add_custom_lesson(admin_id: int, lang: str, level: str, title: str, content: str) -> int:
    now = datetime.now().isoformat()
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO custom_lessons(admin_id, lang, level, title, content, created_at)
            VALUES(?,?,?,?,?,?)
        """, (admin_id, lang, level, title, content, now))
        return cur.lastrowid

def get_custom_lessons(lang: str = None, level: str = None) -> list[dict]:
    with get_conn() as conn:
        query = "SELECT * FROM custom_lessons WHERE 1=1"
        params = []
        if lang:
            query += " AND lang=?"; params.append(lang)
        if level:
            query += " AND level=?"; params.append(level)
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

def add_custom_quiz(admin_id: int, lang: str, questions: list) -> int:
    now = datetime.now().isoformat()
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO custom_quizzes(admin_id, lang, q_json, created_at) VALUES(?,?,?,?)",
            (admin_id, lang, json.dumps(questions), now)
        )
        return cur.lastrowid

# ─────────────────────────────────────────
#  STATS FOR ADMIN
# ─────────────────────────────────────────
def get_global_stats() -> dict:
    with get_conn() as conn:
        total_users    = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        active_today   = conn.execute(
            "SELECT COUNT(*) FROM users WHERE last_active>=?",
            (date.today().isoformat(),)
        ).fetchone()[0]
        total_lessons  = conn.execute("SELECT SUM(total_lessons) FROM users").fetchone()[0] or 0
        total_vocab    = conn.execute("SELECT COUNT(*) FROM vocab").fetchone()[0]
        premium_users  = conn.execute("SELECT COUNT(*) FROM users WHERE is_premium=1").fetchone()[0]
        return {
            "total_users"  : total_users,
            "active_today" : active_today,
            "total_lessons": total_lessons,
            "total_vocab"  : total_vocab,
            "premium_users": premium_users,
        }
