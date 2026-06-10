import requests
from config import REDDIT_LIMIT_PER_SUB, REDDIT_SUBREDDITS

HEADERS = {"User-Agent": "devbrief/1.0"}


def collect():
    try:
        items = []
        for sub_name in REDDIT_SUBREDDITS:
            try:
                url = f"https://www.reddit.com/r/{sub_name}/hot.json?limit={REDDIT_LIMIT_PER_SUB}"
                resp = requests.get(url, headers=HEADERS, timeout=10)
                print(f"[reddit] {sub_name} status: {resp.status_code}")
                resp.raise_for_status()
                posts = resp.json()["data"]["children"]
                for post in posts:
                    data = post["data"]
                    items.append({
                        "source": "reddit",
                        "title": data["title"],
                        "url": data.get("url", ""),
                        "popularity": data.get("score", 0),
                        "keyword_hits": 0,
                        "subreddit": sub_name,
                    })
            except Exception as e:
                print(f"[reddit] {sub_name} error: {e}")
        print(f"[reddit] collected {len(items)} items")
        return items
    except Exception as e:
        print(f"[reddit] error: {e}")
        return []
