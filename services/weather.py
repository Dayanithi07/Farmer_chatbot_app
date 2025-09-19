"""Weather service using OpenWeather API."""

import requests
import streamlit as st
import os
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, lat, lon):
        """Get current weather data."""
        if not self.api_key:
            st.error("OpenWeather API key not found. Please add it to your .env file.")
            return None
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Weather API error: {e}")
            return None
    
    def get_weather_forecast(self, lat, lon, days=5):
        """Get weather forecast."""
        if not self.api_key:
            return None
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Forecast API error: {e}")
            return None
    
    def format_weather_for_farmers(self, weather_data, language='en'):
        """Format weather data in farmer-friendly language."""
        if not weather_data:
            return "Weather data not available."
        
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        wind_speed = weather_data['wind']['speed']
        
        # Farmer-friendly advice based on weather
        advice = []
        
        if temp > 35:
            advice.append("Very hot weather - ensure adequate irrigation and shade for crops.")
        elif temp < 10:
            advice.append("Cold weather - protect sensitive crops from frost.")
        
        if humidity > 80:
            advice.append("High humidity - watch for fungal diseases.")
        elif humidity < 30:
            advice.append("Low humidity - increase watering frequency.")
        
        if wind_speed > 10:
            advice.append("Strong winds - secure tall crops and check for damage.")
        
        if 'rain' in description.lower():
            advice.append("Rain expected - postpone spraying and harvesting if possible.")
        
        weather_summary = f"""
        🌡️ Temperature: {temp}°C
        💧 Humidity: {humidity}%
        🌤️ Conditions: {description.title()}
        💨 Wind Speed: {wind_speed} m/s
        
        🧑‍🌾 Farming Advice:
        {' '.join([f'• {tip}' for tip in advice]) if advice else '• Weather conditions are favorable for normal farming activities.'}
        """
        
        return weather_summary
    
    def create_weather_chart(self, forecast_data):
        """Create weather visualization chart."""
        if not forecast_data:
            return None
        
        dates = []
        temps = []
        humidity = []
        
        for item in forecast_data['list'][:24]:  # Next 24 forecasts (3 days)
            dates.append(datetime.fromtimestamp(item['dt']))
            temps.append(item['main']['temp'])
            humidity.append(item['main']['humidity'])
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Temperature (°C)', 'Humidity (%)'),
            vertical_spacing=0.1
        )
        
        fig.add_trace(
            go.Scatter(x=dates, y=temps, mode='lines+markers', name='Temperature'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=dates, y=humidity, mode='lines+markers', name='Humidity', line=dict(color='blue')),
            row=2, col=1
        )
        
        fig.update_layout(height=400, showlegend=False)
        fig.update_xaxes(title_text="Time")
        fig.update_yaxes(title_text="Temperature (°C)", row=1, col=1)
        fig.update_yaxes(title_text="Humidity (%)", row=2, col=1)
        
        return fig

# Global weather service instance
weather_service = WeatherService()