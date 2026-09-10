# Created: 2026-09-07 23:40 JST
# Updated: 2026-09-10 09:04 JST
import re
import subprocess
import sys
import unittest
from html import unescape
from pathlib import Path

from scripts.sync_previews_from_markdown import (
    apply_category_page_breadcrumbs,
    apply_homepage_typhoon_flood_card,
    apply_merged_category_links,
    apply_site_navigation,
)

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

CATEGORY_PAGE_RE = re.compile(
    r'<main\b(?=[^>]*\bclass=["\'][^"\']*\bcategory-page\b[^"\']*["\'])[^>]*>',
    re.IGNORECASE,
)
CATEGORY_LINK_RE = re.compile(
    r'<a\b[^>]*\bclass=["\'][^"\']*\bcategory-article-link\b[^"\']*["\'][^>]*'
    r'\bdata-article-id=["\']B\d{3}["\'][^>]*>',
    re.IGNORECASE,
)
PRIMARY_NAV_LABELS = [
    "防災入門",
    "台風・水害",
    "地震",
    "停電・断水",
    "被災後・復旧",
    "車と災害",
    "住宅と災害",
    "保険・お金",
    "防災グッズ",
    "地域別",
    "Q&A",
]


def extract_nav(html: str) -> str:
    nav_match = re.search(
        r'<nav\b[^>]*\bclass=["\'][^"\']*\bsite-nav\b[^"\']*["\'][^>]*>'
        r'(.*?)</nav>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return nav_match.group(1) if nav_match else ""


def extract_nav_labels(nav: str) -> list[str]:
    return [
        unescape(re.sub(r"<[^>]+>", "", body).strip())
        for body in re.findall(r"<a\b[^>]*>(.*?)</a>", nav, flags=re.I | re.S)
    ]


class CategoryNavigationSummaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The CI workflow already performs the full article synchronization.
        # For isolated test execution, only apply navigation transforms that are
        # idempotent and do not consume one-time article replacement markers.
        apply_homepage_typhoon_flood_card()
        apply_merged_category_links()
        apply_site_navigation()
        apply_category_page_breadcrumbs()
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_public.py")],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "finalize_search_metadata.py")],
            cwd=ROOT,
            check=True,
        )

    def test_primary_navigation_is_grouped_and_direct(self):
        earthquake_articles = sorted(
            page
            for page in (PUBLIC / "earthquake").glob("*.html")
            if page.name != "index.html"
        )
        self.assertTrue(earthquake_articles)

        pages = [
            PUBLIC / "index.html",
            PUBLIC / "guide" / "index.html",
            PUBLIC / "flood" / "index.html",
            earthquake_articles[0],
            PUBLIC / "outage" / "index.html",
            PUBLIC / "post-disaster" / "index.html",
            PUBLIC / "region" / "index.html",
            PUBLIC / "region" / "miyagi" / "earthquake-tsunami-history.html",
        ]
        for page in pages:
            self.assertTrue(page.exists(), page)
            html = page.read_text(encoding="utf-8")
            nav = extract_nav(html)
            self.assertTrue(nav, page)
            self.assertEqual(PRIMARY_NAV_LABELS, extract_nav_labels(nav), page)
            self.assertEqual(2, nav.count('class="site-nav__divider"'), page)
            self.assertEqual(1, len(re.findall(r'>\s*地域別\s*</a>', nav)), page)
            self.assertNotIn('href="typhoon/index.html"', nav, page)
            self.assertNotIn("災害・状況別", nav, page)
            self.assertNotIn("暮らし別", nav, page)

        homepage_nav = extract_nav((PUBLIC / "index.html").read_text(encoding="utf-8"))
        for href in [
            "guide/index.html",
            "flood/index.html",
            "earthquake/index.html",
            "outage/index.html",
            "post-disaster/index.html",
            "vehicle/index.html",
            "home/index.html",
            "insurance/index.html",
            "goods/index.html",
            "region/index.html",
            "qa.html",
        ]:
            self.assertIn(f'href="{href}"', homepage_nav)
        self.assertLess(homepage_nav.index("goods/index.html"), homepage_nav.index("region/index.html"))

    def test_combined_typhoon_flood_page_is_single_normal_entry(self):
        page = PUBLIC / "flood" / "index.html"
        html = page.read_text(encoding="utf-8")
        self.assertIn("<h1>台風・水害</h1>", html)
        ids = re.findall(r'data-article-id="(B\d{3})"', html)
        self.assertEqual(22, len(ids))
        self.assertEqual(22, len(set(ids)))
        self.assertIn("台風接近前・強風・高潮", html)
        self.assertIn("洪水・河川氾濫・土砂災害", html)

    def test_typhoon_articles_use_combined_structured_breadcrumb(self):
        page = PUBLIC / "typhoon" / "typhoon-preparation-checklist.html"
        self.assertTrue(page.exists())
        html = page.read_text(encoding="utf-8")
        self.assertIn("台風・水害", html)
        self.assertIn("../flood/index.html", html)
        self.assertRegex(html, r'"name":"台風・水害","item":"https://bousaikun\.ashigaru\.jp/flood/index\.html"')

    def test_category_article_summaries_are_in_static_html(self):
        checked_pages = 0
        for page in sorted(PUBLIC.rglob("index.html")):
            html = page.read_text(encoding="utf-8")
            if CATEGORY_PAGE_RE.search(html) is None:
                continue

            article_links = CATEGORY_LINK_RE.findall(html)
            if not article_links:
                continue

            checked_pages += 1
            summaries = re.findall(
                r'<span class="category-article-summary">([^<]+)</span>', html
            )
            self.assertEqual(len(article_links), len(summaries), page)
            self.assertIn('id="bousai-category-listing-styles"', html, page)
            for summary in summaries:
                text = re.sub(r"\s+", " ", summary).strip()
                self.assertTrue(text, page)
                self.assertLessEqual(len(text), 82, page)

        self.assertGreaterEqual(checked_pages, 7)

    def test_finalize_is_idempotent_for_category_enhancements(self):
        guide = PUBLIC / "guide" / "index.html"
        before = guide.read_text(encoding="utf-8")
        before_region_count = len(re.findall(r'>\s*地域別\s*</a>', before))
        before_summary_count = before.count('class="category-article-summary"')
        self.assertGreater(before_summary_count, 0)

        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "finalize_search_metadata.py")],
            cwd=ROOT,
            check=True,
        )

        after = guide.read_text(encoding="utf-8")
        self.assertEqual(before_region_count, len(re.findall(r'>\s*地域別\s*</a>', after)))
        self.assertEqual(before_summary_count, after.count('class="category-article-summary"'))
        self.assertEqual(1, after.count('id="bousai-category-listing-styles"'))


if __name__ == "__main__":
    unittest.main()
