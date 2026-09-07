from __future__ import annotations

import re
from pathlib import Path

import apply_article_content_depth_fixes_20260907 as base


def insert_markdown(path: Path, article_id: str, addition: str) -> None:
    text = path.read_text(encoding="utf-8")
    marker = f"<!-- {base.STAMP}:{article_id} -->"
    if marker in text:
        return

    candidates = ["\n## まとめ\n", "\n## 関連記事\n", "\n## 公的情報\n", "\n## 公的情報・参考資料\n"]
    positions = [(text.find(needle), needle) for needle in candidates if text.find(needle) >= 0]
    if not positions:
        raise RuntimeError(f"Insertion heading not found in {path}")
    pos, _ = min(positions, key=lambda item: item[0])
    block = f"\n{marker}\n\n{addition.rstrip()}\n"
    path.write_text(text[:pos] + block + text[pos:], encoding="utf-8")


def insert_preview(path: Path, article_id: str, addition: str) -> None:
    text = path.read_text(encoding="utf-8")
    marker = f"<!-- {base.STAMP}:{article_id} -->"
    if marker in text:
        return

    patterns = [
        r"<h2(?:\s[^>]*)?>\s*まとめ\s*</h2>",
        r"<h2(?:\s[^>]*)?>\s*関連記事\s*</h2>",
        r"<h2(?:\s[^>]*)?>\s*公的情報(?:・参考資料)?\s*</h2>",
    ]
    matches = []
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            matches.append(match)
    if not matches:
        raise RuntimeError(f"Insertion h2 not found in {path}")
    match = min(matches, key=lambda item: item.start())
    block = f"\n{marker}\n{addition.rstrip()}\n"
    path.write_text(text[: match.start()] + block + text[match.start() :], encoding="utf-8")


base.insert_markdown = insert_markdown
base.insert_preview = insert_preview

if __name__ == "__main__":
    raise SystemExit(base.main())
