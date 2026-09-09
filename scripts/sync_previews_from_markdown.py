# Created: 2026-09-09 14:52 JST
# Updated: 2026-09-09 18:44 JST
"""Compatibility wrapper around the preview synchronizer.

Markdown is the editorial source of truth. The reviewed core regenerates full
article bodies only for pages where that is safe. Some preview pages retain
bespoke hand-built bodies, but their public ``article-lead`` must still follow
the reviewed Markdown introduction rather than drift as a separate copy.

This wrapper therefore:

1. extends full-body synchronization for reviewed articles omitted from the
   original core set;
2. synchronizes the lead for every B001-B060 page from its Markdown intro.

There are no article-specific lead overrides. If an article lead needs editorial
improvement, update the Markdown introduction itself so source, review and public
output remain a single chain of truth.
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:  # package import used by tests
    from . import sync_previews_core as _core
    from .sync_previews_core import *  # noqa: F401,F403
except ImportError:  # direct script execution: python scripts/...
    import sync_previews_core as _core
    from sync_previews_core import *  # type: ignore # noqa: F401,F403

EXTRA_SYNC_ARTICLE_IDS = {"B003", "B008", "B010", "B058"}
_core.SYNC_ARTICLE_IDS.update(EXTRA_SYNC_ARTICLE_IDS)
SYNC_ARTICLE_IDS = _core.SYNC_ARTICLE_IDS
ALL_ARTICLE_IDS = {f"B{i:03d}" for i in range(1, 61)}


def _replace_lead(preview: str, rendered: str, article_id: str, preview_path: Path) -> str:
    match = _core.LEAD_RE.search(preview)
    if not match:
        raise ValueError(f"article-lead not found for {article_id}: {preview_path}")
    return (
        preview[: match.start()]
        + match.group("open")
        + rendered
        + match.group("close")
        + preview[match.end() :]
    )


def apply_markdown_leads() -> list[str]:
    """Synchronize every B001-B060 public lead from its Markdown introduction."""
    registry = _core.load_registry(_core.REGISTRY)
    aliases = _core.preview_aliases(registry)
    by_id = {article["article_id"]: article for article in registry["articles"]}
    missing = ALL_ARTICLE_IDS - set(by_id)
    if missing:
        raise ValueError(f"registry missing article ids: {sorted(missing)}")

    changed: list[str] = []
    for article_id in sorted(ALL_ARTICLE_IDS):
        article = by_id[article_id]
        source_path = _core.ROOT / article["source_path"]
        preview_path = _core.ROOT / article["preview_path"]
        markdown = source_path.read_text(encoding="utf-8")
        intro, _ = _core.parse_source(markdown)
        if not intro:
            raise ValueError(f"Markdown introduction is empty for {article_id}: {source_path}")

        preview = preview_path.read_text(encoding="utf-8")
        rendered = _core.inline_markup(intro, aliases)
        updated = _replace_lead(preview, rendered, article_id, preview_path)
        if updated != preview:
            preview_path.write_text(updated, encoding="utf-8")
            changed.append(article_id)
    return changed


def sync() -> list[str]:
    changed = _core.sync()
    changed.extend(apply_markdown_leads())
    return sorted(set(changed))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if synchronization would change tracked preview files.",
    )
    args = parser.parse_args()

    originals: dict[Path, str] = {}
    if args.check:
        registry = _core.load_registry(_core.REGISTRY)
        by_id = {article["article_id"]: article for article in registry["articles"]}
        for article_id in sorted(ALL_ARTICLE_IDS):
            path = _core.ROOT / by_id[article_id]["preview_path"]
            originals[path] = path.read_text(encoding="utf-8")

    changed = sync()
    print("Synchronized preview articles: " + (", ".join(changed) if changed else "none"))

    if args.check and changed:
        for path, original in originals.items():
            path.write_text(original, encoding="utf-8")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
