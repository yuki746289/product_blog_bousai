# Created: 2026-09-09 09:12 JST
# Updated: 2026-09-09 10:08 JST
import unittest
from pathlib import Path

from scripts.article_diagrams import DIAGRAMS, inject_article_diagram

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_IDS = {"B001", "B003", "B004", "B012", "B015", "B021", "B022", "B028", "B041"}


class ArticleDiagramTests(unittest.TestCase):
    def test_nine_reviewed_diagrams_are_configured(self):
        self.assertEqual(9, len(DIAGRAMS))
        self.assertEqual(EXPECTED_IDS, {spec["article_id"] for spec in DIAGRAMS.values()})

    def test_each_configured_png_exists_in_preview_assets(self):
        for output_path, spec in DIAGRAMS.items():
            with self.subTest(output_path=output_path):
                image_path = ROOT / "preview" / "assets" / "images" / spec["image"]
                self.assertTrue(image_path.is_file(), image_path)
                self.assertGreater(image_path.stat().st_size, 100_000)
                self.assertTrue(spec["image"].endswith(".png"))

    def test_each_diagram_is_an_accessible_responsive_image_figure(self):
        for output_path, spec in DIAGRAMS.items():
            with self.subTest(output_path=output_path):
                figure = spec["figure"]
                self.assertIn(f'data-article-diagram="{spec["article_id"]}"', figure)
                self.assertIn('role="group"', figure)
                self.assertIn('aria-label=', figure)
                self.assertIn('<img ', figure)
                self.assertIn(f'src="{spec["src"]}"', figure)
                self.assertIn(f'alt="{spec["alt"]}"', figure)
                self.assertIn('width="1448"', figure)
                self.assertIn('height="1086"', figure)
                self.assertIn('loading="lazy"', figure)
                self.assertIn('decoding="async"', figure)
                self.assertIn('<figcaption>', figure)
                self.assertNotIn('article-explainer__card', figure)
                self.assertGreaterEqual(len(spec["alt"]), 30)

    def test_asset_paths_are_relative_to_nested_public_article(self):
        for output_path, spec in DIAGRAMS.items():
            with self.subTest(output_path=output_path):
                self.assertEqual(f'../assets/images/{spec["image"]}', spec["src"])

    def test_injection_is_static_idempotent_and_heading_scoped(self):
        path, spec = next(iter(DIAGRAMS.items()))
        source = f"<html><head></head><body><article><h2>{spec['heading']}</h2><p>本文</p></article></body></html>"
        once = inject_article_diagram(source, path)
        twice = inject_article_diagram(once, path)
        marker = f'data-article-diagram="{spec["article_id"]}"'
        self.assertEqual(1, once.count(marker))
        self.assertEqual(once, twice)
        self.assertIn('data-article-diagram-style', once)
        self.assertIn(f'src="{spec["src"]}"', once)
        self.assertLess(once.index('</h2>'), once.index(marker))


if __name__ == '__main__':
    unittest.main()
