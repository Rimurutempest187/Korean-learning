"""
╔══════════════════════════════════════════════════════════════╗
║          🌍 SUPER LEARNING BOT — Main Entry Point           ║
║                   Create by : PINLON-YOUTH                   ║
╚══════════════════════════════════════════════════════════════╝

REQUIREMENTS:
  - Python 3.11+
  - pip install -r requirements.txt
  - Edit .env: set BOT_TOKEN and ADMIN_IDS

RUN:
  python bot.py
"""

import logging
import asyncio
from telegram import Update, BotCommand
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters
)
from config import BOT_TOKEN
import database as db

# ─────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
#  IMPORT HANDLERS
# ─────────────────────────────────────────
from user_handlers import (
    cmd_start, cmd_lang, cmd_profile, cmd_learn, cmd_lesson,
    cmd_path, cmd_review, cmd_vocab, cmd_deck, cmd_save, cmd_flash,
    cmd_say, cmd_listen, cmd_repeat, cmd_tutor, cmd_roleplay, cmd_correct,
    cmd_quiz, cmd_challenge, cmd_exam, cmd_tops, cmd_progress, cmd_streak,
    cmd_badges, cmd_goal, cmd_studygroup, cmd_duel, cmd_share,
    cmd_translate, cmd_report, cmd_help
)
from admin_handlers import (
    cmd_admin_stats, cmd_admin_leaderboard, cmd_broadcast,
    cmd_edlesson, cmd_edvocab, cmd_edquiz, cmd_edpath, cmd_edaudio,
    cmd_roles, cmd_set, cmd_backup, cmd_restore, cmd_resetuser
)
from callback_handlers import handle_callback, handle_message

# ─────────────────────────────────────────
#  BOT COMMANDS MENU (shown in Telegram)
# ─────────────────────────────────────────
USER_COMMANDS = [
    BotCommand("start",       "🌍 Welcome & main menu"),
    BotCommand("lang",        "🌐 Change learning language"),
    BotCommand("profile",     "👤 Your stats & level"),
    BotCommand("learn",       "📚 Today's lesson"),
    BotCommand("lesson",      "📖 Specific lesson topic"),
    BotCommand("path",        "🗺️ Learning roadmap"),
    BotCommand("review",      "🔄 Spaced repetition review"),
    BotCommand("vocab",       "🔤 Daily vocabulary words"),
    BotCommand("deck",        "🗂️ Your saved words"),
    BotCommand("save",        "💾 Save a word to deck"),
    BotCommand("flash",       "🃏 Flashcard mode"),
    BotCommand("say",         "🔊 Hear pronunciation (TTS)"),
    BotCommand("listen",      "🎧 Listening exercise"),
    BotCommand("repeat",      "🔁 Shadowing practice"),
    BotCommand("tutor",       "💬 AI conversation tutor"),
    BotCommand("roleplay",    "🎭 Roleplay scenarios"),
    BotCommand("correct",     "✏️ Grammar check"),
    BotCommand("quiz",        "🧪 Random quiz"),
    BotCommand("challenge",   "⚡ Timed challenge"),
    BotCommand("exam",        "📝 Level test exam"),
    BotCommand("tops",        "🏆 Leaderboard"),
    BotCommand("progress",    "📊 Progress chart"),
    BotCommand("streak",      "🔥 Daily streak"),
    BotCommand("badges",      "🏅 Your achievements"),
    BotCommand("goal",        "🎯 Set daily goal"),
    BotCommand("studygroup",  "👥 Study groups"),
    BotCommand("duel",        "⚔️ Quiz duel battle"),
    BotCommand("share",       "🃏 Share progress card"),
    BotCommand("translate",   "🌐 Quick translation"),
    BotCommand("report",      "📨 Send feedback"),
    BotCommand("help",        "❓ Smart help menu"),
]

# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("❌ ERROR: Please set BOT_TOKEN in your .env file!")
        print("   Get your token from @BotFather on Telegram")
        return

    # Init database
    db.init_db()

    # Build application
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # ── Register User Command Handlers ─────────
    app.add_handler(CommandHandler("start",       cmd_start))
    app.add_handler(CommandHandler("lang",        cmd_lang))
    app.add_handler(CommandHandler("profile",     cmd_profile))
    app.add_handler(CommandHandler("learn",       cmd_learn))
    app.add_handler(CommandHandler("lesson",      cmd_lesson))
    app.add_handler(CommandHandler("path",        cmd_path))
    app.add_handler(CommandHandler("review",      cmd_review))
    app.add_handler(CommandHandler("vocab",       cmd_vocab))
    app.add_handler(CommandHandler("deck",        cmd_deck))
    app.add_handler(CommandHandler("save",        cmd_save))
    app.add_handler(CommandHandler("flash",       cmd_flash))
    app.add_handler(CommandHandler("say",         cmd_say))
    app.add_handler(CommandHandler("listen",      cmd_listen))
    app.add_handler(CommandHandler("repeat",      cmd_repeat))
    app.add_handler(CommandHandler("tutor",       cmd_tutor))
    app.add_handler(CommandHandler("roleplay",    cmd_roleplay))
    app.add_handler(CommandHandler("correct",     cmd_correct))
    app.add_handler(CommandHandler("quiz",        cmd_quiz))
    app.add_handler(CommandHandler("challenge",   cmd_challenge))
    app.add_handler(CommandHandler("exam",        cmd_exam))
    app.add_handler(CommandHandler("tops",        cmd_tops))
    app.add_handler(CommandHandler("progress",    cmd_progress))
    app.add_handler(CommandHandler("streak",      cmd_streak))
    app.add_handler(CommandHandler("badges",      cmd_badges))
    app.add_handler(CommandHandler("goal",        cmd_goal))
    app.add_handler(CommandHandler("studygroup",  cmd_studygroup))
    app.add_handler(CommandHandler("duel",        cmd_duel))
    app.add_handler(CommandHandler("share",       cmd_share))
    app.add_handler(CommandHandler("translate",   cmd_translate))
    app.add_handler(CommandHandler("report",      cmd_report))
    app.add_handler(CommandHandler("help",        cmd_help))

    # ── Register Admin Command Handlers ────────
    app.add_handler(CommandHandler("stats",       cmd_admin_stats))
    app.add_handler(CommandHandler("leaderboard", cmd_admin_leaderboard))
    app.add_handler(CommandHandler("broadcast",   cmd_broadcast))
    app.add_handler(CommandHandler("edlesson",    cmd_edlesson))
    app.add_handler(CommandHandler("edvocab",     cmd_edvocab))
    app.add_handler(CommandHandler("edquiz",      cmd_edquiz))
    app.add_handler(CommandHandler("edpath",      cmd_edpath))
    app.add_handler(CommandHandler("edaudio",     cmd_edaudio))
    app.add_handler(CommandHandler("roles",       cmd_roles))
    app.add_handler(CommandHandler("set",         cmd_set))
    app.add_handler(CommandHandler("backup",      cmd_backup))
    app.add_handler(CommandHandler("restore",     cmd_restore))
    app.add_handler(CommandHandler("resetuser",   cmd_resetuser))

    # ── Callback & Message Handlers ────────────
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ── Post-init: set commands menu & scheduler
    async def post_init(application: Application):
        await application.bot.set_my_commands(USER_COMMANDS)
        from scheduler import setup_scheduler
        setup_scheduler(application)
        info = await application.bot.get_me()
        print(f"\n{'='*50}")
        print(f"  🌍 SUPER LEARNING BOT")
        print(f"  Bot: @{info.username} ({info.full_name})")
        print(f"  Status: ✅ Running")
        print(f"  Create by: PINLON-YOUTH")
        print(f"{'='*50}\n")

    app.post_init = post_init

    # ── Run ────────────────────────────────────
    print("🚀 Starting SUPER LEARNING BOT...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
