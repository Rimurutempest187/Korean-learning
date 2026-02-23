"""
SUPER LEARNING BOT — Scheduled Tasks
=====================================
Daily lesson drop, evening review reminder,
streak warning, motivational quotes.
All using APScheduler — no external service needed.
"""
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram.ext import Application
from telegram.constants import ParseMode

import database as db
import utils
import keyboards as kb
from config import TIMEZONE, DAILY_TIME, REVIEW_TIME, FOOTER


def setup_scheduler(app: Application) -> AsyncIOScheduler:
    tz        = pytz.timezone(TIMEZONE)
    scheduler = AsyncIOScheduler(timezone=tz)

    # Parse times
    daily_h, daily_m   = [int(x) for x in DAILY_TIME.split(":")]
    review_h, review_m = [int(x) for x in REVIEW_TIME.split(":")]

    # ── Daily lesson notification ──────────────
    @scheduler.scheduled_job(CronTrigger(hour=daily_h, minute=daily_m, timezone=tz))
    async def daily_lesson_notification():
        user_ids = db.get_all_user_ids()
        quote    = utils.get_daily_quote()
        for uid in user_ids:
            try:
                user_d = db.get_user(uid)
                if not user_d:
                    continue
                await app.bot.send_message(
                    chat_id=uid,
                    text=(
                        f"☀️ *Good Morning, {user_d['full_name']}!*\n━━━━━━━━━━━━━━━━\n\n"
                        f"📅 *Today's Learning Plan:*\n"
                        f"• 📚 Daily lesson\n"
                        f"• 🔤 5 new vocabulary words\n"
                        f"• 🧪 1 quick quiz\n\n"
                        f"{quote}\n\n"
                        f"🔥 Streak: *{user_d['streak']} days* — keep it going!" + FOOTER
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=kb.Markup([[
                        kb.Btn("📚 Start Lesson", callback_data="learn_daily"),
                        kb.Btn("📖 Daily Words",  callback_data="vocab_daily"),
                    ]])
                )
            except Exception:
                pass

    # ── Evening review reminder ────────────────
    @scheduler.scheduled_job(CronTrigger(hour=review_h, minute=review_m, timezone=tz))
    async def evening_review():
        from datetime import date
        user_ids = db.get_all_user_ids()
        today    = date.today().isoformat()
        for uid in user_ids:
            try:
                user_d = db.get_user(uid)
                if not user_d:
                    continue
                last_active = (user_d.get("last_active") or "")[:10]
                if last_active != today:
                    await app.bot.send_message(
                        chat_id=uid,
                        text=(
                            f"🌙 *Evening Review, {user_d['full_name']}!*\n━━━━━━━━━━━━━━━━\n\n"
                            f"⚠️ You haven't studied today yet!\n\n"
                            f"🔥 Don't break your *{user_d['streak']} day streak!*\n"
                            f"Just 5 minutes is enough! ⏱" + FOOTER
                        ),
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=kb.Markup([[
                            kb.Btn("📚 Quick Lesson", callback_data="learn_daily"),
                            kb.Btn("🧪 Quick Quiz",   callback_data="quiz_random"),
                        ]])
                    )
            except Exception:
                pass

    # ── Weekly progress summary (Sunday 9 AM) ─
    @scheduler.scheduled_job(CronTrigger(day_of_week="sun", hour=9, minute=0, timezone=tz))
    async def weekly_summary():
        user_ids = db.get_all_user_ids()
        for uid in user_ids:
            try:
                user_d = db.get_user(uid)
                if not user_d:
                    continue
                xp     = user_d["xp"]
                from config import get_level
                lv_name, _, _ = get_level(xp)
                total  = user_d.get("total_questions", 0)
                correct = user_d.get("total_correct", 0)
                acc    = f"{int(correct/total*100)}%" if total else "N/A"

                await app.bot.send_message(
                    chat_id=uid,
                    text=(
                        f"📊 *Weekly Report — {user_d['full_name']}*\n━━━━━━━━━━━━━━━━\n\n"
                        f"🏅 Level: *{user_d['cefr_level']}* ({lv_name})\n"
                        f"✅ Accuracy: *{acc}*\n"
                        f"🔥 Streak: *{user_d['streak']} days*\n"
                        f"⭐ XP: *{xp}*\n\n"
                        f"Keep up the amazing work! 🚀" + FOOTER
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=kb.main_menu()
                )
            except Exception:
                pass

    scheduler.start()
    print(f"✅ Scheduler started — Daily: {DAILY_TIME}, Review: {REVIEW_TIME} ({TIMEZONE})")
    return scheduler
