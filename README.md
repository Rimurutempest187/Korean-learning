# ╔═══════════════════════════════════════════════════╗
# ║     🌍 SUPER LEARNING BOT — README                ║
# ║         Create by : PINLON-YOUTH                  ║
# ╚═══════════════════════════════════════════════════╝

# SUPER LEARNING BOT 🌍

**Universal Language Learning Bot for Telegram**
*No paid API keys required — 100% Free to Run!*

---

## 🚀 Quick Start

### 1. Get Your Bot Token
1. Open Telegram → Search `@BotFather`
2. Send `/newbot`
3. Follow instructions → Copy your **Bot Token**

### 2. Setup
```bash
# Clone or extract the bot files
cd super_learning_bot

# Install Python dependencies
pip install -r requirements.txt

# Edit .env file
nano .env
```

### 3. Configure .env
```env
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_IDS=your_telegram_user_id
TIMEZONE=Asia/Yangon
```

> 💡 Get your Telegram User ID: message @userinfobot

### 4. Run
```bash
python bot.py
```

---

## 📁 File Structure

```
super_learning_bot/
├── bot.py              # Main entry point
├── config.py           # Configuration & constants
├── database.py         # SQLite database layer
├── lessons_data.py     # Built-in lesson content
├── user_handlers.py    # User command handlers
├── admin_handlers.py   # Admin command handlers
├── callback_handlers.py # Button & message handlers
├── keyboards.py        # Inline keyboard builder
├── utils.py            # TTS, translation, image utils
├── scheduler.py        # Daily reminders & notifications
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
└── audio_cache/        # TTS audio cache (auto-created)
```

---

## 🔧 Technology Stack

| Feature | Technology | Cost |
|---------|-----------|------|
| Bot Framework | python-telegram-bot | Free |
| Database | SQLite | Free |
| Text-to-Speech | gTTS (Google TTS) | Free |
| Translation | deep-translator | Free |
| Progress Cards | Pillow (PIL) | Free |
| Charts | matplotlib | Free |
| Scheduling | APScheduler | Free |
| AI/ML | Built-in algorithms | Free |

---

## 🌍 Supported Languages

- 🇺🇸 English
- 🇰🇷 Korean
- 🇯🇵 Japanese
- 🇨🇳 Chinese
- 🇲🇲 Burmese
- 🇫🇷 French
- 🇩🇪 German
- 🇪🇸 Spanish
- 🇹🇭 Thai
- 🇻🇳 Vietnamese

---

## 📝 Admin Commands

Add your Telegram ID to `ADMIN_IDS` in `.env`:

| Command | Description |
|---------|-------------|
| /stats | View bot statistics |
| /leaderboard | Global rankings |
| /broadcast | Send to all users |
| /edlesson | Add custom lesson |
| /edquiz | Add quiz question |
| /roles | Manage user roles |
| /backup | Download database backup |
| /resetuser | Reset a user's data |

---

## 🎮 Gamification System

- **XP Points**: Earn XP for every activity
- **Levels**: 11 levels from 🌱 Seed to 🚀 Legend
- **Streaks**: Daily login streaks
- **Badges**: 10 achievement badges
- **Leaderboard**: Global rankings
- **Duels**: Quiz battles

---

*Create by : PINLON-YOUTH*
