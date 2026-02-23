#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text-to-Speech module for SUPER LEARNING BOT
Handles pronunciation and audio generation
"""

import os
import logging
from gtts import gTTS
from io import BytesIO
from typing import Optional

logger = logging.getLogger(__name__)


class TextToSpeech:
    """Text-to-speech handler"""
    
    def __init__(self):
        self.supported_languages = {
            'en': 'en',
            'ko': 'ko',
            'ja': 'ja',
            'zh': 'zh-CN',
            'es': 'es',
            'fr': 'fr',
            'de': 'de',
            'th': 'th',
            'my': 'my'
        }
    
    def generate_speech(self, text: str, language: str = 'en', slow: bool = False) -> Optional[BytesIO]:
        """Generate speech from text"""
        
        try:
            # Get language code
            lang_code = self.supported_languages.get(language, 'en')
            
            # Generate speech
            tts = gTTS(text=text, lang=lang_code, slow=slow)
            
            # Save to BytesIO
            audio_fp = BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            
            return audio_fp
            
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            return None
    
    def generate_vocabulary_audio(self, word: str, language: str = 'en') -> Optional[BytesIO]:
        """Generate audio for vocabulary word"""
        return self.generate_speech(word, language, slow=True)
    
    def generate_sentence_audio(self, sentence: str, language: str = 'en') -> Optional[BytesIO]:
        """Generate audio for sentence"""
        return self.generate_speech(sentence, language, slow=False)
