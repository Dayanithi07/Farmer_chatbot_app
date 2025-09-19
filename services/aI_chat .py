"""AI chat service with Gemini API and Hugging Face fallback."""

import streamlit as st
import requests
import os
from transformers import pipeline
import google.generativeai as genai

class AIChatService:
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.hf_api_key = os.getenv('HUGGINGFACE_API_KEY')
        self.fallback_model = None
        self.setup_gemini()
        self.setup_fallback()
    
    def setup_gemini(self):
        """Setup Gemini AI."""
        if self.gemini_api_key:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                st.success("Gemini AI connected successfully!")
            except Exception as e:
                st.warning(f"Gemini setup error: {e}")
                self.gemini_model = None
        else:
            self.gemini_model = None
    
    def setup_fallback(self):
        """Setup Hugging Face fallback model."""
        try:
            # Use a smaller, faster model for fallback
            self.fallback_model = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",
                device=-1  # Use CPU
            )
        except Exception as e:
            st.warning(f"Fallback model setup error: {e}")
            self.fallback_model = None
    
    def get_farming_response(self, query, language='en', context=None):
        """Get AI response for farming queries."""
        # Create farming-focused prompt
        farming_prompt = f"""
        You are an expert agricultural advisor helping farmers. 
        Respond in {language} language.
        Provide practical, actionable advice in simple language that farmers can understand.
        Focus on local farming practices and be specific about timing, quantities, and methods.
        
        Farmer's question: {query}
        
        Additional context: {context if context else 'None'}
        
        Provide a helpful response with:
        1. Direct answer to the question
        2. Practical steps to take
        3. Any warnings or precautions
        4. Best timing for the advice
        """
        
        # Try Gemini first
        if self.gemini_model:
            try:
                response = self.gemini_model.generate_content(farming_prompt)
                return response.text
            except Exception as e:
                st.warning(f"Gemini API error: {e}. Using fallback...")
        
        # Fallback to Hugging Face
        if self.fallback_model:
            try:
                response = self.fallback_model(
                    farming_prompt,
                    max_length=200,
                    num_return_sequences=1,
                    temperature=0.7
                )
                return response[0]['generated_text']
            except Exception as e:
                st.error(f"Fallback model error: {e}")
        
        # Final fallback - basic response
        return self.get_basic_farming_response(query, language)
    
    def get_basic_farming_response(self, query, language='en'):
        """Basic farming responses when AI models are unavailable."""
        basic_responses = {
            'en': {
                'weather': "Check local weather forecasts regularly. Plan irrigation and harvesting based on weather predictions.",
                'soil': "Test your soil pH and nutrient levels. Add organic matter like compost to improve soil health.",
                'pest': "Monitor crops regularly for pests. Use integrated pest management combining biological and chemical controls.",
                'fertilizer': "Apply fertilizers based on soil test results. Use organic fertilizers when possible.",
                'irrigation': "Water crops early morning or evening. Ensure proper drainage to prevent waterlogging.",
                'default': "For specific farming advice, consult your local agricultural extension officer or experienced farmers in your area."
            },
            'hi': {
                'weather': "स्थानीय मौसम पूर्वानुमान नियमित रूप से जांचें। मौसम की भविष्यवाणी के आधार पर सिंचाई और कटाई की योजना बनाएं।",
                'soil': "अपनी मिट्टी का pH और पोषक तत्व स्तर जांचें। मिट्टी के स्वास्थ्य में सुधार के लिए कंपोस्ट जैसे जैविक पदार्थ जोड़ें।",
                'pest': "कीटों के लिए नियमित रूप से फसलों की निगरानी करें। जैविक और रासायनिक नियंत्रण को मिलाकर एकीकृत कीट प्रबंधन का उपयोग करें।",
                'fertilizer': "मिट्टी परीक्षण परिणामों के आधार पर उर्वरक लगाएं। जब संभव हो तो जैविक उर्वरकों का उपयोग करें।",
                'irrigation': "सुबह जल्दी या शाम को फसलों को पानी दें। जलभराव को रोकने के लिए उचित जल निकासी सुनिश्चित करें।",
                'default': "विशिष्ट कृषि सलाह के लिए, अपने स्थानीय कृषि विस्तार अधिकारी या अपने क्षेत्र के अनुभवी किसानों से सलाह लें।"
            }
        }
        
        query_lower = query.lower()
        responses = basic_responses.get(language, basic_responses['en'])
        
        for key in responses:
            if key in query_lower:
                return responses[key]
        
        return responses['default']
    
    def detect_intent(self, query):
        """Detect the intent of the user query."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['weather', 'rain', 'temperature', 'humidity', 'wind']):
            return 'weather'
        elif any(word in query_lower for word in ['soil', 'ph', 'fertilizer', 'nutrient', 'organic']):
            return 'soil'
        elif any(word in query_lower for word in ['disease', 'pest', 'insect', 'fungus', 'infection']):
            return 'disease'
        elif any(word in query_lower for word in ['irrigation', 'water', 'watering', 'drought']):
            return 'irrigation'
        elif any(word in query_lower for word in ['crop', 'plant', 'seed', 'harvest', 'planting']):
            return 'crop_management'
        else:
            return 'general'

# Global AI chat service instance
ai_chat_service = AIChatService()