import json
import os

def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
