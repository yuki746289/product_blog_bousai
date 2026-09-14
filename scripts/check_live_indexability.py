# Created: 2026-09-14 22:40 JST
"""Audit every URL in the production sitemap for accidental noindex directives."""

from __future__ import annotations

import argparse
import json
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
    if failures:
        print("Live indexability audit failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Live indexability audit passed: {len(urls)} sitemap URL(s), no noindex directives found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
