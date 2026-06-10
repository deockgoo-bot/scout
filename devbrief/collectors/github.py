import requests
from bs4 import BeautifulSoup
from config import GITHUB_LIMIT


def collect():
    try:
        resp = requests.get(
            "https://github.com/trending?since=daily",
            headers={"User-Agent": "devbrief/1.0"},
            timeout=15,
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        items = []
        for article in soup.select("article.Box-row")[:GITHUB_LIMIT]:
            name_tag = article.select_one("h2 a")
            if not name_tag:
                continue
            repo = name_tag.get_text(strip=True).replace("\n", "").replace(" ", "")
            desc_tag = article.select_one("p")
            desc = desc_tag.get_text(strip=True) if desc_tag else ""
            title = f"{repo} — {desc}" if desc else repo

            stars_today = 0
            for span in article.select("span.d-inline-block"):
                text = span.get_text(strip=True)
                if "stars today" in text:
                    try:
                        stars_today = int(text.split()[0].replace(",", ""))
                    except ValueError:
                        pass
                    break

            href = name_tag.get("href", "")
            items.append({
                "source": "github",
                "title": title,
                "url": f"https://github.com{href}",
                "popularity": stars_today,
                "keyword_hits": 0,
            })
        print(f"[github] collected {len(items)} items")
        return items
    except Exception as e:
        print(f"[github] error: {e}")
        return []
