# SUPER LEARNING BOT - Installation & Usage Guide

## 🚀 Quick Start Guide

### Step 1: Get Your Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Get OpenAI API Key (Optional)

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create new API key
5. Copy the key (starts with `sk-`)

### Step 3: Installation

#### On Linux/Mac:

```bash
# Navigate to bot directory
cd super_learning_bot

# Make run script executable
chmod +x run.sh

# Run setup and start bot
./run.sh
```

#### On Windows:

```cmd
# Navigate to bot directory
cd super_learning_bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env file with your tokens
notepad .env

# Run the bot
python bot.py
```

### Step 4: Configure Environment

Edit `.env` file:

```env
# Required: Your bot token from @BotFather
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Optional: OpenAI API key for AI Tutor features
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Your Telegram User ID (get from @userinfobot)
ADMIN_USER_IDS=123456789

# Timezone (adjust to your location)
TIMEZONE=Asia/Yangon

# Reminder times (24-hour format)
DAILY_REMINDER_TIME=09:00
EVENING_REMINDER_TIME=19:00
```

### Step 5: Find Your User ID

1. Open Telegram
2. Search for **@userinfobot**
3. Send `/start`
4. Bot will reply with your user ID
5. Add this ID to `ADMIN_USER_IDS` in `.env`

### Step 6: Run the Bot

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows

# Run the bot
python bot.py
```

You should see:
```
🚀 SUPER LEARNING BOT is starting...
```

### Step 7: Test the Bot

1. Open Telegram
2. Search for your bot (the username you chose)
3. Send `/start` command
4. Follow the onboarding process

## 📋 Requirements

- **Python**: 3.9 or higher
- **RAM**: Minimum 512 MB
- **Storage**: 100 MB free space
- **Internet**: Stable connection required

## 🔧 Troubleshooting

### Bot doesn't respond

**Problem**: Bot token is incorrect
**Solution**: 
1. Double-check token in `.env`
2. Make sure no extra spaces
3. Get new token from @BotFather if needed

### "Module not found" errors

**Problem**: Dependencies not installed
**Solution**:
```bash
pip install -r requirements.txt
```

### AI Tutor not working

**Problem**: OpenAI API key missing or invalid
**Solution**:
1. Add valid API key to `.env`
2. Check API key has credits
3. AI Tutor is optional - bot works without it

### Database errors

**Problem**: Permission issues
**Solution**:
```bash
chmod 666 superlearning.db
```

### Bot stops after closing terminal

**Solution**: Run in background
```bash
nohup python bot.py > bot.log 2>&1 &
```

## 🌐 Deployment Options

### Option 1: Local Computer
- Easy setup
- Free
- Must keep computer running
- Good for testing

### Option 2: VPS (Recommended)
- Always online
- Better performance
- Small monthly cost
- Professional solution

Recommended VPS providers:
- DigitalOcean
- Linode
- Vultr
- AWS EC2

### Option 3: PythonAnywhere
- Free tier available
- Easy deployment
- Limited features on free plan

### Option 4: Heroku
- Free tier (with limits)
- Easy deployment
- Auto-scaling

## 📊 Monitoring

Check bot logs:
```bash
tail -f bot.log
```

Check bot status:
```bash
ps aux | grep bot.py
```

Stop bot:
```bash
pkill -f bot.py
```

## 🔄 Updating

```bash
# Stop the bot
pkill -f bot.py

# Pull latest changes
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart bot
python bot.py
```

## 💾 Backup

Backup your database regularly:

```bash
# Backup database
cp superlearning.db superlearning.db.backup

# Or automated backup
crontab -e
# Add: 0 0 * * * cp /path/to/superlearning.db /path/to/backup/$(date +\%Y\%m\%d)_superlearning.db
```

## 🔒 Security Tips

1. **Never share your bot token**
2. **Keep `.env` file private** (don't commit to git)
3. **Use strong API keys**
4. **Regular backups**
5. **Update dependencies regularly**
6. **Monitor bot logs**

## 📈 Performance Tips

1. **Use database indexes** for faster queries
2. **Cache frequently used data**
3. **Limit message size** to avoid Telegram limits
4. **Use async operations** for better performance
5. **Monitor memory usage**

## 🎨 Customization

### Change Bot Appearance

Edit `bot.py` to customize:
- Welcome messages
- Menu buttons
- Response texts
- Emojis

### Add New Languages

1. Add to `AVAILABLE_LANGUAGES` in `bot.py`
2. Add sample content in `content_manager.py`
3. Update AI prompts in `ai_tutor.py`

### Modify Gamification

Edit `gamification.py` to:
- Change XP amounts
- Add new badges
- Modify level requirements

### Customize Reminders

Edit `scheduler.py` to:
- Change reminder times
- Modify message content
- Add new scheduled tasks

## 📞 Support

Need help? 

1. Check README.md
2. Review this installation guide
3. Check error logs
4. Search for similar issues
5. Contact support

## ✅ Checklist

Before launching:

- [ ] Python 3.9+ installed
- [ ] Dependencies installed
- [ ] Bot token configured
- [ ] OpenAI key added (optional)
- [ ] Admin user ID set
- [ ] Timezone configured
- [ ] Database created
- [ ] Bot tested with `/start`
- [ ] All features working
- [ ] Backup system in place

## 🎉 You're Ready!

Your SUPER LEARNING BOT is now ready to help users learn languages!

**Create by: PINLON-YOUTH**

---

For more information, see README.md
