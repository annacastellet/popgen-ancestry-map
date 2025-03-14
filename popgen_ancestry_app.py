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

Date of creation: 10/03/2025 
Author: Anna Castellet
"""

#################
### IMPORTING ###
#################

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

# Import the add_legend function from legend.py
from legend import add_legend

#################
### FUNCTIONS ###
#################

def custom_autopct(pct: float, threshold: float = 5.0) -> str:
    """
    Displays the slice percentage in the pie chart depending on a threshold.
    
    Args:
        pct (float): The percentage value of a pie slice, matplotlib inputs it directly
        threshold (float, optional): The minimum percentage required to display the label. Default 5.0%
    
    Returns:
        str: Formatted percentage string or an empty string if below the threshold
    """
    if pct >= threshold:
        return f"{pct:.1f}%"
    else:
        return ""


def extract_ancestry_values(population: pd.Series, ancestries: list[str]) -> tuple[list[str], list[float]]:
    """
    Extracts and filters ancestry percentages from a population (row) of the dataset.
    
    Args:
        population (pd.Series): A single row of the data frame representing one population
        ancestry_columns (list[str]): A list of column names that represent the ancestry information (percentages) for the population
    
    Returns:
        tuple[list[str], list[float]]: A tuple containing two lists:
            - List of ancestry labels (column names) that have values greater than 0.
            - List of corresponding values (percentages) for the selected ancestry labels.
    """
    # Create an empty dictionary to store ancestry percentages that are greater than 0
    ancestry_values = {}

    # For each ancestry, get the value 
    for value in ancestries:
        single_ancestry_value = population[value]
    
        # Only add the column to the dictionary if its value is greater than 0
        if single_ancestry_value > 0:
            ancestry_values[value] = single_ancestry_value
            
    return list(ancestry_values.keys()), list(ancestry_values.values())


def create_pie_chart(ancestry_labels: list[str], ancestry_percentages: list[float], ancestry_colors: dict[str, str]) -> str:
    """
    Generates a pie chart image and converts it to a base64-encoded string.
    
    Args:
        ancestry_labels (list[str]): List of ancestry labels
        ancestry_percentages (list[float]): Corresponding percentages for each ancestry
        ancestry_colors (dict[str, str]): Mapping of ancestries to their respective colors
    
    Returns:
        str: Base64-encoded string of the pie chart image
    """
    
    colors = []
    for label in ancestry_labels:
        colors.append(ancestry_colors[label])

    # Plot the pie chart
    fig, ax = plt.subplots(figsize=(5, 5))    
    wedges, _, _ = ax.pie( # only going to use wedges (which is each pie chart segment), ignoring the other two variables that the functinon returns
        ancestry_percentages, 
        # autopct expects a function that will be called later for each slice
        autopct=lambda pct: custom_autopct(pct, 5.0), 
        startangle=90, 
        colors=colors,
        textprops={"fontsize": 14}, 
        pctdistance=0.6 # position of the percentage inside the piechart, 1.2 to put it out the pirchart
    )
    
    # "equal" aspect ratio ensures that pie is drawn as a circle
    ax.axis("equal") 
        
    # Add pie chart legend (individual for each piechart)
    ax.legend(
        wedges, # Recall that wedges are the slices
        ancestry_labels,
        fontsize=14,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        frameon=False # Hide the frame around the legend
    )
    
    # Prepare the pie chart PNG in memory (in a temporary bufer)
    buf = io.BytesIO() # Create an in-memory buffer where the generated pie chart will be stored temporarily in a binary format
    fig.tight_layout(pad=1.0)  # Adjusts the whole plot layout to avoid clipping/stretching of the piechart
    # Save the figure to the buffer, ensuring the legend is included
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.2) # "tight" to avoid innecesary blank spaces around the figure
    buf.seek(0) # Resets the buffer's file pointer to the beggining of the file, to ensure proper reading of the PNG
    
    # Convert the PNG that is stored in the buffer in a binary format to base64 string (to embed in HTML)
    img_str = base64.b64encode(buf.getvalue()).decode("utf8")
    
    return img_str


def create_ancestry_map(df: pd.DataFrame, ancestry_columns: list[str]) -> folium.Map:
    """
    Creates an interactive ancestry map (folium object) with population markers.
    
    Args:
        df (pd.DataFrame): The dataset containing population and ancestry information
        ancestry_columns (list[str]): List of ancestry column names
    
    Returns:
        folium.Map: A Folium map with population markers and pie chart popups
    """
    # Find the center of the map based on the location of the populations
    map_center = [df["Lat"].mean(), df["Long"].mean()]
     
    # Generate a color palette with as many colors as there are ancestry columns
    color_palette = sns.color_palette("Set2", len(ancestry_columns))
    # Convert the color palette to hexadecimal format
    hex_colors = color_palette.as_hex()
    # Create a dictionary that maps each ancestry column to a specific color
    ancestry_colors = dict(zip(ancestry_columns, hex_colors))
    
    # Create the map object with folium
    m = folium.Map(location=map_center, zoom_start=2, tiles="Cartodb Positron", width="100%", height="600px")
    
    # Add legend to the map using the function written in the legend.py code
    m = add_legend(m, ancestry_colors, df, ancestry_columns)
    
    # Iterating through every row of the dataset
    for _, population in df.iterrows(): # iterrows() returns both the index and the row, ignoring the index variable (_)
        # Extract the ancestry labels and their values (percentages)
        labels, values = extract_ancestry_values(population, ancestry_columns)
        
        # Find the dominant ancestry of each population
        if labels:
            # Find the label with the maximum ancestry value
            dominant_ancestry = max(labels, key=lambda label: population[label]) # lambda takes the label and returns the corresponding value, that is passed to max()
        else:
            # If there are no valid labels, set dominant_ancestry to None
            dominant_ancestry = None
        
        # Find the corresponding color for the dominant ancestry, if not found use grey (#808080)
        marker_color = ancestry_colors.get(dominant_ancestry, "#808080")
        
        # Generate the pie chart for each population
        pie_chart_img = create_pie_chart(labels, values, ancestry_colors)
        
        # Write the HTML content of the popup for each marker on the map (title and the PNG image)
        popup_html = f"""
        <html>
            <body>
                <h4 style="text-align:center; font-weight:bold;">{population["Pop"]}</h4>
                <img src="data:image/png;base64,{pie_chart_img}" width="300" height="300"/>
            </body>
        </html>
        """
        
        # Create markers in the map in each population location
        folium.CircleMarker(
            location=[population["Lat"], population["Long"]],
            radius=10,
            color=marker_color, # Dominant ancestry color
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.5,
            popup=folium.Popup(popup_html, max_width=350) # Displays the ancestry pie chart when the marker is clicked
        ).add_to(m)

    return m


#################
### MAIN CODE ###
#################

st.title("Population Ancestry Map")

# Streamlit File Uploader to allow the user to select an Excel file from any directory
uploaded_file = st.file_uploader("Choose the Excel file that contains your ancestry breakdown", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
    
    # Display the header of the dataset
    st.write("File successfully uploaded. Here is a preview:")
    st.dataframe(df.head())
    
    # Define columns to exclude from the dataset (everything but the ancestries)
    excluded_columns = {"Pop", "Lat", "Long", "Continent"}
    # Filter ancestry columns
    ancestry_columns = []
    for col in df.columns:
        if col not in excluded_columns:
            ancestry_columns.append(col)
    
    # Create the Folium map object with the data from the dataframe and the selected ancestry columns
    ancestry_map = create_ancestry_map(df, ancestry_columns)
    
    # Embed the Folium map inside a Streamlit app
    folium_static(ancestry_map)

else:
    st.write("Please upload an Excel file to get your ancestry breakdown map :)")