# Created: 2026-09-08 14:27 JST
"""Triage existing articles for explanation-completeness review.

This tool does not decide whether prose is good or bad. It surfaces sections
that deserve a human editorial review under docs/EXPLANATION_QUALITY_PREFLIGHT.md.
Character-count thresholds are warnings, never padding targets.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = ROOT / "content" / "articles"

SKIP_HEADINGS = (
    "公的情報",
    "参考情報",
    "参考資料",
    "出典",
    "関連記事",
    "関連する商品紹介",
    "関連商品",
)

SAFETY_WORDS = re.compile(
    r"避難|浸水|冠水|水没|停電|断水|火災|土砂|熱中症|津波|高潮|地震|噴火|降灰|台風|洪水"
)
ACTION_WORDS = re.compile(
    r"掃除|固定|離す|離し|移す|移し|移動|避難|備蓄|備える|確認|片付|処分|保管|閉め|止め"
)
CAUSAL_WORDS = re.compile(
    r"ため|ので|から|理由|原因|防ぐ|防ぎ|減ら|つなが|恐れ|危険|おそれ|結果|影響|すると|なれば|なると"
)
VAGUE_PHRASES = (
    "安全に",
    "適切に",
    "必要に応じて",
    "状況に応じて",
    "十分に",
    "建物条件",
    "自治体情報",
)
PRODUCT_TERMS = (
    "養生テープ",
    "飛散防止フィルム",
    "携帯トイレ",
    "防じんマスク",
    "ゴーグル",
    "懐中電灯",
    "モバイルバッテリー",
    "ポータブル電源",
)


@dataclass(frozen=True)
class SectionFinding:
    article_id: str
    article_title: str
    heading: str
    chars: int
    paragraphs: int
    flags: tuple[str, ...]


@dataclass(frozen=True)
class ArticleAudit:
    article_id: str
    title: str
    path: Path
    findings: tuple[SectionFinding, ...]
    product_terms_without_goods_route: tuple[str, ...]


def _frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    return match.group(1).strip() if match else ""


def _strip_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    match = re.match(r"\A---\s*\n.*?\n---\s*\n", text, flags=re.DOTALL)
    return text[match.end() :] if match else text


def _visible_text(markdown: str) -> str:
    text = re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"(?m)^\s*[-*+]\s+", "", text)
    text = re.sub(r"(?m)^\s*\d+[.)]\s+", "", text)
    text = re.sub(r"[#>*_|~]", "", text)
    return re.sub(r"\s+", "", text)


def _iter_h2_sections(text: str) -> Iterable[tuple[str, str]]:
    body = _strip_frontmatter(text)
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", body))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        yield match.group(1).strip(), body[start:end]


def _paragraph_count(section: str) -> int:
    chunks = re.split(r"\n\s*\n", section.strip())
    return sum(
        1
        for chunk in chunks
        if chunk.strip()
        and not chunk.lstrip().startswith(("|", "- [", "* [", ">"))
        and not re.match(r"^\s*[-*+]\s+", chunk)
    )


def audit_article(path: Path) -> ArticleAudit:
    text = path.read_text(encoding="utf-8")
    article_id = _frontmatter_value(text, "article_id") or path.name.split("_", 1)[0]
    title = _frontmatter_value(text, "title") or path.stem
    findings: list[SectionFinding] = []

    for heading, section in _iter_h2_sections(text):
        if any(heading.startswith(skip) for skip in SKIP_HEADINGS):
            continue
        visible = _visible_text(section)
        chars = len(visible)
        paragraphs = _paragraph_count(section)
        flags: list[str] = []

        if chars < 250:
            flags.append("SHORT_H2_LT250")
        elif chars < 400:
            flags.append("H2_UNDER400_REVIEW")

        if SAFETY_WORDS.search(heading) and chars < 400:
            flags.append("SAFETY_H2_UNDER400")

        if paragraphs <= 2 and chars < 400:
            flags.append("ONE_OR_TWO_PARAGRAPH_H2")

        if ACTION_WORDS.search(section) and not CAUSAL_WORDS.search(section) and chars < 500:
            flags.append("ACTION_WITHOUT_CAUSAL_MARKER")

        vague_hits = [phrase for phrase in VAGUE_PHRASES if phrase in section]
        if vague_hits and chars < 500:
            flags.append("VAGUE_PHRASE:" + ",".join(vague_hits))

        if flags:
            findings.append(
                SectionFinding(
                    article_id=article_id,
                    article_title=title,
                    heading=heading,
                    chars=chars,
                    paragraphs=paragraphs,
                    flags=tuple(flags),
                )
            )

    has_goods_route = bool(re.search(r"(?:goods_|/goods/|goods/)[^\s)\"']+", text))
    product_terms = tuple(
        term for term in PRODUCT_TERMS if term in text and not has_goods_route
    )

    return ArticleAudit(
        article_id=article_id,
        title=title,
        path=path,
        findings=tuple(findings),
        product_terms_without_goods_route=product_terms,
    )


def audit_all() -> list[ArticleAudit]:
    return [audit_article(path) for path in sorted(ARTICLES_DIR.glob("B*.md"))]


def repeated_h2_headings(audits: list[ArticleAudit]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for audit in audits:
        text = audit.path.read_text(encoding="utf-8")
        seen = set()
        for heading, _ in _iter_h2_sections(text):
            if any(heading.startswith(skip) for skip in SKIP_HEADINGS):
                continue
            normalized = re.sub(r"\s+", " ", re.sub(r"^[0-9０-９]+[.．]\s*", "", heading)).strip()
            if normalized:
                seen.add(normalized)
        counts.update(seen)
    return {heading: count for heading, count in counts.items() if count >= 4}


def priority_score(audit: ArticleAudit) -> int:
    score = 0
    for finding in audit.findings:
        flags = set(finding.flags)
        if "SHORT_H2_LT250" in flags:
            score += 4
        if "SAFETY_H2_UNDER400" in flags:
            score += 3
        if "ACTION_WITHOUT_CAUSAL_MARKER" in flags:
            score += 2
        if any(flag.startswith("VAGUE_PHRASE:") for flag in flags):
            score += 2
        if "ONE_OR_TWO_PARAGRAPH_H2" in flags:
            score += 1
    score += 2 * len(audit.product_terms_without_goods_route)
    return score


def markdown_report(audits: list[ArticleAudit]) -> str:
    lines = [
        "# Explanation quality triage",
        "",
        "This is a review queue, not an automatic quality verdict.",
        "Character-count warnings must not be fixed by padding.",
        "",
        f"Articles scanned: **{len(audits)}**",
        "",
        "## Priority queue",
        "",
        "| rank | article | score | flagged H2 | product-route terms |",
        "|---:|---|---:|---:|---|",
    ]
    ranked = sorted(audits, key=lambda item: (-priority_score(item), item.article_id))
    for rank, audit in enumerate(ranked, start=1):
        product = ", ".join(audit.product_terms_without_goods_route) or "-"
        lines.append(
            f"| {rank} | {audit.article_id} {audit.title} | {priority_score(audit)} | "
            f"{len(audit.findings)} | {product} |"
        )

    lines.extend(["", "## Flagged sections", ""])
    for audit in ranked:
        if not audit.findings and not audit.product_terms_without_goods_route:
            continue
        lines.append(f"### {audit.article_id} {audit.title}")
        lines.append("")
        for finding in audit.findings:
            flags = " / ".join(finding.flags)
            lines.append(
                f"- `{finding.heading}` — {finding.chars} chars, "
                f"{finding.paragraphs} paragraph(s): {flags}"
            )
        if audit.product_terms_without_goods_route:
            lines.append(
                "- Product terms without an article-level goods route: "
                + ", ".join(audit.product_terms_without_goods_route)
            )
        lines.append("")

    repeated = repeated_h2_headings(audits)
    lines.extend(["## Repeated H2 headings across 4+ articles", ""])
    if repeated:
        for heading, count in sorted(repeated.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"- `{heading}`: {count} articles")
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    print(markdown_report(audit_all()))


if __name__ == "__main__":
    main()
