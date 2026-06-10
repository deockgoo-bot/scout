import feedparser
from datetime import datetime, timezone, timedelta


def collect():
    try:
        feed = feedparser.parse("https://news.hada.io/rss/news")
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        items = []
        for entry in feed.entries:
            try:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                if published < cutoff:
                    continue
            except Exception:
                pass
            items.append({
                "source": "geeknews",
                "title": entry.get("title", ""),
                "url": entry.get("link", ""),
                "popularity": 0,
                "keyword_hits": 0,
            })
        print(f"[geeknews] collected {len(items)} items")
        return items
    except Exception as e:
        print(f"[geeknews] error: {e}")
        return []
