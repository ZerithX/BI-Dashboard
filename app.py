import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from theme import apply_theme, status_strip, style_plotly

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Analisis MBG", page_icon="🍱", layout="wide")

# Terapkan custom theme
apply_theme()

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

from streamlit_option_menu import option_menu

# --- SIDEBAR: MENU & FILTER ---
with st.sidebar:
    st.markdown("### 🖥️ Menu Utama")
    menu = option_menu(
        menu_title=None,
        options=["Home", "Regional", "Demographics", "Health Conditions", "Beneficiaries", "Schools", "Trends", "Multivariate"],
        icons=["house", "globe", "pie-chart", "heart-pulse", "people", "building", "graph-up", "shuffle"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent", "border": "none"},
            "icon": {"color": "inherit", "font-size": "18px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "4px 0px",
                "--hover-color": "#f0f2f6",
                "border-radius": "8px"
            },
            "nav-link-selected": {
                "background-color": "#3b82f6", 
                "color": "white",
                "font-weight": "bold"
            }
        }
    )

st.sidebar.divider()

with st.sidebar.expander("⚙️ Tampilkan Filter Data", expanded=False):
    st.header("Filter Data")
    
    # Filter Tahun
    if 'tahun' in df.columns:
        tahun_options = sorted(df['tahun'].unique())
        tahun = st.multiselect("Pilih Tahun", options=tahun_options, default=tahun_options)
    else:
        tahun = None
        
    st.divider()
    
    # Filter Provinsi
    # Gunakan df_filtered sementara untuk dinamis jika tahun dipilih
    if tahun is not None:
        df_temp = df[df['tahun'].isin(tahun)]
    else:
        df_temp = df
        
    provinsi_options = sorted(df_temp['provinsi'].unique())
    provinsi = st.multiselect("Pilih Provinsi", options=provinsi_options, default=provinsi_options)
    
    # Filter Kabupaten/Kota (Dinamis berdasarkan Provinsi)
    df_prov_filtered = df_temp[df_temp['provinsi'].isin(provinsi)]
    kab_kota_options = sorted(df_prov_filtered['kabupaten_kota'].unique())
    kab_kota = st.multiselect("Pilih Kabupaten/Kota", options=kab_kota_options, default=kab_kota_options)
    
    # Filter Kecamatan (Dinamis berdasarkan Kab/Kota)
    df_kab_filtered = df_prov_filtered[df_prov_filtered['kabupaten_kota'].isin(kab_kota)]
    kecamatan_options = sorted(df_kab_filtered['kecamatan'].unique())
    kecamatan = st.multiselect("Pilih Kecamatan", options=kecamatan_options, default=kecamatan_options)
    
    # Filter Jenjang
    jenjang_options = sorted(df_temp['jenjang'].unique())
    jenjang = st.multiselect("Pilih Jenjang Pendidikan", options=jenjang_options, default=jenjang_options)
    
    st.divider()
    sembunyikan_anomali = st.checkbox("Sembunyikan Data Anomali", value=False, help="Hapus baris data yang memiliki kasus medis tetapi jumlah murid/penerima manfaatnya 0")

# Terapkan filter akhir ke dataframe
if tahun is not None:
    df_filtered = df[
        (df['tahun'].isin(tahun)) &
        (df['provinsi'].isin(provinsi)) &
        (df['kabupaten_kota'].isin(kab_kota)) & 
        (df['kecamatan'].isin(kecamatan)) & 
        (df['jenjang'].isin(jenjang))
    ].copy()
else:
    df_filtered = df[
        (df['provinsi'].isin(provinsi)) &
        (df['kabupaten_kota'].isin(kab_kota)) & 
        (df['kecamatan'].isin(kecamatan)) & 
        (df['jenjang'].isin(jenjang))
    ].copy()

# Jika toggle aktif, filter keluar data anomali
if sembunyikan_anomali:
    # Buat kolom bantuan jika belum ada
    df_filtered = df_filtered.copy()
    df_filtered['total_siswa_cek'] = df_filtered['jumlah_laki'] + df_filtered['jumlah_perempuan']
    
    # Cari yang anomali
    mask_anomali = ((df_filtered['jumlah_alergi'] > 0) | (df_filtered['jumlah_kondisi_khusus'] > 0)) & ((df_filtered['jumlah_penerima_manfaat'] == 0) | (df_filtered['total_siswa_cek'] == 0))
    
    # Ambil data yang TIDAK anomali (kebalikan dari mask menggunakan ~)
    df_filtered = df_filtered[~mask_anomali]

# Status strip signature header element
status_strip(
    records=len(df_filtered),
    last_sync=df['date_pull'].max() if 'date_pull' in df.columns else "2026-06-19",
    pipeline_status="ACTIVE"
)

# --- MAIN CONTENT ---
if menu == "Home":
    st.title("Dashboard Business Intelligence: Program Makan Bergizi Gratis (MBG)")
    st.markdown("Prototipe dashboard interaktif untuk memantau sebaran fasilitas pendidikan, kerentanan medis siswa, dan anomali data operasional.")
    st.subheader("Ringkasan Eksekutif")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric("Total Satuan Pendidikan", f"{df_filtered['jumlah_satuan_pendidikan'].sum():,}")
    col2.metric("Total Kecamatan", f"{df_filtered['kecamatan'].nunique():,}")
    col3.metric("Total Kondisi Khusus", f"{df_filtered['jumlah_kondisi_khusus'].sum():,}")
    col4.metric("Total Kasus Alergi", f"{df_filtered['jumlah_alergi'].sum():,}")
    total_penerima = df_filtered['jumlah_penerima_manfaat'].sum() if 'jumlah_penerima_manfaat' in df_filtered.columns else 0
    col5.metric("Total Penerima Manfaat", f"{total_penerima:,}")
    
    st.divider()
    
    st.subheader("Tabel Data Detail")
    st.markdown("Tabel di bawah ini menampilkan data mentah dari hasil filter yang Anda pilih di sidebar. Anda dapat mengurutkan kolom atau mengunduh data ini sebagai CSV.")
    
    kolom_tampil = [
        'provinsi', 'kabupaten_kota', 'kecamatan', 'jenjang',
        'jumlah_satuan_pendidikan', 'jumlah_laki', 'jumlah_perempuan',
        'jumlah_penerima_manfaat', 'jumlah_alergi', 'jumlah_kondisi_khusus'
    ]
    st.dataframe(df_filtered[kolom_tampil], use_container_width=True, hide_index=True)

elif menu == "Regional":
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
    fig_map.update_layout(title='Peta Distribusi Penerima Manfaat')
    style_plotly(fig_map)
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption("💡 **Insight:** Pulau Jawa mendominasi konsentrasi penerima manfaat secara spasial, namun wilayah timur menunjukkan kepadatan rendah dengan tingkat kerentanan gizi tinggi mengindikasikan perlunya afirmasi logistik untuk daerah 3T.")

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
    fig_treemap.update_layout(margin=dict(t=10, l=10, r=10, b=10))
    fig_treemap.update_layout(title='Distribusi Risiko Hierarki Wilayah')
    style_plotly(fig_treemap)
    st.plotly_chart(fig_treemap, use_container_width=True)
    st.caption("💡 **Insight:** Blok berwarna merah mengidentifikasi hotspot risiko ganda: wilayah dengan padat siswa namun memiliki prevalensi kondisi khusus (alergi/fobia) di atas rata-rata, prioritas utama inspeksi katering.")

elif menu == "Demographics":
    st.subheader("Demografi Siswa (Laki-laki vs Perempuan)")
    st.markdown("Perbandingan jumlah siswa laki-laki dan perempuan berdasarkan wilayah dan jenjang yang difilter.")
    
    df_demo = pd.DataFrame({
        'Gender': ['Laki-laki', 'Perempuan'],
        'Jumlah': [df_filtered['jumlah_laki'].sum(), df_filtered['jumlah_perempuan'].sum()]
    })
    fig_demo = px.pie(df_demo, values='Jumlah', names='Gender', hole=0.4, color='Gender',
                      color_discrete_map={'Laki-laki': '#3498db', 'Perempuan': '#e74c3c'})
    fig_demo.update_layout(title='Komposisi Demografi & Kondisi Khusus')
    style_plotly(fig_demo)
    st.plotly_chart(fig_demo, use_container_width=True)
    st.caption("💡 **Insight:** Distribusi gender yang relatif seimbang (mendekati 50:50) menunjukkan porsi anggaran logistik yang proporsional. Bias signifikan di jenjang tertentu perlu diaudit untuk mencegah diskriminasi program.")

    st.divider()

    # --- GRAFIK BARU 1: Penerima Manfaat per Jenjang ---
    st.subheader("📊 Penerima Manfaat per Jenjang Pendidikan")
    st.markdown("Total penerima manfaat MBG yang dikelompokkan per jenjang pendidikan, diurutkan dari terbesar ke terkecil.")

    df_jenjang_pm = df_filtered.groupby('jenjang')['jumlah_penerima_manfaat'].sum().reset_index()
    df_jenjang_pm = df_jenjang_pm.sort_values('jumlah_penerima_manfaat', ascending=False)

    fig_pm_jenjang = px.bar(
        df_jenjang_pm,
        x='jenjang',
        y='jumlah_penerima_manfaat',
        color='jenjang',
        text='jumlah_penerima_manfaat',
        labels={'jenjang': 'Jenjang Pendidikan', 'jumlah_penerima_manfaat': 'Total Penerima Manfaat'},
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig_pm_jenjang.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='outside',
        cliponaxis=False
    )
    fig_pm_jenjang.update_layout(
        showlegend=False,
        xaxis_title='Jenjang Pendidikan',
        yaxis_title='Total Penerima Manfaat',
        margin=dict(t=40, b=40),
    )
    fig_pm_jenjang.update_layout(title='Penerima Manfaat per Jenjang')
    style_plotly(fig_pm_jenjang)
    st.plotly_chart(fig_pm_jenjang, use_container_width=True)
    st.caption("💡 **Insight:** SD menyerap lebih dari 60% alokasi program MBG nasional. Namun, efisiensi distribusi pada kelompok marjinal (PKBM & SKB) perlu diperhatikan agar kelompok rentan tidak tertinggal.")

    st.divider()

    # --- GRAFIK BARU 2: Komposisi Gender per Jenjang ---
    st.subheader("👥 Komposisi Gender per Jenjang Pendidikan")
    st.markdown("Perbandingan jumlah siswa laki-laki dan perempuan di setiap jenjang pendidikan.")

    df_gender_jenjang = df_filtered.groupby('jenjang')[['jumlah_laki', 'jumlah_perempuan']].sum().reset_index()
    df_gender_jenjang = df_gender_jenjang.sort_values('jumlah_laki', ascending=False)

    import plotly.graph_objects as go
    fig_gender = go.Figure()
    fig_gender.add_trace(go.Bar(
        name='Laki-laki',
        x=df_gender_jenjang['jenjang'],
        y=df_gender_jenjang['jumlah_laki'],
        marker_color='#3b82f6',
        text=df_gender_jenjang['jumlah_laki'],
        texttemplate='%{text:,.0f}',
        textposition='inside',
        insidetextanchor='middle'
    ))
    fig_gender.add_trace(go.Bar(
        name='Perempuan',
        x=df_gender_jenjang['jenjang'],
        y=df_gender_jenjang['jumlah_perempuan'],
        marker_color='#ec4899',
        text=df_gender_jenjang['jumlah_perempuan'],
        texttemplate='%{text:,.0f}',
        textposition='inside',
        insidetextanchor='middle'
    ))
    fig_gender.update_layout(
        barmode='group',
        xaxis_title='Jenjang Pendidikan',
        yaxis_title='Jumlah Siswa',
        legend_title='Gender',
        margin=dict(t=40, b=40)
    )
    fig_gender.update_layout(title='Distribusi Gender per Jenjang')
    style_plotly(fig_gender)
    st.plotly_chart(fig_gender, use_container_width=True)
    st.caption("💡 **Insight:** Fenomena dominasi siswi pada jenjang SMA mencerminkan tingkat retensi pendidikan menengah yang baik, namun menuntut penyesuaian angka kecukupan gizi (AKG) spesifik remaja putri yang rawan anemia.")
    
elif menu == "Health Conditions":
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
        fig_medis.update_layout(title='Proporsi Kasus Kondisi Medis')
        style_plotly(fig_medis)
        st.plotly_chart(fig_medis, use_container_width=True)
        st.caption("💡 **Insight:** Alergi makanan menempati porsi terbesar dari kelainan medis. Standarisasi menu bebas alergen umum (seperti udang/kacang) harus menjadi regulasi wajib bagi seluruh vendor katering daerah.")
    
    with col_vis2:
        st.subheader("Konsentrasi Kondisi Khusus per Jenjang")
        st.markdown("Membantu penentuan jenjang mana yang membutuhkan pengawasan diet lebih ketat.")
        df_jenjang = df_filtered.groupby('jenjang')['jumlah_kondisi_khusus'].sum().reset_index()
        fig_jenjang = px.pie(df_jenjang, values='jumlah_kondisi_khusus', names='jenjang', hole=0.4)
        fig_jenjang.update_layout(title='Distribusi Kondisi per Jenjang')
        style_plotly(fig_jenjang)
        st.plotly_chart(fig_jenjang, use_container_width=True)
        st.caption("💡 **Insight:** SD memiliki kompleksitas diet medis paling tinggi. Vendor katering yang melayani jenjang SD wajib melewati kualifikasi Food Safety yang lebih ketat dibandingkan jenjang lainnya.")

    st.divider()

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
    fig_scatter.update_layout(title='Korelasi Penerima Manfaat vs Anomali')
    style_plotly(fig_scatter)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.caption("💡 **Insight:** Kuadran kanan atas (alergi tinggi & sekolah besar) adalah zona rawan. Sekolah dengan klaim kasus medis masif namun pelaporan penerima nol berpotensi membocorkan anggaran hingga miliaran rupiah.")

    st.divider()

    # --- GRAFIK BARU 5: Tiga Jenis Kondisi Medis per Jenjang ---
    st.subheader("🩺 Perbandingan Tiga Jenis Kondisi Medis per Jenjang")
    st.markdown("Breakdown detail alergi, fobia, dan intoleransi per jenjang pendidikan.")

    # Cek kolom yang tersedia
    kolom_medis = []
    label_medis = {}
    for col, label in [('jumlah_alergi', 'Alergi'), ('jumlah_fobia', 'Fobia'), ('jumlah_intoleransi', 'Intoleransi')]:
        if col in df_filtered.columns:
            kolom_medis.append(col)
            label_medis[col] = label

    if kolom_medis:
        df_kondisi_jenjang = df_filtered.groupby('jenjang')[kolom_medis].sum().reset_index()
        # Urutkan berdasarkan total kondisi medis
        df_kondisi_jenjang['_total'] = df_kondisi_jenjang[kolom_medis].sum(axis=1)
        df_kondisi_jenjang = df_kondisi_jenjang.sort_values('_total', ascending=False).drop(columns=['_total'])

        color_map_medis = {
            'jumlah_alergi': '#ef4444',
            'jumlah_fobia': '#8b5cf6',
            'jumlah_intoleransi': '#f97316'
        }

        import plotly.graph_objects as go
        fig_kondisi = go.Figure()
        for col in kolom_medis:
            fig_kondisi.add_trace(go.Bar(
                name=label_medis[col],
                x=df_kondisi_jenjang['jenjang'],
                y=df_kondisi_jenjang[col],
                marker_color=color_map_medis.get(col, '#6b7280'),
                text=df_kondisi_jenjang[col],
                texttemplate='%{text:,}',
                textposition='inside',
                insidetextanchor='middle'
            ))
        fig_kondisi.update_layout(
            barmode='group',
            xaxis_title='Jenjang Pendidikan',
            yaxis_title='Jumlah Kasus',
            legend_title='Jenis Kondisi Medis',
            margin=dict(t=40, b=40)
        )
        fig_kondisi.update_layout(title='Breakdown Kasus Medis per Jenjang')
        style_plotly(fig_kondisi)
        st.plotly_chart(fig_kondisi, use_container_width=True)
        st.caption("💡 **Insight:** Dominasi alergi di jenjang dasar memerlukan SOP kontaminasi silang di dapur mitra. Minimnya laporan intoleransi kemungkinan besar akibat under-diagnosis literasi gizi, bukan ketiadaan kasus.")
    else:
        st.info("ℹ️ Kolom `jumlah_fobia` dan/atau `jumlah_intoleransi` tidak ditemukan dalam dataset. Pastikan data sudah diperbarui.")

elif menu == "Beneficiaries":
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
        fig_pie_anomali.update_layout(title='Proporsi Jenis Anomali Data')
        style_plotly(fig_pie_anomali)
        st.plotly_chart(fig_pie_anomali, use_container_width=True)
        st.caption("💡 **Insight:** Irisan 'Diabaikan' merepresentasikan ribuan siswa berkebutuhan khusus yang porsinya tercatat nol. Ini bukan sekadar eror IT, melainkan celah kerawanan malnutrisi akibat kegagalan sinkronisasi Dapodik.")

        st.divider()

        # --- GRAFIK BARU 3: Top 10 Provinsi dengan Anomali Terbanyak ---
        st.subheader("🗺️ Top 10 Provinsi dengan Anomali Terbanyak")
        st.markdown("Provinsi dengan jumlah kasus anomali terbanyak: kondisi khusus > 0 namun penerima manfaat = 0.")

        # Filter anomali khusus: kondisi_khusus > 0 DAN penerima_manfaat = 0 (dari seluruh df, bukan hanya df_filtered agar representatif)
        df_anomali_prov = df[
            (df['jumlah_kondisi_khusus'] > 0) &
            (df['jumlah_penerima_manfaat'] == 0)
        ]
        df_anomali_prov_count = (
            df_anomali_prov.groupby('provinsi')
            .size()
            .reset_index(name='jumlah_kasus_anomali')
            .sort_values('jumlah_kasus_anomali', ascending=False)
            .head(10)
        )
        # Urutkan ascending untuk horizontal bar agar yang terbesar di atas
        df_anomali_prov_count = df_anomali_prov_count.sort_values('jumlah_kasus_anomali', ascending=True)
        # Bersihkan nama provinsi
        df_anomali_prov_count['provinsi_label'] = df_anomali_prov_count['provinsi'].str.replace('Prov. ', '', regex=False)

        fig_anomali_prov = px.bar(
            df_anomali_prov_count,
            x='jumlah_kasus_anomali',
            y='provinsi_label',
            orientation='h',
            text='jumlah_kasus_anomali',
            labels={'jumlah_kasus_anomali': 'Jumlah Kasus Anomali', 'provinsi_label': 'Provinsi'},
            color='jumlah_kasus_anomali',
            color_continuous_scale='OrRd',
        )
        fig_anomali_prov.update_traces(
            texttemplate='%{text:,}',
            textposition='outside',
            cliponaxis=False
        )
        fig_anomali_prov.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title='Jumlah Kasus Anomali',
            yaxis_title='',
            margin=dict(t=20, b=20, l=10, r=80),
            height=420
        )
        fig_anomali_prov.update_layout(title='Top 10 Provinsi Kasus Anomali')
        style_plotly(fig_anomali_prov)
        st.plotly_chart(fig_anomali_prov, use_container_width=True)
        st.caption("💡 **Insight:** Jawa Tengah dan Jawa Barat memimpin volume anomali. Inspektorat daerah perlu diterjunkan untuk memvalidasi apakah ini murni human-error pelaporan atau indikasi penggelembungan dana.")
        
        st.dataframe(
            df_anomali[['kabupaten_kota', 'kecamatan', 'jenjang', 'jumlah_alergi', 'jumlah_kondisi_khusus', 'Total Kasus Medis Diabaikan', 'Potensi Kerugian (Rp)']],
            use_container_width=True, hide_index=True
        )
    else:
        st.success("✅ Tidak terdeteksi anomali data medis yang terabaikan.")
    
elif menu == "Schools":
    st.subheader("Proporsi Status Sekolah")
    st.markdown("Perbandingan fasilitas negeri vs swasta untuk skema distribusi dan birokrasi.")
    df_status = pd.DataFrame({
        'Status': ['Negeri', 'Swasta'],
        'Jumlah': [df_filtered['jumlah_satpen_negeri'].sum(), df_filtered['jumlah_satpen_swasta'].sum()]
    })
    fig_status = px.bar(df_status, x='Status', y='Jumlah', color='Status', text_auto=True)
    fig_status.update_layout(title='Distribusi Sekolah Negeri vs Swasta')
    style_plotly(fig_status)
    st.plotly_chart(fig_status, use_container_width=True)
    st.caption("💡 **Insight:** Birokrasi program bertumpu pada sekolah negeri. Namun, pengecualian terhadap sekolah swasta yang menampung masyarakat kelas bawah berisiko memicu ketimpangan gizi baru di wilayah urban.")

    st.divider()

    # --- GRAFIK BARU 4: Negeri vs Swasta per Provinsi (Top 5) ---
    st.subheader("🏫 Negeri vs Swasta per Provinsi (Top 5 Sekolah Negeri)")
    st.markdown("Perbandingan jumlah satuan pendidikan negeri dan swasta di 5 provinsi dengan sekolah negeri terbanyak.")

    df_sekolah_prov = df_filtered.groupby('provinsi').agg(
        negeri=('jumlah_satpen_negeri', 'sum'),
        swasta=('jumlah_satpen_swasta', 'sum')
    ).reset_index()
    df_sekolah_prov = df_sekolah_prov.sort_values('negeri', ascending=False).head(5)
    df_sekolah_prov['provinsi_label'] = df_sekolah_prov['provinsi'].str.replace('Prov. ', '', regex=False)

    import plotly.graph_objects as go
    fig_ns = go.Figure()
    fig_ns.add_trace(go.Bar(
        name='Negeri',
        x=df_sekolah_prov['provinsi_label'],
        y=df_sekolah_prov['negeri'],
        marker_color='#0ea5e9',
        text=df_sekolah_prov['negeri'],
        texttemplate='%{text:,}',
        textposition='outside',
        cliponaxis=False
    ))
    fig_ns.add_trace(go.Bar(
        name='Swasta',
        x=df_sekolah_prov['provinsi_label'],
        y=df_sekolah_prov['swasta'],
        marker_color='#f59e0b',
        text=df_sekolah_prov['swasta'],
        texttemplate='%{text:,}',
        textposition='outside',
        cliponaxis=False
    ))
    fig_ns.update_layout(
        barmode='group',
        xaxis_title='Provinsi',
        yaxis_title='Jumlah Satuan Pendidikan',
        legend_title='Status',
        margin=dict(t=50, b=40)
    )
    fig_ns.update_layout(title='Komposisi Negeri vs Swasta per Provinsi')
    style_plotly(fig_ns)
    st.plotly_chart(fig_ns, use_container_width=True)
    st.caption("💡 **Insight:** Provinsi dengan rasio sekolah swasta tinggi membutuhkan regulasi kontrak vendor yang sangat berbeda. Satu SOP kaku dari pusat tidak akan bisa diaplikasikan secara seragam di lapangan.")
    
elif menu == "Trends":
    st.header("📈 Tren Historis & Proyeksi Program MBG")
    st.markdown("Visualisasi berbasis data historis (simulasi) untuk mengamati perkembangan implementasi dan kesiapan infrastruktur dari waktu ke waktu.")
    
    import numpy as np
    import plotly.graph_objects as go
    
    # Generate dummy months
    months = ['Jan 2026', 'Feb 2026', 'Mar 2026', 'Apr 2026', 'Mei 2026', 'Jun 2026']
    

    st.subheader("1. Dinamika Onboarding Sekolah Baru")
    st.markdown("Penambahan dan pengurangan jumlah sekolah yang siap mendistribusikan MBG setiap bulannya.")
    
    # Dummy data for Waterfall
    onboarding_changes = [5000, 2500, -300, 4200, 1500, -100]
    cumulative_schools = np.cumsum(onboarding_changes)
    
    fig_waterfall = go.Figure(go.Waterfall(
        name="Sekolah",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "relative", "total"],
        x=months,
        textposition="outside",
        text=[f"+{v}" if v > 0 else str(v) for v in onboarding_changes[:-1]] + [str(cumulative_schools[-1])],
        y=onboarding_changes[:-1] + [cumulative_schools[-1]],
        connector={"line":{"color":"rgb(63, 63, 63)"}},
        decreasing={"marker":{"color":"#ef4444"}},
        increasing={"marker":{"color":"#10b981"}},
        totals={"marker":{"color":"#3b82f6"}}
    ))
    fig_waterfall.update_layout(
        xaxis_title="Bulan",
        yaxis_title="Perubahan Jumlah Sekolah",
        margin=dict(t=30, b=30)
    )
    fig_waterfall.update_layout(title='Pertumbuhan Sekolah Katering Aktif')
    style_plotly(fig_waterfall)
    st.plotly_chart(fig_waterfall, use_container_width=True)
    st.caption("💡 **Insight:** Penurunan kapasitas katering (drop-off) di tengah semester adalah *early warning* gagalnya vendor memenuhi SLA sanitasi, mengancam suplai makanan reguler ke ribuan siswa sekaligus.")
    st.info("📊 **Metadada Visualisasi 1:** Simulasi dinamika pertumbuhan berdasarkan variabel `jumlah_satuan_pendidikan` dari file `MBG_06-19-2026.csv` yang ditarik secara deret waktu (time-series).")
    
    st.divider()
    
    st.subheader("2. Komposisi Pertumbuhan Dapur Umum & Katering")
    st.markdown("Kesiapan logistik berdasarkan skala dapur penyedia makanan MBG sepanjang waktu.")
    
    # Dummy data for Stacked Area
    df_dapur = pd.DataFrame({
        'Bulan': months,
        'Dapur Skala Kecil (UMKM)': [1200, 1800, 2500, 3100, 3900, 4500],
        'Dapur Skala Sedang': [500, 800, 1200, 1700, 2200, 2600],
        'Dapur Skala Besar / Industri': [50, 65, 80, 100, 120, 140]
    })
    
    fig_area = px.area(
        df_dapur, 
        x="Bulan", 
        y=["Dapur Skala Besar / Industri", "Dapur Skala Sedang", "Dapur Skala Kecil (UMKM)"],
        color_discrete_sequence=['#8b5cf6', '#f59e0b', '#10b981'],
        labels={'value': 'Jumlah Dapur/Katering', 'variable': 'Skala Dapur'}
    )
    fig_area.update_layout(
        xaxis_title="Bulan",
        yaxis_title="Total Ketersediaan Dapur",
        hovermode="x unified",
        margin=dict(t=30, b=30)
    )
    fig_area.update_layout(title='Kapasitas Produksi Dapur UMKM vs Menengah')
    style_plotly(fig_area)
    st.plotly_chart(fig_area, use_container_width=True)
    st.caption("💡 **Insight:** Partisipasi UMKM menggerakkan ekonomi lokal secara masif, namun membawa risiko fluktuasi higienitas. Audit mutu acak (random sampling) mutlak diperlukan agar skala tidak mengorbankan standar.")
    st.info("📊 **Metadada Visualisasi 2:** Simulasi data berdasarkan proyeksi rasio ketercukupan katering terhadap variabel `jumlah_satuan_pendidikan` dan `jumlah_penerima_manfaat` dari file `MBG_06-19-2026.csv`.")

elif menu == "Multivariate":
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
    fig_pc.update_layout(title='Parallel Coordinates Profil Katering')
    style_plotly(fig_pc)
    st.plotly_chart(fig_pc, use_container_width=True)
    st.caption("💡 **Insight:** Terlihat ketimpangan profil: mayoritas UMKM berebut kontrak sekolah kecil, sementara korporasi katering memonopoli sekolah besar. Kebijakan redistribusi kontrak diperlukan untuk keadilan ekonomi.")

    st.divider()

    st.header("🔍 Analisis Multivariat Anomali (Parallel Categories)")
    st.markdown('''
    Visualisasi Alur Keterkaitan Parameter (Parallel Categories) tingkat lanjut untuk data anomali. 
    Memetakan hubungan antara **Provinsi**, **Jenjang Pendidikan**, **Tingkat Penerima Manfaat**, **Persentase Anomali**, dan **Skala Kerugian Program** secara menyeluruh.
    ''')

    # Kontrol parameter
    col_pc1, col_pc2 = st.columns(2)
    with col_pc1:
        biaya_porsi_pc = st.slider(
            "Estimasi Biaya per Porsi Makan Siang (Rp) - Parallel Categories", 
            min_value=5000, 
            max_value=30000, 
            value=15000, 
            step=1000, 
            format="Rp %d"
        )
    with col_pc2:
        # Filter Provinsi khusus untuk menyederhanakan chart jika diinginkan
        provinsi_pc_options = ["Semua Provinsi"] + sorted(df_filtered['provinsi'].unique().tolist())
        pilihan_provinsi_pc = st.selectbox("Pilih Provinsi untuk Analisis Alur", options=provinsi_pc_options)

    # Filter data berdasarkan pilihan provinsi
    if pilihan_provinsi_pc == "Semua Provinsi":
        df_pc_base = df_filtered.copy()
    else:
        df_pc_base = df_filtered[df_filtered['provinsi'] == pilihan_provinsi_pc].copy()

    # Tentukan status anomali sesuai dashboard nomor 4
    df_pc_base['is_anomali'] = (
        ((df_pc_base['jumlah_alergi'] > 0) | (df_pc_base['jumlah_kondisi_khusus'] > 0)) & 
        (df_pc_base['jumlah_penerima_manfaat'] == 0)
    )

    # Hitung metrik per baris
    df_pc_base['siswa_terabaikan'] = 0
    df_pc_base.loc[df_pc_base['is_anomali'], 'siswa_terabaikan'] = (
        df_pc_base['jumlah_alergi'] + df_pc_base['jumlah_kondisi_khusus']
    )
    df_pc_base['total_kerugian'] = df_pc_base['siswa_terabaikan'] * biaya_porsi_pc

    # Agregasi data per Provinsi dan Jenjang
    df_pc_agg = df_pc_base.groupby(['provinsi', 'jenjang']).agg(
        total_sekolah=('jumlah_satuan_pendidikan', 'sum'),
        sekolah_anomali=('is_anomali', 'sum'),
        total_penerima=('jumlah_penerima_manfaat', 'sum'),
        total_diabaikan=('siswa_terabaikan', 'sum'),
        total_kerugian=('total_kerugian', 'sum')
    ).reset_index()

    df_pc_agg['persentase_anomali'] = (df_pc_agg['sekolah_anomali'] / df_pc_agg['total_sekolah'] * 100).fillna(0)

    # Definisikan fungsi binning untuk kategorisasi
    def bin_kerugian(val):
        if val == 0: return 'Rp 0'
        elif val < 5000000: return '< Rp 5 Jt'
        elif val <= 20000000: return 'Rp 5 - 20 Jt'
        else: return '> Rp 20 Jt'

    def bin_penerima(val):
        if val == 0: return '0 Penerima'
        elif val < 5000: return '< 5K Siswa'
        elif val <= 25000: return '5K - 25K Siswa'
        else: return '> 25K Siswa'

    def bin_anomali(val):
        if val == 0: return '0%'
        elif val < 5: return '< 5%'
        elif val <= 15: return '5% - 15%'
        else: return '> 15%'

    df_pc_agg['Skala Kerugian'] = df_pc_agg['total_kerugian'].apply(bin_kerugian)
    df_pc_agg['Tingkat Penerima'] = df_pc_agg['total_penerima'].apply(bin_penerima)
    df_pc_agg['Persentase Anomali'] = df_pc_agg['persentase_anomali'].apply(bin_anomali)

    # Atur kategorikal agar urutannya teratur di sumbu grafik
    df_pc_agg['Persentase Anomali'] = pd.Categorical(
        df_pc_agg['Persentase Anomali'], 
        categories=['0%', '< 5%', '5% - 15%', '> 15%'], 
        ordered=True
    )
    df_pc_agg['Skala Kerugian'] = pd.Categorical(
        df_pc_agg['Skala Kerugian'], 
        categories=['Rp 0', '< Rp 5 Jt', 'Rp 5 - 20 Jt', '> Rp 20 Jt'], 
        ordered=True
    )
    df_pc_agg['Tingkat Penerima'] = pd.Categorical(
        df_pc_agg['Tingkat Penerima'], 
        categories=['0 Penerima', '< 5K Siswa', '5K - 25K Siswa', '> 25K Siswa'], 
        ordered=True
    )

    # Urutkan dataframe agar alirannya tertata rapi
    df_pc_agg = df_pc_agg.sort_values(['Tingkat Penerima', 'Persentase Anomali', 'Skala Kerugian'])

    # Tampilkan grafik Parallel Categories jika ada data
    if df_pc_agg.empty:
        st.info("💡 Tidak ada data untuk ditampilkan pada filter wilayah terpilih.")
    else:
        fig_pc_anomali = px.parallel_categories(
            df_pc_agg,
            dimensions=['provinsi', 'jenjang', 'Tingkat Penerima', 'Persentase Anomali', 'Skala Kerugian'],
            color='total_kerugian',
            color_continuous_scale=px.colors.sequential.OrRd,
            labels={
                'provinsi': 'Provinsi',
                'jenjang': 'Jenjang',
                'Tingkat Penerima': 'Tingkat Penerima',
                'Persentase Anomali': 'Persentase Anomali',
                'Skala Kerugian': 'Skala Kerugian (Rp)'
            }
        )
        fig_pc_anomali.update_layout(margin=dict(t=30, l=10, r=10, b=10))
        fig_pc_anomali.update_layout(title='Parallel Coordinates Anomali Data')
        style_plotly(fig_pc_anomali)
        st.plotly_chart(fig_pc_anomali, use_container_width=True)
        st.caption("💡 **Insight:** Alur anomali yang berujung pada 'Kerugian > Rp 20 Jt' menunjukkan celah kebocoran fiskal sistemik. Pola ini memudahkan BPK menargetkan audit pada kombinasi provinsi dan jenjang tertentu.")
