import pandas as pd
from transformers import pipeline
import os
from tqdm import tqdm

def analyze_sentiment(input_path, output_path):
    print(f"📂 Membaca file cleaned: {input_path}")
    df_clean = pd.read_csv(input_path)

    if "comment_sample" not in df_clean.columns:
        raise ValueError("Kolom 'comment_sample' tidak ditemukan dalam dataset!")

    # === CEK FILE HASIL SEBELUMNYA ===
    if os.path.exists(output_path):
        print(f"🔁 File hasil sebelumnya ditemukan: {output_path}")
        df_old = pd.read_csv(output_path)

        # Gabungkan berdasarkan video_id + comment_sample untuk deteksi duplikat
        merged = pd.merge(
            df_clean,
            df_old[["video_id", "comment_sample", "sentiment", "confidence"]],
            on=["video_id", "comment_sample"],
            how="left",
            indicator=True
        )

        df_new = merged[merged["_merge"] == "left_only"].drop(columns=["_merge", "sentiment", "confidence"])
        print(f"📈 Komentar baru yang belum dianalisis: {len(df_new)}")

        if len(df_new) == 0:
            print("✅ Tidak ada komentar baru untuk dianalisis.")
            return
    else:
        print("🆕 Tidak ada file hasil sebelumnya — akan menganalisis semua data.")
        df_old = pd.DataFrame()
        df_new = df_clean.copy()

    print(f"➡️ Total komentar yang akan dianalisis: {len(df_new)}")

    # === LOAD MODEL ===
    try:
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
            device=-1  # CPU
        )
        print("✅ Model sentimen berhasil dimuat.")
    except Exception as e:
        print(f"❌ Gagal memuat model: {e}")
        return

    # === ANALISIS SENTIMEN ===
    sentiments = []
    for text in tqdm(df_new["comment_sample"].astype(str).tolist(), desc="Analisis Sentimen"):
        try:
            result = sentiment_pipeline(text[:512])[0]  # batasi max token
            sentiments.append({
                "sentiment": result["label"],
                "confidence": float(result["score"])
            })
        except Exception:
            sentiments.append({"sentiment": "ERROR", "confidence": 0.0})

    # === GABUNGKAN HASIL BARU ===
    df_new["sentiment"] = [s["sentiment"] for s in sentiments]
    df_new["confidence"] = [s["confidence"] for s in sentiments]

    if not df_old.empty:
        df_final = pd.concat([df_old, df_new], ignore_index=True)
        df_final.drop_duplicates(subset=["video_id", "comment_sample"], inplace=True)
    else:
        df_final = df_new

    # === SIMPAN FILE ===
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_final.to_csv(output_path, index=False, encoding="utf-8")

    print(f"✅ Hasil sentiment analysis disimpan ke: {output_path}")
    print(f"➡️ Total komentar dalam file akhir: {len(df_final)}")
    if not df_old.empty:
        print(f"🆕 Komentar baru dianalisis: {len(df_new)} (dari total {len(df_final)})")

# === MAIN ===
if __name__ == "__main__":
    input_path = "../data/master_csv/sound_horeg_cleaned.csv"
    output_path = "../data/master_csv/sound_horeg_sentiment.csv"
    analyze_sentiment(input_path, output_path)
