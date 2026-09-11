# Updated: 2026-09-12 08:52 JST
import unittest
from pathlib import Path

from bousai_blog.registry import load_registry
from tools.audit_explanation_quality import audit_all, markdown_report, priority_score

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "content_registry.json"


class ExplanationQualityAuditTests(unittest.TestCase):
    def test_audit_scans_all_articles_and_emits_review_queue(self):
        audits = audit_all()
        ids = {audit.article_id for audit in audits}
        registry = load_registry(REGISTRY)
        expected_ids = {
            article["article_id"]
            for article in registry["articles"]
            if article.get("article_id", "").startswith("B")
        }

        self.assertEqual(expected_ids, ids)
        self.assertEqual(len(expected_ids), len(audits))

        report = markdown_report(audits)
        self.assertIn(f"Articles scanned: **{len(expected_ids)}**", report)
        self.assertIn("## Priority queue", report)
        self.assertIn("B022", report)
        self.assertTrue(any(priority_score(audit) > 0 for audit in audits))
        print("\nEXPLANATION_QUALITY_TRIAGE\n" + report)


if __name__ == "__main__":
    unittest.main()