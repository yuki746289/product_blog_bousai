from pathlib import Path
import unittest


class ArticleReviewFrameworkCoverageTest(unittest.TestCase):
    def test_all_published_article_reviews_use_current_site_framework(self):
        root = Path(__file__).resolve().parents[1]
        reviews = root / "docs" / "reviews"

        articles = root / "content" / "articles"
        article_ids = sorted(
            {
                path.name.split("_", 1)[0]
                for path in articles.glob("B[0-9][0-9][0-9]_*.md")
            }
        )

        missing = []
        self.assertTrue(article_ids, "no article source files discovered")

        for aid in article_ids:
            path = reviews / f"{aid}_CHECKLIST.md"
            if not path.exists():
                missing.append(f"{aid}: checklist missing")
                continue

            text = path.read_text(encoding="utf-8")
            required_markers = {
                "site checklist": "BOUSAI_SITE_REVIEW_CHECKLIST.md",
                "situational reader model": "persona_mode: `SITUATIONAL_SEGMENT`",
            }
            for label, marker in required_markers.items():
                if marker not in text:
                    missing.append(f"{aid}: {label} marker missing")

            has_pass = "review_status: `PASS`" in text or "review_status: PASS" in text
            has_fix = (
                "review_status: `FIX_REQUIRED`" in text
                or "review_status: FIX_REQUIRED" in text
                or "review_status: `IN_PROGRESS`" in text
                or "review_status: IN_PROGRESS" in text
            )
            if not (has_pass or has_fix):
                missing.append(f"{aid}: review_status marker missing")

            has_ready = (
                "READY_TO_PUBLISH: `YES`" in text
                or "READY_TO_PUBLISH: YES" in text
                or "READY_TO_PUBLISH: `NO`" in text
                or "READY_TO_PUBLISH: NO" in text
            )
            if not has_ready:
                missing.append(f"{aid}: publish decision marker missing")

        self.assertEqual([], missing, "\n" + "\n".join(missing))


if __name__ == "__main__":
    unittest.main()
