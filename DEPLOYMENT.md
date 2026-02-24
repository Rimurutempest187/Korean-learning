# Deployment Guide

## 🚀 Production Deployment Options

### Option 1: VPS/Cloud Server (Recommended)

#### Providers
- **DigitalOcean** ($5-10/month)
- **Linode** ($5/month)
- **Vultr** ($5/month)
- **AWS EC2** (Free tier available)
- **Google Cloud** (Free tier available)

#### Setup on Ubuntu/Debian

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3.10+
sudo apt install python3.10 python3-pip git -y

# 3. Clone/Upload your bot
# Option A: Upload via SCP
scp -r language_learning_bot user@your-server-ip:/home/user/

# Option B: Git
git clone your-repository-url
cd language_learning_bot

# 4. Install dependencies
pip3 install -r requirements.txt

# 5. Configure environment
cp .env.example .env
nano .env
# Add your BOT_TOKEN and ADMIN_ID

# 6. Test run
python3 bot.py
# Press Ctrl+C to stop

# 7. Create systemd service for auto-start
sudo nano /etc/systemd/system/language-bot.service
```

**Service File Content:**
```ini
[Unit]
Description=Language Learning Telegram Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/language_learning_bot
ExecStart=/usr/bin/python3 /home/your-username/language_learning_bot/bot.py
Restart=always
RestartSec=10
StandardOutput=append:/home/your-username/language_learning_bot/bot.log
StandardError=append:/home/your-username/language_learning_bot/error.log

[Install]
WantedBy=multi-user.target
```

```bash
# 8. Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable language-bot
sudo systemctl start language-bot

# 9. Check status
sudo systemctl status language-bot

# 10. View logs
sudo journalctl -u language-bot -f
```

**Service Management Commands:**
```bash
# Start
sudo systemctl start language-bot

# Stop
sudo systemctl stop language-bot

# Restart
sudo systemctl restart language-bot

# Status
sudo systemctl status language-bot

# View logs
sudo journalctl -u language-bot -n 100 --no-pager
```

---

### Option 2: Docker Deployment

#### 1. Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p backups data

# Run bot
CMD ["python", "bot.py"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  language-bot:
    build: .
    container_name: language_learning_bot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./language_bot.db:/app/language_bot.db
      - ./backups:/app/backups
      - ./data:/app/data
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

#### 3. Deploy

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

---

### Option 3: Heroku Deployment

#### 1. Prepare Files

Create `Procfile`:
```
worker: python bot.py
```

Create `runtime.txt`:
```
python-3.10.12
```

#### 2. Deploy

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-language-bot

# Set config vars
heroku config:set BOT_TOKEN=your_token
heroku config:set ADMIN_ID=your_id

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Scale worker
heroku ps:scale worker=1

# View logs
heroku logs --tail
```

---

### Option 4: Railway.app

1. Visit [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Add environment variables:
   - `BOT_TOKEN`
   - `ADMIN_ID`
5. Deploy automatically

---

### Option 5: Render.com

1. Visit [render.com](https://render.com)
2. Click "New" → "Background Worker"
3. Connect repository
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
5. Add environment variables
6. Deploy

---

## 🔒 Security Best Practices

### 1. Environment Variables
```bash
# Never commit .env file
echo ".env" >> .gitignore

# Use strong admin ID
# Don't share bot token
```

### 2. File Permissions
```bash
# Restrict .env access
chmod 600 .env

# Database permissions
chmod 644 language_bot.db
```

### 3. Firewall (VPS)
```bash
# Allow only necessary ports
sudo ufw allow 22/tcp  # SSH
sudo ufw enable
```

### 4. Regular Updates
```bash
# Update dependencies regularly
pip install -r requirements.txt --upgrade

# Update system packages
sudo apt update && sudo apt upgrade
```

---

## 📊 Monitoring

### 1. Log Management

**Using systemd (Linux):**
```bash
# View recent logs
sudo journalctl -u language-bot -n 100

# Follow logs in real-time
sudo journalctl -u language-bot -f

# Logs from today
sudo journalctl -u language-bot --since today
```

**Using Docker:**
```bash
# View logs
docker-compose logs -f language-bot

# Last 100 lines
docker-compose logs --tail=100 language-bot
```

### 2. Database Backup Automation

Create backup script `backup.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp language_bot.db backups/auto_backup_$DATE.db
# Keep only last 7 backups
ls -t backups/auto_backup_*.db | tail -n +8 | xargs -r rm
```

Add to crontab:
```bash
# Edit crontab
crontab -e

# Add daily backup at 3 AM
0 3 * * * /path/to/language_learning_bot/backup.sh
```

### 3. Health Checks

Create `health_check.py`:
```python
import asyncio
import aiosqlite

async def check_health():
    try:
        db = await aiosqlite.connect('language_bot.db')
        cursor = await db.execute('SELECT COUNT(*) FROM users')
        result = await cursor.fetchone()
        await db.close()
        print(f"✅ Database OK - {result[0]} users")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(check_health())
```

---

## 🔄 Update Procedure

### For VPS/Server:

```bash
# 1. Stop bot
sudo systemctl stop language-bot

# 2. Backup database
cp language_bot.db backups/before_update_$(date +%Y%m%d).db

# 3. Pull changes (if using git)
git pull

# Or upload new files via SCP

# 4. Update dependencies
pip3 install -r requirements.txt --upgrade

# 5. Test configuration
python3 test_bot.py

# 6. Restart bot
sudo systemctl start language-bot

# 7. Check status
sudo systemctl status language-bot
```

### For Docker:

```bash
# 1. Backup
docker-compose exec language-bot cp language_bot.db backups/before_update.db

# 2. Update code

# 3. Rebuild and restart
docker-compose up -d --build

# 4. Check logs
docker-compose logs -f
```

---

## 🐛 Troubleshooting Production Issues

### Bot Not Starting

```bash
# Check service status
sudo systemctl status language-bot

# View error logs
sudo journalctl -u language-bot -n 50

# Check if port is in use
sudo lsof -i -P -n | grep python

# Verify Python version
python3 --version
```

### High Memory Usage

```bash
# Monitor resources
htop

# Check bot process
ps aux | grep bot.py

# Restart if needed
sudo systemctl restart language-bot
```

### Database Locked

```bash
# Check for zombie processes
ps aux | grep python

# Kill if necessary
sudo pkill -f bot.py

# Restart cleanly
sudo systemctl start language-bot
```

---

## 📈 Scaling Considerations

### When to Scale:
- \>1000 active users
- High response latency
- Database queries slow

### Scaling Options:
1. **Vertical Scaling:** Upgrade server resources
2. **Database Optimization:** Add indexes, optimize queries
3. **Caching:** Implement Redis for sessions
4. **Load Balancing:** Multiple bot instances (advanced)

---

## 🎯 Production Checklist

- [ ] `.env` file configured
- [ ] BOT_TOKEN set correctly
- [ ] ADMIN_ID verified
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Backup system configured
- [ ] Service/container running
- [ ] Logs accessible
- [ ] Health checks working
- [ ] SSL/TLS configured (if using webhooks)
- [ ] Monitoring in place
- [ ] Documentation updated

---

## 📞 Support & Maintenance

### Regular Tasks:
- **Daily:** Check logs for errors
- **Weekly:** Review user growth, backup database
- **Monthly:** Update dependencies, optimize database
- **Quarterly:** Security audit, performance review

### Emergency Contacts:
- Have backup admin access
- Document recovery procedures
- Keep offline backup of database

---

## 🎓 Additional Resources

- [python-telegram-bot Docs](https://docs.python-telegram-bot.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Linux Server Management](https://www.digitalocean.com/community/tutorials)
- [Docker Documentation](https://docs.docker.com/)

---

**Ready for Production! 🚀**
