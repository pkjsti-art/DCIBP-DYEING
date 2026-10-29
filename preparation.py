import pandas as pd

def prepare_ibp(cleaned_data_list):
    all_ws = pd.DataFrame()
    for data in cleaned_data_list:
        df_ws = data['ws']
        df_ket = data['ket']
        
        # Mapping kolom 'Keterangan' dari sheet Keterangan ke Worksheet berdasarkan 'Kode'
        if 'Kode' in df_ws.columns and 'Kode' in df_ket.columns:
            mapping_dict = dict(zip(df_ket['Kode'], df_ket['Keterangan']))
            df_ws['Keterangan'] = df_ws['Kode'].map(mapping_dict)
        else:
            df_ws['Keterangan'] = "" 
            
        # Menambahkan kolom-kolom baru sesuai kebutuhan
        df_ws['Qty PIBS'] = None
        df_ws['Crosscheck Qty'] = ""
        df_ws['Selisih (GR)'] = None
        df_ws['Keterangan Data Control'] = ""
        
        # Gabungkan semua data IBP yang sudah dipreparasi
        all_ws = pd.concat([all_ws, df_ws], ignore_index=True)
        
    return all_ws

def prepare_pibs(df_pibs):
    # Membuat 'Kode Tanggal' dengan format DDMMYY
    if 'Tanggal' in df_pibs.columns:
        # Konversi ke datetime (memastikan format terbaca walau dari teks)
        df_pibs['Tanggal_DT'] = pd.to_datetime(df_pibs['Tanggal'], errors='coerce')
        # Format menjadi 6 digit angka (misal 090126)
        df_pibs['Kode Tanggal'] = df_pibs['Tanggal_DT'].dt.strftime('%d%m%y')
        df_pibs.drop(columns=['Tanggal_DT'], inplace=True)
    else:
        df_pibs['Kode Tanggal'] = ""
        
    return df_pibs
