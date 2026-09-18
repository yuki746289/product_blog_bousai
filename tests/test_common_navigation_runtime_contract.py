# Created: 2026-09-17 JST
"""Regression checks for production-only common navigation behavior.

The production builder rewrites category_region.html to index.html while building
/region/index.html. Runtime fallbacks must not interpret that rewritten self-link
as a missing region entry and append a duplicate flat link.
"""

from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
COMMON_JS = ROOT / "preview" / "bousai_common.js"


def extract_nav(html: str) -> str:
    match = re.search(
        r'<nav\b[^>]*\bclass=["\'][^"\']*\bsite-nav\b[^"\']*["\'][^>]*>'
        r'(.*?)</nav>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return match.group(1) if match else ""


class CommonNavigationRuntimeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_public.py")],
            cwd=ROOT,
            check=True,
        )

    def test_modern_mega_nav_disables_legacy_region_link_fallback(self) -> None:
        js = COMMON_JS.read_text(encoding="utf-8")
        function = re.search(
            r"function ensureRegionNavLink\(\) \{(?P<body>.*?)\n  \}",
            js,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(function)
        body = function.group("body")
        guard = 'if (nav.querySelector(".site-nav__mega-group")) return;'
        self.assertIn(guard, body)
        self.assertLess(body.index(guard), body.index("var links ="))

        # The production region page rewrites its own submenu href to index.html.
        # This is the exact route shape that previously fooled the legacy fallback.
        region = (PUBLIC / "region" / "index.html").read_text(encoding="utf-8")
        nav = extract_nav(region)
        self.assertTrue(nav)
        self.assertIn('href="index.html"><strong>地域別</strong>', nav)
        self.assertEqual(1, nav.count("<strong>地域別</strong>"))
        self.assertEqual(3, nav.count('class="site-nav__mega-group"'))
        self.assertEqual(12, nav.count('class="site-nav__submenu-card"'))

    def test_current_navigation_state_uses_resolved_paths(self) -> None:
        js = COMMON_JS.read_text(encoding="utf-8")
        self.assertIn("function normalizedNavigationPath(href)", js)
        self.assertIn("new URL(href, window.location.href).pathname", js)
        self.assertIn("var currentPath = normalizedNavigationPath(window.location.href);", js)
        self.assertIn('document.querySelectorAll(".breadcrumb a[href]")', js)

        # Preview-only category_ names do not survive production path rewriting.
        self.assertNotIn('.breadcrumb a[href^="category_"]', js)

    def test_all_representative_production_navs_keep_expected_shape(self) -> None:
        representative = [
            PUBLIC / "index.html",
            PUBLIC / "flood" / "index.html",
            PUBLIC / "earthquake" / "index.html",
            PUBLIC / "region" / "index.html",
            PUBLIC / "topics" / "region-qa" / "index.html",
            PUBLIC / "special" / "linear-rainband" / "index.html",
            PUBLIC / "special" / "linear-rainband" / "regions.html",
        ]
        for page in representative:
            self.assertTrue(page.exists(), page)
            nav = extract_nav(page.read_text(encoding="utf-8"))
            self.assertTrue(nav, page)
            self.assertEqual(3, nav.count('class="site-nav__mega-group"'), page)
            self.assertEqual(3, nav.count('class="site-nav__submenu-toggle"'), page)
            self.assertEqual(12, nav.count('class="site-nav__submenu-card"'), page)
            self.assertEqual(1, nav.count("<strong>地域別</strong>"), page)
            self.assertEqual(1, nav.count("<strong>Q&amp;A</strong>"), page)

    def test_all_linear_rainband_pages_use_shared_header_and_runtime(self) -> None:
        filenames = [
            "index.html",
            "history.html",
            "frequency.html",
            "regions.html",
            "rainfall-records.html",
            "information-history.html",
            "kyushu.html",
            "kanto-koshin.html",
            "chugoku.html",
            "shikoku.html",
            "tokai.html",
        ]
        for filename in filenames:
            page = PUBLIC / "special" / "linear-rainband" / filename
            self.assertTrue(page.exists(), page)
            html = page.read_text(encoding="utf-8")
            nav = extract_nav(html)
            self.assertTrue(nav, page)
            self.assertNotIn("feature-global-nav", html, page)
            self.assertIn("bousai_common.js", html, page)
            self.assertEqual(3, nav.count('class="site-nav__mega-group"'), page)
            self.assertEqual(12, nav.count('class="site-nav__submenu-card"'), page)


if __name__ == "__main__":
    unittest.main()
