# Created: 2026-09-06 / Updated: 2026-09-09 09:55 JST
"""Finalize production-only metadata, article infographics and category navigation.

The preview tree intentionally uses preview-only metadata such as noindex.
This production-only step:
- injects reviewed explanatory infographics into selected article sections,
- adds a self-referencing canonical URL to every published HTML page,
- adds the regional category link to the static top navigation,
- renders category article summaries from each article's meta description,
- validates the generated navigation and summaries.
"""

from __future__ import annotations

import json
import posixpath
import re
from html import escape as html_escape
from html import unescape as html_unescape
from pathlib import Path
from urllib.parse import urljoin

from article_diagrams import DIAGRAMS, inject_article_diagram
from bousai_blog.registry import load_registry as load_content_registry

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
REGISTRY = ROOT / "data/content_registry.json"
SITE_CONFIG = ROOT / "config/site.json"
CATEGORY_SUMMARY_MAX_LENGTH = 82

CANONICAL_TAG_RE = re.compile(
    r'<link\b(?=[^>]*\brel=["\'][^"\']*\bcanonical\b[^"\']*["\'])[^>]*>\s*',
    re.IGNORECASE,
)
HREF_RE = re.compile(r'\bhref=["\'](?P<href>[^"\']+)["\']', re.IGNORECASE)
META_DESCRIPTION_RE = re.compile(
    r'<meta\s+name=["\']description["\']\s+content=["\'](?P<description>[^"\']+)["\']',
    re.IGNORECASE,
)
SITE_NAV_RE = re.compile(
    r'(?P<open><nav\b(?=[^>]*\bclass=["\'][^"\']*\bsite-nav\b[^"\']*["\'])[^>]*>)'
    r'(?P<body>.*?)'
    r'(?P<close></nav>)',
    re.IGNORECASE | re.DOTALL,
)
CATEGORY_PAGE_RE = re.compile(
    r'<main\b(?=[^>]*\bclass=["\'][^"\']*\bcategory-page\b[^"\']*["\'])[^>]*>',
    re.IGNORECASE,
)
QA_ANCHOR_RE = re.compile(
    r'<a\b[^>]*\bhref=["\'][^"\']*qa\.html[^"\']*["\'][^>]*>.*?</a>',
    re.IGNORECASE | re.DOTALL,
)
CATEGORY_LINK_RE = re.compile(
    r'(?P<open><a\b[^>]*\bclass=["\'][^"\']*\bcategory-article-link\b[^"\']*["\'][^>]*>)'
    r'(?P<body>.*?)'
    r'(?P<close></a>)',
    re.IGNORECASE | re.DOTALL,
)
DATA_ARTICLE_ID_RE = re.compile(
    r'\bdata-article-id=["\'](?P<article_id>B\d{3})["\']',
    re.IGNORECASE,
)
FIRST_SPAN_RE = re.compile(
    r'<span(?P<attrs>[^>]*)>(?P<title>.*?)</span>',
    re.IGNORECASE | re.DOTALL,
)
REGION_NAV_TEXT_RE = re.compile(r'>\s*地域別\s*</a>', re.IGNORECASE)
CATEGORY_STATIC_STYLE = """<style id="bousai-category-listing-styles">
.category-article-link[data-article-id] { align-items: flex-start; }
.category-article-copy { display: block; min-width: 0; }
.category-article-title { display: block; color: var(--navy); font-size: .96rem; font-weight: 750; line-height: 1.55; }
.category-article-summary { display: block; margin-top: 5px; color: var(--muted); font-size: .82rem; font-weight: 500; line-height: 1.65; text-decoration: none; }
.category-article-link:hover .category-article-summary,
.category-article-link:focus-visible .category-article-summary { text-decoration: none; }
</style>"""


def canonical_url(base_url: str, relative_output_path: str) -> str:
    """Return the absolute self-referencing canonical URL for one output file."""
    base = base_url.rstrip("/") + "/"
    normalized = relative_output_path.lstrip("/")
    if normalized == "index.html":
        return base
    return urljoin(base, normalized)


def inject_canonical(html: str, canonical: str) -> str:
    """Replace any existing canonical annotation with one production canonical."""
    cleaned = CANONICAL_TAG_RE.sub("", html)
    if "</head>" not in cleaned.lower():
        raise ValueError("Missing </head> while injecting canonical URL")

    tag = f'<link rel="canonical" href="{canonical}">\n'
    return re.sub(
        r"</head>",
        lambda _: tag + "</head>",
        cleaned,
        count=1,
        flags=re.IGNORECASE,
    )


def validate_canonical(html: str, expected: str, relative_output_path: str) -> list[str]:
    errors: list[str] = []
    tags = CANONICAL_TAG_RE.findall(html)
    if len(tags) != 1:
        errors.append(
            f"{relative_output_path}: canonical tag count != 1 ({len(tags)})"
        )
        return errors

    href_match = HREF_RE.search(tags[0])
    if not href_match:
        errors.append(f"{relative_output_path}: canonical href missing")
    elif href_match.group("href") != expected:
        errors.append(
            f"{relative_output_path}: canonical mismatch: "
            f"{href_match.group('href')} != {expected}"
        )
    return errors


def is_category_page(html: str) -> bool:
    return CATEGORY_PAGE_RE.search(html) is not None


def extract_meta_description(html: str) -> str:
    match = META_DESCRIPTION_RE.search(html)
    if not match:
        return ""
    return " ".join(html_unescape(match.group("description")).split())


def shorten_category_summary(text: str) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= CATEGORY_SUMMARY_MAX_LENGTH:
        return normalized
    shortened = normalized[: CATEGORY_SUMMARY_MAX_LENGTH - 1].rstrip("、。・ ")
    return shortened + "…"


def load_article_summaries() -> dict[str, str]:
    registry = load_content_registry(REGISTRY)
    summaries: dict[str, str] = {}

    for article in registry.get("articles", []):
        article_id = article.get("article_id")
        output_path = article.get("planned_public_path")
        if not article_id or not output_path:
            continue

        article_path = PUBLIC / output_path.lstrip("/")
        if not article_path.exists():
            continue

        description = extract_meta_description(article_path.read_text(encoding="utf-8"))
        if description:
            summaries[article_id.upper()] = shorten_category_summary(description)

    return summaries


def region_nav_href(relative_output_path: str) -> str:
    """Return a relative href that always retains `region/index.html` in the URL."""
    parent = posixpath.dirname(relative_output_path)
    depth = len([part for part in parent.split("/") if part and part != "."])
    return "../" * depth + "region/index.html"


def inject_region_navigation(html: str, relative_output_path: str) -> str:
    """Add the regional category link to the static site navigation exactly once."""
    match = SITE_NAV_RE.search(html)
    if not match:
        return html

    body = match.group("body")
    if REGION_NAV_TEXT_RE.search(body):
        return html

    href = html_escape(region_nav_href(relative_output_path), quote=True)
    region_anchor = f'<a href="{href}">地域別</a>'
    qa_match = QA_ANCHOR_RE.search(body)
    if qa_match:
        body = body[: qa_match.start()] + region_anchor + "\n" + body[qa_match.start() :]
    else:
        body = body.rstrip() + "\n" + region_anchor + "\n"

    replacement = match.group("open") + body + match.group("close")
    return html[: match.start()] + replacement + html[match.end() :]


def inject_category_listing_styles(html: str) -> str:
    if 'id="bousai-category-listing-styles"' in html:
        return html
    if "</head>" not in html.lower():
        raise ValueError("Missing </head> while injecting category listing styles")
    return re.sub(
        r"</head>",
        lambda _: CATEGORY_STATIC_STYLE + "\n</head>",
        html,
        count=1,
        flags=re.IGNORECASE,
    )


def inject_category_article_summaries(html: str, summaries: dict[str, str]) -> str:
    """Render article meta descriptions below titles on category pages."""

    def replace_link(match: re.Match[str]) -> str:
        opening = match.group("open")
        body = match.group("body")
        closing = match.group("close")

        if "category-article-summary" in body:
            return match.group(0)

        article_id_match = DATA_ARTICLE_ID_RE.search(opening)
        if not article_id_match:
            return match.group(0)

        article_id = article_id_match.group("article_id").upper()
        summary = summaries.get(article_id, "")
        if not summary:
            return match.group(0)

        title_match = FIRST_SPAN_RE.search(body)
        if not title_match:
            return match.group(0)

        title_html = title_match.group("title").strip()
        summary_html = html_escape(summary, quote=False)
        replacement_span = (
            '<span class="category-article-copy">'
            f'<strong class="category-article-title">{title_html}</strong>'
            f'<span class="category-article-summary">{summary_html}</span>'
            "</span>"
        )
        new_body = body[: title_match.start()] + replacement_span + body[title_match.end() :]
        return opening + new_body + closing

    return CATEGORY_LINK_RE.sub(replace_link, html)


def validate_category_enhancements(html: str, relative_output_path: str) -> list[str]:
    errors: list[str] = []
    nav_match = SITE_NAV_RE.search(html)
    if nav_match:
        region_links = REGION_NAV_TEXT_RE.findall(nav_match.group("body"))
        if len(region_links) != 1:
            errors.append(
                f"{relative_output_path}: regional navigation count != 1 ({len(region_links)})"
            )

    if not is_category_page(html):
        return errors

    article_link_count = 0
    for match in CATEGORY_LINK_RE.finditer(html):
        if DATA_ARTICLE_ID_RE.search(match.group("open")):
            article_link_count += 1

    summary_count = html.count('class="category-article-summary"')
    if article_link_count != summary_count:
        errors.append(
            f"{relative_output_path}: category summary count mismatch "
            f"({summary_count}/{article_link_count})"
        )
    if article_link_count and 'id="bousai-category-listing-styles"' not in html:
        errors.append(f"{relative_output_path}: category listing static styles missing")

    return errors


def finalize_public() -> None:
    if not PUBLIC.exists():
        raise FileNotFoundError("public directory is missing; run build_public.py first")

    config = json.loads(SITE_CONFIG.read_text(encoding="utf-8"))
    base_url = config["public_base_url"]
    html_files = sorted(PUBLIC.rglob("*.html"))
    if not html_files:
        raise ValueError("No public HTML files found")

    article_summaries = load_article_summaries()
    errors: list[str] = []
    diagram_count = 0

    for path in html_files:
        relative = path.relative_to(PUBLIC).as_posix()
        expected = canonical_url(base_url, relative)
        html = path.read_text(encoding="utf-8")

        enhanced = inject_article_diagram(html, relative)
        diagram_spec = DIAGRAMS.get(relative)
        if diagram_spec:
            marker = f'data-article-diagram="{diagram_spec["article_id"]}"'
            marker_count = enhanced.count(marker)
            if marker_count != 1:
                errors.append(
                    f"{relative}: article infographic marker count != 1 "
                    f"for {diagram_spec['article_id']} ({marker_count})"
                )
            else:
                diagram_count += 1

        enhanced = inject_region_navigation(enhanced, relative)
        if is_category_page(enhanced):
            enhanced = inject_category_article_summaries(enhanced, article_summaries)
            enhanced = inject_category_listing_styles(enhanced)

        finalized = inject_canonical(enhanced, expected)
        path.write_text(finalized, encoding="utf-8")
        errors.extend(validate_canonical(finalized, expected, relative))
        errors.extend(validate_category_enhancements(finalized, relative))

    if diagram_count != len(DIAGRAMS):
        errors.append(
            f"article infographic presence count mismatch: "
            f"{diagram_count}/{len(DIAGRAMS)}"
        )

    if errors:
        raise ValueError("Production metadata/category validation failed:\n" + "\n".join(errors))

    print(
        f"Production metadata/category navigation finalized for {len(html_files)} HTML files; "
        f"article summaries available: {len(article_summaries)}; "
        f"article infographics present: {diagram_count}."
    )


if __name__ == "__main__":
    finalize_public()
