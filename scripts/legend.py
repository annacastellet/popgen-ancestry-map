#!/usr/bin/python3

"""
Script name: legend.py

Description: This program defines a function that adds a draggable legend to a Folium map.
It generates an interactive map that plots populations with pie chart popups showing their ancestry breakdowns, based on the provided dataset.

User-defined functions: add_legend
Modules: folium.elements.MarcoElement, jinja2.Template

Usage: <foliumMapObject> = add_legend(m, ancestry_colors, df, ancestry_columns)
This code is intended to be used as part of a larger mapping application where the map can be displayed with an interactive legend showing dominant ancestries

Created: 13/03/2025
Author: Anna Castellet (adapted from Jaro Steindorff)
"""

from folium.elements import MacroElement
from jinja2 import Template

def add_legend(m, ancestry_colors, df, ancestry_columns, threshold=0.45):
    """
    Adds a draggable legend to the provided folium map, including only the ancestries
    that are dominant in at least one population.
    
    Args:
        m (folium.Map): The Folium map object
        ancestry_colors (dict): Dictionary mapping ancestry names to their colors
        df (pd.DataFrame): The DataFrame containing population data
        ancestry_columns (list): List of ancestry columns
        threshold (float): The threshold percentage to consider an ancestry as dominant (default is 0.45, i.e., 45%)
    
    Returns:
        m : The map object with the legend added
    """
    # Creat a set of ancestries that are dominant in at least one population
    dominant_ancestries = set()

    # Iterating through every row of the dataset
    for _, population in df.iterrows():
        # Create a dictionary of ancestry values for the current population
        ancestry_values = {}
        for col in ancestry_columns:
            ancestry_values[col] = population[col]

        # Find the ancestry with the highest value (percentage)
        max_ancestry = max(ancestry_values, key=ancestry_values.get)

        # If the maximum ancestry value is >= to the threshold, add it to the set of dominant ancestries
        if ancestry_values[max_ancestry] >= threshold:
            dominant_ancestries.add(max_ancestry)

    # Filter the ancestry_colors to include only the ones correspondig to the dominant ancestries
    filtered_ancestry_colors = {}
    # Iterate over each ancestry and its corresponding color
    for ancestry, color in ancestry_colors.items():
        # If the ancestry is in the set of dominant ancestries, add it to the filtered coolors dictionary, which will be used for te legend
        if ancestry in dominant_ancestries:
            filtered_ancestry_colors[ancestry] = color

    # Build the legend items based on the filtered ancestries
    legend_items = "".join(
        f"""
        <li>
            <svg height='12' width='12'>
                <rect width='12' height='12' style='fill:{color}; stroke:black; opacity: 0.8;' />
            </svg>
            {ancestry}
        </li>
        """ for ancestry, color in filtered_ancestry_colors.items()
    )

    template = f"""
    {{% macro html(this, kwargs) %}}
    <div id='maplegend' class='maplegend'
    style='position: absolute; z-index: 9999; background-color: rgba(255, 255, 255, 0.8);
    border-radius: 6px; padding: 10px; font-size: 12px; width: auto; min-width: 150px; right: 20px; top: 20px; cursor: move;'>
    <div class='legend-scale'>
    <ul class='legend-labels'>
    {legend_items}
    </ul>
    </div>
    </div>
    <style type='text/css'>
    .maplegend .legend-scale ul {{margin: 0; padding: 0; color: #0f0f0f;}}
    .maplegend .legend-scale ul li {{list-style: none; line-height: 18px; margin-bottom: 4px;}}
    .maplegend ul.legend-labels li svg {{margin-right: 6px; vertical-align: middle;}}
    </style>
    <script type='text/javascript'>
    dragElement(document.getElementById('maplegend'));

    function dragElement(element) {{
        var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        element.onmousedown = dragMouseDown;
        function dragMouseDown(e) {{
            e = e || window.event;
            e.preventDefault();
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            document.onmousemove = elementDrag;
        }}
        function elementDrag(e) {{
            e = e || window.event;
            e.preventDefault();
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            element.style.top = (element.offsetTop - pos2) + "px";
            element.style.left = (element.offsetLeft - pos1) + "px";
        }}
        function closeDragElement() {{
            document.onmouseup = null;
            document.onmousemove = null;
        }}
    }}
    </script>
    {{% endmacro %}}
    """
    macro = MacroElement()
    macro._template = Template(template)
    macro.add_to(m)
    return m
