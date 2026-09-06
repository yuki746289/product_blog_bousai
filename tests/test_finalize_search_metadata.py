from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from finalize_search_metadata import canonical_url, inject_canonical, validate_canonical


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
            '<link rel="canonical" href="https://old.example/page">'
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


if __name__ == "__main__":
    unittest.main()
