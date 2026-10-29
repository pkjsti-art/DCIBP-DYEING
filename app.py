import streamlit as st
import pandas as pd
from cleaning import clean_data_ibp, clean_data_pibs
from preparation import prepare_ibp, prepare_pibs
from crosscheck import run_crosscheck
from export import generate_excel_download
import io

# Custom CSS for Cyber/Futuristic Theme
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #00ffcc;
    }
    h1, h2, h3 {
        color: #00ffcc;
        text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
    }
    .stButton>button {
        background-color: #1a1a2e;
        color: #00ffcc;
        border: 1px solid #00ffcc;
        box-shadow: 0 0 10px #00ffcc;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00ffcc;
        color: #0e1117;
        box-shadow: 0 0 20px #00ffcc, 0 0 30px #00ffcc;
    }
    .stFileUploader>div>div>div>button {
        color: #00ffcc;
    }
    .stDataFrame {
        border: 1px solid #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

st.title("Data Control IBP Dyeing (DCIBP DYEING)")

# Sidebar Menu
with st.sidebar:
    st.header("Menu")
    menu = st.selectbox("Pilih Opsi", ["Crosscheck Data IBP Dyeing"])

if menu == "Crosscheck Data IBP Dyeing":
    st.subheader("Fitur Import Data")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Master IBP Dyeing**")
        files_ibp = st.file_uploader("Upload File Master IBP (Bisa lebih dari 1)", type=["xlsx", "xls"], accept_multiple_files=True, key="ibp")
    with col2:
        st.markdown("**Master PIBS**")
        files_pibs = st.file_uploader("Upload File Master PIBS (Bisa lebih dari 1)", type=["xlsx", "xls"], accept_multiple_files=True, key="pibs")

    if st.button("Proses Data"):
        if not files_ibp or not files_pibs:
            st.error("Silakan upload kedua jenis file (Master IBP dan Master PIBS) terlebih dahulu.")
        else:
            try:
                with st.spinner("Sedang memproses data..."):
                    # 1. Cleaning & Concatenation
                    ibp_clean = clean_data_ibp(files_ibp)
                    pibs_clean = clean_data_pibs(files_pibs)

                    # 2. Preparation
                    ibp_prep = prepare_ibp(ibp_clean)
                    pibs_prep = prepare_pibs(pibs_clean)

                    # 3. Crosscheck
                    hasil_akhir, pibs_final = run_crosscheck(ibp_prep, pibs_prep)
                    
                    st.success("Proses selesai!")

                    # Menampilkan Tabel Hasil
                    st.subheader("Tabel Hasil Cek Data (Worksheet)")
                    st.dataframe(hasil_akhir, use_container_width=True)

                    # Tombol Download
                    excel_data = generate_excel_download(hasil_akhir, pibs_final)
                    st.download_button(
                        label="Download Data Hasil Crosscheck",
                        data=excel_data,
                        file_name="Hasil_Crosscheck_DCIBP_Dyeing.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses: {e}")
