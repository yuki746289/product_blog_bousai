# Created: 2026-09-09 16:13 JST
# Updated: 2026-09-09 16:17 JST
import re
import unittest
from html import unescape
from pathlib import Path

from scripts import sync_previews_core as _core
from scripts.sync_previews_from_markdown import LEAD_OVERRIDES

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/reviews/ARTICLE_INTRO_MAP_REVIEW_20260909.md"
LEAD_RE = re.compile(
    r'<p\s+class=["\']article-lead["\'][^>]*>(.*?)</p>',
    re.IGNORECASE | re.DOTALL,
)
TAG_RE = re.compile(r"<[^>]+>")


def plain_html(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(TAG_RE.sub("", value))).strip()


class ArticleIntroMapReviewTests(unittest.TestCase):
    def test_manual_review_ledger_covers_all_sixty_articles(self):
        text = LEDGER.read_text(encoding="utf-8")
        rows = re.findall(r"^\| (B\d{3}) \| PASS \| (KEEP|OVERRIDE) \|", text, re.MULTILINE)
        self.assertEqual(60, len(rows))
        self.assertEqual({f"B{i:03d}" for i in range(1, 61)}, {article_id for article_id, _ in rows})

    def test_only_five_articles_need_public_lead_overrides(self):
        self.assertEqual({"B013", "B021", "B024", "B029", "B057"}, set(LEAD_OVERRIDES))

    def test_reviewed_lead_overrides_are_present_in_preview(self):
        registry = _core.load_registry(_core.REGISTRY)
        by_id = {article["article_id"]: article for article in registry["articles"]}

        for article_id, expected in LEAD_OVERRIDES.items():
            with self.subTest(article_id=article_id):
                preview = (ROOT / by_id[article_id]["preview_path"]).read_text(encoding="utf-8")
                match = LEAD_RE.search(preview)
                self.assertIsNotNone(match)
                self.assertEqual(expected, plain_html(match.group(1)))

    def test_override_copy_is_compact(self):
        for article_id, text in LEAD_OVERRIDES.items():
            with self.subTest(article_id=article_id):
                self.assertGreaterEqual(len(text), 55)
                self.assertLessEqual(len(text), 150)


if __name__ == "__main__":
    unittest.main()
