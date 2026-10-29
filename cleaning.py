import pandas as pd
import streamlit as st
import io

def clean_data_ibp(files):
    all_ibp = pd.DataFrame()
    for file in files:
        # Baca Worksheet (skip 3 baris atas)
        df_ws = pd.read_excel(file, sheet_name='Worksheet', skiprows=3)
        # Baca Keterangan
        df_ket = pd.read_excel(file, sheet_name='Keterangan')
        
        # Gabungkan data dari file yang sama untuk keperluan mapping (disimpan sementara di dictionary atau dict list)
        # Tapi instruksinya, cleaning membersihkan dulu.
        
        # Hapus spasi berlebih atau karakter ghaib (strip)
        df_ws = df_ws.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df_ket = df_ket.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        # Karena Keterangan perlu di-mapping nanti, kita gabungkan dulu semua Worksheet
        # Untuk mapping Keterangan, asumsi: Kode di sheet Keterangan unik antar file atau file ini diproses per file dulu baru digabung.
        # Agar aman, kita mapping per file dulu di tahap preparation, jadi cleaning mereturn list of tuples (df_ws, df_ket) atau kita proses mappingnya sebelum concat.
        pass # Akan disesuaikan
        
    return files # Mengembalikan files asli untuk diproses di preparation agar mapping per file akurat

def clean_data_pibs(files):
    all_pibs = pd.DataFrame()
    for file in files:
        df = pd.read_excel(file)
        
        # Hapus spasi berlebih
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        # Filter No. Ticket yang mengandung "PIBS"
        if 'No. Ticket' in df.columns:
            df = df[df['No. Ticket'].astype(str).str.contains('PIBS', na=False, case=False)]
            
        all_pibs = pd.concat([all_pibs, df], ignore_index=True)
    return all_pibs
