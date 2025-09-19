"""Plant disease detection service using Hugging Face models."""

import streamlit as st
from transformers import pipeline
from PIL import Image
import torch
import numpy as np
import requests
import os

class DiseaseDetectionService:
    def __init__(self):
        self.model_name = "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
        self.classifier = None
        self.load_model()
    
    def load_model(self):
        """Load the plant disease detection model."""
        try:
            # Check if CUDA is available
            device = 0 if torch.cuda.is_available() else -1
            
            self.classifier = pipeline(
                "image-classification",
                model=self.model_name,
                device=device
            )
            st.success("Disease detection model loaded successfully!")
        except Exception as e:
            st.error(f"Error loading disease detection model: {e}")
            self.classifier = None
    
    def detect_disease(self, image):
        """Detect plant disease from image."""
        if not self.classifier:
            return None
        
        try:
            # Ensure image is in RGB format
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get predictions
            predictions = self.classifier(image)
            
            # Return top 3 predictions
            return predictions[:3]
        except Exception as e:
            st.error(f"Error in disease detection: {e}")
            return None
    
    def get_disease_advice(self, disease_name, confidence, language='en'):
        """Get farming advice for detected disease."""
        # Disease advice database
        disease_advice = {
            'healthy': {
                'en': "Your plant looks healthy! Continue with regular care and monitoring.",
                'hi': "आपका पौधा स्वस्थ दिख रहा है! नियमित देखभाल और निगरानी जारी रखें।",
                'ta': "உங்கள் செடி ஆரோக்கியமாக தெரிகிறது! வழக்கமான பராமரிப்பு மற்றும் கண்காணிப்பைத் தொடரவும்।",
                'te': "మీ మొక్క ఆరోగ్యంగా కనిపిస్తోంది! సాధారణ సంరక్షణ మరియు పర్యవేక్షణను కొనసాగించండి।"
            },
            'bacterial_blight': {
                'en': "Bacterial blight detected. Remove affected leaves, improve air circulation, and apply copper-based fungicide.",
                'hi': "बैक्टीरियल ब्लाइट का पता चला। प्रभावित पत्तियों को हटाएं, हवा का संचार बेहतर बनाएं, और तांबा आधारित कवकनाशी लगाएं।",
                'ta': "பாக்டீரியல் ப்ளைட் கண்டறியப்பட்டது. பாதிக்கப்பட்ட இலைகளை அகற்றி, காற்று சுழற்சியை மேம்படுத்தி, செம்பு அடிப்படையிலான பூஞ்சைக் கொல்லியைப் பயன்படுத்தவும்।",
                'te': "బ్యాక్టీరియల్ బ్లైట్ గుర్తించబడింది. ప్రభావిత ఆకులను తొలగించి, గాలి ప్రసరణను మెరుగుపరచి, రాగి ఆధారిత శిలీంధ్రనాశకాన్ని వర్తించండి।"
            },
            'leaf_spot': {
                'en': "Leaf spot disease found. Remove infected leaves, avoid overhead watering, and apply appropriate fungicide.",
                'hi': "पत्ती धब्बा रोग मिला। संक्रमित पत्तियों को हटाएं, ऊपर से पानी देने से बचें, और उपयुक्त कवकनाशी लगाएं।",
                'ta': "இலைப் புள்ளி நோய் கண்டறியப்பட்டது. பாதிக்கப்பட்ட இலைகளை அகற்றி, மேல் நீர்ப்பாசனத்தைத் தவிர்த்து, பொருத்தமான பூஞ்சைக் கொல்லியைப் பயன்படுத்தவும்।",
                'te': "ఆకు మచ్చ వ్యాధి కనుగొనబడింది. సోకిన ఆకులను తొలగించి, పైనుండి నీరు పోయడం మానుకుని, తగిన శిలీంధ్రనాశకాన్ని వర్తించండి।"
            }
        }
        
        # Default advice if specific disease not found
        default_advice = {
            'en': f"Disease detected with {confidence:.1%} confidence. Consult with local agricultural extension officer for specific treatment.",
            'hi': f"{confidence:.1%} विश्वसनीयता के साथ रोग का पता चला। विशिष्ट उपचार के लिए स्थानीय कृषि विस्तार अधिकारी से सलाह लें।",
            'ta': f"{confidence:.1%} நம்பகத்தன்மையுடன் நோய் கண்டறியப்பட்டது. குறிப்பிட்ட சிகிச்சைக்காக உள்ளூர் விவசாய விரிவாக்க அதிகாரியுடன் ஆலோசிக்கவும்.",
            'te': f"{confidence:.1%} విశ్వసనీయతతో వ్యాధి గుర్తించబడింది. నిర్దిష్ట చికిత్స కోసం స్థానిక వ్యవసాయ విస్తరణ అధికారితో సంప్రదించండి।"
        }
        
        # Clean disease name for lookup
        clean_disease = disease_name.lower().replace(' ', '_').replace('-', '_')
        
        # Find matching advice
        for key, advice in disease_advice.items():
            if key in clean_disease or clean_disease in key:
                return advice.get(language, advice['en'])
        
        return default_advice.get(language, default_advice['en'])
    
    def format_detection_results(self, predictions, language='en'):
        """Format disease detection results for display."""
        if not predictions:
            return "No predictions available."
        
        result = f"🔍 Disease Detection Results:\n\n"
        
        for i, pred in enumerate(predictions, 1):
            confidence = pred['score']
            disease = pred['label']
            
            result += f"{i}. {disease.title()}\n"
            result += f"   Confidence: {confidence:.1%}\n"
            
            if i == 1:  # Most likely prediction
                advice = self.get_disease_advice(disease, confidence, language)
                result += f"\n🧑‍🌾 Recommended Action:\n{advice}\n"
            
            result += "\n"
        
        return result

# Global disease detection service instance
disease_detection_service = DiseaseDetectionService()