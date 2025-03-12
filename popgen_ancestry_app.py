#!/usr/bin/python3

"""
Script name: popgen_ancestry_app.py

Description:

User-defined functions: 
Standard modules: 
Non-standard modules: 

Procedure:
    1.

Usage: streamlit run popgen_ancestry_app.py

Version: 1.0
Date: 10/03/2025 
Author: Anna Castellet
"""

import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import folium
from folium.plugins import MarkerCluster
import io
import base64


# Read the input Excel file
df = pd.read_excel(r"\\wsl.localhost\Ubuntu\home\annac\binp29\popgen_project\modern_ancestry_in_populations.xlsx")

def create_pie_chart(row, ancestry_columns):
    # Extract the values for each ancestry column
    ancestry_values = [row[col] for col in ancestry_columns]
    
    # Remove zero values and corresponding labels (optional, to only show relevant slices)
    ancestry_values = [val for val in ancestry_values if val > 0]
    labels = [label for label, val in zip(ancestry_columns, ancestry_values) if val > 0]
    
    # Plot the pie chart
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(ancestry_values, labels=labels, autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Convert plot to a PNG image to embed in HTML (for popup)
    buf = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buf)
    buf.seek(0)
    
    # Convert PNG to base64 string (to embed in HTML)
    img_str = base64.b64encode(buf.getvalue()).decode("utf8")
    
    return img_str

# Start the streamlit app
st.title("Modern Ancestries in Populations")

# Dynamically get the ancestry columns (excluding "Pop", "Lat", "Long", and other non-ancestry columns)
ancestry_columns = [col for col in df.columns if col not in ["Pop", "Lat", "Long", "Continent"]]

# Create a base map using Folium
map_center = [df["Lat"].mean(), df["Long"].mean()]
m = folium.Map(location=map_center, zoom_start=1)

# Add a MarkerCluster to group markers on the map
marker_cluster = MarkerCluster().add_to(m)

# Add markers for each population
for _, row in df.iterrows():
    # Generate the pie chart for the population based on the ancestry columns
    pie_chart_img = create_pie_chart(row, ancestry_columns)
    
    # HTML to display the pie chart in the popup
    popup_html = f"""
    <html>
        <body>
            <h4>{row["Pop"]}</h4>
            <img src="data:image/png;base64,{pie_chart_img}" width="300" height="300"/>
        </body>
    </html>
    """
    
    # Add the marker with the pie chart in the popup
    folium.Marker(
        location=[row["Lat"], row["Long"]],
        popup=folium.Popup(popup_html, max_width=350)
    ).add_to(marker_cluster)

# Display the map using Streamlit
folium_static(m)