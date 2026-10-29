import pandas as pd

def prepare_ibp(cleaned_data_list):
    all_ws = pd.DataFrame()
    for data in cleaned_data_list:
        df_ws = data['ws']
        df_ket = data['ket']
        
        # Mapping Keterangan
        if 'Kode' in df_ws.columns and 'Kode' in df_ket.columns:
            mapping_dict = dict(zip(df_ket['Kode'], df_ket['Keterangan']))
            df_ws['Keterangan'] = df_ws['Kode'].map(mapping_dict).fillna("")
        else:
            df_ws['Keterangan'] = ""
            
        # Bikin kolom baru (Pandas akan menaruhnya di paling kanan terlebih dahulu)
        df_ws['Qty PIBS'] = None
        df_ws['Crosscheck Qty'] = ""
        df_ws['Selisih (GR)'] = None
        df_ws['Keterangan Data Control'] = ""
        
        # === LOGIKA HARD-SORTING TATA LETAK KOLOM ===
        cols = list(df_ws.columns)
        
        # Fungsi untuk memindah posisi elemen di dalam list
        def move_col(cols_list, col_name, after_col):
            if col_name in cols_list and after_col in cols_list:
                cols_list.remove(col_name)
                cols_list.insert(cols_list.index(after_col) + 1, col_name)
            return cols_list

        # Geser satu per satu sesuai dengan aturan yang disepakati
        cols = move_col(cols, 'Keterangan', 'Gudang')
        cols = move_col(cols, 'Qty PIBS', 'Qty')
        cols = move_col(cols, 'Crosscheck Qty', 'Total')
        cols = move_col(cols, 'Selisih (GR)', 'Crosscheck Qty')
        cols = move_col(cols, 'Keterangan Data Control', 'Selisih (GR)')
        
        # Terapkan urutan kolom baru yang sudah digeser ke dataframe
        df_ws = df_ws[cols]
        
        # Gabungkan data
        all_ws = pd.concat([all_ws, df_ws], ignore_index=True)
        
    return all_ws

def prepare_pibs(df_pibs):
    if 'Tanggal' in df_pibs.columns:
        df_pibs['Tanggal_DT'] = pd.to_datetime(df_pibs['Tanggal'], errors='coerce')
        df_pibs['Kode Tanggal'] = df_pibs['Tanggal_DT'].dt.strftime('%d%m%y')
        
        # Geser kolom 'Kode Tanggal' agar berada tepat setelah 'Tanggal'
        cols = list(df_pibs.columns)
        if 'Kode Tanggal' in cols and 'Tanggal' in cols:
            cols.remove('Kode Tanggal')
            cols.insert(cols.index('Tanggal') + 1, 'Kode Tanggal')
        df_pibs = df_pibs[cols]
            
        df_pibs.drop(columns=['Tanggal_DT'], inplace=True, errors='ignore')
    else:
        df_pibs['Kode Tanggal'] = ""
        
    return df_pibs
