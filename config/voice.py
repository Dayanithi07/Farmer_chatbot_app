"""Voice input and output utilities."""

import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import io
import tempfile
import os
from pydub import AudioSegment
from pydub.playback import play
import base64

class VoiceService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
    
    def speech_to_text(self, audio_data, language='en'):
        """Convert speech to text."""
        try:
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error with speech recognition service: {e}"
    
    def text_to_speech(self, text, language='en'):
        """Convert text to speech and return audio data."""
        try:
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                
                # Read the audio file
                with open(tmp_file.name, 'rb') as audio_file:
                    audio_data = audio_file.read()
                
                # Clean up
                os.unlink(tmp_file.name)
                
                return audio_data
        except Exception as e:
            st.error(f"Text-to-speech error: {e}")
            return None
    
    def play_audio_in_streamlit(self, audio_data):
        """Play audio in Streamlit interface."""
        if audio_data:
            # Encode audio data to base64
            audio_base64 = base64.b64encode(audio_data).decode()
            
            # Create HTML audio element
            audio_html = f"""
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            """
            
            st.markdown(audio_html, unsafe_allow_html=True)

# Global voice service instance
voice_service = VoiceService()