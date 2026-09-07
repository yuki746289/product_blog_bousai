from __future__ import annotations

import unittest
from pathlib import Path

from bousai_blog.registry import load_registry

ROOT = Path(__file__).resolve().parents[1]


class RegionHistoryBatch2Tests(unittest.TestCase):
    def text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_batch_is_registered_and_publishable(self) -> None:
        registry = load_registry(ROOT / "data/content_registry.json")
        by_id = {item["article_id"]: item for item in registry["articles"]}
        expected = {
            "B053": "region/nagoya/flood-storm-surge-history.html",
            "B054": "region/kobe/earthquake-history.html",
            "B055": "region/kochi/nankai-earthquake-tsunami-history.html",
            "B056": "region/kagoshima/sakurajima-eruption-ash-history.html",
        }
        for article_id, path in expected.items():
            with self.subTest(article_id=article_id):
                item = by_id[article_id]
                self.assertEqual(path, item["planned_public_path"])
                self.assertEqual("READY_TO_PUBLISH", item["status"])
                self.assertEqual("APPROVED", item["manual_review_status"])
                self.assertEqual([], item["publish_blockers"])
                self.assertEqual("2026-09-07", item["published_at"])

    def test_every_article_turns_data_into_countermeasures(self) -> None:
        source_paths = {
            "B053": "content/articles/B053_nagoya_flood_storm_surge_history.md",
            "B054": "content/articles/B054_kobe_earthquake_history.md",
            "B055": "content/articles/B055_kochi_nankai_earthquake_tsunami_history.md",
            "B056": "content/articles/B056_kagoshima_sakurajima_eruption_ash_history.md",
        }
        preview_paths = {article_id: f"preview/article_{article_id.lower()}.html" for article_id in source_paths}
        for article_id, source_path in source_paths.items():
            with self.subTest(article_id=article_id):
                source = self.text(source_path)
                preview = self.text(preview_paths[article_id])
                self.assertIn("データから考える", source)
                self.assertIn("データから考える", preview)
                self.assertIn("読み取れる", source)
                self.assertIn("読み取れる", preview)
                self.assertNotIn("amazon.co.jp", preview.lower())

    def test_nagoya_preserves_storm_surge_flood_and_inland_flood_distinction(self) -> None:
        source = self.text("content/articles/B053_nagoya_flood_storm_surge_history.md")
        preview = self.text("preview/article_b053.html")
        for token in ("5.31", "79日", "97.0", "534.5", "内水氾濫", "高潮"):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        for link in ("article_b043.html", "article_b042.html", "article_b020.html", "article_b008.html", "article_b010.html"):
            self.assertIn(link, source)
            self.assertIn(link, preview)

    def test_kobe_separates_structural_furniture_and_fire_measures(self) -> None:
        source = self.text("content/articles/B054_kobe_earthquake_history.md")
        preview = self.text("preview/article_b054.html")
        for token in ("67,421", "55,145", "175件", "7,386", "原因が特定", "感震ブレーカー"):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        for link in ("article_b023.html", "article_b040.html", "article_b039.html", "article_b024.html"):
            self.assertIn(link, source)
            self.assertIn(link, preview)

    def test_kochi_keeps_latest_projection_and_history_separate(self) -> None:
        source = self.text("content/articles/B055_kochi_nankai_earthquake_tsunami_history.md")
        preview = self.text("preview/article_b055.html")
        for token in ("1946", "4〜6m", "3分", "338", "280,484", "発生時期を予測"):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        self.assertIn("2025年10月29日", source)
        self.assertIn("2026年3月24日", source)
        self.assertIn("記事ID: B055", preview)

    def test_kagoshima_keeps_scenario_and_current_forecast_separate(self) -> None:
        source = self.text("content/articles/B056_kagoshima_sakurajima_eruption_ash_history.md")
        preview = self.text("preview/article_b056.html")
        for token in ("18,000", "99回", "105g", "最大1m", "0.1mm", "降灰予報"):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        self.assertIn("Public Domain", preview)
        self.assertIn("Sakurajima%20taisyo%20eruption%20at%20seto%20strait.jpg", preview)

    def test_research_image_and_review_records_exist(self) -> None:
        for article_id in ("B053", "B054", "B055", "B056"):
            self.assertTrue((ROOT / f"docs/research/{article_id}_REGION_BRIEF.md").is_file())
            self.assertTrue((ROOT / f"docs/research/{article_id}_IMAGES.md").is_file())
            review = self.text(f"docs/reviews/{article_id}_CHECKLIST.md")
            self.assertIn("review_status: PASS", review)
            self.assertIn("READY_TO_PUBLISH: YES", review)

    def test_region_category_has_seven_populated_regions_without_empty_placeholders(self) -> None:
        region = self.text("preview/category_region.html")
        self.assertIn("7地域・7記事", region)
        for heading in ("北海道・東北", "関東", "中部", "近畿", "中国", "四国", "九州・沖縄"):
            self.assertIn(f"<h2>{heading}</h2>", region)
        for article_id in range(48, 57):
            if article_id in (51, 52):
                continue
            self.assertIn(f'article_b{article_id:03d}.html', region)
        self.assertNotIn("準備中", region)

    def test_disaster_categories_surface_new_regional_articles(self) -> None:
        flood = self.text("preview/category_flood.html")
        earthquake = self.text("preview/category_earthquake.html")
        guide = self.text("preview/category_guide.html")
        self.assertIn('href="article_b053.html"', flood)
        self.assertIn('href="article_b054.html"', earthquake)
        self.assertIn('href="article_b055.html"', earthquake)
        self.assertIn('href="article_b056.html"', guide)
        for html in (flood, earthquake, guide):
            self.assertIn('href="category_region.html"', html)


if __name__ == "__main__":
    unittest.main()
