"""
SUPER LEARNING BOT — Configuration Module
==========================================
All config constants, XP rules, badge definitions,
supported languages, and lesson level maps.
"""
import os
from dotenv import load_dotenv
# config.py ရဲ့ အပေါ်ဆုံးမှာ import လုပ်ပါ
from typing import Optional

# line 105 ကို အောက်ပါအတိုင်း ပြင်ပါ
load_dotenv()

# ─────────────────────────────────────────
#  BOT CORE
#  ─────────────────────────────────────────
BOT_TOKEN   = os.getenv("BOT_TOKEN", "")
ADMIN_IDS   = [int(x) for x in os.getenv("ADMIN_IDS", "0").split(",") if x.strip().isdigit()]
DB_PATH     = os.getenv("DB_PATH", "super_learning_bot.db")
 TIMEZONE    = os.getenv("TIMEZONE", "Asia/Yangon")
DAILY_TIME  = os.getenv("DAILY_LESSON_TIME", "08:00")
REVIEW_TIME = os.getenv("EVENING_REVIEW_TIME", "20:00")

# ─────────────────────────────────────────
#  GAMIFICATION
# ─────────────────────────────────────────
XP_RULES = {
    "lesson_complete"   : 50,
    "quiz_correct"      : 10,
    "quiz_wrong"        : 0,
    "daily_streak"      : 20,
    "flashcard_session" : 15,
    "review_session"    : 25,
    "duel_win"          : 40,
    "duel_participate"  : 10,
    "share_card"        : 5,
}

LEVELS = [
    (0,     "🌱 Seed"),
    (100,   "🌿 Sprout"),
    (300,   "🌳 Sapling"),
    (600,   "⭐ Star"),
    (1000,  "🌟 Rising Star"),
    (1500,  "💫 Bright"),
    (2200,  "🔥 Flame"),
    (3000,  "💎 Diamond"),
    (4500,  "🏆 Champion"),
    (6000,  "👑 Master"),
    (10000, "🚀 Legend"),
]

def get_level(xp: int) -> tuple[str, int, int]:
    """Returns (level_name, current_level_index, xp_for_next_level)."""
    for i, (req, name) in enumerate(LEVELS):
        if xp < req:
            return LEVELS[i - 1][1] if i > 0 else LEVELS[0][1], i - 1, req
    return LEVELS[-1][1], len(LEVELS) - 1, -1

BADGES = {
    "first_lesson"   : ("🎯", "First Step",    "Complete your first lesson"),
    "week_streak"    : ("🔥", "Week Warrior",  "7-day login streak"),
    "month_streak"   : ("🌙", "Moon Walker",   "30-day login streak"),
    "vocab_100"      : ("📖", "Word Hoarder",  "Save 100 vocabulary words"),
    "quiz_ace"       : ("🧠", "Quiz Ace",      "Score 100% on a quiz"),
    "speed_demon"    : ("⚡", "Speed Demon",   "Complete a challenge in <60s"),
    "social_star"    : ("🤝", "Social Star",   "Join 5 study groups"),
    "duel_master"    : ("⚔️",  "Duel Master",   "Win 10 duels"),
    "polyglot"       : ("🌍", "Polyglot",      "Study 3 different languages"),
    "completionist"  : ("🏅", "Completionist", "Finish all lessons in a path"),
}

# ─────────────────────────────────────────
 #  SUPPORTED LANGUAGES
# ─────────────────────────────────────────
SUPPORTED_LANGS = {
    "english"   : {"code": "en", "name": "🇺🇸 English",   "tts_lang": "en"},
    "korean"    : {"code": "ko", "name": "🇰🇷 Korean",    "tts_lang": "ko"},
    "japanese"   : {"code": "ja", "name": "🇯🇵 Japanese",  "tts_lang": "ja"},
    "chinese"   : {"code": "zh-cn", "name": "🇨🇳 Chinese", "tts_lang": "zh"},
    "burmese"   : {"code": "my", "name": "🇲🇲 Burmese",   "tts_lang": "my"},
    "french"    : {"code": "fr", "name": "🇫🇷 French",    "tts_lang": "fr"},
    "german"    : {"code": "de", "name": "🇩🇪 German",    "tts_lang": "de"},
    "spanish"   : {"code": "es", "name": "🇪🇸 Spanish",   "tts_lang": "es"},
    "thai"      : {"code": "th", "name": "🇹🇭 Thai",      "tts_lang": "th"},
    "vietnamese": {"code": "vi", "name": "🇻🇳 Vietnamese","tts_lang": "vi"},
}

LANG_ALIASES = {
    "eng"     : "english",
    "kor"     : "korean",
    "jp"      : "japanese",
    "jap"     : "japanese",
    "chn"     : "chinese",
    "chi"     : "chinese",
    "myan"    : "burmese",
    "mm"      : "burmese",
    "fr"      : "french",
    "de"      : "german",
    "es"      : "spanish",
    "spa"     : "spanish",
    "th"      : "thai",
    "viet"    : "vietnamese",
    "vi"      : "vietnamese",
}
def resolve_lang(text: str) -> Optional[str]:
    key = text.strip().lower()
    if key in SUPPORTED_LANGS:
        return key
    return LANG_ALIASES.get(key)

# ─────────────────────────────────────────
#  LEVEL SYSTEM
# ─────────────────────────────────────────
CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

# ─────────────────────────────────────────
#  UI CONSTANTS
# ─────────────────────────────────────────
FOOTER = "\n\n─────────────────\n_Create by : **PINLON-YOUTH**_"

MAIN_MENU_TEXT = (
    "🌍 *SUPER LEARNING BOT*\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Choose what you want to do:"
)
 
