# Created: 2026-09-21 JST
import unittest
from pathlib import Path

from bousai_blog.registry import load_registry
from scripts.enhance_linear_rainband_feature import region_panel

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "content_registry.json"


class LinearRainbandPrefectureBatch1Tests(unittest.TestCase):
    def setUp(self):
        registry = load_registry(REGISTRY)
        self.by_id = {item["article_id"]: item for item in registry["articles"]}

    def test_batch_is_registered(self):
        expected = {
            "B082": "special/linear-rainband/prefecture/kagoshima.html",
            "B083": "special/linear-rainband/prefecture/miyazaki.html",
            "B084": "special/linear-rainband/prefecture/kumamoto.html",
            "B085": "special/linear-rainband/prefecture/kochi.html",
            "B086": "special/linear-rainband/prefecture/wakayama.html",
        }
        for article_id, public_path in expected.items():
            self.assertIn(article_id, self.by_id)
            self.assertEqual(public_path, self.by_id[article_id]["planned_public_path"])
            self.assertEqual("READY_TO_PUBLISH", self.by_id[article_id]["status"])

    def test_sources_are_prefecture_specific(self):
        checks = {
            "B082_linear_rainband_kagoshima.md": ("鹿児島県", "2025年8月8日", "災害種別"),
            "B083_linear_rainband_miyazaki.md": ("宮崎県", "2024年10月22日", "避難"),
            "B084_linear_rainband_kumamoto.md": ("熊本県", "球磨川", "防災情報くまもと"),
            "B085_linear_rainband_kochi.md": ("高知県", "三崎432.5mm", "高知県防災アプリ"),
            "B086_linear_rainband_wakayama.md": ("和歌山県", "2011年", "安全レベル"),
        }
        for filename, markers in checks.items():
            text = (ROOT / "content" / "articles" / filename).read_text(encoding="utf-8")
            for marker in markers:
                self.assertIn(marker, text, filename)
            self.assertIn("関連ページ", text)
            self.assertIn("公的情報", text)

    def test_all_previews_exist_and_are_preview_noindex(self):
        for number in range(82, 87):
            path = ROOT / "preview" / f"article_b{number:03d}.html"
            self.assertTrue(path.exists(), str(path))
            html = path.read_text(encoding="utf-8").lower()
            self.assertIn('name="robots" content="noindex"', html)

    def test_feature_panel_links_prefecture_pages(self):
        html = region_panel()
        for number in range(82, 87):
            self.assertIn(f'article_b{number:03d}.html', html)


if __name__ == "__main__":
    unittest.main()
