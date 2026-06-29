import re

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_reg = False
in_health = False
in_ben = False
in_sch = False
in_multi = False

i = 0
while i < len(lines):
    line = lines[i]
    
    # 1. Sidebar filter Negeri/Swasta
    if 'st.sidebar.divider()' in line:
        new_lines.append(line)
        new_lines.append('status_sekolah = st.sidebar.multiselect("Status Kepemilikan", options=[\'Negeri\', \'Swasta\'], default=[\'Negeri\', \'Swasta\'])\n')
        i += 1
        continue
        
    # 2. Apply status filter
    if "if 'tahun' in df.columns:" in line:
        new_lines.append(line)
        new_lines.append(lines[i+1]) # filter_kondisi = filter_kondisi & (df['tahun'].isin(tahun))
        new_lines.append("if 'Negeri' not in status_sekolah:\n")
        new_lines.append("    filter_kondisi = filter_kondisi & (df['jumlah_satpen_swasta'] > 0)\n")
        new_lines.append("if 'Swasta' not in status_sekolah:\n")
        new_lines.append("    filter_kondisi = filter_kondisi & (df['jumlah_satpen_negeri'] > 0)\n")
        i += 2
        continue

    # 3. Executive Summary
    if '# --- METRIK UTAMA (KPI) ---' in line:
        while not 'st.divider()' in lines[i]:
            i += 1
        # Re-write the Executive Summary block
        exec_block = """# --- METRIK UTAMA (KPI) ---
st.subheader("Ringkasan Eksekutif")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Satuan Pendidikan", f"{df_filtered['jumlah_satuan_pendidikan'].sum():,}")
col2.metric("Total Laki-laki", f"{df_filtered['jumlah_laki'].sum():,}")
col3.metric("Total Perempuan", f"{df_filtered['jumlah_perempuan'].sum():,}")
total_penerima = df_filtered['jumlah_penerima_manfaat'].sum() if 'jumlah_penerima_manfaat' in df_filtered.columns else 0
col4.metric("Total Penerima Manfaat", f"{total_penerima:,}")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Total Kondisi Khusus", f"{df_filtered['jumlah_kondisi_khusus'].sum():,}")
col6.metric("Total Kasus Alergi", f"{df_filtered['jumlah_alergi'].sum():,}")
col7.metric("Total Sekolah Negeri", f"{df_filtered['jumlah_satpen_negeri'].sum():,}")
col8.metric("Total Sekolah Swasta", f"{df_filtered['jumlah_satpen_swasta'].sum():,}")

st.divider()

# --- TABS ---
tab_reg, tab_demo, tab_health, tab_ben, tab_sch, tab_trend, tab_multi = st.tabs([
    "Regional", "Demographics", "Health Conditions", "Beneficiaries", "Schools", "Trends", "Multivariate"
])

with tab_demo:
    st.subheader("Analisis Demografi Siswa")
    st.markdown("Perbandingan jumlah siswa Laki-laki dan Perempuan secara keseluruhan.")
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
        # force x-axis to be discrete
        fig_trend.update_xaxes(type='category')
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Data histori tren tidak cukup untuk ditampilkan.")

with tab_reg:
"""
        new_lines.append(exec_block)
        i += 1
        in_reg = True
        continue
        
    # Handling specific blocks to route to tabs
    if in_reg and 'col_vis1, col_vis2 = st.columns(2)' in line:
        in_reg = False
        in_health = True
        new_lines.append("with tab_health:\n")
        new_lines.append("    " + line)
        i += 1
        continue
        
    if in_health and 'col_vis3, col_vis4 = st.columns(2)' in line:
        in_health = False
        new_lines.append("with tab_sch:\n")
        i += 1
        continue
        
    if 'with col_vis3:' in line:
        # Currently we are in tab_sch
        new_lines.append("    # Proporsi Sekolah\n")
        i += 1
        while 'st.plotly_chart(fig_status' not in lines[i]:
            new_lines.append("    " + lines[i].replace('    ', '', 1))
            i += 1
        new_lines.append("    " + lines[i].replace('    ', '', 1))
        i += 1
        continue
        
    if 'with col_vis4:' in line:
        in_ben = True
        new_lines.append("with tab_ben:\n")
        i += 1
        continue
        
    if in_ben and 'col_multi1, col_multi2 = st.columns(2)' in line:
        in_ben = False
        in_multi = True
        new_lines.append("with tab_multi:\n")
        i += 1
        continue

    if in_multi and 'st.header("Tabel Data Detail")' in line:
        in_multi = False
        new_lines.append(line)
        i += 1
        continue

    # Skip col definitions that we removed
    if 'with col_multi1:' in line or 'with col_multi2:' in line:
        i += 1
        continue
        
    # Indentation logic
    if in_reg or in_health or in_ben or in_multi:
        if line.strip() == 'st.divider()':
            # Skip dividers inside tabs if they are top level
            if not line.startswith(' '):
                i += 1
                continue
        if line.strip() == '':
            new_lines.append(line)
        else:
            if line.startswith('with '):
                new_lines.append('    ' + line)
            elif not line.startswith(' '):
                new_lines.append('    ' + line)
            else:
                new_lines.append('    ' + line)
    else:
        new_lines.append(line)
        
    i += 1

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
