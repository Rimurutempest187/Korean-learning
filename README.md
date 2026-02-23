# SUPER LEARNING BOT - Universal Language Learning Bot

**Create by: PINLON-YOUTH**

## 🌍 Overview

SUPER LEARNING BOT is a comprehensive Telegram bot designed to help users learn languages effectively through:
- **Adaptive Learning Engine**: Personalized daily lessons
- **AI Tutor**: Conversation practice with AI
- **Gamification**: XP, levels, streaks, and badges
- **Progress Tracking**: Detailed analytics and visualizations
- **Multi-language Support**: Learn English, Korean, Japanese, Chinese, Spanish, French, German, Thai, Myanmar

## ✨ Key Features

### 🎓 Learning Features
- **Daily Lessons**: Auto-generated lessons based on level
- **Vocabulary System**: Spaced repetition flashcards
- **Grammar Explanations**: Interactive grammar learning
- **Pronunciation Practice**: Text-to-speech exercises
- **Listening Exercises**: Audio comprehension training

### 💬 AI-Powered Features
- **AI Tutor Mode**: Natural conversation practice
- **Scenario Practice**: Restaurant, airport, shopping, interviews
- **Grammar Correction**: Real-time sentence correction
- **Personalized Feedback**: Adaptive learning recommendations

### 🎮 Gamification
- **XP & Levels**: Earn points for every activity
- **Streak System**: Daily learning streaks with bonuses
- **Badges**: 10+ achievement badges to collect
- **Leaderboard**: Compete with other learners
- **Daily Challenges**: Special goals with bonus rewards

### 📊 Progress Tracking
- **Personal Dashboard**: Visual progress cards
- **Weekly Reports**: Automated progress summaries
- **Learning Analytics**: Detailed statistics
- **Study Calendar**: GitHub-style contribution calendar

### 👥 Social Features
- **Study Groups**: Join group learning sessions
- **Leaderboard**: Global rankings
- **Progress Sharing**: Share achievements with friends

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenAI API Key (optional, for AI Tutor features)

### Installation

1. **Clone or download the bot files**
```bash
cd super_learning_bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` file and add your tokens:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
ADMIN_USER_IDS=your_telegram_user_id
```

4. **Run the bot**
```bash
python bot.py
```

## 📱 User Commands

### 🔰 Getting Started
- `/start` - Start the bot and set up your profile
- `/lang` - Change learning language
- `/profile` - View your profile and stats

### 📚 Learning
- `/learn` - Start today's lesson
- `/lesson <topic>` - Learn specific topic
- `/path` - View learning roadmap
- `/review` - Review previous content

### 🧠 Vocabulary
- `/vocab` - Today's vocabulary words
- `/deck` - Your saved vocabulary deck
- `/save <word>` - Save word to deck
- `/flash` - Flashcard practice mode

### 🎧 Practice
- `/say <text>` - Pronunciation practice
- `/listen` - Listening exercise
- `/repeat` - Shadowing practice

### 💬 AI Tutor
- `/tutor` - Start conversation practice
- `/roleplay <scenario>` - Practice specific scenarios
- `/correct <sentence>` - Get grammar correction

### 🎯 Quizzes
- `/quiz` - Take a quiz
- `/challenge` - Timed challenge mode
- `/exam` - Level test
- `/tops` - View leaderboard

### 📊 Progress
- `/progress` - View progress analytics
- `/streak` - Check your streak
- `/badges` - View earned badges
- `/goal` - Set daily goals

### 🤝 Social
- `/studygroup` - Join study groups
- `/duel` - Quiz battle with friends
- `/share` - Share progress card

### ⚙️ Utility
- `/translate <text>` - Quick translation
- `/report` - Send feedback
- `/help` - Show help menu

## 👨‍💼 Admin Commands

### 📚 Content Management
- `/edlesson` - Add/edit lessons
- `/edpath` - Manage learning path
- `/edvocab` - Upload vocabulary
- `/edquiz` - Add quizzes
- `/edaudio` - Upload audio files

### 👥 User Management
- `/stats` - Platform statistics
- `/leaderboard` - Global rankings
- `/broadcast <message>` - Send announcement
- `/roles` - Manage user roles

### ⚙️ System
- `/set` - Configure bot settings
- `/backup` - Backup database
- `/restore` - Restore from backup
- `/resetuser` - Reset user progress

## 🏗️ Project Structure

```
super_learning_bot/
├── bot.py                  # Main bot application
├── database.py             # Database operations
├── models.py               # Data models
├── ai_tutor.py            # AI conversation features
├── content_manager.py      # Content management
├── gamification.py         # XP, levels, badges
├── progress_card.py        # Progress visualizations
├── scheduler.py            # Daily reminders
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── README.md              # This file
└── superlearning.db       # SQLite database (auto-created)
```

## 🎨 Features Breakdown

### Adaptive Learning Engine
- Analyzes user performance
- Adjusts difficulty automatically
- Focuses on weak areas
- Personalizes content recommendations

### Smart Memory System
The bot tracks:
- Vocabulary retention
- Grammar accuracy
- Speaking fluency
- Listening comprehension

### Daily Planner
Automatically builds daily lessons with:
- 5 new vocabulary words
- 1 grammar point
- 1 listening exercise
- 1 practice quiz

### Progress Card Generator
Creates beautiful visual reports showing:
- Weekly study time
- Accuracy trends
- Streak calendar
- Level progress
- Badge collection

## 🎯 Gamification System

### XP System
Earn XP for:
- Completing lessons: 50 XP
- Taking quizzes: 30 XP
- Learning vocabulary: 5 XP per word
- AI conversations: 20 XP
- Daily goal completion: 25 XP
- Streak bonuses: up to 50 XP

### Badges
Unlock badges like:
- 👣 First Steps - Complete first lesson
- 🔥 Week Warrior - 7-day streak
- 🎯 Monthly Master - 30-day streak
- 📚 Word Wizard - Learn 100 words
- 🏆 Quiz Champion - 10 perfect scores
- 💬 Conversation Pro - 50 AI chats

### Streak System
- Daily login bonuses
- Streak warnings
- Milestone rewards
- Recovery options

## 🔧 Configuration

### Environment Variables
```env
# Required
TELEGRAM_BOT_TOKEN=your_token

# Optional
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
ADMIN_USER_IDS=123456789,987654321
TIMEZONE=Asia/Yangon
DAILY_REMINDER_TIME=09:00
EVENING_REMINDER_TIME=19:00
ENABLE_PREMIUM_FEATURES=false
LOG_LEVEL=INFO
```

### Database
The bot uses SQLite by default. Tables:
- `users` - User profiles
- `lessons` - Learning content
- `vocabulary` - Word database
- `user_progress` - Learning history
- `quizzes` - Quiz questions
- `badges` - Achievements
- `conversations` - AI chat history

## 📈 Analytics

Track:
- Active users (daily/weekly/monthly)
- Lesson completion rates
- Quiz accuracy
- Average study time
- Retention rates
- Feature usage

## 🌟 Premium Features (Optional)

- Advanced AI conversations
- Personalized study plans
- Certificate generation
- Priority support
- Ad-free experience
- Extended analytics

## 🐛 Troubleshooting

### Bot not responding
1. Check `TELEGRAM_BOT_TOKEN` is correct
2. Ensure bot is running (`python bot.py`)
3. Check firewall/network settings

### AI Tutor not working
1. Verify `OPENAI_API_KEY` is set
2. Check API quota/billing
3. See logs for error details

### Database errors
1. Check write permissions
2. Backup and delete `superlearning.db`
3. Restart bot to recreate

## 📝 Development

### Adding New Languages
1. Add language code to `AVAILABLE_LANGUAGES` in `bot.py`
2. Add sample content to `content_manager.py`
3. Update AI tutor prompts in `ai_tutor.py`

### Adding New Badges
1. Define badge in `gamification.py`
2. Add check logic in `check_badge_eligibility()`
3. Add badge icon and description

### Customizing Reminders
Edit `scheduler.py` to:
- Change reminder times
- Add new scheduled tasks
- Customize message content

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Test thoroughly
4. Submit pull request

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Credits

**Create by: PINLON-YOUTH**

Special thanks to:
- python-telegram-bot community
- OpenAI for GPT API
- All language learners worldwide

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Contact via Telegram
- Email support team

## 🚀 Future Roadmap

- [ ] Voice message support
- [ ] Image-based learning
- [ ] Group learning sessions
- [ ] Live tutor matching
- [ ] Mobile app version
- [ ] Web dashboard
- [ ] More languages
- [ ] Advanced analytics
- [ ] Integration with other platforms

---

**Start your language learning journey today! 🌍📚**

_Create by: PINLON-YOUTH_
