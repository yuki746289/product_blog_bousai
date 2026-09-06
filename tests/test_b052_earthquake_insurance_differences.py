from __future__ import annotations

import unittest
from pathlib import Path

from bousai_blog.registry import load_registry

ROOT = Path(__file__).resolve().parents[1]


class B052EarthquakeInsuranceDifferencesTests(unittest.TestCase):
    def _text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_source_and_preview_keep_core_same_vs_different_boundary(self) -> None:
        source = self._text("content/articles/B052_earthquake_insurance_company_differences.md")
        preview = self._text("preview/article_b052.html")
        for text in (source, preview):
            self.assertIn("30〜50％", text)
            self.assertIn("5,000万円", text)
            self.assertIn("1,000万円", text)
            self.assertIn("全損", text)
            self.assertIn("大半損", text)
            self.assertIn("小半損", text)
            self.assertIn("一部損", text)
            self.assertIn("地震火災費用", text)
            self.assertIn("払込方法", text)

    def test_article_does_not_turn_statutory_earthquake_insurance_into_ranking(self) -> None:
        source = self._text("content/articles/B052_earthquake_insurance_company_differences.md")
        preview = self._text("preview/article_b052.html")
        for text in (source, preview):
            self.assertIn("会社差", text)
            self.assertNotIn("おすすめ1位", text)
            self.assertNotIn("最安会社ランキング", text)
            self.assertNotIn("amazon.co.jp", text.lower())
        self.assertIn("地震保険会社ランキングではなく", source)
        self.assertIn("地震保険の会社ランキングは作らず", preview)

    def test_internal_links_preserve_cluster_roles(self) -> None:
        source = self._text("content/articles/B052_earthquake_insurance_company_differences.md")
        preview = self._text("preview/article_b052.html")
        for link in ("article_b017.html", "article_b051.html", "article_b019.html"):
            self.assertIn(link, source)
            self.assertIn(link, preview)

    def test_registry_and_category_publish_b052(self) -> None:
        registry = load_registry(ROOT / "data/content_registry.json")
        matches = [item for item in registry["articles"] if item.get("article_id") == "B052"]
        self.assertEqual(1, len(matches))
        article = matches[0]
        self.assertEqual("B017", article["parent_article_id"])
        self.assertEqual("insurance/earthquake-insurance-company-differences.html", article["planned_public_path"])
        self.assertEqual("2026-09-07", article["published_at"])
        self.assertEqual(0, article["image_source_count"])
        self.assertEqual("APPROVED", article["image_status"])

        category = self._text("preview/category_insurance.html")
        self.assertIn('href="article_b052.html"', category)
        self.assertIn('data-article-id="B052"', category)
        self.assertLess(category.index('data-article-id="B017"'), category.index('data-article-id="B052"'))
        self.assertLess(category.index('data-article-id="B052"'), category.index('data-article-id="B018"'))

    def test_research_review_and_no_image_decision_exist(self) -> None:
        brief = self._text("docs/research/B052_EARTHQUAKE_INSURANCE_DIFFERENCES_BRIEF.md")
        review = self._text("docs/reviews/B052_CHECKLIST.md")
        images = self._text("docs/research/B052_IMAGES.md")
        self.assertIn("記事化する", brief)
        self.assertIn("review_status: PASS", review)
        self.assertIn("READY_TO_PUBLISH: YES", review)
        self.assertIn("image_source_count: 0", images)
        self.assertIn("image_status: APPROVED", images)


if __name__ == "__main__":
    unittest.main()
