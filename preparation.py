import pandas as pd

def prepare_ibp(cleaned_data_list):
    all_ws = pd.DataFrame()
    for data in cleaned_data_list:
        df_ws = data['ws']
        df_ket = data['ket']
        
        # 1. Siapkan data mapping Keterangan
        if 'Kode' in df_ws.columns and 'Kode' in df_ket.columns:
            mapping_dict = dict(zip(df_ket['Kode'], df_ket['Keterangan']))
            ket_values = df_ws['Kode'].map(mapping_dict).fillna("")
        else:
            ket_values = ""
            
        # Fungsi bantu untuk menyisipkan kolom tepat di sebelah kanan kolom referensi
        def insert_col_after(df, ref_col, new_col, value):
            if ref_col in df.columns:
                if new_col not in df.columns:
                    idx = df.columns.get_loc(ref_col) + 1
                    df.insert(idx, new_col, value)
                else:
                    df[new_col] = value
            else:
                # Jika kolom referensi tidak ditemukan, taruh di paling kanan
                df[new_col] = value

        # Eksekusi penyisipan kolom sesuai urutan konsep
        insert_col_after(df_ws, 'Gudang', 'Keterangan', ket_values)
        insert_col_after(df_ws, 'Qty', 'Qty PIBS', None)
        insert_col_after(df_ws, 'Total', 'Crosscheck Qty', "")
        insert_col_after(df_ws, 'Crosscheck Qty', 'Selisih (GR)', None)
        insert_col_after(df_ws, 'Selisih (GR)', 'Keterangan Data Control', "")
        
        # Gabungkan semua data IBP yang sudah dipreparasi
        all_ws = pd.concat([all_ws, df_ws], ignore_index=True)
        
    return all_ws

def prepare_pibs(df_pibs):
    if 'Tanggal' in df_pibs.columns:
        # Konversi ke datetime agar seragam
        df_pibs['Tanggal_DT'] = pd.to_datetime(df_pibs['Tanggal'], errors='coerce')
        kode_tanggal_vals = df_pibs['Tanggal_DT'].dt.strftime('%d%m%y')
        
        # Sisipkan 'Kode Tanggal' tepat di sebelah kanan kolom 'Tanggal'
        if 'Kode Tanggal' not in df_pibs.columns:
            idx = df_pibs.columns.get_loc('Tanggal') + 1
            df_pibs.insert(idx, 'Kode Tanggal', kode_tanggal_vals)
        else:
            df_pibs['Kode Tanggal'] = kode_tanggal_vals
            
        df_pibs.drop(columns=['Tanggal_DT'], inplace=True)
    else:
        df_pibs['Kode Tanggal'] = ""
        
    return df_pibs
