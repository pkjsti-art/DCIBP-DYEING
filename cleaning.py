import pandas as pd

def clean_data_ibp(files):
    cleaned_data = []
    for file in files:
        # Baca Worksheet (skip 3 baris atas)
        df_ws = pd.read_excel(file, sheet_name='Worksheet', skiprows=3)
        # Baca Keterangan
        df_ket = pd.read_excel(file, sheet_name='Keterangan')
        
        # Hapus spasi berlebih atau karakter ghaib (strip) di seluruh sel bertipe string
        df_ws = df_ws.map(lambda x: str(x).strip() if isinstance(x, str) else x)
        df_ket = df_ket.map(lambda x: str(x).strip() if isinstance(x, str) else x)
        
        cleaned_data.append({'ws': df_ws, 'ket': df_ket})
        
    return cleaned_data

def clean_data_pibs(files):
    all_pibs = pd.DataFrame()
    for file in files:
        df = pd.read_excel(file)
        
        # Hapus spasi berlebih
        df = df.map(lambda x: str(x).strip() if isinstance(x, str) else x)
        
        # Filter No. Ticket yang mengandung "PIBS"
        if 'No. Ticket' in df.columns:
            df = df[df['No. Ticket'].astype(str).str.contains('PIBS', na=False, case=False)]
            
        # Gabungkan jika ada lebih dari 1 file PIBS
        all_pibs = pd.concat([all_pibs, df], ignore_index=True)
        
    return all_pibs
