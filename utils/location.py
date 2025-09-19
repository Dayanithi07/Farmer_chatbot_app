"""Location utilities for the farming assistant."""

import requests
import streamlit as st
from geopy.geocoders import Nominatim
import json

def get_user_location():
    """Get user location using IP geolocation as fallback."""
    try:
        # Try to get location from IP
        response = requests.get('http://ip-api.com/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return {
                    'latitude': data['lat'],
                    'longitude': data['lon'],
                    'city': data['city'],
                    'region': data['regionName'],
                    'country': data['country']
                }
    except Exception as e:
        st.error(f"Error getting location: {e}")
    
    return None

def reverse_geocode(lat, lon):
    """Get address from coordinates."""
    try:
        geolocator = Nominatim(user_agent="farming_assistant")
        location = geolocator.reverse(f"{lat}, {lon}")
        if location:
            return location.address
    except Exception as e:
        st.error(f"Error in reverse geocoding: {e}")
    
    return f"Lat: {lat}, Lon: {lon}"

def get_location_input():
    """Get location input from user with multiple options."""
    st.subheader("📍 Location Setup")
    
    location_method = st.radio(
        "How would you like to provide your location?",
        ["Auto-detect", "Manual coordinates", "City name"]
    )
    
    location_data = None
    
    if location_method == "Auto-detect":
        if st.button("🌍 Detect My Location"):
            with st.spinner("Detecting location..."):
                location_data = get_user_location()
                if location_data:
                    st.success(f"Location detected: {location_data['city']}, {location_data['region']}")
                    st.session_state.location = location_data
                else:
                    st.error("Could not detect location automatically. Please try manual input.")
    
    elif location_method == "Manual coordinates":
        col1, col2 = st.columns(2)
        with col1:
            lat = st.number_input("Latitude", value=0.0, format="%.6f")
        with col2:
            lon = st.number_input("Longitude", value=0.0, format="%.6f")
        
        if st.button("📍 Use These Coordinates"):
            if lat != 0.0 and lon != 0.0:
                address = reverse_geocode(lat, lon)
                location_data = {
                    'latitude': lat,
                    'longitude': lon,
                    'address': address
                }
                st.session_state.location = location_data
                st.success(f"Location set: {address}")
    
    elif location_method == "City name":
        city_name = st.text_input("Enter your city name:")
        if st.button("🔍 Find City") and city_name:
            try:
                geolocator = Nominatim(user_agent="farming_assistant")
                location = geolocator.geocode(city_name)
                if location:
                    location_data = {
                        'latitude': location.latitude,
                        'longitude': location.longitude,
                        'address': location.address
                    }
                    st.session_state.location = location_data
                    st.success(f"Location found: {location.address}")
                else:
                    st.error("City not found. Please check the spelling.")
            except Exception as e:
                st.error(f"Error finding city: {e}")
    
    return location_data