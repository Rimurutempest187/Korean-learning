#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for SUPER LEARNING BOT
Run this to verify installation
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import telegram
        print("✅ python-telegram-bot")
    except ImportError:
        print("❌ python-telegram-bot not installed")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow")
    except ImportError:
        print("❌ Pillow not installed")
        return False
    
    try:
        import matplotlib
        print("✅ matplotlib")
    except ImportError:
        print("❌ matplotlib not installed")
        return False
    
    try:
        from gtts import gTTS
        print("✅ gTTS")
    except ImportError:
        print("❌ gTTS not installed")
        return False
    
    try:
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        print("✅ APScheduler")
    except ImportError:
        print("❌ APScheduler not installed")
        return False
    
    try:
        import openai
        print("✅ openai")
    except ImportError:
        print("⚠️  openai not installed (optional)")
    
    return True

def test_env():
    """Test if .env file exists and has required values"""
    print("\n🔧 Testing environment configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Please copy .env.example to .env and configure it")
        return False
    
    print("✅ .env file exists")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token or token == 'your_telegram_bot_token_here':
        print("❌ TELEGRAM_BOT_TOKEN not configured")
        return False
    
    print("✅ TELEGRAM_BOT_TOKEN configured")
    
    return True

def test_database():
    """Test database initialization"""
    print("\n💾 Testing database...")
    
    try:
        from database import Database
        db = Database()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("SUPER LEARNING BOT - Installation Test")
    print("Create by: PINLON-YOUTH")
    print("=" * 50)
    print()
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
        print("\n❌ Some dependencies are missing")
        print("   Run: pip install -r requirements.txt")
    
    # Test environment
    if not test_env():
        all_passed = False
    
    # Test database
    if not test_database():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed!")
        print("🚀 You can now run: python bot.py")
    else:
        print("❌ Some tests failed")
        print("📋 Please fix the issues above and try again")
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
