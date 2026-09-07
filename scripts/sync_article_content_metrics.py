from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path

from audit_article_content_metrics import audit

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATHS = [
    ROOT / "data" / "content_registry.json",
    ROOT / "data" / "content_registry_additions.json",
]
MODIFIED_ARTICLES_20260907 = {
    "B001", "B017", "B023", "B025", "B031", "B032", "B043",
    "B045", "B046", "B047", "B053", "B054", "B055", "B056",
}


def with_metric_after_article_id(article: dict, count: int) -> dict:
    ordered: OrderedDict[str, object] = OrderedDict()
    inserted = False
    for key, value in article.items():
        if key == "body_char_count_approx":
            continue
        ordered[key] = value
        if key == "article_id":
            ordered["body_char_count_approx"] = count
            inserted = True
    if not inserted:
        raise ValueError("article_id is required")
    return dict(ordered)


def sync() -> None:
    counts = {row.article_id: row.body_char_count for row in audit()}
    seen: set[str] = set()

    for path in REGISTRY_PATHS:
        data = json.loads(path.read_text(encoding="utf-8"))
        updated_articles = []
        for article in data.get("articles", []):
            article_id = article.get("article_id")
            if article_id not in counts:
                updated_articles.append(article)
                continue
            updated = with_metric_after_article_id(article, counts[article_id])
            if article_id in MODIFIED_ARTICLES_20260907 and "modified_at" in updated:
                updated["modified_at"] = "2026-09-07"
            updated_articles.append(updated)
            seen.add(article_id)
        data["articles"] = updated_articles
        if "updated_at" in data:
            data["updated_at"] = "2026-09-07T20:10:00+09:00"
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    missing = sorted(set(counts) - seen)
    if missing:
        raise SystemExit("Registry entries missing for: " + ", ".join(missing))


if __name__ == "__main__":
    sync()
