"""
Lesson Handler - Manages lesson browsing and selection
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from managers.user_manager import UserManager
from managers.lesson_manager import LessonManager
from config import Config
from utils.formatter import escape_markdown, create_progress_bar

logger = logging.getLogger(__name__)


class LessonHandler:
    """Handles lesson navigation and content display"""
    
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
        self.lesson_manager = LessonManager()
        self.config = Config()
    
    async def learn_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show language selection menu"""
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = update.effective_user.id
        else:
            user_id = update.effective_user.id
        
        text = (
            "*📚 Choose Your Language*\n\n"
            "Select which language you want to learn:\n"
            "All lessons are translated to Myanmar 🇲🇲"
        )
        
        keyboard = []
        for lang_code, lang_data in self.config.LANGUAGES.items():
            keyboard.append([
                InlineKeyboardButton(
                    lang_data['name'],
                    callback_data=f"lang_{lang_code}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")])
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="MarkdownV2"
            )
        else:
            await update.message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="MarkdownV2"
            )
    
    async def handle_language_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle language selection"""
        query = update.callback_query
        await query.answer()
        
        language = query.data.split("_")[1]
        context.user_data['selected_language'] = language
        
        # Update user's current language
        await self.user_manager.db.execute(
            "UPDATE users SET current_language = ? WHERE user_id = ?",
            (language, update.effective_user.id)
        )
        
        # Show units
        await self._show_units(query, language)
    
    async def _show_units(self, query, language: str):
        """Show available units for selected language"""
        lang_name = self.config.LANGUAGES[language]['name']
        
        # Get user progress
        user_id = query.from_user.id
        progress = await self.user_manager.get_user_progress(user_id, language)
        
        text = (
            f"*{escape_markdown(lang_name)} Lessons*\n\n"
            f"📊 Completed: {progress['total_lessons']} lessons\n\n"
            f"Select your level:"
        )
        
        keyboard = []
        for unit in self.config.UNITS:
            unit_lessons = self.lesson_manager.get_lessons(language, unit)
            if unit_lessons:
                # Count completed lessons in this unit
                completed_in_unit = len([
                    l for l in progress['lessons'] 
                    if l['unit'] == unit
                ])
                total_in_unit = len(unit_lessons)
                progress_bar = create_progress_bar(completed_in_unit, total_in_unit)
                
                keyboard.append([
                    InlineKeyboardButton(
                        f"{'🔰' if unit == 'beginner' else '⚡️' if unit == 'intermediate' else '🏆'} "
                        f"{unit.title()} {progress_bar}",
                        callback_data=f"unit_{language}_{unit}"
                    )
                ])
        
        keyboard.append([InlineKeyboardButton("← Back", callback_data="menu_learn")])
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="MarkdownV2"
        )
    
    async def handle_unit_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle unit selection and show lessons"""
        query = update.callback_query
        await query.answer()
        
        _, language, unit = query.data.split("_")
        context.user_data['selected_unit'] = unit
        
        lessons = self.lesson_manager.get_lessons(language, unit)
        
        if not lessons:
            await query.edit_message_text(
                f"*{unit.title()} Level*\n\n"
                f"No lessons available yet\\. Coming soon\\! 🚧",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("← Back", callback_data=f"lang_{language}")
                ]]),
                parse_mode="MarkdownV2"
            )
            return
        
        text = f"*{unit.title()} Lessons*\n\nSelect a lesson:"
        
        keyboard = []
        for lesson in lessons:
            # Check if completed
            progress = await self.user_manager.db.fetch_one(
                """SELECT completed, score FROM progress 
                   WHERE user_id = ? AND language = ? AND unit = ? AND lesson_id = ?""",
                (query.from_user.id, language, unit, lesson['id'])
            )
            
            status = "✅" if progress and progress['completed'] else "📝"
            score_text = f" ({progress['score']}%)" if progress and progress['completed'] else ""
            
            keyboard.append([
                InlineKeyboardButton(
                    f"{status} {lesson['title']}{score_text}",
                    callback_data=f"lesson_{language}_{unit}_{lesson['id']}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("← Back", callback_data=f"lang_{language}")])
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="MarkdownV2"
        )
    
    async def handle_lesson_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Display lesson content"""
        query = update.callback_query
        await query.answer()
        
        _, language, unit, lesson_id = query.data.split("_", 3)
        
        lesson = self.lesson_manager.get_lesson(language, unit, lesson_id)
        
        if not lesson:
            await query.answer("Lesson not found!", show_alert=True)
            return
        
        # Check hearts
        user = await self.user_manager.get_or_create_user(query.from_user.id)
        if user['hearts'] <= 0:
            await query.answer(
                "❤️ No hearts left! Wait for refill or comeback later.",
                show_alert=True
            )
            return
        
        # Build lesson content
        text = f"*{escape_markdown(lesson['title'])}*\n\n"
        text += f"_{escape_markdown(lesson['description'])}_\n\n"
        text += "*Vocabulary:*\n\n"
        
        for item in lesson['vocabulary'][:5]:  # Show first 5 words
            word = escape_markdown(item['word'])
            translation = escape_markdown(item['translation'])
            
            if language == 'japanese' and 'furigana' in item:
                furigana = escape_markdown(item['furigana'])
                text += f"• {word} \\({furigana}\\) \\- {translation}\n"
            elif language == 'korean' and 'romanization' in item:
                roman = escape_markdown(item['romanization'])
                text += f"• {word} \\({roman}\\) \\- {translation}\n"
            else:
                text += f"• {word} \\- {translation}\n"
        
        text += f"\n*Ready to test your knowledge?*"
        
        keyboard = [
            [InlineKeyboardButton("🎯 Start Quiz", callback_data=f"quiz_{language}_{unit}_{lesson_id}")],
            [InlineKeyboardButton("← Back", callback_data=f"unit_{language}_{unit}")]
        ]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="MarkdownV2"
        )#  YES / NO
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
