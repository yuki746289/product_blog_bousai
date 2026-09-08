# Updated: 2026-09-08 14:06 JST
import unittest
from pathlib import Path

from scripts.audit_article_content_metrics import audit
from bousai_blog.registry import load_registry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "content_registry.json"


class ArticleContentRegistryMetricsTests(unittest.TestCase):
    def test_all_article_metrics_exist_and_match_current_source(self):
        expected = {row.article_id: row.body_char_count for row in audit()}
        registry = load_registry(REGISTRY)
        actual = {}
        for article in registry.get("articles", []):
            article_id = article.get("article_id")
            if article_id in expected:
                self.assertIn(
                    "body_char_count_approx",
                    article,
                    f"{article_id} is missing body_char_count_approx",
                )
                actual[article_id] = article["body_char_count_approx"]

        self.assertEqual(set(expected), set(actual))
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
