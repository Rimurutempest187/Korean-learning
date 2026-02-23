#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Tutor module for SUPER LEARNING BOT
Handles conversation practice and corrections
"""

import os
import logging
from typing import List, Dict, Optional
import openai
from openai import OpenAI

logger = logging.getLogger(__name__)


class AITutor:
    """AI-powered conversation tutor"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            self.client = OpenAI(api_key=api_key)
            self.enabled = True
        else:
            self.enabled = False
            logger.warning("OpenAI API key not found. AI Tutor features disabled.")
        
        self.conversations = {}  # Store conversation history per user
    
    def get_system_prompt(self, language: str, level: str, scenario: str = "general") -> str:
        """Generate system prompt for AI tutor"""
        
        scenario_prompts = {
            "restaurant": "You are helping the user practice ordering food at a restaurant.",
            "airport": "You are helping the user practice at an airport (check-in, security, customs).",
            "shopping": "You are helping the user practice shopping and asking about products.",
            "interview": "You are helping the user practice job interview conversations.",
            "free": "You are having a natural conversation with the user."
        }
        
        scenario_text = scenario_prompts.get(scenario, scenario_prompts["free"])
        
        prompt = f"""You are a friendly and patient language tutor helping a student learn {language}.

Student Level: {level}

Your role:
- {scenario_text}
- Respond in {language} (with English translations in parentheses if needed)
- Keep responses appropriate for {level} level
- Gently correct mistakes by showing the correct form
- Be encouraging and supportive
- Ask follow-up questions to keep the conversation going
- If the user makes a grammar mistake, correct it naturally in your response

Example correction format:
User: "I go to school yesterday"
You: "Great! Just a small note: 'I went to school yesterday' (past tense). Where is your school located?"

Keep responses concise and conversational."""
        
        return prompt
    
    async def get_response(self, user_id: int, message: str, language: str = "English", 
                           level: str = "Beginner", scenario: str = "free") -> str:
        """Get AI tutor response to user message"""
        
        if not self.enabled:
            return "AI Tutor is currently unavailable. Please configure OpenAI API key."
        
        try:
            # Initialize conversation history if not exists
            if user_id not in self.conversations:
                self.conversations[user_id] = []
            
            # Add user message to history
            self.conversations[user_id].append({
                "role": "user",
                "content": message
            })
            
            # Keep only last 10 messages to manage context length
            if len(self.conversations[user_id]) > 10:
                self.conversations[user_id] = self.conversations[user_id][-10:]
            
            # Prepare messages for API
            messages = [
                {"role": "system", "content": self.get_system_prompt(language, level, scenario)}
            ] + self.conversations[user_id]
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using cost-effective model
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversations[user_id].append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            return "Sorry, I encountered an error. Please try again."
    
    async def correct_sentence(self, sentence: str, language: str = "English") -> str:
        """Correct grammar in a sentence"""
        
        if not self.enabled:
            return "Grammar correction is currently unavailable."
        
        try:
            prompt = f"""Analyze this {language} sentence and provide corrections if needed:

Sentence: "{sentence}"

Provide:
1. Corrected version (if needed)
2. Brief explanation of errors
3. Example of correct usage

If the sentence is already correct, say so and provide encouragement."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are a {language} grammar expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error correcting sentence: {e}")
            return "Sorry, I couldn't correct that sentence right now."
    
    async def explain_grammar(self, grammar_point: str, language: str = "English", 
                             level: str = "Beginner") -> str:
        """Explain a grammar point"""
        
        if not self.enabled:
            return "Grammar explanations are currently unavailable."
        
        try:
            prompt = f"""Explain this {language} grammar point for a {level} level student:

Grammar Point: {grammar_point}

Provide:
1. Simple explanation
2. 2-3 examples
3. Common mistakes to avoid

Keep it clear and appropriate for {level} level."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are a {language} teacher."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.5
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error explaining grammar: {e}")
            return "Sorry, I couldn't provide that explanation right now."
    
    def clear_conversation(self, user_id: int):
        """Clear conversation history for a user"""
        if user_id in self.conversations:
            del self.conversations[user_id]
    
    async def generate_quiz_questions(self, language: str, level: str, 
                                     topic: str = "general", count: int = 5) -> List[Dict]:
        """Generate quiz questions using AI"""
        
        if not self.enabled:
            return []
        
        try:
            prompt = f"""Generate {count} multiple-choice questions for learning {language} at {level} level.
Topic: {topic}

Format each question as:
Question: [question text]
A) [option]
B) [option]
C) [option]
D) [option]
Correct: [A/B/C/D]
Explanation: [brief explanation]

Make questions appropriate for {level} level."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a language test creator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            # Parse response into structured questions
            # This is a simplified parser - could be enhanced
            questions = []
            content = response.choices[0].message.content
            
            # Basic parsing logic would go here
            # For now, return empty list (implement proper parsing in production)
            
            return questions
            
        except Exception as e:
            logger.error(f"Error generating quiz: {e}")
            return []
