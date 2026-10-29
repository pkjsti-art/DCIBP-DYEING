import pandas as pd

def run_crosscheck(ibp_prep, pibs_prep):
    # Ini kerangka kosong untuk proses crosscheck
    # Sementara mengembalikan data kosong agar UI tidak error
    hasil_akhir = pd.DataFrame({"Status": ["Belum ada data", "Menunggu logika crosscheck"]})
    return hasil_akhir, pibs_prep
