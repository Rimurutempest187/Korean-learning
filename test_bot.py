"""
Test Script for Language Learning Bot
Run this to verify all components are working
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from managers.database_manager import DatabaseManager
from managers.user_manager import UserManager
from managers.lesson_manager import LessonManager


class BotTester:
    """Test bot components"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.config = Config()
    
    def test(self, name: str, condition: bool, error_msg: str = ""):
        """Test a condition"""
        if condition:
            print(f"✅ {name}")
            self.passed += 1
        else:
            print(f"❌ {name}")
            if error_msg:
                print(f"   Error: {error_msg}")
            self.failed += 1
    
    async def run_tests(self):
        """Run all tests"""
        print("\n🧪 Testing Language Learning Bot Components\n")
        print("=" * 50)
        
        # Test 1: Configuration
        print("\n1️⃣ Testing Configuration...")
        try:
            self.test(
                "BOT_TOKEN exists",
                bool(self.config.BOT_TOKEN),
                "Set BOT_TOKEN in .env file"
            )
            self.test(
                "ADMIN_ID exists",
                self.config.ADMIN_ID > 0,
                "Set ADMIN_ID in .env file"
            )
            self.test(
                "Languages configured",
                len(self.config.LANGUAGES) == 3,
                "Should have 3 languages"
            )
        except Exception as e:
            print(f"❌ Configuration error: {e}")
            self.failed += 1
        
        # Test 2: Database
        print("\n2️⃣ Testing Database...")
        try:
            db = DatabaseManager("test_bot.db")
            await db.initialize()
            self.test("Database initialized", True)
            
            # Test query
            result = await db.fetch_one("SELECT 1 as test")
            self.test("Database queries work", result['test'] == 1)
            
            await db.close()
            
            # Cleanup
            if os.path.exists("test_bot.db"):
                os.remove("test_bot.db")
                self.test("Database cleanup", True)
        except Exception as e:
            print(f"❌ Database error: {e}")
            self.failed += 1
        
        # Test 3: User Manager
        print("\n3️⃣ Testing User Manager...")
        try:
            db = DatabaseManager("test_bot.db")
            await db.initialize()
            user_manager = UserManager(db)
            
            # Create test user
            user = await user_manager.get_or_create_user(12345, "testuser", "Test")
            self.test("User creation", user['user_id'] == 12345)
            self.test("Default hearts", user['hearts'] == 5)
            self.test("Default XP", user['xp'] == 0)
            
            # Test XP addition
            new_xp = await user_manager.add_xp(12345, 100)
            self.test("Add XP", new_xp == 100)
            
            # Test heart loss
            hearts = await user_manager.lose_heart(12345)
            self.test("Lose heart", hearts == 4)
            
            await db.close()
            os.remove("test_bot.db")
        except Exception as e:
            print(f"❌ User Manager error: {e}")
            self.failed += 1
        
        # Test 4: Lesson Manager
        print("\n4️⃣ Testing Lesson Manager...")
        try:
            lesson_manager = LessonManager()
            
            # Test lesson loading
            self.test("Lessons loaded", bool(lesson_manager.lessons_data))
            
            # Test English lessons
            eng_units = lesson_manager.get_units("english")
            self.test("English units exist", len(eng_units) > 0)
            
            eng_beginner = lesson_manager.get_lessons("english", "beginner")
            self.test("English beginner lessons exist", len(eng_beginner) > 0)
            
            # Test lesson retrieval
            lesson = lesson_manager.get_lesson("english", "beginner", "eng_b_01")
            self.test("Get specific lesson", lesson is not None)
            self.test("Lesson has vocabulary", 'vocabulary' in lesson)
            self.test("Lesson has quiz", 'quiz' in lesson)
            
            # Test quiz questions
            quiz = lesson_manager.get_quiz_questions("english", "beginner", "eng_b_01")
            self.test("Quiz questions exist", len(quiz) > 0)
            
        except Exception as e:
            print(f"❌ Lesson Manager error: {e}")
            self.failed += 1
        
        # Test 5: File Structure
        print("\n5️⃣ Testing File Structure...")
        required_files = [
            "bot.py",
            "config.py",
            "requirements.txt",
            "README.md",
            ".env.example",
            "data/lessons.json",
            "managers/database_manager.py",
            "managers/user_manager.py",
            "managers/lesson_manager.py",
            "handlers/start_handler.py",
            "handlers/lesson_handler.py",
            "handlers/quiz_handler.py",
            "utils/formatter.py",
            "utils/error_handler.py"
        ]
        
        for file in required_files:
            exists = os.path.exists(file)
            self.test(f"File exists: {file}", exists)
        
        # Test 6: Utilities
        print("\n6️⃣ Testing Utilities...")
        try:
            from utils.formatter import (
                escape_markdown,
                create_progress_bar,
                format_duration,
                truncate_text
            )
            
            # Test escape_markdown
            text = "Hello_World*Test"
            escaped = escape_markdown(text)
            self.test("Markdown escaping", "\\" in escaped)
            
            # Test progress bar
            progress = create_progress_bar(3, 6)
            self.test("Progress bar", len(progress) == 6)
            self.test("Progress bar content", "▬" in progress and "▭" in progress)
            
            # Test duration formatting
            duration = format_duration(3700)
            self.test("Duration formatting", "1h" in duration)
            
            # Test text truncation
            long_text = "A" * 200
            truncated = truncate_text(long_text, 100)
            self.test("Text truncation", len(truncated) <= 100)
            
        except Exception as e:
            print(f"❌ Utilities error: {e}")
            self.failed += 1
        
        # Results
        print("\n" + "=" * 50)
        print("\n📊 Test Results:")
        print(f"   ✅ Passed: {self.passed}")
        print(f"   ❌ Failed: {self.failed}")
        print(f"   📈 Success Rate: {(self.passed/(self.passed+self.failed)*100):.1f}%")
        
        if self.failed == 0:
            print("\n🎉 All tests passed! Bot is ready to run.")
            print("   Run: python bot.py")
        else:
            print("\n⚠️  Some tests failed. Please fix issues before running.")
        
        print("\n" + "=" * 50 + "\n")


async def main():
    """Run tests"""
    tester = BotTester()
    await tester.run_tests()


if __name__ == "__main__":
    asyncio.run(main())
