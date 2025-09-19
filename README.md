# 🌾 AI Farming Assistant

A comprehensive voice-first, AI-powered assistant designed specifically for farmers. This application supports multiple languages and provides practical farming guidance through various AI-powered features.

## 🌟 Features

### 🌍 Multilingual Support
- **Languages**: English, Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali
- **Voice Support**: Text-to-speech and speech-to-text in all supported languages
- **UI Translation**: Complete interface translation based on selected language

### 📸 Plant Disease Detection
- **AI-Powered Analysis**: Uses MobileNetV2 model for accurate disease identification
- **Instant Results**: Upload or capture images for immediate analysis
- **Treatment Advice**: Provides specific treatment recommendations for detected diseases
- **Confidence Scoring**: Shows prediction confidence levels

### 🌦️ Weather Integration
- **Real-time Data**: Current weather conditions using OpenWeather API
- **Farmer-Focused**: Weather information presented in farming context
- **Visual Charts**: Temperature and humidity trends
- **Advisory Alerts**: Weather-based farming recommendations

### 🌱 Soil Analysis
- **Comprehensive Testing**: pH, organic carbon, nitrogen, and texture analysis
- **SoilGrids Integration**: Global soil data from scientific databases
- **Visual Reports**: Interactive charts showing soil composition
- **Actionable Advice**: Specific fertilizer and soil improvement recommendations

### 🤖 AI Chat Assistant
- **Dual AI System**: Primary Gemini API with Hugging Face fallback
- **Intent Detection**: Automatically categorizes farming queries
- **Context-Aware**: Incorporates weather and location data in responses
- **Conversational**: Natural language interaction in farmer-friendly terms

### 🎤 Voice Interface
- **Speech-to-Text**: Voice input in multiple languages
- **Text-to-Speech**: Audio responses for accessibility
- **Hands-Free Operation**: Perfect for field use

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Required API keys (see setup below)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-farming-assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup environment variables**
```bash
cp .env.example .env
```

Edit `.env` file with your API keys:
```env
OPENWEATHER_API_KEY=your_openweather_api_key
GEMINI_API_KEY=your_gemini_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

4. **Run the application**
```bash
streamlit run app.py
```

## 🔑 API Keys Setup

### OpenWeather API
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Add to `.env` file

### Google Gemini API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to `.env` file

### Hugging Face API (Optional)
1. Visit [Hugging Face](https://huggingface.co/settings/tokens)
2. Create an access token
3. Add to `.env` file

## 📱 Usage Guide

### 1. Language Selection
- Choose your preferred language from the sidebar
- All UI elements and voice responses will adapt

### 2. Location Setup
- Provide your location for weather and soil data
- Options: Auto-detect, manual coordinates, or city name

### 3. Disease Detection
- Upload or capture crop images
- Get instant AI analysis with treatment advice
- Listen to audio recommendations

### 4. Weather Monitoring
- Get current weather conditions
- View forecasts with farming implications
- Receive weather-based advisory

### 5. Soil Analysis
- Analyze soil properties at your location
- Get fertilizer and soil improvement recommendations
- View soil composition charts

### 6. AI Chat
- Ask farming questions in natural language
- Get context-aware responses
- Voice input and output supported

## 🏗️ Architecture

### Frontend
- **Streamlit**: Web interface with mobile-responsive design
- **Plotly**: Interactive charts and visualizations
- **PIL**: Image processing for disease detection

### AI Models
- **MobileNetV2**: Plant disease identification
- **Google Gemini**: Primary conversational AI
- **Hugging Face Models**: Fallback AI and specialized tasks

### APIs & Services
- **OpenWeather**: Weather data
- **SoilGrids**: Global soil information
- **Google Translate**: Multilingual support
- **Google TTS**: Text-to-speech conversion

### Data Flow
```
User Input → Language Detection → Intent Analysis → Service Routing → AI Processing → Translation → Voice Output
```

## 🌾 Farming Features

### Disease Management
- 38+ plant diseases supported
- Treatment protocols included
- Prevention strategies
- Organic and chemical solutions

### Weather Advisory
- Irrigation scheduling
- Harvest timing
- Pest risk assessment
- Crop protection alerts

### Soil Health
- pH optimization
- Nutrient management
- Organic matter improvement
- Fertilizer recommendations

### Crop Management
- Planting schedules
- Growth monitoring
- Yield optimization
- Market timing

## 🔧 Customization

### Adding New Languages
1. Update `config/languages.py`
2. Add translations to `UI_TRANSLATIONS`
3. Test TTS support

### Adding New Diseases
1. Update disease advice database in `services/disease_detection.py`
2. Add multilingual treatment protocols
3. Test with sample images

### Extending AI Responses
1. Modify prompts in `services/ai_chat.py`
2. Add new intent categories
3. Include regional farming practices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenWeatherMap for weather data
- SoilGrids for soil information
- Hugging Face for AI models
- Google for translation and TTS services
- The farming community for inspiration and feedback

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**🌾 Empowering farmers with AI technology for sustainable agriculture**