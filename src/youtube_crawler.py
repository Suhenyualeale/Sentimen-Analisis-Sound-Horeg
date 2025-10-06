import requests
import csv
import os
import logging
import pandas as pd
from time import sleep

class YouTubeCrawler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.search_url = "https://www.googleapis.com/youtube/v3/search"
        self.comment_url = "https://www.googleapis.com/youtube/v3/commentThreads"

    def search(self, query, max_results=50, delay=1):
        """Crawl video berdasarkan kata kunci (default 50 video per kata kunci)"""
        all_videos = []
        next_page_token = None
        total_fetched = 0

        while True:
            batch_size = min(50, max_results - total_fetched)
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": batch_size,
                "key": self.api_key,
                "regionCode": "ID",
                "relevanceLanguage": "id"
            }
            if next_page_token:
                params["pageToken"] = next_page_token

            response = requests.get(self.search_url, params=params)
            if response.status_code != 200:
                logging.error(f"🚫 Gagal ambil video '{query}': {response.status_code} - {response.text}")
                break

            data = response.json()
            items = data.get("items", [])
            for item in items:
                video = {
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "channel": item["snippet"]["channelTitle"],
                    "published_at": item["snippet"]["publishedAt"],
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                }
                all_videos.append(video)
                total_fetched += 1

            logging.info(f"📹 {len(items)} video ditemukan untuk '{query}' (total sejauh ini: {total_fetched})")

            next_page_token = data.get("nextPageToken")
            if not next_page_token or total_fetched >= max_results:
                break

            sleep(delay)

        logging.info(f"✅ Total video untuk '{query}': {len(all_videos)}")
        return all_videos

    def get_comments(self, video_id, max_comments=200, delay=1):
        """Ambil komentar top-level dari video (default 200 komentar)"""
        comments = []
        next_page_token = None

        while len(comments) < max_comments:
            params = {
                "part": "snippet",
                "videoId": video_id,
                "maxResults": min(100, max_comments - len(comments)),
                "textFormat": "plainText",
                "key": self.api_key
            }
            if next_page_token:
                params["pageToken"] = next_page_token

            try:
                response = requests.get(self.comment_url, params=params)
                if response.status_code != 200:
                    logging.warning(f"⚠️ Gagal ambil komentar video {video_id}: {response.status_code}")
                    break

                data = response.json()
                items = data.get("items", [])
                for item in items:
                    text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    comments.append(text)

                next_page_token = data.get("nextPageToken")
                if not next_page_token:
                    break

                sleep(delay)

            except Exception as e:
                logging.error(f"💥 Error ambil komentar video {video_id}: {e}")
                break

        logging.info(f"💬 {len(comments)} komentar diambil dari video {video_id}")
        return comments

    def save_to_csv(self, data, output_path):
        """Simpan hasil crawling. Jika file sudah ada → tambahkan tanpa overwrite."""
        if not data:
            logging.warning("⚠️ Tidak ada data untuk disimpan.")
            return

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_new = pd.DataFrame(data)

        if os.path.exists(output_path):
            df_old = pd.read_csv(output_path)
            combined = pd.concat([df_old, df_new], ignore_index=True)
            combined.drop_duplicates(subset=["video_id", "comment_sample"], inplace=True)
            combined.to_csv(output_path, index=False, encoding="utf-8")
            logging.info(f"🧩 Data baru ditambahkan ke {output_path}. Total sekarang: {len(combined)} baris.")
        else:
            df_new.to_csv(output_path, index=False, encoding="utf-8")
            logging.info(f"✅ File baru dibuat di {output_path} dengan {len(df_new)} baris.")

    def crawl_comments_only(self, keywords, video_limit=50, comments_per_video=200, delay=1):
        """Crawl komentar dari beberapa video per kata kunci"""
        all_data = []
        for kw in keywords:
            logging.info(f"🚀 Mulai crawling keyword: '{kw}'")
            videos = self.search(kw, max_results=video_limit, delay=delay)
            for v in videos:
                comments = self.get_comments(v["video_id"], max_comments=comments_per_video, delay=delay)
                for c in comments:
                    all_data.append({
                        "video_id": v["video_id"],
                        "title": v["title"],
                        "description": v["description"],
                        "channel": v["channel"],
                        "published_at": v["published_at"],
                        "url": v["url"],
                        "comment_sample": c,
                        "keyword": kw  # Tambahkan kolom keyword agar bisa difilter di dashboard
                    })
        return all_data
