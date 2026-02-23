# -*- coding: utf-8 -*-
"""
SUPER LEARNING BOT — Built-in Lesson Content
=============================================
Comprehensive lesson data for English, Korean, Japanese.
No API needed — everything is embedded.
"""

from typing import Dict, List, Optional, Tuple, Any

# ─────────────────────────────────────────
#  ENGLISH LESSONS
# ─────────────────────────────────────────
ENGLISH_LESSONS = {
    "A1": {
        "greetings": {
            "title": "👋 Greetings & Introductions",
            "vocab": [
                {"word": "Hello",       "meaning": "An expression of greeting",            "example": "Hello! How are you?"},
                {"word": "Good morning","meaning": "Greeting used in the morning",          "example": "Good morning, teacher!"},
                {"word": "Goodbye",     "meaning": "Expression when leaving",               "example": "Goodbye! See you tomorrow."},
                {"word": "Please",      "meaning": "Used to make polite requests",          "example": "Can you help me, please?"},
                {"word": "Thank you",   "meaning": "Expression of gratitude",               "example": "Thank you for your help!"},
                {"word": "Sorry",       "meaning": "Expression of apology",                 "example": "I'm sorry I'm late."},
                {"word": "Excuse me",   "meaning": "Used to get attention or apologize",    "example": "Excuse me, where is the bank?"},
                {"word": "My name is",  "meaning": "Used to introduce yourself",            "example": "My name is John. Nice to meet you!"},
            ],
            "grammar": {
                "rule": "Subject + am/is/are + complement",
                "example": "I am a student. She is a teacher. They are friends.",
                "tip": "💡 Use 'am' with I, 'is' with he/she/it, 'are' with you/we/they"
            },
            "quiz": [
                {"q": "Which is correct?", "opts": ["I are happy","I is happy","I am happy","I be happy"], "ans": 2},
                {"q": "How do you greet someone in the morning?", "opts": ["Good night","Good evening","Good morning","Good afternoon"], "ans": 2},
                {"q": "Fill in: She ___ a teacher.", "opts": ["am","is","are","be"], "ans": 1},
                {"q": "What does 'Excuse me' mean?", "opts": ["Thank you","Sorry to bother you","Goodbye","Hello"], "ans": 1},
                {"q": "Which is a greeting?", "opts": ["Goodbye","See you","Hello","All of the above"], "ans": 3},
            ]
        },
        "numbers": {
            "title": "🔢 Numbers & Counting",
            "vocab": [
                {"word": "One",    "meaning": "1",  "example": "I have one cat."},
                {"word": "Two",    "meaning": "2",  "example": "Two eyes, two ears."},
                {"word": "Three",  "meaning": "3",  "example": "Three friends came."},
                {"word": "Ten",    "meaning": "10", "example": "I have ten fingers."},
                {"word": "Hundred","meaning": "100","example": "One hundred dollars."},
                {"word": "First",  "meaning": "1st","example": "She finished first."},
                {"word": "Last",   "meaning": "Final","example": "This is the last one."},
            ],
            "grammar": {
                "rule": "Ordinal numbers: add -th to most numbers",
                "example": "1st (first), 2nd (second), 3rd (third), 4th (fourth)",
                "tip": "💡 Exceptions: first, second, third are irregular!"
            },
            "quiz": [
                {"q": "How do you say 7 in English?", "opts": ["Six","Eight","Seven","Five"], "ans": 2},
                {"q": "What comes after 'first'?", "opts": ["Third","Second","Fourth","Fifth"], "ans": 1},
                {"q": "7 + 3 = ?", "opts": ["Nine","Eleven","Ten","Eight"], "ans": 2},
                {"q": "Which is the ordinal of 3?", "opts": ["Threeth","Thirdly","Third","Three"], "ans": 2},
            ]
        },
        "colors": {
            "title": "🎨 Colors",
            "vocab": [
                {"word": "Red",    "meaning": "🔴 Red color",   "example": "The apple is red."},
                {"word": "Blue",   "meaning": "🔵 Blue color",  "example": "The sky is blue."},
                {"word": "Green",  "meaning": "🟢 Green color", "example": "Grass is green."},
                {"word": "Yellow", "meaning": "🟡 Yellow color","example": "The sun is yellow."},
                {"word": "White",  "meaning": "⬜ White color", "example": "Snow is white."},
                {"word": "Black",  "meaning": "⬛ Black color", "example": "The cat is black."},
            ],
            "grammar": {
                "rule": "Adjective placement: adjective + noun",
                "example": "A red car. The blue sky. Green trees.",
                "tip": "💡 In English, adjectives come BEFORE the noun."
            },
            "quiz": [
                {"q": "What color is the sky?", "opts": ["Red","Green","Blue","Yellow"], "ans": 2},
                {"q": "Which is correct?", "opts": ["A car red","Red a car","A car is red","The red car"], "ans": 3},
                {"q": "What color is grass?", "opts": ["Blue","Green","White","Red"], "ans": 1},
            ]
        },
    },
    "A2": {
        "daily_routine": {
            "title": "⏰ Daily Routine",
            "vocab": [
                {"word": "Wake up",    "meaning": "To stop sleeping",      "example": "I wake up at 7 AM."},
                {"word": "Breakfast",  "meaning": "Morning meal",          "example": "I eat breakfast every day."},
                {"word": "Commute",    "meaning": "Travel to work/school", "example": "My commute takes 30 minutes."},
                {"word": "Lunch",      "meaning": "Midday meal",           "example": "Let's have lunch together."},
                {"word": "Dinner",     "meaning": "Evening meal",          "example": "We have dinner at 7 PM."},
                {"word": "Sleep",      "meaning": "To rest at night",      "example": "I sleep 8 hours a night."},
                {"word": "Exercise",   "meaning": "Physical activity",     "example": "I exercise every morning."},
            ],
            "grammar": {
                "rule": "Simple Present Tense for routines",
                "example": "I wake up at 7. She goes to school. They eat dinner together.",
                "tip": "💡 Add -s/-es to verbs with he/she/it: go→goes, eat→eats"
            },
            "quiz": [
                {"q": "She ___ to school every day.", "opts": ["go","goes","going","went"], "ans": 1},
                {"q": "When do you have breakfast?", "opts": ["At night","In the morning","In the evening","At noon"], "ans": 1},
                {"q": "What is 'commute'?", "opts": ["Sleep","Travel to work","Eat","Exercise"], "ans": 1},
                {"q": "I ___ 8 hours a night.", "opts": ["sleeps","sleeping","sleep","slept"], "ans": 2},
                {"q": "Which is a daily routine word?", "opts": ["Mountain","Ocean","Wake up","Airplane"], "ans": 2},
            ]
        },
        "shopping": {
            "title": "🛒 Shopping",
            "vocab": [
                {"word": "Buy",     "meaning": "To purchase",         "example": "I want to buy a shirt."},
                {"word": "Sell",    "meaning": "To exchange for money","example": "They sell fresh fruits."},
                {"word": "Price",   "meaning": "The cost of something","example": "What is the price?"},
                {"word": "Cheap",   "meaning": "Low in price",         "example": "This is very cheap!"},
                {"word": "Expensive","meaning": "High in price",       "example": "That bag is expensive."},
                {"word": "Discount","meaning": "Reduction in price",   "example": "There's a 50% discount today!"},
                {"word": "Receipt", "meaning": "Proof of purchase",    "example": "Can I have a receipt?"},
            ],
            "grammar": {
                "rule": "How much / How many",
                "example": "How much is this? How many apples do you want?",
                "tip": "💡 'How much' for uncountable/price, 'How many' for countable things"
            },
            "quiz": [
                {"q": "How ___ is this dress?", "opts": ["many","much","lot","some"], "ans": 1},
                {"q": "The opposite of 'expensive' is:", "opts": ["Big","Cheap","Fast","New"], "ans": 1},
                {"q": "A 'discount' means:", "opts": ["Higher price","Same price","Lower price","No price"], "ans": 2},
            ]
        },
    },
}

# ─────────────────────────────────────────
#  KOREAN LESSONS
# ─────────────────────────────────────────
KOREAN_LESSONS = {
    "A1": {
        "hangul_basics": {
            "title": "🇰🇷 Hangul Basics (한글 기초)",
            "vocab": [
                {"word": "안녕하세요 (Annyeonghaseyo)", "meaning": "Hello (formal)",     "example": "안녕하세요! 저는 민준이에요."},
                {"word": "감사합니다 (Gamsahamnida)",  "meaning": "Thank you (formal)",  "example": "도와줘서 감사합니다."},
                {"word": "네 (Ne)",                   "meaning": "Yes",                  "example": "네, 알겠습니다."},
                {"word": "아니요 (Aniyo)",             "meaning": "No",                  "example": "아니요, 괜찮아요."},
                {"word": "죄송합니다 (Joesonghamnida)","meaning": "I'm sorry (formal)",  "example": "늦어서 죄송합니다."},
                {"word": "이름 (Ireum)",               "meaning": "Name",                "example": "이름이 뭐예요?"},
                {"word": "나라 (Nara)",                "meaning": "Country",              "example": "어느 나라 사람이에요?"},
            ],
            "grammar": {
                "rule": "저는 ~ 이에요/예요 (I am ~)",
                "example": "저는 학생이에요. (I am a student.) 저는 민준이에요. (I am Minjun.)",
                "tip": "💡 이에요 after consonant, 예요 after vowel"
            },
            "quiz": [
                {"q": "How do you say 'Hello' formally in Korean?", "opts": ["감사합니다","안녕하세요","죄송합니다","이름"], "ans": 1},
                {"q": "'네' means:", "opts": ["No","Maybe","Yes","Hello"], "ans": 2},
                {"q": "I am a student = 저는 학생___", "opts": ["이에요","예요","있어요","해요"], "ans": 0},
                {"q": "'감사합니다' means:", "opts": ["Sorry","Yes","Thank you","Goodbye"], "ans": 2},
                {"q": "How do you ask 'What is your name?'", "opts": ["어디에요?","이름이 뭐예요?","뭐 해요?","어때요?"], "ans": 1},
            ]
        },
    },
}

# ─────────────────────────────────────────
#  ALL LESSONS REGISTRY
# ─────────────────────────────────────────
ALL_LESSONS = {
    "english" : ENGLISH_LESSONS,
    "korean"  : KOREAN_LESSONS,
    "japanese": {}, # Placeholder
}

def get_lessons_for(lang: str, level: Optional[str] = None) -> Dict:
    lang_data = ALL_LESSONS.get(lang, ENGLISH_LESSONS)
    if level:
        return lang_data.get(level, {})
    return lang_data

def get_lesson(lang: str, level: str, key: str) -> Optional[Dict]:
    return ALL_LESSONS.get(lang, {}).get(level, {}).get(key)

def get_daily_lesson(lang: str, level: str, completed: List) -> Optional[Tuple[str, Dict]]:
    lang_data = ALL_LESSONS.get(lang, ENGLISH_LESSONS)
    level_data = lang_data.get(level, {})
    for key, lesson in level_data.items():
        if key not in completed:
            return key, lesson
    # All done — wrap around
    if level_data:
        first_key = list(level_data.keys())[0]
        return first_key, level_data[first_key]
    return None

def determine_level(correct: int, total: int) -> str:
    ratio = correct / total if total > 0 else 0
    if ratio >= 0.875: return "C2"
    if ratio >= 0.75:  return "C1"
    if ratio >= 0.625: return "B2"
    if ratio >= 0.5:   return "B1"
    if ratio >= 0.25:  return "A2"
    return "A1"

# ─────────────────────────────────────────
#  DAILY VOCAB (rotating)
# ─────────────────────────────────────────
DAILY_VOCAB = {
    "english": [
        {"word": "Perseverance", "meaning": "Continued effort despite difficulties", "example": "Her perseverance paid off in the end."},
        {"word": "Eloquent",     "meaning": "Fluent and persuasive in speaking",     "example": "He gave an eloquent speech."},
        {"word": "Resilient",    "meaning": "Able to recover quickly",                "example": "Children are very resilient."},
        {"word": "Endeavor",     "meaning": "To try hard to do something",           "example": "We will endeavor to improve."},
        {"word": "Ambiguous",    "meaning": "Having more than one possible meaning", "example": "His answer was ambiguous."},
        {"word": "Concise",      "meaning": "Brief but comprehensive",                "example": "Please be concise in your reply."},
        {"word": "Diligent",     "meaning": "Having steady effort and care",          "example": "She is a diligent student."},
    ],
}

def get_daily_words(lang: str, count: int = 5) -> List[Dict]:
    import datetime
    words = DAILY_VOCAB.get(lang, DAILY_VOCAB["english"])
    day   = datetime.date.today().day
    start = day % len(words)
    result = []
    for i in range(count):
        result.append(words[(start + i) % len(words)])
    return result
