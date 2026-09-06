# Created: 2026-09-06
"""Finalize search-engine metadata after the public static build.

The preview tree intentionally uses preview-only metadata such as noindex.
This production-only step adds a self-referencing canonical URL to every
published HTML page and validates that exactly one canonical remains.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
SITE_CONFIG = ROOT / "config" / "site.json"

CANONICAL_TAG_RE = re.compile(
    r'<link\b(?=[^>]*\brel=["\'][^"\']*\bcanonical\b[^"\']*["\'])[^>]*>\s*',
    re.IGNORECASE,
)
HREF_RE = re.compile(r'\bhref=["\'](?P<href>[^"\']+)["\']', re.IGNORECASE)


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


def finalize_public() -> None:
    if not PUBLIC.exists():
        raise FileNotFoundError("public directory is missing; run build_public.py first")

    config = json.loads(SITE_CONFIG.read_text(encoding="utf-8"))
    base_url = config["public_base_url"]
    html_files = sorted(PUBLIC.rglob("*.html"))
    if not html_files:
        raise ValueError("No public HTML files found")

    errors: list[str] = []
    for path in html_files:
        relative = path.relative_to(PUBLIC).as_posix()
        expected = canonical_url(base_url, relative)
        html = path.read_text(encoding="utf-8")
        finalized = inject_canonical(html, expected)
        path.write_text(finalized, encoding="utf-8")
        errors.extend(validate_canonical(finalized, expected, relative))

    if errors:
        raise ValueError("Canonical validation failed:\n" + "\n".join(errors))

    print(f"Canonical URLs finalized for {len(html_files)} HTML files.")


if __name__ == "__main__":
    finalize_public()
