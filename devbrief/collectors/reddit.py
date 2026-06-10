import os
import time
import praw
from config import REDDIT_LIMIT_PER_SUB, REDDIT_SUBREDDITS


def collect():
    try:
        reddit = praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            user_agent="devbrief/1.0",
        )
        cutoff = time.time() - 86400
        items = []
        for sub_name in REDDIT_SUBREDDITS:
            try:
                sub = reddit.subreddit(sub_name)
                count = 0
                for post in sub.hot(limit=50):
                    if count >= REDDIT_LIMIT_PER_SUB:
                        break
                    if post.created_utc < cutoff:
                        continue
                    items.append({
                        "source": "reddit",
                        "title": post.title,
                        "url": post.url,
                        "popularity": post.score,
                        "keyword_hits": 0,
                        "subreddit": sub_name,
                    })
                    count += 1
            except Exception as e:
                print(f"[reddit] {sub_name} error: {e}")
        print(f"[reddit] collected {len(items)} items")
        return items
    except Exception as e:
        print(f"[reddit] error: {e}")
        return []
