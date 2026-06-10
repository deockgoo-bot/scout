import feedparser
from config import REDDIT_LIMIT_PER_SUB, REDDIT_SUBREDDITS


def collect():
    try:
        items = []
        for sub_name in REDDIT_SUBREDDITS:
            try:
                feed = feedparser.parse(f"https://www.reddit.com/r/{sub_name}/hot/.rss")
                count = 0
                for entry in feed.entries:
                    if count >= REDDIT_LIMIT_PER_SUB:
                        break
                    items.append({
                        "source": "reddit",
                        "title": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "popularity": 0,
                        "keyword_hits": 0,
                        "subreddit": sub_name,
                    })
                    count += 1
                print(f"[reddit] {sub_name}: {count} items")
            except Exception as e:
                print(f"[reddit] {sub_name} error: {e}")
        print(f"[reddit] collected {len(items)} items")
        return items
    except Exception as e:
        print(f"[reddit] error: {e}")
        return []
