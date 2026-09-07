import unittest

from scripts.audit_article_content_metrics import audit, markdown


class ArticleContentMetricsTests(unittest.TestCase):
    def test_article_length_guidelines(self):
        rows = audit()
        print("\nARTICLE_CONTENT_METRICS\n" + markdown(rows) + "\n")
        failures = [row for row in rows if row.length_status == "FAIL_LENGTH"]
        self.assertEqual(
            [],
            [(row.article_id, row.body_char_count, row.minimum_char_count) for row in failures],
            "Articles below the current checklist minimum require strengthening or a documented exception.",
        )


if __name__ == "__main__":
    unittest.main()
