"""
Initialize handlers package
"""
from .start_handler import StartHandler
from .lesson_handler import LessonHandler
from .quiz_handler import QuizHandler
from .profile_handler import ProfileHandler
from .leaderboard_handler import LeaderboardHandler
from .admin_handler import AdminHandler

__all__ = [
    'StartHandler',
    'LessonHandler',
    'QuizHandler',
    'ProfileHandler',
    'LeaderboardHandler',
    'AdminHandler'
]
