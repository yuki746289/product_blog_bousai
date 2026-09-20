from pathlib import Path
import re
import unittest


ARTICLE_RE = re.compile(r"^(B\d{3})_.*\.md$")
REVIEW_RE = re.compile(r"^(B\d{3})_CHECKLIST\.md$")


class ArticleReviewFrameworkCoverageTest(unittest.TestCase):
    def test_all_article_sources_have_passing_review_records(self):
        root = Path(__file__).resolve().parents[1]
        articles_dir = root / "content" / "articles"
        reviews_dir = root / "docs" / "reviews"

        article_ids = {}
        for path in sorted(articles_dir.glob("B[0-9][0-9][0-9]_*.md")):
            match = ARTICLE_RE.match(path.name)
            if match:
                article_ids[match.group(1)] = path

        self.assertTrue(article_ids, "No Bxxx article sources found")

        problems = []
        for aid, article_path in sorted(article_ids.items()):
            review_path = reviews_dir / f"{aid}_CHECKLIST.md"
            if not review_path.exists():
                problems.append(
                    f"{aid}: checklist missing for {article_path.relative_to(root)}"
                )
                continue

            text = review_path.read_text(encoding="utf-8")
            required_markers = {
                "site checklist": "BOUSAI_SITE_REVIEW_CHECKLIST.md",
                "published review status": "review_status: `PASS`",
                "publish decision": "READY_TO_PUBLISH: `YES`",
            }
            for label, marker in required_markers.items():
                if marker not in text:
                    problems.append(f"{aid}: {label} marker missing")

            blocking_markers = (
                "review_status: `IN_PROGRESS`",
                "review_status: `FAIL`",
                "review_status: PASS_WITH_PUBLISH_BLOCKERS",
                "READY_TO_PUBLISH: `NO`",
                "READY_TO_PUBLISH: **NO",
            )
            for marker in blocking_markers:
                if marker in text:
                    problems.append(f"{aid}: blocking review marker remains: {marker}")

        review_ids = set()
        for path in reviews_dir.glob("B[0-9][0-9][0-9]_CHECKLIST.md"):
            match = REVIEW_RE.match(path.name)
            if match:
                review_ids.add(match.group(1))
        for aid in sorted(review_ids - set(article_ids)):
            problems.append(f"{aid}: orphan checklist without article source")

        self.assertEqual([], problems, "\n" + "\n".join(problems))

    def test_review_gate_is_not_hardcoded_to_an_article_number_range(self):
        source = Path(__file__).read_text(encoding="utf-8")
        self.assertNotIn("range(1, 38)", source)
        self.assertIn('glob("B[0-9][0-9][0-9]_*.md")', source)


if __name__ == "__main__":
    unittest.main()
