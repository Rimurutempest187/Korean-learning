# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Get Your Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the **bot token** (format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Get Your Admin ID

1. Search for **@userinfobot** on Telegram
2. Start the bot
3. Copy your **user ID** (a number like `123456789`)

### Step 3: Install

```bash
# Install Python 3.10+ if not already installed
# On Ubuntu/Debian:
sudo apt update
sudo apt install python3.10 python3-pip

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure

Create a `.env` file in the root directory:

```bash
cp .env.example .env
nano .env
```

Edit the file:
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_ID=123456789
DB_PATH=language_bot.db
```

### Step 5: Run

```bash
python bot.py
```

You should see:
```
✅ Database initialized: language_bot.db
✅ Bot initialized successfully
✅ All handlers registered
✅ Job queue configured
🚀 Starting Language Learning Bot...
```

### Step 6: Test

Open Telegram and find your bot, then send:
```
/start
```

## 🎯 First Steps

1. **Send `/start`** - Initialize the bot
2. **Click "📚 Start Learning"** - Browse lessons
3. **Select a language** - English, Japanese, or Korean
4. **Choose "Beginner"** - Start with basics
5. **Pick a lesson** - "Greetings & Basics" is recommended
6. **Study vocabulary** - Review the words
7. **Take the quiz** - Click "🎯 Start Quiz"
8. **Earn XP!** - Get points for correct answers

## 💡 Tips

- Start with Beginner lessons to build XP
- Wrong answers cost hearts - be careful!
- Hearts refill every 4 hours automatically
- Practice daily to maintain your streak
- Check `/top` to see the leaderboard
- Use `/profile` to track your progress

## 🔧 Troubleshooting

### Bot doesn't start
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### "BOT_TOKEN not found" error
- Make sure `.env` file exists in the root directory
- Check that variable names are correct (no spaces)
- Verify token format: `number:letters`

### Bot responds slowly
- Normal for first message (initialization)
- Check internet connection
- Verify server resources

## 📱 Using the Bot

### Navigation
- All navigation is via **inline keyboard buttons**
- No need to type commands manually
- Use "← Back" buttons to go back
- "🏠 Main Menu" returns to start

### Quiz System
- Multiple choice: Click the correct answer
- Text input: Type your answer (for some questions)
- ✅ Correct = +10 XP
- ❌ Wrong = -1 ❤️

### Hearts System
- Start with 5 hearts ❤️❤️❤️❤️❤️
- Wrong answer = lose 1 heart
- No hearts = can't take quizzes
- Automatic refill every 4 hours
- Check profile for heart status

### XP & Levels
- Correct answer: +10 XP
- Complete lesson: +50 XP
- Unlock achievement: Bonus XP
- Level = XP ÷ 100

### Streaks
- Practice every day to build streak 🔥
- Miss a day = streak resets to 0
- Get reminder after 24 hours inactive
- Toggle notifications in profile

## 🎮 Commands Reference

| Command | Description |
|---------|-------------|
| `/start` | Start bot / Main menu |
| `/learn` | Browse lessons |
| `/profile` | Your stats & settings |
| `/top` | Leaderboard (Top 10) |
| `/help` | Show help guide |
| `/backup` | 🔒 Admin: Backup database |
| `/restore` | 🔒 Admin: Restore database |

## 🏆 Achievement Guide

| Achievement | Requirement | XP Bonus |
|-------------|------------|----------|
| 🎓 First Steps | Complete 1 lesson | +100 XP |
| 🔥 Week Warrior | 7-day streak | +200 XP |
| 🏆 Monthly Master | 30-day streak | +500 XP |
| 📚 Bookworm | Complete 10 lessons | +300 XP |
| 🌟 Scholar | Complete 50 lessons | +1000 XP |
| 💯 Perfect Score | 100% quiz score | +150 XP |

## 📊 Progress Tracking

### Progress Bars
```
▬▬▬▭▭▭  = 50% complete
▬▬▬▬▬▬  = 100% complete
▭▭▭▭▭▭  = 0% complete
```

### Lesson Status
- 📝 = Not started
- ✅ = Completed
- (95%) = Previous score

## 🌍 Available Languages

| Language | Level | Lessons |
|----------|-------|---------|
| 🇬🇧 English | Beginner | 2 lessons |
| 🇬🇧 English | Intermediate | 1 lesson |
| 🇯🇵 Japanese | Beginner | 1 lesson |
| 🇰🇷 Korean | Beginner | 1 lesson |

*More lessons coming soon!*

## 🔐 Admin Features

### Database Backup
```
/backup
```
- Creates timestamped backup
- Downloads .db file
- Stored in `backups/` folder

### Database Restore
```
/restore
```
- Reply with backup file
- Creates safety backup first
- Restores from uploaded file

## ❓ FAQ

**Q: How often do hearts refill?**
A: Every 4 hours, automatically.

**Q: Can I practice without hearts?**
A: No, you need at least 1 heart to take quizzes.

**Q: What happens if I miss a day?**
A: Your streak resets to 0, but XP remains.

**Q: Can I change languages?**
A: Yes, anytime via `/learn` → Select new language.

**Q: How do I turn off notifications?**
A: `/profile` → Click "🔔 Notifications" button.

**Q: Can I see other users' profiles?**
A: No, only leaderboard rankings visible.

## 🚨 Getting Help

1. Check this guide first
2. Review error messages carefully
3. Check bot logs for details
4. Verify `.env` configuration
5. Ensure database has write permissions

## 🎓 Best Practices

### For Learners
- ✅ Start with easier lessons
- ✅ Review vocabulary before quiz
- ✅ Practice daily for streaks
- ✅ Don't rush through questions
- ✅ Check leaderboard for motivation

### For Admins
- ✅ Backup database regularly
- ✅ Monitor bot logs
- ✅ Keep dependencies updated
- ✅ Test new lessons before adding
- ✅ Secure `.env` file

## 🔄 Updating the Bot

```bash
# Pull latest changes (if using git)
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart bot
# Stop current process (Ctrl+C)
python bot.py
```

## 🎉 Ready to Learn!

You're all set! Send `/start` to your bot and begin your language learning journey!

**Happy Learning! 🚀📚**
