import sys

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False

css = """
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #f8fafc;
}
.stApp {
    background-color: #0f172a;
}
[data-testid="stSidebar"] {
    background-color: #1e293b;
}
[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
    color: #ffffff !important;
}
[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 1.25rem;
    border-radius: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -1px rgba(0, 0, 0, 0.3);
    border: 1px solid #334155;
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
}
[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
}
h1, h2, h3, h4, h5, h6 {
    color: #f8fafc !important;
    font-weight: 700 !important;
}
p, span, div {
    color: #f8fafc;
}
div.stButton > button, div.stTabs [data-baseweb="tab"] {
    background-color: #1e293b;
    color: #cbd5e1;
    border: 1px solid #334155;
    border-radius: 8px;
    font-weight: 500;
    padding: 0.5rem 1rem;
}
div.stTabs [aria-selected="true"] {
    background-color: #3b82f6;
    color: #ffffff !important;
}
hr {
    border-color: #334155;
}
</style>
''', unsafe_allow_html=True)
"""

tab_str = """
# --- TABS ---
tab_reg, tab_demo, tab_health, tab_ben, tab_sch, tab_trend, tab_multi = st.tabs([
    "Regional", "Demographics", "Health Conditions", "Beneficiaries", "Schools", "Trends", "Multivariate"
])

with tab_demo:
    st.subheader("Analisis Demografi Siswa")
    st.markdown("Perbandingan jumlah siswa Laki-laki dan Perempuan.")
    df_demo = pd.DataFrame({
        'Gender': ['Laki-laki', 'Perempuan'],
        'Jumlah': [df_filtered['jumlah_laki'].sum(), df_filtered['jumlah_perempuan'].sum()]
    })
    fig_demo = px.pie(df_demo, values='Jumlah', names='Gender', hole=0.4, color='Gender', color_discrete_map={'Laki-laki':'#3b82f6', 'Perempuan':'#ec4899'})
    st.plotly_chart(fig_demo, use_container_width=True)

with tab_trend:
    st.subheader("Analisis Tren")
    st.markdown("Tren fasilitas dan penerima manfaat.")
    if 'tahun' in df_filtered.columns and len(df_filtered['tahun'].unique()) > 0:
        df_trend = df_filtered.groupby('tahun')[['jumlah_satuan_pendidikan', 'jumlah_penerima_manfaat']].sum().reset_index()
        fig_trend = px.line(df_trend, x='tahun', y=['jumlah_satuan_pendidikan', 'jumlah_penerima_manfaat'], markers=True)
        fig_trend.update_xaxes(type='category')
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Data histori tren tidak cukup untuk ditampilkan.")

"""

i = 0
current_tab = None

while i < len(lines):
    line = lines[i]
    
    if 'st.set_page_config' in line:
        new_lines.append(line)
        new_lines.append(css)
        i += 1
        continue
        
    if 'st.title("Dashboard Business' in line:
        new_lines.append('st.title("MBG Dashboard - Executive Overview")\n')
        i += 1
        continue
        
    # Filters
    if line.startswith("# Filter Provinsi"):
        new_lines.append("""# Filter Tahun
if 'tahun' in df.columns:
    tahun_options = sorted(df['tahun'].unique())
    tahun = st.sidebar.multiselect("Pilih Tahun", options=tahun_options, default=tahun_options)
    df_tahun_filtered = df[df['tahun'].isin(tahun)]
else:
    df_tahun_filtered = df
    tahun = []

# Filter Provinsi
provinsi_options = sorted(df_tahun_filtered['provinsi'].unique())
provinsi = st.sidebar.multiselect("Pilih Provinsi", options=provinsi_options, default=provinsi_options)

# Filter Kabupaten/Kota (Dinamis berdasarkan Provinsi)
df_prov_filtered = df_tahun_filtered[df_tahun_filtered['provinsi'].isin(provinsi)]
kab_kota_options = sorted(df_prov_filtered['kabupaten_kota'].unique())
kab_kota = st.sidebar.multiselect("Pilih Kabupaten/Kota", options=kab_kota_options, default=kab_kota_options)

# Filter Kecamatan (Dinamis berdasarkan Kab/Kota)
df_kab_filtered = df_prov_filtered[df_prov_filtered['kabupaten_kota'].isin(kab_kota)]
kecamatan_options = sorted(df_kab_filtered['kecamatan'].unique())
kecamatan = st.sidebar.multiselect("Pilih Kecamatan", options=kecamatan_options, default=kecamatan_options)

# Filter Jenjang
jenjang_options = sorted(df_tahun_filtered['jenjang'].unique())
jenjang = st.sidebar.multiselect("Pilih Jenjang Pendidikan", options=jenjang_options, default=jenjang_options)

st.sidebar.divider()
status_sekolah = st.sidebar.multiselect("Status Sekolah", options=['Negeri', 'Swasta'], default=['Negeri', 'Swasta'])
sembunyikan_anomali = st.sidebar.checkbox("Sembunyikan Data Anomali", value=False)

# Terapkan filter akhir ke dataframe
filter_kondisi = (
    (df['provinsi'].isin(provinsi)) &
    (df['kabupaten_kota'].isin(kab_kota)) & 
    (df['kecamatan'].isin(kecamatan)) & 
    (df['jenjang'].isin(jenjang))
)
if 'tahun' in df.columns:
    filter_kondisi = filter_kondisi & (df['tahun'].isin(tahun))
if 'Negeri' not in status_sekolah:
    filter_kondisi = filter_kondisi & (df['jumlah_satpen_swasta'] > 0)
if 'Swasta' not in status_sekolah:
    filter_kondisi = filter_kondisi & (df['jumlah_satpen_negeri'] > 0)

df_filtered = df[filter_kondisi].copy()
""")
        # Skip original filters
        while not line.startswith("# Jika toggle aktif"):
            i += 1
            line = lines[i]
        continue

    # Exec Summary
    if line.startswith("# --- METRIK UTAMA"):
        new_lines.append("""# --- METRIK UTAMA (KPI) ---
st.subheader("Ringkasan Eksekutif")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Satuan Pendidikan", f"{df_filtered['jumlah_satuan_pendidikan'].sum():,}")
col2.metric("Total Laki-laki", f"{df_filtered['jumlah_laki'].sum():,}")
col3.metric("Total Perempuan", f"{df_filtered['jumlah_perempuan'].sum():,}")
total_penerima = df_filtered['jumlah_penerima_manfaat'].sum() if 'jumlah_penerima_manfaat' in df_filtered.columns else 0
col4.metric("Total Penerima Manfaat", f"{total_penerima:,}")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Total Kondisi Khusus", f"{df_filtered['jumlah_kondisi_khusus'].sum():,}")
col6.metric("Total Sekolah Negeri", f"{df_filtered['jumlah_satpen_negeri'].sum():,}")
col7.metric("Total Sekolah Swasta", f"{df_filtered['jumlah_satpen_swasta'].sum():,}")
col8.metric("Total Kecamatan", f"{df_filtered['kecamatan'].nunique():,}")

st.divider()
""")
        new_lines.append(tab_str)
        # skip to # --- VISUALISASI ---
        while not line.startswith("# --- VISUALISASI ---"):
            i += 1
            line = lines[i]
        continue
        
    # Routing Tabs
    if line.startswith("# --- VISUALISASI ---"):
        current_tab = "with tab_reg:\n"
        new_lines.append(current_tab)
        i += 1
        continue
        
    if line.startswith("col_vis1, col_vis2 = st.columns(2)"):
        current_tab = "with tab_health:\n"
        new_lines.append(current_tab)
        new_lines.append("    col_vis1, col_vis2 = st.columns(2)\n")
        i += 1
        continue
        
    if line.startswith("col_vis3, col_vis4 = st.columns(2)"):
        # This is where we break into Schools and Beneficiaries
        i += 1
        continue
        
    if line.startswith("with col_vis3:"):
        current_tab = "with tab_sch:\n"
        new_lines.append(current_tab)
        i += 1
        continue
        
    if line.startswith("with col_vis4:"):
        current_tab = "with tab_ben:\n"
        new_lines.append(current_tab)
        i += 1
        continue
        
    if line.startswith("col_multi1, col_multi2 = st.columns(2)"):
        # Ignore these column wrappers too
        i += 1
        continue
        
    if line.startswith("with col_multi1:"):
        current_tab = "with tab_multi:\n"
        new_lines.append(current_tab)
        i += 1
        continue
        
    if line.startswith("with col_multi2:"):
        # We put treemap in sch tab
        current_tab = "with tab_sch:\n"
        new_lines.append(current_tab)
        i += 1
        continue
        
    if line.startswith("st.subheader(\"Alur Keterkaitan Parameter"):
        current_tab = "with tab_multi:\n"
        new_lines.append(current_tab)
        new_lines.append("    " + line)
        i += 1
        continue
        
    if line.startswith("st.divider()"):
        # Ignore top-level dividers as tabs handle spacing nicely
        if current_tab:
            i += 1
            continue
            
    if line.startswith("# --- TABEL DATA"):
        current_tab = None
        new_lines.append(line)
        i += 1
        continue
        
    if current_tab:
        if line.strip() == "":
            new_lines.append(line)
        else:
            new_lines.append("    " + line)
    else:
        new_lines.append(line)
        
    i += 1

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
