# Created: 2026-09-03
"""Article date display and JSON-LD generation for production builds."""

from __future__ import annotations

import html as html_lib
import json
import re
from urllib.parse import urljoin

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ARTICLE_META_RE = re.compile(
    r'<div\s+class=["\']article-meta["\'][^>]*>(?P<body>.*?)</div>',
    re.IGNORECASE | re.DOTALL,
)
SPAN_RE = re.compile(r"<span>(?P<body>.*?)</span>", re.IGNORECASE | re.DOTALL)
DESCRIPTION_RE = re.compile(
    r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
FEATURE_IMAGE_RE = re.compile(
    r'<figure\s+class=["\']article-feature-image["\'][^>]*>.*?'
    r'<img[^>]+src=["\']([^"\']+)["\']',
    re.IGNORECASE | re.DOTALL,
)
GENERATED_JSONLD_RE = re.compile(
    r'<script\s+type=["\']application/ld\+json["\']\s+'
    r'data-generated=["\']article-structured-data["\']>.*?</script>\s*',
    re.IGNORECASE | re.DOTALL,
)

CATEGORY_BREADCRUMBS = {
    "guide": ("防災入門", "guide/index.html"),
    "water-outage": ("停電・断水", "outage/index.html"),
    "blackout": ("停電・断水", "outage/index.html"),
    "flood": ("大雨・水害", "flood/index.html"),
    "typhoon": ("台風", "typhoon/index.html"),
    "earthquake": ("地震", "earthquake/index.html"),
    "vehicle": ("車と災害", "vehicle/index.html"),
    "insurance": ("保険・お金", "insurance/index.html"),
    "home": ("住宅と災害", "home/index.html"),
    "post-disaster": ("被災後", "post-disaster/index.html"),
    "goods": ("防災グッズ", "goods/index.html"),
}


def _required_date(article: dict, field: str) -> str:
    value = article.get(field)
    if not isinstance(value, str) or not DATE_RE.fullmatch(value):
        raise ValueError(f"{article.get('article_id', '?')}: invalid or missing {field}: {value!r}")
    return value


def _jp_date(value: str) -> str:
    year, month, day = (int(part) for part in value.split("-"))
    return f"{year}年{month}月{day}日"


def normalize_article_meta(html: str, article: dict) -> str:
    published = _required_date(article, "published_at")
    modified = _required_date(article, "modified_at")
    checked = _required_date(article, "source_checked_at")

    def replace_meta(match: re.Match[str]) -> str:
        extras: list[str] = []
        for span in SPAN_RE.finditer(match.group("body")):
            raw = span.group(0)
            text = re.sub(r"<[^>]+>", "", span.group("body")).strip()
            if ("商品" in text or "Amazon" in text) and ("確認" in text or "価格" in text):
                extras.append(raw)

        core = [
            f'<span>公開日: <time datetime="{published}">{_jp_date(published)}</time></span>',
            f'<span>最終更新日: <time datetime="{modified}">{_jp_date(modified)}</time></span>',
            f'<span>情報確認日: <time datetime="{checked}">{_jp_date(checked)}</time></span>',
        ]
        return '<div class="article-meta">' + "".join(core + extras) + "</div>"

    if not ARTICLE_META_RE.search(html):
        raise ValueError(f"{article.get('article_id', '?')}: article-meta not found")
    return ARTICLE_META_RE.sub(replace_meta, html, count=1)


def _description(html: str) -> str:
    match = DESCRIPTION_RE.search(html)
    if not match:
        raise ValueError("meta description not found for article structured data")
    return html_lib.unescape(match.group(1).strip())


def _absolute(base_url: str, page_url: str, url: str) -> str:
    if url.startswith(("http://", "https://")):
        return url
    if url.startswith("/"):
        return urljoin(base_url, url.lstrip("/"))
    return urljoin(page_url, url)


def build_structured_data(html: str, article: dict, output_path: str, site_config: dict) -> dict:
    published = _required_date(article, "published_at")
    modified = _required_date(article, "modified_at")
    base_url = site_config["public_base_url"].rstrip("/") + "/"
    page_url = urljoin(base_url, output_path)
    site_name = site_config.get("site_name", "防災くらしガイド")
    language = site_config.get("content_language", "ja-JP")

    organization = {
        "@type": "Organization",
        "name": site_name,
        "url": base_url,
    }
    posting = {
        "@type": "BlogPosting",
        "headline": article["title"],
        "description": _description(html),
        "datePublished": published,
        "dateModified": modified,
        "inLanguage": language,
        "url": page_url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": page_url},
        "author": organization,
        "publisher": organization,
    }

    image_match = FEATURE_IMAGE_RE.search(html)
    if image_match:
        posting["image"] = [_absolute(base_url, page_url, image_match.group(1))]

    category = CATEGORY_BREADCRUMBS.get(article.get("category"))
    if not category:
        raise ValueError(
            f"{article.get('article_id', '?')}: breadcrumb category mapping missing: "
            f"{article.get('category')!r}"
        )
    category_name, category_path = category

    breadcrumb = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "トップ",
                "item": base_url,
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": category_name,
                "item": urljoin(base_url, category_path),
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": article["title"],
                "item": page_url,
            },
        ],
    }

    return {
        "@context": "https://schema.org",
        "@graph": [posting, breadcrumb],
    }


def inject_structured_data(html: str, article: dict, output_path: str, site_config: dict) -> str:
    html = GENERATED_JSONLD_RE.sub("", html)
    payload = build_structured_data(html, article, output_path, site_config)
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    script = (
        '<script type="application/ld+json" '
        'data-generated="article-structured-data">'
        + serialized
        + "</script>\n"
    )
    if "</head>" not in html:
        raise ValueError(f"{article.get('article_id', '?')}: missing </head>")
    return html.replace("</head>", script + "</head>", 1)


def apply_article_metadata(html: str, article: dict, output_path: str, site_config: dict) -> str:
    html = normalize_article_meta(html, article)
    return inject_structured_data(html, article, output_path, site_config)


def validate_article_output(html: str, article: dict, output_path: str, site_config: dict) -> list[str]:
    errors: list[str] = []
    article_id = article.get("article_id", "?")

    try:
        published = _required_date(article, "published_at")
        modified = _required_date(article, "modified_at")
        checked = _required_date(article, "source_checked_at")
    except ValueError as exc:
        return [str(exc)]

    expected_tokens = [
        f'公開日: <time datetime="{published}">',
        f'最終更新日: <time datetime="{modified}">',
        f'情報確認日: <time datetime="{checked}">',
    ]
    for token in expected_tokens:
        if token not in html:
            errors.append(f"{article_id}: missing visible article date token: {token}")

    scripts = re.findall(
        r'<script\s+type=["\']application/ld\+json["\']\s+'
        r'data-generated=["\']article-structured-data["\']>(.*?)</script>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if len(scripts) != 1:
        errors.append(f"{article_id}: generated JSON-LD script count != 1")
        return errors

    try:
        payload = json.loads(scripts[0])
    except json.JSONDecodeError as exc:
        errors.append(f"{article_id}: invalid JSON-LD: {exc}")
        return errors

    graph = payload.get("@graph", [])
    posting = next((node for node in graph if node.get("@type") == "BlogPosting"), None)
    breadcrumb = next((node for node in graph if node.get("@type") == "BreadcrumbList"), None)
    if not posting:
        errors.append(f"{article_id}: BlogPosting missing")
    else:
        if posting.get("headline") != article.get("title"):
            errors.append(f"{article_id}: BlogPosting headline mismatch")
        if posting.get("datePublished") != published:
            errors.append(f"{article_id}: BlogPosting datePublished mismatch")
        if posting.get("dateModified") != modified:
            errors.append(f"{article_id}: BlogPosting dateModified mismatch")

    if not breadcrumb:
        errors.append(f"{article_id}: BreadcrumbList missing")
    else:
        items = breadcrumb.get("itemListElement", [])
        if len(items) != 3:
            errors.append(f"{article_id}: BreadcrumbList item count != 3")
        elif items[-1].get("name") != article.get("title"):
            errors.append(f"{article_id}: BreadcrumbList article name mismatch")

    return errors
