# Created: 2026-09-15 JST
"""Regression checks for the second regional linear-rainband article batch."""

from pathlib import Path
import unittest

from bousai_blog.registry import load_registry


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "content_registry.json"


class LinearRainbandRegionalArticleBatch2Tests(unittest.TestCase):
    def setUp(self):
        registry = load_registry(REGISTRY)
        self.by_id = {article["article_id"]: article for article in registry["articles"]}

    def test_batch_is_registered_as_b070_children(self):
        expected = {
            "B075": "special/linear-rainband/chugoku.html",
            "B076": "special/linear-rainband/shikoku.html",
            "B077": "special/linear-rainband/tokai.html",
        }
        for article_id, public_path in expected.items():
            self.assertIn(article_id, self.by_id)
            article = self.by_id[article_id]
            self.assertEqual("B070", article["parent_article_id"])
            self.assertEqual(public_path, article["planned_public_path"])
            self.assertEqual("READY_TO_PUBLISH", article["status"])
            self.assertEqual([], article["publish_blockers"])

    def test_chugoku_has_region_specific_evidence_and_boundary(self):
        text = (ROOT / "content/articles/B075_linear_rainband_chugoku.md").read_text(encoding="utf-8")
        for marker in ("2014年広島豪雨", "2025年山口", "512.0mm", "九州北部地方（山口県を含む）"):
            self.assertIn(marker, text)
        self.assertIn("鳥取・島根・岡山を「少ない地域」と決めることはできません", text)

    def test_shikoku_has_region_specific_evidence_and_boundary(self):
        text = (ROOT / "content/articles/B076_linear_rainband_shikoku.md").read_text(encoding="utf-8")
        for marker in ("四国の南東斜面", "三崎432.5mm", "佐喜浜420.5mm", "徳島県南部"):
            self.assertIn(marker, text)
        self.assertIn("高知・徳島・愛媛・香川を一括りにしない", text)

    def test_tokai_has_region_specific_evidence_and_boundary(self):
        text = (ROOT / "content/articles/B077_linear_rainband_tokai.md").read_text(encoding="utf-8")
        for marker in ("三重、愛知、静岡", "500mmを超え", "1時間127.0mm", "静岡県伊豆"):
            self.assertIn(marker, text)
        self.assertIn("静岡・愛知・岐阜・三重を一括りにしない", text)

    def test_b070_links_all_five_regional_articles(self):
        source = (ROOT / "content/articles/B070_linear_rainband_regions.md").read_text(encoding="utf-8")
        preview = (ROOT / "preview/article_b070.html").read_text(encoding="utf-8")
        for public_path, preview_name in (
            ("special/linear-rainband/kyushu.html", "article_b073.html"),
            ("special/linear-rainband/kanto-koshin.html", "article_b074.html"),
            ("special/linear-rainband/chugoku.html", "article_b075.html"),
            ("special/linear-rainband/shikoku.html", "article_b076.html"),
            ("special/linear-rainband/tokai.html", "article_b077.html"),
        ):
            self.assertIn(public_path, source)
            self.assertIn(f'href="{preview_name}"', preview)

    def test_batch_keeps_current_safety_boundary(self):
        for article_id, filename in (
            ("B075", "B075_linear_rainband_chugoku.md"),
            ("B076", "B076_linear_rainband_shikoku.md"),
            ("B077", "B077_linear_rainband_tokai.md"),
        ):
            text = (ROOT / "content/articles" / filename).read_text(encoding="utf-8")
            self.assertIn("半日前", text, article_id)
            self.assertIn("直前予測", text, article_id)
            self.assertIn("発生情報", text, article_id)
            self.assertIn("キキクル", text, article_id)
            self.assertIn("自治体", text, article_id)

        self.assertIn("発生情報が出てから初めて避難を考えるものではありません", (ROOT / "content/articles/B075_linear_rainband_chugoku.md").read_text(encoding="utf-8"))
        self.assertIn("発生情報まで待って避難判断を始めません", (ROOT / "content/articles/B076_linear_rainband_shikoku.md").read_text(encoding="utf-8"))
        self.assertIn("発生情報が出るまで避難を待つものではありません", (ROOT / "content/articles/B077_linear_rainband_tokai.md").read_text(encoding="utf-8"))

    def test_new_previews_are_noindex_only_before_public_build(self):
        for article_id in ("B075", "B076", "B077"):
            article = self.by_id[article_id]
            preview = (ROOT / article["preview_path"]).read_text(encoding="utf-8").lower()
            self.assertIn('name="robots" content="noindex"', preview)
            self.assertTrue(article["planned_public_path"])


if __name__ == "__main__":
    unittest.main()
