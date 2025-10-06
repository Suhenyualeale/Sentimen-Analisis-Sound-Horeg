import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
from collections import Counter
import re

# === Konfigurasi halaman ===
st.set_page_config(
    page_title="Analisis Sentimen Sound Horeg", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === Custom CSS untuk styling ===
st.markdown("""
<style>
    .stApp { background: #0e1117; }
    .main-header {
        background: #1e1e1e; padding: 40px 30px; border-radius: 12px;
        text-align: center; margin-bottom: 30px; border: 1px solid #2d2d2d;
    }
    .main-header h1 { color: #ffffff; font-size: 2.5em; font-weight: 600; margin: 0; }
    .main-header p { color: #a0a0a0; font-size: 1em; margin-top: 10px; font-weight: 300; }
    .section-header { color: #ffffff; font-size: 1.5em; margin: 40px 0 20px 0;
        padding-bottom: 10px; border-bottom: 2px solid #2d2d2d; font-weight: 500; }
    [data-testid="metric-container"] {
        background: #1e1e1e; padding: 20px; border-radius: 8px; border: 1px solid #2d2d2d;
    }
    [data-testid="stMetricValue"] { font-size: 2em; color: #ffffff; }
    [data-testid="stMetricLabel"] { color: #a0a0a0; }
</style>
""", unsafe_allow_html=True)

# === Load data ===
@st.cache_data
def load_data():
    df = pd.read_csv("../data/master_csv/sound_horeg_sentiment.csv")
    # Pastikan kolom tanggal benar
    if "published_at" in df.columns:
        df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
        df["year"] = df["published_at"].dt.year
        df["month"] = df["published_at"].dt.strftime("%B")
    return df

df = load_data()

# === Header ===
st.markdown("""
<div class="main-header">
    <h1>🎶 Analisis Sentimen Sound Horeg</h1>
    <p>Dashboard Analisis Sentimen Komentar YouTube Berdasarkan Waktu</p>
</div>
""", unsafe_allow_html=True)

# === Filter Tahun & Bulan ===
if "year" in df.columns:
    col_y, col_m = st.columns(2)
    with col_y:
        years = sorted(df["year"].dropna().unique(), reverse=True)
        years = ["All"] + [str(y) for y in years]
        selected_year = st.selectbox("📅 Pilih Tahun", years, index=0)

    with col_m:
        if selected_year != "All":
            months = sorted(df[df["year"] == int(selected_year)]["month"].dropna().unique())
        else:
            months = sorted(df["month"].dropna().unique())
        months = ["All"] + months
        selected_month = st.selectbox("🗓️ Pilih Bulan", months, index=0)

    # Filter data berdasarkan pilihan
    if selected_year != "All":
        df = df[df["year"] == int(selected_year)]
    if selected_month != "All":
        df = df[df["month"] == selected_month]

# === Ringkasan Metrics ===
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Komentar", f"{len(df):,}")
with col2:
    st.metric("Sentimen Unik", df["sentiment"].nunique())
with col3:
    st.metric("Rata-rata Confidence", f"{df['confidence'].mean():.2%}")
with col4:
    st.metric("Sentimen Terbanyak", df["sentiment"].mode()[0])

# === Distribusi Sentimen ===
st.markdown('<p class="section-header">📊 Distribusi Sentimen</p>', unsafe_allow_html=True)
sentiment_counts = df["sentiment"].value_counts().reset_index()
sentiment_counts.columns = ["sentiment", "jumlah"]

col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    fig_pie = px.pie(sentiment_counts, values='jumlah', names='sentiment', hole=0.4)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(
        height=400, paper_bgcolor='#1e1e1e', plot_bgcolor='#1e1e1e',
        font=dict(color='#ffffff'), title_font=dict(size=16, color='#ffffff')
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_chart2:
    fig_bar = px.bar(sentiment_counts, x='sentiment', y='jumlah', text='jumlah')
    fig_bar.update_traces(texttemplate='%{text}', textposition='outside', marker_color='#4a9eff')
    fig_bar.update_layout(
        height=400, paper_bgcolor='#1e1e1e', plot_bgcolor='#1e1e1e',
        font=dict(color='#ffffff'), xaxis=dict(gridcolor='#2d2d2d'), yaxis=dict(gridcolor='#2d2d2d')
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# === Confidence Score ===
st.markdown('<p class="section-header">📈 Confidence Score</p>', unsafe_allow_html=True)
fig_box = px.box(df, x='sentiment', y='confidence', points="all")
fig_box.update_layout(
    height=400, paper_bgcolor='#1e1e1e', plot_bgcolor='#1e1e1e',
    font=dict(color='#ffffff'), xaxis=dict(gridcolor='#2d2d2d'), yaxis=dict(gridcolor='#2d2d2d')
)
st.plotly_chart(fig_box, use_container_width=True)

# === Analisis Kata ===
st.markdown('<p class="section-header">🔤 Kata yang Sering Muncul</p>', unsafe_allow_html=True)

def extract_words(text):
    if pd.isna(text):
        return []
    text = str(text).lower()
    return [w for w in re.findall(r'\b[a-zA-Z]+\b', text) if len(w) > 2]

stopwords = set(["yang","dan","di","ini","itu","dengan","untuk","pada","ada","tidak","sudah","the","and","for"])
all_words = []
for comment in df['comment_sample'].dropna():
    all_words.extend([w for w in extract_words(comment) if w not in stopwords])

if len(all_words) > 0:
    top_words = Counter(all_words).most_common(25)
    top_df = pd.DataFrame(top_words, columns=['Kata', 'Frekuensi'])
    fig_words = px.bar(top_df, y='Kata', x='Frekuensi', orientation='h')
    fig_words.update_layout(
        height=600, paper_bgcolor='#1e1e1e', plot_bgcolor='#1e1e1e',
        font=dict(color='#ffffff'), yaxis={'categoryorder':'total ascending'}
    )
    st.plotly_chart(fig_words, use_container_width=True)

# === Eksplorasi Komentar ===
st.markdown('<p class="section-header">💬 Eksplorasi Komentar</p>', unsafe_allow_html=True)
sentiment_choice = st.selectbox("Pilih Sentimen", df["sentiment"].unique())
min_conf = st.slider("Minimum Confidence", 0.0, 1.0, 0.0, 0.05)
n = st.number_input("Jumlah Komentar", 5, 100, 20)

filtered = df[(df["sentiment"] == sentiment_choice) & (df["confidence"] >= min_conf)][["comment_sample", "confidence"]].head(n)
st.dataframe(filtered, use_container_width=True, height=400)

# === Footer ===
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 20px; color: #606060; font-size: 0.9em;'>
    Dashboard Analisis Sentimen Sound Horeg © 2025
</div>
""", unsafe_allow_html=True)
