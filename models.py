#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data models for SUPER LEARNING BOT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class User:
    """User model"""
    user_id: int
    username: str
    learning_language: str
    level: str
    daily_goal_minutes: int = 10
    xp: int = 0
    streak: int = 0
    last_activity: Optional[str] = None
    total_lessons: int = 0
    total_minutes: int = 0
    weekly_lessons: int = 0
    monthly_lessons: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Lesson:
    """Lesson model"""
    id: Optional[int] = None
    language: str = ""
    level: str = ""
    topic: str = ""
    content: Dict = field(default_factory=dict)
    vocabulary: List[Dict] = field(default_factory=list)
    grammar: Dict = field(default_factory=dict)
    audio_url: str = ""
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Vocabulary:
    """Vocabulary model"""
    id: Optional[int] = None
    language: str = ""
    level: str = ""
    word: str = ""
    translation: str = ""
    pronunciation: str = ""
    example: str = ""
    audio_url: str = ""


@dataclass
class Quiz:
    """Quiz model"""
    id: Optional[int] = None
    language: str = ""
    level: str = ""
    quiz_type: str = ""
    questions: List[Dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Progress:
    """User progress model"""
    id: Optional[int] = None
    user_id: int = 0
    lesson_id: int = 0
    completed: bool = False
    score: int = 0
    time_spent: int = 0
    completed_at: Optional[datetime] = None


@dataclass
class Badge:
    """Badge/Achievement model"""
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    icon: str = ""
    requirement: str = ""


@dataclass
class Conversation:
    """AI Conversation model"""
    id: Optional[int] = None
    user_id: int = 0
    scenario: str = ""
    messages: List[Dict] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
