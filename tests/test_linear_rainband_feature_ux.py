# Created: 2026-09-15 09:20 JST
import unittest
from pathlib import Path

from scripts.enhance_linear_rainband_feature import (
    enhance_category_flood,
    enhance_category_region,
    enhance_feature_page,
)

ROOT = Path(__file__).resolve().parents[1]


class LinearRainbandFeatureUxTests(unittest.TestCase):
    def test_b067_source_is_broad_pillar_and_not_fixed_to_five_pages(self):
        text = (ROOT / "content/articles/B067_linear_rainband_feature.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "# 線状降水帯とは？過去事例・発生数・多い地域・雨量記録をデータで見る",
            text,
        )
        self.assertNotIn("この特集の5ページ", text)
        for slug in (
            "kyushu.html",
            "kanto-koshin.html",
            "chugoku.html",
            "shikoku.html",
            "tokai.html",
        ):
            self.assertIn(slug, text)

    def test_core_child_breadcrumb_links_to_feature_top(self):
        sample = (
            '<html><head></head><body><nav class="breadcrumb">old</nav>'
            '<nav class="feature-nav"><a href="old.html">old</a></nav></body></html>'
        )
        actual = enhance_feature_page(sample, "B068")
        self.assertIn('<a href="article_b067.html">線状降水帯特集</a>', actual)
        self.assertIn('aria-label="線状降水帯特集の主要テーマ"', actual)
        self.assertIn('href="article_b068.html" aria-current="page"', actual)

    def test_regional_child_has_two_level_feature_breadcrumb(self):
        sample = (
            '<html><head></head><body><nav class="breadcrumb">old</nav>'
            '<nav class="feature-nav"><a href="old.html">old</a></nav></body></html>'
        )
        actual = enhance_feature_page(sample, "B075")
        self.assertIn('<a href="article_b067.html">線状降水帯特集</a>', actual)
        self.assertIn('<a href="article_b070.html">地域別</a>', actual)
        self.assertIn('aria-label="線状降水帯の地域別記事"', actual)
        self.assertIn('href="article_b075.html" aria-current="page"', actual)

    def test_b070_separates_core_nav_from_region_grid(self):
        sample = (
            '<html><head></head><body><nav class="breadcrumb">old</nav>'
            '<nav class="feature-nav"><a href="old.html">old</a></nav><h2>本文</h2></body></html>'
        )
        actual = enhance_feature_page(sample, "B070")
        self.assertIn('id="linear-rainband-region-panel"', actual)
        self.assertIn('href="article_b070.html" aria-current="page"', actual)
        self.assertIn('class="feature-region-card" href="article_b073.html"', actual)
        core_nav = actual.split('aria-label="線状降水帯特集の主要テーマ"', 1)[1].split(
            "</nav>", 1
        )[0]
        self.assertNotIn("article_b073.html", core_nav)

    def test_feature_nav_is_reinserted_after_markdown_body_sync(self):
        sample = (
            '<html><head></head><body><nav class="breadcrumb">old</nav>'
            '<article><header><h1>old</h1><p class="article-lead">old</p></header>'
            '<div class="article-body"><h2>本文</h2><p>本文です。</p></div>'
            '</article></body></html>'
        )

        pillar = enhance_feature_page(sample, "B067")
        self.assertIn('aria-label="線状降水帯特集の主要テーマ"', pillar)
        self.assertIn('id="linear-rainband-region-panel"', pillar)
        self.assertIn("地域から線状降水帯を見る", pillar)

        regional = enhance_feature_page(sample, "B075")
        self.assertIn('aria-label="線状降水帯の地域別記事"', regional)
        self.assertIn('href="article_b075.html" aria-current="page"', regional)

        self.assertEqual(pillar, enhance_feature_page(pillar, "B067"))
        self.assertEqual(regional, enhance_feature_page(regional, "B075"))

    def test_b067_preview_metadata_uses_broad_search_intent(self):
        sample = (
            '<html><head><meta name="description" content="old"><title>old</title></head>'
            '<body><nav class="breadcrumb">old</nav><h1>old</h1>'
            '<p class="article-lead">old</p><nav class="feature-nav"></nav>'
            '<h2>線状降水帯の主な事例とデータ</h2></body></html>'
        )
        actual = enhance_feature_page(sample, "B067")
        self.assertIn("<title>線状降水帯とは？", actual)
        self.assertIn("<h1>線状降水帯とは？", actual)
        self.assertIn("九州・関東甲信・中国・四国・東海", actual)
        self.assertIn("線状降水帯の主な事例とデータ", actual)
        self.assertIn('id="linear-rainband-region-panel"', actual)

    def test_category_hubs_gain_feature_entry_points(self):
        sample = (
            '<html><head></head><body><header class="category-hero">'
            '<h1>カテゴリ</h1><p>現在は8地域・8記事を掲載しています。</p>'
            '</header><section class="category-section"></section></body></html>'
        )
        flood = enhance_category_flood(sample)
        self.assertIn("注目特集：線状降水帯", flood)
        self.assertIn('href="article_b067.html"', flood)
        self.assertIn('href="article_b070.html"', flood)

        region = enhance_category_region(sample)
        self.assertIn("線状降水帯を地域から見る", region)
        self.assertIn("災害史記事は現在8地域・8記事", region)
        for number in range(73, 78):
            self.assertIn(f'article_b{number:03d}.html', region)

    def test_transforms_are_idempotent(self):
        sample = (
            '<html><head></head><body><nav class="breadcrumb">old</nav>'
            '<nav class="feature-nav"><a href="old.html">old</a></nav></body></html>'
        )
        once = enhance_feature_page(sample, "B074")
        twice = enhance_feature_page(once, "B074")
        self.assertEqual(once, twice)


if __name__ == "__main__":
    unittest.main()
