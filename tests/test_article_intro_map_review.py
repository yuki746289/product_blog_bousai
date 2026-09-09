# Created: 2026-09-09 16:13 JST
# Updated: 2026-09-09 18:45 JST
import re
import unittest
from html import unescape
from pathlib import Path

from scripts import sync_previews_core as _core
from scripts.sync_previews_from_markdown import ALL_ARTICLE_IDS

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
    def setUp(self):
        self.registry = _core.load_registry(_core.REGISTRY)
        self.by_id = {article["article_id"]: article for article in self.registry["articles"]}
        self.aliases = _core.preview_aliases(self.registry)

    def preview_lead(self, article_id: str) -> str:
        preview = (ROOT / self.by_id[article_id]["preview_path"]).read_text(encoding="utf-8")
        match = LEAD_RE.search(preview)
        self.assertIsNotNone(match, f"article-lead missing: {article_id}")
        return plain_html(match.group(1))

    def markdown_intro(self, article_id: str) -> str:
        markdown = (ROOT / self.by_id[article_id]["source_path"]).read_text(encoding="utf-8")
        intro, _ = _core.parse_source(markdown)
        self.assertTrue(intro.strip(), f"Markdown intro missing: {article_id}")
        return plain_html(_core.inline_markup(intro, self.aliases))

    def test_manual_review_ledger_covers_all_sixty_articles(self):
        text = LEDGER.read_text(encoding="utf-8")
        rows = re.findall(r"^\| (B\d{3}) \| PASS \| KEEP \|", text, re.MULTILINE)
        self.assertEqual(60, len(rows))
        self.assertEqual(ALL_ARTICLE_IDS, set(rows))
        self.assertNotIn("OVERRIDE", text)

    def test_sync_scope_covers_exactly_b001_through_b060(self):
        self.assertEqual({f"B{i:03d}" for i in range(1, 61)}, ALL_ARTICLE_IDS)
        self.assertTrue(ALL_ARTICLE_IDS.issubset(self.by_id))

    def test_all_public_leads_equal_markdown_intros(self):
        for article_id in sorted(ALL_ARTICLE_IDS):
            with self.subTest(article_id=article_id):
                self.assertEqual(self.markdown_intro(article_id), self.preview_lead(article_id))

    def test_former_override_articles_keep_compact_article_specific_intros(self):
        expected_terms = {
            "B013": ("水災", "風災", "建物", "家財"),
            "B021": ("台風", "24", "12", "6", "中止"),
            "B024": ("停電", "断水", "トイレ", "復電"),
            "B029": ("車", "脱出", "停止表示", "水害"),
            "B057": ("地震", "揺れ", "津波", "火災"),
        }
        for article_id, terms in expected_terms.items():
            with self.subTest(article_id=article_id):
                text = self.markdown_intro(article_id)
                self.assertGreaterEqual(len(text), 55)
                self.assertLessEqual(len(text), 180)
                for term in terms:
                    self.assertIn(term, text)
                self.assertEqual(text, self.preview_lead(article_id))

    def test_b056_public_lead_preserves_kagoshima_article_specific_context(self):
        lead = self.preview_lead("B056")
        for term in ("桜島", "鹿児島市", "大正噴火", "降灰"):
            with self.subTest(term=term):
                self.assertIn(term, lead)
        self.assertEqual(self.markdown_intro("B056"), lead)


if __name__ == "__main__":
    unittest.main()
