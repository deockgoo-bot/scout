import os
import random
from datetime import datetime
import requests


def translate(text):
    try:
        resp = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": text[:500], "langpair": "en|ko"},
            timeout=5,
        )
        data = resp.json()
        result = data["responseData"]["translatedText"]
        return result or ""
    except Exception as e:
        print(f"[translate] error: {e}")
        return ""

GREETINGS = [
    "좋은 아침이에요! 오늘도 좋은 하루 되세요 ☀️",
    "일어나셨나요? 오늘의 개발 소식 가져왔어요 🌅",
    "모닝커피 한 잔과 함께 오늘의 소식을 확인해보세요 ☕",
    "굿모닝! 밤새 쌓인 기술 소식들이에요 🌞",
    "오늘도 파이팅! 놓치면 아쉬울 소식들 모아왔어요 💪",
]


def format_message(items, date_str):
    icons = {"github": "⭐", "hn": "🔶", "geeknews": "🇰🇷", "reddit": "💬"}
    labels = {"github": "GitHub", "hn": "HN", "geeknews": "GeekNews"}

    best = max(items, key=lambda x: x.get("score", 0))

    greeting = random.choice(GREETINGS)
    lines = [f"{greeting}\n\n📰 데일리 브리핑 ({date_str})\n"]
    for i, item in enumerate(items, 1):
        src = item["source"]
        if src == "reddit":
            label = f"Reddit·{item.get('subreddit', '')}"
        else:
            label = labels.get(src, src)

        title = item["title"][:80]
        url = item["url"]
        ko = translate(title) if src != "geeknews" else ""

        is_best = item is best
        title_str = f"<b>{title}</b>" if is_best else title
        prefix = "🏆 " if is_best else ""
        line = f"{i}. {prefix}[{label}] {title_str}"
        if ko and ko.lower() != title.lower():
            line += f"\n   <b>{ko}</b>" if is_best else f"\n   {ko}"
        line += f"\n   {url}"
        lines.append(line + "\n")

    full = "\n".join(lines)

    if len(full) > 4096:
        mid = len(items) // 2
        return [format_message(items[:mid], date_str)[0], format_message(items[mid:], date_str)[0]]
    return [full]


def send(items, date_str):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    parts = format_message(items, date_str)
    success = 0
    for part in parts:
        resp = requests.post(url, json={"chat_id": chat_id, "text": part, "parse_mode": "HTML"})
        if resp.ok:
            print(f"[sender] message sent ({len(part)} chars)")
            success += 1
        else:
            print(f"[sender] failed: {resp.status_code} {resp.text}")

    if success == 0:
        raise RuntimeError("All Telegram sends failed")
