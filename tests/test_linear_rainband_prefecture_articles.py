# Created: 2026-09-21 JST
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
SCRIPTS = ROOT / "scripts"
for path in (SRC, SCRIPTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from bousai_blog.registry import load_registry
from audit_article_content_metrics import audit
from enhance_linear_rainband_feature import enhance_feature_page


class LinearRainbandPrefectureBatch1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = load_registry(ROOT / "data" / "content_registry.json")
        cls.by_id = {a["article_id"]: a for a in registry["articles"]}
        cls.metrics = {m.article_id: m for m in audit()}

    def test_registry_paths_and_parents(self):
        expected = {
            "B082": ("B073", "special/linear-rainband/prefecture/kagoshima.html"),
            "B083": ("B073", "special/linear-rainband/prefecture/miyazaki.html"),
            "B084": ("B073", "special/linear-rainband/prefecture/kumamoto.html"),
            "B085": ("B073", "special/linear-rainband/prefecture/nagasaki.html"),
            "B086": ("B073", "special/linear-rainband/prefecture/oita.html"),
        }
        for article_id, (parent, public_path) in expected.items():
            self.assertIn(article_id, self.by_id)
            article = self.by_id[article_id]
            self.assertEqual(parent, article["parent_article_id"])
            self.assertEqual(public_path, article["planned_public_path"])
            self.assertEqual("READY_TO_PUBLISH", article["status"])

    def test_all_articles_meet_detail_length_rule(self):
        for article_id in ("B082", "B083", "B084", "B085", "B086"):
            metric = self.metrics[article_id]
            self.assertGreaterEqual(metric.body_char_count, 2500, article_id)
            self.assertEqual("PASS", metric.length_status)
            self.assertEqual(
                metric.body_char_count,
                self.by_id[article_id]["body_char_count_approx"],
                article_id,
            )

    def test_history_and_evacuation_are_not_generic_placeholders(self):
        markers = {
            "B082": ("1993", "薩摩", "指定緊急避難場所"),
            "B083": ("2024", "2025", "河川水位"),
            "B084": ("2012", "2020", "球磨川"),
            "B085": ("1982", "2023", "指定緊急避難場所"),
            "B086": ("2017", "2023", "雨量・水位"),
        }
        for article_id, required in markers.items():
            source_path = ROOT / self.by_id[article_id]["source_path"]
            text = source_path.read_text(encoding="utf-8")
            for marker in required:
                self.assertIn(marker, text, f"{article_id}: {marker}")
            self.assertIn("キキクル", text, article_id)
            self.assertIn("避難", text, article_id)
            self.assertIn("公的情報・参考資料", text, article_id)

    def test_feature_navigation_and_breadcrumb_are_applied(self):
        for article_id in ("B082", "B083", "B084", "B085", "B086"):
            preview = ROOT / self.by_id[article_id]["preview_path"]
            html = preview.read_text(encoding="utf-8")
            enhanced = enhance_feature_page(html, article_id)
            self.assertIn('class="feature-region-nav"', enhanced, article_id)
            self.assertIn("線状降水帯特集", enhanced, article_id)
            self.assertIn("地域別", enhanced, article_id)
            self.assertIn('class="breadcrumb"', enhanced, article_id)

    def test_preview_is_noindex_until_production_build(self):
        for article_id in ("B082", "B083", "B084", "B085", "B086"):
            preview = ROOT / self.by_id[article_id]["preview_path"]
            html = preview.read_text(encoding="utf-8").lower()
            self.assertIn('name="robots" content="noindex"', html, article_id)


if __name__ == "__main__":
    unittest.main()
