"""
Lesson Manager - Handles lesson content and structure
"""
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class LessonManager:
    """Manages lesson content and progression"""
    
    def __init__(self, lessons_path: str = "data/lessons.json"):
        self.lessons_path = lessons_path
        self.lessons_data: Dict[str, Any] = {}
        self.load_lessons()
    
    def load_lessons(self):
        """Load lessons from JSON file"""
        try:
            lessons_file = Path(self.lessons_path)
            if lessons_file.exists():
                with open(lessons_file, 'r', encoding='utf-8') as f:
                    self.lessons_data = json.load(f)
                logger.info(f"✅ Loaded lessons from {self.lessons_path}")
            else:
                logger.warning(f"⚠️ Lessons file not found: {self.lessons_path}")
                self.lessons_data = self._get_default_lessons()
        except Exception as e:
            logger.error(f"❌ Error loading lessons: {e}")
            self.lessons_data = self._get_default_lessons()
    
    def get_units(self, language: str) -> List[str]:
        """Get available units for a language"""
        if language in self.lessons_data:
            return list(self.lessons_data[language].keys())
        return []
    
    def get_lessons(self, language: str, unit: str) -> List[Dict[str, Any]]:
        """Get lessons for a specific unit"""
        if language in self.lessons_data and unit in self.lessons_data[language]:
            return self.lessons_data[language][unit]
        return []
    
    def get_lesson(self, language: str, unit: str, lesson_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific lesson"""
        lessons = self.get_lessons(language, unit)
        for lesson in lessons:
            if lesson['id'] == lesson_id:
                return lesson
        return None
    
    def get_quiz_questions(self, language: str, unit: str, lesson_id: str) -> List[Dict[str, Any]]:
        """Get quiz questions for a lesson"""
        lesson = self.get_lesson(language, unit, lesson_id)
        if lesson and 'quiz' in lesson:
            return lesson['quiz']
        return []
    
    @staticmethod
    def _get_default_lessons() -> Dict[str, Any]:
        """Return default lesson structure"""
        return {
            "english": {
                "beginner": [
                    {
                        "id": "eng_b_01",
                        "title": "Greetings & Basics",
                        "description": "Learn essential greetings",
                        "vocabulary": [
                            {"word": "Hello", "translation": "မင်္ဂလာပါ", "pronunciation": "mingalarpar"},
                            {"word": "Thank you", "translation": "ကျေးဇူးတင်ပါတယ်", "pronunciation": "kyay zu tin ba deh"},
                            {"word": "Goodbye", "translation": "သွားတော့မယ်", "pronunciation": "thwa daw meh"}
                        ],
                        "quiz": [
                            {
                                "question": "How do you say 'Hello' in Myanmar?",
                                "options": ["မင်္ဂလာပါ", "ကျေးဇူးတင်ပါတယ်", "သွားတော့မယ်", "နေကောင်းလား"],
                                "correct": 0,
                                "type": "multiple_choice"
                            },
                            {
                                "question": "Translate: Thank you",
                                "answer": "ကျေးဇူးတင်ပါတယ်",
                                "type": "text_input"
                            }
                        ]
                    }
                ],
                "intermediate": [],
                "advanced": []
            },
            "japanese": {
                "beginner": [
                    {
                        "id": "jpn_b_01",
                        "title": "Hiragana Basics",
                        "description": "Learn basic Hiragana characters",
                        "vocabulary": [
                            {"word": "こんにちは", "furigana": "こんにちは", "translation": "မင်္ဂလာပါ", "pronunciation": "konnichiwa"},
                            {"word": "ありがとう", "furigana": "ありがとう", "translation": "ကျေးဇူးတin်ပါတယ်", "pronunciation": "arigatou"},
                            {"word": "さようなら", "furigana": "さようなら", "translation": "သွားတော့မယ်", "pronunciation": "sayounara"}
                        ],
                        "quiz": [
                            {
                                "question": "What does こんにちは mean?",
                                "options": ["Hello", "Thank you", "Goodbye", "Good night"],
                                "correct": 0,
                                "type": "multiple_choice"
                            }
                        ]
                    }
                ],
                "intermediate": [],
                "advanced": []
            },
            "korean": {
                "beginner": [
                    {
                        "id": "kor_b_01",
                        "title": "Hangeul Introduction",
                        "description": "Learn basic Korean alphabet",
                        "vocabulary": [
                            {"word": "안녕하세요", "romanization": "annyeonghaseyo", "translation": "မင်္ဂလာပါ", "pronunciation": "annyeonghaseyo"},
                            {"word": "감사합니다", "romanization": "gamsahamnida", "translation": "ကျေးဇူးတင်ပါတယ်", "pronunciation": "gamsahamnida"},
                            {"word": "안녕히 가세요", "romanization": "annyeonghi gaseyo", "translation": "သွားတော့မယ်", "pronunciation": "annyeonghi gaseyo"}
                        ],
                        "quiz": [
                            {
                                "question": "How do you say 'Hello' in Korean?",
                                "options": ["안녕하세요", "감사합니다", "안녕히 가세요", "좋은 아침"],
                                "correct": 0,
                                "type": "multiple_choice"
                            }
                        ]
                    }
                ],
                "intermediate": [],
                "advanced": []
            }
        }
