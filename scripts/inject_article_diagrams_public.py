# Created: 2026-09-09 09:38 JST
"""Inject configured explanatory infographics into built production HTML."""

from __future__ import annotations

from pathlib import Path

from article_diagrams import DIAGRAMS, inject_article_diagram

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


def inject_all() -> list[str]:
    changed: list[str] = []
    for output_path, spec in DIAGRAMS.items():
        path = PUBLIC / output_path
        if not path.is_file():
            raise FileNotFoundError(f"Production article missing for diagram {spec['article_id']}: {path}")
        original = path.read_text(encoding="utf-8")
        updated = inject_article_diagram(original, output_path)
        marker = f'data-article-diagram="{spec["article_id"]}"'
        if updated.count(marker) != 1:
            raise ValueError(f"Expected one diagram marker for {spec['article_id']}")
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(spec["article_id"])
    return changed


def main() -> int:
    changed = inject_all()
    print("Injected article diagrams: " + ", ".join(changed))
    if len(changed) != len(DIAGRAMS):
        raise SystemExit(f"Expected {len(DIAGRAMS)} changed articles, got {len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
