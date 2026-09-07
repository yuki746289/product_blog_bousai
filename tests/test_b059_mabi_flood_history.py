# Created: 2026-09-08 08:16 JST
from __future__ import annotations

import unittest
from pathlib import Path

from bousai_blog.registry import load_registry

ROOT = Path(__file__).resolve().parents[1]


class B059MabiFloodHistoryTests(unittest.TestCase):
    def text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_b059_is_registered_reviewed_and_publishable(self) -> None:
        registry = load_registry(ROOT / "data/content_registry.json")
        item = next(article for article in registry["articles"] if article["article_id"] == "B059")
        self.assertEqual("region/okayama/mabi-2018-flood-history.html", item["planned_public_path"])
        self.assertEqual("READY_TO_PUBLISH", item["status"])
        self.assertEqual("APPROVED", item["manual_review_status"])
        self.assertEqual("PASS", item["review_checklist_status"])
        self.assertEqual([], item["publish_blockers"])
        self.assertEqual("2026-09-08", item["published_at"])
        self.assertEqual("2026-09-08", item["modified_at"])
        self.assertEqual(0, item["image_source_count"])
        self.assertEqual(3828, item["body_char_count_approx"])

    def test_source_and_preview_keep_verified_2018_damage_data(self) -> None:
        source = self.text("content/articles/B059_mabi_2018_flood_history.md")
        preview = self.text("preview/article_b059.html")
        for token in (
            "309.5mm",
            "270.5mm",
            "8か所",
            "約1,200ha",
            "最大約5m",
            "74人",
            "4,633棟",
            "約8,900戸",
            "約4,200戸",
            "バックウォーター",
        ):
            self.assertIn(token, source)
            self.assertIn(token, preview)

    def test_b059_separates_history_current_engineering_and_current_hazard(self) -> None:
        source = self.text("content/articles/B059_mabi_2018_flood_history.md")
        preview = self.text("preview/article_b059.html")
        for token in ("2024年3月", "約4.6km", "計画規模（L1）", "想定最大規模（L2）", "内水"):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        self.assertIn("今後は浸水しない", source)
        self.assertIn("洪水リスクがなくなった", preview)
        self.assertIn("2018年の浸水実績は現在の危険区域そのものではありません", preview)

    def test_b059_turns_data_into_actions_and_links_to_action_articles(self) -> None:
        source = self.text("content/articles/B059_mabi_2018_flood_history.md")
        preview = self.text("preview/article_b059.html")
        self.assertIn("データから考える", source)
        self.assertIn("データから考える", preview)
        self.assertIn("読み取れる地域課題", source)
        self.assertIn("読み取れる地域課題", preview)
        for link in (
            "article_b042.html",
            "article_b020.html",
            "article_b008.html",
            "article_b003.html",
            "article_b015.html",
            "article_b037.html",
        ):
            self.assertIn(link, source)
            self.assertIn(link, preview)
        self.assertNotIn("amazon.co.jp", preview.lower())

    def test_b059_research_image_and_review_records_exist(self) -> None:
        brief = self.text("docs/research/B059_REGION_BRIEF.md")
        images = self.text("docs/research/B059_IMAGES.md")
        review = self.text("docs/reviews/B059_CHECKLIST.md")
        self.assertIn("F-B059-001", brief)
        self.assertIn("F-B059-006", brief)
        self.assertIn("image_source_count: 0", images)
        self.assertIn("image_status: APPROVED", images)
        self.assertIn("review_status: PASS", review)
        self.assertIn("READY_TO_PUBLISH: YES", review)
        self.assertIn("3,828字", review)

    def test_region_and_flood_categories_surface_b059(self) -> None:
        region = self.text("preview/category_region.html")
        flood = self.text("preview/category_flood.html")
        for html in (region, flood):
            self.assertIn('href="article_b059.html"', html)
            self.assertIn('data-article-id="B059"', html)
        self.assertIn("8地域・8記事", region)
        self.assertIn("岡山・真備", region)


if __name__ == "__main__":
    unittest.main()
