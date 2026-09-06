# Created: 2026-09-05
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class KeywordBatchSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = json.loads((ROOT / "data" / "content_registry.json").read_text(encoding="utf-8"))
        cls.by_id = {article["article_id"]: article for article in registry["articles"]}

    def text(self, article_id):
        return (ROOT / self.by_id[article_id]["source_path"]).read_text(encoding="utf-8")

    def preview_text(self, article_id):
        return (ROOT / self.by_id[article_id]["preview_path"]).read_text(encoding="utf-8")

    def test_batch_is_registered_and_publishable(self):
        for article_id in ("B044", "B045", "B046", "B047"):
            article = self.by_id[article_id]
            self.assertEqual("READY_TO_PUBLISH", article["status"])
            self.assertEqual("APPROVED", article["manual_review_status"])
            self.assertEqual([], article["publish_blockers"])

    def test_b044_vehicle_overnight_boundaries(self):
        text = self.text("B044")
        self.assertIn("車の中だから安全", text)
        self.assertIn("窓を少し開けるだけでは危険を防げない", text)
        self.assertIn("支援情報から孤立しない", text)

    def test_b045_refrigerator_food_boundaries(self):
        text = self.text("B045")
        self.assertIn("○時間までなら安全", text)
        self.assertIn("味見だけで", text)
        self.assertIn("必要以上に開けない", text)
        self.assertNotIn("4時間までなら安全", text)

    def test_b046_window_tape_boundaries(self):
        text = self.text("B046")
        self.assertIn("養生テープだけを台風の窓対策にしない", text)
        self.assertIn("割れなくなると考えない", text)
        self.assertIn("強風中に外側から補修", text)

    def test_b047_heatstroke_boundaries(self):
        required_content = (
            "自力で水が飲めない、意識がない場合",
            "屋内、車庫、換気が不十分な場所で発電機を使わない",
            "モバイル扇風機や保冷剤があるから長時間自宅で大丈夫",
            "停電前に準備しておくこと",
            "高齢者・乳幼児・持病のある人を優先して確認した",
            "article_b004.html",
            "article_b028.html",
            "article_b044.html",
        )
        for target in (self.text("B047"), self.preview_text("B047")):
            for phrase in required_content:
                self.assertIn(phrase, target)

    def test_parent_and_category_links_exist(self):
        self.assertIn("article_b044.html", (ROOT / "preview/category_vehicle.html").read_text(encoding="utf-8"))
        outage = (ROOT / "preview/category_outage.html").read_text(encoding="utf-8")
        self.assertIn("article_b045.html", outage)
        self.assertIn("article_b047.html", outage)
        self.assertIn("article_b046.html", (ROOT / "preview/category_typhoon.html").read_text(encoding="utf-8"))
        self.assertIn("article_b044.html", (ROOT / "preview/article_b029.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
