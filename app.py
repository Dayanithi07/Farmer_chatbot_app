"""Main Streamlit application for AI Farming Assistant."""

import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Import services
from config.languages import SUPPORTED_LANGUAGES
from utils.translation import translator_service
from utils.location import get_location_input
from utils.voice import voice_service
from services.weather import weather_service
from services.soil import soil_service
from services.disease_detection import disease_detection_service
from services.ai_chat import ai_chat_service

# Page configuration
st.set_page_config(
    page_title="🌾 AI Farming Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables."""
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    if 'location' not in st.session_state:
        st.session_state.location = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def language_selector():
    """Language selection interface."""
    st.sidebar.header("🌍 Language / भाषा / மொழி")
    
    language_options = {code: f"{lang['flag']} {lang['name']}" 
                       for code, lang in SUPPORTED_LANGUAGES.items()}
    
    selected_language = st.sidebar.selectbox(
        "Select Language:",
        options=list(language_options.keys()),
        format_func=lambda x: language_options[x],
        index=list(language_options.keys()).index(st.session_state.language)
    )
    
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()

def location_setup():
    """Location setup interface."""
    if not st.session_state.location:
        st.sidebar.header("📍 Location Setup")
        st.sidebar.info("Location is required for weather and soil data.")
        
        if st.sidebar.button("🌍 Setup Location"):
            st.session_state.show_location_setup = True
    else:
        location = st.session_state.location
        st.sidebar.success(f"📍 Location: {location.get('city', 'Unknown')}")
        if st.sidebar.button("📍 Change Location"):
            st.session_state.location = None
            st.rerun()

def voice_interface():
    """Voice input interface."""
    lang = st.session_state.language
    ui_text = translator_service.get_ui_text
    
    st.subheader(f"🎤 {ui_text('speak_request', lang)}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(ui_text('speak_button', lang), type="primary"):
            st.session_state.listening = True
    
    with col2:
        if st.button(ui_text('stop_button', lang)):
            st.session_state.listening = False
    
    # Text input as alternative
    text_input = st.text_input("Or type your question:", key="text_query")
    
    return text_input

def disease_detection_interface():
    """Disease detection interface."""
    lang = st.session_state.language
    ui_text = translator_service.get_ui_text
    
    st.subheader(f"📸 {ui_text('disease_title', lang)}")
    
    uploaded_file = st.file_uploader(
        ui_text('upload_image', lang),
        type=['jpg', 'jpeg', 'png'],
        key="disease_image"
    )
    
    if uploaded_file is not None:
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("🔍 Analyze Image", type="primary"):
            with st.spinner(ui_text('processing', lang)):
                # Detect disease
                predictions = disease_detection_service.detect_disease(image)
                
                if predictions:
                    # Display results
                    results = disease_detection_service.format_detection_results(predictions, lang)
                    st.success("Analysis Complete!")
                    st.text_area("Results:", results, height=200)
                    
                    # Generate voice response
                    audio_data = voice_service.text_to_speech(results, lang)
                    if audio_data:
                        voice_service.play_audio_in_streamlit(audio_data)
                else:
                    st.error(ui_text('error', lang))

def weather_interface():
    """Weather information interface."""
    lang = st.session_state.language
    ui_text = translator_service.get_ui_text
    
    if not st.session_state.location:
        st.warning(ui_text('no_location', lang))
        return
    
    st.subheader(f"🌦️ {ui_text('weather_title', lang)}")
    
    location = st.session_state.location
    lat, lon = location['latitude'], location['longitude']
    
    if st.button("🌤️ Get Weather Update", type="primary"):
        with st.spinner(ui_text('processing', lang)):
            # Get current weather
            weather_data = weather_service.get_current_weather(lat, lon)
            
            if weather_data:
                # Format for farmers
                weather_summary = weather_service.format_weather_for_farmers(weather_data, lang)
                
                # Translate if needed
                if lang != 'en':
                    weather_summary = translator_service.translate_text(weather_summary, lang)
                
                st.success("Weather Update:")
                st.text_area("Weather Information:", weather_summary, height=200)
                
                # Get forecast and create chart
                forecast_data = weather_service.get_weather_forecast(lat, lon)
                if forecast_data:
                    chart = weather_service.create_weather_chart(forecast_data)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                
                # Generate voice response
                audio_data = voice_service.text_to_speech(weather_summary, lang)
                if audio_data:
                    voice_service.play_audio_in_streamlit(audio_data)
            else:
                st.error(ui_text('error', lang))

def soil_interface():
    """Soil analysis interface."""
    lang = st.session_state.language
    ui_text = translator_service.get_ui_text
    
    if not st.session_state.location:
        st.warning(ui_text('no_location', lang))
        return
    
    st.subheader(f"🌱 {ui_text('soil_title', lang)}")
    
    location = st.session_state.location
    lat, lon = location['latitude'], location['longitude']
    
    if st.button("🌱 Analyze Soil", type="primary"):
        with st.spinner(ui_text('processing', lang)):
            # Get soil data
            soil_data = soil_service.get_soil_data(lat, lon)
            
            if soil_data:
                # Interpret soil data
                soil_analysis = soil_service.interpret_soil_data(soil_data, lang)
                
                # Translate if needed
                if lang != 'en':
                    soil_analysis = translator_service.translate_text(soil_analysis, lang)
                
                st.success("Soil Analysis Complete:")
                st.text_area("Soil Analysis:", soil_analysis, height=200)
                
                # Create visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    texture_chart = soil_service.create_soil_chart(soil_data)
                    if texture_chart:
                        st.plotly_chart(texture_chart, use_container_width=True)
                
                with col2:
                    properties_chart = soil_service.create_soil_properties_chart(soil_data)
                    if properties_chart:
                        st.plotly_chart(properties_chart, use_container_width=True)
                
                # Generate voice response
                audio_data = voice_service.text_to_speech(soil_analysis, lang)
                if audio_data:
                    voice_service.play_audio_in_streamlit(audio_data)
            else:
                st.error(ui_text('error', lang))

def chat_interface():
    """AI chat interface."""
    lang = st.session_state.language
    ui_text = translator_service.get_ui_text
    
    st.subheader(f"🤖 {ui_text('advisory_title', lang)}")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask your farming question..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner(ui_text('processing', lang)):
                # Detect intent
                intent = ai_chat_service.detect_intent(prompt)
                
                # Get context based on intent
                context = None
                if intent == 'weather' and st.session_state.location:
                    location = st.session_state.location
                    weather_data = weather_service.get_current_weather(
                        location['latitude'], location['longitude']
                    )
                    if weather_data:
                        context = f"Current weather: {weather_data['weather'][0]['description']}, {weather_data['main']['temp']}°C"
                
                # Get AI response
                response = ai_chat_service.get_farming_response(prompt, lang, context)
                
                # Translate if needed
                if lang != 'en':
                    response = translator_service.translate_text(response, lang)
                
                st.write(response)
                
                # Add assistant response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Generate voice response
                audio_data = voice_service.text_to_speech(response, lang)
                if audio_data:
                    voice_service.play_audio_in_streamlit(audio_data)

def main():
    """Main application function."""
    initialize_session_state()
    
    # Language selector in sidebar
    language_selector()
    
    # Location setup in sidebar
    location_setup()
    
    # Main title
    lang = st.session_state.language
    ui_text = translator_service.get_ui_text
    
    st.title(ui_text('app_title', lang))
    st.markdown(ui_text('welcome', lang))
    
    # Handle location setup
    if hasattr(st.session_state, 'show_location_setup') and st.session_state.show_location_setup:
        location_data = get_location_input()
        if location_data:
            st.session_state.show_location_setup = False
            st.rerun()
        return
    
    # Main interface tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎤 Voice Chat",
        "📸 Disease Detection", 
        "🌦️ Weather",
        "🌱 Soil Analysis",
        "💬 AI Chat"
    ])
    
    with tab1:
        voice_interface()
        chat_interface()
    
    with tab2:
        disease_detection_interface()
    
    with tab3:
        weather_interface()
    
    with tab4:
        soil_interface()
    
    with tab5:
        chat_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("🌾 AI Farming Assistant - Empowering farmers with technology")

if __name__ == "__main__":
    main()