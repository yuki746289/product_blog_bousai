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
from enhance_linear_rainband_feature import enhance_feature_page, region_panel


class LinearRainbandPrefectureBatch2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = load_registry(ROOT / "data" / "content_registry.json")
        cls.by_id = {a["article_id"]: a for a in registry["articles"]}
        cls.metrics = {m.article_id: m for m in audit()}

    def test_registry_paths_and_parents(self):
        expected = {
            "B087": ("B076", "special/linear-rainband/prefecture/kochi.html"),
            "B088": ("B070", "special/linear-rainband/prefecture/wakayama.html"),
            "B089": ("B077", "special/linear-rainband/prefecture/mie.html"),
            "B090": ("B077", "special/linear-rainband/prefecture/shizuoka.html"),
            "B091": ("B074", "special/linear-rainband/prefecture/chiba.html"),
        }
        for article_id, (parent, public_path) in expected.items():
            self.assertIn(article_id, self.by_id)
            article = self.by_id[article_id]
            self.assertEqual(parent, article["parent_article_id"])
            self.assertEqual(public_path, article["planned_public_path"])
            self.assertEqual("READY_TO_PUBLISH", article["status"])

    def test_all_articles_meet_detail_length_rule(self):
        for article_id in ("B087", "B088", "B089", "B090", "B091"):
            metric = self.metrics[article_id]
            self.assertGreaterEqual(metric.body_char_count, 2500, article_id)
            self.assertEqual("PASS", metric.length_status)
            self.assertEqual(
                metric.body_char_count,
                self.by_id[article_id]["body_char_count_approx"],
                article_id,
            )

    def test_prefecture_specific_history_and_safety(self):
        markers = {
            "B087": ("2022", "2023", "高知県防災アプリ"),
            "B088": ("2011", "2023", "安全レベル"),
            "B089": ("2023", "2024", "伊勢志摩"),
            "B090": ("2022", "2025", "突風"),
            "B091": ("2019", "2026", "令和8年8月千葉豪雨"),
        }
        for article_id, required in markers.items():
            text = (ROOT / self.by_id[article_id]["source_path"]).read_text(encoding="utf-8")
            for marker in required:
                self.assertIn(marker, text, f"{article_id}: {marker}")
            self.assertIn("避難", text, article_id)
            self.assertIn("キキクル", text, article_id)
            self.assertIn("公的情報・参考資料", text, article_id)
            self.assertNotIn("\\n", text, article_id)

    def test_feature_panel_and_breadcrumb_support_batch2(self):
        panel = region_panel()
        for article_id in ("B087", "B088", "B089", "B090", "B091"):
            article = self.by_id[article_id]
            preview_name = Path(article["preview_path"]).name
            self.assertIn(preview_name, panel)
            html = (ROOT / article["preview_path"]).read_text(encoding="utf-8")
            enhanced = enhance_feature_page(html, article_id)
            self.assertIn('class="feature-region-nav"', enhanced, article_id)
            self.assertIn("線状降水帯特集", enhanced, article_id)
            self.assertIn("地域別", enhanced, article_id)
            self.assertIn('class="breadcrumb"', enhanced, article_id)

    def test_previews_are_noindex_before_public_build(self):
        for article_id in ("B087", "B088", "B089", "B090", "B091"):
            html = (ROOT / self.by_id[article_id]["preview_path"]).read_text(encoding="utf-8").lower()
            self.assertIn('name="robots" content="noindex"', html, article_id)


if __name__ == "__main__":
    unittest.main()
