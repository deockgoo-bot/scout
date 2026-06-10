from config import KEYWORDS, KEYWORD_BONUS, GITHUB_MIN, HN_MIN, GEEKNEWS_MIN, REDDIT_MIN, TOTAL


def count_keyword_hits(text):
    text_lower = text.lower()
    return sum(1 for kw in KEYWORDS if kw in text_lower)


def apply_filter(items):
    result = []
    for item in items:
        if item["source"] == "geeknews":
            item["keyword_hits"] = 1
        else:
            hits = count_keyword_hits(item["title"])
            if hits == 0:
                continue
            item["keyword_hits"] = hits
        item["score"] = item["popularity"] * (1 + item["keyword_hits"] * KEYWORD_BONUS)
        result.append(item)
    return result


def select_top(items):
    by_source = {"github": [], "hn": [], "geeknews": [], "reddit": []}
    for item in items:
        src = item["source"]
        if src in by_source:
            by_source[src].append(item)

    for src in by_source:
        by_source[src].sort(key=lambda x: x.get("score", 0), reverse=True)

    minimums = {
        "github": GITHUB_MIN,
        "reddit": REDDIT_MIN,
        "hn": HN_MIN,
        "geeknews": GEEKNEWS_MIN,
    }

    selected = []
    selected_ids = set()

    for src, min_count in minimums.items():
        for item in by_source[src][:min_count]:
            uid = (item["source"], item["url"])
            if uid not in selected_ids:
                selected.append(item)
                selected_ids.add(uid)

    remaining = [
        item for item in items
        if (item["source"], item["url"]) not in selected_ids
    ]
    remaining.sort(key=lambda x: x.get("score", 0), reverse=True)

    for item in remaining:
        if len(selected) >= TOTAL:
            break
        selected.append(item)

    return selected[:TOTAL]
