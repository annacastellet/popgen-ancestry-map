#!/usr/bin/python3

from folium.elements import MacroElement
from jinja2 import Template

def add_legend(m):
    """
    Adds a draggable legend to the provided folium map.
    
    The legend includes:
    - Symbols representing different types of areas and routes.
    - A color gradient representing scaled genetic distances.
    
    Parameters:
    m (folium.Map, optional): An existing Folium map object to plot on.
    
    Returns:
    m : The map object with the legend added.
    """
    template = """
    {% macro html(this, kwargs) %}
    <div id='maplegend' class='maplegend'
    style='position: absolute; z-index: 9999; background-color: rgba(255, 255, 255, 0.5);
    border-radius: 6px; padding: 10px; font-size: 10.5px; width: 180px; height: 110px; right: 20px; top: 20px; cursor: move;'>
    <div class='legend-scale'>
    <ul class='legend-labels'>
    <li><svg height="12" width="12">
    <polygon points="5,0 10,3.33 10,8.67 5,12 0,8.67 0,3.33" style="fill:none;opacity: 0.5;stroke:black" />
    </svg>Area with Samples</li>
    <li><svg height="12" width="12">
    <polygon points="5,0 10,3.33 10,8.67 5,12 0,8.67 0,3.33" style="fill:black;opacity: 0.6;stroke:none" />
    </svg>Isolated Population</li>
    <li><svg height="12" width="10"><line x1="0" y1="2" x2="10" y2="10" style="stroke:green;stroke-width:2" /></svg>Possible Migration Route</li>
    </ul>
    </div>
    <div class='legend-gradient'>
    <span style="font-weight: bold;">Scaled Genetic Distances (log2)</span>
    <span style='background: linear-gradient(to right,
    rgb(237, 201, 175) 0%, /* Sand yellow */
    rgb(255, 165, 0) 50%, /* Orange */
    rgb(139, 0, 0) 100% /* Dark red */
    );
    width: 100%; height: 10px; display: block;'></span>
    <div style='display: flex; justify-content: space-between;'>
    <span>-1</span>
    <span>0</span>
    <span>1</span>
    </div>
    </div>
    </div>
    <style type='text/css'>
    .maplegend .legend-scale ul {margin: 0; padding: 0; color: #0f0f0f;}
    .maplegend .legend-scale ul li {list-style: none; line-height: 18px; margin-bottom: 1.5px;}
    .maplegend ul.legend-labels li span {float: left; height: 12px; width: 12px; margin-right: 4.5px;}
    .maplegend ul.legend-labels li svg {margin-right: 4.5px;}
    </style>
    <script type='text/javascript'>
    dragElement(document.getElementById('maplegend'));

    function dragElement(element) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    if (document.getElementById(element.id + "header")) {

    document.getElementById(element.id + "header").onmousedown = dragMouseDown;
    } else {

    element.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    element.style.top = (element.offsetTop - pos2) + "px";
    element.style.left = (element.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
    }
    }
    </script>
    {% endmacro %}
    """
    macro = MacroElement()
    macro._template = Template(template)

    macro.add_to(m)
    return m
