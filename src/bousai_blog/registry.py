# Updated: 2026-09-08 08:16 JST
"""Load the base content registry plus small reviewed additions.

The original registry is intentionally kept stable. New article batches can be
reviewed as small adjacent JSON files instead of replacing the entire large
registry document in one commit.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

ADDITIONS_GLOB = "content_registry_additions*.json"


def _read_registry_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"registry root must be an object: {path}")
    if not isinstance(data.get("articles"), list):
        raise ValueError(f"registry.articles must be an array: {path}")
    return data


def load_registry(path: str | Path, *, include_additions: bool = True) -> dict[str, Any]:
    """Load a registry and append adjacent reviewed addition batches when present."""
    registry_path = Path(path)
    data = deepcopy(_read_registry_file(registry_path))

    if not include_additions or registry_path.name != "content_registry.json":
        return data

    for additions_path in sorted(registry_path.parent.glob(ADDITIONS_GLOB)):
        additions = _read_registry_file(additions_path)
        data["articles"].extend(deepcopy(additions["articles"]))
    return data
