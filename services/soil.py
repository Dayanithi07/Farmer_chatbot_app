"""Soil analysis service using SoilGrids API."""

import requests
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class SoilService:
    def __init__(self):
        self.base_url = "https://rest.soilgrids.org"
    
    def get_soil_data(self, lat, lon):
        """Get soil data from SoilGrids API."""
        try:
            # SoilGrids properties we're interested in
            properties = [
                'phh2o',      # pH in water
                'soc',        # Soil organic carbon
                'nitrogen',   # Total nitrogen
                'sand',       # Sand content
                'clay',       # Clay content
                'silt'        # Silt content
            ]
            
            soil_data = {}
            
            for prop in properties:
                url = f"{self.base_url}/soilgrids/v2.0/properties/query"
                params = {
                    'lon': lon,
                    'lat': lat,
                    'property': prop,
                    'depth': '0-5cm',  # Top soil layer
                    'value': 'mean'
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'properties' in data and prop in data['properties']:
                        layers = data['properties'][prop]['depths']
                        if layers:
                            # Get the first depth layer (0-5cm)
                            value = layers[0]['values']['mean']
                            soil_data[prop] = value
            
            return soil_data
        except requests.exceptions.RequestException as e:
            st.error(f"Soil API error: {e}")
            return None
        except Exception as e:
            st.error(f"Error processing soil data: {e}")
            return None
    
    def interpret_soil_data(self, soil_data, language='en'):
        """Interpret soil data for farmers."""
        if not soil_data:
            return "Soil data not available."
        
        interpretation = []
        recommendations = []
        
        # pH interpretation
        if 'phh2o' in soil_data:
            ph = soil_data['phh2o'] / 10  # Convert from pH*10 to pH
            if ph < 6.0:
                interpretation.append(f"🔴 Soil is acidic (pH: {ph:.1f})")
                recommendations.append("Consider adding lime to reduce acidity")
            elif ph > 8.0:
                interpretation.append(f"🔵 Soil is alkaline (pH: {ph:.1f})")
                recommendations.append("Consider adding organic matter or sulfur")
            else:
                interpretation.append(f"🟢 Soil pH is good (pH: {ph:.1f})")
        
        # Organic carbon
        if 'soc' in soil_data:
            soc = soil_data['soc'] / 10  # Convert to g/kg
            if soc < 10:
                interpretation.append(f"🔴 Low organic matter ({soc:.1f} g/kg)")
                recommendations.append("Add compost or organic fertilizers")
            elif soc > 30:
                interpretation.append(f"🟢 High organic matter ({soc:.1f} g/kg)")
            else:
                interpretation.append(f"🟡 Moderate organic matter ({soc:.1f} g/kg)")
        
        # Soil texture
        if all(k in soil_data for k in ['sand', 'clay', 'silt']):
            sand = soil_data['sand'] / 10
            clay = soil_data['clay'] / 10
            silt = soil_data['silt'] / 10
            
            if clay > 40:
                interpretation.append("🟤 Clay soil - good for water retention")
                recommendations.append("Ensure good drainage, avoid overwatering")
            elif sand > 60:
                interpretation.append("🟡 Sandy soil - good drainage")
                recommendations.append("Water more frequently, add organic matter")
            else:
                interpretation.append("🟢 Loamy soil - ideal for most crops")
        
        # Nitrogen
        if 'nitrogen' in soil_data:
            nitrogen = soil_data['nitrogen'] / 100  # Convert to g/kg
            if nitrogen < 1:
                interpretation.append(f"🔴 Low nitrogen ({nitrogen:.2f} g/kg)")
                recommendations.append("Apply nitrogen-rich fertilizers")
            else:
                interpretation.append(f"🟢 Adequate nitrogen ({nitrogen:.2f} g/kg)")
        
        result = f"""
        🌱 Soil Analysis Results:
        
        {chr(10).join([f'• {item}' for item in interpretation])}
        
        🧑‍🌾 Recommendations:
        {chr(10).join([f'• {rec}' for rec in recommendations]) if recommendations else '• Your soil conditions are generally good for farming.'}
        """
        
        return result
    
    def create_soil_chart(self, soil_data):
        """Create soil composition visualization."""
        if not soil_data or not all(k in soil_data for k in ['sand', 'clay', 'silt']):
            return None
        
        # Convert to percentages
        sand = soil_data['sand'] / 10
        clay = soil_data['clay'] / 10
        silt = soil_data['silt'] / 10
        
        # Create pie chart for soil texture
        labels = ['Sand', 'Clay', 'Silt']
        values = [sand, clay, silt]
        colors = ['#F4A460', '#8B4513', '#DEB887']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker_colors=colors,
            textinfo='label+percent',
            textfont_size=12
        )])
        
        fig.update_layout(
            title="Soil Texture Composition",
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_soil_properties_chart(self, soil_data):
        """Create chart for soil properties."""
        if not soil_data:
            return None
        
        properties = []
        values = []
        colors = []
        
        if 'phh2o' in soil_data:
            ph = soil_data['phh2o'] / 10
            properties.append('pH')
            values.append(ph)
            colors.append('#FF6B6B' if ph < 6 or ph > 8 else '#4ECDC4')
        
        if 'soc' in soil_data:
            soc = soil_data['soc'] / 10
            properties.append('Organic Carbon (g/kg)')
            values.append(soc)
            colors.append('#FF6B6B' if soc < 10 else '#4ECDC4')
        
        if 'nitrogen' in soil_data:
            nitrogen = soil_data['nitrogen'] / 100
            properties.append('Nitrogen (g/kg)')
            values.append(nitrogen)
            colors.append('#FF6B6B' if nitrogen < 1 else '#4ECDC4')
        
        if properties:
            fig = go.Figure(data=[go.Bar(
                x=properties,
                y=values,
                marker_color=colors,
                text=[f'{v:.2f}' for v in values],
                textposition='auto'
            )])
            
            fig.update_layout(
                title="Soil Properties",
                height=400,
                yaxis_title="Value"
            )
            
            return fig
        
        return None

# Global soil service instance
soil_service = SoilService()