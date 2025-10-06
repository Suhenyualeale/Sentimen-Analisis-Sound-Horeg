import pandas as pd
import os

def check_csv(path):
    if not os.path.exists(path):
        print(f"❌ File tidak ditemukan: {path}")
        return
    try:
        df = pd.read_csv(path)
        print(f"📂 File: {path}")
        print(f"   Jumlah baris: {len(df)}")
        print(f"   Kolom tersedia: {list(df.columns)}")
        print("=" * 80)
    except Exception as e:
        print(f"⚠️ Gagal membaca {path}: {e}")

if __name__ == "__main__":
    # daftar file yang sering dipakai
    files_to_check = [
        r"D:\sound-horeg-youtube\data\master_csv\sound_horeg_comments.csv",
        r"D:\sound-horeg-youtube\data\master_csv\sound_horeg_cleaned.csv",
        r"D:\sound-horeg-youtube\data\master_csv\sound_horeg_sentiment.csv",
    ]

    for f in files_to_check:
        check_csv(f)
