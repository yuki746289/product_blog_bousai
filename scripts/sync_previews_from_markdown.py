# Created: 2026-09-09 14:52 JST
# Updated: 2026-09-09 21:23 JST
"""Compatibility wrapper around the preview synchronizer.

Markdown is the editorial source of truth. The reviewed core regenerates full
article bodies only for pages where that is safe. Some preview pages retain
bespoke hand-built bodies, but their public ``article-lead`` must still follow
the reviewed Markdown introduction rather than drift as a separate copy.

This wrapper therefore:

1. extends full-body synchronization for reviewed articles omitted from the
   original core set;
2. synchronizes the lead for every B001-B060 page from its Markdown intro;
3. normalizes every article breadcrumb so its category is a real, clickable
   published category rather than an unlinked display-only label;
4. inserts a breadcrumb when an older bespoke preview omitted it entirely;
5. exposes every user-facing category directly in the site navigation;
6. keeps category pages flat so reaching an article never requires an
   intermediate category-group page.

There are no article-specific lead overrides. If an article lead needs editorial
improvement, update the Markdown introduction itself so source, review and public
output remain a single chain of truth.
"""

from __future__ import annotations

import argparse
import html as html_lib
import re
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

# User-facing categories are intentionally flat. Every category is reachable
# directly from the global navigation; no intermediate grouping page is needed.
SITE_NAV_LINKS = (
    ("防災入門", "category_guide.html"),
    ("台風", "category_typhoon.html"),
    ("大雨・水害", "category_flood.html"),
    ("地震", "category_earthquake.html"),
    ("停電・断水", "category_outage.html"),
    ("被災後・復旧", "category_post_disaster.html"),
    ("住宅", "category_home.html"),
    ("車", "category_vehicle.html"),
    ("保険", "category_insurance.html"),
    ("防災グッズ", "category_goods.html"),
    ("地域別", "category_region.html"),
    ("Q&A", "qa.html"),
)

# Canonical visible article-category destinations in preview. build_public.py
# rewrites these flat preview links to the nested production category paths.
CATEGORY_PREVIEW_BREADCRUMBS = {
    "guide": ("防災入門", "category_guide.html"),
    "water-outage": ("停電・断水", "category_outage.html"),
    "blackout": ("停電・断水", "category_outage.html"),
    "flood": ("大雨・水害", "category_flood.html"),
    "typhoon": ("台風", "category_typhoon.html"),
    "earthquake": ("地震", "category_earthquake.html"),
    "vehicle": ("車と災害", "category_vehicle.html"),
    "insurance": ("保険・お金", "category_insurance.html"),
    "home": ("住宅と災害", "category_home.html"),
    "post-disaster": ("被災後・復旧", "category_post_disaster.html"),
    "goods": ("防災グッズ", "category_goods.html"),
}

# Category pages themselves are top-level user destinations. The tuple is
# (parent label, parent preview path, current category label). Parents are null
# by design so the public information architecture remains one category deep.
CATEGORY_PAGE_HIERARCHY = {
    "category_guide.html": (None, None, "防災入門"),
    "category_typhoon.html": (None, None, "台風"),
    "category_flood.html": (None, None, "大雨・水害"),
    "category_earthquake.html": (None, None, "地震"),
    "category_outage.html": (None, None, "停電・断水"),
    "category_post_disaster.html": (None, None, "被災後・復旧"),
    "category_vehicle.html": (None, None, "車と災害"),
    "category_home.html": (None, None, "住宅と災害"),
    "category_insurance.html": (None, None, "保険・お金"),
    "category_goods.html": (None, None, "防災グッズ"),
    "category_region.html": (None, None, "地域別"),
}

BREADCRUMB_RE = re.compile(
    r'<nav\s+class=["\']breadcrumb["\'][^>]*>(?P<body>.*?)</nav>',
    re.IGNORECASE | re.DOTALL,
)
SITE_NAV_RE = re.compile(
    r'<nav\s+class=["\']site-nav["\'][^>]*>.*?</nav>',
    re.IGNORECASE | re.DOTALL,
)
MAIN_OPEN_RE = re.compile(r"<main\b[^>]*>", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")


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


def _current_breadcrumb_label(match: re.Match[str], article: dict) -> str:
    """Keep the concise current-page crumb while replacing its category parent."""
    visible = html_lib.unescape(TAG_RE.sub("", match.group("body")))
    parts = [part.strip() for part in visible.split(">") if part.strip()]
    if len(parts) >= 2:
        return parts[-1]
    return article["title"]


def _breadcrumb_markup(category_name: str, category_preview: str, current_label: str) -> str:
    return (
        '<nav class="breadcrumb" aria-label="パンくずリスト">'
        '<a href="index.html">トップ</a> &gt; '
        f'<a href="{category_preview}">{html_lib.escape(category_name)}</a> &gt; '
        f"{html_lib.escape(current_label)}</nav>"
    )


def apply_article_breadcrumbs() -> list[str]:
    """Link or insert every article breadcrumb to its canonical published category."""
    registry = _core.load_registry(_core.REGISTRY)
    by_id = {article["article_id"]: article for article in registry["articles"]}
    missing = ALL_ARTICLE_IDS - set(by_id)
    if missing:
        raise ValueError(f"registry missing article ids: {sorted(missing)}")

    changed: list[str] = []
    for article_id in sorted(ALL_ARTICLE_IDS):
        article = by_id[article_id]
        category = article.get("category")
        category_info = CATEGORY_PREVIEW_BREADCRUMBS.get(category)
        if not category_info:
            raise ValueError(f"breadcrumb category mapping missing for {article_id}: {category!r}")
        category_name, category_preview = category_info
        category_path = _core.ROOT / "preview" / category_preview
        if not category_path.exists():
            raise FileNotFoundError(
                f"breadcrumb category page missing for {article_id}: {category_path}"
            )

        preview_path = _core.ROOT / article["preview_path"]
        preview = preview_path.read_text(encoding="utf-8")
        match = BREADCRUMB_RE.search(preview)
        if match:
            current_label = _current_breadcrumb_label(match, article)
            replacement = _breadcrumb_markup(category_name, category_preview, current_label)
            updated = preview[: match.start()] + replacement + preview[match.end() :]
        else:
            main_match = MAIN_OPEN_RE.search(preview)
            if not main_match:
                raise ValueError(f"main element not found for {article_id}: {preview_path}")
            replacement = _breadcrumb_markup(category_name, category_preview, article["title"])
            updated = preview[: main_match.end()] + replacement + preview[main_match.end() :]

        if updated != preview:
            preview_path.write_text(updated, encoding="utf-8")
            changed.append(article_id)
    return changed


def _site_nav_markup() -> str:
    anchors = "".join(
        f'<a href="{href}">{html_lib.escape(label)}</a>'
        for label, href in SITE_NAV_LINKS
    )
    return f'<nav class="site-nav" aria-label="メインナビゲーション">{anchors}</nav>'


def apply_site_navigation() -> list[str]:
    """Expose every user-facing category directly from the global navigation."""
    preview_dir = _core.ROOT / "preview"
    replacement = _site_nav_markup()
    changed: list[str] = []

    for path in sorted(preview_dir.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        if not SITE_NAV_RE.search(html):
            continue
        updated = SITE_NAV_RE.sub(replacement, html, count=1)
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            changed.append(f"NAV:{path.name}")
    return changed


def _category_page_breadcrumb(parent_label: str | None, parent_href: str | None, current_label: str) -> str:
    parts = ['<a href="index.html">トップ</a>']
    if parent_label and parent_href:
        parts.append(f'<a href="{parent_href}">{html_lib.escape(parent_label)}</a>')
    parts.append(html_lib.escape(current_label))
    return '<nav class="breadcrumb" aria-label="パンくずリスト">' + " &gt; ".join(parts) + "</nav>"


def apply_category_page_breadcrumbs() -> list[str]:
    """Keep category breadcrumbs flat: top -> category."""
    preview_dir = _core.ROOT / "preview"
    changed: list[str] = []

    for filename, (parent_label, parent_href, current_label) in CATEGORY_PAGE_HIERARCHY.items():
        path = preview_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"category hierarchy page missing: {path}")
        html = path.read_text(encoding="utf-8")
        match = BREADCRUMB_RE.search(html)
        if not match:
            raise ValueError(f"category breadcrumb missing: {path}")
        replacement = _category_page_breadcrumb(parent_label, parent_href, current_label)
        updated = html[: match.start()] + replacement + html[match.end() :]
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            changed.append(f"CATEGORY:{filename}")
    return changed


def sync() -> list[str]:
    changed = _core.sync()
    changed.extend(apply_markdown_leads())
    changed.extend(apply_article_breadcrumbs())
    changed.extend(apply_site_navigation())
    changed.extend(apply_category_page_breadcrumbs())
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
        preview_dir = _core.ROOT / "preview"
        for path in sorted(preview_dir.glob("*.html")):
            originals[path] = path.read_text(encoding="utf-8")

    changed = sync()
    print("Synchronized preview content: " + (", ".join(changed) if changed else "none"))

    if args.check and changed:
        for path, original in originals.items():
            path.write_text(original, encoding="utf-8")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
