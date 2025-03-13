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

# Standard Libraries
import io
import base64

# Third-party Libraries
import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns

# Streamlit File Uploader to allow the user to select an Excel file
uploaded_file = st.file_uploader("Choose the Excel file that contains your ancestry breakdown", type="xlsx")

def custom_autopct(pct):
    '''
    Define custom autopct depending on the value of the percentage
    '''
    if pct >= 5:  # Only show the percentage if it's 2% or more
        return f"{pct:.1f}%"
    else:
        return "" # Don't show anything for slices smaller than 2%


def create_pie_chart(row, ancestry_columns, ancestry_colours):
    # Extract the values for each ancestry column
    ancestry_values = [row[col] for col in ancestry_columns]
    
    # Keep all labels but only plot non-zero slices
    labels = [ancestry_columns[i] for i, value in enumerate(ancestry_values) if value > 0]
    slice_values = [value for value in ancestry_values if value > 0]
    
    # Get the correct colors for the pie chart (same as markers)
    slice_colors = [ancestry_colors[label] for label in labels]
    
    # Debugging: Print the extracted values
    #st.write(f"Ancestry Values for {row['Pop']}: {dict(zip(ancestry_columns, ancestry_values))}")

    # Plot the pie chart
    fig, ax = plt.subplots(figsize=(5, 5))    
    wedges, texts, autotexts = ax.pie(
        slice_values,
        autopct=custom_autopct,
        startangle=90,
        colors=slice_colors,
        textprops={"fontsize": 14},
        pctdistance=0.6
    )
    ax.axis("equal") # Equal aspect ratio ensures that pie is drawn as a circle.
        
    # Add legend inside the pie chart
    ax.legend(
        wedges,
        labels,
        fontsize=14,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1), # Position it outside the figure
        frameon=False # Hide the frame around the legend
    )
    
    # Convert plot to a PNG image to embed in HTML (for popup)
    buf = io.BytesIO()
    fig.tight_layout(pad=1.0)  # Automatically adjusts the layout to avoid clipping/stretching
    # Save the figure to the buffer, ensuring the legend is included
    fig.savefig(buf, format='png', bbox_inches="tight", pad_inches=0.2)
    buf.seek(0)
    
    # Convert PNG to base64 string (to embed in HTML)
    img_str = base64.b64encode(buf.getvalue()).decode("utf8")
    
    return img_str

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip() # Ensure columns are clean
    st.write("File successfully uploaded. Here is a preview:")
    st.dataframe(df.head())
    
    # Start the streamlit app
    st.title("Population Ancestry Map")

    # Dynamically get the ancestry columns (excluding "Pop", "Lat", "Long", and other non-ancestry columns)
    ancestry_columns = [col for col in df.columns if col not in ["Pop", "Lat", "Long", "Continent"]]

    # Create a base map using Folium
    map_center = [df["Lat"].mean(), df["Long"].mean()]
    m = folium.Map(location=map_center, zoom_start=2, width="100%", height="600px")
    
    # Dynamically generate a color palette
    color_palette = sns.color_palette("Set2", len(ancestry_columns)).as_hex()

    # Create a dictionary to map ancestry columns to colors
    ancestry_colors = dict(zip(ancestry_columns, color_palette))

    # Add markers for each population
    for _, row in df.iterrows():
        # Find the ancestry with the highest percentage
        ancestry_values = {col: row[col] for col in ancestry_columns}
        dominant_ancestry = max(ancestry_values, key=ancestry_values.get)  
        marker_color = ancestry_colors.get(dominant_ancestry, '#808080')  # Default to gray if ancestry not found
        #st.write(f"Population: {row['Pop']}, Dominant Ancestry: {dominant_ancestry}, Color: {marker_color}")
        
        # Generate the pie chart for the population based on the ancestry columns
        pie_chart_img = create_pie_chart(row, ancestry_columns, marker_color)
        
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
        folium.CircleMarker(
            location=[row["Lat"], row["Long"]],
            radius=10,
            color=marker_color,
            fill = True,
            fill_color=marker_color,
            fill_opacity=0.5,
            popup=folium.Popup(popup_html, max_width=350)
        ).add_to(m)

    # Display the map
    folium_static(m)
    
else:
    st.write("Please upload an Excel file to get your ancestry breakdown map :)")