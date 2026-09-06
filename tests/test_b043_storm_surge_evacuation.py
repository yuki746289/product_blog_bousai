# Created: 2026-09-05
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class B043StormSurgeEvacuationTests(unittest.TestCase):
    def test_b043_is_high_risk_reviewed_and_registered(self):
        registry = json.loads((ROOT / "data" / "content_registry.json").read_text(encoding="utf-8"))
        article = next(a for a in registry["articles"] if a.get("article_id") == "B043")
        self.assertEqual("high", article["risk_level"])
        self.assertTrue(article["manual_review_required"])
        self.assertEqual("APPROVED", article["manual_review_status"])
        self.assertEqual("PASS", article["review_checklist_status"])
        self.assertEqual("typhoon/storm-surge-evacuation.html", article["planned_public_path"])

    def test_b043_keeps_core_safety_boundaries(self):
        article = (ROOT / "content" / "articles" / "B043_storm_surge_evacuation.md").read_text(encoding="utf-8")
        required = [
            "暴風が吹き始める前に危険な場所からの避難を完了する",
            "高潮は津波とは別の現象",
            "満潮時刻だけを見て判断しない",
            "レベル5は避難開始を待つ段階ではない",
            "海岸・防波堤・河口へ様子を見に行かない",
            "車避難は「台風だから車が安全」とは限らない",
        ]
        for phrase in required:
            self.assertIn(phrase, article)
        self.assertNotIn("海岸から1km", article)
        self.assertNotIn("標高10m以上なら安全", article)

    def test_b043_has_evidence_and_preview(self):
        for path in [
            ROOT / "docs" / "research" / "B043_STORM_SURGE_BRIEF.md",
            ROOT / "docs" / "research" / "B043_SOURCES.md",
            ROOT / "docs" / "research" / "B043_IMAGES.md",
            ROOT / "docs" / "reviews" / "B043_CHECKLIST.md",
            ROOT / "preview" / "article_b043.html",
        ]:
            self.assertTrue(path.exists(), path)


if __name__ == "__main__":
    unittest.main()
