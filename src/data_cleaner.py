import pandas as pd
import re
import os

def remove_emojis(text):
    if not isinstance(text, str):
        return text
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # simbol & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def clean_file(input_path, output_path):
    print(f"📂 Membaca file: {input_path}")
    df = pd.read_csv(input_path)

    if "comment_sample" not in df.columns:
        raise ValueError("Kolom 'comment_sample' tidak ditemukan dalam dataset!")

    print(f"➡️ Jumlah baris sebelum cleaning: {len(df)}")

    # Bersihkan emoji
    df["comment_sample"] = df["comment_sample"].astype(str).apply(remove_emojis)

    # Simpan hasil cleaned
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"✅ File cleaned disimpan ke: {output_path}")
    print(f"➡️ Jumlah baris sesudah cleaning: {len(df)}")


if __name__ == "__main__":
    input_path = "../data/master_csv/sound_horeg_comments.csv"
    output_path = "../data/master_csv/sound_horeg_cleaned.csv"
    clean_file(input_path, output_path)
