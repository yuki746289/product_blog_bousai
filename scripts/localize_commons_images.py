# Created: 2026-09-03
"""Localize redistributable Wikimedia Commons images for production.

This script runs after scripts/build_public.py. It rewrites Wikimedia Commons
images used in article figures and site listing/card images. Product and
manufacturer images are intentionally excluded.

Behavior:
- discovers unique eligible Commons image URLs before rewriting pages;
- downloads unique images in parallel to keep deployment time bounded;
- follows only Commons -> upload.wikimedia.org redirects;
- converts to WebP, with a 960 px main asset and 720 px responsive variant;
- writes stable hashed assets under public/assets/images/commons/;
- adds intrinsic width/height to reduce layout shift;
- gives eager feature images high fetch priority;
- preserves visible attribution and adds a Commons source-page link when needed;
- leaves the original external URL unchanged if an individual download fails.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import io
import json
import posixpath
import re
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote, unquote, urlencode, urlparse
from urllib.request import Request, urlopen

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
ASSET_DIR = PUBLIC / "assets" / "images" / "commons"
MANIFEST = ASSET_DIR / "manifest.json"

MAIN_MAX_WIDTH = 960
MOBILE_MAX_WIDTH = 720
MAX_DOWNLOAD_WORKERS = 6

ALLOWED_SOURCE_HOSTS = {"commons.wikimedia.org", "upload.wikimedia.org"}
ALLOWED_FINAL_HOSTS = {"commons.wikimedia.org", "upload.wikimedia.org", "thumb.wikimedia.org"}

FIGURE_RE = re.compile(
    r"(?P<open><figure\b(?P<attrs>[^>]*)>)(?P<body>.*?)(?P<close></figure>)",
    re.IGNORECASE | re.DOTALL,
)
IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE | re.DOTALL)
SRC_RE = re.compile(r'\bsrc="(?P<src>[^"]+)"', re.IGNORECASE | re.DOTALL)
FIGCAPTION_RE = re.compile(
    r"(?P<open><figcaption\b[^>]*>)(?P<body>.*?)(?P<close></figcaption>)",
    re.IGNORECASE | re.DOTALL,
)


def is_commons_source(source_url: str) -> bool:
    host = (urlparse(html.unescape(source_url)).hostname or "").lower()
    return host in ALLOWED_SOURCE_HOSTS


def is_eligible_figure(attrs: str, body: str) -> bool:
    class_match = re.search(r'class="([^"]+)"', attrs, re.IGNORECASE)
    classes = set(class_match.group(1).split()) if class_match else set()
    if not ({"article-feature-image", "article-inline-image"} & classes):
        return False
    if "Wikimedia Commons" not in body:
        return False

    img_match = IMG_RE.search(body)
    if not img_match:
        return False
    src_match = SRC_RE.search(img_match.group(0))
    if not src_match:
        return False

    return is_commons_source(src_match.group("src"))


def extract_eligible_source(attrs: str, body: str) -> str | None:
    if not is_eligible_figure(attrs, body):
        return None
    img_match = IMG_RE.search(body)
    assert img_match is not None
    src_match = SRC_RE.search(img_match.group(0))
    assert src_match is not None
    return src_match.group("src")


def commons_filename(source_url: str) -> str | None:
    parsed = urlparse(html.unescape(source_url))
    path = unquote(parsed.path)
    marker = "/wiki/Special:Redirect/file/"
    if marker in path:
        return path.split(marker, 1)[1]
    if parsed.hostname == "upload.wikimedia.org":
        parts = [part for part in path.split("/") if part]
        if len(parts) >= 2:
            return parts[-2] if "/thumb/" in path else parts[-1]
    return None


def commons_description_url(source_url: str) -> str | None:
    filename = commons_filename(source_url)
    if not filename:
        return None
    return "https://commons.wikimedia.org/wiki/File:" + quote(
        filename, safe="()_,-.%"
    )


def stable_asset_name(source_url: str) -> str:
    digest = hashlib.sha256(
        html.unescape(source_url).encode("utf-8")
    ).hexdigest()[:16]
    return f"commons_{digest}.webp"


def resolve_download_url(source_url: str) -> str:
    parsed = urlparse(html.unescape(source_url))
    if parsed.hostname == "upload.wikimedia.org" and "/thumb/" not in parsed.path:
        return html.unescape(source_url)

    filename = commons_filename(source_url)
    if not filename:
        return html.unescape(source_url)

    query = urlencode({
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "imageinfo",
        "redirects": "1",
        "iiprop": "url",
        "iiurlwidth": str(MAIN_MAX_WIDTH),
        "titles": f"File:{filename}",
    })
    request = Request(
        f"https://commons.wikimedia.org/w/api.php?{query}",
        headers={"User-Agent": "bousai-kurashi-guide-image-localizer/1.2 (+https://bousaikun.ashigaru.jp/)"},
    )
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    pages = payload.get("query", {}).get("pages", [])
    if not pages:
        raise ValueError("Commons API returned no pages")
    imageinfo = pages[0].get("imageinfo") or []
    if not imageinfo:
        raise ValueError(f"Commons API image not found: {filename}")
    info = imageinfo[0]
    return info.get("thumburl") or info["url"]


def download_image(source_url: str, retries: int = 3) -> tuple[bytes, str]:
    last_error: Exception | None = None
    resolved_url: str | None = None
    try:
        resolved_url = resolve_download_url(source_url)
    except Exception as exc:
        last_error = exc

    candidates: list[str] = []
    if resolved_url:
        candidates.append(resolved_url)
    original_url = html.unescape(source_url)
    if original_url not in candidates:
        candidates.append(original_url)

    for candidate in candidates:
        for attempt in range(retries):
            try:
                request = Request(
                    candidate,
                    headers={"User-Agent": "bousai-kurashi-guide-image-localizer/1.2 (+https://bousaikun.ashigaru.jp/)"},
                )
                with urlopen(request, timeout=35) as response:
                    final_url = response.geturl()
                    host = (urlparse(final_url).hostname or "").lower()
                    if host not in ALLOWED_FINAL_HOSTS:
                        raise ValueError(f"unexpected redirect host: {host}")
                    return response.read(), final_url
            except Exception as exc:
                last_error = exc
                if attempt + 1 < retries:
                    time.sleep(1.0 * (attempt + 1))
    assert last_error is not None
    raise last_error


def optimize_webp(
    data: bytes,
    destination: Path,
    max_width: int = MAIN_MAX_WIDTH,
) -> tuple[int, int, int]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(io.BytesIO(data)) as original:
        image = ImageOps.exif_transpose(original)
        if image.width > max_width:
            height = round(image.height * max_width / image.width)
            image = image.resize((max_width, height), Image.Resampling.LANCZOS)

        if image.mode not in ("RGB", "RGBA"):
            image = image.convert(
                "RGBA" if "transparency" in image.info else "RGB"
            )

        image.save(destination, format="WEBP", quality=80, method=6)
        return image.width, image.height, destination.stat().st_size


def prepare_entry(source_url: str) -> dict:
    asset_name = stable_asset_name(source_url)
    destination = ASSET_DIR / asset_name

    try:
        raw, final_url = download_image(source_url)
        width, height, optimized_bytes = optimize_webp(raw, destination)

        mobile_path = None
        mobile_width = None
        mobile_height = None
        mobile_bytes = 0
        if width > MOBILE_MAX_WIDTH:
            mobile_name = asset_name.replace(".webp", "_720.webp")
            mobile_destination = ASSET_DIR / mobile_name
            mobile_width, mobile_height, mobile_bytes = optimize_webp(
                raw,
                mobile_destination,
                max_width=MOBILE_MAX_WIDTH,
            )
            mobile_path = f"assets/images/commons/{mobile_name}"

        return {
            "source_url": html.unescape(source_url),
            "final_url": final_url,
            "local_path": f"assets/images/commons/{asset_name}",
            "width": width,
            "height": height,
            "mobile_path": mobile_path,
            "mobile_width": mobile_width,
            "mobile_height": mobile_height,
            "source_bytes": len(raw),
            "optimized_bytes": optimized_bytes,
            "mobile_bytes": mobile_bytes,
            "status": "localized",
        }
    except Exception as exc:
        return {
            "source_url": html.unescape(source_url),
            "status": "failed",
            "error": f"{type(exc).__name__}: {exc}",
        }


def discover_sources() -> list[str]:
    sources: set[str] = set()
    for page in sorted(PUBLIC.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        for match in IMG_RE.finditer(text):
            src_match = SRC_RE.search(match.group(0))
            if not src_match:
                continue
            source = src_match.group("src")
            if is_commons_source(source):
                sources.add(source)
    return sorted(sources)


def prepare_cache(sources: list[str]) -> dict[str, dict]:
    if not sources:
        return {}

    worker_count = min(MAX_DOWNLOAD_WORKERS, len(sources))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        entries = list(executor.map(prepare_entry, sources))
    return dict(zip(sources, entries, strict=True))


def add_image_attributes(
    tag: str,
    width: int,
    height: int,
    feature: bool,
) -> str:
    if not re.search(r"\bwidth=", tag, re.IGNORECASE):
        tag = tag[:-1] + f' width="{width}">'
    if not re.search(r"\bheight=", tag, re.IGNORECASE):
        tag = tag[:-1] + f' height="{height}">'
    if not re.search(r"\bdecoding=", tag, re.IGNORECASE):
        tag = tag[:-1] + ' decoding="async">'
    if (
        feature
        and 'loading="eager"' in tag
        and not re.search(r"\bfetchpriority=", tag, re.IGNORECASE)
    ):
        tag = tag[:-1] + ' fetchpriority="high">'
    return tag


def add_responsive_attributes(
    tag: str,
    mobile_url: str | None,
    mobile_width: int | None,
    full_url: str,
    full_width: int,
) -> str:
    if not mobile_url or not mobile_width or mobile_width >= full_width:
        return tag
    if re.search(r"\bsrcset=", tag, re.IGNORECASE):
        return tag

    return (
        tag[:-1]
        + f' srcset="{mobile_url} {mobile_width}w, '
        + f'{full_url} {full_width}w"'
        + ' sizes="(max-width: 760px) calc(100vw - 32px), 900px">'
    )


def ensure_source_link(body: str, source_url: str) -> str:
    caption_match = FIGCAPTION_RE.search(body)
    if not caption_match:
        return body
    if re.search(
        r'href="https://commons\.wikimedia\.org/',
        caption_match.group(0),
        re.IGNORECASE,
    ):
        return body

    description_url = commons_description_url(source_url)
    if not description_url:
        return body

    appendix = (
        ' <a href="'
        + description_url
        + '" target="_blank" '
        + 'rel="noopener noreferrer">Wikimedia Commonsの元画像</a>'
    )
    replacement = (
        caption_match.group("open")
        + caption_match.group("body").rstrip()
        + appendix
        + caption_match.group("close")
    )
    return (
        body[: caption_match.start()]
        + replacement
        + body[caption_match.end() :]
    )


def localize_html_file(
    path: Path,
    cache: dict[str, dict],
) -> tuple[int, int]:
    original_html = path.read_text(encoding="utf-8")
    localized_count = 0
    failed_count = 0

    def replace_figure(match: re.Match[str]) -> str:
        nonlocal localized_count, failed_count
        attrs = match.group("attrs")
        body = match.group("body")
        source_url = extract_eligible_source(attrs, body)
        if not source_url:
            return match.group(0)

        img_match = IMG_RE.search(body)
        assert img_match is not None
        tag = img_match.group(0)

        entry = cache.get(source_url)
        if entry is None:
            entry = prepare_entry(source_url)
            cache[source_url] = entry

        if entry["status"] != "localized":
            return match.group(0)

        page_rel = path.relative_to(PUBLIC).as_posix()
        page_dir = posixpath.dirname(page_rel) or "."
        local_url = posixpath.relpath(entry["local_path"], page_dir)

        new_tag = SRC_RE.sub(
            lambda _m: f'src="{local_url}"',
            tag,
            count=1,
        )

        feature = "article-feature-image" in attrs
        new_tag = add_image_attributes(
            new_tag,
            entry["width"],
            entry["height"],
            feature,
        )

        mobile_url = None
        if entry.get("mobile_path"):
            mobile_url = posixpath.relpath(entry["mobile_path"], page_dir)
        new_tag = add_responsive_attributes(
            new_tag,
            mobile_url,
            entry.get("mobile_width"),
            local_url,
            entry["width"],
        )

        new_body = (
            body[: img_match.start()]
            + new_tag
            + body[img_match.end() :]
        )
        new_body = ensure_source_link(new_body, source_url)

        localized_count += 1
        return match.group("open") + new_body + match.group("close")

    rewritten = FIGURE_RE.sub(replace_figure, original_html)

    def replace_remaining_img(match: re.Match[str]) -> str:
        nonlocal localized_count, failed_count
        tag = match.group(0)
        src_match = SRC_RE.search(tag)
        if not src_match:
            return tag

        source_url = src_match.group("src")
        if not is_commons_source(source_url):
            return tag

        entry = cache.get(source_url)
        if entry is None:
            entry = prepare_entry(source_url)
            cache[source_url] = entry

        if entry["status"] != "localized":
            failed_count += 1
            return tag

        page_rel = path.relative_to(PUBLIC).as_posix()
        page_dir = posixpath.dirname(page_rel) or "."
        local_url = posixpath.relpath(entry["local_path"], page_dir)

        new_tag = SRC_RE.sub(
            lambda _m: f'src="{local_url}"',
            tag,
            count=1,
        )
        new_tag = add_image_attributes(
            new_tag,
            entry["width"],
            entry["height"],
            feature=False,
        )

        mobile_url = None
        if entry.get("mobile_path"):
            mobile_url = posixpath.relpath(entry["mobile_path"], page_dir)
        new_tag = add_responsive_attributes(
            new_tag,
            mobile_url,
            entry.get("mobile_width"),
            local_url,
            entry["width"],
        )

        if not re.search(r"\bdata-commons-source=", new_tag, re.IGNORECASE):
            source_page = commons_description_url(source_url)
            if source_page:
                new_tag = new_tag[:-1] + (
                    ' data-commons-source="' + html.escape(source_page, quote=True) + '">'
                )

        localized_count += 1
        return new_tag

    rewritten = IMG_RE.sub(replace_remaining_img, rewritten)

    if rewritten != original_html:
        path.write_text(rewritten, encoding="utf-8")

    return localized_count, failed_count


def run(min_localized: int = 0) -> dict:
    if not PUBLIC.exists():
        raise FileNotFoundError(
            "public directory does not exist; run build_public.py first"
        )

    ASSET_DIR.mkdir(parents=True, exist_ok=True)

    sources = discover_sources()
    cache = prepare_cache(sources)

    page_results: list[dict] = []
    total_localized = 0
    total_failed = 0

    for page in sorted(PUBLIC.rglob("*.html")):
        localized, failed = localize_html_file(page, cache)
        if localized or failed:
            page_results.append(
                {
                    "page": page.relative_to(PUBLIC).as_posix(),
                    "localized": localized,
                    "failed": failed,
                }
            )
        total_localized += localized
        total_failed += failed

    assets = sorted(
        cache.values(),
        key=lambda item: item["source_url"],
    )
    unique_localized = sum(
        1 for item in assets if item["status"] == "localized"
    )
    unique_failed = sum(
        1 for item in assets if item["status"] == "failed"
    )
    source_bytes = sum(
        item.get("source_bytes", 0) for item in assets
    )
    optimized_bytes = sum(
        item.get("optimized_bytes", 0) for item in assets
    )
    responsive_variant_bytes = sum(
        item.get("mobile_bytes", 0) for item in assets
    )
    failure_reasons = Counter(
        item.get("error", "unknown").split(":", 1)[0]
        for item in assets
        if item["status"] == "failed"
    )

    manifest = {
        "generated_by": "scripts/localize_commons_images.py",
        "download_workers": min(MAX_DOWNLOAD_WORKERS, len(sources))
        if sources
        else 0,
        "pages_with_eligible_images": len(page_results),
        "image_occurrences_localized": total_localized,
        "image_occurrences_failed": total_failed,
        "unique_images_localized": unique_localized,
        "unique_images_failed": unique_failed,
        "failure_reasons": dict(failure_reasons),
        "failure_samples": [
            {
                "source_url": item.get("source_url"),
                "error": item.get("error"),
            }
            for item in assets
            if item["status"] == "failed"
        ][:10],
        "source_bytes": source_bytes,
        "optimized_bytes": optimized_bytes,
        "responsive_variant_bytes": responsive_variant_bytes,
        "saved_bytes": max(0, source_bytes - optimized_bytes),
        "pages": page_results,
        "assets": assets,
    }
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = {
        key: value
        for key, value in manifest.items()
        if key not in {"pages", "assets"}
    }
    print(json.dumps(summary, ensure_ascii=False))

    if total_localized < min_localized:
        raise SystemExit(
            f"localized image occurrences {total_localized} "
            f"< required minimum {min_localized}"
        )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-localized", type=int, default=0)
    args = parser.parse_args()
    run(min_localized=args.min_localized)


if __name__ == "__main__":
    main()
