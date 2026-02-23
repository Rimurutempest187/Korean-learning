"""
SUPER LEARNING BOT — Admin Command Handlers
============================================
All /admin commands: content management, stats,
broadcast, user management.
"""
import json
from datetime import datetime

from telegram import Update, InputFile
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

import database as db
import keyboards as kb
from config import FOOTER, ADMIN_IDS

# ─────────────────────────────────────────
#  GUARD DECORATOR
# ─────────────────────────────────────────
def admin_only(func):
    async def wrapper(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("⛔ *Admin access required.*", parse_mode=ParseMode.MARKDOWN)
            return
        return await func(update, ctx)
    wrapper.__name__ = func.__name__
    return wrapper

# ─────────────────────────────────────────
#  /stats — Global Statistics
# ─────────────────────────────────────────
@admin_only
async def cmd_admin_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    stats = db.get_global_stats()
    text  = (
        "📊 *Global Bot Statistics*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👥 Total Users:     *{stats['total_users']}*\n"
        f"🟢 Active Today:    *{stats['active_today']}*\n"
        f"📚 Total Lessons:   *{stats['total_lessons']}*\n"
        f"📖 Total Vocab:     *{stats['total_vocab']}*\n"
        f"⭐ Premium Users:   *{stats['premium_users']}*\n"
        + FOOTER
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# ─────────────────────────────────────────
#  /leaderboard — Admin view
# ─────────────────────────────────────────
@admin_only
async def cmd_admin_leaderboard(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    leaders = db.get_leaderboard(20)
    lines   = ["🏆 *Admin Leaderboard View (Top 20)*\n━━━━━━━━━━━━━━━━━━━━"]
    for i, row in enumerate(leaders, 1):
        lines.append(f"{i:2}. {row.get('full_name','?')[:15]} — XP:{row['xp']} | Streak:{row['streak']}d")
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)

# ─────────────────────────────────────────
#  /broadcast — Send message to all users
# ─────────────────────────────────────────
@admin_only
async def cmd_broadcast(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text(
            "📢 *Broadcast Usage:*\n`/broadcast Your message here`\n\n"
            "Add *CONFIRM* at the start to actually send:\n"
            "`/broadcast CONFIRM Your message`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if ctx.args[0].upper() != "CONFIRM":
        preview = " ".join(ctx.args)
        user_ids = db.get_all_user_ids()
        await update.message.reply_text(
            f"📢 *Broadcast Preview*\n━━━━━━━━━━━━━━━━\n\n{preview}\n\n"
            f"_Will send to {len(user_ids)} users._\n\n"
            f"To confirm: `/broadcast CONFIRM {preview}`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    message  = " ".join(ctx.args[1:])
    user_ids = db.get_all_user_ids()
    sent, failed = 0, 0

    await update.message.reply_text(f"📤 Broadcasting to {len(user_ids)} users...")

    for uid in user_ids:
        try:
            await ctx.bot.send_message(
                chat_id=uid,
                text=f"📢 *Announcement from SUPER LEARNING BOT:*\n\n{message}" + FOOTER,
                parse_mode=ParseMode.MARKDOWN
            )
            sent += 1
        except Exception:
            failed += 1

    await update.message.reply_text(
        f"✅ *Broadcast complete!*\nSent: {sent} | Failed: {failed}",
        parse_mode=ParseMode.MARKDOWN
    )

# ─────────────────────────────────────────
#  /edlesson — Add custom lesson
# ─────────────────────────────────────────
@admin_only
async def cmd_edlesson(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args or len(ctx.args) < 3:
        await update.message.reply_text(
            "📚 *Add Custom Lesson:*\n"
            "`/edlesson <lang> <level> <title> | <content>`\n\n"
            "Example:\n"
            "`/edlesson english A1 Colors | Red=🔴, Blue=🔵, Green=🟢`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    lang  = ctx.args[0].lower()
    level = ctx.args[1].upper()
    rest  = " ".join(ctx.args[2:])

    if "|" in rest:
        title, content = rest.split("|", 1)
    else:
        title, content = rest, rest

    lesson_id = db.add_custom_lesson(update.effective_user.id, lang, level, title.strip(), content.strip())
    await update.message.reply_text(
        f"✅ *Lesson added!*\nID: {lesson_id} | {lang.upper()} {level}: {title.strip()}",
        parse_mode=ParseMode.MARKDOWN
    )

# ─────────────────────────────────────────
#  /edvocab — Upload vocab set
# ─────────────────────────────────────────
@admin_only
async def cmd_edvocab(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *Upload Vocabulary Set:*\n\n"
        "Send a message in format:\n"
        "`/edvocab english`\n"
        "Then send words as:\n"
        "`word1 = meaning1`\n"
        "`word2 = meaning2`\n\n"
        "Or use `/save <word>` for individual words.",
        parse_mode=ParseMode.MARKDOWN
    )

# ─────────────────────────────────────────
#  /edquiz — Add custom quiz question
# ─────────────────────────────────────────
@admin_only
async def cmd_edquiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text(
            "🧪 *Add Quiz Question:*\n"
            "`/edquiz <lang> <question> | opt1 | opt2 | opt3 | opt4 | correct_index`\n\n"
            "Example:\n"
            "`/edquiz english What color is the sky? | Red | Blue | Green | Yellow | 1`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    lang = ctx.args[0].lower()
    rest = " ".join(ctx.args[1:])
    parts = [p.strip() for p in rest.split("|")]

    if len(parts) < 6:
        await update.message.reply_text("❌ Need: question | opt1 | opt2 | opt3 | opt4 | answer_index")
        return

    question = {"q": parts[0], "opts": parts[1:5], "ans": int(parts[5])}
    qid      = db.add_custom_quiz(update.effective_user.id, lang, [question])
    await update.message.reply_text(
        f"✅ *Quiz question added!* (ID: {qid})\n_{parts[0]}_",
        parse_mode=ParseMode.MARKDOWN
    )

# ─────────────────────────────────────────
#  /edpath — Manage roadmap
# ─────────────────────────────────────────
@admin_only
async def cmd_edpath(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🗺️ *Learning Path Management*\n\n"
        "Use /edlesson to add lessons to specific levels.\n"
        "Built-in path:\n"
        "🌱 A1 → 🌿 A2 → ⭐ B1 → 🌟 B2 → 💫 C1 → 👑 C2\n\n"
        "Custom lessons added via /edlesson appear in the path automatically.",
        parse_mode=ParseMode.MARKDOWN
    )

# ─────────────────────────────────────────
#  /edaudio — Upload listening files
# ─────────────────────────────────────────
@admin_only
async def cmd_edaudio(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎧 *Upload Audio Files:*\n\n"
        "Reply to an audio file with: `/edaudio <lang> <question> | opt1 | opt2 | opt3 | ans_index`\n\n"
        "Or use the TTS system:\n"
        "The bot auto-generates audio from text using gTTS (no upload needed).",
        parse_mode=ParseMode.MARKDOWN
    )

# ─────────────────────────────────────────
#  /roles — Assign roles
# ─────────────────────────────────────────
@admin_only
async def cmd_roles(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args or len(ctx.args) < 2:
        await update.message.reply_text(
            "👥 *Role Assignment:*\n"
            "`/roles premium <user_id>` — Grant premium\n"
            "`/roles revoke <user_id>` — Revoke premium\n"
            "`/roles admin add <user_id>` — Add admin (edit .env)",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    action  = ctx.args[0].lower()
    try:
        target_id = int(ctx.args[1])
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID")
        return

    if action == "premium":
        db.update_user(target_id, is_premium=1)
        await update.message.reply_text(f"✅ User {target_id} granted *Premium* status!", parse_mode=ParseMode.MARKDOWN)
    elif action == "revoke":
        db.update_user(target_id, is_premium=0)
        await update.message.reply_text(f"✅ User {target_id} premium *revoked*.", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("❌ Unknown action. Use: premium / revoke")

# ─────────────────────────────────────────
#  /set — Configure bot settings
# ─────────────────────────────────────────
@admin_only
async def cmd_set(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚙️ *Bot Configuration*\n━━━━━━━━━━━━━━━━\n\n"
        "Daily lesson time: Set in `.env` → `DAILY_LESSON_TIME`\n"
        "Evening review: Set in `.env` → `EVENING_REVIEW_TIME`\n"
        "Timezone: Set in `.env` → `TIMEZONE`\n\n"
        "Restart bot after changing .env settings.",
        parse_mode=ParseMode.MARKDOWN
    )

# ─────────────────────────────────────────
#  /backup — Backup database
# ─────────────────────────────────────────
@admin_only
async def cmd_backup(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    import shutil, os
    from config import DB_PATH
    backup_path = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    try:
        shutil.copy2(DB_PATH, backup_path)
        await update.message.reply_document(
            document=open(backup_path, "rb"),
            filename=backup_path,
            caption="✅ *Database backup created!*"
        )
        os.remove(backup_path)
    except Exception as e:
        await update.message.reply_text(f"❌ Backup failed: {e}")

# ─────────────────────────────────────────
#  /restore
# ─────────────────────────────────────────
@admin_only
async def cmd_restore(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔄 *Restore Database:*\n\n"
        "Reply to a .db backup file with /restore to restore.\n"
        "⚠️ This will *overwrite* current data!",
        parse_mode=ParseMode.MARKDOWN
    )

# ─────────────────────────────────────────
#  /resetuser
# ─────────────────────────────────────────
@admin_only
async def cmd_resetuser(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: `/resetuser <user_id>`", parse_mode=ParseMode.MARKDOWN)
        return

    try:
        target = int(ctx.args[0])
        db.update_user(target, xp=0, streak=0, total_lessons=0,
                       total_correct=0, total_questions=0, cefr_level="A1")
        await update.message.reply_text(f"✅ User {target} has been reset.", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
