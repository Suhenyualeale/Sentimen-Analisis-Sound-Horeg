import logging
import os
from youtube_crawler import YouTubeCrawler
from utils import load_json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_DIR, "logs", "crawler.log")
CONFIG_PATH = os.path.join(BASE_DIR, "config", "api_settings.json")
SETTINGS_PATH = os.path.join(BASE_DIR, "config", "settings.json")

# === Setup logging ===
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    logging.info("=== Memulai crawling komentar YouTube (50 video per keyword, 200 komentar/video) ===")

    # Load API key dan pengaturan
    api_config = load_json(CONFIG_PATH)
    settings = load_json(SETTINGS_PATH)

    crawler = YouTubeCrawler(api_key=api_config["youtube_api_key"])

    keywords = [
        "Fakta MUI Sound Horeg Haram",
      "sound Horeg",
      "Sound Horeg Haram",
      "Pro Kontra Sound Horeg",
      "Thomas Alva Edi Sound Horeg",
      "Event Sound Horeg"
    ]

    # Crawl komentar fokus per keyword
    data = crawler.crawl_comments_only(
        keywords,
        video_limit=settings.get("video_limit", 50),          # 50 video per keyword
        comments_per_video=settings.get("comments_per_video", 200),  # 200 komentar per video
        delay=settings.get("delay_seconds", 1)
    )

    # Simpan CSV
    output_path = os.path.join(BASE_DIR, "data", "master_csv", "sound_horeg_comments.csv")
    crawler.save_to_csv(data, output_path)

    logging.info("Crawling selesai. Dataset komentar berhasil disimpan.")
    print(f"[✅] Crawling selesai. Dataset komentar tersimpan → {output_path}")
