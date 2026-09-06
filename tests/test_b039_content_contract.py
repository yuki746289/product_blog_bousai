# Created: 2026-09-04
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class B039ContentContractTest(unittest.TestCase):
    def test_b039_is_high_risk_reviewed_and_registered(self):
        registry = json.loads((ROOT / "data" / "content_registry.json").read_text(encoding="utf-8"))
        article = next(a for a in registry["articles"] if a.get("article_id") == "B039")
        self.assertEqual("high", article["risk_level"])
        self.assertTrue(article["manual_review_required"])
        self.assertEqual("APPROVED", article["manual_review_status"])
        self.assertEqual("PASS", article["review_checklist_status"])
        self.assertEqual("READY_TO_PUBLISH", article["status"])
        self.assertEqual("earthquake/earthquake-stay-home-or-shelter.html", article["planned_public_path"])

    def test_b039_keeps_core_safety_boundaries(self):
        article = (ROOT / "content" / "articles" / "B039_earthquake_stay_home_or_shelter.md").read_text(encoding="utf-8")
        required = [
            "危険があるなら避難。安全な自宅なら在宅避難も選べる",
            "在宅避難は「一度決めたら家を出ない」という意味ではありません。",
            "建物の安全性を専門的に判断する必要がある場合",
            "物資が自動的に届くわけではありません。",
            "指定緊急避難場所",
            "指定避難所",
            "福祉避難所等については自治体によって利用方法が異なります。",
        ]
        for phrase in required:
            self.assertIn(phrase, article)

    def test_b039_has_evidence_and_navigation(self):
        for path in [
            ROOT / "docs" / "research" / "B039_STAY_HOME_OR_SHELTER_BRIEF.md",
            ROOT / "docs" / "research" / "B039_SOURCES.md",
            ROOT / "docs" / "research" / "B039_IMAGES.md",
            ROOT / "docs" / "reviews" / "B039_CHECKLIST.md",
            ROOT / "preview" / "article_b039.html",
        ]:
            self.assertTrue(path.exists(), path)

        category = (ROOT / "preview" / "category_earthquake.html").read_text(encoding="utf-8")
        b007 = (ROOT / "content" / "articles" / "B007_earthquake_preparedness_basics.md").read_text(encoding="utf-8")
        b024 = (ROOT / "content" / "articles" / "B024_earthquake_blackout_water_outage.md").read_text(encoding="utf-8")
        self.assertIn('data-article-id="B039"', category)
        self.assertIn("article_b039.html", b007)
        self.assertIn("article_b039.html", b024)


if __name__ == "__main__":
    unittest.main()
