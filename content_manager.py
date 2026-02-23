#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Content Manager for SUPER LEARNING BOT
Manages lessons, vocabulary, and learning content
"""

import random
import logging
from typing import List, Dict, Optional
from database import Database

logger = logging.getLogger(__name__)


class ContentManager:
    """Manages learning content"""
    
    def __init__(self):
        self.db = Database()
        self._initialize_sample_content()
    
    def _initialize_sample_content(self):
        """Initialize sample content for demo purposes"""
        # This would be replaced with actual content in production
        
        self.sample_topics = {
            'Beginner': [
                'Greetings and Introductions',
                'Numbers and Counting',
                'Family Members',
                'Daily Activities',
                'Food and Drinks',
                'Colors and Shapes',
                'Weather',
                'Basic Questions'
            ],
            'Elementary': [
                'Shopping',
                'Directions',
                'Time and Dates',
                'Hobbies',
                'Transportation',
                'Health and Body',
                'Jobs and Professions',
                'Describing People'
            ],
            'Intermediate': [
                'Travel and Tourism',
                'Making Plans',
                'Expressing Opinions',
                'Past Experiences',
                'Future Plans',
                'Describing Places',
                'Social Issues',
                'Technology'
            ],
            'Upper-Intermediate': [
                'Business Communication',
                'Academic Discussion',
                'Cultural Differences',
                'Environmental Issues',
                'Media and News',
                'Health and Fitness',
                'Arts and Entertainment',
                'Complex Grammar'
            ],
            'Advanced': [
                'Idioms and Expressions',
                'Formal Writing',
                'Debate and Argumentation',
                'Literature Discussion',
                'Professional Presentations',
                'Negotiation Skills',
                'Advanced Grammar Nuances',
                'Cultural Linguistics'
            ]
        }
        
        # Sample vocabulary by language
        self.sample_vocabulary = {
            'en': {
                'Beginner': [
                    {'word': 'Hello', 'translation': 'မင်္ဂလာပါ', 'pronunciation': 'həˈloʊ', 
                     'example': 'Hello! How are you?'},
                    {'word': 'Thank you', 'translation': 'ကျေးဇူးတင်ပါတယ်', 'pronunciation': 'θæŋk juː', 
                     'example': 'Thank you for your help!'},
                    {'word': 'Water', 'translation': 'ရေ', 'pronunciation': 'ˈwɔːtər', 
                     'example': 'Can I have some water?'},
                    {'word': 'Food', 'translation': 'အစားအစာ', 'pronunciation': 'fuːd', 
                     'example': 'The food is delicious!'},
                    {'word': 'Friend', 'translation': 'သူငယ်ချင်း', 'pronunciation': 'frend', 
                     'example': 'She is my best friend.'}
                ]
            },
            'ko': {
                'Beginner': [
                    {'word': '안녕하세요', 'translation': 'Hello', 'pronunciation': 'annyeonghaseyo', 
                     'example': '안녕하세요! 만나서 반갑습니다.'},
                    {'word': '감사합니다', 'translation': 'Thank you', 'pronunciation': 'gamsahamnida', 
                     'example': '도와주셔서 감사합니다.'},
                    {'word': '물', 'translation': 'Water', 'pronunciation': 'mul', 
                     'example': '물 한 잔 주세요.'},
                    {'word': '음식', 'translation': 'Food', 'pronunciation': 'eumsik', 
                     'example': '이 음식은 맛있어요.'},
                    {'word': '친구', 'translation': 'Friend', 'pronunciation': 'chingu', 
                     'example': '제 친구입니다.'}
                ]
            },
            'ja': {
                'Beginner': [
                    {'word': 'こんにちは', 'translation': 'Hello', 'pronunciation': 'konnichiwa', 
                     'example': 'こんにちは！お元気ですか？'},
                    {'word': 'ありがとう', 'translation': 'Thank you', 'pronunciation': 'arigatou', 
                     'example': 'ありがとうございます。'},
                    {'word': '水', 'translation': 'Water', 'pronunciation': 'mizu', 
                     'example': '水をください。'},
                    {'word': '食べ物', 'translation': 'Food', 'pronunciation': 'tabemono', 
                     'example': 'この食べ物は美味しいです。'},
                    {'word': '友達', 'translation': 'Friend', 'pronunciation': 'tomodachi', 
                     'example': '私の友達です。'}
                ]
            }
        }
    
    def generate_daily_lesson(self, language: str, level: str) -> Dict:
        """Generate a daily lesson for user"""
        
        # Get available topics for level
        topics = self.sample_topics.get(level, self.sample_topics['Beginner'])
        topic = random.choice(topics)
        
        # Check if lesson exists in database
        lessons = self.db.get_lessons_by_level(language, level, limit=1)
        
        if lessons:
            return lessons[0]
        
        # Generate new lesson structure
        lesson = {
            'id': random.randint(1000, 9999),  # Temporary ID
            'language': language,
            'level': level,
            'topic': topic,
            'content': {
                'introduction': f'Today we will learn about {topic}.',
                'main_content': 'Detailed lesson content would go here.',
                'practice': 'Practice exercises would go here.'
            },
            'vocabulary': self.get_daily_vocabulary(language, level, count=5),
            'grammar': {
                'point': 'Key grammar point',
                'explanation': 'Grammar explanation',
                'examples': []
            }
        }
        
        return lesson
    
    def get_daily_vocabulary(self, language: str, level: str, count: int = 5) -> List[Dict]:
        """Get daily vocabulary words"""
        
        # Try to get from database first
        vocab_list = self.db.get_vocabulary(language, level, limit=count)
        
        if vocab_list:
            return vocab_list
        
        # Use sample vocabulary
        if language in self.sample_vocabulary:
            if level in self.sample_vocabulary[language]:
                sample_words = self.sample_vocabulary[language][level]
                return random.sample(sample_words, min(count, len(sample_words)))
        
        # Return default vocabulary
        return self.sample_vocabulary['en']['Beginner'][:count]
    
    def get_lesson_by_topic(self, language: str, level: str, topic: str) -> Optional[Dict]:
        """Get a specific lesson by topic"""
        
        lessons = self.db.get_lessons_by_level(language, level, limit=20)
        
        for lesson in lessons:
            if lesson['topic'].lower() == topic.lower():
                return lesson
        
        # Generate if not found
        return self.generate_daily_lesson(language, level)
    
    def get_learning_path(self, language: str) -> List[Dict]:
        """Get complete learning path roadmap"""
        
        path = []
        
        for level in ['Beginner', 'Elementary', 'Intermediate', 'Upper-Intermediate', 'Advanced']:
            topics = self.sample_topics.get(level, [])
            
            path.append({
                'level': level,
                'topics': topics,
                'estimated_hours': len(topics) * 2,  # 2 hours per topic
                'description': f'{level} level content'
            })
        
        return path
    
    def create_quiz_from_vocabulary(self, vocab_list: List[Dict]) -> Dict:
        """Create a quiz from vocabulary list"""
        
        questions = []
        
        for vocab in vocab_list[:5]:  # Max 5 questions
            # Create multiple choice question
            question = {
                'type': 'multiple_choice',
                'question': f'What does "{vocab["word"]}" mean?',
                'options': [
                    vocab['translation'],
                    'Random option 1',
                    'Random option 2',
                    'Random option 3'
                ],
                'correct': 0,  # First option is correct
                'explanation': f'The correct translation is: {vocab["translation"]}'
            }
            
            # Shuffle options
            random.shuffle(question['options'])
            # Update correct index after shuffle
            question['correct'] = question['options'].index(vocab['translation'])
            
            questions.append(question)
        
        return {
            'questions': questions,
            'total': len(questions),
            'type': 'vocabulary'
        }
    
    def get_grammar_explanation(self, language: str, level: str, grammar_point: str) -> Dict:
        """Get grammar explanation"""
        
        # This would fetch from database or AI in production
        return {
            'point': grammar_point,
            'level': level,
            'explanation': f'Explanation for {grammar_point}',
            'examples': [
                'Example 1',
                'Example 2',
                'Example 3'
            ],
            'common_mistakes': [
                'Common mistake 1',
                'Common mistake 2'
            ],
            'practice_exercises': []
        }
    
    def get_listening_exercise(self, language: str, level: str) -> Dict:
        """Get listening exercise"""
        
        return {
            'title': 'Listening Exercise',
            'audio_url': '',  # Would be actual audio file
            'transcript': 'Full transcript of the audio',
            'questions': [
                {
                    'question': 'What is the main topic?',
                    'options': ['Option A', 'Option B', 'Option C'],
                    'correct': 0
                }
            ]
        }
    
    def search_content(self, language: str, query: str, content_type: str = 'all') -> List[Dict]:
        """Search for content by query"""
        
        results = []
        
        if content_type in ['all', 'lessons']:
            # Search lessons
            # Implementation would search database
            pass
        
        if content_type in ['all', 'vocabulary']:
            # Search vocabulary
            pass
        
        if content_type in ['all', 'grammar']:
            # Search grammar
            pass
        
        return results
