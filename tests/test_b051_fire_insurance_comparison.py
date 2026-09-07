from __future__ import annotations

import unittest
from pathlib import Path

from bousai_blog.registry import load_registry

ROOT = Path(__file__).resolve().parents[1]


class B051FireInsuranceComparisonTests(unittest.TestCase):
    def _text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_source_and_preview_keep_all_comparison_targets(self) -> None:
        source = self._text("content/articles/B051_fire_insurance_10_company_comparison.md")
        preview = self._text("preview/article_b051.html")
        companies = (
            "ソニー損保", "SBI損保", "セコム損保", "SOMPOダイレクト", "日新火災",
            "三井住友海上", "東京海上日動", "あいおいニッセイ同和損保", "AIG損保", "損保ジャパン",
        )
        for company in companies:
            self.assertIn(company, source)
            self.assertIn(company, preview)

    def test_individual_company_explanations_are_substantive_and_scannable(self) -> None:
        source = self._text("content/articles/B051_fire_insurance_10_company_comparison.md")
        preview = self._text("preview/article_b051.html")
        self.assertGreaterEqual(source.count("**特徴："), 10)
        self.assertGreaterEqual(source.count("**確認ポイント："), 10)
        self.assertGreaterEqual(preview.count("<strong>特徴："), 10)
        self.assertGreaterEqual(preview.count("<strong>確認ポイント："), 10)
        for token in ("実損払", "定率払", "ワイド・ベーシック・スリム", "フルサポート", "特定設備", "水災一時金特約", "ベーシックI型"):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        self.assertIn("特定設備水災補償特約", preview)

    def test_company_details_are_single_column_after_copy_expansion(self) -> None:
        preview = self._text("preview/article_b051.html")
        # The comparison table stays compact, but long company explanations
        # must not return to a multi-column layout.
        self.assertEqual(3, preview.count('class="visual-card-grid" style="grid-template-columns:1fr"'))
        self.assertNotIn('style="grid-template-columns:2fr', preview)

    def test_article_keeps_neutral_comparison_boundaries(self) -> None:
        source = self._text("content/articles/B051_fire_insurance_10_company_comparison.md")
        preview = self._text("preview/article_b051.html")
        self.assertIn("最安ランキング", source)
        self.assertIn("総合1位〜10位のランキングではありません", preview)
        for text in (source, preview):
            self.assertIn("水災", text)
            self.assertIn("支払", text)
            self.assertIn("2026年10月1日", text)
            self.assertNotIn("amazon.co.jp", text.lower())
            self.assertNotIn("おすすめ1位", text)
            self.assertNotIn("必ず保険金", text)

    def test_internal_cluster_links_are_preserved(self) -> None:
        source = self._text("content/articles/B051_fire_insurance_10_company_comparison.md")
        preview = self._text("preview/article_b051.html")
        for link in ("article_b013.html", "article_b016.html", "article_b017.html"):
            self.assertIn(link, source)
            self.assertIn(link, preview)
        self.assertIn("article_b019.html", preview)

    def test_registry_and_insurance_category_publish_b051(self) -> None:
        registry = load_registry(ROOT / "data/content_registry.json")
        matches = [item for item in registry["articles"] if item.get("article_id") == "B051"]
        self.assertEqual(1, len(matches))
        article = matches[0]
        self.assertEqual("insurance/fire-insurance-10-company-comparison.html", article["planned_public_path"])
        self.assertEqual("2026-09-07", article["published_at"])
        self.assertEqual(0, article["image_source_count"])
        self.assertEqual("APPROVED", article["image_status"])
        category = self._text("preview/category_insurance.html")
        self.assertIn('href="article_b051.html"', category)
        self.assertIn('data-article-id="B051"', category)

    def test_review_and_no_image_decision_are_recorded(self) -> None:
        review = self._text("docs/reviews/B051_CHECKLIST.md")
        images = self._text("docs/research/B051_IMAGES.md")
        self.assertIn("review_status: PASS", review)
        self.assertIn("READY_TO_PUBLISH: YES", review)
        self.assertIn("image_source_count: 0", images)
        self.assertIn("image_status: APPROVED", images)


if __name__ == "__main__":
    unittest.main()
