# Created: 2026-09-14 JST
"""Regression checks for the regional linear-rainband article expansion."""

from pathlib import Path
import unittest

from bousai_blog.registry import load_registry


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "content_registry.json"


class LinearRainbandRegionalArticleTests(unittest.TestCase):
    def setUp(self):
        registry = load_registry(REGISTRY)
        self.by_id = {article["article_id"]: article for article in registry["articles"]}

    def test_kyushu_and_kanto_are_registered_as_b070_children(self):
        expected = {
            "B073": "special/linear-rainband/kyushu.html",
            "B074": "special/linear-rainband/kanto-koshin.html",
        }
        for article_id, public_path in expected.items():
            self.assertIn(article_id, self.by_id)
            article = self.by_id[article_id]
            self.assertEqual("B070", article["parent_article_id"])
            self.assertEqual(public_path, article["planned_public_path"])
            self.assertEqual("READY_TO_PUBLISH", article["status"])
            self.assertEqual([], article["publish_blockers"])

    def test_regional_sources_have_region_specific_evidence(self):
        kyushu = (ROOT / "content/articles/B073_linear_rainband_kyushu.md").read_text(
            encoding="utf-8"
        )
        kanto = (ROOT / "content/articles/B074_linear_rainband_kanto_koshin.md").read_text(
            encoding="utf-8"
        )

        for marker in ("2017年九州北部豪雨", "1時間129.5mm", "日降水量516.0mm"):
            self.assertIn(marker, kyushu)
        for marker in ("2015年関東・東北豪雨", "2026年千葉豪雨", "1時間115.0mm", "24時間367.0mm"):
            self.assertIn(marker, kanto)

        self.assertIn("九州北部・九州南部・奄美・沖縄を一括りにしない", kyushu)
        self.assertIn("「関東地方」と「関東甲信地方」は同じではない", kanto)

    def test_b070_is_the_regional_hub(self):
        hub = (ROOT / "content/articles/B070_linear_rainband_regions.md").read_text(
            encoding="utf-8"
        )
        preview = (ROOT / "preview/article_b070.html").read_text(encoding="utf-8")

        self.assertIn("special/linear-rainband/kyushu.html", hub)
        self.assertIn("special/linear-rainband/kanto-koshin.html", hub)
        self.assertIn('href="article_b073.html"', preview)
        self.assertIn('href="article_b074.html"', preview)

    def test_regional_articles_keep_current_safety_boundary(self):
        for path in (
            ROOT / "content/articles/B073_linear_rainband_kyushu.md",
            ROOT / "content/articles/B074_linear_rainband_kanto_koshin.md",
        ):
            text = path.read_text(encoding="utf-8")
            self.assertIn("半日前", text)
            self.assertIn("直前予測", text)
            self.assertIn("発生情報", text)
            self.assertIn("キキクル", text)
            self.assertIn("自治体", text)

        kyushu = (ROOT / "content/articles/B073_linear_rainband_kyushu.md").read_text(
            encoding="utf-8"
        )
        kanto = (ROOT / "content/articles/B074_linear_rainband_kanto_koshin.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("発生情報が出てから初めて避難を考えるものではありません", kyushu)
        self.assertIn("発生情報が出たら動く", kanto)

    def test_preview_noindex_is_only_a_preview_concern(self):
        for article_id in ("B073", "B074"):
            preview_path = ROOT / self.by_id[article_id]["preview_path"]
            text = preview_path.read_text(encoding="utf-8").lower()
            self.assertIn('name="robots" content="noindex"', text)

            # Production publication is controlled by the registry/build pipeline;
            # the public build removes preview noindex and is covered by the
            # existing all-public-HTML and live-sitemap indexability tests.
            self.assertTrue(self.by_id[article_id]["planned_public_path"])


if __name__ == "__main__":
    unittest.main()
