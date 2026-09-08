from __future__ import annotations

import unittest
from pathlib import Path

from bousai_blog.registry import load_registry
from scripts.audit_article_content_metrics import audit

ROOT = Path(__file__).resolve().parents[1]


class B060VolcanicAshGoodsTests(unittest.TestCase):
    def text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_b060_is_registered_as_reviewed_product_article(self) -> None:
        registry = load_registry(ROOT / "data/content_registry.json")
        by_id = {item["article_id"]: item for item in registry["articles"]}
        item = by_id["B060"]
        self.assertEqual("goods/volcanic-ash-protection.html", item["planned_public_path"])
        self.assertEqual("product", item["content_role"])
        self.assertTrue(item["affiliate"])
        self.assertEqual("READY_TO_PUBLISH", item["status"])
        self.assertEqual("APPROVED", item["manual_review_status"])
        self.assertEqual([], item["publish_blockers"])
        self.assertEqual("2026-12-08", item["next_review_at"])

    def test_b060_current_metric_matches_registry(self) -> None:
        metrics = {row.article_id: row for row in audit()}
        row = metrics["B060"]
        self.assertEqual(3602, row.body_char_count)
        self.assertEqual("PASS_NO_NUMERIC_RULE", row.length_status)

    def test_product_page_keeps_safety_before_commerce(self) -> None:
        preview = self.text("preview/article_b060.html")
        safety = preview.index("多量（1mm以上）")
        first_amazon = preview.index("amazon.co.jp")
        self.assertLess(safety, first_amazon)
        self.assertIn("商品より公的情報と避難行動を優先", preview)
        self.assertIn('class="article-shell product-page"', preview)
        self.assertIn("Amazonのアソシエイトとして", preview)

    def test_three_products_have_traceable_specs_and_search_links(self) -> None:
        source = self.text("content/articles/B060_volcanic_ash_protection_goods.md")
        preview = self.text("preview/article_b060.html")
        for token in (
            "DD02-S2-2K", "第TM657号", "2,198円",
            "DD02V-S2-2K", "第TM656号", "3,188円",
            "LX-22", "JIS T 8147:2016", "3,850円",
        ):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        for query in (
            "s?k=DD02-S2-2K&tag=yukitaka83-22",
            "s?k=DD02V-S2-2K&tag=yukitaka83-22",
            "s?k=%E9%87%8D%E6%9D%BE+LX-22&tag=yukitaka83-22",
        ):
            self.assertIn(query, source)
            self.assertIn(query.replace("&", "&"), preview)
        self.assertNotIn("m.media-amazon.com", preview)
        self.assertNotIn("/dp/", preview)

    def test_image_exception_is_explicit_and_no_fake_product_image_is_used(self) -> None:
        record = self.text("docs/research/B060_IMAGES.md")
        preview = self.text("preview/article_b060.html")
        self.assertIn("Amazonが正規に提供する画像URL", record)
        self.assertIn("ASINから画像URLを推測", record)
        self.assertIn("実商品画像の代用となるAI画像も使わない", record)
        self.assertNotIn("<img", preview.lower())

    def test_b056_b058_and_goods_category_link_to_b060(self) -> None:
        for path in (
            "content/articles/B056_kagoshima_sakurajima_eruption_ash_history.md",
            "content/articles/B058_volcano_eruption_ash_immediate_actions.md",
            "preview/article_b056.html",
            "preview/article_b058.html",
            "preview/category_goods.html",
        ):
            with self.subTest(path=path):
                self.assertIn("article_b060.html", self.text(path))

    def test_research_and_review_records_exist(self) -> None:
        self.assertTrue((ROOT / "docs/research/B060_PRODUCT_BRIEF.md").is_file())
        self.assertTrue((ROOT / "docs/research/B060_IMAGES.md").is_file())
        review = self.text("docs/reviews/B060_CHECKLIST.md")
        self.assertIn("review_status: PASS", review)
        self.assertIn("READY_TO_PUBLISH: YES", review)
        self.assertIn("PASS WITH DOCUMENTED EXCEPTION", review)


if __name__ == "__main__":
    unittest.main()
