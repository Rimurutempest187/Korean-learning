"""
SUPER LEARNING BOT — Built-in Lesson Content
=============================================
Comprehensive lesson data for English, Korean, Japanese.
No API needed — everything is embedded.
"""

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
    "B1": {
        "travel": {
            "title": "✈️ Travel & Transportation",
            "vocab": [
                {"word": "Departure",  "meaning": "The act of leaving",          "example": "Departure time is 9 AM."},
                {"word": "Arrival",    "meaning": "The act of reaching",          "example": "Arrival is at 2 PM."},
                {"word": "Passport",   "meaning": "ID document for travel",       "example": "Don't forget your passport!"},
                {"word": "Boarding",   "meaning": "Getting on a plane/bus",       "example": "Boarding starts in 20 minutes."},
                {"word": "Itinerary",  "meaning": "Planned travel schedule",      "example": "Here is our travel itinerary."},
                {"word": "Currency",   "meaning": "Money used in a country",      "example": "What currency do they use?"},
                {"word": "Accommodation","meaning": "A place to stay",            "example": "We need to book accommodation."},
            ],
            "grammar": {
                "rule": "Future tense: will / going to",
                "example": "I will fly to Japan next week. I'm going to book a hotel.",
                "tip": "💡 'will' for spontaneous decisions, 'going to' for planned actions"
            },
            "quiz": [
                {"q": "I ___ book a hotel tomorrow. (planned)", "opts": ["will","am going to","was","had"], "ans": 1},
                {"q": "What is an 'itinerary'?", "opts": ["A hotel","A travel plan","A passport","A ticket"], "ans": 1},
                {"q": "Where do you show your passport?", "opts": ["Restaurant","School","Airport","Gym"], "ans": 2},
                {"q": "The plane ___ at 3 PM.", "opts": ["arrive","arriving","arrives","will arrive"], "ans": 3},
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
                {"word": "네 (Ne)",                   "meaning": "Yes",                 "example": "네, 알겠습니다."},
                {"word": "아니요 (Aniyo)",             "meaning": "No",                  "example": "아니요, 괜찮아요."},
                {"word": "죄송합니다 (Joesonghamnida)","meaning": "I'm sorry (formal)",  "example": "늦어서 죄송합니다."},
                {"word": "이름 (Ireum)",               "meaning": "Name",                "example": "이름이 뭐예요?"},
                {"word": "나라 (Nara)",                "meaning": "Country",             "example": "어느 나라 사람이에요?"},
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
        "numbers_kr": {
            "title": "🔢 Korean Numbers (숫자)",
            "vocab": [
                {"word": "일 (Il)",   "meaning": "1 (Sino-Korean)", "example": "일 층 (1st floor)"},
                {"word": "이 (I)",    "meaning": "2 (Sino-Korean)", "example": "이 월 (February)"},
                {"word": "삼 (Sam)", "meaning": "3 (Sino-Korean)", "example": "삼 일 (3 days)"},
                {"word": "하나",      "meaning": "1 (Native Korean)","example": "하나, 둘, 셋..."},
                {"word": "둘",        "meaning": "2 (Native Korean)","example": "사과 둘 (2 apples)"},
                {"word": "셋",        "meaning": "3 (Native Korean)","example": "세 시 (3 o'clock)"},
                {"word": "열",        "meaning": "10 (Native Korean)","example": "열 살 (10 years old)"},
            ],
            "grammar": {
                "rule": "Korean has TWO number systems",
                "example": "Sino-Korean: 1=일,2=이,3=삼 (dates, money, phone)\nNative Korean: 1=하나,2=둘,3=셋 (counting items, age)",
                "tip": "💡 Use Native Korean for counting objects and age!"
            },
            "quiz": [
                {"q": "How do you say '3' in Sino-Korean?", "opts": ["셋","삼","세","셋"], "ans": 1},
                {"q": "Which number system is used for age?", "opts": ["Sino-Korean","Native Korean","Both","Neither"], "ans": 1},
                {"q": "'둘' means:", "opts": ["1","3","2","4"], "ans": 2},
            ]
        },
    },
    "A2": {
        "food": {
            "title": "🍜 Korean Food (음식)",
            "vocab": [
                {"word": "밥 (Bap)",       "meaning": "Rice / meal",    "example": "밥 먹었어요? (Did you eat?)"},
                {"word": "물 (Mul)",        "meaning": "Water",          "example": "물 한 잔 주세요."},
                {"word": "맛있어요",         "meaning": "Delicious",      "example": "이 김치 정말 맛있어요!"},
                {"word": "맵다 (Maepda)",   "meaning": "Spicy",          "example": "이 음식은 너무 매워요."},
                {"word": "달다 (Dalda)",    "meaning": "Sweet",          "example": "이 케이크는 달아요."},
                {"word": "식당 (Sikdang)", "meaning": "Restaurant",     "example": "근처에 식당이 있어요?"},
                {"word": "메뉴 (Menyu)",   "meaning": "Menu",           "example": "메뉴 좀 주세요."},
            ],
            "grammar": {
                "rule": "주세요 (juseyo) = Please give me",
                "example": "물 주세요 (Please give me water)\n메뉴 주세요 (Please give me the menu)",
                "tip": "💡 Noun + 주세요 is one of the most useful restaurant phrases!"
            },
            "quiz": [
                {"q": "'맛있어요' means:", "opts": ["Spicy","Delicious","Sweet","Hot"], "ans": 1},
                {"q": "How to say 'Please give me water'?", "opts": ["물 먹어요","물 주세요","물 가요","물 있어요"], "ans": 1},
                {"q": "'식당' means:", "opts": ["Market","Restaurant","Hotel","School"], "ans": 1},
            ]
        },
    },
}

# ─────────────────────────────────────────
#  JAPANESE LESSONS
# ─────────────────────────────────────────
JAPANESE_LESSONS = {
    "A1": {
        "hiragana": {
            "title": "🇯🇵 Japanese Greetings (挨拶)",
            "vocab": [
                {"word": "おはようございます",  "meaning": "Good morning (formal)",  "example": "おはようございます！元気ですか？"},
                {"word": "こんにちは",          "meaning": "Hello / Good afternoon", "example": "こんにちは！いい天気ですね。"},
                {"word": "こんばんは",          "meaning": "Good evening",           "example": "こんばんは！今日はどうでしたか？"},
                {"word": "ありがとうございます", "meaning": "Thank you (formal)",     "example": "助けてくれてありがとうございます。"},
                {"word": "すみません",          "meaning": "Excuse me / Sorry",      "example": "すみません、駅はどこですか？"},
                {"word": "はい",               "meaning": "Yes",                    "example": "はい、わかりました。"},
                {"word": "いいえ",             "meaning": "No",                     "example": "いいえ、違います。"},
                {"word": "わたしは ~ です",     "meaning": "I am ~",                 "example": "わたしはアリです。"},
            ],
            "grammar": {
                "rule": "～は ～ です (X wa Y desu = X is Y)",
                "example": "わたしは学生です。(I am a student.)\nこれは本です。(This is a book.)",
                "tip": "💡 は (wa) marks the topic, です (desu) is like 'am/is/are'"
            },
            "quiz": [
                {"q": "How do you say 'Hello' in Japanese?", "opts": ["ありがとう","おはよう","こんにちは","さようなら"], "ans": 2},
                {"q": "'はい' means:", "opts": ["No","Maybe","Yes","Please"], "ans": 2},
                {"q": "I am a student = わたしは学生___", "opts": ["は","が","です","を"], "ans": 2},
                {"q": "'すみません' is used to:", "opts": ["Say goodbye","Say thank you","Get attention","Say yes"], "ans": 2},
                {"q": "Good morning (formal) in Japanese:", "opts": ["こんにちは","こんばんは","おはようございます","さようなら"], "ans": 2},
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
    "japanese": JAPANESE_LESSONS,
}

def get_lessons_for(lang: str, level: str = None) -> dict:
    lang_data = ALL_LESSONS.get(lang, ENGLISH_LESSONS)
    if level:
        return lang_data.get(level, {})
    return lang_data

def get_lesson(lang: str, level: str, key: str) -> dict | None:
    return ALL_LESSONS.get(lang, {}).get(level, {}).get(key)

def get_daily_lesson(lang: str, level: str, completed: list) -> tuple[str, dict] | None:
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

# ─────────────────────────────────────────
#  ROLEPLAY SCENARIOS
# ─────────────────────────────────────────
ROLEPLAY_SCENARIOS = {
    "restaurant": {
        "title": "🍽️ At a Restaurant",
        "context": "You are a customer at a restaurant.",
        "prompts": [
            "Bot (Waiter): Welcome! Do you have a reservation?",
            "Bot (Waiter): What would you like to order?",
            "Bot (Waiter): How would you like your steak cooked?",
            "Bot (Waiter): Would you like dessert?",
            "Bot (Waiter): Here is your bill. That will be $25.",
        ],
        "vocab": ["reservation", "menu", "order", "bill", "waiter", "chef", "appetizer", "dessert"],
    },
    "airport": {
        "title": "✈️ At the Airport",
        "context": "You are checking in at the airport.",
        "prompts": [
            "Bot (Staff): Good morning! May I see your passport?",
            "Bot (Staff): How many bags are you checking in?",
            "Bot (Staff): Do you have any liquids in your carry-on?",
            "Bot (Staff): Your boarding gate is B12. Have a safe flight!",
        ],
        "vocab": ["passport", "boarding pass", "gate", "departure", "carry-on", "check-in", "customs"],
    },
    "job_interview": {
        "title": "💼 Job Interview",
        "context": "You are being interviewed for a job.",
        "prompts": [
            "Bot (Interviewer): Tell me about yourself.",
            "Bot (Interviewer): Why do you want this position?",
            "Bot (Interviewer): What are your greatest strengths?",
            "Bot (Interviewer): Where do you see yourself in 5 years?",
            "Bot (Interviewer): Do you have any questions for us?",
        ],
        "vocab": ["experience", "qualifications", "skills", "team player", "initiative", "responsibilities"],
    },
    "hotel": {
        "title": "🏨 At the Hotel",
        "context": "You are checking in at a hotel.",
        "prompts": [
            "Bot (Receptionist): Good evening! Do you have a booking?",
            "Bot (Receptionist): How many nights will you be staying?",
            "Bot (Receptionist): Would you like a king or twin room?",
            "Bot (Receptionist): Breakfast is served from 7-10 AM.",
        ],
        "vocab": ["reservation", "check-in", "check-out", "room service", "key card", "lobby", "concierge"],
    },
}

# ─────────────────────────────────────────
#  LEVEL TEST QUESTIONS
# ─────────────────────────────────────────
LEVEL_TEST = {
    "english": [
        {"q": "What is the capital of England?",         "opts": ["Paris","London","Berlin","Rome"],     "ans": 1, "level": "A1"},
        {"q": "She ___ to school every day.",             "opts": ["go","goes","going","went"],           "ans": 1, "level": "A1"},
        {"q": "Choose the correct sentence:",            "opts": ["I am go school","I go to school","I going school","I goes school"], "ans": 1, "level": "A2"},
        {"q": "Which sentence uses Past Simple?",        "opts": ["I eat breakfast","I will eat","I ate breakfast","I am eating"], "ans": 2, "level": "A2"},
        {"q": "By the time she arrived, he ___ left.",   "opts": ["has","had","have","will have"],        "ans": 1, "level": "B1"},
        {"q": "The report ___ submitted by Friday.",     "opts": ["must","should be","must be","has"],    "ans": 2, "level": "B2"},
        {"q": "Hardly ___ he sat down when the phone rang.", "opts": ["had","did","was","has"],           "ans": 0, "level": "C1"},
        {"q": "The phenomenon ___ considerable debate.", "opts": ["has elicit","has elicited","eliciting","have elicited"], "ans": 1, "level": "C2"},
    ]
}

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
        {"word": "Resilient",    "meaning": "Able to recover quickly",               "example": "Children are very resilient."},
        {"word": "Endeavor",     "meaning": "To try hard to do something",           "example": "We will endeavor to improve."},
        {"word": "Ambiguous",    "meaning": "Having more than one possible meaning", "example": "His answer was ambiguous."},
        {"word": "Concise",      "meaning": "Brief but comprehensive",               "example": "Please be concise in your reply."},
        {"word": "Diligent",     "meaning": "Having steady effort and care",         "example": "She is a diligent student."},
    ],
    "korean": [
        {"word": "노력 (Noryeok)",     "meaning": "Effort / Hard work",   "example": "노력하면 성공할 수 있어요."},
        {"word": "꿈 (Kkum)",          "meaning": "Dream",                "example": "제 꿈은 의사가 되는 거예요."},
        {"word": "사랑 (Sarang)",      "meaning": "Love",                 "example": "사랑해요!"},
        {"word": "행복 (Haengbok)",    "meaning": "Happiness",            "example": "오늘 정말 행복해요."},
        {"word": "친구 (Chingu)",      "meaning": "Friend",               "example": "제 친구는 정말 좋아요."},
    ],
    "japanese": [
        {"word": "努力 (Doryoku)",    "meaning": "Effort",    "example": "努力すれば夢が叶います。"},
        {"word": "夢 (Yume)",         "meaning": "Dream",     "example": "私の夢は医者になることです。"},
        {"word": "友達 (Tomodachi)", "meaning": "Friend",    "example": "友達と一緒に勉強します。"},
        {"word": "幸せ (Shiawase)", "meaning": "Happiness", "example": "今日は幸せです。"},
    ],
}

def get_daily_words(lang: str, count: int = 5) -> list[dict]:
    import datetime
    words = DAILY_VOCAB.get(lang, DAILY_VOCAB["english"])
    day   = datetime.date.today().day
    start = day % len(words)
    result = []
    for i in range(count):
        result.append(words[(start + i) % len(words)])
    return result
