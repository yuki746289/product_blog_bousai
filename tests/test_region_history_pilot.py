from __future__ import annotations

import json
import unittest
from pathlib import Path

from bousai_blog.registry import load_registry

ROOT = Path(__file__).resolve().parents[1]


class RegionHistoryPilotTests(unittest.TestCase):
    def _text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_b048_miyagi_source_and_preview_keep_history_safety_boundary(self) -> None:
        source = self._text("content/articles/B048_miyagi_earthquake_tsunami_history.md")
        preview = self._text("preview/article_b048.html")
        for token in (
            "1978年宮城県沖地震",
            "東日本大震災",
            "津波災害警戒区域",
            "過去に被災しなかった",
        ):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        for link in ("article_b023.html", "article_b024.html", "article_b041.html", "article_b030.html"):
            self.assertIn(link, source)
            self.assertIn(link, preview)
        self.assertIn("Damage%20of%20Tsunami%20in%20Natori.JPEG", preview)
        self.assertNotIn("amazon.co.jp", preview.lower())

    def test_b049_hiroshima_source_and_preview_do_not_turn_history_into_prediction(self) -> None:
        source = self._text("content/articles/B049_hiroshima_landslide_history.md")
        preview = self._text("preview/article_b049.html")
        for token in (
            "1999年",
            "2014年",
            "2018年",
            "土砂災害ハザードマップ",
            "将来の被災地点予想",
        ):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        for link in ("article_b036.html", "article_b020.html", "article_b042.html", "article_b015.html"):
            self.assertIn(link, source)
            self.assertIn(link, preview)
        self.assertIn("%E5%BA%83%E5%B3%B6%E5%9C%9F%E7%A0%82", preview)
        self.assertNotIn("amazon.co.jp", preview.lower())

    def test_b050_arakawa_source_and_preview_separate_history_from_current_hazard(self) -> None:
        source = self._text("content/articles/B050_arakawa_flood_history.md")
        preview = self._text("preview/article_b050.html")
        for token in (
            "明治43年",
            "荒川放水路",
            "カスリーン台風",
            "浸水継続時間",
            "大雨時に川や水門を見に行かない",
        ):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        for link in ("article_b042.html", "article_b012.html", "article_b008.html", "article_b010.html", "article_b015.html"):
            self.assertIn(link, source)
            self.assertIn(link, preview)
        self.assertIn("%E6%97%A7%E5%B2%A9%E6%B7%B5%E6%B0%B4%E9%96%80.jpg", preview)
        self.assertNotIn("amazon.co.jp", preview.lower())

    def test_research_and_image_records_exist_for_all_three(self) -> None:
        for article_id in ("B048", "B049", "B050"):
            self.assertTrue((ROOT / f"docs/research/{article_id}_REGION_BRIEF.md").is_file())
            self.assertTrue((ROOT / f"docs/research/{article_id}_IMAGES.md").is_file())
            self.assertTrue((ROOT / f"docs/reviews/{article_id}_CHECKLIST.md").is_file())

    def test_registry_loader_merges_only_the_reviewed_additions(self) -> None:
        base = json.loads((ROOT / "data/content_registry.json").read_text(encoding="utf-8"))
        additions = json.loads((ROOT / "data/content_registry_additions.json").read_text(encoding="utf-8"))
        registry = load_registry(ROOT / "data/content_registry.json")

        base_ids = [article["article_id"] for article in base["articles"]]
        addition_ids = [article["article_id"] for article in additions["articles"]]
        ids = [article["article_id"] for article in registry["articles"]]

        self.assertEqual(len(base_ids) + len(addition_ids), len(ids))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(base_ids + addition_ids, ids)

        for article in additions["articles"]:
            self.assertEqual("READY_TO_PUBLISH", article["status"])
            self.assertEqual([], article["publish_blockers"])
            self.assertEqual("APPROVED", article["manual_review_status"])
            self.assertRegex(article["published_at"], r"^\d{4}-\d{2}-\d{2}$")
            self.assertRegex(article["modified_at"], r"^\d{4}-\d{2}-\d{2}$")

        regional = {article["article_id"]: article for article in additions["articles"] if article["article_id"] in {"B048", "B049", "B050"}}
        self.assertEqual({"B048", "B049", "B050"}, set(regional))
        for article in regional.values():
            self.assertEqual("2026-09-07", article["published_at"])
            self.assertEqual("2026-09-07", article["modified_at"])

    def test_category_routes_surface_region_history_without_new_top_level_category(self) -> None:
        earthquake = self._text("preview/category_earthquake.html")
        flood = self._text("preview/category_flood.html")

        self.assertIn("地域の災害史から備えを考える", earthquake)
        self.assertIn('href="article_b048.html"', earthquake)
        self.assertIn('data-article-id="B048"', earthquake)

        self.assertIn("地域の災害史から備えを考える", flood)
        self.assertIn('href="article_b049.html"', flood)
        self.assertIn('href="article_b050.html"', flood)
        self.assertIn('data-article-id="B049"', flood)
        self.assertIn('data-article-id="B050"', flood)


if __name__ == "__main__":
    unittest.main()
