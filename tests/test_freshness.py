# Created: 2026-08-31 22:48 JST

import unittest
from datetime import date

from bousai_blog.freshness import inspect_registry


class FreshnessTests(unittest.TestCase):
    def test_ready_article_is_publishable(self):
        data = {"articles": [{
            "article_id": "B100",
            "slug": "ready",
            "status": "READY_TO_PUBLISH",
            "risk_level": "elevated",
            "manual_review_required": True,
            "manual_review_status": "APPROVED",
            "publish_blockers": [],
            "next_review_at": "2026-12-01"
        }]}
        report = inspect_registry(data, today=date(2026, 8, 31))
        self.assertEqual([], report["errors"])
        self.assertEqual(["B100"], report["publishable"])

    def test_ready_article_with_blocker_is_error(self):
        data = {"articles": [{
            "article_id": "B101",
            "slug": "blocked",
            "status": "READY_TO_PUBLISH",
            "risk_level": "standard",
            "manual_review_required": False,
            "manual_review_status": "NOT_REVIEWED",
            "publish_blockers": ["source_required"]
        }]}
        report = inspect_registry(data, today=date(2026, 8, 31))
        self.assertTrue(any("has blockers" in item for item in report["errors"]))

    def test_published_article_due_for_review(self):
        data = {"articles": [{
            "article_id": "B102",
            "slug": "published",
            "status": "PUBLISHED",
            "risk_level": "standard",
            "manual_review_required": False,
            "manual_review_status": "NOT_REVIEWED",
            "publish_blockers": [],
            "next_review_at": "2026-08-31"
        }]}
        report = inspect_registry(data, today=date(2026, 8, 31))
        self.assertEqual(["B102"], report["due"])

    def test_high_risk_requires_manual_review(self):
        data = {"articles": [{
            "article_id": "B103",
            "slug": "high-risk",
            "status": "DRAFTED",
            "risk_level": "high",
            "manual_review_required": False,
            "manual_review_status": "NOT_REVIEWED",
            "publish_blockers": []
        }]}
        report = inspect_registry(data, today=date(2026, 8, 31))
        self.assertTrue(any("high-risk article" in item for item in report["errors"]))


if __name__ == "__main__":
    unittest.main()
