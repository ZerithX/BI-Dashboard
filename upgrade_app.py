import sys

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Import option_menu
if 'from streamlit_option_menu import option_menu' not in content:
    content = content.replace('import streamlit as st', 'import streamlit as st\nfrom streamlit_option_menu import option_menu')

# 2. Replace the CSS block
# We will just replace everything between <style> and </style> with a cleaner version that focuses on cards.
import re
new_css = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
/* Style metric cards */
[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 1.25rem;
    border-radius: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
    border: 1px solid #334155;
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
}
[data-testid="stMetricValue"] {
    font-weight: 700 !important;
    font-size: 1.5rem !important;
}
</style>"""
content = re.sub(r'<style>.*?</style>', new_css, content, flags=re.DOTALL)

# 3. Replace tabs with option_menu
tabs_def = """# --- TABS ---
tab_reg, tab_demo, tab_health, tab_ben, tab_sch, tab_trend, tab_multi = st.tabs([
    "Regional", "Demographics", "Health Conditions", "Beneficiaries", "Schools", "Trends", "Multivariate"
])"""

menu_def = """# --- SIDEBAR MENU ---
with st.sidebar:
    selected_tab = option_menu("Menu Utama", 
        ["Regional", "Demographics", "Health Conditions", "Beneficiaries", "Schools", "Trends", "Multivariate"], 
        icons=['map', 'pie-chart', 'heart-pulse', 'people', 'building', 'graph-up', 'bezier2'], 
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "transparent"},
            "icon": {"color": "#3b82f6", "font-size": "20px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#334155"},
            "nav-link-selected": {"background-color": "#3b82f6"},
        }
    )"""
content = content.replace(tabs_def, menu_def)

# Replace 'with tab_xxx:' with 'if selected_tab == "xxx":'
content = content.replace('with tab_reg:', 'if selected_tab == "Regional":')
content = content.replace('with tab_demo:', 'if selected_tab == "Demographics":')
content = content.replace('with tab_health:', 'if selected_tab == "Health Conditions":')
content = content.replace('with tab_ben:', 'if selected_tab == "Beneficiaries":')
content = content.replace('with tab_sch:', 'if selected_tab == "Schools":')
content = content.replace('with tab_trend:', 'if selected_tab == "Trends":')
content = content.replace('with tab_multi:', 'if selected_tab == "Multivariate":')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
