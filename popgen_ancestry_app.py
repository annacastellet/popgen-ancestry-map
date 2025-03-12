#!/usr/bin/python3

'''
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
'''

import streamlit as st
import pandas as pd
import plotly.express as px

# Read the input Excel file
df = pd.read_excel(r"\\wsl.localhost\Ubuntu\home\annac\binp29\popgen_project\modern_ancestry_in_populations.xlsx")

# Start the streamlit app
st.title("Modern Ancestries in Populations")

# Plot the map
fig = px.scatter_mapbox(
    df,
    lat="Lat",
    lon="Long",
    hover_name="Pop",
    size_max=50, # Set circles sizes
    color_discrete_sequence=["red"], # Set circles colors (temporary)
    zoom=1, # How close or far the map is initially displayed (between 1 and 2 is okay for wide global view)
    height=600 # Vertical size of the map in pizels
)
fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig)

# Create a dropdown menu with selectbox(), where you can select a population
selected_pop = st.selectbox("Select a Population", df["Pop"].unique())

# Show pie chart for ancestry breakdown
if selected_pop:
    ancestry_data = df[df["Pop"] == selected_pop].iloc[:, 4:].T  # Extract df columns that corresponds to the ancestry
    ancestry_data.columns = ["Percentage"]
    ancestry_data = ancestry_data[ancestry_data["Percentage"] > 0]  # Remove zero values
    
    pie_fig = px.pie(
        ancestry_data, 
        names=ancestry_data.index, 
        values="Percentage", 
        title=f"{selected_pop} Ancestry Breakdown"
    )
    st.plotly_chart(pie_fig)