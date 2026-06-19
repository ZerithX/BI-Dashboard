# 🍱 Dashboard Business Intelligence: Program Makan Bergizi Gratis (MBG)

Selamat datang di repositori **Dashboard BI MBG**! Dashboard interaktif ini dirancang menggunakan **Streamlit** untuk memantau sebaran fasilitas pendidikan, katering, kondisi medis khusus siswa, serta mendeteksi anomali operasional pada program Makan Bergizi Gratis (MBG) di Indonesia.

---

## 🚀 Fitur Utama
1. **Ringkasan Eksekutif (KPI):** Metrik ringkas mengenai total satuan pendidikan, kecamatan, penerima manfaat, dan kondisi medis khusus.
2. **Tabel Ringkasan per Provinsi (Interaktif):** 
   - Menampilkan total sekolah, proporsi Negeri/Swasta, total penerima manfaat, dan jumlah kondisi medis khusus.
   - **Klik nama provinsi** untuk memfilter seluruh grafik dan data di dashboard secara dinamis.
3. **Visualisasi Data Dinamis:**
   - Bar Chart: Peta Kerentanan Medis per Kecamatan.
   - Pie Chart: Konsentrasi Kondisi Khusus per Jenjang & Rasio Penerima Manfaat.
   - Bar Chart: Proporsi Status Sekolah & Cakupan Penerima per Jenjang.
4. **Deteksi Anomali Data:** Mengidentifikasi data mencurigakan secara otomatis (misalnya kasus medis terdeteksi, namun jumlah siswa/penerima manfaat tercatat 0).
5. **Analisis Multivariat:** Korelasi interaktif dengan *Bubble Chart* dan struktur hierarki sebaran risiko dengan *Treemap*.

---

## 🛠️ Tech Stack
- **Python 3.10+**
- **Streamlit** (Framework Web Dashboard)
- **Pandas** (Pengolahan Data & Agregasi)
- **Plotly Express** (Visualisasi Grafik Interaktif)

---

## 💻 Cara Menjalankan Project di Lokal

Jika kamu ingin menjalankan dashboard ini di komputer lokalmu, ikuti langkah-langkah berikut:

### 1. Kloning Repositori
Buka terminal/command prompt dan jalankan perintah berikut:
```bash
git clone https://github.com/ZerithX/BI-Dashboard.git
cd BI-Dashboard
```

### 2. Buat & Aktifkan Virtual Environment (Opsional tapi Direkomendasikan)
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instal Dependensi
Instal seluruh library Python yang dibutuhkan melalui `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi Streamlit
Jalankan dashboard di server lokal Anda:
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser Anda pada alamat `http://localhost:8501`.

---

## 🤝 Alur Kontribusi (Git Workflow)

Bagi anggota tim yang ingin menambahkan fitur, memperbarui visualisasi, atau memperbaiki bug pada dashboard ini, gunakan panduan git berikut untuk berkolaborasi dengan aman:

### 1. Ambil Perubahan Terbaru (Pull)
Sebelum Anda mulai menulis kode baru, selalu ambil pembaruan terbaru dari GitHub agar tidak terjadi konflik kode (*conflict code*):
```bash
git pull origin main
```

### 2. Lakukan Perubahan Kode
Edit file `app.py` atau tambahkan dataset baru di folder `data/` sesuai kebutuhan analisis Anda.

### 3. Periksa Status File yang Diubah
Lihat daftar file apa saja yang telah Anda ubah atau tambahkan dengan perintah:
```bash
git status
```

### 4. Simpan Perubahan (Add & Commit)
Tambahkan file yang diubah ke area staging, lalu buat pesan commit yang deskriptif tentang apa yang Anda tambahkan/ubah:
```bash
# Untuk menambahkan semua file baru/berubah
git add .

# Atau jika hanya ingin menambahkan file spesifik
git add app.py

# Buat commit dengan pesan yang jelas
git commit -m "Menambahkan [Nama Fitur/Perubahan] ke dashboard"
```

### 5. Kirim Perubahan ke GitHub (Push)
Kirimkan commit lokal Anda ke repositori utama di GitHub:
```bash
git push origin main
```
*Catatan: Setelah berhasil melakukan push, server Streamlit Community Cloud akan otomatis mendeteksi perubahan ini dan memperbarui dashboard online dalam waktu 1-2 menit.*

---

## 📂 Struktur Direktori Proyek
```text
BI-Dashboard/
│
├── data/                    # Tempat penyimpanan dataset (.csv)
│   └── 15caf9d5-2f49-8340-b228-3a7f3299d100.csv  # Dataset utama program MBG
│
├── app.py                   # File utama kode Streamlit dashboard
├── requirements.txt         # Daftar pustaka / dependencies (streamlit, pandas, plotly)
└── README.md                # Dokumentasi proyek (file ini)
```

Jika memiliki pertanyaan atau menemukan kendala saat setup, hubungi koordinator kelompok Anda! Selamat berkolaborasi! 🍱🚀
