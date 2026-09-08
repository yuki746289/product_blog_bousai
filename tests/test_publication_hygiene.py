# Created: 2026-09-08 16:35 JST
"""Regression checks that prevent editor/AI work notes from leaking into articles."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTICLE_DIR = ROOT / "content" / "articles"
PREVIEW_DIR = ROOT / "preview"
FINAL_REVIEW_RULE = ROOT / "docs" / "FINAL_ARTICLE_REVIEW_CHECKLIST.md"

# These are production/editorial workflow phrases, not reader-facing content.
FORBIDDEN_PUBLICATION_MARKERS = (
    "別途検討します",
    "今後追加します",
    "商品記事を作成予定",
    "この記事からAmazonへ直接つなげず",
    "商品候補",
    "採用理由",
    "編集メモ",
    "作業メモ",
    "TODO",
    "FIXME",
)


class PublicationHygieneTest(unittest.TestCase):
    def _reader_facing_files(self):
        yield from sorted(ARTICLE_DIR.glob("B*.md"))
        yield from sorted(PREVIEW_DIR.glob("article*.html"))

    def test_internal_work_notes_are_not_published(self):
        failures = []
        for path in self._reader_facing_files():
            text = path.read_text(encoding="utf-8")
            for marker in FORBIDDEN_PUBLICATION_MARKERS:
                if marker in text:
                    failures.append(f"{path.relative_to(ROOT)}: {marker}")
        self.assertEqual([], failures, "Internal/editorial notes leaked into reader-facing content")

    def test_final_review_rule_is_present_and_actionable(self):
        self.assertTrue(FINAL_REVIEW_RULE.exists())
        text = FINAL_REVIEW_RULE.read_text(encoding="utf-8")
        for required in (
            "P0 公開本文の衛生チェック",
            "画像・図解の挿入判断",
            "publication_hygiene",
            "visual_support",
            "B001〜B060",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
