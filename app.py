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

st.sidebar.header("Konfigurasi Data")
st.sidebar.markdown("Unggah file CSV Anda atau gunakan data default.")
uploaded_file = st.sidebar.file_uploader("Pilih file dataset", type=['csv'])

@st.cache_data
def load_data(file_source):
    return pd.read_csv(file_source)

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.sidebar.success("File berhasil diunggah!")
elif Path(DEFAULT_DATA).exists():
    df = load_data(DEFAULT_DATA)
    st.sidebar.info(f"Menggunakan data default: `{DEFAULT_DATA}`")
else:
    st.error("❌ Data tidak ditemukan. Silakan unggah file CSV.")
    st.stop()

# --- FILTER DATA PADA SIDEBAR ---
st.sidebar.divider()
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

# Terapkan filter akhir ke dataframe
df_filtered = df[
    (df['provinsi'].isin(provinsi)) &
    (df['kabupaten_kota'].isin(kab_kota)) & 
    (df['kecamatan'].isin(kecamatan)) & 
    (df['jenjang'].isin(jenjang))
]

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
col_vis1, col_vis2 = st.columns(2)

with col_vis1:
    st.subheader("1. Peta Kerentanan Medis per Kecamatan")
    st.markdown("Menampilkan agregasi kasus alergi dan kondisi khusus untuk mitigasi risiko katering.")
    df_medis = df_filtered.groupby('kecamatan')[['jumlah_alergi', 'jumlah_kondisi_khusus']].sum().reset_index()
    # Mengabaikan wilayah yang nilainya 0 agar chart lebih bersih
    df_medis = df_medis[(df_medis['jumlah_alergi'] > 0) | (df_medis['jumlah_kondisi_khusus'] > 0)]
    
    fig_medis = px.bar(df_medis, x='kecamatan', y=['jumlah_alergi', 'jumlah_kondisi_khusus'], 
                       barmode='group', labels={'value': 'Jumlah Kasus', 'variable': 'Kategori'})
    st.plotly_chart(fig_medis, use_container_width=True)

with col_vis2:
    st.subheader("2. Konsentrasi Kondisi Khusus per Jenjang")
    st.markdown("Membantu penentuan jenjang mana yang membutuhkan pengawasan diet lebih ketat.")
    df_jenjang = df_filtered.groupby('jenjang')['jumlah_kondisi_khusus'].sum().reset_index()
    fig_jenjang = px.pie(df_jenjang, values='jumlah_kondisi_khusus', names='jenjang', hole=0.4)
    st.plotly_chart(fig_jenjang, use_container_width=True)

st.divider()

col_vis3, col_vis4 = st.columns(2)

with col_vis3:
    st.subheader("3. Proporsi Status Sekolah")
    st.markdown("Perbandingan fasilitas negeri vs swasta untuk skema distribusi dan birokrasi.")
    df_status = pd.DataFrame({
        'Status': ['Negeri', 'Swasta'],
        'Jumlah': [df_filtered['jumlah_satpen_negeri'].sum(), df_filtered['jumlah_satpen_swasta'].sum()]
    })
    fig_status = px.bar(df_status, x='Status', y='Jumlah', color='Status', text_auto=True)
    st.plotly_chart(fig_status, use_container_width=True)

with col_vis4:
    st.subheader("4. Pemantauan Kualitas Data (Deteksi Anomali)")
    st.markdown("*Flagging* data mencurigakan: Kasus medis (Alergi/Kondisi Khusus) > 0, tetapi Jumlah Siswa atau Penerima Manfaat tercatat 0.")
    
    # Deteksi anomali lebih luas
    df_filtered['total_siswa_cek'] = df_filtered['jumlah_laki'] + df_filtered['jumlah_perempuan']
    df_anomali = df_filtered[
        ((df_filtered['jumlah_alergi'] > 0) | (df_filtered['jumlah_kondisi_khusus'] > 0)) & 
        ((df_filtered['jumlah_penerima_manfaat'] == 0) | (df_filtered['total_siswa_cek'] == 0))
    ]
    
    if not df_anomali.empty:
        st.warning(f"⚠️ Terdeteksi {len(df_anomali)} baris dengan anomali data (Data 'Siswa Hantu').")
        st.dataframe(
            df_anomali[['kabupaten_kota', 'kecamatan', 'jenjang', 'jumlah_alergi', 'jumlah_kondisi_khusus', 'jumlah_penerima_manfaat']],
            use_container_width=True, hide_index=True
        )
    else:
        st.success("✅ Tidak ada anomali terdeteksi pada parameter ini.")

st.divider()

# --- ANALISIS PENERIMA MANFAAT ---
col_vis5, col_vis6 = st.columns(2)

with col_vis5:
    st.subheader("5. Rasio Penerima Manfaat")
    st.markdown("Perbandingan antara total siswa (L+P) yang sudah menerima manfaat program MBG vs yang belum.")
    
    total_l_p = (df_filtered['jumlah_laki'] + df_filtered['jumlah_perempuan']).sum()
    total_penerima_v = df_filtered['jumlah_penerima_manfaat'].sum()
    total_belum = max(0, total_l_p - total_penerima_v)
    
    df_pie_manfaat = pd.DataFrame({
        'Status': ['Penerima', 'Belum Menerima'],
        'Jumlah': [total_penerima_v, total_belum]
    })
    
    fig_pie_manfaat = px.pie(df_pie_manfaat, values='Jumlah', names='Status', 
                             color='Status', color_discrete_map={'Penerima':'#00CC96', 'Belum Menerima':'#EF553B'},
                             hole=0.4)
    st.plotly_chart(fig_pie_manfaat, use_container_width=True)

with col_vis6:
    st.subheader("6. Cakupan Penerima per Jenjang")
    st.markdown("Melihat efektivitas distribusi program MBG di setiap tingkatan pendidikan.")
    
    df_bar_manfaat = df_filtered.groupby('jenjang').agg({
        'jumlah_laki': 'sum',
        'jumlah_perempuan': 'sum',
        'jumlah_penerima_manfaat': 'sum'
    }).reset_index()
    df_bar_manfaat['Total Siswa'] = df_bar_manfaat['jumlah_laki'] + df_bar_manfaat['jumlah_perempuan']
    df_bar_manfaat = df_bar_manfaat.rename(columns={'jumlah_penerima_manfaat': 'Penerima Manfaat'})
    
    fig_bar_manfaat = px.bar(df_bar_manfaat, x='jenjang', y=['Total Siswa', 'Penerima Manfaat'],
                             barmode='group', labels={'value': 'Jumlah Jiwa', 'variable': 'Kategori'},
                             color_discrete_sequence=['#636EFA', '#00CC96'])
    st.plotly_chart(fig_bar_manfaat, use_container_width=True)
        
st.header("📈 Analisis Multivariat")
st.markdown("Menggabungkan beberapa dimensi data (Wilayah, Jenjang, Jumlah Sekolah, dan Risiko Medis) secara bersamaan untuk menemukan korelasi tingkat lanjut.")

col_multi1, col_multi2 = st.columns(2)

with col_multi1:
    st.subheader("7. Korelasi Alergi vs Kondisi Khusus (Bubble Chart)")
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
        template="plotly_white"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_multi2:
    st.subheader("8. Distribusi Risiko dalam Hierarki Wilayah (Treemap)")
    st.markdown("Ukuran Kotak: Jumlah Sekolah | Warna: Intensitas Kasus Kondisi Khusus.")
    
    fig_treemap = px.treemap(
        df_filtered,
        path=[px.Constant("Semua Wilayah"), 'kabupaten_kota', 'kecamatan', 'jenjang'],
        values='jumlah_satuan_pendidikan',
        color='jumlah_kondisi_khusus',
        hover_data=['jumlah_alergi', 'jumlah_penerima_manfaat'],
        color_continuous_scale='Reds', # Warna semakin merah = kondisi khusus semakin banyak
        labels={'jumlah_kondisi_khusus': 'Kondisi Khusus'}
    )
    # Memperbaiki margin agar pas
    fig_treemap.update_layout(margin=dict(t=10, l=10, r=10, b=10))
    st.plotly_chart(fig_treemap, use_container_width=True)