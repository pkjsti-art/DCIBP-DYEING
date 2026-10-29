import pandas as pd
import io

def generate_excel_download(hasil_akhir, pibs_final):
    output = io.BytesIO()
    
    # Memaksa konversi ke tipe data numerik (angka) untuk kolom krusial
    cols_to_numeric = ['Qty', 'Qty PIBS', 'Harga', 'Total', 'Selisih (GR)']
    for col in cols_to_numeric:
        if col in hasil_akhir.columns:
            hasil_akhir[col] = pd.to_numeric(hasil_akhir[col], errors='coerce')
            
    # Membuat file excel dengan engine xlsxwriter
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        hasil_akhir.to_excel(writer, sheet_name='Hasil Crosscheck IBP', index=False)
        
        # Tambahkan sheet Master PIBS yang sudah bersih
        if isinstance(pibs_final, pd.DataFrame) and not pibs_final.empty:
            pibs_final.to_excel(writer, sheet_name='Master PIBS', index=False)
            
    return output.getvalue()
