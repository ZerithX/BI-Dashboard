import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

menu_block = """# --- SIDEBAR MENU ---
with st.sidebar:
    selected_tab = option_menu("Menu Utama", 
        ["Home", "Regional", "Demographics", "Health Conditions", "Beneficiaries", "Schools", "Trends", "Multivariate"], 
        icons=['house', 'map', 'pie-chart', 'heart-pulse', 'people', 'building', 'graph-up', 'bezier2'], 
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "transparent"},
            "icon": {"color": "#3b82f6", "font-size": "20px"}, 
            "nav-link": {"color": "#1e293b", "font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#e2e8f0"},
            "nav-link-selected": {"background-color": "#3b82f6", "color": "#ffffff"},
        }
    )
"""

# Remove existing menu block (lines 143-156 roughly)
# Instead of regex, I'll just remove the exact string (without trailing whitespace)
old_menu_search = """# --- SIDEBAR MENU ---
with st.sidebar:
    selected_tab = option_menu("Menu Utama", 
        ["Home", "Regional", "Demographics", "Health Conditions", "Beneficiaries", "Schools", "Trends", "Multivariate"], 
        icons=['house', 'map', 'pie-chart', 'heart-pulse', 'people', 'building', 'graph-up', 'bezier2'], 
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "transparent"},
            "icon": {"color": "#3b82f6", "font-size": "20px"}, 
            "nav-link": {"color": "#1e293b", "font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#e2e8f0"},
            "nav-link-selected": {"background-color": "#3b82f6", "color": "#ffffff"},
        }
    )"""
content = content.replace(old_menu_search, "")

# Find st.sidebar.header("Filter Wilayah & Jenjang") and replace it with menu_block + st.sidebar.header
insert_point = '# --- SIDEBAR: FILTER ---'
if insert_point in content:
    content = content.replace(insert_point, menu_block + '\n' + insert_point)

# Also fix the missing 'import streamlit_option_menu' just in case? No, it's there.
# Let's save it.
with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)
