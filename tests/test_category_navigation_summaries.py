# Created: 2026-09-07 23:40 JST / Updated: 2026-09-07
import re
import subprocess
import sys
import unittest
from pathlib import Path

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


class CategoryNavigationSummaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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

    def test_region_link_is_static_and_unique_in_navigation(self):
        earthquake_articles = sorted(
            page
            for page in (PUBLIC / "earthquake").glob("*.html")
            if page.name != "index.html"
        )
        self.assertTrue(earthquake_articles)

        pages = [
            PUBLIC / "index.html",
            PUBLIC / "guide" / "index.html",
            earthquake_articles[0],
            PUBLIC / "region" / "index.html",
            PUBLIC / "region" / "miyagi" / "earthquake-tsunami-history.html",
        ]
        for page in pages:
            self.assertTrue(page.exists(), page)
            html = page.read_text(encoding="utf-8")
            nav_match = re.search(
                r'<nav\b[^>]*\bclass=["\'][^"\']*\bsite-nav\b[^"\']*["\'][^>]*>'
                r'(.*?)</nav>',
                html,
                flags=re.IGNORECASE | re.DOTALL,
            )
            self.assertIsNotNone(nav_match, page)
            nav = nav_match.group(1)
            self.assertEqual(1, len(re.findall(r'>\s*地域別\s*</a>', nav)), page)
            self.assertIn("region/index.html", nav, page)

    def test_category_article_summaries_are_in_static_html(self):
        checked_pages = 0
        for page in sorted(PUBLIC.glob("*/index.html")):
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

        self.assertGreaterEqual(checked_pages, 5)

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
