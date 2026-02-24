# Language Learning Ecosystem Telegram Bot

A production-ready Telegram bot for learning English, Japanese, and Korean with translations to Myanmar. Built with gamification features inspired by Duolingo.

## 🌟 Features

### Core Learning
- **Multi-Language Support**: English 🇬🇧, Japanese 🇯🇵, Korean 🇰🇷 → Myanmar 🇲🇲
- **Structured Progression**: Beginner, Intermediate, and Advanced units
- **Interactive Quizzes**: Multiple choice and text input questions
- **Rich Content**: Furigana for Japanese, Romanization for Korean

### Gamification
- **❤️ Hearts System**: 5 hearts, lose 1 per wrong answer, refill every 4 hours
- **⭐️ XP System**: 
  - +10 XP per correct answer
  - +50 XP per completed lesson
- **🔥 Streak System**: Daily learning streaks with reminders
- **🏆 Achievements**: Unlock badges for milestones
- **📊 Leaderboard**: Top 10 users with medals 🥇🥈🥉

### Social & Retention
- **Notifications**: 24-hour inactivity reminders
- **Profile Statistics**: Track progress across languages
- **Progress Bars**: Visual progress indicators
- **Leaderboard Competition**: Compete with other learners

### Admin Features
- **Database Backup**: `/backup` command
- **Database Restore**: `/restore` command
- **Restricted Access**: Admin-only commands

## 📋 Requirements

```
python>=3.10
python-telegram-bot>=20.0
aiosqlite>=0.19.0
python-dotenv>=1.0.0
gTTS>=2.3.0
deep-translator>=1.11.0
```

## 🚀 Installation

### 1. Clone or Download the Project

```bash
# Create project directory
mkdir language_learning_bot
cd language_learning_bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_ID=your_telegram_user_id_here
DB_PATH=language_bot.db
```

**How to get your BOT_TOKEN:**
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the instructions
3. Copy the token provided

**How to get your ADMIN_ID:**
1. Search for [@userinfobot](https://t.me/userinfobot) on Telegram
2. Start the bot and it will show your user ID

### 4. Run the Bot

```bash
python bot.py
```

## 📁 Project Structure

```
language_learning_bot/
│
├── bot.py                          # Main entry point
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables
├── README.md                      # This file
│
├── managers/
│   ├── database_manager.py       # Database operations
│   ├── user_manager.py            # User data & game mechanics
│   ├── lesson_manager.py          # Lesson content management
│   └── notification_manager.py    # Notification handling
│
├── handlers/
│   ├── start_handler.py          # /start, /help, main menu
│   ├── lesson_handler.py         # Lesson browsing & display
│   ├── quiz_handler.py           # Quiz sessions & answers
│   ├── profile_handler.py        # User profile & stats
│   ├── leaderboard_handler.py    # Leaderboard display
│   └── admin_handler.py          # Admin commands
│
├── utils/
│   ├── error_handler.py          # Global error handling
│   └── formatter.py              # Text formatting utilities
│
├── data/
│   └── lessons.json              # Lesson content (expandable)
│
└── backups/                      # Database backups (auto-created)
```

## 🎮 Bot Commands

### User Commands
- `/start` - Initialize bot and show main menu
- `/learn` - Browse available lessons
- `/profile` - View your profile and statistics
- `/top` - View leaderboard (Top 10)
- `/help` - Show help information

### Admin Commands (Restricted)
- `/backup` - Create database backup
- `/restore` - Restore database from file

## 🎯 Usage Flow

1. **Start**: User sends `/start`
2. **Choose Language**: Select English, Japanese, or Korean
3. **Select Unit**: Choose Beginner, Intermediate, or Advanced
4. **Pick Lesson**: Select a specific lesson
5. **Study Vocabulary**: Review words and translations
6. **Take Quiz**: Answer questions to earn XP
7. **Track Progress**: View profile and leaderboard

## 🔧 Configuration

### Game Mechanics (in `config.py`)

```python
MAX_HEARTS = 5                    # Maximum hearts
HEART_REFILL_HOURS = 4           # Hours between refills
XP_PER_CORRECT_ANSWER = 10       # XP for correct answer
XP_PER_LESSON_COMPLETE = 50      # XP for completing lesson
STREAK_NOTIFICATION_HOURS = 24   # Inactivity reminder delay
```

### Database Schema

**Users Table:**
- user_id, username, first_name
- xp, hearts, streak
- last_active, last_heart_refill
- notification_enabled, current_language

**Progress Table:**
- user_id, language, unit, lesson_id
- completed, score, completed_at

**Achievements Table:**
- user_id, achievement_id, unlocked_at

**Quiz Sessions Table:**
- user_id, language, lesson_id
- current_question, correct_answers
- total_questions, session_data

## 📚 Adding New Lessons

Edit `data/lessons.json` to add new content:

```json
{
  "english": {
    "beginner": [
      {
        "id": "eng_b_03",
        "title": "Your Lesson Title",
        "description": "Lesson description",
        "vocabulary": [
          {
            "word": "Word",
            "translation": "Myanmar Translation",
            "pronunciation": "pronunciation"
          }
        ],
        "quiz": [
          {
            "question": "Question text?",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "correct": 0,
            "type": "multiple_choice"
          }
        ]
      }
    ]
  }
}
```

## 🔒 Security Features

- **Environment Variables**: Sensitive data not in code
- **Admin Verification**: Protected admin commands
- **Error Handling**: Robust exception management
- **Database Safety**: Async operations prevent locks
- **Input Validation**: Sanitized user inputs

## 📊 Monitoring & Logs

The bot logs important events:
- User registrations
- XP gains
- Achievement unlocks
- Admin actions
- Errors and exceptions

## 🚢 Deployment

### Local Development
```bash
python bot.py
```

### Production Deployment Options

**1. VPS/Cloud Server (Recommended)**
```bash
# Using systemd service
sudo nano /etc/systemd/system/language-bot.service

[Unit]
Description=Language Learning Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/language_learning_bot
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target

# Start service
sudo systemctl start language-bot
sudo systemctl enable language-bot
```

**2. Docker (Optional)**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

**3. Heroku/Railway/Render**
- Add `Procfile`: `worker: python bot.py`
- Set environment variables in platform settings

## 🐛 Troubleshooting

### Bot doesn't respond
- Check BOT_TOKEN is correct
- Verify bot is running (`python bot.py`)
- Check internet connection

### Database errors
- Ensure write permissions for DB file
- Check disk space
- Run `/backup` regularly

### Hearts not refilling
- Check system time is correct
- Verify HEART_REFILL_HOURS setting

## 🔮 Future Enhancements

- [ ] Audio pronunciation with gTTS
- [ ] Voice message responses
- [ ] Spaced repetition system
- [ ] Daily challenges
- [ ] Friend referral system
- [ ] Premium features
- [ ] More languages
- [ ] Mobile app integration

## 📄 License

This project is provided as-is for educational and commercial use.

## 👨‍💻 Support

For issues or questions:
1. Check the troubleshooting section
2. Review bot logs for errors
3. Verify configuration settings

## 🙏 Acknowledgments

- Inspired by Duolingo's gamification approach
- Built with python-telegram-bot library
- Myanmar translations for cultural accessibility

---

**Made with ❤️ for language learners worldwide**
