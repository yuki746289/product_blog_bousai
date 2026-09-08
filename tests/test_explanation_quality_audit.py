# Created: 2026-09-08 14:28 JST
import unittest

from tools.audit_explanation_quality import audit_all, markdown_report, priority_score


class ExplanationQualityAuditTests(unittest.TestCase):
    def test_audit_scans_all_articles_and_emits_review_queue(self):
        audits = audit_all()
        self.assertEqual(60, len(audits))
        ids = {audit.article_id for audit in audits}
        self.assertEqual({f"B{number:03d}" for number in range(1, 61)}, ids)

        report = markdown_report(audits)
        self.assertIn("Articles scanned: **60**", report)
        self.assertIn("## Priority queue", report)
        self.assertIn("B022", report)
        self.assertTrue(any(priority_score(audit) > 0 for audit in audits))
        print("\nEXPLANATION_QUALITY_TRIAGE\n" + report)


if __name__ == "__main__":
    unittest.main()
