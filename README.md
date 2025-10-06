# 🎶 Analisis Sentimen Komentar YouTube — Sound Horeg

Proyek ini bertujuan untuk **mengumpulkan dan menganalisis komentar YouTube** pada konten bertema *Sound Horeg* menggunakan *Natural Language Processing (NLP)* untuk memahami persepsi penonton terhadap fenomena musik ini.

---

## 📊 Deskripsi Singkat

Sistem ini secara otomatis:
1. **Melakukan crawling** komentar YouTube berdasarkan kata kunci
2. **Membersihkan data** (emoji, noise, duplikasi) agar siap dianalisis
3. **Menganalisis sentimen** menggunakan model *DistilBERT Multilingual Sentiment Analysis*
4. **Menyajikan hasilnya** dalam dashboard interaktif berbasis **Streamlit**

---

## ⚙️ Teknologi yang Digunakan

| Komponen | Teknologi |
|----------|-----------|
| **Bahasa Pemrograman** | Python 3 |
| **API** | YouTube Data API v3 |
| **Analisis Teks** | Hugging Face Transformers (`distilbert-base-multilingual-cased`) |
| **Visualisasi Dashboard** | Streamlit, Plotly, Matplotlib |
| **Manajemen Data** | Pandas, CSV |
| **Cloud & Repository** | GitHub |

---

## 🚀 Cara Menjalankan

### 1. Clone Repository
```bash
git clone https://github.com/Susilo19042004/Crawling-Sound-Horeg.git
cd Crawling-Sound-Horeg/src
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Jalankan Proses Analisis

#### a. Crawling komentar
```bash
python youtube_crawler.py
```

#### b. Bersihkan data
```bash
python data_cleaner.py
```

#### c. Analisis sentimen
```bash
python sentiment_analysis.py
```

#### d. Tampilkan dashboard
```bash
streamlit run app_sentiment.py
```

---

## 📈 Fitur Dashboard

Dashboard interaktif menampilkan:

- 📊 **Distribusi sentimen** (positif, negatif, netral)
- 📈 **Rata-rata confidence score** model
- 🔤 **Word Cloud** & Top 20 kata terbanyak
- 💬 **Eksplorasi komentar** berdasarkan sentimen & confidence score
- 📅 **Filter** berdasarkan bulan dan tahun analisis

---

## 🧠 Kesimpulan

Hasil analisis sentimen menunjukkan bahwa:

⚠️ **Sebagian besar komentar** pada konten bertema *Sound Horeg* bersifat **negatif**, menunjukkan adanya kritik, keluhan, atau ketidakpuasan terhadap fenomena musik ini. Hal ini kemungkinan terkait dengan kebisingan, stereotip, atau perbedaan selera musik.

✅ **Komentar positif dan netral** juga ditemukan dalam jumlah yang cukup signifikan, menandakan bahwa masih ada sebagian penonton yang mengapresiasi atau menerima konten *Sound Horeg*.

📊 **Dashboard Streamlit** memudahkan eksplorasi hasil analisis secara visual, membantu memahami tren opini masyarakat secara lebih cepat dan interaktif.

---

