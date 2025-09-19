"""Translation utilities for multilingual support."""

from googletrans import Translator
import streamlit as st
from config.languages import UI_TRANSLATIONS

class TranslationService:
    def __init__(self):
        self.translator = Translator()
    
    def translate_text(self, text, target_language='en', source_language='auto'):
        """Translate text to target language."""
        try:
            if target_language == 'en' and source_language == 'auto':
                return text
            
            result = self.translator.translate(text, dest=target_language, src=source_language)
            return result.text
        except Exception as e:
            st.error(f"Translation error: {e}")
            return text
    
    def get_ui_text(self, key, language='en'):
        """Get UI text in specified language."""
        return UI_TRANSLATIONS.get(language, UI_TRANSLATIONS['en']).get(key, key)
    
    def detect_language(self, text):
        """Detect the language of input text."""
        try:
            detection = self.translator.detect(text)
            return detection.lang
        except Exception as e:
            st.error(f"Language detection error: {e}")
            return 'en'

# Global translator instance
translator_service = TranslationService()