from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RegionHistoryPilotTests(unittest.TestCase):
    def _text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_b048_miyagi_source_and_preview_keep_history_safety_boundary(self) -> None:
        source = self._text("content/articles/B048_miyagi_earthquake_tsunami_history.md")
        preview = self._text("preview/article_b048.html")
        for token in (
            "1978年宮城県沖地震",
            "東日本大震災",
            "津波災害警戒区域",
            "過去に被災しなかった",
        ):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        for link in ("article_b023.html", "article_b024.html", "article_b041.html", "article_b030.html"):
            self.assertIn(link, source)
            self.assertIn(link, preview)
        self.assertIn("Damage%20of%20Tsunami%20in%20Natori.JPEG", preview)
        self.assertNotIn("amazon.co.jp", preview.lower())

    def test_b049_hiroshima_source_and_preview_do_not_turn_history_into_prediction(self) -> None:
        source = self._text("content/articles/B049_hiroshima_landslide_history.md")
        preview = self._text("preview/article_b049.html")
        for token in (
            "1999年",
            "2014年",
            "2018年",
            "土砂災害ハザードマップ",
            "将来の被災地点予想",
        ):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        for link in ("article_b036.html", "article_b020.html", "article_b042.html", "article_b015.html"):
            self.assertIn(link, source)
            self.assertIn(link, preview)
        self.assertIn("%E5%BA%83%E5%B3%B6%E5%9C%9F%E7%A0%82", preview)
        self.assertNotIn("amazon.co.jp", preview.lower())

    def test_b050_arakawa_source_and_preview_separate_history_from_current_hazard(self) -> None:
        source = self._text("content/articles/B050_arakawa_flood_history.md")
        preview = self._text("preview/article_b050.html")
        for token in (
            "明治43年",
            "荒川放水路",
            "カスリーン台風",
            "浸水継続時間",
            "大雨時に川や水門を見に行かない",
        ):
            self.assertIn(token, source)
            self.assertIn(token, preview)
        for link in ("article_b042.html", "article_b012.html", "article_b008.html", "article_b010.html", "article_b015.html"):
            self.assertIn(link, source)
            self.assertIn(link, preview)
        self.assertIn("%E6%97%A7%E5%B2%A9%E6%B7%B5%E6%B0%B4%E9%96%80.jpg", preview)
        self.assertNotIn("amazon.co.jp", preview.lower())

    def test_research_and_image_records_exist_for_all_three(self) -> None:
        for article_id in ("B048", "B049", "B050"):
            self.assertTrue((ROOT / f"docs/research/{article_id}_REGION_BRIEF.md").is_file())
            self.assertTrue((ROOT / f"docs/research/{article_id}_IMAGES.md").is_file())
            self.assertTrue((ROOT / f"docs/reviews/{article_id}_CHECKLIST.md").is_file())


if __name__ == "__main__":
    unittest.main()
