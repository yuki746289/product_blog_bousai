# Created: 2026-09-09 19:02 JST
"""Regression tests for visible and structured article breadcrumbs."""

import re
import unittest
from pathlib import Path

from scripts import sync_previews_core as _core
from scripts.article_metadata import CATEGORY_BREADCRUMBS
from scripts.build_public import STATIC_HTML_MAP
from scripts.sync_previews_from_markdown import (
    ALL_ARTICLE_IDS,
    CATEGORY_PREVIEW_BREADCRUMBS,
)

ROOT = Path(__file__).resolve().parents[1]
BREADCRUMB_RE = re.compile(
    r'<nav\s+class=["\']breadcrumb["\'][^>]*>(?P<body>.*?)</nav>',
    re.IGNORECASE | re.DOTALL,
)


class ArticleBreadcrumbContractTests(unittest.TestCase):
    def setUp(self):
        self.registry = _core.load_registry(_core.REGISTRY)
        self.by_id = {article["article_id"]: article for article in self.registry["articles"]}

    def test_all_sixty_articles_have_a_real_published_category_route(self):
        self.assertTrue(ALL_ARTICLE_IDS.issubset(self.by_id))
        for article_id in sorted(ALL_ARTICLE_IDS):
            article = self.by_id[article_id]
            category = article.get("category")
            with self.subTest(article_id=article_id, category=category):
                self.assertIn(category, CATEGORY_PREVIEW_BREADCRUMBS)
                self.assertIn(category, CATEGORY_BREADCRUMBS)

                visible_name, preview_category = CATEGORY_PREVIEW_BREADCRUMBS[category]
                structured_name, public_category = CATEGORY_BREADCRUMBS[category]
                self.assertEqual(visible_name, structured_name)
                self.assertIn(preview_category, STATIC_HTML_MAP)
                self.assertEqual(public_category, STATIC_HTML_MAP[preview_category])
                self.assertTrue((ROOT / "preview" / preview_category).exists())

    def test_all_sixty_visible_breadcrumbs_link_the_category(self):
        for article_id in sorted(ALL_ARTICLE_IDS):
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

    def test_outage_articles_use_the_existing_outage_category(self):
        for article_id in ("B003", "B004"):
            article = self.by_id[article_id]
            category_name, preview_category = CATEGORY_PREVIEW_BREADCRUMBS[article["category"]]
            self.assertEqual("停電・断水", category_name)
            self.assertEqual("category_outage.html", preview_category)
            self.assertEqual("outage/index.html", STATIC_HTML_MAP[preview_category])

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
