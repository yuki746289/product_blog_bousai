import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class B038StrandedCommuterTests(unittest.TestCase):
    def setUp(self):
        self.article = (ROOT / "content" / "articles" / "B038_earthquake_stranded_commuter.md").read_text(encoding="utf-8")
        self.preview = (ROOT / "preview" / "article_b038.html").read_text(encoding="utf-8")
        self.sources = (ROOT / "docs" / "research" / "B038_SOURCES.md").read_text(encoding="utf-8")
        self.category = (ROOT / "preview" / "category_earthquake.html").read_text(encoding="utf-8")
        self.parent = (ROOT / "content" / "articles" / "B007_earthquake_preparedness_basics.md").read_text(encoding="utf-8")

    def test_core_safety_message_is_preserved(self):
        for text in (self.article, self.preview):
            with self.subTest(target="article" if text is self.article else "preview"):
                self.assertIn("むやみに移動", text)
                self.assertIn("津波", text)
                self.assertIn("一時滞在施設", text)
                self.assertIn("災害時帰宅支援ステーション", text)
                self.assertIn("72時間", text)
                self.assertIn("分散帰宅", text)

        self.assertIn("全国一律の帰宅禁止時間でも", self.preview)
        self.assertIn("4日目以降でなければ帰宅できない", self.preview)
        self.assertIn("○km以内なら安全に歩ける", self.preview)

    def test_72_hour_guidance_keeps_required_qualification(self):
        self.assertIn("全国一律の絶対待機時間にしない", (ROOT / "docs" / "reviews" / "B038_CHECKLIST.md").read_text(encoding="utf-8"))
        self.assertIn("4日目以降でなければ帰宅させてはならない", self.sources)
        self.assertIn("72時間が経過しただけで帰宅経路が安全になる保証もない", self.sources)

    def test_registry_and_navigation_include_b038(self):
        registry = json.loads((ROOT / "data" / "content_registry.json").read_text(encoding="utf-8"))
        matches = [a for a in registry["articles"] if a.get("article_id") == "B038"]
        self.assertEqual(1, len(matches))
        self.assertEqual("earthquake/earthquake-stranded-commuter.html", matches[0]["planned_public_path"])
        self.assertEqual("READY_TO_PUBLISH", matches[0]["status"])
        self.assertIn('data-article-id="B038"', self.category)
        self.assertIn("article_b038.html", self.parent)

    def test_article_uses_current_primary_sources(self):
        self.assertIn("令和8年1月", self.sources)
        self.assertIn("令和8年版 防災白書", self.sources)
        self.assertIn("https://www.bousai.go.jp/jishin/kitakukonnan/", self.sources)
        self.assertIn("https://www.bousai.go.jp/kaigirep/hakusho/r08/", self.sources)


if __name__ == "__main__":
    unittest.main()
