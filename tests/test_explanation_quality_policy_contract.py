# Created: 2026-09-08 14:13 JST
import unittest
from pathlib import Path

from bousai_blog.registry import load_registry

ROOT = Path(__file__).resolve().parents[1]


class ExplanationQualityPolicyContractTests(unittest.TestCase):
    def test_policy_contains_required_quality_gates(self):
        policy = (ROOT / "docs" / "EXPLANATION_QUALITY_PREFLIGHT.md").read_text(
            encoding="utf-8"
        )
        for needle in (
            "テクニカルライター / インストラクショナルデザイナー",
            "生活者UX / 行動リアリティ",
            "通常H2",
            "400〜800字程度",
            "安全判断・避難・制度等の重要H2",
            "600〜1,000字程度",
            "文字数を満たすためだけの同義反復",
            "養生テープ",
            "AMAZON_WORK_PREFLIGHT.md",
            "explanation_quality_review",
        ):
            self.assertIn(needle, policy)

    def test_b022_pilot_fixes_explanation_gaps(self):
        article = (ROOT / "content" / "articles" / "B022_apartment_typhoon_flood.md").read_text(
            encoding="utf-8"
        )
        preview = (ROOT / "preview" / "article_b022.html").read_text(encoding="utf-8")
        for needle in (
            "排水口が詰まると",
            "居住者個人が勝手に設置することを標準行動にはしません",
            "養生テープだけで窓そのものを割れなく",
            "家屋倒壊等氾濫想定区域",
            "article_b046.html",
        ):
            self.assertIn(needle, article)
            self.assertIn(needle, preview)

    def test_registry_update_patch_applies_to_b022(self):
        registry = load_registry(ROOT / "data" / "content_registry.json")
        articles = {item["article_id"]: item for item in registry["articles"]}
        b022 = articles["B022"]
        self.assertEqual(4576, b022["body_char_count_approx"])
        self.assertEqual("2026-09-08", b022["last_reviewed_at"])
        self.assertEqual("2026-09-08", b022["review_checklist_last_checked_at"])
        self.assertEqual("2026-09-08", b022["modified_at"])


if __name__ == "__main__":
    unittest.main()
