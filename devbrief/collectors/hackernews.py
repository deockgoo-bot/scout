import requests
from config import HN_LIMIT

BASE = "https://hacker-news.firebaseio.com/v0"


def collect():
    try:
        ids = requests.get(f"{BASE}/topstories.json", timeout=10).json()[:HN_LIMIT]
        items = []
        for id_ in ids:
            try:
                item = requests.get(f"{BASE}/item/{id_}.json", timeout=10).json()
                if not item or item.get("score", 0) < 10:
                    continue
                if not item.get("url") and not item.get("title"):
                    continue
                items.append({
                    "source": "hn",
                    "title": item.get("title", ""),
                    "url": item.get("url") or f"https://news.ycombinator.com/item?id={id_}",
                    "popularity": item.get("score", 0),
                    "keyword_hits": 0,
                })
            except Exception:
                continue
        print(f"[hackernews] collected {len(items)} items")
        return items
    except Exception as e:
        print(f"[hackernews] error: {e}")
        return []
