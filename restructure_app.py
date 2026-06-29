import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

# 1. Update plotly template to white
content = content.replace('pio.templates.default = "plotly_dark"', 'pio.templates.default = "plotly_white"')

# 2. Update CSS for metric cards
content = content.replace('background-color: #1e293b;', 'background-color: #ffffff;')
content = content.replace('box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);', 'box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);')
content = content.replace('border: 1px solid #334155;', 'border: 1px solid #e2e8f0;')
content = content.replace('color: #94a3b8 !important;', 'color: #64748b !important;')
content = content.replace('font-weight: 700 !important;\n    font-size: 1.5rem !important;', 'color: #0f172a !important;\n    font-weight: 700 !important;\n    font-size: 1.5rem !important;')

# Remove emojis from metric labels
content = content.replace('🤒 ', '').replace('😨 ', '').replace('🤢 ', '').replace('♿ ', '').replace('👥 ', '').replace('✅ ', '').replace('❌ ', '')

# 3. Sidebar Option Menu updates
old_menu = """    selected_tab = option_menu("Menu Utama", 
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
new_menu = """    selected_tab = option_menu("Menu Utama", 
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
content = content.replace(old_menu, new_menu)

# Move Sidebar Menu ABOVE filters.
# Currently, Sidebar menu is defined after METRIK UTAMA. We need to move it to just after st.title
sidebar_menu_block_match = re.search(r'# --- SIDEBAR MENU ---.*?\)', content, re.DOTALL)
if sidebar_menu_block_match:
    sidebar_menu_block = sidebar_menu_block_match.group(0)
    # Remove it from its current place
    content = content.replace(sidebar_menu_block + '\n', '')
    
    # Insert it right after st.title
    title_match = re.search(r'st\.title\(.*?\)\n', content)
    if title_match:
        content = content[:title_match.end()] + '\n' + sidebar_menu_block + '\n\n' + content[title_match.end():]

# 4. Wrap filters in Expander
filter_code_start = "# Filter Tahun"
filter_code_end = "df_filtered = df[filter_kondisi].copy()"

# Regex to find everything between filter_code_start and filter_code_end
filter_match = re.search(r'(' + re.escape(filter_code_start) + r'.*?' + re.escape(filter_code_end) + r')', content, re.DOTALL)
if filter_match:
    old_filters = filter_match.group(1)
    # indent old filters
    indented_filters = '\n'.join(['    ' + line if line.strip() else line for line in old_filters.split('\n')])
    new_filters = 'with st.sidebar.expander("Tampilkan Filter Data"):\n' + indented_filters
    content = content.replace(old_filters, new_filters)

# 5. Move Executive Summary to Home Tab
exec_start = "# --- METRIK UTAMA (KPI) ---"
exec_end = "st.divider()"
# Find the exec block
exec_match = re.search(r'(' + re.escape(exec_start) + r'.*?' + re.escape(exec_end) + r')', content, re.DOTALL)
if exec_match:
    old_exec = exec_match.group(1)
    indented_exec = '\n'.join(['    ' + line if line.strip() else line for line in old_exec.split('\n')])
    new_exec = 'if selected_tab == "Home":\n' + indented_exec
    content = content.replace(old_exec, new_exec)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)
