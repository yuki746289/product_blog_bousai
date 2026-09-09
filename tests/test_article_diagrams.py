# Created: 2026-09-09 09:12 JST
# Updated: 2026-09-09 09:38 JST
import unittest

from scripts.article_diagrams import DIAGRAMS, inject_article_diagram

EXPECTED_IDS = {"B001", "B003", "B004", "B012", "B015", "B021", "B022", "B028", "B041"}


class ArticleDiagramTests(unittest.TestCase):
    def test_nine_reviewed_diagrams_are_configured(self):
        self.assertEqual(9, len(DIAGRAMS))
        self.assertEqual(EXPECTED_IDS, {spec["article_id"] for spec in DIAGRAMS.values()})

    def test_each_diagram_has_explanatory_caption_and_accessible_group_label(self):
        for output_path, spec in DIAGRAMS.items():
            with self.subTest(output_path=output_path):
                figure = spec["figure"]
                self.assertIn(f'data-article-diagram="{spec["article_id"]}"', figure)
                self.assertIn('role="group"', figure)
                self.assertIn('aria-label=', figure)
                self.assertIn('<figcaption>', figure)
                self.assertIn('article-explainer__title', figure)

    def test_injection_is_static_idempotent_and_heading_scoped(self):
        path, spec = next(iter(DIAGRAMS.items()))
        source = f"<html><head></head><body><article><h2>{spec['heading']}</h2><p>本文</p></article></body></html>"
        once = inject_article_diagram(source, path)
        twice = inject_article_diagram(once, path)
        marker = f'data-article-diagram="{spec["article_id"]}"'
        self.assertEqual(1, once.count(marker))
        self.assertEqual(once, twice)
        self.assertIn('data-article-diagram-style', once)
        self.assertLess(once.index('</h2>'), once.index(marker))

    def test_high_risk_diagrams_include_caution_text(self):
        for article_id in ("B003", "B012", "B015", "B021", "B022", "B041"):
            spec = next(item for item in DIAGRAMS.values() if item["article_id"] == article_id)
            with self.subTest(article_id=article_id):
                self.assertIn('article-explainer__warning', spec["figure"])


if __name__ == '__main__':
    unittest.main()
