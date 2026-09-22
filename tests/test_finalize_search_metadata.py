from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from finalize_search_metadata import (
    canonical_url,
    inject_canonical,
    inject_region_navigation,
    inject_static_breadcrumb,
    static_breadcrumb_items,
    validate_canonical,
    validate_category_enhancements,
    validate_static_breadcrumb,
)


class FinalizeSearchMetadataTests(unittest.TestCase):
    def test_canonical_url_for_homepage(self) -> None:
        self.assertEqual(
            canonical_url("https://example.test/", "index.html"),
            "https://example.test/",
        )

    def test_canonical_url_for_nested_page(self) -> None:
        self.assertEqual(
            canonical_url("https://example.test/", "goods/power-charging.html"),
            "https://example.test/goods/power-charging.html",
        )

    def test_inject_canonical_replaces_existing_tag(self) -> None:
        source = (
            "<html><head>"
            '<link href="https://old.example/page" rel="canonical">'
            "<title>Test</title></head><body></body></html>"
        )
        expected = "https://example.test/guide/test.html"
        result = inject_canonical(source, expected)

        self.assertEqual(result.lower().count('rel="canonical"'), 1)
        self.assertIn(f'href="{expected}"', result)
        self.assertNotIn("old.example", result)
        self.assertEqual(validate_canonical(result, expected, "guide/test.html"), [])

    def test_validate_rejects_missing_canonical(self) -> None:
        errors = validate_canonical(
            "<html><head><title>Test</title></head><body></body></html>",
            "https://example.test/",
            "index.html",
        )
        self.assertTrue(errors)

    def test_static_breadcrumb_uses_user_facing_names(self) -> None:
        items = static_breadcrumb_items(
            "goods/water-food.html",
            "https://example.test/",
        )
        self.assertEqual(
            ["防災くらしガイド", "防災グッズ", "水・非常食"],
            [item["name"] for item in items],
        )

        source = "<html><head><title>Test</title></head><body></body></html>"
        result = inject_static_breadcrumb(
            source,
            "goods/water-food.html",
            "https://example.test/",
        )
        self.assertEqual(
            [],
            validate_static_breadcrumb(
                result,
                "goods/water-food.html",
                "https://example.test/",
            ),
        )
        self.assertEqual(result.count('data-generated="page-breadcrumb"'), 1)

    def test_mega_navigation_is_not_given_legacy_region_link(self) -> None:
        source = (
            '<nav class="site-nav" aria-label="メインナビゲーション">'
            '<div class="site-nav__mega-group" data-group-label="地域・疑問から探す">'
            '<div class="site-nav__submenu">'
            '<a class="site-nav__submenu-card" href="index.html">'
            '<strong>地域別</strong><span>地域の災害史と備え</span></a>'
            '<a class="site-nav__submenu-card" href="../qa.html">'
            '<strong>Q&A</strong><span>よくある疑問</span></a>'
            '</div></div></nav>'
        )

        result = inject_region_navigation(source, "region/index.html")

        self.assertEqual(result, source)
        self.assertNotIn('>地域別</a>', result)
        self.assertEqual(result.count('<strong>地域別</strong>'), 1)
        self.assertEqual(validate_category_enhancements(result, "region/index.html"), [])

    def test_mega_navigation_rejects_stray_legacy_region_link(self) -> None:
        source = (
            '<nav class="site-nav">'
            '<div class="site-nav__mega-group">'
            '<a class="site-nav__submenu-card" href="index.html"><strong>地域別</strong></a>'
            '<a href="index.html">地域別</a>'
            '</div></nav>'
        )

        errors = validate_category_enhancements(source, "region/index.html")
        self.assertTrue(any("stray legacy regional navigation" in error for error in errors))

    def test_legacy_navigation_still_gets_region_link(self) -> None:
        source = (
            '<nav class="site-nav">'
            '<a href="category_flood.html">台風・水害</a>'
            '<a href="qa.html">Q&A</a>'
            '</nav>'
        )

        result = inject_region_navigation(source, "guide/example.html")
        self.assertIn('<a href="../region/index.html">地域別</a>', result)
        self.assertEqual(validate_category_enhancements(result, "guide/example.html"), [])


if __name__ == "__main__":
    unittest.main()
