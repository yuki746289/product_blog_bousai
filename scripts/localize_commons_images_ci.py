# Created: 2026-09-06T17:23+09:00
"""CI-safe Wikimedia Commons localization wrapper.

The production image localizer intentionally leaves an external URL in place
when an individual download fails. That fallback is useful for local previews,
but production deployment must not publish a partially localized build.

This wrapper:
- reduces Commons download concurrency from 6 to 2;
- tries the existing source URL first to avoid an unnecessary Commons API call;
- retries HTTP 429/5xx and network errors with Retry-After-aware backoff;
- fails before FTPS deployment when any Commons image could not be localized;
- verifies that no external Wikimedia image src remains in generated HTML.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from scripts import localize_commons_images as localizer

MAX_DOWNLOAD_WORKERS = 2
HTTP_RETRIES = 5
RETRY_BASE_SECONDS = 2.0
MAX_RETRY_DELAY_SECONDS = 45.0
USER_AGENT = "bousai-kurashi-guide-image-localizer/1.3 (+https://bousaikun.ashigaru.jp/)"
EXTERNAL_WIKIMEDIA_SRC_RE = re.compile(
    r'src="https://(?:commons|upload)\.wikimedia\.org/',
    re.IGNORECASE,
)


def retry_after_seconds(error: HTTPError, now: datetime | None = None) -> float | None:
    value = error.headers.get("Retry-After") if error.headers else None
    if not value:
        return None

    try:
        return max(0.0, float(value))
    except ValueError:
        pass

    try:
        retry_at = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        return None

    if retry_at.tzinfo is None:
        retry_at = retry_at.replace(tzinfo=timezone.utc)
    current = now or datetime.now(timezone.utc)
    return max(0.0, (retry_at - current).total_seconds())


def retry_delay_seconds(attempt: int, error: Exception | None = None) -> float:
    if isinstance(error, HTTPError):
        retry_after = retry_after_seconds(error)
        if retry_after is not None:
            return min(max(1.0, retry_after), MAX_RETRY_DELAY_SECONDS)
    return min(RETRY_BASE_SECONDS * (2 ** attempt), MAX_RETRY_DELAY_SECONDS)


def read_url(
    request: Request,
    timeout: int,
    retries: int = HTTP_RETRIES,
) -> tuple[bytes, str]:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urlopen(request, timeout=timeout) as response:
                return response.read(), response.geturl()
        except HTTPError as exc:
            last_error = exc
            transient = exc.code == 429 or 500 <= exc.code <= 599
            if not transient or attempt + 1 >= retries:
                raise
        except URLError as exc:
            last_error = exc
            if attempt + 1 >= retries:
                raise

        time.sleep(retry_delay_seconds(attempt, last_error))

    assert last_error is not None
    raise last_error


def request_bytes(url: str, timeout: int = 35) -> tuple[bytes, str]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    return read_url(request, timeout=timeout)


def resolve_download_url(source_url: str) -> str:
    parsed = urlparse(html.unescape(source_url))
    if parsed.hostname == "upload.wikimedia.org" and "/thumb/" not in parsed.path:
        return html.unescape(source_url)

    filename = localizer.commons_filename(source_url)
    if not filename:
        return html.unescape(source_url)

    query = urlencode({
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "imageinfo",
        "redirects": "1",
        "iiprop": "url",
        "iiurlwidth": str(localizer.MAIN_MAX_WIDTH),
        "titles": f"File:{filename}",
    })
    data, _ = request_bytes(
        f"https://commons.wikimedia.org/w/api.php?{query}",
        timeout=30,
    )
    payload = json.loads(data.decode("utf-8"))
    pages = payload.get("query", {}).get("pages", [])
    if not pages:
        raise ValueError("Commons API returned no pages")
    imageinfo = pages[0].get("imageinfo") or []
    if not imageinfo:
        raise ValueError(f"Commons API image not found: {filename}")
    info = imageinfo[0]
    return info.get("thumburl") or info["url"]


def validate_final_host(final_url: str) -> None:
    host = (urlparse(final_url).hostname or "").lower()
    if host not in localizer.ALLOWED_FINAL_HOSTS:
        raise ValueError(f"unexpected redirect host: {host}")


def download_image(source_url: str) -> tuple[bytes, str]:
    """Download the existing source URL first, then use API resolution as fallback."""
    original_url = html.unescape(source_url)
    last_error: Exception | None = None

    try:
        raw, final_url = request_bytes(original_url)
        validate_final_host(final_url)
        return raw, final_url
    except Exception as exc:
        last_error = exc

    try:
        resolved_url = resolve_download_url(source_url)
    except Exception as exc:
        last_error = exc
        resolved_url = None

    if resolved_url and resolved_url != original_url:
        try:
            raw, final_url = request_bytes(resolved_url)
            validate_final_host(final_url)
            return raw, final_url
        except Exception as exc:
            last_error = exc

    assert last_error is not None
    raise last_error


def external_wikimedia_pages(public_dir: Path) -> list[str]:
    offenders: list[str] = []
    for page in sorted(public_dir.rglob("*.html")):
        if EXTERNAL_WIKIMEDIA_SRC_RE.search(page.read_text(encoding="utf-8")):
            offenders.append(page.relative_to(public_dir).as_posix())
    return offenders


def validate_production_build(manifest: dict, public_dir: Path) -> None:
    failed = int(manifest.get("unique_images_failed", 0))
    if failed:
        samples = manifest.get("failure_samples", [])[:3]
        details = "; ".join(
            f"{item.get('source_url')}: {item.get('error')}" for item in samples
        )
        suffix = f" ({details})" if details else ""
        raise SystemExit(
            f"Commons localization incomplete: {failed} unique image(s) failed{suffix}"
        )

    offenders = external_wikimedia_pages(public_dir)
    if offenders:
        raise SystemExit(
            "External Wikimedia image src remains before deployment: "
            + ", ".join(offenders[:10])
        )


def run(min_localized: int = 1) -> dict:
    localizer.MAX_DOWNLOAD_WORKERS = MAX_DOWNLOAD_WORKERS
    localizer.download_image = download_image
    manifest = localizer.run(min_localized=min_localized)
    validate_production_build(manifest, localizer.PUBLIC)
    print("Commons production localization check passed.")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-localized", type=int, default=1)
    args = parser.parse_args()
    run(min_localized=args.min_localized)


if __name__ == "__main__":
    main()
