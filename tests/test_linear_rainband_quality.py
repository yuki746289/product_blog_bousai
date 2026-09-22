from pathlib import Path
import unittest

from scripts import sync_previews_from_markdown as preview_sync


ROOT = Path(__file__).resolve().parents[1]
ARTICLE_DIR = ROOT / "content" / "articles"

FILES = [
    "B067_linear_rainband_feature.md",
    "B068_linear_rainband_history.md",
    "B069_linear_rainband_frequency.md",
    "B070_linear_rainband_regions.md",
    "B071_linear_rainband_rainfall_records.md",
    "B072_linear_rainband_information_history.md",
    "B073_linear_rainband_kyushu.md",
    "B074_linear_rainband_kanto_koshin.md",
    "B075_linear_rainband_chugoku.md",
    "B076_linear_rainband_shikoku.md",
    "B077_linear_rainband_tokai.md",
    "B097_guerrilla_rain_vs_linear_rainband.md",
]


class LinearRainbandQualityTest(unittest.TestCase):
    def _texts(self):
        return {
            name: (ARTICLE_DIR / name).read_text(encoding="utf-8")
            for name in FILES
        }

    def test_editorial_todo_language_is_not_published(self):
        forbidden = [
            "今後このページで追加する集計",
            "将来的には",
            "今後のCSV集計",
            "地方名だけを差し替えた量産",
            "## 先に確認：",
            "## まず見る：",
            "| 読み方 |",
            "代表事例",
        ]
        for name, text in self._texts().items():
            for phrase in forbidden:
                self.assertNotIn(phrase, text, f"{name}: {phrase}")

    def test_current_2026_information_names_are_explicit(self):
        history = (ARTICLE_DIR / "B072_linear_rainband_information_history.md").read_text(encoding="utf-8")
        for phrase in [
            "気象解説情報（線状降水帯半日前予測）",
            "気象防災速報（線状降水帯直前予測）",
            "気象防災速報（線状降水帯発生）",
            "警戒レベル4相当以上",
            "警戒レベル5",
        ]:
            self.assertIn(phrase, history)

    def test_pillar_explains_level5_is_not_linear_rainband_alert(self):
        pillar = (ARTICLE_DIR / "B067_linear_rainband_feature.md").read_text(encoding="utf-8")
        self.assertIn("線状降水帯発生情報＝警戒レベル5ではない", pillar)
        self.assertIn("レベル4までに避難する", pillar)

    def test_all_linear_rainband_articles_are_full_body_and_lead_sync_targets(self):
        expected = {f"B{i:03d}" for i in range(67, 78)} | {"B097"}
        self.assertTrue(expected.issubset(preview_sync.SYNC_ARTICLE_IDS))
        self.assertTrue(expected.issubset(preview_sync.LEAD_SYNC_ARTICLE_IDS))

    def test_public_source_sections_use_clickable_official_links(self):
        for name, text in self._texts().items():
            source_pos = max(
                text.rfind("## 公的情報・参考資料"),
                text.rfind("## 参考資料"),
                text.rfind("## 出典"),
            )
            self.assertGreaterEqual(source_pos, 0, name)
            source = text[source_pos:]
            source_lines = [line for line in source.splitlines() if line.startswith("- ")]
            self.assertTrue(source_lines, name)
            for line in source_lines:
                self.assertIn("](", line, f"{name}: {line}")
                self.assertTrue(
                    "jma.go.jp" in line or "data.jma.go.jp" in line,
                    f"{name}: non-JMA source link {line}",
                )

    def test_region_pages_do_not_repeat_old_four_stage_template(self):
        for name in FILES[6:]:
            text = (ARTICLE_DIR / name).read_text(encoding="utf-8")
            self.assertNotIn("確認する情報を4段階", text)
            self.assertNotIn("確認する情報を4つに分ける", text)


if __name__ == "__main__":
    unittest.main()
