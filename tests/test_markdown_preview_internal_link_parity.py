# Created: 2026-09-06
"""Guard against internal article links being dropped between Markdown and preview HTML.

This intentionally checks only local HTML links. It does not require prose,
heading, or layout parity because preview HTML may edit presentation while
preserving the reader's navigation paths.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit

from bousai_blog.registry import load_registry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "content_registry.json"

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HTML_HREF_RE = re.compile(r"\bhref=[\"']([^\"']+)[\"']", re.IGNORECASE)

# Source Markdown may use final production paths while preview HTML must still
# point at pre-build filenames. Normalize both representations to preview names.
STATIC_PRODUCTION_TO_PREVIEW = {
    "guide/index.html": "category_guide.html",
    "typhoon/index.html": "category_typhoon.html",
    "flood/index.html": "category_flood.html",
    "earthquake/index.html": "category_earthquake.html",
    "vehicle/index.html": "category_vehicle.html",
    "home/index.html": "category_home.html",
    "insurance/index.html": "category_insurance.html",
    "goods/index.html": "category_goods.html",
    "outage/index.html": "category_outage.html",
    "post-disaster/index.html": "category_post_disaster.html",
    "goods/water-food.html": "goods_water_food.html",
    "goods/toilet-hygiene.html": "goods_toilet_hygiene.html",
    "goods/light-information.html": "goods_light_information.html",
    "goods/power-charging.html": "goods_power_charging.html",
}

# These are reviewed editorial omissions, not accidental link loss. Keeping the
# list explicit prevents a broad escape hatch. If preview later restores one of
# these links, the test fails until the stale exception is removed.
INTENTIONAL_OMISSIONS = {
    "B026": {
        "article_b002.html": (
            "The preview keeps more topic-specific related routes (B025/B024 and "
            "the water-food guide); the generic emergency-bag backlink is omitted."
        ),
    },
    "B028": {
        "article_b002.html": (
            "The preview keeps more topic-specific related routes (B004/B024/B027); "
            "the generic emergency-bag backlink is omitted."
        ),
    },
}


def production_to_preview_map(registry: dict) -> dict[str, str]:
    mapping = dict(STATIC_PRODUCTION_TO_PREVIEW)
    for article in registry["articles"]:
        planned = article.get("planned_public_path")
        preview = article.get("preview_path")
        if planned and preview:
            mapping[planned.lstrip("/")] = Path(preview).name
    return mapping


def normalize_local_html_target(
    raw: str,
    aliases: dict[str, str] | None = None,
) -> str | None:
    """Normalize one local HTML target to preview basename plus optional fragment."""
    target = raw.strip().strip("<>")
    parts = urlsplit(target)
    if parts.scheme or parts.netloc or target.startswith(("#", "mailto:", "tel:")):
        return None
    if not parts.path.lower().endswith(".html"):
        return None

    normalized_path = parts.path.replace("\\", "/").lstrip("./")
    preview_name = aliases.get(normalized_path) if aliases else None
    basename = preview_name or Path(normalized_path).name
    if not basename:
        return None
    return basename + (f"#{parts.fragment}" if parts.fragment else "")


def markdown_internal_html_links(text: str, aliases: dict[str, str]) -> set[str]:
    links: set[str] = set()
    for match in MARKDOWN_LINK_RE.finditer(text):
        normalized = normalize_local_html_target(match.group(1), aliases)
        if normalized:
            links.add(normalized)
    return links


def preview_internal_html_links(text: str) -> set[str]:
    links: set[str] = set()
    for match in HTML_HREF_RE.finditer(text):
        normalized = normalize_local_html_target(match.group(1))
        if normalized:
            links.add(normalized)
    return links


class MarkdownPreviewInternalLinkParityTests(unittest.TestCase):
    def test_source_internal_html_links_are_preserved_in_preview(self) -> None:
        registry = load_registry(REGISTRY)
        aliases = production_to_preview_map(registry)
        failures: list[str] = []
        stale_exceptions: list[str] = []

        for article in registry["articles"]:
            source_path = article.get("source_path")
            preview_path = article.get("preview_path")
            if not source_path or not preview_path or not source_path.endswith(".md"):
                continue

            article_id = article["article_id"]
            source = (ROOT / source_path).read_text(encoding="utf-8")
            preview = (ROOT / preview_path).read_text(encoding="utf-8")
            source_links = markdown_internal_html_links(source, aliases)
            preview_links = preview_internal_html_links(preview)
            allowed = set(INTENTIONAL_OMISSIONS.get(article_id, {}))

            for link in allowed:
                if link not in source_links:
                    stale_exceptions.append(
                        f"{article_id}: intentional omission no longer exists in source: {link}"
                    )
                elif link in preview_links:
                    stale_exceptions.append(
                        f"{article_id}: intentional omission is now present in preview: {link}"
                    )

            missing = sorted((source_links - preview_links) - allowed)
            if missing:
                failures.append(
                    f"{article_id}: preview missing source link(s): "
                    + ", ".join(missing)
                )

        self.assertEqual([], stale_exceptions, "\n" + "\n".join(stale_exceptions))
        self.assertEqual([], failures, "\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
