from pathlib import Path
import unittest


class ArticleReviewFrameworkCoverageTest(unittest.TestCase):
    def test_all_article_sources_have_completed_review_records(self):
        root = Path(__file__).resolve().parents[1]
        reviews = root / "docs" / "reviews"
        articles = root / "content" / "articles"

        article_ids = sorted(
            {
                path.name.split("_", 1)[0]
                for path in articles.glob("B[0-9][0-9][0-9]_*.md")
            }
        )

        errors = []
        self.assertTrue(article_ids, "no article source files discovered")

        for aid in article_ids:
            checklist = reviews / f"{aid}_CHECKLIST.md"
            if not checklist.exists():
                errors.append(f"{aid}: checklist missing")
                continue

            text = checklist.read_text(encoding="utf-8")

            blocked_markers = (
                "review_status: `FIX_REQUIRED`",
                "review_status: FIX_REQUIRED",
                "review_status: `IN_PROGRESS`",
                "review_status: IN_PROGRESS",
                "READY_TO_PUBLISH: `NO`",
                "READY_TO_PUBLISH: NO",
            )
            blocked = [marker for marker in blocked_markers if marker in text]
            if blocked:
                errors.append(f"{aid}: incomplete review remains ({', '.join(blocked)})")
                continue

            # Support both current and legacy checklist formats while requiring
            # an explicit completed review decision.
            pass_markers = (
                "review_status: `PASS`",
                "review_status: PASS",
                "review_checklist_status: PASS",
                "判定: PASS",
            )
            ready_markers = (
                "READY_TO_PUBLISH: `YES`",
                "READY_TO_PUBLISH: YES",
                "production_build_status: READY_FOR_DEPLOY",
                "article_status: `READY_TO_PUBLISH`",
                "article_status: READY_TO_PUBLISH",
            )

            if not any(marker in text for marker in pass_markers):
                errors.append(f"{aid}: PASS review decision missing")
            if not any(marker in text for marker in ready_markers):
                errors.append(f"{aid}: publish-ready decision missing")

        self.assertEqual([], errors, "\n" + "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
