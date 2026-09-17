# Created: 2026-09-14 22:40 JST
# Updated: 2026-09-17 22:17 JST
"""Audit production sitemap indexability and critical live navigation structure."""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "site.json"
GOOGLEBOT_UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
REGION_NAV_LABEL = "地域・疑問から探す"
SITE_NAV_RE = re.compile(
    r'(?P<open><nav\b(?=[^>]*\bclass=["\'][^"\']*\bsite-nav\b[^"\']*["\'])[^>]*>)'
    r'(?P<body>.*?)'
    r'(?P<close></nav>)',
    re.IGNORECASE | re.DOTALL,
)
LEGACY_REGION_NAV_RE = re.compile(
    r'<a\b[^>]*>\s*地域別\s*</a>',
    re.IGNORECASE | re.DOTALL,
)


class RobotsMetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.noindex = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "meta":
            return
        values = {key.lower(): (value or "") for key, value in attrs}
        if values.get("name", "").strip().lower() not in {"robots", "googlebot"}:
            return
        directives = _split_directives(values.get("content", ""))
        if "noindex" in directives:
            self.noindex = True


class RegionMegaNavParser(HTMLParser):
    """Collect the live '地域・疑問から探す' mega-menu structure."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[dict[str, object]] = []
        self.group_count = 0
        self.group_data_items: list[str] = []
        self.submenu_count = 0
        self.anchors: list[dict[str, object]] = []

    def _inside_target_group(self) -> bool:
        return any(bool(frame.get("target_root")) for frame in self.stack)

    def _current_anchor(self) -> dict[str, object] | None:
        for frame in reversed(self.stack):
            anchor = frame.get("anchor")
            if isinstance(anchor, dict):
                return anchor
        return None

    def _inside_strong(self) -> bool:
        return any(frame.get("tag") == "strong" for frame in self.stack)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        values = {key.lower(): (value or "") for key, value in attrs}
        classes = set(values.get("class", "").split())
        target_root = (
            tag == "div"
            and "site-nav__mega-group" in classes
            and values.get("data-group-label") == REGION_NAV_LABEL
        )
        if target_root:
            self.group_count += 1
            self.group_data_items.append(values.get("data-items", ""))

        inside_target = self._inside_target_group() or target_root
        frame: dict[str, object] = {"tag": tag, "target_root": target_root}

        if inside_target and tag == "div" and "site-nav__submenu" in classes:
            self.submenu_count += 1

        if inside_target and tag == "a":
            anchor: dict[str, object] = {
                "classes": classes,
                "href": values.get("href", ""),
                "text_parts": [],
                "strong_parts": [],
            }
            frame["anchor"] = anchor

        self.stack.append(frame)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        anchor = self._current_anchor()
        if anchor is None:
            return
        anchor["text_parts"].append(data)  # type: ignore[union-attr]
        if self._inside_strong():
            anchor["strong_parts"].append(data)  # type: ignore[union-attr]

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if not self.stack:
            return

        match_index = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index].get("tag") == tag:
                match_index = index
                break
        if match_index is None:
            return

        closing = self.stack[match_index:]
        del self.stack[match_index:]
        for frame in closing:
            anchor = frame.get("anchor")
            if isinstance(anchor, dict):
                anchor["text"] = _normalize_text("".join(anchor["text_parts"]))
                anchor["strong_text"] = _normalize_text("".join(anchor["strong_parts"]))
                self.anchors.append(anchor)


def _normalize_text(value: str) -> str:
    return " ".join(value.split())


def _split_directives(value: str) -> set[str]:
    normalized = value.lower().replace(";", ",")
    tokens: set[str] = set()
    for part in normalized.split(","):
        tokens.update(token for token in part.split() if token)
    return tokens


def html_has_meta_noindex(html: str) -> bool:
    parser = RobotsMetaParser()
    parser.feed(html)
    return parser.noindex


def region_mega_nav_failures(html: str) -> list[str]:
    parser = RegionMegaNavParser()
    parser.feed(html)
    parser.close()

    failures: list[str] = []
    if parser.group_count != 1:
        failures.append(
            f"region mega-menu group count must be 1, found {parser.group_count}"
        )
    if parser.group_data_items != ["2"]:
        failures.append(
            "region mega-menu data-items must be exactly ['2'], "
            f"found {parser.group_data_items!r}"
        )
    if parser.submenu_count != 1:
        failures.append(
            f"region mega-menu submenu count must be 1, found {parser.submenu_count}"
        )

    cards = [
        anchor
        for anchor in parser.anchors
        if "site-nav__submenu-card" in anchor.get("classes", set())
    ]
    if len(cards) != 2:
        failures.append(f"region mega-menu card count must be 2, found {len(cards)}")

    region_cards = [anchor for anchor in cards if anchor.get("strong_text") == "地域別"]
    if len(region_cards) != 1:
        failures.append(f"地域別 card count must be 1, found {len(region_cards)}")

    qa_cards = [anchor for anchor in cards if anchor.get("strong_text") == "Q&A"]
    if len(qa_cards) != 1:
        failures.append(f"Q&A card count must be 1, found {len(qa_cards)}")

    nav_match = SITE_NAV_RE.search(html)
    legacy_bare_count = (
        len(LEGACY_REGION_NAV_RE.findall(nav_match.group("body"))) if nav_match else 0
    )
    if legacy_bare_count:
        failures.append(
            f"legacy bare 地域別 link must be absent from site-nav, found {legacy_bare_count}"
        )

    return failures


def headers_have_noindex(headers: Mapping[str, str] | object) -> bool:
    values: Sequence[str]
    get_all = getattr(headers, "get_all", None)
    if callable(get_all):
        values = get_all("X-Robots-Tag") or []
    else:
        value = headers.get("X-Robots-Tag", "") if hasattr(headers, "get") else ""
        values = [value] if value else []
    return any("noindex" in _split_directives(value) for value in values)


def parse_sitemap_urls(xml_text: str) -> list[str]:
    root = ET.fromstring(xml_text)
    urls: list[str] = []
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] == "loc" and element.text:
            url = element.text.strip()
            if url:
                urls.append(url)
    return urls


def _request(url: str, timeout: int = 30) -> tuple[bytes, object]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": GOOGLEBOT_UA,
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(), response.headers


def fetch_with_retries(url: str, retries: int = 3, timeout: int = 30) -> tuple[bytes, object]:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            return _request(url, timeout=timeout)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(attempt * 2)
    assert last_error is not None
    raise last_error


def _same_origin(url: str, base_url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    base = urllib.parse.urlparse(base_url)
    return parsed.scheme == base.scheme and parsed.netloc == base.netloc


def audit_url(url: str) -> str | None:
    try:
        body, headers = fetch_with_retries(url)
    except Exception as exc:  # network failures must fail the deployment audit
        return f"FETCH ERROR {url}: {exc}"

    if headers_have_noindex(headers):
        return f"X-Robots-Tag noindex: {url}"

    html = body.decode("utf-8", errors="replace")
    if html_has_meta_noindex(html):
        return f"meta robots noindex: {url}"
    return None


def audit_urls(urls: Iterable[str], workers: int = 4) -> list[str]:
    failures: list[str] = []
    url_list = list(urls)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(audit_url, url): url for url in url_list}
        for future in as_completed(futures):
            failure = future.result()
            if failure:
                failures.append(failure)
    return sorted(failures)


def audit_live_region_navigation(base_url: str) -> list[str]:
    url = urllib.parse.urljoin(base_url, "region/index.html")
    try:
        body, _ = fetch_with_retries(url)
    except Exception as exc:
        return [f"FETCH ERROR {url}: {exc}"]

    html = body.decode("utf-8", errors="replace")
    return [f"{url}: {failure}" for failure in region_mega_nav_failures(html)]


def load_base_url(config_path: Path) -> str:
    data = json.loads(config_path.read_text(encoding="utf-8"))
    return data["public_base_url"].rstrip("/") + "/"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    base_url = load_base_url(args.config)
    sitemap_url = urllib.parse.urljoin(base_url, "sitemap.xml")
    sitemap_body, sitemap_headers = fetch_with_retries(sitemap_url)
    if headers_have_noindex(sitemap_headers):
        raise SystemExit(f"Sitemap has X-Robots-Tag noindex: {sitemap_url}")

    urls = parse_sitemap_urls(sitemap_body.decode("utf-8", errors="replace"))
    if not urls:
        raise SystemExit("Production sitemap contains no URLs")

    foreign = [url for url in urls if not _same_origin(url, base_url)]
    if foreign:
        sample = ", ".join(foreign[:5])
        raise SystemExit(f"Sitemap contains URL(s) outside the production origin: {sample}")

    failures = audit_urls(urls, workers=max(1, args.workers))
    failures.extend(audit_live_region_navigation(base_url))
    if failures:
        print("Live production audit failed:")
        for failure in sorted(failures):
            print(f"- {failure}")
        return 1

    print(
        f"Live production audit passed: {len(urls)} sitemap URL(s), "
        "no noindex directives found, region mega-menu structure verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
