# bot.py
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database file paths
DB_USERS = "data/users.json"
DB_LESSONS = "data/lessons.json"
DB_VOCAB = "data/vocab.json"
DB_QUIZ = "data/quiz.json"
DB_SETTINGS = "data/settings.json"
DB_TUTORS = "data/tutors.json"

# Admin IDs (comma-separated in .env)
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# ==================== Database Helper Functions ====================

def ensure_data_dir():
    """Create data directory if not exists"""
    os.makedirs("data", exist_ok=True)

def load_json(filepath: str, default=None) -> dict:
    """Load JSON file"""
    ensure_data_dir()
    if default is None:
        default = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def save_json(filepath: str, data: dict):
    """Save JSON file"""
    ensure_data_dir()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_data(user_id: int) -> dict:
    """Get user data"""
    users = load_json(DB_USERS, {})
    user_key = str(user_id)
    if user_key not in users:
        users[user_key] = {
            "user_id": user_id,
            "streak": 0,
            "last_active": "",
            "completed_lessons": [],
            "quiz_scores": [],
            "total_score": 0,
            "role": "user",
            "progress": {}
        }
        save_json(DB_USERS, users)
    return users[user_key]

def save_user_data(user_id: int, data: dict):
    """Save user data"""
    users = load_json(DB_USERS, {})
    users[str(user_id)] = data
    save_json(DB_USERS, users)

def update_streak(user_id: int):
    """Update user's daily streak"""
    user = get_user_data(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    
    if user["last_active"] == today:
        return user["streak"]
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    if user["last_active"] == yesterday:
        user["streak"] += 1
    else:
        user["streak"] = 1
    
    user["last_active"] = today
    save_user_data(user_id, user)
    return user["streak"]

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    if user_id in ADMIN_IDS:
        return True
    user = get_user_data(user_id)
    return user.get("role") in ["admin", "tutor"]

# ==================== User Commands ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    user_id = user.id
    
    # Initialize user
    get_user_data(user_id)
    
    welcome_msg = f"""
🇰🇷 <b>ကိုရီးယားဘာသာစကား သင်ကြားရေး Bot မှ ကြိုဆိုပါတယ်!</b>

မင်္ဂလာပါ {user.first_name}! 👋

<b>📚 အသုံးပြုနည်း:</b>

<b>သင်ယူရေး Commands:</b>
/lesson - သင်ခန်းစာများ ကြည့်ရန်
/vocab - နေ့စဉ် vocabulary
/flashcard - Flashcard လေ့ကျင့်ရန်
/quiz - Quiz ဖြေဆိုရန်
/practice - စကားပြောလေ့ကျင့်ရန်
/pronounce <text> - အသံထွက် နားထောင်ရန်
/translate <text> - ဘာသာပြန်ရန်

<b>တိုးတက်မှု Commands:</b>
/streak - နေ့စဉ်သင်ယူမှု streak
/progress - သင်၏တိုးတက်မှု

<b>အခြား Commands:</b>
/homework - Homework တင်ရန်
/report - အကြံပြုချက်ပို့ရန်

စတင်သင်ယူလိုက်ပါ! 🚀

<i>Create by: PINLON-YOUTH</i>
"""
    
    await update.message.reply_text(welcome_msg, parse_mode="HTML")

async def lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /lesson command"""
    args = context.args
    lessons = load_json(DB_LESSONS, {"lessons": []})
    
    if not args or args[0] == "list":
        if not lessons["lessons"]:
            await update.message.reply_text("📚 သင်ခန်းစာများ မရှိသေးပါ။")
            return
        
        msg = "<b>📚 ရရှိနိုင်သော သင်ခန်းစာများ:</b>\n\n"
        for lesson in lessons["lessons"]:
            msg += f"🔹 <code>{lesson['id']}</code> - {lesson['title']}\n"
        msg += f"\n<i>အသုံးပြုပုံ: /startlesson &lt;lesson_id&gt;</i>"
        
        await update.message.reply_text(msg, parse_mode="HTML")
    else:
        lesson_id = args[0]
        lesson_data = next((l for l in lessons["lessons"] if l["id"] == lesson_id), None)
        
        if lesson_data:
            msg = f"<b>📖 {lesson_data['title']}</b>\n\n{lesson_data.get('content', 'သင်ခန်းစာအကြောင်းအရာ မရှိသေးပါ။')}"
            await update.message.reply_text(msg, parse_mode="HTML")
        else:
            await update.message.reply_text(f"❌ သင်ခန်းစာ '{lesson_id}' မတွေ့ပါ။")

async def startlesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /startlesson command"""
    if not context.args:
        await update.message.reply_text("❌ အသုံးပြုပုံ: /startlesson <lesson_id>")
        return
    
    lesson_id = context.args[0]
    lessons = load_json(DB_LESSONS, {"lessons": []})
    lesson_data = next((l for l in lessons["lessons"] if l["id"] == lesson_id), None)
    
    if not lesson_data:
        await update.message.reply_text(f"❌ သင်ခန်းစာ '{lesson_id}' မတွေ့ပါ။")
        return
    
    user_id = update.effective_user.id
    user = get_user_data(user_id)
    
    msg = f"<b>🎓 သင်ခန်းစာ: {lesson_data['title']}</b>\n\n"
    msg += f"{lesson_data.get('content', '')}\n\n"
    
    if "audio" in lesson_data:
        msg += f"🔊 Audio: {lesson_data['audio']}\n"
    
    msg += f"\n✅ သင်ခန်းစာ စတင်ပြီးပါပြီ!"
    
    # Mark as completed
    if lesson_id not in user["completed_lessons"]:
        user["completed_lessons"].append(lesson_id)
        save_user_data(user_id, user)
    
    update_streak(user_id)
    
    await update.message.reply_text(msg, parse_mode="HTML")

async def vocab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /vocab command"""
    vocab_data = load_json(DB_VOCAB, {"words": []})
    
    if not vocab_data["words"]:
        await update.message.reply_text("📖 Vocabulary မရှိသေးပါ။")
        return
    
    args = context.args
    
    if args and args[0] == "today":
        # Show today's vocab
        today_words = [w for w in vocab_data["words"] if w.get("daily", False)]
        if not today_words:
            today_words = random.sample(vocab_data["words"], min(5, len(vocab_data["words"])))
    else:
        # Random vocab
        today_words = random.sample(vocab_data["words"], min(5, len(vocab_data["words"])))
    
    msg = "<b>📖 ယနေ့ Vocabulary:</b>\n\n"
    for i, word in enumerate(today_words, 1):
        msg += f"{i}. <b>{word['word']}</b>\n"
        msg += f"   အဓိပ္పာယ်: {word['meaning']}\n"
        if "example" in word:
            msg += f"   ဥပမာ: {word['example']}\n"
        msg += "\n"
    
    update_streak(update.effective_user.id)
    
    await update.message.reply_text(msg, parse_mode="HTML")

async def flashcard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /flashcard command"""
    vocab_data = load_json(DB_VOCAB, {"words": []})
    
    if not vocab_data["words"]:
        await update.message.reply_text("📖 Vocabulary မရှိသေးပါ။")
        return
    
    word = random.choice(vocab_data["words"])
    
    keyboard = [
        [InlineKeyboardButton("📖 အဓိပ္பာယ် ပြရန်", callback_data=f"flashcard_show_{word['word']}")],
        [InlineKeyboardButton("➡️ နောက်တစ်ခု", callback_data="flashcard_next")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    msg = f"<b>🎴 Flashcard:</b>\n\n<b>{word['word']}</b>"
    
    await update.message.reply_text(msg, parse_mode="HTML", reply_markup=reply_markup)

async def flashcard_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle flashcard button callbacks"""
    query = update.callback_query
    await query.answer()
    
    vocab_data = load_json(DB_VOCAB, {"words": []})
    
    if query.data.startswith("flashcard_show_"):
        word_text = query.data.replace("flashcard_show_", "")
        word = next((w for w in vocab_data["words"] if w["word"] == word_text), None)
        
        if word:
            msg = f"<b>🎴 Flashcard:</b>\n\n<b>{word['word']}</b>\n\n"
            msg += f"📖 အဓိပ္ပာယ်: {word['meaning']}\n"
            if "example" in word:
                msg += f"ဥပမာ: {word['example']}"
            
            keyboard = [[InlineKeyboardButton("➡️ နောက်တစ်ခု", callback_data="flashcard_next")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(msg, parse_mode="HTML", reply_markup=reply_markup)
    
    elif query.data == "flashcard_next":
        if vocab_data["words"]:
            word = random.choice(vocab_data["words"])
            keyboard = [
                [InlineKeyboardButton("📖 အဓိပ္ပာယ် ပြရန်", callback_data=f"flashcard_show_{word['word']}")],
                [InlineKeyboardButton("➡️ နောက်တစ်ခု", callback_data="flashcard_next")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            msg = f"<b>🎴 Flashcard:</b>\n\n<b>{word['word']}</b>"
            await query.edit_message_text(msg, parse_mode="HTML", reply_markup=reply_markup)

async def pronounce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pronounce command"""
    if not context.args:
        await update.message.reply_text("❌ အသုံးပြုပုံ: /pronounce <Korean text>")
        return
    
    text = " ".join(context.args)
    
    msg = f"🔊 <b>အသံထွက်:</b> {text}\n\n"
    msg += "⚠️ TTS feature လိုအပ်ပါတယ်။ Pronunciation guide:\n"
    msg += f"<code>{text}</code>\n\n"
    msg += "<i>Note: Real TTS integration လိုအပ်ပါတယ် (e.g., Google TTS API)</i>"
    
    await update.message.reply_text(msg, parse_mode="HTML")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /translate command"""
    if not context.args:
        await update.message.reply_text("❌ အသုံးပြုပုံ: /translate <text>")
        return
    
    text = " ".join(context.args)
    
    # Simple translation simulation (you'd integrate real translation API)
    translations = {
        "hello": "안녕하세요",
        "thank you": "감사합니다",
        "i love korean": "나는 한국어를 사랑해요",
        "goodbye": "안녕히 가세요"
    }
    
    result = translations.get(text.lower(), "")
    
    if result:
        msg = f"🌐 <b>ဘာသာပြန်:</b>\n\n{text} ➡️ {result}"
    else:
        msg = f"🌐 <b>ဘာသာပြန်:</b>\n\n⚠️ Translation API integration လိုအပ်ပါတယ်။\n\nရိုက်ထည့်ခဲ့သည်: {text}"
    
    await update.message.reply_text(msg, parse_mode="HTML")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /quiz command"""
    quiz_data = load_json(DB_QUIZ, {"quizzes": []})
    
    if not quiz_data["quizzes"]:
        await update.message.reply_text("❓ Quiz မရှိသေးပါ။")
        return
    
    question = random.choice(quiz_data["quizzes"])
    
    keyboard = [
        [InlineKeyboardButton(f"A. {question['A']}", callback_data=f"quiz_{question['id']}_A")],
        [InlineKeyboardButton(f"B. {question['B']}", callback_data=f"quiz_{question['id']}_B")],
        [InlineKeyboardButton(f"C. {question['C']}", callback_data=f"quiz_{question['id']}_C")],
        [InlineKeyboardButton(f"D. {question['D']}", callback_data=f"quiz_{question['id']}_D")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    msg = f"<b>❓ Quiz:</b>\n\n{question['question']}"
    
    await update.message.reply_text(msg, parse_mode="HTML", reply_markup=reply_markup)
    
    update_streak(update.effective_user.id)

async def quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quiz answer callbacks"""
    query = update.callback_query
    await query.answer()
    
    quiz_data = load_json(DB_QUIZ, {"quizzes": []})
    
    parts = query.data.split("_")
    quiz_id = parts[1]
    answer = parts[2]
    
    question = next((q for q in quiz_data["quizzes"] if q["id"] == quiz_id), None)
    
    if not question:
        await query.edit_message_text("❌ Quiz မတွေ့ပါ။")
        return
    
    user_id = query.from_user.id
    user = get_user_data(user_id)
    
    if answer == question["correct"]:
        result = "✅ မှန်ကန်ပါတယ်!"
        user["quiz_scores"].append(1)
        user["total_score"] += 1
    else:
        result = f"❌ မှားပါတယ်။ မှန်ကန်သောအဖြေ: {question['correct']}"
        user["quiz_scores"].append(0)
    
    save_user_data(user_id, user)
    
    msg = f"<b>❓ Quiz:</b>\n\n{question['question']}\n\n{result}\n\n"
    msg += f"<b>သင်၏ စုစုပေါင်း Score:</b> {user['total_score']}"
    
    await query.edit_message_text(msg, parse_mode="HTML")

async def streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /streak command"""
    user_id = update.effective_user.id
    current_streak = update_streak(user_id)
    user = get_user_data(user_id)
    
    msg = f"<b>🔥 သင်၏ Learning Streak:</b>\n\n"
    msg += f"🔥 လက်ရှိ Streak: <b>{current_streak}</b> နေ့\n"
    msg += f"📅 နောက်ဆုံးသင်ယူသည့်နေ့: {user['last_active']}\n\n"
    msg += "💪 ဆက်လက်ကြိုးစားပါ!"
    
    await update.message.reply_text(msg, parse_mode="HTML")

async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /progress command"""
    user_id = update.effective_user.id
    user = get_user_data(user_id)
    
    total_lessons = len(user["completed_lessons"])
    total_quizzes = len(user["quiz_scores"])
    correct_answers = sum(user["quiz_scores"])
    accuracy = (correct_answers / total_quizzes * 100) if total_quizzes > 0 else 0
    
    msg = f"<b>📊 သင်၏တိုးတက်မှု:</b>\n\n"
    msg += f"📚 ပြီးမြောက်ပြီးသော သင်ခန်းစာ: <b>{total_lessons}</b>\n"
    msg += f"❓ Quiz ဖြေဆိုခဲ့သည်: <b>{total_quizzes}</b>\n"
    msg += f"✅ မှန်ကန်သောအဖြေ: <b>{correct_answers}</b>\n"
    msg += f"📈 တိကျမှု: <b>{accuracy:.1f}%</b>\n"
    msg += f"⭐ စုစုပေါင်း Score: <b>{user['total_score']}</b>\n"
    msg += f"🔥 Streak: <b>{user['streak']}</b> နေ့\n\n"
    msg += "🎯 ဆက်လက်တိုးတက်ပါစေ!"
    
    await update.message.reply_text(msg, parse_mode="HTML")

async def practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /practice command"""
    scenarios = [
        {
            "name": "ordering_coffee",
            "question": "☕ ကော်ဖီဆိုင်မှာ: ကော်ဖီ မှာယူချင်ရင် ဘယ်လိုပြောမလဲ?",
            "example": "아이스 아메리카노 한 잔 주세요 (Ice Americano တစ်ခွက်ပေးပါ)"
        },
        {
            "name": "greeting",
            "question": "👋 နှုတ်ဆက်ခြင်း: မနက်ခင်းစာ မှာဘယ်လိုနှုတ်ဆက်မလဲ?",
            "example": "좋은 아침입니다 (ကောင်းသော မနက်ခင်းပါ)"
        },
        {
            "name": "shopping",
            "question": "🛍️ ဈေးဝယ်ခြင်း: ဈေးဘယ်လောက်လဲ လို့ ဘယ်လိုမေးမလဲ?",
            "example": "이거 얼마예요? (ဒါ ဘယ်လောက်လဲ?)"
        }
    ]
    
    scenario = random.choice(scenarios)
    
    msg = f"<b>💬 စကားပြောလေ့ကျင့်ခန်း:</b>\n\n"
    msg += f"{scenario['question']}\n\n"
    msg += f"<b>ဥပမာအဖြေ:</b>\n{scenario['example']}\n\n"
    msg += "📝 သင့်အဖြေကို ရိုက်ထည့်ကြည့်ပါ!"
    
    await update.message.reply_text(msg, parse_mode="HTML")

async def homework(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /homework command"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    if not context.args:
        msg = "📝 <b>Homework တင်ရန်:</b>\n\n"
        msg += "အသုံးပြုပုံ:\n"
        msg += "/homework <သင့် homework အကြောင်းအရာ>\n\n"
        msg += "သို့မဟုတ် file တစ်ခုကို attach လုပ်ပြီး caption မှာ /homework လို့ရိုက်ထည့်ပါ။"
        await update.message.reply_text(msg, parse_mode="HTML")
        return
    
    homework_text = " ".join(context.args)
    
    # Save to admin notifications (in real implementation)
    msg = f"✅ သင့် homework ကို တင်သွင်းပြီးပါပြီ!\n\n"
    msg += f"📄 အကြောင်းအရာ: {homework_text}\n\n"
    msg += "👨‍🏫 Tutor များက မကြာမီ စစ်ဆေးပေးပါလိမ့်မည်။"
    
    # Notify admins
    for admin_id in ADMIN_IDS:
        try:
            admin_msg = f"📨 <b>Homework အသစ်:</b>\n\n"
            admin_msg += f"👤 User: {user_name} (ID: {user_id})\n"
            admin_msg += f"📄 {homework_text}"
            await context.bot.send_message(chat_id=admin_id, text=admin_msg, parse_mode="HTML")
        except:
            pass
    
    await update.message.reply_text(msg, parse_mode="HTML")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /report command"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    if not context.args:
        await update.message.reply_text("❌ အသုံးပြုပုံ: /report <သင့်အကြံပြုချက် သို့မဟုတ် ပြဿနာ>")
        return
    
    report_text = " ".join(context.args)
    
    # Notify admins
    for admin_id in ADMIN_IDS:
        try:
            admin_msg = f"📢 <b>Report အသစ်:</b>\n\n"
            admin_msg += f"👤 User: {user_name} (ID: {user_id})\n"
            admin_msg += f"📄 {report_text}"
            await context.bot.send_message(chat_id=admin_id, text=admin_msg, parse_mode="HTML")
        except:
            pass
    
    await update.message.reply_text("✅ သင့် report ကို ပို့ပြီးပါပြီ။ ကျေးဇူးတင်ပါတယ်! 🙏")

# ==================== Admin Commands ====================

async def admin_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Decorator to check admin access"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ ဤ command ကို admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return False
    return True

async def edlesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edlesson command"""
    if not await admin_only(update, context):
        return
    
    if not context.args:
        msg = "📚 <b>Lesson စီမံခန့်ခွဲရန်:</b>\n\n"
        msg += "အသုံးပြုပုံ:\n"
        msg += "/edlesson add|lesson_id|title|content\n"
        msg += "/edlesson edit|lesson_id|title|content\n"
        msg += "/edlesson delete|lesson_id\n"
        msg += "/edlesson list"
        await update.message.reply_text(msg, parse_mode="HTML")
        return
    
    lessons = load_json(DB_LESSONS, {"lessons": []})
    
    if context.args[0] == "list":
        if not lessons["lessons"]:
            await update.message.reply_text("📚 Lesson များ မရှိသေးပါ။")
            return
        
        msg = "<b>📚 Lesson စာရင်း:</b>\n\n"
        for lesson in lessons["lessons"]:
            msg += f"🔹 {lesson['id']} - {lesson['title']}\n"
        await update.message.reply_text(msg, parse_mode="HTML")
        return
    
    parts = " ".join(context.args).split("|")
    
    if len(parts) < 2:
        await update.message.reply_text("❌ Format မှားနေပါသည်။")
        return
    
    action = parts[0].strip()
    
    if action == "add":
        if len(parts) < 4:
            await update.message.reply_text("❌ Format: /edlesson add|lesson_id|title|content")
            return
        
        lesson_id = parts[1].strip()
        title = parts[2].strip()
        content = parts[3].strip()
        
        lessons["lessons"].append({
            "id": lesson_id,
            "title": title,
            "content": content
        })
        save_json(DB_LESSONS, lessons)
        await update.message.reply_text(f"✅ Lesson '{lesson_id}' ထည့်သွင်းပြီးပါပြီ!")
    
    elif action == "delete":
        lesson_id = parts[1].strip()
        lessons["lessons"] = [l for l in lessons["lessons"] if l["id"] != lesson_id]
        save_json(DB_LESSONS, lessons)
        await update.message.reply_text(f"✅ Lesson '{lesson_id}' ဖျက်ပြီးပါပြီ!")

async def edvocab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edvocab command"""
    if not await admin_only(update, context):
        return
    
    if not context.args:
        msg = "📖 <b>Vocabulary စီမံခန့်ခွဲရန်:</b>\n\n"
        msg += "အသုံးပြုပုံ:\n"
        msg += "/edvocab add|word|meaning|example\n"
        msg += "/edvocab delete|word\n"
        msg += "/edvocab list"
        await update.message.reply_text(msg, parse_mode="HTML")
        return
    
    vocab_data = load_json(DB_VOCAB, {"words": []})
    
    if context.args[0] == "list":
        if not vocab_data["words"]:
            await update.message.reply_text("📖 Vocabulary မရှိသေးပါ။")
            return
        
        msg = "<b>📖 Vocabulary စာရင်း:</b>\n\n"
        for word in vocab_data["words"][:20]:  # Show first 20
            msg += f"🔹 {word['word']} - {word['meaning']}\n"
        await update.message.reply_text(msg, parse_mode="HTML")
        return
    
    parts = " ".join(context.args).split("|")
    
    if len(parts) < 2:
        await update.message.reply_text("❌ Format မှားနေပါသည်။")
        return
    
    action = parts[0].strip()
    
    if action == "add":
        if len(parts) < 3:
            await update.message.reply_text("❌ Format: /edvocab add|word|meaning|example")
            return
        
        word = parts[1].strip()
        meaning = parts[2].strip()
        example = parts[3].strip() if len(parts) > 3 else ""
        
        vocab_data["words"].append({
            "word": word,
            "meaning": meaning,
            "example": example
        })
        save_json(DB_VOCAB, vocab_data)
        await update.message.reply_text(f"✅ Vocabulary '{word}' ထည့်သွင်းပြီးပါပြီ!")
    
    elif action == "delete":
        word = parts[1].strip()
        vocab_data["words"] = [w for w in vocab_data["words"] if w["word"] != word]
        save_json(DB_VOCAB, vocab_data)
        await update.message.reply_text(f"✅ Vocabulary '{word}' ဖျက်ပြီးပါပြီ!")

async def edquiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edquiz command"""
    if not await admin_only(update, context):
        return
    
    if not context.args:
        msg = "❓ <b>Quiz စီမံခန့်ခွဲရန်:</b>\n\n"
        msg += "အသုံးပြုပုံ:\n"
        msg += "/edquiz add|topic|question|A|B|C|D|correct\n"
        msg += "/edquiz list"
        await update.message.reply_text(msg, parse_mode="HTML")
        return
    
    quiz_data = load_json(DB_QUIZ, {"quizzes": []})
    
    if context.args[0] == "list":
        if not quiz_data["quizzes"]:
            await update.message.reply_text("❓ Quiz များ မရှိသေးပါ။")
            return
        
        msg = "<b>❓ Quiz စာရင်း:</b>\n\n"
        for quiz in quiz_data["quizzes"][:10]:
            msg += f"🔹 {quiz['id']}: {quiz['question']}\n"
        await update.message.reply_text(msg, parse_mode="HTML")
        return
    
    parts = " ".join(context.args).split("|")
    
    if parts[0].strip() == "add":
        if len(parts) < 8:
            await update.message.reply_text("❌ Format: /edquiz add|topic|question|A|B|C|D|correct")
            return
        
        quiz_id = f"q{len(quiz_data['quizzes']) + 1}"
        
        quiz_data["quizzes"].append({
            "id": quiz_id,
            "topic": parts[1].strip(),
            "question": parts[2].strip(),
            "A": parts[3].strip(),
            "B": parts[4].strip(),
            "C": parts[5].strip(),
            "D": parts[6].strip(),
            "correct": parts[7].strip()
        })
        save_json(DB_QUIZ, quiz_data)
        await update.message.reply_text(f"✅ Quiz '{quiz_id}' ထည့်သွင်းပြီးပါပြီ!")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /broadcast command"""
    if not await admin_only(update, context):
        return
    
    if not context.args:
        await update.message.reply_text("❌ အသုံးပြုပုံ: /broadcast <message>")
        return
    
    message = " ".join(context.args)
    users = load_json(DB_USERS, {})
    
    sent = 0
    failed = 0
    
    for user_id in users.keys():
        try:
            await context.bot.send_message(
                chat_id=int(user_id),
                text=f"📢 <b>Announcement:</b>\n\n{message}",
                parse_mode="HTML"
            )
            sent += 1
        except:
            failed += 1
    
    await update.message.reply_text(f"✅ Broadcast ပို့ပြီးပါပြီ!\n\n✅ ပို့ပြီး: {sent}\n❌ မအောင်မြင်: {failed}")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    if not await admin_only(update, context):
        return
    
    users = load_json(DB_USERS, {})
    lessons = load_json(DB_LESSONS, {"lessons": []})
    vocab = load_json(DB_VOCAB, {"words": []})
    quizzes = load_json(DB_QUIZ, {"quizzes": []})
    
    total_users = len(users)
    total_lessons = len(lessons["lessons"])
    total_vocab = len(vocab["words"])
    total_quizzes = len(quizzes["quizzes"])
    
    # Active users (last 7 days)
    active_users = 0
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    for user in users.values():
        if user.get("last_active", "") >= seven_days_ago:
            active_users += 1
    
    # Top learners
    top_users = sorted(users.values(), key=lambda x: x.get("total_score", 0), reverse=True)[:5]
    
    msg = "<b>📊 Bot Statistics:</b>\n\n"
    msg += f"👥 စုစုပေါင်း Users: {total_users}\n"
    msg += f"✅ Active Users (7 days): {active_users}\n"
    msg += f"📚 Lessons: {total_lessons}\n"
    msg += f"📖 Vocabulary: {total_vocab}\n"
    msg += f"❓ Quizzes: {total_quizzes}\n\n"
    
    msg += "<b>🏆 Top Learners:</b>\n"
    for i, user in enumerate(top_users, 1):
        msg += f"{i}. User {user['user_id']} - Score: {user['total_score']}\n"
    
    await update.message.reply_text(msg, parse_mode="HTML")

async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /backup command"""
    if not await admin_only(update, context):
        return
    
    import shutil
    import zipfile
    from datetime import datetime
    
    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    with zipfile.ZipFile(backup_name, 'w') as zipf:
        for file in [DB_USERS, DB_LESSONS, DB_VOCAB, DB_QUIZ, DB_SETTINGS, DB_TUTORS]:
            if os.path.exists(file):
                zipf.write(file)
    
    await update.message.reply_document(
        document=open(backup_name, 'rb'),
        filename=backup_name,
        caption="✅ Backup ပြီးပါပြီ!"
    )
    
    os.remove(backup_name)

async def roles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /roles command"""
    if not await admin_only(update, context):
        return
    
    if not context.args or len(context.args) < 2:
        msg = "👥 <b>Role စီမံခန့်ခွဲရန်:</b>\n\n"
        msg += "အသုံးပြုပုံ:\n"
        msg += "/roles set <user_id> <role>\n"
        msg += "/roles remove <user_id>\n"
        msg += "/roles list\n\n"
        msg += "Roles: user, tutor, admin"
        await update.message.reply_text(msg, parse_mode="HTML")
        return
    
    action = context.args[0]
    
    if action == "list":
        users = load_json(DB_USERS, {})
        msg = "<b>👥 User Roles:</b>\n\n"
        for user_id, user_data in users.items():
            role = user_data.get("role", "user")
            if role != "user":
                msg += f"👤 {user_id}: {role}\n"
        await update.message.reply_text(msg, parse_mode="HTML")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("❌ Format မှားနေပါသည်။")
        return
    
    target_user_id = int(context.args[1])
    
    if action == "set":
        if len(context.args) < 3:
            await update.message.reply_text("❌ အသုံးပြုပုံ: /roles set <user_id> <role>")
            return
        
        role = context.args[2]
        if role not in ["user", "tutor", "admin"]:
            await update.message.reply_text("❌ Role သည် user, tutor, သို့မဟုတ် admin ဖြစ်ရမည်။")
            return
        
        user = get_user_data(target_user_id)
        user["role"] = role
        save_user_data(target_user_id, user)
        await update.message.reply_text(f"✅ User {target_user_id} ကို {role} အဖြစ် သတ်မှတ်ပြီးပါပြီ!")
    
    elif action == "remove":
        user = get_user_data(target_user_id)
        user["role"] = "user"
        save_user_data(target_user_id, user)
        await update.message.reply_text(f"✅ User {target_user_id} ၏ special role ကို ဖယ်ရှားပြီးပါပြီ!")

# ==================== Main ====================

def main():
    """Start the bot"""
    # Get bot token from environment
    token = os.getenv("BOT_TOKEN")
    if not token:
        logger.error("BOT_TOKEN not found in .env file!")
        return
    
    # Create application
    application = Application.builder().token(token).build()
    
    # User commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("lesson", lesson))
    application.add_handler(CommandHandler("startlesson", startlesson))
    application.add_handler(CommandHandler("vocab", vocab))
    application.add_handler(CommandHandler("flashcard", flashcard))
    application.add_handler(CommandHandler("pronounce", pronounce))
    application.add_handler(CommandHandler("translate", translate))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("streak", streak))
    application.add_handler(CommandHandler("progress", progress))
    application.add_handler(CommandHandler("practice", practice))
    application.add_handler(CommandHandler("homework", homework))
    application.add_handler(CommandHandler("report", report))
    
    # Admin commands
    application.add_handler(CommandHandler("edlesson", edlesson))
    application.add_handler(CommandHandler("edvocab", edvocab))
    application.add_handler(CommandHandler("edquiz", edquiz))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("backup", backup))
    application.add_handler(CommandHandler("roles", roles))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(flashcard_callback, pattern="^flashcard_"))
    application.add_handler(CallbackQueryHandler(quiz_callback, pattern="^quiz_"))
    
    # Start bot
    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
