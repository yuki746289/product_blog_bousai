# Created: 2026-09-06
"""Guard against internal article links being dropped between Markdown and preview HTML.

This intentionally checks only local HTML links. It does not require prose,
heading, or layout parity because preview HTML may edit presentation while
preserving the reader's navigation paths.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "content_registry.json"

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HTML_HREF_RE = re.compile(r"\bhref=[\"']([^\"']+)[\"']", re.IGNORECASE)


def normalize_local_html_target(raw: str) -> str | None:
    """Normalize one local HTML target to basename plus optional fragment."""
    target = raw.strip().strip("<>")
    parts = urlsplit(target)
    if parts.scheme or parts.netloc or target.startswith(("#", "mailto:", "tel:")):
        return None
    if not parts.path.lower().endswith(".html"):
        return None
    basename = Path(parts.path.replace("\\", "/")).name
    if not basename:
        return None
    return basename + (f"#{parts.fragment}" if parts.fragment else "")


def markdown_internal_html_links(text: str) -> set[str]:
    links: set[str] = set()
    for match in MARKDOWN_LINK_RE.finditer(text):
        normalized = normalize_local_html_target(match.group(1))
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
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        failures: list[str] = []

        for article in registry["articles"]:
            source_path = article.get("source_path")
            preview_path = article.get("preview_path")
            if not source_path or not preview_path or not source_path.endswith(".md"):
                continue

            source = (ROOT / source_path).read_text(encoding="utf-8")
            preview = (ROOT / preview_path).read_text(encoding="utf-8")
            source_links = markdown_internal_html_links(source)
            preview_links = preview_internal_html_links(preview)
            missing = sorted(source_links - preview_links)
            if missing:
                failures.append(
                    f"{article['article_id']}: preview missing source link(s): "
                    + ", ".join(missing)
                )

        self.assertEqual([], failures, "\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
