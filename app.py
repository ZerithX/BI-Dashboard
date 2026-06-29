import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.io as pio
from pathlib import Path

# Tema bawaan Plotly agar sesuai dengan antarmuka terang
pio.templates.default = "plotly_white"

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Analisis MBG", page_icon="🍱", layout="wide")

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
/* Style metric cards */
[data-testid="stMetric"] {
    background-color: #ffffff;
    padding: 1.25rem;
    border-radius: 1rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.15);
    border: 2px solid #94a3b8;
}
[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
}
[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
}
</style>
''', unsafe_allow_html=True)

st.title("MBG Dashboard - Executive Overview")
st.markdown("Prototipe dashboard interaktif untuk memantau sebaran fasilitas pendidikan, kerentanan medis siswa, dan anomali data operasional.")

# --- SIDEBAR MENU ---
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

# --- MEMUAT DATA ---
DEFAULT_DATA = "./data/MBG_06-19-2026.csv"

@st.cache_data
def load_data(file_source):
    return pd.read_csv(file_source)

if Path(DEFAULT_DATA).exists():
    df = load_data(DEFAULT_DATA)
else:
    st.error(f"File `{DEFAULT_DATA}` tidak ditemukan di folder proyek. Pastikan file sudah dipindahkan ke folder data.")
    st.stop()

# Koordinat Provinsi
PROV_COORDS = {
    'Prov. Aceh': (4.6951, 96.7494), 'Prov. Sumatera Utara': (2.1154, 99.5451), 'Prov. Sumatera Barat': (-0.7399, 100.8000), 'Prov. Riau': (0.2933, 101.7068), 'Prov. Jambi': (-1.6115, 103.6131), 'Prov. Sumatera Selatan': (-3.3194, 104.9147), 'Prov. Bengkulu': (-3.7928, 102.2608), 'Prov. Lampung': (-4.5586, 105.4068), 'Prov. Kepulauan Bangka Belitung': (-2.7411, 106.4406), 'Prov. Kepulauan Riau': (3.9456, 108.1429), 'Prov. D.K.I. Jakarta': (-6.2088, 106.8456), 'Prov. Jawa Barat': (-6.9204, 107.6046), 'Prov. Jawa Tengah': (-7.1509, 110.1403), 'Prov. D.I. Yogyakarta': (-7.8753, 110.4262), 'Prov. Jawa Timur': (-7.5361, 112.2384), 'Prov. Banten': (-6.4058, 106.0640), 'Prov. Bali': (-8.4095, 115.1889), 'Prov. Nusa Tenggara Barat': (-8.6529, 117.3616), 'Prov. Nusa Tenggara Timur': (-8.6574, 121.0794), 'Prov. Kalimantan Barat': (-0.2788, 111.4753), 'Prov. Kalimantan Tengah': (-1.6815, 113.3824), 'Prov. Kalimantan Selatan': (-3.0926, 115.2838), 'Prov. Kalimantan Timur': (1.6406, 116.4194), 'Prov. Kalimantan Utara': (3.0731, 116.0414), 'Prov. Sulawesi Utara': (0.6247, 123.9750), 'Prov. Sulawesi Tengah': (-1.4300, 121.4456), 'Prov. Sulawesi Selatan': (-3.6688, 119.9741), 'Prov. Sulawesi Tenggara': (-4.1449, 122.1746), 'Prov. Gorontalo': (0.6999, 122.4467), 'Prov. Sulawesi Barat': (-2.8441, 119.2321), 'Prov. Maluku': (-3.2385, 130.1453), 'Prov. Maluku Utara': (1.5709, 127.8088), 'Prov. Papua': (-4.2699, 138.0803), 'Prov. Papua Barat': (-1.3361, 133.1747), 'Prov. Papua Selatan': (-7.9227, 139.3876), 'Prov. Papua Tengah': (-3.9877, 136.1950), 'Prov. Papua Pegunungan': (-4.2255, 139.0223), 'Prov. Papua Barat Daya': (-1.3340, 132.3392)
}

# --- SIDEBAR: FILTER ---
with st.sidebar:
    st.divider()
    with st.expander("🛠️ Tampilkan Filter Data", expanded=False):
        if 'tahun' in df.columns:
            tahun_options = sorted(df['tahun'].unique())
            tahun = st.multiselect("Pilih Tahun", options=tahun_options, default=tahun_options)
            df_tahun_filtered = df[df['tahun'].isin(tahun)]
        else:
            df_tahun_filtered = df
            tahun = []

        provinsi_options = sorted(df_tahun_filtered['provinsi'].unique())
        provinsi = st.multiselect("Pilih Provinsi", options=provinsi_options, default=provinsi_options)

        df_prov_filtered = df_tahun_filtered[df_tahun_filtered['provinsi'].isin(provinsi)]
        kab_kota_options = sorted(df_prov_filtered['kabupaten_kota'].unique())
        kab_kota = st.multiselect("Pilih Kabupaten/Kota", options=kab_kota_options, default=kab_kota_options)

        df_kab_filtered = df_prov_filtered[df_prov_filtered['kabupaten_kota'].isin(kab_kota)]
        kecamatan_options = sorted(df_kab_filtered['kecamatan'].unique())
        kecamatan = st.multiselect("Pilih Kecamatan", options=kecamatan_options, default=kecamatan_options)

        jenjang_options = sorted(df_tahun_filtered['jenjang'].unique())
        jenjang = st.multiselect("Pilih Jenjang Pendidikan", options=jenjang_options, default=jenjang_options)

        status_sekolah = st.multiselect("Status Sekolah", options=['Negeri', 'Swasta'], default=['Negeri', 'Swasta'])
        sembunyikan_anomali = st.checkbox("Sembunyikan Data Anomali", value=False)

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

if sembunyikan_anomali:
    df_filtered = df_filtered.copy()
    df_filtered['total_siswa_cek'] = df_filtered['jumlah_laki'] + df_filtered['jumlah_perempuan']
    mask_anomali = ((df_filtered['jumlah_alergi'] > 0) | (df_filtered['jumlah_kondisi_khusus'] > 0)) & ((df_filtered['jumlah_penerima_manfaat'] == 0) | (df_filtered['total_siswa_cek'] == 0))
    df_filtered = df_filtered[~mask_anomali]

if selected_tab == "Home":
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

if selected_tab == "Demographics":
    st.subheader("Analisis Demografi Siswa")
    st.markdown("Perbandingan jumlah siswa Laki-laki dan Perempuan berdasarkan wilayah yang difilter.")
    
    jml_laki = df_filtered['jumlah_laki'].sum()
    jml_perempuan = df_filtered['jumlah_perempuan'].sum()
    
    if jml_laki == 0 and jml_perempuan == 0:
        st.warning("Tidak ada data demografi siswa untuk filter saat ini.")
    else:
        df_demo = pd.DataFrame({
            'Gender': ['Laki-laki', 'Perempuan'],
            'Jumlah': [jml_laki, jml_perempuan]
        })
        fig_demo = px.pie(df_demo, values='Jumlah', names='Gender', hole=0.4, color='Gender', color_discrete_map={'Laki-laki':'#3b82f6', 'Perempuan':'#ec4899'})
        fig_demo.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_demo, use_container_width=True)

if selected_tab == "Trends":
    st.subheader("Analisis Tren")
    st.markdown("Tren fasilitas dan penerima manfaat.")
    if 'tahun' in df_filtered.columns and len(df_filtered['tahun'].unique()) > 0:
        df_trend = df_filtered.groupby('tahun')[['jumlah_satuan_pendidikan', 'jumlah_penerima_manfaat']].sum().reset_index()
        if len(df_trend) == 1:
            fig_trend = px.bar(df_trend, x='tahun', y=['jumlah_satuan_pendidikan', 'jumlah_penerima_manfaat'], barmode='group')
        else:
            fig_trend = px.line(df_trend, x='tahun', y=['jumlah_satuan_pendidikan', 'jumlah_penerima_manfaat'], markers=True)
        fig_trend.update_xaxes(type='category')
        fig_trend.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Data histori tren tidak cukup untuk ditampilkan.")

if selected_tab == "Regional":
    st.subheader("Peta Sebaran Wilayah Pendidikan")
    st.markdown("Visualisasi interaktif sebaran fasilitas pendidikan di berbagai level administratif.")

    import hashlib

    def get_synthetic_coord(name, base_lat, base_lon, radius=0.8):
        h1 = int(hashlib.md5((str(name) + "_lat").encode()).hexdigest(), 16) / (16**32)
        h2 = int(hashlib.md5((str(name) + "_lon").encode()).hexdigest(), 16) / (16**32)
        offset_lat = (h1 * 2 - 1) * radius
        offset_lon = (h2 * 2 - 1) * radius
        return base_lat + offset_lat, base_lon + offset_lon

    total_prov = len(df['provinsi'].unique())
    total_kab = len(df_prov_filtered['kabupaten_kota'].unique())

    if len(kecamatan) < len(kecamatan_options) or len(kab_kota) == 1:
        group_col = 'kecamatan'
        hover_name = 'kecamatan'
        radius = 0.05
        groupby_cols = ['kecamatan', 'kabupaten_kota', 'provinsi']
    elif len(kab_kota) < total_kab or len(provinsi) == 1:
        group_col = 'kabupaten_kota'
        hover_name = 'kabupaten_kota'
        radius = 0.5
        groupby_cols = ['kabupaten_kota', 'provinsi']
    else:
        group_col = 'provinsi'
        hover_name = 'provinsi'
        radius = 0
        groupby_cols = ['provinsi']

    df_map = df_filtered.groupby(groupby_cols).agg({'jumlah_satuan_pendidikan': 'sum', 'jumlah_penerima_manfaat': 'sum'}).reset_index()

    if df_map.empty:
        st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
    else:
        def get_real_coord(nama_lokasi, def_lat, def_lon):
            return def_lat, def_lon

        lats, lons = [], []
        for _, row in df_map.iterrows():
            base_lat, base_lon = PROV_COORDS.get(row['provinsi'], (-2.5, 118.0))
            if group_col == 'provinsi':
                lat, lon = get_real_coord(row['provinsi'], base_lat, base_lon)
            elif group_col == 'kabupaten_kota':
                lat, lon = get_synthetic_coord(row['kabupaten_kota'], base_lat, base_lon, radius)
            elif group_col == 'kecamatan':
                kab_lat, kab_lon = get_synthetic_coord(row['kabupaten_kota'], base_lat, base_lon, 0.5)
                lat, lon = get_synthetic_coord(row['kecamatan'], kab_lat, kab_lon, radius)
            lats.append(lat)
            lons.append(lon)
            
        df_map['lat'] = lats
        df_map['lon'] = lons
    
        fig_map = px.scatter_mapbox(
            df_map, 
            lat="lat", 
            lon="lon", 
            size="jumlah_satuan_pendidikan",
            color="jumlah_penerima_manfaat",
            hover_name=hover_name,
            hover_data={"lat": False, "lon": False, "provinsi": True, "jumlah_satuan_pendidikan": True, "jumlah_penerima_manfaat": True},
            color_continuous_scale=px.colors.sequential.Viridis,
            size_max=20,
            zoom=6 if group_col == 'kabupaten_kota' else 9,
            center={"lat": df_map['lat'].mean(), "lon": df_map['lon'].mean()},
            mapbox_style="carto-positron"
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)

if selected_tab == "Health Conditions":
    st.subheader("Analisis Kondisi Khusus & Kerentanan Medis")
    st.markdown("Pemantauan detail jumlah kondisi medis yang dilaporkan oleh sekolah untuk mitigasi risiko penanganan konsumsi makanan.")
    
    hc1, hc2, hc3, hc4 = st.columns(4)
    hc1.metric("Total Alergi", f"{df_filtered['jumlah_alergi'].sum():,}")
    hc2.metric("Total Fobia", f"{df_filtered['jumlah_fobia'].sum():,}")
    hc3.metric("Intoleransi", f"{df_filtered['jumlah_intoleransi'].sum():,}")
    hc4.metric("Kondisi Khusus", f"{df_filtered['jumlah_kondisi_khusus'].sum():,}")
    
    st.divider()
    
    col_vis1, col_vis2 = st.columns(2)
    with col_vis1:
        st.subheader("Peta Kerentanan Medis per Kecamatan")
        st.markdown("Agregasi jenis kondisi yang paling dominan di tiap wilayah.")
        df_medis = df_filtered.groupby('kecamatan')[['jumlah_alergi', 'jumlah_kondisi_khusus', 'jumlah_fobia', 'jumlah_intoleransi']].sum().reset_index()
        df_medis = df_medis[(df_medis['jumlah_alergi'] > 0) | (df_medis['jumlah_kondisi_khusus'] > 0) | (df_medis['jumlah_fobia'] > 0) | (df_medis['jumlah_intoleransi'] > 0)]
    
        fig_medis = px.bar(df_medis, x='kecamatan', y=['jumlah_alergi', 'jumlah_kondisi_khusus', 'jumlah_fobia', 'jumlah_intoleransi'], 
                           barmode='group', labels={'value': 'Jumlah Kasus', 'variable': 'Kategori Risiko'})
        fig_medis.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_medis, use_container_width=True)

    with col_vis2:
        st.subheader("Risiko per Jenjang Pendidikan")
        st.markdown("Membantu penentuan jenjang yang membutuhkan ahli nutrisi spesifik.")
        df_jenjang = df_filtered.groupby('jenjang')[['jumlah_kondisi_khusus', 'jumlah_alergi']].sum().reset_index()
        df_jenjang['Total Risiko'] = df_jenjang['jumlah_kondisi_khusus'] + df_jenjang['jumlah_alergi']
        fig_jenjang = px.pie(df_jenjang, values='Total Risiko', names='jenjang', hole=0.4)
        fig_jenjang.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_jenjang, use_container_width=True)

if selected_tab == "Schools":
    st.subheader("Proporsi Status Sekolah")
    st.markdown("Perbandingan fasilitas negeri vs swasta untuk skema distribusi dan birokrasi.")
    df_status = pd.DataFrame({
        'Status': ['Negeri', 'Swasta'],
        'Jumlah': [df_filtered['jumlah_satpen_negeri'].sum(), df_filtered['jumlah_satpen_swasta'].sum()]
    })
    fig_status = px.bar(df_status, x='Status', y='Jumlah', color='Status', text_auto=True)
    fig_status.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_status, use_container_width=True)
    st.divider()
    
    st.subheader("Distribusi Risiko dalam Hierarki Wilayah (Treemap)")
    st.markdown("Ukuran Kotak: Jumlah Sekolah | Warna: Intensitas Kasus Kondisi Khusus.")
    
    fig_treemap = px.treemap(
        df_filtered,
        path=[px.Constant("Semua Wilayah"), 'kabupaten_kota', 'kecamatan', 'jenjang'],
        values='jumlah_satuan_pendidikan',
        color='jumlah_kondisi_khusus',
        hover_data=['jumlah_alergi', 'jumlah_penerima_manfaat'],
        color_continuous_scale='Reds',
        labels={'jumlah_kondisi_khusus': 'Kondisi Khusus'},
    )
    fig_treemap.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", margin=dict(t=10, l=10, r=10, b=10))
    st.plotly_chart(fig_treemap, use_container_width=True)

if selected_tab == "Beneficiaries":
    st.subheader("Analisis Penerima Manfaat")
    st.markdown("Monitoring penyaluran manfaat dan perbandingan dengan total peserta didik.")
    
    total_siswa_semua = df_filtered['jumlah_laki'].sum() + df_filtered['jumlah_perempuan'].sum()
    total_terima = df_filtered['jumlah_penerima_manfaat'].sum() if 'jumlah_penerima_manfaat' in df_filtered.columns else 0
    total_tidak_terima = total_siswa_semua - total_terima
    
    b1, b2, b3 = st.columns(3)
    b1.metric("Total Siswa Terdaftar", f"{total_siswa_semua:,}")
    b2.metric("Total Penerima Manfaat", f"{total_terima:,}")
    b3.metric("Belum/Tidak Menerima", f"{total_tidak_terima:,}")
    
    st.divider()

    st.subheader("Pemantauan Kualitas Data (Deteksi Anomali)")
    st.markdown("*Flagging* data mencurigakan: Ada penderita Kasus Medis (Alergi/Kondisi Khusus), tetapi *Jumlah Penerima Manfaat* tercatat 0.")
    st.markdown("Harga MBG per porsi Rp15.000")
    
    df_anomali = df_filtered[
        ((df_filtered['jumlah_alergi'] > 0) | (df_filtered['jumlah_kondisi_khusus'] > 0)) & 
        (df_filtered['jumlah_penerima_manfaat'] == 0)
    ].copy()
    
    if not df_anomali.empty:
        df_anomali['Total Kasus Medis Diabaikan'] = df_anomali['jumlah_alergi'] + df_anomali['jumlah_kondisi_khusus']
        df_anomali['Potensi Kerugian (Rp)'] = df_anomali['Total Kasus Medis Diabaikan'] * 15000
        total_kerugian = df_anomali['Potensi Kerugian (Rp)'].sum()
        total_diabaikan = df_anomali['Total Kasus Medis Diabaikan'].sum()
        
        total_kasus_semua = df_filtered['jumlah_alergi'].sum() + df_filtered['jumlah_kondisi_khusus'].sum()
        total_terlayani = max(0, total_kasus_semua - total_diabaikan)
        
        st.warning(f"⚠️ Terdeteksi {len(df_anomali)} wilayah dengan anomali (Siswa berisiko diabaikan).")
        st.metric("Total Potensi Kerugian/Maladministrasi (Per Hari)", f"Rp {total_kerugian:,.0f}")
        
        col_anomali1, col_anomali2 = st.columns([1, 2])
        
        with col_anomali1:
            df_pie_anomali = pd.DataFrame({
                'Status': ['Terlayani', 'Diabaikan (Anomali)'],
                'Jumlah': [total_terlayani, total_diabaikan]
            })
            fig_pie_anomali = px.pie(
                df_pie_anomali, values='Jumlah', names='Status', 
                color='Status', color_discrete_map={'Terlayani':'#00CC96', 'Diabaikan (Anomali)':'#EF553B'},
                hole=0.4, height=280
            )
            fig_pie_anomali.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='#ffffff', plot_bgcolor='#ffffff')
            st.plotly_chart(fig_pie_anomali, use_container_width=True)
            
        with col_anomali2:
            st.dataframe(
                df_anomali[['kabupaten_kota', 'kecamatan', 'jenjang', 'jumlah_alergi', 'jumlah_kondisi_khusus', 'Total Kasus Medis Diabaikan', 'Potensi Kerugian (Rp)']],
                use_container_width=True, hide_index=True, height=280
            )
    else:
        st.success("✅ Tidak terdeteksi anomali data medis yang terabaikan.")

if selected_tab == "Multivariate":
    st.subheader("Korelasi Alergi vs Kondisi Khusus (Bubble Chart)")
    st.markdown("Sumbu X: Alergi | Sumbu Y: Kondisi Khusus | Warna: Jenjang | Ukuran Gelembung: Jumlah Sekolah.")
    
    df_scatter = df_filtered[(df_filtered['jumlah_alergi'] > 0) | (df_filtered['jumlah_kondisi_khusus'] > 0)]
    if df_scatter.empty:
        df_scatter = df_filtered

    fig_scatter = px.scatter(
        df_scatter,
        x="jumlah_alergi",
        y="jumlah_kondisi_khusus",
        size="jumlah_satuan_pendidikan",
        color="jenjang",
        hover_name="kecamatan",
        hover_data=["kabupaten_kota"],
        labels={
            "jumlah_alergi": "Total Kasus Alergi",
            "jumlah_kondisi_khusus": "Total Kondisi Khusus",
            "jumlah_satuan_pendidikan": "Kapasitas Sekolah",
            "jenjang": "Jenjang"
        },
        size_max=40,
    )
    fig_scatter.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.divider()
    st.subheader("Alur Keterkaitan Parameter (Parallel Categories)")
    st.markdown("Menganalisis hubungan antara Jenjang Pendidikan, Status Kepemilikan Mayoritas Sekolah, Tingkat Cakupan MBG, dan Risiko Medis.")

    df_pc = df_filtered.copy()
    def get_dominasi(negeri, swasta):
        if negeri > swasta:
            return 'Mayoritas Negeri'
        elif swasta > negeri:
            return 'Mayoritas Swasta'
        else:
            return 'Berimbang'

    df_pc['Status Dominan'] = df_pc.apply(lambda row: get_dominasi(row['jumlah_satpen_negeri'], row['jumlah_satpen_swasta']), axis=1)

    def cakupan_mbg(penerima, total_sekolah):
        if total_sekolah == 0: return 'Tidak Jelas'
        avg = penerima / total_sekolah
        if avg > 100: return 'Tinggi'
        elif avg > 50: return 'Sedang'
        else: return 'Rendah'

    df_pc['Cakupan MBG'] = df_pc.apply(lambda row: cakupan_mbg(row['jumlah_penerima_manfaat'], row['jumlah_satuan_pendidikan']), axis=1)

    def tingkat_risiko(alergi, khusus):
        total = alergi + khusus
        if total > 50: return 'Tinggi'
        elif total > 10: return 'Sedang'
        else: return 'Rendah'

    df_pc['Tingkat Risiko Medis'] = df_pc.apply(lambda row: tingkat_risiko(row['jumlah_alergi'], row['jumlah_kondisi_khusus']), axis=1)

    df_pc_grouped = df_pc.groupby(['jenjang', 'Status Dominan', 'Cakupan MBG', 'Tingkat Risiko Medis']).size().reset_index(name='Jumlah Wilayah')

    fig_pc = px.parallel_categories(
        df_pc_grouped,
        dimensions=['jenjang', 'Status Dominan', 'Cakupan MBG', 'Tingkat Risiko Medis'],
        color="Jumlah Wilayah",
        color_continuous_scale=px.colors.sequential.Teal,
        labels={
            'jenjang': 'Jenjang Pendidikan', 
            'Status Dominan': 'Status Kepemilikan Mayoritas', 
            'Cakupan MBG': 'Cakupan Distribusi', 
            'Tingkat Risiko Medis': 'Risiko Medis'
        }
    )
    fig_pc.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", margin=dict(t=30, b=30, l=30, r=30))
    st.plotly_chart(fig_pc, use_container_width=True)
    
    st.divider()
    st.subheader("Matriks Korelasi (Heatmap)")
    st.markdown("Korelasi antara berbagai parameter numerik untuk menemukan pola tersembunyi.")
    
    cols_corr = ['jumlah_satuan_pendidikan', 'jumlah_laki', 'jumlah_perempuan', 'jumlah_alergi', 'jumlah_kondisi_khusus', 'jumlah_penerima_manfaat']
    if all(col in df_filtered.columns for col in cols_corr):
        df_corr = df_filtered[cols_corr].corr()
        fig_corr = px.imshow(df_corr, text_auto=".2f", color_continuous_scale='Blues', aspect='auto')
        fig_corr.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_corr, use_container_width=True)

st.divider()
st.subheader("Data Rinci")
st.dataframe(df_filtered, use_container_width=True)