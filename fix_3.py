import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

# 1. Enhance CSS for Metric Cards to make them highly contrasting
old_css = """[data-testid="stMetric"] {
    background-color: #ffffff;
    padding: 1.25rem;
    border-radius: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border: 1px solid #e2e8f0;
}"""
new_css = """[data-testid="stMetric"] {
    background-color: #ffffff;
    padding: 1.25rem;
    border-radius: 1rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.15);
    border: 2px solid #94a3b8;
}"""
content = content.replace(old_css, new_css)

# 2. Revert Popover to Expander
old_filter = """# --- SIDEBAR: FILTER ---
with st.sidebar:
    st.divider()
    # Gunakan st.popover agar menu terbuka menimpa konten bukan mendorong ke bawah
    with st.popover("🛠️ Tampilkan Filter Data", use_container_width=True):"""
new_filter = """# --- SIDEBAR: FILTER ---
with st.sidebar:
    st.divider()
    with st.expander("🛠️ Tampilkan Filter Data", expanded=False):"""
content = content.replace(old_filter, new_filter)

# 3. Fix Map visibility (Remove paper_bgcolor and plot_bgcolor from fig_map)
old_map = 'fig_map.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", margin={"r":0,"t":0,"l":0,"b":0})'
new_map = 'fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})'
content = content.replace(old_map, new_map)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)
