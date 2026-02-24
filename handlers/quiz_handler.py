"""
Quiz Handler - Manages quiz sessions and answers
"""
import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from managers.user_manager import UserManager
from managers.lesson_manager import LessonManager
from config import Config
from utils.formatter import escape_markdown

logger = logging.getLogger(__name__)


class QuizHandler:
    """Handles quiz sessions and answer validation"""
    
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
        self.lesson_manager = LessonManager()
        self.config = Config()
    
    async def handle_quiz_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start a new quiz session"""
        query = update.callback_query
        await query.answer()
        
        _, language, unit, lesson_id = query.data.split("_", 3)
        
        # Get quiz questions
        questions = self.lesson_manager.get_quiz_questions(language, unit, lesson_id)
        
        if not questions:
            await query.answer("No quiz available for this lesson!", show_alert=True)
            return
        
        # Create quiz session
        user_id = query.from_user.id
        await self.user_manager.db.execute(
            """INSERT INTO quiz_sessions 
               (user_id, language, lesson_id, current_question, correct_answers, total_questions, session_data)
               VALUES (?, ?, ?, 0, 0, ?, ?)""",
            (user_id, language, lesson_id, len(questions), json.dumps(questions))
        )
        
        # Show first question
        await self._show_question(query, user_id, questions, 0, language, unit, lesson_id)
    
    async def _show_question(self, query, user_id: int, questions: list, 
                            question_idx: int, language: str, unit: str, lesson_id: str):
        """Display a quiz question"""
        if question_idx >= len(questions):
            # Quiz complete
            await self._complete_quiz(query, user_id, language, unit, lesson_id)
            return
        
        question = questions[question_idx]
        
        # Get current hearts
        user = await self.user_manager.get_or_create_user(user_id)
        hearts = "❤️" * user['hearts'] + "🖤" * (self.config.MAX_HEARTS - user['hearts'])
        
        text = (
            f"*Quiz Question {question_idx + 1}/{len(questions)}*\n"
            f"{hearts}\n\n"
            f"{escape_markdown(question['question'])}"
        )
        
        if question['type'] == 'multiple_choice':
            keyboard = []
            for idx, option in enumerate(question['options']):
                keyboard.append([
                    InlineKeyboardButton(
                        escape_markdown(option, for_button=True),
                        callback_data=f"answer_{language}_{unit}_{lesson_id}_{question_idx}_{idx}"
                    )
                ])
            
            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="MarkdownV2"
            )
        
        elif question['type'] == 'text_input':
            text += "\n\n_Type your answer:_"
            
            # Store context for text answer
            context.user_data['awaiting_text_answer'] = {
                'language': language,
                'unit': unit,
                'lesson_id': lesson_id,
                'question_idx': question_idx,
                'correct_answer': question['answer']
            }
            
            keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data=f"unit_{language}_{unit}")]]
            
            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="MarkdownV2"
            )
    
    async def handle_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle multiple choice answer"""
        query = update.callback_query
        await query.answer()
        
        parts = query.data.split("_")
        language = parts[1]
        unit = parts[2]
        lesson_id = parts[3]
        question_idx = int(parts[4])
        user_answer = int(parts[5])
        
        user_id = query.from_user.id
        
        # Get session
        session = await self.user_manager.db.fetch_one(
            """SELECT session_data, correct_answers FROM quiz_sessions 
               WHERE user_id = ? AND lesson_id = ? 
               ORDER BY id DESC LIMIT 1""",
            (user_id, lesson_id)
        )
        
        if not session:
            await query.answer("Session expired!", show_alert=True)
            return
        
        questions = json.loads(session['session_data'])
        question = questions[question_idx]
        
        is_correct = user_answer == question['correct']
        
        if is_correct:
            # Correct answer
            await self.user_manager.add_xp(user_id, self.config.XP_PER_CORRECT_ANSWER)
            await self.user_manager.db.execute(
                """UPDATE quiz_sessions 
                   SET correct_answers = correct_answers + 1, current_question = ?
                   WHERE user_id = ? AND lesson_id = ? 
                   AND id = (SELECT MAX(id) FROM quiz_sessions WHERE user_id = ? AND lesson_id = ?)""",
                (question_idx + 1, user_id, lesson_id, user_id, lesson_id)
            )
            
            feedback = "✅ *Correct!*\n\n+{} XP".format(self.config.XP_PER_CORRECT_ANSWER)
        else:
            # Wrong answer
            hearts = await self.user_manager.lose_heart(user_id)
            await self.user_manager.db.execute(
                """UPDATE quiz_sessions 
                   SET current_question = ?
                   WHERE user_id = ? AND lesson_id = ?
                   AND id = (SELECT MAX(id) FROM quiz_sessions WHERE user_id = ? AND lesson_id = ?)""",
                (question_idx + 1, user_id, lesson_id, user_id, lesson_id)
            )
            
            correct_answer = escape_markdown(question['options'][question['correct']])
            feedback = f"❌ *Incorrect!*\n\nCorrect answer: {correct_answer}\n\n❤️ Hearts remaining: {hearts}"
            
            if hearts == 0:
                feedback += "\n\n⚠️ *No hearts left!* Come back later or wait for refill."
        
        keyboard = [[InlineKeyboardButton("Next →", callback_data=f"quiz_next_{language}_{unit}_{lesson_id}")]]
        
        await query.edit_message_text(
            feedback,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="MarkdownV2"
        )
        
        # Auto-advance after short delay if hearts remain or correct
        if is_correct or hearts > 0:
            # Schedule next question
            context.user_data['next_question_data'] = {
                'language': language,
                'unit': unit,
                'lesson_id': lesson_id,
                'question_idx': question_idx + 1
            }
    
    async def handle_text_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text input answers"""
        if 'awaiting_text_answer' not in context.user_data:
            return
        
        answer_data = context.user_data['awaiting_text_answer']
        user_answer = update.message.text.strip()
        correct_answer = answer_data['correct_answer']
        
        user_id = update.effective_user.id
        
        is_correct = user_answer.lower() == correct_answer.lower()
        
        if is_correct:
            await self.user_manager.add_xp(user_id, self.config.XP_PER_CORRECT_ANSWER)
            await update.message.reply_text(
                f"✅ *Correct!*\n\n+{self.config.XP_PER_CORRECT_ANSWER} XP",
                parse_mode="MarkdownV2"
            )
        else:
            hearts = await self.user_manager.lose_heart(user_id)
            await update.message.reply_text(
                f"❌ *Incorrect!*\n\nCorrect answer: {escape_markdown(correct_answer)}\n\n"
                f"❤️ Hearts remaining: {hearts}",
                parse_mode="MarkdownV2"
            )
        
        # Clear context
        del context.user_data['awaiting_text_answer']
    
    async def _complete_quiz(self, query, user_id: int, language: str, unit: str, lesson_id: str):
        """Complete quiz and show results"""
        session = await self.user_manager.db.fetch_one(
            """SELECT correct_answers, total_questions FROM quiz_sessions 
               WHERE user_id = ? AND lesson_id = ? 
               ORDER BY id DESC LIMIT 1""",
            (user_id, lesson_id)
        )
        
        if not session:
            return
        
        correct = session['correct_answers']
        total = session['total_questions']
        score = int((correct / total) * 100) if total > 0 else 0
        
        # Complete lesson
        await self.user_manager.complete_lesson(user_id, language, unit, lesson_id, score)
        
        # Check achievements
        if score == 100:
            unlocked = await self.user_manager.unlock_achievement(user_id, "perfect_quiz")
            if unlocked:
                achievement_text = "\n\n🎉 *Achievement Unlocked:* 💯 Perfect Score!"
            else:
                achievement_text = ""
        else:
            achievement_text = ""
        
        # Get updated user data
        user = await self.user_manager.get_or_create_user(user_id)
        
        text = (
            f"🎊 *Quiz Complete!*\n\n"
            f"Score: {correct}/{total} \\({score}%\\)\n"
            f"XP Earned: \\+{self.config.XP_PER_LESSON_COMPLETE}\n"
            f"Current XP: {user['xp']}\n"
            f"Streak: {user['streak']} days 🔥"
            f"{achievement_text}"
        )
        
        keyboard = [
            [InlineKeyboardButton("📚 More Lessons", callback_data=f"unit_{language}_{unit}")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")]
        ]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="MarkdownV2"
        )
