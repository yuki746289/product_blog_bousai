# Created: 2026-09-09 19:02 JST
# Updated: 2026-09-10 09:04 JST
"""Regression tests for visible and structured article breadcrumbs."""

import re
import unittest
from pathlib import Path

from scripts import sync_previews_core as _core
from scripts.article_metadata import CATEGORY_BREADCRUMBS, article_breadcrumb_items
from scripts.sync_previews_from_markdown import (
    BREADCRUMB_ARTICLE_IDS,
    CATEGORY_PREVIEW_BREADCRUMBS,
)

ROOT = Path(__file__).resolve().parents[1]
BREADCRUMB_RE = re.compile(
    r'<nav\s+class=["\']breadcrumb["\'][^>]*>(?P<body>.*?)</nav>',
    re.IGNORECASE | re.DOTALL,
)

# Public article-category destinations. Typhoon and flood intentionally share
# the same visible category route after the navigation merge.
CATEGORY_PREVIEW_TO_PUBLIC = {
    "category_guide.html": "guide/index.html",
    "category_evacuation.html": "evacuation/index.html",
    "category_outage.html": "outage/index.html",
    "category_flood.html": "flood/index.html",
    "category_earthquake.html": "earthquake/index.html",
    "category_vehicle.html": "vehicle/index.html",
    "category_insurance.html": "insurance/index.html",
    "category_home.html": "home/index.html",
    "category_post_disaster.html": "post-disaster/index.html",
    "category_goods.html": "goods/index.html",
}


class ArticleBreadcrumbContractTests(unittest.TestCase):
    def setUp(self):
        self.registry = _core.load_registry(_core.REGISTRY)
        self.by_id = {article["article_id"]: article for article in self.registry["articles"]}

    def test_all_articles_have_a_real_published_category_route(self):
        self.assertTrue(BREADCRUMB_ARTICLE_IDS.issubset(self.by_id))
        for article_id in sorted(BREADCRUMB_ARTICLE_IDS):
            article = self.by_id[article_id]
            category = article.get("category")
            with self.subTest(article_id=article_id, category=category):
                self.assertIn(category, CATEGORY_PREVIEW_BREADCRUMBS)
                self.assertIn(category, CATEGORY_BREADCRUMBS)

                visible_name, preview_category = CATEGORY_PREVIEW_BREADCRUMBS[category]
                structured_name, public_category = CATEGORY_BREADCRUMBS[category]
                self.assertEqual(visible_name, structured_name)
                self.assertIn(preview_category, CATEGORY_PREVIEW_TO_PUBLIC)
                self.assertEqual(public_category, CATEGORY_PREVIEW_TO_PUBLIC[preview_category])
                self.assertTrue((ROOT / "preview" / preview_category).exists())

    def test_all_visible_breadcrumbs_link_the_category(self):
        for article_id in sorted(BREADCRUMB_ARTICLE_IDS):
            article = self.by_id[article_id]
            category_name, preview_category = CATEGORY_PREVIEW_BREADCRUMBS[article["category"]]
            preview_path = ROOT / article["preview_path"]
            html = preview_path.read_text(encoding="utf-8")
            match = BREADCRUMB_RE.search(html)
            with self.subTest(article_id=article_id):
                self.assertIsNotNone(match, f"breadcrumb missing: {preview_path}")
                self.assertIn('aria-label="パンくずリスト"', match.group(0))
                self.assertIn('<a href="index.html">トップ</a>', match.group(0))
                self.assertIn(
                    f'<a href="{preview_category}">{category_name}</a>',
                    match.group(0),
                )

    def test_evacuation_articles_share_one_visible_category(self):
        for article_id in ("B033", "B034", "B035", "B061", "B062", "B065", "B066", "B078", "B079", "B080", "B081"):
            article = self.by_id[article_id]
            self.assertEqual("evacuation", article["category"])
            self.assertEqual(
                ("避難・避難生活", "category_evacuation.html"),
                CATEGORY_PREVIEW_BREADCRUMBS[article["category"]],
            )
            self.assertEqual(
                ("避難・避難生活", "evacuation/index.html"),
                CATEGORY_BREADCRUMBS[article["category"]],
            )

    def test_typhoon_and_flood_articles_share_one_visible_category(self):
        for internal_category in ("typhoon", "flood"):
            self.assertEqual(
                ("台風・水害", "category_flood.html"),
                CATEGORY_PREVIEW_BREADCRUMBS[internal_category],
            )
            self.assertEqual(
                ("台風・水害", "flood/index.html"),
                CATEGORY_BREADCRUMBS[internal_category],
            )

    def test_outage_articles_use_the_existing_outage_category(self):
        for article_id in ("B003", "B004"):
            article = self.by_id[article_id]
            category_name, preview_category = CATEGORY_PREVIEW_BREADCRUMBS[article["category"]]
            self.assertEqual("停電・断水", category_name)
            self.assertEqual("category_outage.html", preview_category)
            self.assertEqual("outage/index.html", CATEGORY_PREVIEW_TO_PUBLIC[preview_category])

    def test_structured_breadcrumbs_use_short_labels_and_special_hierarchies(self):
        config = {
            "public_base_url": "https://bousaikun.ashigaru.jp/",
            "site_name": "防災くらしガイド",
        }

        chiba = self.by_id["B091"]
        chiba_items = article_breadcrumb_items(
            chiba,
            chiba["planned_public_path"],
            config,
        )
        self.assertEqual(
            ["防災くらしガイド", "線状降水帯", "千葉県"],
            [item["name"] for item in chiba_items],
        )

        kanagawa = self.by_id["B098"]
        kanagawa_items = article_breadcrumb_items(
            kanagawa,
            kanagawa["planned_public_path"],
            config,
        )
        self.assertEqual(
            ["防災くらしガイド", "線状降水帯", "神奈川県"],
            [item["name"] for item in kanagawa_items],
        )

        osaka = self.by_id["B093"]
        osaka_items = article_breadcrumb_items(
            osaka,
            osaka["planned_public_path"],
            config,
        )
        self.assertEqual(
            ["防災くらしガイド", "地域別", "大阪府の大雨・都市型水害"],
            [item["name"] for item in osaka_items],
        )

        feature = self.by_id["B067"]
        feature_items = article_breadcrumb_items(
            feature,
            feature["planned_public_path"],
            config,
        )
        self.assertEqual(
            ["防災くらしガイド", "線状降水帯"],
            [item["name"] for item in feature_items],
        )

        normal = self.by_id["B008"]
        normal_items = article_breadcrumb_items(
            normal,
            normal["planned_public_path"],
            config,
        )
        self.assertEqual(
            ["防災くらしガイド", "車と災害", "車の冠水・水没"],
            [item["name"] for item in normal_items],
        )

    def test_future_prefecture_breadcrumb_name_is_derived_from_title(self):
        article = {
            "article_id": "B999",
            "title": "佐賀県の線状降水帯｜過去の発生履歴・直近事例を一覧で解説",
            "category": "flood",
        }
        items = article_breadcrumb_items(
            article,
            "special/linear-rainband/prefecture/saga.html",
            {
                "public_base_url": "https://bousaikun.ashigaru.jp/",
                "site_name": "防災くらしガイド",
            },
        )
        self.assertEqual(
            ["防災くらしガイド", "線状降水帯", "佐賀県"],
            [item["name"] for item in items],
        )

    def test_post_disaster_category_name_is_consistent(self):
        self.assertEqual(
            ("被災後・復旧", "category_post_disaster.html"),
            CATEGORY_PREVIEW_BREADCRUMBS["post-disaster"],
        )
        self.assertEqual(
            ("被災後・復旧", "post-disaster/index.html"),
            CATEGORY_BREADCRUMBS["post-disaster"],
        )


if __name__ == "__main__":
    unittest.main()
