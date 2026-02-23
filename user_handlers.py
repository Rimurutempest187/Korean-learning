"""
SUPER LEARNING BOT — User Command Handlers
==========================================
All /commands for regular users.
"""
import io
import json
import random
from datetime import datetime

from telegram import Update, InputFile
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

import database as db
import keyboards as kb
import utils
from config import (FOOTER, MAIN_MENU_TEXT, SUPPORTED_LANGS, ADMIN_IDS,
                    XP_RULES, BADGES, get_level, resolve_lang)
from lessons_data import (get_daily_lesson, get_lesson, get_daily_words,
                          LEVEL_TEST, determine_level, ROLEPLAY_SCENARIOS,
                          get_listening_exercise, ALL_LESSONS, CEFR_LEVELS)

# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────
async def send(update: Update, text: str, **kw):
    """Helper for replying with Markdown."""
    kw.setdefault("parse_mode", ParseMode.MARKDOWN)
    kw.setdefault("disable_web_page_preview", True)
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(text, **kw)
        except Exception:
            await update.callback_query.message.reply_text(text, **kw)
    else:
        await update.message.reply_text(text, **kw)

def _ensure_user(user_id, username, full_name):
    db.upsert_user(user_id, username, full_name)
    streak = db.update_streak(user_id)
    return db.get_user(user_id), streak

# ─────────────────────────────────────────
#  /start
# ─────────────────────────────────────────
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    user_d, streak = _ensure_user(u.id, u.username or "", u.full_name or "User")

    welcome = (
        "🌍 *SUPER LEARNING BOT*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Welcome back, *{u.first_name}*! 👋\n\n"
        f"🔥 Streak: *{streak} day(s)*\n"
        f"⭐ XP: *{user_d['xp']}*\n\n"
        "What would you like to do today?\n"
        + FOOTER
    )
    await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN, reply_markup=kb.main_menu())

# ─────────────────────────────────────────
#  /lang
# ─────────────────────────────────────────
async def cmd_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")

    if ctx.args:
        lang_key = resolve_lang(" ".join(ctx.args))
        if lang_key:
            db.update_user(u.id, lang=lang_key)
            info = SUPPORTED_LANGS[lang_key]
            await update.message.reply_text(
                f"✅ Learning language set to *{info['name']}*!\n\nUse /learn to start your first lesson.",
                parse_mode=ParseMode.MARKDOWN
            )
            return

    text = "🌍 *Choose your learning language:*\n\nTip: You can also use `/lang Korean` etc."
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb.lang_picker())

# ─────────────────────────────────────────
#  /profile
# ─────────────────────────────────────────
async def cmd_profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)
    badges = db.get_user_badges(u.id)

    xp       = user_d["xp"]
    lv_name, _, xp_next = get_level(xp)
    total    = user_d.get("total_questions", 0)
    correct  = user_d.get("total_correct", 0)
    accuracy = f"{int(correct/total*100)}%" if total else "N/A"

    badge_line = " ".join(BADGES[b][0] for b in badges) if badges else "None yet"

    text = (
        f"👤 *{user_d['full_name']}*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🌍 Language: *{SUPPORTED_LANGS.get(user_d['lang'], {}).get('name', user_d['lang'])}*\n"
        f"📊 Level: *{user_d['cefr_level']}* | {lv_name}\n"
        f"⭐ XP: *{xp}*" + (f" / {xp_next}" if xp_next > 0 else " (MAX)") + "\n"
        f"🔥 Streak: *{user_d['streak']} days*\n"
        f"📚 Lessons Done: *{user_d['total_lessons']}*\n"
        f"✅ Accuracy: *{accuracy}*\n"
        f"🏅 Badges: {badge_line}\n"
        + FOOTER
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb.back_btn())

# ─────────────────────────────────────────
#  /learn
# ─────────────────────────────────────────
async def cmd_learn(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)
    lang   = user_d["lang"]
    level  = user_d["cefr_level"]

    completed = db.get_completed_lessons(u.id, lang)
    result    = get_daily_lesson(lang, level, completed)

    if not result:
        await update.message.reply_text(
            "🎉 *You've completed all available lessons for this level!*\n\n"
            "Use /path to advance to the next level or /review for spaced repetition.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    lesson_key, lesson = result
    db.set_state(u.id, "lesson", {"key": lesson_key, "lang": lang, "level": level, "step": 0})
    await _deliver_lesson(update, lesson, lesson_key)

async def _deliver_lesson(update: Update, lesson: dict, key: str):
    vocab = lesson.get("vocab", [])
    grammar = lesson.get("grammar", {})

    text = (
        f"📚 *{lesson['title']}*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔤 *Vocabulary:*\n"
    )
    for item in vocab[:6]:
        text += f"• **{item['word']}** — {item['meaning']}\n  _{item['example']}_\n"

    if grammar:
        text += (
            f"\n📖 *Grammar: {grammar.get('rule', '')}*\n"
            f"_{grammar.get('example', '')}_\n"
            f"{grammar.get('tip', '')}\n"
        )

    text += "\n✅ Tap below to take the quiz!"
    markup = kb.Markup([[
        kb.Btn("🧪 Take Quiz", callback_data=f"lesson_quiz:{key}"),
        kb.Btn("⏭️ Skip",       callback_data="lesson_skip"),
    ]])
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)

# ─────────────────────────────────────────
#  /lesson <topic>
# ─────────────────────────────────────────
async def cmd_lesson(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)

    if not ctx.args:
        await update.message.reply_text(
            "📚 *Lesson Topics Available:*\n\nUsage: `/lesson greetings` or `/lesson shopping`\n\n"
            "Available topics:\n• greetings\n• numbers\n• colors\n• daily_routine\n• shopping\n• travel\n"
            "• hangul_basics (Korean)\n• hiragana (Japanese)",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    topic  = "_".join(ctx.args).lower()
    lang   = user_d["lang"]
    level  = user_d["cefr_level"]

    lesson = get_lesson(lang, level, topic)
    if not lesson:
        # Search all levels
        for lv in CEFR_LEVELS:
            lesson = get_lesson(lang, lv, topic)
            if lesson:
                level = lv
                break

    if not lesson:
        await update.message.reply_text(
            f"❌ No lesson found for *{topic}*.\nTry /learn for your daily lesson.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    db.set_state(u.id, "lesson", {"key": topic, "lang": lang, "level": level, "step": 0})
    await _deliver_lesson(update, lesson, topic)

# ─────────────────────────────────────────
#  /path — Learning Roadmap
# ─────────────────────────────────────────
async def cmd_path(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d    = db.get_user(u.id)
    lang      = user_d["lang"]
    cur_level = user_d["cefr_level"]
    completed = db.get_completed_lessons(u.id, lang)

    lang_data = ALL_LESSONS.get(lang, {})
    lines = [f"🗺️ *Learning Roadmap — {SUPPORTED_LANGS.get(lang, {}).get('name', lang)}*\n━━━━━━━━━━━━━━"]

    level_labels = {
        "A1": "🌱 A1 – Beginner",     "A2": "🌿 A2 – Elementary",
        "B1": "⭐ B1 – Intermediate",  "B2": "🌟 B2 – Upper-Int",
        "C1": "💫 C1 – Advanced",      "C2": "👑 C2 – Mastery",
    }

    for lv in CEFR_LEVELS:
        marker = " ← *YOU ARE HERE*" if lv == cur_level else ""
        lessons_in_level = lang_data.get(lv, {})
        lines.append(f"\n{level_labels.get(lv, lv)}{marker}")
        if lessons_in_level:
            for key, les in lessons_in_level.items():
                done = "✅" if key in completed else "🔲"
                lines.append(f"  {done} {les['title']}")
        else:
            lines.append("  _(More lessons coming soon)_")

    lines.append(FOOTER)
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=kb.level_picker("advlevel"))

# ─────────────────────────────────────────
#  /review — Spaced Repetition
# ─────────────────────────────────────────
async def cmd_review(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    due    = db.get_due_reviews(u.id)

    if not due:
        await update.message.reply_text(
            "🎉 *No vocabulary due for review right now!*\n\n"
            "Come back later or add more words with /save.\n"
            "Keep it up! 🌟", parse_mode=ParseMode.MARKDOWN
        )
        return

    questions = utils.build_vocab_quiz(due, count=min(len(due), 8))
    if not questions:
        await update.message.reply_text("Not enough vocab for review yet. Add more with /save <word>")
        return

    sid   = db.start_quiz_session(u.id, questions, mode="review")
    db.set_state(u.id, "quiz", {"sid": sid, "questions": questions, "index": 0, "score": 0, "answers": []})
    await _send_quiz_question(update, questions[0], sid, 0)

# ─────────────────────────────────────────
#  VOCAB COMMANDS
# ─────────────────────────────────────────
async def cmd_vocab(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)
    words  = utils.get_daily_words(user_d["lang"], 5)

    text = "📖 *Today's Vocabulary*\n━━━━━━━━━━━━━━━━━━━━\n\n"
    for i, w in enumerate(words, 1):
        text += f"*{i}. {w['word']}*\n   📝 {w['meaning']}\n   💬 _{w['example']}_\n\n"
    text += "_Tip: Use /save <word> to add to your deck!_" + FOOTER

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb.vocab_menu())

async def cmd_deck(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u     = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)
    deck  = db.get_vocab_deck(u.id, user_d["lang"])

    if not deck:
        await update.message.reply_text(
            "📭 *Your vocabulary deck is empty!*\n\n"
            "Use `/save word` to add words to your deck.\nOr use /vocab for today's words.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    text = f"🗂️ *Your Vocabulary Deck* ({len(deck)} words)\n━━━━━━━━━━━━━━━━━━\n\n"
    for item in deck[:15]:
        text += f"• *{item['word']}* — {item['meaning']}\n"
    if len(deck) > 15:
        text += f"\n_...and {len(deck)-15} more words._"
    text += FOOTER

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb.vocab_menu())

async def cmd_save(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")

    if not ctx.args:
        await update.message.reply_text("Usage: `/save <word>`\nExample: `/save resilient`", parse_mode=ParseMode.MARKDOWN)
        return

    word    = " ".join(ctx.args)
    user_d  = db.get_user(u.id)
    lang    = user_d["lang"]
    lang_code = SUPPORTED_LANGS.get(lang, {}).get("code", "en")

    # Auto-translate to get meaning
    try:
        from deep_translator import GoogleTranslator
        meaning = GoogleTranslator(source="auto", target="en").translate(word)
        if meaning.lower() == word.lower():
            meaning = f"(meaning of '{word}')"
    except Exception:
        meaning = f"(meaning of '{word}')"

    saved = db.save_vocab(u.id, word, meaning, f"Example with: {word}", lang)

    if saved:
        # Badge check
        count = db.count_vocab(u.id)
        if count >= 100 and db.award_badge(u.id, "vocab_100"):
            await update.message.reply_text("🏅 *New Badge: Word Hoarder!* You've saved 100 words!", parse_mode=ParseMode.MARKDOWN)

        db.add_xp(u.id, 2)
        await update.message.reply_text(
            f"✅ *Saved!*\n\n*{word}* → {meaning}\n\nTotal words: *{count}*",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(f"ℹ️ *{word}* is already in your deck!", parse_mode=ParseMode.MARKDOWN)

async def cmd_flash(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)
    deck   = db.get_vocab_deck(u.id, user_d["lang"])

    if len(deck) < 2:
        await update.message.reply_text(
            "❌ Need at least 2 words in your deck for flashcards!\nUse /save to add words.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    random.shuffle(deck)
    card   = deck[0]
    db.set_state(u.id, "flashcard", {"deck": [d["id"] for d in deck], "index": 0})
    db.add_xp(u.id, XP_RULES["flashcard_session"])

    text = (
        f"🃏 *Flashcard Mode*\n━━━━━━━━━━━━━━━━\n\n"
        f"*Word:* {card['word']}\n\n"
        f"||*Meaning:* {card['meaning']}||\n"
        f"_Tap to reveal · Rate your memory!_"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=kb.flashcard_rating(card["id"]))

# ─────────────────────────────────────────
#  PRONUNCIATION / TTS
# ─────────────────────────────────────────
async def cmd_say(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")

    if not ctx.args:
        await update.message.reply_text("Usage: `/say <text>`\nExample: `/say Good morning!`", parse_mode=ParseMode.MARKDOWN)
        return

    text   = " ".join(ctx.args)
    user_d = db.get_user(u.id)
    lang_code = SUPPORTED_LANGS.get(user_d["lang"], {}).get("tts_lang", "en")

    await update.message.reply_text("🔊 Generating audio...")
    path = utils.generate_tts(text, lang_code)

    if path:
        await update.message.reply_voice(voice=open(path, "rb"), caption=f"🔊 _{text}_")
    else:
        await update.message.reply_text("❌ TTS failed. Please try again.")

async def cmd_listen(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)
    lang   = user_d["lang"]

    exercise = get_listening_exercise(lang)
    lang_code = SUPPORTED_LANGS.get(lang, {}).get("tts_lang", "en")

    await update.message.reply_text("🎧 *Listening Exercise*\nGenerating audio...")
    path = utils.generate_tts(exercise["text"], lang_code)

    if path:
        await update.message.reply_voice(
            voice=open(path, "rb"),
            caption="🎧 *Listen carefully, then answer the question below!*"
        )

    markup = kb.Markup([
        [kb.Btn(f"{i+1}. {opt}", callback_data=f"listen:{exercise['ans']}:{i}")]
        for i, opt in enumerate(exercise["opts"])
    ])
    await update.message.reply_text(
        f"❓ *{exercise['question']}*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup
    )

async def cmd_repeat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔁 *Shadowing Practice Mode*\n━━━━━━━━━━━━━━━━\n\n"
        "1️⃣ Listen to the audio carefully\n"
        "2️⃣ Repeat exactly what you hear\n"
        "3️⃣ Record yourself and compare\n\n"
        "Try: `/say I would like a table for two, please.`\n"
        "_Shadowing improves pronunciation & fluency!_ 🎤" + FOOTER,
        parse_mode=ParseMode.MARKDOWN
    )

# ─────────────────────────────────────────
#  TUTOR MODE
# ─────────────────────────────────────────
async def cmd_tutor(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    db.set_state(u.id, "tutor", {"mode": "chat"})

    await update.message.reply_text(
        "💬 *AI Tutor Mode*\n━━━━━━━━━━━━━━━━\n\n"
        "I'm your language tutor! You can:\n"
        "• Chat freely to practice your language\n"
        "• Ask grammar questions\n"
        "• Request translation help\n\n"
        "_Just type anything to start!_\nType /exit to leave tutor mode." + FOOTER,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb.tutor_menu()
    )

async def cmd_roleplay(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")

    if ctx.args:
        scenario_key = "_".join(ctx.args).lower()
        if scenario_key in ROLEPLAY_SCENARIOS:
            await _start_roleplay(update, u.id, scenario_key)
            return

    await update.message.reply_text(
        "🎭 *Choose a Roleplay Scenario:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb.roleplay_picker()
    )

async def _start_roleplay(update: Update, user_id: int, scenario_key: str):
    scenario = ROLEPLAY_SCENARIOS[scenario_key]
    db.set_state(user_id, "roleplay", {"key": scenario_key, "step": 0})

    prompt = scenario["prompts"][0]
    vocab_list = ", ".join(scenario["vocab"][:5])

    text = (
        f"🎭 *{scenario['title']}*\n━━━━━━━━━━━━━━━━━━━\n\n"
        f"📌 _Scenario: {scenario['context']}_\n\n"
        f"*Key vocab:* {vocab_list}\n\n"
        f"━━━━━━━━━━━━\n{prompt}\n\n"
        "_Your turn! Type your response_ ✍️\nType /exit to end roleplay."
    )
    markup = kb.Markup([[kb.Btn("❌ End Roleplay", callback_data="roleplay_end")]])
    if update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    else:
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)

async def cmd_correct(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")

    if not ctx.args:
        await update.message.reply_text(
            "Usage: `/correct <sentence>`\nExample: `/correct I goes to school yesterday`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    sentence = " ".join(ctx.args)
    result   = utils.grammar_check(sentence)
    await update.message.reply_text(result + FOOTER, parse_mode=ParseMode.MARKDOWN)

# ─────────────────────────────────────────
#  QUIZ ENGINE
# ─────────────────────────────────────────
async def cmd_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)
    lang   = user_d["lang"]
    level  = user_d["cefr_level"]

    # Build quiz from lesson data + vocab
    from lessons_data import ALL_LESSONS
    questions = []
    lang_data = ALL_LESSONS.get(lang, {})
    level_data = lang_data.get(level, {})
    for lesson in level_data.values():
        questions.extend(lesson.get("quiz", []))

    if not questions:
        # Fallback to English
        for lesson in ALL_LESSONS.get("english", {}).get("A1", {}).values():
            questions.extend(lesson.get("quiz", []))

    random.shuffle(questions)
    questions = questions[:8]

    if not questions:
        await update.message.reply_text("❌ No quiz questions available yet. Complete some lessons first!", parse_mode=ParseMode.MARKDOWN)
        return

    sid = db.start_quiz_session(u.id, questions, "quiz")
    db.set_state(u.id, "quiz", {"sid": sid, "questions": questions, "index": 0, "score": 0, "answers": []})
    await _send_quiz_question(update, questions[0], sid, 0)

async def _send_quiz_question(update: Update, question: dict, sid: int, index: int):
    text = f"🧪 *Question {index + 1}*\n━━━━━━━━━━━━━━━━\n\n{question['q']}"
    markup = kb.quiz_options(question["opts"], sid, index)
    if update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    else:
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)

async def cmd_challenge(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)

    questions = []
    for lang_data in ALL_LESSONS.values():
        for level_data in lang_data.values():
            for lesson in level_data.values():
                questions.extend(lesson.get("quiz", []))

    random.shuffle(questions)
    questions = questions[:10]

    now = datetime.now().isoformat()
    sid = db.start_quiz_session(u.id, questions, "challenge")
    db.set_state(u.id, "quiz", {"sid": sid, "questions": questions, "index": 0,
                                "score": 0, "answers": [], "mode": "challenge",
                                "start_time": now})

    await update.message.reply_text(
        "⚡ *TIMED CHALLENGE MODE!*\n━━━━━━━━━━━━━━━━\n\n"
        "⏱ 10 questions · Answer as fast as you can!\n"
        "Speed bonus XP available! 🚀\n\n"
        "Ready? Here comes Question 1...",
        parse_mode=ParseMode.MARKDOWN
    )
    await _send_quiz_question(update, questions[0], sid, 0)

async def cmd_exam(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)
    lang   = user_d["lang"]

    test_questions = LEVEL_TEST.get(lang, LEVEL_TEST["english"])
    sid = db.start_quiz_session(u.id, test_questions, "exam")
    db.set_state(u.id, "quiz", {"sid": sid, "questions": test_questions,
                                "index": 0, "score": 0, "answers": [], "mode": "exam"})

    await update.message.reply_text(
        f"📝 *LEVEL TEST — {lang.capitalize()}*\n━━━━━━━━━━━━━━━━\n\n"
        f"*{len(test_questions)} questions* to determine your CEFR level.\n"
        "Answer carefully. Good luck! 🍀",
        parse_mode=ParseMode.MARKDOWN
    )
    await _send_quiz_question(update, test_questions[0], sid, 0)

async def cmd_tops(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    leaders = db.get_leaderboard(10)
    lines   = ["🏆 *GLOBAL LEADERBOARD*\n━━━━━━━━━━━━━━━━━━━━"]
    medals  = ["🥇", "🥈", "🥉"] + ["🔸"] * 10

    for i, row in enumerate(leaders):
        name = (row.get("full_name") or "Anonymous")[:15]
        lines.append(f"{medals[i]} *{i+1}.* {name} — ⭐ {row['xp']} XP  🔥 {row['streak']}d")

    lines.append(FOOTER)
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)

# ─────────────────────────────────────────
#  PROGRESS
# ─────────────────────────────────────────
async def cmd_progress(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)

    xp      = user_d["xp"]
    lv_name, _, xp_next = get_level(xp)
    total   = user_d.get("total_questions", 0)
    correct = user_d.get("total_correct", 0)
    acc     = f"{int(correct/total*100)}%" if total else "N/A"

    # Generate chart
    chart_buf = utils.generate_stats_chart([xp // 4, xp // 3, xp // 2, xp])
    await update.message.reply_photo(
        photo=InputFile(chart_buf, filename="progress.png"),
        caption=(
            f"📊 *Your Progress*\n━━━━━━━━━━━━━━━━\n"
            f"⭐ XP: *{xp}*  |  Level: *{lv_name}*\n"
            f"📚 Lessons: *{user_d['total_lessons']}*\n"
            f"✅ Accuracy: *{acc}*\n"
            f"🔥 Streak: *{user_d['streak']} days*"
        ),
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_streak(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)
    streak = user_d["streak"]

    fire = "🔥" * min(streak, 10)
    msg  = (
        f"🔥 *Daily Streak: {streak} days*\n━━━━━━━━━━━━━━━━\n\n"
        f"{fire}\n\n"
    )
    if streak >= 7  and db.award_badge(u.id, "week_streak"):
        msg += "🏅 *NEW BADGE: Week Warrior!*\n"
    if streak >= 30 and db.award_badge(u.id, "month_streak"):
        msg += "🏅 *NEW BADGE: Moon Walker!*\n"

    if streak == 0:
        msg += "Start your streak by completing a lesson today! 🌱"
    elif streak < 7:
        msg += f"Keep going! {7-streak} more days to earn the *Week Warrior* badge!"
    else:
        msg += "Amazing consistency! You're a language learning machine! 💪"

    await update.message.reply_text(msg + FOOTER, parse_mode=ParseMode.MARKDOWN)

async def cmd_badges(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    earned = db.get_user_badges(u.id)

    lines = ["🏅 *Your Badges*\n━━━━━━━━━━━━━━━━\n"]
    for badge_id, (icon, name, desc) in BADGES.items():
        status = icon if badge_id in earned else "🔒"
        lines.append(f"{status} *{name}*\n   _{desc}_")

    lines.append(FOOTER)
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)

async def cmd_goal(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)

    if ctx.args and ctx.args[0].isdigit():
        mins = int(ctx.args[0])
        db.update_user(u.id, daily_goal=mins)
        await update.message.reply_text(
            f"🎯 *Daily goal set to {mins} minutes!*\nI'll remind you if you haven't studied today. 📱",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    await update.message.reply_text(
        f"🎯 *Daily Learning Goal*\nCurrent: *{user_d['daily_goal']} minutes/day*\n\nChoose a new goal:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb.goal_picker()
    )

# ─────────────────────────────────────────
#  SOCIAL COMMANDS
# ─────────────────────────────────────────
async def cmd_studygroup(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    groups = db.list_groups()

    if ctx.args:
        # Create a group
        name   = " ".join(ctx.args)
        user_d = db.get_user(u.id)
        gid    = db.create_group(name, u.id, user_d["lang"])
        groups_count = len(db.get_user_groups(u.id))
        if groups_count >= 5:
            db.award_badge(u.id, "social_star")
        await update.message.reply_text(
            f"✅ *Study group created!*\nGroup: *{name}* (ID: {gid})\n\n"
            f"Share ID `{gid}` with friends to join!\nUse `/studygroup join {gid}` to join.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if not groups:
        text = "👥 *No study groups yet!*\n\nCreate one: `/studygroup My Group Name`"
    else:
        lines = ["👥 *Active Study Groups*\n━━━━━━━━━━━━━━"]
        for g in groups[:10]:
            lines.append(f"• *{g['name']}* [{g['lang']}] — {g.get('member_count', 0)} members  `ID:{g['id']}`")
        lines.append("\n_Join: `/studygroup join <ID>`_")
        text = "\n".join(lines)

    await update.message.reply_text(text + FOOTER, parse_mode=ParseMode.MARKDOWN)

async def cmd_duel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")

    await update.message.reply_text(
        "⚔️ *Quiz Duel Mode*\n━━━━━━━━━━━━━━━━\n\n"
        "Challenge another user to a quiz battle!\n\n"
        "Usage: `/duel @username`\n\n"
        "_Both players answer the same questions. Highest score wins!_ 🏆",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_share(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u      = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")
    user_d = db.get_user(u.id)
    badges = db.get_user_badges(u.id)

    await update.message.reply_text("🎨 Generating your progress card...")
    try:
        card_buf = utils.generate_progress_card(user_d, badges)
        await update.message.reply_photo(
            photo=InputFile(card_buf, filename="progress_card.png"),
            caption=(
                f"🌍 *My Language Learning Journey*\n"
                f"Level: {user_d['cefr_level']} | XP: {user_d['xp']} | Streak: {user_d['streak']}d\n"
                f"_via SUPER LEARNING BOT — Create by PINLON-YOUTH_"
            )
        )
        db.add_xp(u.id, XP_RULES["share_card"])
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating card: {e}")

# ─────────────────────────────────────────
#  UTILITY COMMANDS
# ─────────────────────────────────────────
async def cmd_translate(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")

    if not ctx.args:
        await update.message.reply_text("Usage: `/translate <text>`\nExample: `/translate Hello how are you`", parse_mode=ParseMode.MARKDOWN)
        return

    text   = " ".join(ctx.args)
    user_d = db.get_user(u.id)
    target = SUPPORTED_LANGS.get(user_d["lang"], {}).get("code", "en")

    result = utils.translate_text(text, target)
    await update.message.reply_text(
        f"🌐 *Translation*\n━━━━━━━━━━━━━━\n\n"
        f"📤 _{text}_\n\n"
        f"📥 *{result}*",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_report(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    _ensure_user(u.id, u.username or "", u.full_name or "User")

    if not ctx.args:
        await update.message.reply_text(
            "📨 *Send Feedback*\n\nUsage: `/report <your message>`\nExample: `/report I found a bug in the quiz`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    msg    = " ".join(ctx.args)
    # Forward to admins
    for admin_id in ADMIN_IDS:
        try:
            await ctx.bot.send_message(
                chat_id=admin_id,
                text=f"📨 *User Report*\nFrom: {u.full_name} (ID: {u.id})\n\n{msg}",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception:
            pass

    await update.message.reply_text(
        "✅ *Report sent to admins! Thank you for your feedback.* 🙏",
        parse_mode=ParseMode.MARKDOWN
    )

async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🌍 *SUPER LEARNING BOT — Help*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔰 *Getting Started*\n"
        "/start — Welcome & main menu\n"
        "/lang — Change learning language\n"
        "/profile — Your stats & badges\n\n"
        "📚 *Learning*\n"
        "/learn — Today's lesson\n"
        "/lesson \\<topic\\> — Specific lesson\n"
        "/path — Learning roadmap\n"
        "/review — Spaced repetition review\n\n"
        "🔤 *Vocabulary*\n"
        "/vocab — Daily words\n"
        "/deck — Your saved words\n"
        "/save \\<word\\> — Save a word\n"
        "/flash — Flashcard mode\n\n"
        "🎧 *Pronunciation*\n"
        "/say \\<text\\> — Hear pronunciation\n"
        "/listen — Listening exercise\n"
        "/repeat — Shadowing guide\n\n"
        "💬 *AI Tutor*\n"
        "/tutor — Conversation practice\n"
        "/roleplay \\<scenario\\> — Roleplay mode\n"
        "/correct \\<sentence\\> — Grammar check\n\n"
        "🧪 *Quizzes*\n"
        "/quiz — Random quiz\n"
        "/challenge — Timed challenge\n"
        "/exam — Level test\n"
        "/tops — Leaderboard\n\n"
        "📊 *Progress*\n"
        "/progress — Stats chart\n"
        "/streak — Daily streak\n"
        "/badges — Your achievements\n"
        "/goal — Set daily goal\n\n"
        "🤝 *Social*\n"
        "/studygroup — Study groups\n"
        "/duel — Quiz battle\n"
        "/share — Share progress card\n\n"
        "📨 *Utilities*\n"
        "/translate \\<text\\> — Quick translation\n"
        "/report \\<msg\\> — Send feedback\n"
        + FOOTER
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb.main_menu())
