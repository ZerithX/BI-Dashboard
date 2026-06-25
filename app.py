import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Analisis MBG", page_icon="🍱", layout="wide")

st.title("Dashboard Business Intelligence: Program Makan Bergizi Gratis (MBG)")
st.markdown("Prototipe dashboard interaktif untuk memantau sebaran fasilitas pendidikan, kerentanan medis siswa, dan anomali data operasional.")

# --- MEMUAT DATA ---
DEFAULT_DATA = "./data/MBG_06-19-2026.csv"

@st.cache_data
def load_data(file_source):
    return pd.read_csv(file_source)

# 2. Bypass langsung tanpa kondisi if-else uploader lagi
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
st.sidebar.header("Filter Wilayah & Jenjang")

# Filter Provinsi
provinsi_options = sorted(df['provinsi'].unique())
provinsi = st.sidebar.multiselect("Pilih Provinsi", options=provinsi_options, default=provinsi_options)

# Filter Kabupaten/Kota (Dinamis berdasarkan Provinsi)
df_prov_filtered = df[df['provinsi'].isin(provinsi)]
kab_kota_options = sorted(df_prov_filtered['kabupaten_kota'].unique())
kab_kota = st.sidebar.multiselect("Pilih Kabupaten/Kota", options=kab_kota_options, default=kab_kota_options)

# Filter Kecamatan (Dinamis berdasarkan Kab/Kota)
df_kab_filtered = df_prov_filtered[df_prov_filtered['kabupaten_kota'].isin(kab_kota)]
kecamatan_options = sorted(df_kab_filtered['kecamatan'].unique())
kecamatan = st.sidebar.multiselect("Pilih Kecamatan", options=kecamatan_options, default=kecamatan_options)

# Filter Jenjang
jenjang_options = sorted(df['jenjang'].unique())
jenjang = st.sidebar.multiselect("Pilih Jenjang Pendidikan", options=jenjang_options, default=jenjang_options)

st.sidebar.divider()
sembunyikan_anomali = st.sidebar.checkbox("Sembunyikan Data Anomali", value=False, help="Hapus baris data yang memiliki kasus medis tetapi jumlah murid/penerima manfaatnya 0")

# Terapkan filter akhir ke dataframe
df_filtered = df[
    (df['provinsi'].isin(provinsi)) &
    (df['kabupaten_kota'].isin(kab_kota)) & 
    (df['kecamatan'].isin(kecamatan)) & 
    (df['jenjang'].isin(jenjang))
]

# Jika toggle aktif, filter keluar data anomali
if sembunyikan_anomali:
    # Buat kolom bantuan jika belum ada
    df_filtered = df_filtered.copy()
    df_filtered['total_siswa_cek'] = df_filtered['jumlah_laki'] + df_filtered['jumlah_perempuan']
    
    # Cari yang anomali
    mask_anomali = ((df_filtered['jumlah_alergi'] > 0) | (df_filtered['jumlah_kondisi_khusus'] > 0)) & ((df_filtered['jumlah_penerima_manfaat'] == 0) | (df_filtered['total_siswa_cek'] == 0))
    
    # Ambil data yang TIDAK anomali (kebalikan dari mask menggunakan ~)
    df_filtered = df_filtered[~mask_anomali]

# --- METRIK UTAMA (KPI) ---
st.subheader("Ringkasan Eksekutif")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Satuan Pendidikan", f"{df_filtered['jumlah_satuan_pendidikan'].sum():,}")
col2.metric("Total Kecamatan", f"{df_filtered['kecamatan'].nunique():,}")
col3.metric("Total Kondisi Khusus", f"{df_filtered['jumlah_kondisi_khusus'].sum():,}")
col4.metric("Total Kasus Alergi", f"{df_filtered['jumlah_alergi'].sum():,}")
total_penerima = df_filtered['jumlah_penerima_manfaat'].sum() if 'jumlah_penerima_manfaat' in df_filtered.columns else 0
col5.metric("Total Penerima Manfaat", f"{total_penerima:,}")

st.divider()

# --- VISUALISASI ---
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
    radius = 0.8
    groupby_cols = ['kabupaten_kota', 'provinsi']
else:
    group_col = 'provinsi'
    hover_name = 'provinsi'
    radius = 0
    groupby_cols = ['provinsi']

df_map = df_filtered.groupby(groupby_cols).agg({
    'jumlah_satuan_pendidikan': 'sum',
    'jumlah_penerima_manfaat': 'sum'
}).reset_index()

if group_col == 'provinsi':
    import json
    with open('./data/indonesia-prov.geojson', 'r') as f:
        geojson_data = json.load(f)
        
    def map_prov_to_geojson(prov_name):
        p = prov_name.upper().replace('PROV. ', '')
        mapping = {
            'D.K.I. JAKARTA': 'DKI JAKARTA',
            'D.I. YOGYAKARTA': 'DAERAH ISTIMEWA YOGYAKARTA',
            'ACEH': 'DI. ACEH',
            'KEPULAUAN BANGKA BELITUNG': 'BANGKA BELITUNG',
            'NUSA TENGGARA BARAT': 'NUSATENGGARA BARAT',
            'PAPUA BARAT DAYA': 'PAPUA BARAT',
            'PAPUA PEGUNUNGAN': 'PAPUA',
            'PAPUA SELATAN': 'PAPUA',
            'PAPUA TENGAH': 'PAPUA'
        }
        return mapping.get(p, p)
        
    df_map['geojson_key'] = df_map['provinsi'].apply(map_prov_to_geojson)
    df_map_agg = df_map.groupby('geojson_key').agg({
        'jumlah_satuan_pendidikan': 'sum',
        'jumlah_penerima_manfaat': 'sum'
    }).reset_index()

    fig_map = px.choropleth_mapbox(
        df_map_agg,
        geojson=geojson_data,
        locations='geojson_key',
        featureidkey="properties.Propinsi",
        color="jumlah_penerima_manfaat",
        hover_name="geojson_key",
        hover_data={"geojson_key": False, "jumlah_satuan_pendidikan": True, "jumlah_penerima_manfaat": True},
        color_continuous_scale=px.colors.sequential.Viridis,
        mapbox_style="carto-positron",
        zoom=3.5,
        center={"lat": -2.5, "lon": 118.0},
        opacity=0.7
    )
else:
    import pandas as pd
    import re
    try:
        df_coords = pd.read_csv('./data/kabkota_coords.csv')
        df_coords['match_name'] = df_coords['name'].str.lower().str.replace('kabupaten ', '').str.replace('kota ', '').str.replace('administrasi ', '').str.strip()
    except:
        df_coords = pd.DataFrame()
        
    def get_real_coord(kab_name, fallback_lat, fallback_lon):
        if df_coords.empty:
            return fallback_lat, fallback_lon
        q = str(kab_name).lower()
        q = re.sub(r'^(kab\.|kota)\s*', '', q).strip()
        match = df_coords[df_coords['match_name'] == q]
        if not match.empty:
            return match.iloc[0]['latitude'], match.iloc[0]['longitude']
        match_partial = df_coords[df_coords['match_name'].str.contains(q, na=False, regex=False)]
        if not match_partial.empty:
            return match_partial.iloc[0]['latitude'], match_partial.iloc[0]['longitude']
        return get_synthetic_coord(kab_name, fallback_lat, fallback_lon, 0.8)

    lats = []
    lons = []
    for _, row in df_map.iterrows():
        base_lat, base_lon = PROV_COORDS.get(row['provinsi'], (-2.5, 118.0))
        if group_col == 'kabupaten_kota':
            lat, lon = get_real_coord(row['kabupaten_kota'], base_lat, base_lon)
        elif group_col == 'kecamatan':
            kab_lat, kab_lon = get_real_coord(row['kabupaten_kota'], base_lat, base_lon)
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

st.divider()

col_vis1, col_vis2 = st.columns(2)

with col_vis1:
    st.subheader("Peta Kerentanan Medis per Kecamatan")
    st.markdown("Menampilkan agregasi kasus alergi dan kondisi khusus untuk mitigasi risiko katering.")
    df_medis = df_filtered.groupby('kecamatan')[['jumlah_alergi', 'jumlah_kondisi_khusus']].sum().reset_index()
    # Mengabaikan wilayah yang nilainya 0 agar chart lebih bersih
    df_medis = df_medis[(df_medis['jumlah_alergi'] > 0) | (df_medis['jumlah_kondisi_khusus'] > 0)]
    
    fig_medis = px.bar(df_medis, x='kecamatan', y=['jumlah_alergi', 'jumlah_kondisi_khusus'], 
                       barmode='group', labels={'value': 'Jumlah Kasus', 'variable': 'Kategori'},
                       )
    st.plotly_chart(fig_medis, use_container_width=True)

with col_vis2:
    st.subheader("Konsentrasi Kondisi Khusus per Jenjang")
    st.markdown("Membantu penentuan jenjang mana yang membutuhkan pengawasan diet lebih ketat.")
    df_jenjang = df_filtered.groupby('jenjang')['jumlah_kondisi_khusus'].sum().reset_index()
    fig_jenjang = px.pie(df_jenjang, values='jumlah_kondisi_khusus', names='jenjang', hole=0.4)
    st.plotly_chart(fig_jenjang, use_container_width=True)

st.divider()

col_vis3, col_vis4 = st.columns(2)

with col_vis3:
    st.subheader("Proporsi Status Sekolah")
    st.markdown("Perbandingan fasilitas negeri vs swasta untuk skema distribusi dan birokrasi.")
    df_status = pd.DataFrame({
        'Status': ['Negeri', 'Swasta'],
        'Jumlah': [df_filtered['jumlah_satpen_negeri'].sum(), df_filtered['jumlah_satpen_swasta'].sum()]
    })
    fig_status = px.bar(df_status, x='Status', y='Jumlah', color='Status', text_auto=True)
    st.plotly_chart(fig_status, use_container_width=True)

with col_vis4:
    st.subheader("Pemantauan Kualitas Data (Deteksi Anomali)")
    st.markdown("*Flagging* data mencurigakan: Ada penderita Kasus Medis (Alergi/Kondisi Khusus), tetapi *Jumlah Penerima Manfaat* tercatat 0.")
    st.markdown("Harga MBG per porsi Rp15.000")
    
    # Anomali: Penerima 0 tapi Kasus Medis > 0
    df_anomali = df_filtered[
        ((df_filtered['jumlah_alergi'] > 0) | (df_filtered['jumlah_kondisi_khusus'] > 0)) & 
        (df_filtered['jumlah_penerima_manfaat'] == 0)
    ].copy()
    
    if not df_anomali.empty:
        df_anomali['Total Kasus Medis Diabaikan'] = df_anomali['jumlah_alergi'] + df_anomali['jumlah_kondisi_khusus']
        df_anomali['Potensi Kerugian (Rp)'] = df_anomali['Total Kasus Medis Diabaikan'] * 15000
        total_kerugian = df_anomali['Potensi Kerugian (Rp)'].sum()
        total_diabaikan = df_anomali['Total Kasus Medis Diabaikan'].sum()
        
        # Hitung Rasio Kasus Medis Keseluruhan
        total_kasus_semua = df_filtered['jumlah_alergi'].sum() + df_filtered['jumlah_kondisi_khusus'].sum()
        total_terlayani = max(0, total_kasus_semua - total_diabaikan)
        
        st.warning(f"⚠️ Terdeteksi {len(df_anomali)} wilayah dengan anomali (Siswa berisiko diabaikan).")
        st.metric("Total Potensi Kerugian/Maladministrasi (Per Hari)", f"Rp {total_kerugian:,.0f}")
        
        # Grafik Rasio Anomali
        df_pie_anomali = pd.DataFrame({
            'Status': ['Terlayani', 'Diabaikan (Anomali)'],
            'Jumlah': [total_terlayani, total_diabaikan]
        })
        fig_pie_anomali = px.pie(
            df_pie_anomali, values='Jumlah', names='Status', 
            color='Status', color_discrete_map={'Terlayani':'#00CC96', 'Diabaikan (Anomali)':'#EF553B'},
            hole=0.4, height=280
        )
        fig_pie_anomali.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_pie_anomali, use_container_width=True)
        
        st.dataframe(
            df_anomali[['kabupaten_kota', 'kecamatan', 'jenjang', 'jumlah_alergi', 'jumlah_kondisi_khusus', 'Total Kasus Medis Diabaikan', 'Potensi Kerugian (Rp)']],
            use_container_width=True, hide_index=True
        )
    else:
        st.success("✅ Tidak terdeteksi anomali data medis yang terabaikan.")

st.divider()

col_multi1, col_multi2 = st.columns(2)

with col_multi1:
    st.subheader("Korelasi Alergi vs Kondisi Khusus (Bubble Chart)")
    st.markdown("Sumbu X: Alergi | Sumbu Y: Kondisi Khusus | Warna: Jenjang | Ukuran Gelembung: Jumlah Sekolah.")
    
    # Memfilter row dengan minimal 1 kasus agar chart lebih fokus
    df_scatter = df_filtered[(df_filtered['jumlah_alergi'] > 0) | (df_filtered['jumlah_kondisi_khusus'] > 0)]
    
    # Jika data terlalu sedikit yang >0, kita pakai df_filtered as is
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
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_multi2:
    st.subheader("Distribusi Risiko dalam Hierarki Wilayah (Treemap)")
    st.markdown("Ukuran Kotak: Jumlah Sekolah | Warna: Intensitas Kasus Kondisi Khusus.")
    
    fig_treemap = px.treemap(
        df_filtered,
        path=[px.Constant("Semua Wilayah"), 'kabupaten_kota', 'kecamatan', 'jenjang'],
        values='jumlah_satuan_pendidikan',
        color='jumlah_kondisi_khusus',
        hover_data=['jumlah_alergi', 'jumlah_penerima_manfaat'],
        color_continuous_scale='Reds', # Warna semakin merah = kondisi khusus semakin banyak
        labels={'jumlah_kondisi_khusus': 'Kondisi Khusus'},
    )
    # Memperbaiki margin agar pas
    fig_treemap.update_layout(margin=dict(t=10, l=10, r=10, b=10))
    st.plotly_chart(fig_treemap, use_container_width=True)

st.divider()

st.subheader("Alur Keterkaitan Parameter (Parallel Categories)")
st.markdown("Menganalisis hubungan antara Jenjang Pendidikan, Status Kepemilikan Mayoritas Sekolah, Tingkat Cakupan MBG, dan Risiko Medis.")

# 1. Menyiapkan data turunan (Derived Categories)
df_pc = df_filtered.copy()

# Dominasi Sekolah
def get_dominasi(negeri, swasta):
    if negeri > swasta:
        return 'Mayoritas Negeri'
    elif swasta > negeri:
        return 'Mayoritas Swasta'
    else:
        return 'Berimbang'

df_pc['Dominasi Sekolah'] = df_pc.apply(lambda row: get_dominasi(row['jumlah_satpen_negeri'], row['jumlah_satpen_swasta']), axis=1)

# Status Cakupan
def get_cakupan(penerima, l, p):
    total = l + p
    if total == 0:
        return 'Tidak Ada Siswa'
    ratio = penerima / total
    if ratio >= 0.9:
        return 'Ter-cover Penuh'
    elif ratio > 0.1:
        return 'Sebagian'
    else:
        return 'Belum Ter-cover'

df_pc['Status Cakupan'] = df_pc.apply(lambda row: get_cakupan(row['jumlah_penerima_manfaat'], row['jumlah_laki'], row['jumlah_perempuan']), axis=1)

# Risiko Medis
def get_risiko(alergi, khusus):
    kasus = alergi + khusus
    if kasus == 0:
        return 'Aman (0 Kasus)'
    elif kasus > 5:
        return 'Risiko Tinggi (>5)'
    else:
        return 'Risiko Rendah (1-5)'
        
df_pc['Risiko Medis'] = df_pc.apply(lambda row: get_risiko(row['jumlah_alergi'], row['jumlah_kondisi_khusus']), axis=1)

# 2. Agregasi data untuk Parallel Categories
df_pc_agg = df_pc.groupby(['jenjang', 'Dominasi Sekolah', 'Status Cakupan', 'Risiko Medis']).size().reset_index(name='Jumlah Agregasi Area')

# 3. Membuat Plot
fig_pc = px.parallel_categories(
    df_pc_agg, 
    dimensions=['jenjang', 'Dominasi Sekolah', 'Status Cakupan', 'Risiko Medis'],
    color='Jumlah Agregasi Area',
    color_continuous_scale=px.colors.sequential.Tealgrn,
    labels={
        'jenjang': 'Jenjang',
        'Dominasi Sekolah': 'Status Mayoritas',
        'Status Cakupan': 'Cakupan MBG',
        'Risiko Medis': 'Kategori Risiko'
    }
)
fig_pc.update_layout(margin=dict(t=30, l=10, r=10, b=10))
st.plotly_chart(fig_pc, use_container_width=True)

st.divider()

# --- TABEL DATA DETAIL ---
st.header("Tabel Data Detail")
st.markdown("Tabel di bawah ini menampilkan data mentah dari hasil filter yang Anda pilih di *sidebar*. Anda dapat mengurutkan kolom atau mengunduh data ini sebagai CSV.")

# Tampilkan tabel interaktif (hanya kolom-kolom yang relevan agar lebih rapi)
kolom_tampil = [
    'provinsi', 'kabupaten_kota', 'kecamatan', 'jenjang',
    'jumlah_satuan_pendidikan', 'jumlah_laki', 'jumlah_perempuan',
    'jumlah_penerima_manfaat', 'jumlah_alergi', 'jumlah_kondisi_khusus'
]
st.dataframe(df_filtered[kolom_tampil], use_container_width=True, hide_index=True)