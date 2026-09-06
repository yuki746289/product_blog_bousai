# Created: 2026-09-04
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class B040SensitiveBreakerTests(unittest.TestCase):
    def test_b040_is_reviewed_registered_and_elevated(self):
        registry = json.loads((ROOT / "data" / "content_registry.json").read_text(encoding="utf-8"))
        article = next(a for a in registry["articles"] if a.get("article_id") == "B040")
        self.assertEqual("elevated", article["risk_level"])
        self.assertEqual("PASS", article["review_checklist_status"])
        self.assertEqual("READY_TO_PUBLISH", article["status"])
        self.assertEqual("earthquake/earthquake-sensitive-breaker.html", article["planned_public_path"])

    def test_b040_keeps_core_safety_boundaries(self):
        article = (ROOT / "content" / "articles" / "B040_earthquake_sensitive_breaker.md").read_text(encoding="utf-8")
        required = [
            "停電させる設備",
            "電気工事が必要な製品を自己施工しない",
            "夜間用の足元灯・懐中電灯・ランタン",
            "医療機器",
            "ブレーカー操作のために避難を遅らせません",
            "水に濡れた・浸水した機器",
            "焦げた臭い",
            "全国共通の補助制度が必ず使えるという意味ではありません",
        ]
        for phrase in required:
            self.assertIn(phrase, article)

    def test_b040_has_evidence_and_navigation(self):
        for path in [
            ROOT / "docs" / "research" / "B040_SENSITIVE_BREAKER_BRIEF.md",
            ROOT / "docs" / "research" / "B040_SOURCES.md",
            ROOT / "docs" / "research" / "B040_IMAGES.md",
            ROOT / "docs" / "reviews" / "B040_CHECKLIST.md",
            ROOT / "preview" / "article_b040.html",
        ]:
            self.assertTrue(path.exists(), path)

        category = (ROOT / "preview" / "category_earthquake.html").read_text(encoding="utf-8")
        b007 = (ROOT / "content" / "articles" / "B007_earthquake_preparedness_basics.md").read_text(encoding="utf-8")
        b024 = (ROOT / "content" / "articles" / "B024_earthquake_blackout_water_outage.md").read_text(encoding="utf-8")
        self.assertIn('data-article-id="B040"', category)
        self.assertIn("article_b040.html", b007)
        self.assertIn("article_b040.html", b024)

    def test_b040_preview_preserves_safety_and_official_context(self):
        preview = (ROOT / "preview" / "article_b040.html").read_text(encoding="utf-8")
        self.assertIn("感震ブレーカーやブレーカー操作のために、津波・火災・倒壊等からの避難を遅らせない", preview)
        self.assertIn("医療機器の遮断可否を当サイトだけで判断しない", preview)
        self.assertIn("内閣府「感震ブレーカーの普及促進」", preview)
        self.assertIn("総務省消防庁「感震ブレーカー」", preview)


if __name__ == "__main__":
    unittest.main()
