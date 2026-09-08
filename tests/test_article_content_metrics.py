# Updated: 2026-09-09 06:17 JST
import json
import unittest
from pathlib import Path

from scripts.audit_article_content_metrics import audit, markdown

ROOT = Path(__file__).resolve().parents[1]
EXCEPTIONS_PATH = ROOT / "docs" / "reviews" / "ARTICLE_LENGTH_EXCEPTIONS_20260909.json"


class ArticleContentMetricsTests(unittest.TestCase):
    def test_article_length_guidelines_or_documented_exception(self):
        rows = audit()
        print("\nARTICLE_CONTENT_METRICS\n" + markdown(rows) + "\n")
        failures = {row.article_id: row for row in rows if row.length_status == "FAIL_LENGTH"}

        data = json.loads(EXCEPTIONS_PATH.read_text(encoding="utf-8"))
        exceptions = {item["article_id"]: item for item in data["articles"]}

        self.assertEqual(
            set(failures),
            set(exceptions),
            "Every article below the warning threshold must have an explicit reviewed exception, and stale exceptions are not allowed.",
        )

        for article_id, row in failures.items():
            exception = exceptions[article_id]
            with self.subTest(article_id=article_id):
                self.assertEqual("PASS", exception["final_review_status"])
                self.assertEqual(row.body_char_count, exception["body_char_count"])
                self.assertEqual(row.minimum_char_count, exception["minimum_char_count"])
                self.assertGreaterEqual(len(exception["rationale"].strip()), 40)


if __name__ == "__main__":
    unittest.main()
