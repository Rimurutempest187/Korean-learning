# -*- coding: utf-8 -*-
"""
SUPER LEARNING BOT — Utility Modules
=====================================
Progress card generator, TTS, translation, charts.
All FREE — no paid API keys required.
"""

import os
import io
import random
import hashlib
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

# ─────────────────────────────────────────
#  PROGRESS CARD GENERATOR
# ─────────────────────────────────────────
def generate_progress_card(user: dict, badges: list) -> io.BytesIO:
    """Generate a beautiful progress card image."""
    W, H = 700, 420
    img  = Image.new("RGB", (W, H), color=(18, 18, 30))
    draw = ImageDraw.Draw(img)

    # Gradient overlay
    for y in range(H):
        ratio = y / H
        r = int(18  + (40  - 18)  * ratio)
        g = int(18  + (20  - 18)  * ratio)
        b = int(30  + (60  - 30)  * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Accent bar
    draw.rectangle([0, 0, W, 6], fill=(99, 102, 241))

    # Try to load a font; fall back to default
    try:
        font_big   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_med   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
        font_tiny  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except Exception:
        font_big = font_med = font_small = font_tiny = ImageFont.load_default()

    # Avatar circle placeholder
    av_x, av_y, av_r = 60, 70, 45
    draw.ellipse([av_x - av_r, av_y - av_r, av_x + av_r, av_y + av_r], fill=(99, 102, 241))
    initials = (user.get("full_name") or "U")[:2].upper()
    draw.text((av_x - 15, av_y - 14), initials, font=font_med, fill=(255, 255, 255))

    # Name & level
    name  = (user.get("full_name") or "Learner")[:20]
    level = user.get("cefr_level", "A1")
    xp    = user.get("xp", 0)

    from config import get_level
    lv_name, _, xp_next = get_level(xp)

    draw.text((125, 45),  name,     font=font_big,   fill=(255, 255, 255))
    draw.text((125, 88),  lv_name,  font=font_small, fill=(167, 139, 250))
    draw.text((125, 112), f"CEFR: {level}", font=font_tiny, fill=(156, 163, 175))

    # XP Bar
    bar_x, bar_y, bar_w, bar_h = 40, 165, 620, 22
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=11, fill=(40, 40, 60))
    if xp_next > 0:
        fill_w = int(bar_w * min(xp / xp_next, 1.0))
    else:
        fill_w = bar_w
    draw.rounded_rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + bar_h], radius=11, fill=(99, 102, 241))
    xp_text = f"XP: {xp}" + (f" / {xp_next}" if xp_next > 0 else " (MAX)")
    draw.text((bar_x + 10, bar_y + 3), xp_text, font=font_tiny, fill=(220, 220, 255))

    # Stats row
    stats = [
        ("🎯", "Streak",   f"{user.get('streak', 0)} days"),
        ("📚", "Lessons",  str(user.get("total_lessons", 0))),
        ("✅", "Accuracy", _accuracy(user)),
        ("🌍", "Lang",      user.get("lang", "english").capitalize()),
    ]
    sx = 40
    for icon, label, val in stats:
        draw.rectangle([sx, 210, sx + 145, 300], fill=(28, 28, 45))
        draw.rectangle([sx, 210, sx + 145, 214], fill=(99, 102, 241))
        draw.text((sx + 10, 220), f"{icon} {label}", font=font_tiny,  fill=(156, 163, 175))
        draw.text((sx + 10, 243), val,                font=font_med,   fill=(255, 255, 255))
        sx += 160

    # Badges row
    draw.text((40, 315), "🏅 Badges:", font=font_small, fill=(167, 139, 250))
    from config import BADGES
    bx = 40
    for b in badges[:8]:
        info = BADGES.get(b)
        if info:
            draw.text((bx, 340), info[0], font=font_med, fill=(255, 255, 255))
            bx += 38

    if not badges:
        draw.text((130, 340), "No badges yet — keep learning! 🚀", font=font_small, fill=(107, 114, 128))

    # Footer
    draw.text((40, 390), "🌍 SUPER LEARNING BOT  •  Create by : PINLON-YOUTH", font=font_tiny, fill=(75, 85, 99))
    draw.line([(0, 385), (W, 385)], fill=(40, 40, 60))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def _accuracy(user: dict) -> str:
    total = user.get("total_questions", 0)
    if total == 0:
        return "N/A"
    acc = int(user.get("total_correct", 0) / total * 100)
    return f"{acc}%"

# ─────────────────────────────────────────
#  STATS CHART
# ─────────────────────────────────────────
def generate_stats_chart(xp_history: list) -> io.BytesIO:
    """Generate XP over time bar chart."""
    fig, ax = plt.subplots(figsize=(8, 4), facecolor="#12121e")
    ax.set_facecolor("#1a1a2e")

    if not xp_history:
        xp_history = [0]

    days   = [f"Day {i+1}" for i in range(len(xp_history))]
    colors = ["#6366f1"] * len(xp_history)

    ax.bar(days, xp_history, color=colors, edgecolor="#4f46e5", linewidth=0.5)
    ax.set_title("📊 XP Progress", color="white", fontsize=14, pad=15)
    ax.set_xlabel("Sessions", color="#9ca3af", fontsize=10)
    ax.set_ylabel("XP Gained", color="#9ca3af", fontsize=10)
    ax.tick_params(colors="white", labelsize=8)
    ax.spines["bottom"].set_color("#374151")
    ax.spines["left"].set_color("#374151")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="PNG", dpi=120, facecolor="#12121e")
    plt.close()
    buf.seek(0)
    return buf

# ─────────────────────────────────────────
#  TTS (Text-to-Speech) — FREE via gTTS
# ─────────────────────────────────────────
def generate_tts(text: str, lang_code: str = "en", cache_dir: str = "audio_cache") -> str:
    """Generate TTS audio file. Returns file path."""
    try:
        from gtts import gTTS
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)

        # Cache by hash
        key  = hashlib.md5(f"{lang_code}:{text}".encode()).hexdigest()
        path = os.path.join(cache_dir, f"{key}.mp3")

        if not os.path.exists(path):
            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(path)

        return path
    except Exception as e:
        print(f"TTS error: {e}")
        return None

# ─────────────────────────────────────────
#  TRANSLATION — FREE via deep-translator
# ─────────────────────────────────────────
def translate_text(text: str, target: str = "en", source: str = "auto") -> str:
    """Translate text. Free, no API key needed."""
    try:
        from deep_translator import GoogleTranslator
        result = GoogleTranslator(source=source, target=target).translate(text)
        return result or text
    except Exception as e:
        return f"[Translation error: {e}]"

# ─────────────────────────────────────────
#  MOTIVATIONAL QUOTES
# ─────────────────────────────────────────
QUOTES = [
    "💬 'The limits of my language mean the limits of my world.' — Wittgenstein",
    "💬 'Learning another language is like becoming another person.' — Shiki",
    "💬 'One language sets you in a corridor for life. Two languages open every door.' — Searls",
    "💬 'To have another language is to possess a second soul.' — Charlemagne",
    "💬 'Language is the road map of a culture.' — Rita Mae Brown",
    "💬 'You can never understand one language until you understand at least two.' — Searls",
    "💬 'Every language is a world. Without translation, we would inhabit parishes bordering on silence.' — Steiner",
    "💬 'If you talk to a man in a language he understands, that goes to his head.' — Mandela",
    "💬 'The more languages you know, the more you are human.' — Masaryk",
]

def get_daily_quote() -> str:
    from datetime import date
    return QUOTES[date.today().day % len(QUOTES)]

# ─────────────────────────────────────────
#  RANDOM QUIZ GENERATOR
# ─────────────────────────────────────────
def build_vocab_quiz(word_list: list, count: int = 5) -> list:
    """Build a multiple-choice quiz from a vocabulary list."""
    if len(word_list) < 4:
        return []
    questions = []
    random.shuffle(word_list)
    for i, item in enumerate(word_list[:count]):
        distractors = [w["meaning"] for w in word_list if w["word"] != item["word"]]
        random.shuffle(distractors)
        opts = distractors[:3] + [item["meaning"]]
        random.shuffle(opts)
        ans  = opts.index(item["meaning"])
        questions.append({
            "q"   : f"What does '{item['word']}' mean?",
            "opts": opts,
            "ans" : ans,
            "word": item["word"],
        })
    return questions

def shuffle_quiz(questions: list) -> list:
    q = questions.copy()
    random.shuffle(q)
    return q[:10]

# ─────────────────────────────────────────
#  GRAMMAR CORRECTION
# ─────────────────────────────────────────
COMMON_ERRORS = [
    (r"\bi are\b", "I am", "Use 'am' with 'I'"),
    (r"\bhe are\b", "he is", "Use 'is' with 'he'"),
    (r"\bshe are\b", "she is", "Use 'is' with 'she'"),
    (r"\bthey is\b", "they are", "Use 'are' with 'they'"),
    (r"\bwe is\b", "we are", "Use 'are' with 'we'"),
    (r"\bdid not went\b", "did not go", "After 'did', use base form of verb"),
    (r"\bmore better\b", "better", "Don't use 'more' with comparative adjectives"),
]

def grammar_check(sentence: str) -> str:
    import re
    original = sentence
    feedback = []
    corrected = sentence

    for pattern, correction, tip in COMMON_ERRORS:
        if re.search(pattern, sentence, re.IGNORECASE):
            corrected = re.sub(pattern, correction, corrected, flags=re.IGNORECASE)
            if tip:
                feedback.append(f"📌 {tip}")

    result = f"📝 *Original:*\n_{original}_\n\n"
    if corrected.lower().strip() != original.lower().strip():
        result += f"✅ *Corrected:*\n_{corrected}_\n\n"
        if feedback:
            result += "💡 *Tips:*\n" + "\n".join(feedback)
    else:
        result += "✅ *No obvious errors found!*\n\n💡 Keep practicing! 🌟"

    return result

# ─────────────────────────────────────────
#  LISTENING EXERCISES
# ─────────────────────────────────────────
LISTENING_EXERCISES = [
    {
        "lang"  : "english",
        "text"  : "Good morning! My name is Sarah. I am a doctor. I work at City Hospital.",
        "question": "What is Sarah's job?",
        "opts"  : ["Teacher","Doctor","Engineer","Nurse"],
        "ans"   : 1,
    },
    {
        "lang"  : "english",
        "text"  : "The train to London departs at nine fifteen from platform three.",
        "question": "What platform does the train depart from?",
        "opts"  : ["Platform 1","Platform 2","Platform 3","Platform 4"],
        "ans"   : 2,
    }
]

def get_listening_exercise(lang: str) -> dict:
    exercises = [e for e in LISTENING_EXERCISES if e["lang"] == lang]
    if not exercises:
        exercises = LISTENING_EXERCISES
    return random.choice(exercises)
