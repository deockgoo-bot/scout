import re

from config import (
    KEYWORDS_STRONG, KEYWORDS_WEAK, STRONG_BONUS, WEAK_BONUS,
    GITHUB_MIN, HN_MIN, GEEKNEWS_MIN, REDDIT_MIN, TOTAL,
)


def _compile(keywords):
    # 단어 경계 매칭: "rag"가 "storage"에, "cli"가 "client"에 걸리는 오탐 방지
    return [re.compile(r"\b" + re.escape(kw) + r"\b", re.IGNORECASE) for kw in keywords]


_STRONG_PATTERNS = _compile(KEYWORDS_STRONG)
_WEAK_PATTERNS = _compile(KEYWORDS_WEAK)


def count_hits(text, patterns):
    return sum(1 for p in patterns if p.search(text))


def apply_filter(items):
    result = []
    for item in items:
        if item["source"] == "geeknews":
            item["keyword_hits"] = 1
            item["score"] = item["popularity"]
            result.append(item)
            continue

        strong = count_hits(item["title"], _STRONG_PATTERNS)
        weak = count_hits(item["title"], _WEAK_PATTERNS)
        # 강한 키워드 1개 이상, 또는 약한 키워드 2개 이상이어야 통과
        if strong == 0 and weak < 2:
            continue
        item["keyword_hits"] = strong + weak
        item["score"] = item["popularity"] * (1 + strong * STRONG_BONUS + weak * WEAK_BONUS)
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
