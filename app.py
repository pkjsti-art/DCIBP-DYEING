import streamlit as st
import pandas as pd
from cleaning import clean_data_ibp, clean_data_pibs
from preparation import prepare_ibp, prepare_pibs
from crosscheck import run_crosscheck
from export import generate_excel_download

# --- TARUH KODE st.markdown(""" <style> ... </style> """) ANDA DI SINI ---

st.title("Data Control IBP Dyeing (DCIBP DYEING)")

# 1. Inisialisasi Memori (Session State) agar hasil tidak hilang saat direfresh/download
if 'proses_selesai' not in st.session_state:
    st.session_state.proses_selesai = False
    st.session_state.hasil_akhir = None
    st.session_state.pibs_final = None

# Sidebar Menu
with st.sidebar:
    st.header("Menu")
    menu = st.selectbox("Pilih Opsi", ["Crosscheck Data IBP Dyeing"])

if menu == "Crosscheck Data IBP Dyeing":
    st.subheader("Pusat Unggah Dokumen Kontrol Data")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Master IBP Dyeing**")
        files_ibp = st.file_uploader("Pilih & Unggah File Master IBP", type=["xlsx", "xls"], accept_multiple_files=True, key="ibp")
    with col2:
        st.markdown("**Master PIBS**")
        files_pibs = st.file_uploader("Pilih & Unggah File Master PIBS", type=["xlsx", "xls"], accept_multiple_files=True, key="pibs")

    # Tombol Eksekusi
    if st.button("Proses Data"):
        if not files_ibp or not files_pibs:
            st.error("Silakan upload kedua jenis file (Master IBP dan Master PIBS) terlebih dahulu.")
        else:
            try:
                with st.spinner("Sedang memproses data..."):
                    ibp_clean = clean_data_ibp(files_ibp)
                    pibs_clean = clean_data_pibs(files_pibs)

                    ibp_prep = prepare_ibp(ibp_clean)
                    pibs_prep = prepare_pibs(pibs_clean)

                    hasil_akhir, pibs_final = run_crosscheck(ibp_prep, pibs_prep)
                    
                    # Simpan hasil ke dalam memori
                    st.session_state.hasil_akhir = hasil_akhir
                    st.session_state.pibs_final = pibs_final
                    st.session_state.proses_selesai = True
                    
                    st.success("Proses selesai!")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses: {e}")

    # 2. Tampilkan Tabel dan Tombol Download DI LUAR tombol proses (agar tidak hilang)
    if st.session_state.proses_selesai:
        st.subheader("Tabel Hasil Cek Data (Worksheet)")
        st.dataframe(st.session_state.hasil_akhir, use_container_width=True)

        excel_data = generate_excel_download(st.session_state.hasil_akhir, st.session_state.pibs_final)
        st.download_button(
            label="Download Data Hasil Crosscheck",
            data=excel_data,
            file_name="Hasil_Crosscheck_DCIBP_Dyeing.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
