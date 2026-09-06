# Created: 2026-09-06
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


class B045B046PublicSyncTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_public.py")],
            cwd=ROOT,
            check=True,
        )

    def test_b045_preview_and_public_keep_source_semantics(self):
        preview = (ROOT / "preview" / "article_b045.html").read_text(encoding="utf-8")
        public = (PUBLIC / "blackout" / "blackout-refrigerator-food-safety.html").read_text(encoding="utf-8")

        preview_required = (
            "ドライアイスや保冷剤",
            "密閉空間での二酸化炭素濃度上昇",
            "肉汁等の漏れによる交差汚染",
            'href="article_b004.html"',
            'href="article_b028.html"',
            'href="article_b031.html"',
        )
        for phrase in preview_required:
            self.assertIn(phrase, preview)

        public_required = (
            "ドライアイスや保冷剤",
            "密閉空間での二酸化炭素濃度上昇",
            "肉汁等の漏れによる交差汚染",
            'href="blackout-preparedness.html"',
            'href="../goods/portable-power-station-disaster.html"',
            'href="../guide/emergency-food-expiration.html"',
        )
        for phrase in public_required:
            self.assertIn(phrase, public)

    def test_b046_preview_and_public_keep_source_semantics(self):
        preview = (ROOT / "preview" / "article_b046.html").read_text(encoding="utf-8")
        public = (PUBLIC / "typhoon" / "typhoon-window-glass.html").read_text(encoding="utf-8")

        preview_required = (
            "段ボール・プラダン・板",
            "板自体が飛来物になる",
            "破損後は写真・保険・修理を安全確認後に",
            'href="article_b006.html"',
            'href="article_b016.html"',
            'href="article_b022.html"',
        )
        for phrase in preview_required:
            self.assertIn(phrase, preview)

        public_required = (
            "段ボール・プラダン・板",
            "板自体が飛来物になる",
            "破損後は写真・保険・修理を安全確認後に",
            'href="typhoon-preparation-checklist.html"',
            'href="../insurance/typhoon-wind-damage-insurance.html"',
            'href="../home/apartment-typhoon-flood.html"',
        )
        for phrase in public_required:
            self.assertIn(phrase, public)


if __name__ == "__main__":
    unittest.main()
