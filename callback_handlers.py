"""
SUPER LEARNING BOT — Callback Query & Message Handlers
=======================================================
Handles all InlineKeyboard callbacks and free-text messages
(tutor mode, roleplay, quiz answers, etc.)
"""
import json
import random
from datetime import datetime

from telegram import Update, InputFile
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

import database as db
import keyboards as kb
import utils
from config import (FOOTER, MAIN_MENU_TEXT, SUPPORTED_LANGS, XP_RULES,
                    BADGES, get_level, resolve_lang)
from lessons_data import (get_lesson, ROLEPLAY_SCENARIOS, ALL_LESSONS,
                          determine_level, LEVEL_TEST, get_daily_lesson)
from user_handlers import _send_quiz_question, _start_roleplay, cmd_learn

# ─────────────────────────────────────────
#  CALLBACK ROUTER
# ─────────────────────────────────────────
async def handle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q    = update.callback_query
    data = q.data
    uid  = q.from_user.id
    await q.answer()

    # ── Main menu ──────────────────────────────
    if data == "menu_main":
        await q.edit_message_text(MAIN_MENU_TEXT + FOOTER, parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=kb.main_menu())

    elif data == "menu_learn":
        await q.edit_message_text(
            "📚 *Learning Hub*\nChoose how to learn today:",
            parse_mode=ParseMode.MARKDOWN, reply_markup=kb.learn_menu()
        )

    elif data == "menu_review":
        from user_handlers import cmd_review
        await cmd_review(update, ctx)

    elif data == "menu_tutor":
        await q.edit_message_text(
            "💬 *AI Tutor*\nPractice your language skills:",
            parse_mode=ParseMode.MARKDOWN, reply_markup=kb.tutor_menu()
        )

    elif data == "menu_progress":
        from user_handlers import cmd_progress
        await cmd_progress(update, ctx)

    elif data == "menu_vocab":
        await q.edit_message_text("🔤 *Vocabulary*", parse_mode=ParseMode.MARKDOWN, reply_markup=kb.vocab_menu())

    elif data == "menu_quiz":
        await q.edit_message_text("🧪 *Quiz Engine*", parse_mode=ParseMode.MARKDOWN, reply_markup=kb.quiz_menu())

    elif data == "menu_social":
        await q.edit_message_text("🤝 *Social Features*", parse_mode=ParseMode.MARKDOWN, reply_markup=kb.social_menu())

    elif data == "menu_settings":
        user_d = db.get_user(uid) or {}
        lang   = user_d.get("lang", "english")
        level  = user_d.get("cefr_level", "A1")
        text   = (
            f"⚙️ *Settings*\n━━━━━━━━━━━━━━━━\n"
            f"🌍 Language: *{SUPPORTED_LANGS.get(lang, {}).get('name', lang)}*\n"
            f"📊 Level: *{level}*\n"
            f"🎯 Daily Goal: *{user_d.get('daily_goal', 15)} min*"
        )
        await q.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb.settings_menu())

    # ── Language selection ─────────────────────
    elif data.startswith("setlang:"):
        lang_key = data.split(":", 1)[1]
        if lang_key in SUPPORTED_LANGS:
            db.update_user(uid, lang=lang_key)
            info = SUPPORTED_LANGS[lang_key]
            await q.edit_message_text(
                f"✅ Learning language set to *{info['name']}*!\n\nUse /learn to start! 🚀",
                parse_mode=ParseMode.MARKDOWN, reply_markup=kb.main_menu()
            )

    elif data.startswith("advlevel:"):
        level_key = data.split(":", 1)[1]
        db.update_user(uid, cefr_level=level_key)
        await q.edit_message_text(
            f"✅ Level advanced to *{level_key}*!\n\nUse /learn to begin your new level lessons! 🌟",
            parse_mode=ParseMode.MARKDOWN, reply_markup=kb.main_menu()
        )

    # ── Learn actions ──────────────────────────
    elif data == "learn_daily":
        await cmd_learn(update, ctx)

    elif data == "learn_path":
        from user_handlers import cmd_path
        await cmd_path(update, ctx)

    elif data == "learn_listen":
        from user_handlers import cmd_listen
        await cmd_listen(update, ctx)

    elif data == "learn_review":
        from user_handlers import cmd_review
        await cmd_review(update, ctx)

    # ── Lesson quiz start ──────────────────────
    elif data.startswith("lesson_quiz:"):
        lesson_key = data.split(":", 1)[1]
        user_d     = db.get_user(uid)
        lesson     = get_lesson(user_d["lang"], user_d["cefr_level"], lesson_key)
        if not lesson:
            await q.edit_message_text("❌ Lesson not found.", parse_mode=ParseMode.MARKDOWN)
            return

        questions = lesson.get("quiz", [])
        if not questions:
            await q.edit_message_text("No quiz questions for this lesson yet!", parse_mode=ParseMode.MARKDOWN)
            return

        sid = db.start_quiz_session(uid, questions, "lesson")
        db.set_state(uid, "quiz", {"sid": sid, "questions": questions, "index": 0,
                                   "score": 0, "answers": [], "lesson_key": lesson_key,
                                   "lang": user_d["lang"], "level": user_d["cefr_level"]})
        await _send_quiz_question(update, questions[0], sid, 0)

    elif data == "lesson_skip":
        db.clear_state(uid)
        await q.edit_message_text("⏭️ Lesson skipped.\n\nUse /learn for your next lesson!", parse_mode=ParseMode.MARKDOWN)

    # ── Quiz answer ────────────────────────────
    elif data.startswith("quiz:"):
        parts   = data.split(":")
        sid     = int(parts[1])
        q_index = int(parts[2])
        chosen  = int(parts[3])

        state, state_data = db.get_state(uid)
        if state != "quiz":
            await q.edit_message_text("⚠️ Quiz session expired. Use /quiz to start a new one.")
            return

        questions = state_data.get("questions", [])
        if q_index >= len(questions):
            return

        question = questions[q_index]
        correct  = question["ans"]
        is_right = chosen == correct

        if is_right:
            state_data["score"] = state_data.get("score", 0) + 1
            db.add_xp(uid, XP_RULES["quiz_correct"])
            feedback = f"✅ *Correct!* +{XP_RULES['quiz_correct']} XP\n_{question['opts'][correct]}_"
        else:
            feedback = f"❌ *Wrong!*\nCorrect answer: *{question['opts'][correct]}*"

        state_data.setdefault("answers", []).append({"q": q_index, "chosen": chosen, "correct": is_right})

        next_index = q_index + 1
        if next_index < len(questions):
            state_data["index"] = next_index
            db.set_state(uid, "quiz", state_data)
            await q.edit_message_text(
                f"{feedback}\n\n_Loading next question..._",
                parse_mode=ParseMode.MARKDOWN
            )
            await _send_quiz_question(update, questions[next_index], sid, next_index)
        else:
            # Quiz finished
            score = state_data["score"]
            total = len(questions)
            db.update_quiz_session(sid, score, total, state_data.get("answers", []))
            db.clear_state(uid)

            # Check for completion XP
            mode = state_data.get("mode", "quiz")
            xp_bonus = 0
            if mode == "exam":
                new_level = determine_level(score, total)
                db.update_user(uid, cefr_level=new_level)
                level_msg = f"\n\n🎓 *Your CEFR Level: {new_level}*"
            else:
                level_msg = ""

            if score == total:
                db.award_badge(uid, "quiz_ace")
                xp_bonus = XP_RULES["lesson_complete"]
                db.add_xp(uid, xp_bonus)

            perc   = int(score / total * 100)
            rating = "🌟 Excellent!" if perc >= 80 else ("👍 Good job!" if perc >= 60 else "📚 Keep practicing!")

            # Mark lesson complete if lesson quiz
            lesson_key = state_data.get("lesson_key")
            if lesson_key:
                lang  = state_data.get("lang", "english")
                level = state_data.get("level", "A1")
                db.mark_lesson_done(uid, lesson_key, lang, score)
                db.award_badge(uid, "first_lesson")
                db.add_xp(uid, XP_RULES["lesson_complete"])

            await q.edit_message_text(
                f"🎉 *Quiz Complete!*\n━━━━━━━━━━━━━━━━━━\n\n"
                f"Score: *{score}/{total}* ({perc}%) {rating}\n"
                + (f"Bonus XP: +{xp_bonus} ⭐" if xp_bonus else "")
                + level_msg + FOOTER,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=kb.main_menu()
            )

    # ── Listening exercise answer ──────────────
    elif data.startswith("listen:"):
        parts   = data.split(":")
        correct = int(parts[1])
        chosen  = int(parts[2])
        if chosen == correct:
            await q.edit_message_text("✅ *Correct!* Great listening! 🎧\n+10 XP", parse_mode=ParseMode.MARKDOWN)
            db.add_xp(uid, 10)
        else:
            await q.edit_message_text(f"❌ *Not quite!*\nCorrect answer was option {correct + 1}.\nKeep practicing! 🎧", parse_mode=ParseMode.MARKDOWN)

    # ── Vocab actions ──────────────────────────
    elif data == "vocab_daily":
        from user_handlers import cmd_vocab
        await cmd_vocab(update, ctx)

    elif data == "vocab_deck":
        from user_handlers import cmd_deck
        await cmd_deck(update, ctx)

    elif data == "vocab_flash":
        from user_handlers import cmd_flash
        await cmd_flash(update, ctx)

    elif data == "vocab_review":
        from user_handlers import cmd_review
        await cmd_review(update, ctx)

    # ── Flashcard rating ───────────────────────
    elif data.startswith("fc:"):
        parts    = data.split(":")
        vocab_id = int(parts[1])
        quality  = int(parts[2])
        db.update_vocab_sm2(vocab_id, quality)
        db.add_xp(uid, XP_RULES["flashcard_session"] // 3)

        user_d = db.get_user(uid)
        deck   = db.get_vocab_deck(uid, user_d["lang"])
        state, state_data = db.get_state(uid)
        idx    = state_data.get("index", 0) + 1

        if idx < len(deck):
            card = deck[idx]
            db.set_state(uid, "flashcard", {"deck": [d["id"] for d in deck], "index": idx})
            text = (
                f"🃏 *Flashcard {idx+1}/{len(deck)}*\n━━━━━━━━━━━━━━━━\n\n"
                f"*Word:* {card['word']}\n\n"
                f"||*Meaning:* {card['meaning']}||\n"
                "_Tap to reveal · Rate your memory!_"
            )
            await q.edit_message_text(text, parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=kb.flashcard_rating(card["id"]))
        else:
            db.clear_state(uid)
            db.add_xp(uid, XP_RULES["flashcard_session"])
            await q.edit_message_text(
                f"🎉 *Flashcard session complete!*\n\n"
                f"Reviewed *{len(deck)}* words. +{XP_RULES['flashcard_session']} XP 🌟",
                parse_mode=ParseMode.MARKDOWN, reply_markup=kb.main_menu()
            )

    # ── Quiz actions ───────────────────────────
    elif data == "quiz_random":
        from user_handlers import cmd_quiz
        await cmd_quiz(update, ctx)

    elif data == "quiz_challenge":
        from user_handlers import cmd_challenge
        await cmd_challenge(update, ctx)

    elif data == "quiz_exam":
        from user_handlers import cmd_exam
        await cmd_exam(update, ctx)

    elif data == "quiz_tops":
        from user_handlers import cmd_tops
        await cmd_tops(update, ctx)

    # ── Social actions ─────────────────────────
    elif data == "social_groups":
        from user_handlers import cmd_studygroup
        await cmd_studygroup(update, ctx)

    elif data == "social_duel":
        from user_handlers import cmd_duel
        await cmd_duel(update, ctx)

    elif data == "social_share":
        from user_handlers import cmd_share
        await cmd_share(update, ctx)

    # ── Settings actions ───────────────────────
    elif data == "settings_lang":
        await q.edit_message_text("🌍 *Choose your learning language:*",
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=kb.lang_picker())

    elif data == "settings_goal":
        user_d = db.get_user(uid) or {}
        await q.edit_message_text(
            f"🎯 *Set Daily Goal*\nCurrent: *{user_d.get('daily_goal', 15)} min/day*",
            parse_mode=ParseMode.MARKDOWN, reply_markup=kb.goal_picker()
        )

    elif data == "settings_profile":
        from user_handlers import cmd_profile
        await cmd_profile(update, ctx)

    elif data.startswith("goal:"):
        mins = int(data.split(":", 1)[1])
        db.update_user(uid, daily_goal=mins)
        await q.edit_message_text(
            f"🎯 *Daily goal set: {mins} minutes/day!*\nI'll remind you to study today! 📱",
            parse_mode=ParseMode.MARKDOWN, reply_markup=kb.main_menu()
        )

    # ── Tutor actions ──────────────────────────
    elif data == "tutor_chat":
        db.set_state(uid, "tutor", {"mode": "chat"})
        await q.edit_message_text(
            "💬 *Free Chat Mode*\n━━━━━━━━━━━━━━━━\n\n"
            "Chat with me to practice your language!\n"
            "Just type anything — I'll respond and help you improve.\n\n"
            "Type /exit to stop.",
            parse_mode=ParseMode.MARKDOWN
        )

    elif data == "tutor_grammar":
        db.set_state(uid, "tutor", {"mode": "grammar"})
        await q.edit_message_text(
            "✏️ *Grammar Check Mode*\n━━━━━━━━━━━━━━━━\n\n"
            "Type a sentence and I'll check it for you!\n"
            "Or use `/correct <sentence>` directly.\n\n"
            "Type /exit to stop.",
            parse_mode=ParseMode.MARKDOWN
        )

    elif data == "tutor_roleplay":
        await q.edit_message_text("🎭 *Choose a Roleplay Scenario:*",
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=kb.roleplay_picker())

    elif data == "tutor_shadow":
        await q.edit_message_text(
            "🔁 *Shadowing Practice*\n━━━━━━━━━━━━━━━━\n\n"
            "1. Use `/say <text>` to hear pronunciation\n"
            "2. Repeat what you hear out loud\n"
            "3. Practice until it sounds natural!\n\n"
            "Try: `/say Nice to meet you, my name is John`",
            parse_mode=ParseMode.MARKDOWN, reply_markup=kb.back_btn("menu_tutor")
        )

    elif data.startswith("roleplay:"):
        scenario_key = data.split(":", 1)[1]
        await _start_roleplay(update, uid, scenario_key)

    elif data == "roleplay_end":
        db.clear_state(uid)
        await q.edit_message_text(
            "🎭 Roleplay ended. Great practice! 🌟\n\n"
            "Use /roleplay to start a new scenario.",
            parse_mode=ParseMode.MARKDOWN, reply_markup=kb.main_menu()
        )

    # ── Duel actions ───────────────────────────
    elif data.startswith("duel_accept:"):
        duel_id = int(data.split(":", 1)[1])
        await q.edit_message_text(
            f"⚔️ *Duel #{duel_id} Accepted!*\nGet ready — the quiz is starting!",
            parse_mode=ParseMode.MARKDOWN
        )

    elif data.startswith("duel_decline:"):
        duel_id = int(data.split(":", 1)[1])
        await q.edit_message_text(f"❌ Duel #{duel_id} declined.", parse_mode=ParseMode.MARKDOWN)

# ─────────────────────────────────────────
#  FREE-TEXT MESSAGE HANDLER
# ─────────────────────────────────────────
async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u    = update.effective_user
    text = update.message.text.strip()

    # Ensure user exists
    db.upsert_user(u.id, u.username or "", u.full_name or "User")
    state, state_data = db.get_state(u.id)

    # ── /exit shortcut ─────────────────────────
    if text.lower() in ["/exit", "exit", "quit", "stop"]:
        db.clear_state(u.id)
        await update.message.reply_text(
            "👋 Exited current mode.\n\nUse /start to return to the main menu.",
            reply_markup=kb.main_menu()
        )
        return

    # ── Roleplay mode ──────────────────────────
    if state == "roleplay":
        scenario_key = state_data.get("key")
        step         = state_data.get("step", 0)
        scenario     = ROLEPLAY_SCENARIOS.get(scenario_key, {})
        prompts      = scenario.get("prompts", [])

        next_step = step + 1
        if next_step < len(prompts):
            state_data["step"] = next_step
            db.set_state(u.id, "roleplay", state_data)

            feedback = _roleplay_feedback(text, scenario_key)
            bot_line = prompts[next_step]
            markup   = kb.Markup([[kb.Btn("❌ End Roleplay", callback_data="roleplay_end")]])
            await update.message.reply_text(
                f"{feedback}\n\n━━━━━━━━━━━━\n{bot_line}\n\n_Your turn!_ ✍️",
                parse_mode=ParseMode.MARKDOWN, reply_markup=markup
            )
        else:
            db.clear_state(u.id)
            db.add_xp(u.id, XP_RULES["lesson_complete"])
            await update.message.reply_text(
                f"🎉 *Roleplay Complete!* +{XP_RULES['lesson_complete']} XP\n\n"
                "Great conversation practice! Keep it up! 💪\n\n"
                "Use /roleplay for another scenario.",
                parse_mode=ParseMode.MARKDOWN, reply_markup=kb.main_menu()
            )
        return

    # ── Tutor chat mode ────────────────────────
    if state == "tutor":
        mode = state_data.get("mode", "chat")

        if mode == "grammar":
            result = utils.grammar_check(text)
            await update.message.reply_text(result + FOOTER, parse_mode=ParseMode.MARKDOWN)
            return

        # Chat mode — rule-based conversational tutor
        response = _tutor_response(text)
        await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        return

    # ── Default — show main menu ───────────────
    await update.message.reply_text(
        "💬 Use the menu below or type a command!\n\nType /help to see all commands.",
        reply_markup=kb.main_menu()
    )

# ─────────────────────────────────────────
#  TUTOR RESPONSE ENGINE (rule-based)
# ─────────────────────────────────────────
def _tutor_response(text: str) -> str:
    text_lower = text.lower().strip()

    # Greetings
    if any(w in text_lower for w in ["hello", "hi", "hey", "good morning", "good evening"]):
        return random.choice([
            "👋 Hello! How are you today? Try to answer in a full sentence! 😊",
            "Hi there! Great to see you! What would you like to practice today?",
            "Hey! 😄 Try responding: *'I'm doing great, thank you!'* — how does that sound?",
        ])

    # Questions about self
    if "my name" in text_lower or "i am" in text_lower or "i'm" in text_lower:
        return (
            "👍 Great introduction!\n\n"
            "*Tip:* You can expand it:\n"
            "_\"My name is [name]. I am from [country]. I am learning [language].\"_\n\n"
            "Try writing that! 📝"
        )

    # How are you
    if "how are you" in text_lower or "how do you do" in text_lower:
        return (
            "I'm great, thanks for asking! 😊\n\n"
            "Now your turn — how are *you* doing?\n"
            "_Try: 'I am doing well, thank you!'_"
        )

    # What/Where/When questions
    if text_lower.startswith("what") or text_lower.startswith("where") or text_lower.startswith("when"):
        return (
            "🤔 Good question! I see you're practicing *question formation*.\n\n"
            "💡 *Tip:* Questions in English use auxiliary verbs:\n"
            "• What *is* your name?\n"
            "• Where *do* you live?\n"
            "• When *did* you start learning?\n\n"
            "Keep practicing! You're doing well! 💪"
        )

    # Grammar mistakes detection
    result = utils.grammar_check(text)
    if "Corrected" in result:
        return f"📝 *Tutor feedback:*\n{result}\n\n_Keep writing! Practice makes perfect!_ 🌟"

    # Default encouraging response
    responses = [
        f"👍 Good sentence! Keep it up!\n\n💡 *Try expanding:* _{text}_ → add more details!",
        f"✅ Nice try! Here's a tip: try using adjectives to make it more interesting.\n\n_{text}_",
        f"🌟 Good effort! Now try using this in a full paragraph.\n\n_'{text}'_ — can you continue the story?",
        "📝 I see what you're doing! Keep writing — practice is the key to fluency! 💪",
    ]
    return random.choice(responses)

# ─────────────────────────────────────────
#  ROLEPLAY FEEDBACK
# ─────────────────────────────────────────
def _roleplay_feedback(text: str, scenario: str) -> str:
    check = utils.grammar_check(text)
    if "Corrected" in check:
        return f"💬 *Your response noted!*\n{check}"
    else:
        return f"💬 *Your response:* _{text}_\n✅ Looks good! Keep going!"
