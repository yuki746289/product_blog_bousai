from pathlib import Path
import unittest


class ArticleReviewFrameworkCoverageTest(unittest.TestCase):
    def test_all_published_article_reviews_use_current_site_framework(self):
        root = Path(__file__).resolve().parents[1]
        reviews = root / "docs" / "reviews"

        missing = []
        for n in range(1, 38):
            aid = f"B{n:03d}"
            path = reviews / f"{aid}_CHECKLIST.md"
            if not path.exists():
                missing.append(f"{aid}: checklist missing")
                continue

            text = path.read_text(encoding="utf-8")
            required_markers = {
                "site checklist": "BOUSAI_SITE_REVIEW_CHECKLIST.md",
                "situational reader model": "persona_mode: `SITUATIONAL_SEGMENT`",
                "published review status": "review_status: `PASS`",
                "publish decision": "READY_TO_PUBLISH: `YES`",
            }
            for label, marker in required_markers.items():
                if marker not in text:
                    missing.append(f"{aid}: {label} marker missing")

            if "review_status: `IN_PROGRESS`" in text:
                missing.append(f"{aid}: stale IN_PROGRESS remains")

        self.assertEqual([], missing, "\n" + "\n".join(missing))


if __name__ == "__main__":
    unittest.main()
