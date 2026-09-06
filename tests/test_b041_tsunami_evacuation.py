# Created: 2026-09-05
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class B041TsunamiEvacuationTests(unittest.TestCase):
    def test_b041_is_high_risk_reviewed_and_registered(self):
        registry = json.loads((ROOT / "data" / "content_registry.json").read_text(encoding="utf-8"))
        article = next(a for a in registry["articles"] if a.get("article_id") == "B041")
        self.assertEqual("high", article["risk_level"])
        self.assertTrue(article["manual_review_required"])
        self.assertEqual("APPROVED", article["manual_review_status"])
        self.assertEqual("PASS", article["review_checklist_status"])
        self.assertEqual("READY_TO_PUBLISH", article["status"])
        self.assertEqual("earthquake/tsunami-evacuation.html", article["planned_public_path"])

    def test_b041_keeps_core_safety_boundaries(self):
        article = (ROOT / "content" / "articles" / "B041_tsunami_evacuation.md").read_text(encoding="utf-8")
        required = [
            "津波警報等を待たず",
            "徒歩を原則",
            "車は絶対禁止",
            "津波警報・注意報が解除されるまでは",
            "第一波が最大とは限らない",
            "家族を迎えに行くため、危険区域へ戻らない",
            "到達予想時刻を「その時刻までは安全」と読まない",
            "当サイト独自の標高・距離・時間閾値を作らない",
        ]
        for phrase in required:
            self.assertIn(phrase, article)

        self.assertNotIn("車で避難すべき", article)
        self.assertNotIn("海から1km", article)
        self.assertNotIn("標高10m以上なら安全", article)

    def test_b041_preserves_warning_advisory_distinction(self):
        article = (ROOT / "content" / "articles" / "B041_tsunami_evacuation.md").read_text(encoding="utf-8")
        self.assertIn("大津波警報・津波警報", article)
        self.assertIn("海の中にいる人はただちに海から上がり、海岸から離れる", article)
        self.assertIn("注意報・警報の発表内容を待たず", article)

    def test_b041_preview_keeps_emergency_copy_and_japanese_image(self):
        preview = (ROOT / "preview" / "article_b041.html").read_text(encoding="utf-8")
        self.assertIn("津波警報等を待たず高い安全な場所へ避難", preview)
        self.assertIn("徒歩が原則", preview)
        self.assertIn("津波警報・注意報が解除されるまでは", preview)
        self.assertIn("Sign%20of%20Route%20for%20Tsunami%20Evacuation%20Building%20in%20Japan.jpg", preview)
        self.assertIn("CC BY-SA 4.0", preview)
        self.assertNotIn("海から1km", preview)
        self.assertNotIn("標高10m以上なら安全", preview)

    def test_b041_has_evidence_and_navigation(self):
        for path in [
            ROOT / "docs" / "research" / "B041_TSUNAMI_EVACUATION_BRIEF.md",
            ROOT / "docs" / "research" / "B041_SOURCES.md",
            ROOT / "docs" / "research" / "B041_IMAGES.md",
            ROOT / "docs" / "reviews" / "B041_CHECKLIST.md",
            ROOT / "preview" / "article_b041.html",
        ]:
            self.assertTrue(path.exists(), path)

        category = (ROOT / "preview" / "category_earthquake.html").read_text(encoding="utf-8")
        b007 = (ROOT / "content" / "articles" / "B007_earthquake_preparedness_basics.md").read_text(encoding="utf-8")
        b039 = (ROOT / "content" / "articles" / "B039_earthquake_stay_home_or_shelter.md").read_text(encoding="utf-8")
        self.assertIn('data-article-id="B041"', category)
        self.assertIn("article_b041.html", b007)
        self.assertIn("article_b041.html", b039)


if __name__ == "__main__":
    unittest.main()
