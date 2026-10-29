import streamlit as st
from cleaning import clean_data_ibp, clean_data_pibs
from preparation import prepare_ibp, prepare_pibs
from crosscheck import run_crosscheck
from export import generate_excel_download

# ... (Kode UI/UX Streamlit di sini) ...

if st.button("Proses Data"):
    # 1. Cleaning
    ibp_clean = clean_data_ibp(file_ibp)
    pibs_clean = clean_data_pibs(file_pibs)
    
    # 2. Preparation
    ibp_prep = prepare_ibp(ibp_clean)
    pibs_prep = prepare_pibs(pibs_clean)
    
    # 3. Crosscheck
    hasil_akhir = run_crosscheck(ibp_prep, pibs_prep)
    
    # 4. Tampilkan di UI & Siapkan File Export
    st.dataframe(hasil_akhir)
    file_excel = generate_excel_download(hasil_akhir, pibs_clean)
