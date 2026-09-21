import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SpecificationInvariantRuleTests(unittest.TestCase):
    def test_governance_preserves_approved_spec_after_failures(self):
        text = (ROOT / "docs" / "RULES_GOVERNANCE.md").read_text(encoding="utf-8")
        for marker in (
            "障害時の仕様不変ルール",
            "ユーザー承認済みの仕様は変更しない",
            "「画像」をHTML/CSS図解へ置換",
            "最後に承認された仕様・完了条件・未完了タスク",
            "確認待ち",
        ):
            self.assertIn(marker, text)

    def test_release_checklist_verifies_deliverable_type_and_visibility(self):
        text = (ROOT / "docs" / "SITE_RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
        for marker in (
            "仕様・成果物の一致確認",
            "承認済みの成果物種別",
            "「画像」と「HTML/CSS図解」",
            "PC・スマートフォン双方",
            "公開画面上の配置・順序・可視性",
        ):
            self.assertIn(marker, text)

    def test_article_review_rejects_silent_media_substitution(self):
        text = (ROOT / "docs" / "ARTICLE_REVIEW_CHECKLIST.md").read_text(encoding="utf-8")
        self.assertIn("C01-15", text)
        self.assertIn("C01-16", text)
        self.assertIn("画像指定をHTML/CSS図解等へ勝手に代替せず", text)


if __name__ == "__main__":
    unittest.main()
