import pandas as pd
import io

def generate_excel_download(hasil_akhir, pibs_final):
    # Ini kerangka kosong untuk fitur download Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        hasil_akhir.to_excel(writer, sheet_name='Worksheet', index=False)
        if isinstance(pibs_final, pd.DataFrame) and not pibs_final.empty:
            pibs_final.to_excel(writer, sheet_name='Master PIBS', index=False)
    return output.getvalue()
