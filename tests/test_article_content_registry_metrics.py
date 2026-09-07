# Updated: 2026-09-08 08:16 JST
import json
import unittest
from pathlib import Path

from scripts.audit_article_content_metrics import audit

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATHS = [
    ROOT / "data" / "content_registry.json",
    *sorted((ROOT / "data").glob("content_registry_additions*.json")),
]


class ArticleContentRegistryMetricsTests(unittest.TestCase):
    def test_all_article_metrics_exist_and_match_current_source(self):
        expected = {row.article_id: row.body_char_count for row in audit()}
        actual = {}
        for path in REGISTRY_PATHS:
            data = json.loads(path.read_text(encoding="utf-8"))
            for article in data.get("articles", []):
                article_id = article.get("article_id")
                if article_id in expected:
                    self.assertIn(
                        "body_char_count_approx",
                        article,
                        f"{article_id} is missing body_char_count_approx in {path.name}",
                    )
                    actual[article_id] = article["body_char_count_approx"]

        self.assertEqual(set(expected), set(actual))
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
