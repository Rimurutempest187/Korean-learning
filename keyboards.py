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
        [Btn("📚 Learn",    callback_data="menu_learn"),
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
def quiz_options(options: list, session_id: int, q_index: int):
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
#  LEARNING MENUS
# ─────────────────────────────────────────
def learn_menu():
    return Markup([
        [Btn("📅 Daily Lesson", callback_data="learn_daily"),
         Btn("🗺️ Learning Path", callback_data="learn_path")],
        [Btn("🎧 Listening", callback_data="learn_listen"),
         Btn("🔄 Review",    callback_data="learn_review")],
        [Btn("◀️ Menu",      callback_data="menu_main")],
    ])

def vocab_menu():
    return Markup([
        [Btn("📖 Daily Words",   callback_data="vocab_daily"),
         Btn("🗂️ My Deck",       callback_data="vocab_deck")],
        [Btn("🃏 Flashcards",    callback_data="vocab_flash"),
         Btn("📥 Review Due",    callback_data="vocab_review")],
        [Btn("◀️ Menu",          callback_data="menu_main")],
    ])

def quiz_menu():
    return Markup([
        [Btn("🎲 Random Quiz",   callback_data="quiz_random"),
         Btn("⚡ Challenge",      callback_data="quiz_challenge")],
        [Btn("📝 Level Exam",    callback_data="quiz_exam"),
         Btn("🏆 Leaderboard",   callback_data="quiz_tops")],
        [Btn("◀️ Menu",          callback_data="menu_main")],
    ])

def social_menu():
    return Markup([
        [Btn("👥 Study Groups",  callback_data="social_groups"),
         Btn("⚔️ Duel",          callback_data="social_duel")],
        [Btn("🃏 Share Card",    callback_data="social_share"),
         Btn("◀️ Menu",          callback_data="menu_main")],
    ])

def settings_menu():
    return Markup([
        [Btn("🌍 Change Language", callback_data="settings_lang"),
         Btn("🎯 Daily Goal",      callback_data="settings_goal")],
        [Btn("👤 Profile",         callback_data="settings_profile"),
         Btn("◀️ Menu",            callback_data="menu_main")],
    ])

def tutor_menu():
    return Markup([
        [Btn("💬 Free Chat",       callback_data="tutor_chat"),
         Btn("🎭 Roleplay",        callback_data="tutor_roleplay")],
        [Btn("✏️ Grammar Check",   callback_data="tutor_grammar"),
         Btn("🔁 Shadowing",       callback_data="tutor_shadow")],
        [Btn("◀️ Menu",            callback_data="menu_main")],
    ])

def roleplay_picker():
    # handle dynamic import to avoid circular dependency
    try:
        from lessons_data import ROLEPLAY_SCENARIOS
    except ImportError:
        ROLEPLAY_SCENARIOS = {}
        
    rows = []
    items = list(ROLEPLAY_SCENARIOS.items())
    for i in range(0, len(items), 2):
        row = []
        for key, info in items[i:i+2]:
            row.append(Btn(info["title"], callback_data=f"roleplay:{key}"))
        rows.append(row)
    rows.append([Btn("◀️ Back", callback_data="menu_tutor")])
    return Markup(rows)

def goal_picker():
    options = [5, 10, 15, 20, 30, 45, 60]
    rows = []
    for i in range(0, len(options), 3):
        row = [Btn(f"⏱ {m} min", callback_data=f"goal:{m}") for m in options[i:i+3]]
        rows.append(row)
    rows.append([Btn("◀️ Back", callback_data="menu_settings")])
    return Markup(rows)

def flashcard_rating(vocab_id: int):
    return Markup([[
        Btn("😰 Hard (1)",  callback_data=f"fc:{vocab_id}:1"),
        Btn("🤔 OK (3)",    callback_data=f"fc:{vocab_id}:3"),
        Btn("😄 Easy (5)",  callback_data=f"fc:{vocab_id}:5"),
    ]])

def duel_invite(duel_id: int):
    return Markup([[
        Btn("⚔️ Accept", callback_data=f"duel_accept:{duel_id}"),
        Btn("❌ Decline", callback_data=f"duel_decline:{duel_id}"),
    ]])
