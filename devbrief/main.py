from datetime import datetime

from collectors.github import collect as collect_github
from collectors.hackernews import collect as collect_hn
from collectors.geeknews import collect as collect_geeknews
from collectors.reddit import collect as collect_reddit
from filter import apply_filter, select_top
from sender import send


def main():
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[main] DevBrief {today}")

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(collect_github),
            executor.submit(collect_hn),
            executor.submit(collect_geeknews),
            executor.submit(collect_reddit),
        ]
        all_items = []
        for f in futures:
            all_items.extend(f.result())

    print(f"[main] total collected: {len(all_items)}")

    filtered = apply_filter(all_items)
    print(f"[main] after filter: {len(filtered)}")

    selected = select_top(filtered)
    print(f"[main] selected: {len(selected)}")

    send(selected, today)
    print("[main] done")


if __name__ == "__main__":
    main()
