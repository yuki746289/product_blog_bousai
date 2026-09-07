from __future__ import annotations

import unittest
from pathlib import Path

from bousai_blog.registry import load_registry

ROOT = Path(__file__).resolve().parents[1]


class RegionalEmergencyActionLinksTests(unittest.TestCase):
    def _text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_action_articles_are_registered_and_routed(self) -> None:
        registry = load_registry(ROOT / "data/content_registry.json")
        by_id = {item["article_id"]: item for item in registry["articles"]}

        self.assertEqual(
            "earthquake/earthquake-immediate-actions.html",
            by_id["B057"]["planned_public_path"],
        )
        self.assertEqual("high", by_id["B057"]["risk_level"])
        self.assertEqual("action", by_id["B057"]["content_role"])

        self.assertEqual(
            "guide/volcano-eruption-ash-actions.html",
            by_id["B058"]["planned_public_path"],
        )
        self.assertEqual("high", by_id["B058"]["risk_level"])
        self.assertEqual("action", by_id["B058"]["content_role"])

        earthquake = self._text("preview/category_earthquake.html")
        guide = self._text("preview/category_guide.html")
        self.assertIn('href="article_b057.html"', earthquake)
        self.assertIn('data-article-id="B057"', earthquake)
        self.assertIn('href="article_b058.html"', guide)
        self.assertIn('data-article-id="B058"', guide)

    def test_earthquake_action_article_preserves_initial_safety_order(self) -> None:
        source = self._text("content/articles/B057_earthquake_immediate_actions.md")
        preview = self._text("preview/article_b057.html")
        for token in (
            "まず身の安全",
            "あわてて外へ飛び出",
            "津波警報を待つことを前提にしません",
            "article_b041.html",
            "article_b040.html",
            "article_b039.html",
            "article_b038.html",
        ):
            self.assertIn(token, source)
            self.assertIn(token, preview)

    def test_volcano_action_article_preserves_warning_and_ash_boundaries(self) -> None:
        source = self._text("content/articles/B058_volcano_eruption_ash_immediate_actions.md")
        preview = self._text("preview/article_b058.html")
        for token in (
            "警戒が必要な範囲",
            "少量",
            "やや多量",
            "多量",
            "外出を控える",
            "article_b056.html",
        ):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        self.assertIn("危険区域に残ってよい", source)
        self.assertIn("危険区域に残ってよい", preview)

    def test_each_regional_history_has_a_relevant_action_route(self) -> None:
        routes = {
            "B048": ("content/articles/B048_miyagi_earthquake_tsunami_history.md", "preview/article_b048.html", "article_b041.html"),
            "B049": ("content/articles/B049_hiroshima_landslide_history.md", "preview/article_b049.html", "article_b036.html"),
            "B050": ("content/articles/B050_arakawa_flood_history.md", "preview/article_b050.html", "article_b042.html"),
            "B053": ("content/articles/B053_nagoya_flood_storm_surge_history.md", "preview/article_b053.html", "article_b043.html"),
            "B054": ("content/articles/B054_kobe_earthquake_history.md", "preview/article_b054.html", "article_b057.html"),
            "B055": ("content/articles/B055_kochi_nankai_earthquake_tsunami_history.md", "preview/article_b055.html", "article_b041.html"),
            "B056": ("content/articles/B056_kagoshima_sakurajima_eruption_ash_history.md", "preview/article_b056.html", "article_b058.html"),
        }
        for article_id, (source_path, preview_path, action_link) in routes.items():
            with self.subTest(article_id=article_id):
                self.assertIn(action_link, self._text(source_path))
                self.assertIn(action_link, self._text(preview_path))

    def test_action_articles_have_review_and_image_decisions(self) -> None:
        for article_id in ("B057", "B058"):
            review = self._text(f"docs/reviews/{article_id}_CHECKLIST.md")
            images = self._text(f"docs/research/{article_id}_IMAGES.md")
            self.assertIn("review_status: PASS", review)
            self.assertIn("READY_TO_PUBLISH: YES", review)
            self.assertIn("image_source_count: 0", images)
            self.assertIn("image_status: APPROVED", images)


if __name__ == "__main__":
    unittest.main()
