import streamlit as st
import pandas as pd
from cleaning import clean_data_ibp, clean_data_pibs
from preparation import prepare_ibp, prepare_pibs
from crosscheck import run_crosscheck
from export import generate_excel_download

# Custom CSS for Cyber/Futuristic Theme
st.markdown("""
<style>
    /* Full Futuristic Gradient Cyber Background with Matrix Grid */
    .stApp {
        background: radial-gradient(circle at 30% 20%, rgba(14, 21, 37, 0.95) 0%, rgba(10, 11, 21, 0.98) 100%),
                    linear-gradient(rgba(0, 255, 204, 0.015) 1px, transparent 1px) 0 0 / 20px 20px,
                    linear-gradient(90deg, rgba(0, 255, 204, 0.015) 1px, transparent 1px) 0 0 / 20px 20px;
        color: #00ffcc !important;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Cyber Title & Text Neon Glow Effect */
    h1, h2, h3, h4, h5, p, label, .stMarkdown, .stText {
        color: #00ffcc !important;
    }
    h1, h2, h3 {
        text-shadow: 0 0 5px rgba(0, 255, 204, 0.4), 
                     0 0 15px rgba(0, 255, 204, 0.3), 
                     0 0 30px rgba(0, 255, 204, 0.2);
        letter-spacing: 1px;
    }

    /* Sidebar Visual Overhaul */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #090e1a 0%, #05060b 100%) !important;
        border-right: 2px solid rgba(0, 255, 204, 0.2);
        box-shadow: 5px 0 25px rgba(0, 255, 204, 0.05);
    }
    .sidebar .sidebar-content {
        background: transparent !important;
    }

    /* Streamlit File Upload visual styling */
    .stFileUploader {
        background: rgba(14, 21, 37, 0.6) !important;
        border: 1px solid rgba(0, 255, 204, 0.3) !important;
        border-radius: 8px;
        padding: 15px;
        box-shadow: inset 0 0 15px rgba(0, 255, 204, 0.05);
    }
    .stFileUploader>div>div>div>button {
        color: #00ffcc !important;
        border: 1px solid rgba(0, 255, 204, 0.5) !important;
        background-color: rgba(0, 255, 204, 0.05) !important;
    }

    /* Cybermatic Buttons */
    .stButton>button {
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.1) 0%, rgba(24, 24, 38, 0.8) 100%) !important;
        color: #00ffcc !important;
        border: 1px solid #00ffcc !important;
        box-shadow: 0 0 12px rgba(0, 255, 204, 0.4), inset 0 0 8px rgba(0, 255, 204, 0.2);
        border-radius: 6px;
        font-weight: bold;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background: #00ffcc !important;
        color: #05060b !important;
        box-shadow: 0 0 25px #00ffcc, inset 0 0 10px rgba(255,255,255,0.6);
        transform: translateY(-2px);
    }

    /* Futuristic Cyber Borders & Tables */
    .stDataFrame {
        border: 1px solid rgba(0, 255, 204, 0.4) !important;
        background: rgba(10, 11, 21, 0.9) !important;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.1);
    }
    
    /* Notifikasi Box */
    .stAlert {
        background-color: rgba(14, 21, 37, 0.9) !important;
        border: 1px solid #00ffcc !important;
        color: #00ffcc !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Data Control IBP Dyeing (DCIBP DYEING)")

# 1. Inisialisasi Memori (Session State)
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
                    
                    st.success("Proses silang data selesai! Silakan lihat tabel di bawah.")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses: {e}")

    # 2. Tampilkan Tabel dan Tombol Download DI LUAR tombol proses
    if st.session_state.proses_selesai:
        st.markdown("---")
        st.subheader("Tabel Hasil Cek Data (Worksheet)")
        st.dataframe(st.session_state.hasil_akhir, use_container_width=True)

        excel_data = generate_excel_download(st.session_state.hasil_akhir, st.session_state.pibs_final)
        st.download_button(
            label="Download Data Hasil Crosscheck",
            data=excel_data,
            file_name="Hasil_Crosscheck_DCIBP_Dyeing.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
