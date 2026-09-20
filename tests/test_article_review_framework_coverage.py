from pathlib import Path
import unittest


class ArticleReviewFrameworkCoverageTest(unittest.TestCase):
    @staticmethod
    def _status_lines(text: str) -> set[str]:
        normalized = text.replace("`", "").replace("**", "")
        return {
            line.strip().lstrip("- ").strip()
            for line in normalized.splitlines()
            if line.strip()
        }

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
            lines = self._status_lines(text)

            blocked_lines = {
                "review_status: FIX_REQUIRED",
                "review_status: IN_PROGRESS",
                "review_status: PASS_WITH_PUBLISH_BLOCKERS",
                "READY_TO_PUBLISH: NO",
            }
            blocked = sorted(blocked_lines & lines)
            if blocked:
                errors.append(f"{aid}: incomplete review remains ({', '.join(blocked)})")
                continue

            pass_lines = {
                "review_status: PASS",
                "review_checklist_status: PASS",
                "判定: PASS",
            }
            ready_lines = {
                "READY_TO_PUBLISH: YES",
                "production_build_status: READY_FOR_DEPLOY",
                "article_status: READY_TO_PUBLISH",
            }

            has_pass = bool(pass_lines & lines)
            has_ready = bool(ready_lines & lines) or any(
                line.startswith("公開可能") for line in lines
            )

            if not has_pass:
                errors.append(f"{aid}: PASS review decision missing")
            if not has_ready:
                errors.append(f"{aid}: publish-ready decision missing")

        self.assertEqual([], errors, "\n" + "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
