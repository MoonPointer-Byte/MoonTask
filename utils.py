# utils.py
import json
import os
import threading
import requests
from theme import DATA_FILE

class DataManager:
    @staticmethod
    def load_data():
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return {}
        return {}

    @staticmethod
    def save_data(data):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Save failed: {e}")

class PoetryManager:
    def __init__(self):
        self.default = {
            "content": "人闲桂花落，夜静春山空。",
            "author": "王维",
            "origin": "鸟鸣涧",
            "category": "古诗文-静谧"
        }

    def fetch_poem(self, callback):
        def run():
            try:
                resp = requests.get("https://v1.jinrishici.com/all.json", timeout=3)
                if resp.status_code == 200:
                    data = resp.json()
                    callback({
                        "content": data.get("content"),
                        "author": data.get("author"),
                        "origin": data.get("origin"),
                        "category": data.get("category")
                    })
                else:
                    callback(self.default)
            except:
                callback(self.default)
        threading.Thread(target=run, daemon=True).start()