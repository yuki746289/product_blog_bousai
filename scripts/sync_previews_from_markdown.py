# Created: 2026-09-09 14:52 JST
# Updated: 2026-09-09 16:13 JST
"""Compatibility wrapper around the preview synchronizer.

B003/B008/B010/B058 were omitted from the original synchronization set even
though Markdown is the editorial source of truth. Keep the reviewed core
unchanged and extend its target set here so CI, local deploy and production
deploy all use the same correction without duplicating the large renderer
implementation.

A small number of bespoke preview pages intentionally keep their hand-built
article bodies. For those pages, concise article-map leads are synchronized
here without regenerating the bespoke body layout.
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

# These articles use bespoke preview bodies that should not be generically
# regenerated. The lead is the public article map, so keep it concise and make
# it summarize the main chapter flow reviewed on 2026-09-09.
LEAD_OVERRIDES = {
    "B013": (
        "水災補償の有無だけでなく、風災との違い、建物・家財・賃貸の対象、"
        "支払条件とハザード、被災後の安全・記録・連絡まで順に確認します。"
    ),
    "B021": (
        "台風前日は、準備の締切を先に決め、24・12・6時間前を目安に屋外・窓・排水・"
        "備蓄・充電・車・家族予定を前倒しします。最後は避難先を確認し、当日に住宅作業を"
        "続けない中止条件まで決めます。"
    ),
    "B024": (
        "地震後の停電・断水に備え、飲料水と生活用水、トイレ、照明・充電、発電機と復電時の"
        "火災、冷蔵庫・情報、集合住宅の設備停止、在宅避難の継続判断まで順に確認します。"
    ),
    "B029": (
        "車載防災用品は、脱出・停止表示・トイレ・水と食品を優先し、ライトやモバイル電源の"
        "車内保管、水害時に車へ戻らない判断、季節・車検に合わせた点検までまとめて考えます。"
    ),
    "B057": (
        "地震直後は、揺れている間の身の安全から始め、揺れが収まった後に津波・火災・電気・"
        "建物の危険を確認します。外出先での行動と、平時に用意しておくことまで時間順に整理します。"
    ),
}


def apply_lead_overrides() -> list[str]:
    registry = _core.load_registry(_core.REGISTRY)
    aliases = _core.preview_aliases(registry)
    by_id = {article["article_id"]: article for article in registry["articles"]}
    changed: list[str] = []

    for article_id in sorted(LEAD_OVERRIDES):
        article = by_id[article_id]
        preview_path = _core.ROOT / article["preview_path"]
        preview = preview_path.read_text(encoding="utf-8")
        match = _core.LEAD_RE.search(preview)
        if not match:
            raise ValueError(f"article-lead not found for {article_id}: {preview_path}")

        rendered = _core.inline_markup(LEAD_OVERRIDES[article_id], aliases)
        updated = (
            preview[: match.start()]
            + match.group("open")
            + rendered
            + match.group("close")
            + preview[match.end() :]
        )
        if updated != preview:
            preview_path.write_text(updated, encoding="utf-8")
            changed.append(article_id)

    return changed


def sync() -> list[str]:
    changed = _core.sync()
    changed.extend(apply_lead_overrides())
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
        ids = (
            set(SYNC_ARTICLE_IDS)
            | set(_core.TARGETED_PREVIEW_REPLACEMENTS)
            | set(LEAD_OVERRIDES)
        )
        for article_id in sorted(ids):
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
