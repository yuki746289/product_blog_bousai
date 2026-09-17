# Created: 2026-09-17 JST
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class B024EarthquakeBlackoutWaterOutageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = json.loads((ROOT / "data" / "content_registry.json").read_text(encoding="utf-8"))
        cls.article = next(a for a in registry["articles"] if a["article_id"] == "B024")

    def source(self):
        return (ROOT / self.article["source_path"]).read_text(encoding="utf-8")

    def preview(self):
        return (ROOT / self.article["preview_path"]).read_text(encoding="utf-8")

    def test_b024_is_current_reviewed_and_publishable(self):
        self.assertEqual("READY_TO_PUBLISH", self.article["status"])
        self.assertEqual("APPROVED", self.article["manual_review_status"])
        self.assertEqual([], self.article["publish_blockers"])
        self.assertIn("source_checked_at: 2026-09-17", self.source())
        self.assertIn("next_review_at: 2027-03-17", self.source())

    def test_toilet_guidance_distinguishes_sewer_restriction_from_building_check(self):
        required = (
            "下水道の使用制限が出ている地域では、水洗トイレの使用を控えます",
            "使用制限が出ていない場合も",
            "集合住宅ではまず管理会社へ問い合わせる",
            "浴槽の水を使って大量に流すことを自己判断で始めません",
            "1人1日5回、1週間で35回分",
        )
        for target in (self.source(), self.preview()):
            for phrase in required:
                self.assertIn(phrase, target)

    def test_electrical_fire_and_generator_boundaries_are_explicit(self):
        required = (
            "時間的な猶予がある場合は分電盤のブレーカーを切る",
            "ブレーカー操作のために避難を遅らせません",
            "屋内では絶対に使用しない",
            "自動車内やテント内では使用しません",
            "出入口・窓などの開口部から離し",
        )
        for target in (self.source(), self.preview()):
            for phrase in required:
                self.assertIn(phrase, target)
            self.assertNotIn("発電機は換気すれば屋内で使える", target)

    def test_home_evacuation_does_not_override_immediate_hazard_escape(self):
        required = (
            "指定緊急避難場所",
            "指定避難所",
            "差し迫った危険があるとき",
            "生命を守る避難を優先",
            "在宅避難を続ける前提を外します",
            "article_b039.html",
        )
        for target in (self.source(), self.preview()):
            for phrase in required:
                self.assertIn(phrase, target)

    def test_current_primary_source_memo_records_safety_boundaries(self):
        memo = (ROOT / "docs/research/B024_SOURCES.md").read_text(encoding="utf-8")
        for source_id in range(1, 10):
            self.assertIn(f"F-B024-{source_id:03d}", memo)
        for phrase in (
            "確認日: 2026-09-17",
            "下水道使用制限が出ている地域では使用を控え",
            "屋内で絶対に使用せず",
            "指定緊急避難場所",
            "指定避難所",
        ):
            self.assertIn(phrase, memo)


if __name__ == "__main__":
    unittest.main()
