import pandas as pd
import re

def run_crosscheck(ibp_df, pibs_df):
    # 1. Agregasi PIBS (Penjumlahan jika ada duplikasi Kode Tanggal & Kode Obat)
    if not pibs_df.empty and set(['Kode Tanggal', 'Kode Obat', 'Actual']).issubset(pibs_df.columns):
        # Konversi Actual ke angka, nilai error/kosong jadi 0
        pibs_df['Actual'] = pd.to_numeric(pibs_df['Actual'], errors='coerce').fillna(0)
        # Group dan SUM
        pibs_grouped = pibs_df.groupby(['Kode Tanggal', 'Kode Obat'])['Actual'].sum().reset_index()
    else:
        pibs_grouped = pd.DataFrame()

    # 2. Proses Pencocokan
    for index, row in ibp_df.iterrows():
        ket = str(row.get('Keterangan', ''))
        
        # Mengecek apakah ada CMCP dan bukan MANUAL
        if 'CMCP' in ket.upper() and 'MANUAL' not in ket.upper():
            # Ekstrak 6 digit angka tanggal setelah kata CMCP
            match = re.search(r'CMCP.*?(\d{6})', ket.upper())
            if match:
                kode_tanggal = match.group(1)
                kode_bahan = str(row.get('Kode Bahan Baku', ''))
                
                # Ambil Qty IBP dan pastikan bertipe angka
                qty_ibp = pd.to_numeric(row.get('Qty', 0), errors='coerce')
                if pd.isna(qty_ibp): qty_ibp = 0
                    
                # Cari kecocokan di data PIBS yang sudah di-sum
                if not pibs_grouped.empty:
                    matched_pibs = pibs_grouped[
                        (pibs_grouped['Kode Tanggal'] == kode_tanggal) & 
                        (pibs_grouped['Kode Obat'].astype(str) == kode_bahan)
                    ]
                    
                    # Jika data cocok/match
                    if not matched_pibs.empty:
                        # Ambil nilai SUM Actual dari PIBS
                        qty_pibs = matched_pibs['Actual'].values[0]
                        ibp_df.at[index, 'Qty PIBS'] = qty_pibs
                        
                        # Kalkulasi Selisih
                        selisih = qty_ibp - qty_pibs
                        ibp_df.at[index, 'Selisih (GR)'] = selisih
                        
                        # Penentuan Status
                        if selisih == 0:
                            ibp_df.at[index, 'Crosscheck Qty'] = "CORRECT"
                        else:
                            ibp_df.at[index, 'Crosscheck Qty'] = "INCORRECT"
                            
    return ibp_df, pibs_df
