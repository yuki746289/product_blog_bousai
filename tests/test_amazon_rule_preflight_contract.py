from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AmazonRulePreflightContractTests(unittest.TestCase):
    def text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_required_amazon_rule_files_exist(self) -> None:
        for path in (
            "docs/AMAZON_WORK_PREFLIGHT.md",
            "docs/AFFILIATE_POLICY.md",
            "docs/AMAZON_PRODUCT_AVAILABILITY_POLICY.md",
            "docs/reviews/ARTICLE_CHECKLIST_TEMPLATE.md",
        ):
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file(), path)

    def test_preflight_requires_current_amazon_policies_before_implementation(self) -> None:
        preflight = self.text("docs/AMAZON_WORK_PREFLIGHT.md")
        for token in (
            "docs/AFFILIATE_POLICY.md",
            "docs/AMAZON_PRODUCT_AVAILABILITY_POLICY.md",
            "CR-05B / CR-06",
            "C06 商品導線・商品記事",
            "過去の会話・記憶・以前読んだルールだけで代替しない",
            "商品選定・ASIN確定・商品画像実装・Amazon CTA実装・公開へ進まない",
        ):
            self.assertIn(token, preflight)

    def test_affiliate_policy_makes_preflight_a_hard_gate(self) -> None:
        policy = self.text("docs/AFFILIATE_POLICY.md")
        self.assertIn("## 0. 作業開始前の必須プレフライト", policy)
        self.assertIn("docs/AMAZON_WORK_PREFLIGHT.md", policy)
        self.assertIn("docs/AMAZON_PRODUCT_AVAILABILITY_POLICY.md", policy)
        self.assertIn("Amazon関連の作業単位ごと", policy)
        self.assertIn("プレフライトが `PASS` でない場合", policy)

    def test_article_checklist_template_requires_amazon_evidence(self) -> None:
        template = self.text("docs/reviews/ARTICLE_CHECKLIST_TEMPLATE.md")
        for token in (
            "Amazon関連作業の適用判定",
            "Amazonプレフライト",
            "docs/AMAZON_WORK_PREFLIGHT.md",
            "docs/AMAZON_PRODUCT_AVAILABILITY_POLICY.md",
            "amazon_preflight:",
            "amazon_preflight_checked_at:",
            "amazon_policy_refs:",
            "amazon_scope:",
        ):
            self.assertIn(token, template)


if __name__ == "__main__":
    unittest.main()
