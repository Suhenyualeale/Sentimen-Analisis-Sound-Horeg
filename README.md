# 🎶 Analisis Sentimen Komentar YouTube — Sound Horeg

## 📘 Deskripsi Proyek
Proyek ini bertujuan untuk **mengumpulkan, membersihkan, dan menganalisis sentimen komentar YouTube** terkait fenomena **Sound Horeg** menggunakan model **DistilBERT Multilingual Sentiment Analysis**.  
Hasil analisis divisualisasikan dalam **dashboard interaktif Streamlit** agar pengguna dapat memahami persepsi publik terhadap konten Sound Horeg secara cepat dan visual.


## 🧩 Struktur Proyek

sound-horeg-youtube/
├── src/
│ ├── youtube_crawler.py # Script crawling komentar YouTube
│ ├── data_cleaner.py # Script pembersihan data mentah
│ ├── sentiment_analysis.py # Script analisis sentimen
│ ├── app_sentiment.py # Dashboard Streamlit interaktif
│
├── data/
│ └── master_csv/
│ ├── sound_horeg_comments.csv # Hasil crawling komentar mentah
│ ├── sound_horeg_cleaned.csv # Data setelah cleaning
│ └── sound_horeg_sentiment.csv # Data setelah analisis sentimen
│
└── README.md



---

## ⚙️ Pipeline Analisis

### 1️⃣ Crawling Komentar YouTube (`youtube_crawler.py`)
- Mengambil komentar dari video YouTube dengan keyword tertentu.
- Dapat menambahkan **kata kunci baru** tanpa menghapus data lama.
- Hasil disimpan dalam `sound_horeg_comments.csv`.

📦 **Output:**  
`../data/master_csv/sound_horeg_comments.csv`

---

### 2️⃣ Pembersihan Data (`data_cleaner.py`)
- Menghapus duplikasi komentar.
- Menghapus emoji, tanda baca berlebih, dan spasi ganda.
- Menstandarkan format teks untuk memudahkan analisis NLP.

📦 **Input:** `sound_horeg_comments.csv`  
📦 **Output:** `sound_horeg_cleaned.csv`

🖥️ Contoh output log:
