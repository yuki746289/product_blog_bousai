# Created: 2026-08-31 22:48 JST
"""Validate the content registry and report freshness/publication issues."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

VALID_STATUSES = {
    "PLANNED",
    "RESEARCHING",
    "DRAFTED",
    "REVIEW_REQUIRED",
    "READY_TO_PUBLISH",
    "PUBLISHED",
    "REVIEW_DUE",
    "SUSPENDED",
    "ARCHIVED",
}
VALID_RISK_LEVELS = {"standard", "elevated", "high"}
VALID_REVIEW_STATUSES = {"NOT_REVIEWED", "APPROVED", "REJECTED"}


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value[:10])


def load_registry(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("registry root must be an object")
    if not isinstance(data.get("articles"), list):
        raise ValueError("registry.articles must be an array")
    return data


def inspect_registry(data: dict[str, Any], today: date | None = None) -> dict[str, list[str]]:
    today = today or date.today()
    errors: list[str] = []
    due: list[str] = []
    publishable: list[str] = []
    seen_ids: set[str] = set()
    seen_slugs: set[str] = set()

    for index, article in enumerate(data["articles"], start=1):
        prefix = f"article[{index}]"
        if not isinstance(article, dict):
            errors.append(f"{prefix}: must be an object")
            continue

        article_id = article.get("article_id")
        slug = article.get("slug")
        status = article.get("status")
        risk_level = article.get("risk_level")
        blockers = article.get("publish_blockers", [])
        manual_required = bool(article.get("manual_review_required"))
        manual_status = article.get("manual_review_status", "NOT_REVIEWED")

        if not article_id:
            errors.append(f"{prefix}: article_id is required")
        elif article_id in seen_ids:
            errors.append(f"{article_id}: duplicate article_id")
        else:
            seen_ids.add(article_id)

        if not slug:
            errors.append(f"{article_id or prefix}: slug is required")
        elif slug in seen_slugs:
            errors.append(f"{article_id or prefix}: duplicate slug")
        else:
            seen_slugs.add(slug)

        if status not in VALID_STATUSES:
            errors.append(f"{article_id or prefix}: invalid status {status!r}")
        if risk_level not in VALID_RISK_LEVELS:
            errors.append(f"{article_id or prefix}: invalid risk_level {risk_level!r}")
        if manual_status not in VALID_REVIEW_STATUSES:
            errors.append(f"{article_id or prefix}: invalid manual_review_status {manual_status!r}")

        if not isinstance(blockers, list):
            errors.append(f"{article_id or prefix}: publish_blockers must be an array")
            blockers = []

        if risk_level == "high" and not manual_required:
            errors.append(f"{article_id or prefix}: high-risk article must require manual review")

        if status == "READY_TO_PUBLISH":
            if blockers:
                errors.append(f"{article_id or prefix}: READY_TO_PUBLISH has blockers")
            if manual_required and manual_status != "APPROVED":
                errors.append(f"{article_id or prefix}: manual review is required but not APPROVED")
            if not blockers and (not manual_required or manual_status == "APPROVED"):
                publishable.append(article_id or prefix)

        try:
            next_review = _parse_date(article.get("next_review_at"))
        except ValueError:
            errors.append(f"{article_id or prefix}: invalid next_review_at")
            next_review = None

        if status == "PUBLISHED" and next_review and next_review <= today:
            due.append(article_id or prefix)

    return {"errors": errors, "due": due, "publishable": publishable}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", nargs="?", default="data/content_registry.json")
    parser.add_argument("--today", help="Override today's date (YYYY-MM-DD)")
    args = parser.parse_args()

    today = _parse_date(args.today) if args.today else date.today()
    report = inspect_registry(load_registry(args.registry), today=today)

    print(f"checked_at={datetime.now().isoformat(timespec='seconds')}")
    print(f"errors={len(report['errors'])}")
    print(f"review_due={len(report['due'])}")
    print(f"ready_to_publish={len(report['publishable'])}")

    for item in report["errors"]:
        print(f"ERROR: {item}")
    for item in report["due"]:
        print(f"REVIEW_DUE: {item}")
    for item in report["publishable"]:
        print(f"READY_TO_PUBLISH: {item}")

    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
