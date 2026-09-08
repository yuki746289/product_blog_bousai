# Updated: 2026-09-08 14:06 JST
"""Load the base content registry plus reviewed additions and metadata patches.

The original registry is intentionally kept stable. New article batches can be
reviewed as small adjacent JSON files, and existing article metadata can be
updated through small reviewed patch files instead of replacing the large base
registry document in one commit.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

ADDITIONS_GLOB = "content_registry_additions*.json"
UPDATES_GLOB = "content_registry_updates*.json"


def _read_registry_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"registry root must be an object: {path}")
    if not isinstance(data.get("articles"), list):
        raise ValueError(f"registry.articles must be an array: {path}")
    return data


def _apply_article_updates(data: dict[str, Any], updates_path: Path) -> None:
    updates = _read_registry_file(updates_path)
    by_id = {
        article.get("article_id"): article
        for article in data["articles"]
        if article.get("article_id")
    }

    for patch in updates["articles"]:
        article_id = patch.get("article_id")
        if not article_id:
            raise ValueError(f"article_id is required in update patch: {updates_path}")
        if article_id not in by_id:
            raise ValueError(
                f"registry update refers to unknown article {article_id}: {updates_path}"
            )
        if len(patch) < 2:
            raise ValueError(
                f"registry update for {article_id} has no fields to update: {updates_path}"
            )
        by_id[article_id].update(deepcopy(patch))


def load_registry(path: str | Path, *, include_additions: bool = True) -> dict[str, Any]:
    """Load a registry, append reviewed additions, then apply metadata patches."""
    registry_path = Path(path)
    data = deepcopy(_read_registry_file(registry_path))

    if not include_additions or registry_path.name != "content_registry.json":
        return data

    for additions_path in sorted(registry_path.parent.glob(ADDITIONS_GLOB)):
        additions = _read_registry_file(additions_path)
        data["articles"].extend(deepcopy(additions["articles"]))

    for updates_path in sorted(registry_path.parent.glob(UPDATES_GLOB)):
        _apply_article_updates(data, updates_path)

    return data
