# Created: 2026-09-09 06:17 JST
"""Synchronize reviewed Markdown article content into preview HTML shells.

The public builder consumes preview/*.html, while editorial review is performed
against content/articles/*.md. This script keeps the reviewed Markdown as the
text source of truth without discarding the existing preview shell, feature
image, or inline editorial images.

Only the explicitly reviewed final-quality batch is synchronized here. B060 is
a product page with bespoke product-card HTML, so it uses targeted text
replacements instead of generic body rendering.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from bousai_blog.registry import load_registry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "content_registry.json"

# Articles whose reviewed Markdown changed materially in the final-quality pass,
# plus articles whose source links were newer than their preview HTML.
SYNC_ARTICLE_IDS = {
    "B001", "B002", "B004", "B005", "B006", "B007", "B009", "B011",
    "B012", "B014", "B015", "B016", "B017", "B018", "B020", "B023",
    "B024", "B025", "B026", "B027", "B028", "B031", "B032", "B034",
    "B043", "B045", "B046", "B047",
}

# Product page B060 is intentionally not body-rendered because its preview
# contains verified manufacturer images and bespoke Amazon product cards.
TARGETED_PREVIEW_REPLACEMENTS = {
    "B060": (
        ("商品情報は定期見直し", "商品情報は棚卸し日・使用後・買い替え時に見直し"),
        (
            "商品の劣化・販売継続を定期的に見直す",
            "防災用品の棚卸し日をカレンダーに登録し、使用後・買い替え時にも保管状態、劣化、販売継続を確認する",
        ),
    ),
}

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
    "region/index.html": "category_region.html",
    "goods/water-food.html": "goods_water_food.html",
    "goods/toilet-hygiene.html": "goods_toilet_hygiene.html",
    "goods/light-information.html": "goods_light_information.html",
    "goods/power-charging.html": "goods_power_charging.html",
}

FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
ARTICLE_BODY_RE = re.compile(
    r'(?P<open><div\s+class=["\']article-body["\'][^>]*>)(?P<body>.*?)(?P<close></div>\s*</article>)',
    re.DOTALL | re.IGNORECASE,
)
LEAD_RE = re.compile(
    r'(?P<open><p\s+class=["\']article-lead["\'][^>]*>).*?(?P<close></p>)',
    re.DOTALL | re.IGNORECASE,
)
INLINE_FIGURE_RE = re.compile(
    r'<figure\b[^>]*class=["\'][^"\']*article-inline-image[^"\']*["\'][^>]*>.*?</figure>',
    re.DOTALL | re.IGNORECASE,
)
HEADING_HTML_RE = re.compile(r"<h(?P<level>[23])[^>]*>(?P<text>.*?)</h(?P=level)>", re.DOTALL | re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
H3_RE = re.compile(r"^###\s+(.+?)\s*$")
UL_RE = re.compile(r"^\s*[-+*]\s+(.+)$")
OL_RE = re.compile(r"^\s*\d+[.)]\s+(.+)$")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*$")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def preview_aliases(registry: dict) -> dict[str, str]:
    aliases = dict(STATIC_PRODUCTION_TO_PREVIEW)
    for article in registry["articles"]:
        planned = article.get("planned_public_path")
        preview = article.get("preview_path")
        if planned and preview:
            aliases[planned.lstrip("/")] = Path(preview).name
    return aliases


def rewrite_preview_target(raw: str, aliases: dict[str, str]) -> str:
    target = raw.strip().strip("<>")
    parts = urlsplit(target)
    if parts.scheme or parts.netloc or target.startswith(("#", "mailto:", "tel:")):
        return target
    path = parts.path.replace("\\", "/").lstrip("./")
    replacement = aliases.get(path)
    if replacement:
        return urlunsplit(("", "", replacement, parts.query, parts.fragment))
    return target


def inline_markup(text: str, aliases: dict[str, str]) -> str:
    escaped = html.escape(text, quote=False)

    # Protect Markdown links before applying other inline replacements.
    link_placeholders: list[str] = []

    def link_repl(match: re.Match[str]) -> str:
        label = match.group(1)
        raw_target = html.unescape(match.group(2))
        target = rewrite_preview_target(raw_target, aliases)
        safe_label = html.escape(html.unescape(label), quote=False)
        safe_target = html.escape(target, quote=True)
        attrs = ""
        parts = urlsplit(target)
        if parts.scheme in {"http", "https"}:
            attrs = ' target="_blank" rel="noopener noreferrer"'
        token = f"@@LINK{len(link_placeholders)}@@"
        link_placeholders.append(f'<a href="{safe_target}"{attrs}>{safe_label}</a>')
        return token

    escaped = MARKDOWN_LINK_RE.sub(link_repl, escaped)
    escaped = INLINE_CODE_RE.sub(r"<code>\1</code>", escaped)
    escaped = BOLD_RE.sub(r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)

    for index, value in enumerate(link_placeholders):
        escaped = escaped.replace(f"@@LINK{index}@@", value)
    return escaped


def split_cells(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def is_table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    return "|" in lines[index] and bool(TABLE_SEPARATOR_RE.match(lines[index + 1]))


def is_block_start(lines: list[str], index: int) -> bool:
    line = lines[index]
    stripped = line.strip()
    if not stripped:
        return True
    if H2_RE.match(line) or H3_RE.match(line) or UL_RE.match(line) or OL_RE.match(line):
        return True
    if stripped.startswith(">"):
        return True
    if is_table_start(lines, index):
        return True
    return False


def normalize_heading_text(value: str) -> str:
    value = html.unescape(TAG_RE.sub("", value))
    value = re.sub(r"\s+", "", value)
    return value.strip()


def render_markdown_blocks(lines: list[str], aliases: dict[str, str]) -> str:
    out: list[str] = []
    i = 0
    key_points_open = False

    def close_key_points() -> None:
        nonlocal key_points_open
        if key_points_open:
            out.append("</section>")
            key_points_open = False

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if not stripped:
            i += 1
            continue

        h2 = H2_RE.match(raw)
        if h2:
            close_key_points()
            title = inline_markup(h2.group(1), aliases)
            if normalize_heading_text(title).startswith("結論"):
                out.append(f'<section class="key-points"><h2>{title}</h2>')
                key_points_open = True
            else:
                out.append(f"<h2>{title}</h2>")
            i += 1
            continue

        h3 = H3_RE.match(raw)
        if h3:
            out.append(f"<h3>{inline_markup(h3.group(1), aliases)}</h3>")
            i += 1
            continue

        if is_table_start(lines, i):
            headers = split_cells(lines[i])
            i += 2
            rows: list[list[str]] = []
            while i < len(lines):
                candidate = lines[i]
                if not candidate.strip() or "|" not in candidate:
                    break
                if H2_RE.match(candidate) or H3_RE.match(candidate):
                    break
                rows.append(split_cells(candidate))
                i += 1
            out.append('<div class="table-wrap"><table><thead><tr>')
            out.extend(f"<th>{inline_markup(cell, aliases)}</th>" for cell in headers)
            out.append("</tr></thead><tbody>")
            for row in rows:
                out.append("<tr>")
                out.extend(f"<td>{inline_markup(cell, aliases)}</td>" for cell in row)
                out.append("</tr>")
            out.append("</tbody></table></div>")
            continue

        ul = UL_RE.match(raw)
        if ul:
            items: list[str] = []
            while i < len(lines):
                match = UL_RE.match(lines[i])
                if not match:
                    break
                item = match.group(1).strip()
                item = re.sub(r"^\[ \]\s*", "☐ ", item)
                item = re.sub(r"^\[[xX]\]\s*", "☑ ", item)
                items.append(item)
                i += 1
            out.append('<ul class="checklist">')
            out.extend(f"<li>{inline_markup(item, aliases)}</li>" for item in items)
            out.append("</ul>")
            continue

        ol = OL_RE.match(raw)
        if ol:
            items = []
            while i < len(lines):
                match = OL_RE.match(lines[i])
                if not match:
                    break
                items.append(match.group(1).strip())
                i += 1
            out.append("<ol>")
            out.extend(f"<li>{inline_markup(item, aliases)}</li>" for item in items)
            out.append("</ol>")
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]).strip())
                i += 1
            quote_text = " ".join(part for part in quote_lines if part)
            out.append(f"<blockquote><p>{inline_markup(quote_text, aliases)}</p></blockquote>")
            continue

        paragraph: list[str] = [stripped]
        i += 1
        while i < len(lines) and not is_block_start(lines, i):
            paragraph.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline_markup(' '.join(paragraph), aliases)}</p>")

    close_key_points()
    return "\n".join(out)


def parse_source(markdown: str) -> tuple[str, list[str]]:
    text = FRONTMATTER_RE.sub("", markdown, count=1)
    text = COMMENT_RE.sub("", text)
    lines = text.splitlines()

    h1_index = next((i for i, line in enumerate(lines) if re.match(r"^#\s+", line)), -1)
    start = h1_index + 1 if h1_index >= 0 else 0
    h2_index = next((i for i in range(start, len(lines)) if H2_RE.match(lines[i])), len(lines))

    intro_parts: list[str] = []
    current: list[str] = []
    for line in lines[start:h2_index]:
        if not line.strip():
            if current:
                intro_parts.append(" ".join(current))
                current = []
            continue
        current.append(line.strip())
    if current:
        intro_parts.append(" ".join(current))

    intro = " ".join(intro_parts)
    return intro, lines[h2_index:]


def extract_figures(old_body: str) -> list[tuple[int, str, str]]:
    figures: list[tuple[int, str, str]] = []
    for match in INLINE_FIGURE_RE.finditer(old_body):
        before = old_body[: match.start()]
        headings = list(HEADING_HTML_RE.finditer(before))
        if headings:
            heading = headings[-1]
            level = int(heading.group("level"))
            anchor = normalize_heading_text(heading.group("text"))
        else:
            level = 2
            anchor = ""
        figures.append((level, anchor, match.group(0)))
    return figures


def insert_one_figure(body: str, level: int, anchor: str, figure: str) -> tuple[str, bool]:
    pattern = re.compile(rf"<h{level}[^>]*>(.*?)</h{level}>", re.DOTALL | re.IGNORECASE)
    for match in pattern.finditer(body):
        if normalize_heading_text(match.group(1)) == anchor:
            pos = match.end()
            return body[:pos] + "\n" + figure + body[pos:], True
    return body, False


def insert_preserved_figures(new_body: str, figures: list[tuple[int, str, str]]) -> str:
    unmatched: list[str] = []
    for level, anchor, figure in figures:
        new_body, inserted = insert_one_figure(new_body, level, anchor, figure)
        if not inserted:
            unmatched.append(figure)

    if unmatched:
        related = re.search(r"<h2[^>]*>関連記事</h2>", new_body, re.IGNORECASE)
        pos = related.start() if related else len(new_body)
        block = "\n".join(unmatched) + "\n"
        new_body = new_body[:pos] + block + new_body[pos:]
    return new_body


def sync_generic(article: dict, aliases: dict[str, str]) -> bool:
    source_path = ROOT / article["source_path"]
    preview_path = ROOT / article["preview_path"]
    markdown = source_path.read_text(encoding="utf-8")
    preview = preview_path.read_text(encoding="utf-8")

    body_match = ARTICLE_BODY_RE.search(preview)
    if not body_match:
        raise ValueError(f"article-body not found: {preview_path}")

    intro, content_lines = parse_source(markdown)
    rendered = render_markdown_blocks(content_lines, aliases)
    figures = extract_figures(body_match.group("body"))
    rendered = insert_preserved_figures(rendered, figures)

    updated = (
        preview[: body_match.start()]
        + body_match.group("open")
        + "\n"
        + rendered
        + "\n"
        + body_match.group("close")
        + preview[body_match.end() :]
    )

    lead_match = LEAD_RE.search(updated)
    if lead_match and intro:
        updated = (
            updated[: lead_match.start()]
            + lead_match.group("open")
            + inline_markup(intro, aliases)
            + lead_match.group("close")
            + updated[lead_match.end() :]
        )

    if updated == preview:
        return False
    preview_path.write_text(updated, encoding="utf-8")
    return True


def sync_targeted(article: dict) -> bool:
    preview_path = ROOT / article["preview_path"]
    preview = preview_path.read_text(encoding="utf-8")
    updated = preview
    for old, new in TARGETED_PREVIEW_REPLACEMENTS.get(article["article_id"], ()):
        if old not in updated:
            raise ValueError(f"targeted preview text not found for {article['article_id']}: {old}")
        updated = updated.replace(old, new)
    if updated == preview:
        return False
    preview_path.write_text(updated, encoding="utf-8")
    return True


def sync() -> list[str]:
    registry = load_registry(REGISTRY)
    aliases = preview_aliases(registry)
    by_id = {article["article_id"]: article for article in registry["articles"]}
    changed: list[str] = []

    for article_id in sorted(SYNC_ARTICLE_IDS):
        article = by_id[article_id]
        if sync_generic(article, aliases):
            changed.append(article_id)

    for article_id in sorted(TARGETED_PREVIEW_REPLACEMENTS):
        article = by_id[article_id]
        if sync_targeted(article):
            changed.append(article_id)

    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if synchronization would change tracked preview files.",
    )
    args = parser.parse_args()

    before: dict[Path, str] = {}
    if args.check:
        registry = load_registry(REGISTRY)
        by_id = {article["article_id"]: article for article in registry["articles"]}
        for article_id in sorted(SYNC_ARTICLE_IDS | set(TARGETED_PREVIEW_REPLACEMENTS)):
            path = ROOT / by_id[article_id]["preview_path"]
            before[path] = path.read_text(encoding="utf-8")

    changed = sync()
    print("Synchronized preview articles: " + (", ".join(changed) if changed else "none"))

    if args.check and changed:
        for path, original in before.items():
            path.write_text(original, encoding="utf-8")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
