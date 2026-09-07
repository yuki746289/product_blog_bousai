from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE_DIR = ROOT / "content" / "articles"

SOURCE_SECTION_RE = re.compile(
    r"^##\s+(?:公的情報(?:・参考資料)?|参考資料|出典|Sources?)\s*$",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^##\s+")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^\)]+\)")
RAW_URL_RE = re.compile(r"https?://\S+")
HTML_TAG_RE = re.compile(r"<[^>]+>")
CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`([^`]*)`")


@dataclass
class Metric:
    article_id: str
    title: str
    content_role: str
    risk_level: str
    body_char_count: int
    minimum_char_count: int | None
    length_status: str
    source_path: str


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    meta: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"\'')
    return meta, text[match.end():]


def remove_source_sections(body: str) -> str:
    kept: list[str] = []
    skipping = False
    for line in body.splitlines():
        if SOURCE_SECTION_RE.match(line.strip()):
            skipping = True
            continue
        if skipping and HEADING_RE.match(line.strip()):
            skipping = False
        if not skipping:
            kept.append(line)
    return "\n".join(kept)


def reader_visible_text(body: str) -> str:
    text = remove_source_sections(body)
    text = CODE_FENCE_RE.sub(" ", text)
    text = MARKDOWN_LINK_RE.sub(r"\1", text)
    text = RAW_URL_RE.sub(" ", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = INLINE_CODE_RE.sub(r"\1", text)

    # Markdown syntax is not reader-visible text. Keep table/list cell wording.
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", text)
    text = re.sub(r"(?m)^\s*>\s?", "", text)
    text = re.sub(r"(?m)^\s*[-+*]\s+", "", text)
    text = re.sub(r"(?m)^\s*\d+[.)]\s+", "", text)
    text = text.replace("|", " ")
    text = re.sub(r"(?m)^\s*:?-{3,}:?(?:\s+:?-{3,}:?)*\s*$", "", text)
    text = re.sub(r"[*_~]", "", text)
    text = re.sub(r"\\([#*_[\]()>`~|])", r"\1", text)
    return text


def count_reader_chars(body: str) -> int:
    text = reader_visible_text(body)
    # Count reader-visible characters, excluding whitespace. Japanese prose is
    # not distorted by word-tokenization and the result is reproducible.
    return sum(1 for char in text if not char.isspace())


def minimum_for(role: str, risk: str) -> int | None:
    role = role.lower()
    risk = risk.lower()
    if role == "pillar":
        return 3000
    if role in {"detail", "practical"}:
        if risk == "high":
            return 3000
        return 2500
    return None


def audit() -> list[Metric]:
    rows: list[Metric] = []
    for path in sorted(ARTICLE_DIR.glob("B*.md")):
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        article_id = meta.get("article_id", path.name.split("_", 1)[0])
        role = meta.get("content_role", "")
        risk = meta.get("risk_level", "")
        count = count_reader_chars(body)
        minimum = minimum_for(role, risk)
        if minimum is None:
            status = "PASS_NO_NUMERIC_RULE"
        elif count >= minimum:
            status = "PASS"
        else:
            status = "FAIL_LENGTH"
        rows.append(
            Metric(
                article_id=article_id,
                title=meta.get("title", ""),
                content_role=role,
                risk_level=risk,
                body_char_count=count,
                minimum_char_count=minimum,
                length_status=status,
                source_path=path.relative_to(ROOT).as_posix(),
            )
        )
    return rows


def markdown(rows: list[Metric]) -> str:
    lines = [
        "| ID | role | risk | chars | min | status | title |",
        "|---|---|---|---:|---:|---|---|",
    ]
    for row in rows:
        minimum = "-" if row.minimum_char_count is None else str(row.minimum_char_count)
        title = row.title.replace("|", "｜")
        lines.append(
            f"| {row.article_id} | {row.content_role} | {row.risk_level} | "
            f"{row.body_char_count} | {minimum} | {row.length_status} | {title} |"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--fail-under-minimum", action="store_true")
    args = parser.parse_args()

    rows = audit()
    if args.format == "json":
        print(json.dumps([asdict(row) for row in rows], ensure_ascii=False, indent=2))
    else:
        print(markdown(rows))

    failures = [row for row in rows if row.length_status == "FAIL_LENGTH"]
    if args.fail_under_minimum and failures:
        print("\nFAIL_LENGTH: " + ", ".join(row.article_id for row in failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
