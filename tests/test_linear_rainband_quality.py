from pathlib import Path
import unittest

from scripts import sync_previews_from_markdown as preview_sync
from scripts import enhance_linear_rainband_feature as feature_enhance


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
PREFECTURE_FILES = [
    "B082_linear_rainband_kagoshima.md",
    "B083_linear_rainband_miyazaki.md",
    "B084_linear_rainband_kumamoto.md",
    "B085_linear_rainband_nagasaki.md",
    "B086_linear_rainband_oita.md",
    "B087_linear_rainband_kochi.md",
    "B088_linear_rainband_wakayama.md",
    "B089_linear_rainband_mie.md",
    "B090_linear_rainband_shizuoka.md",
    "B091_linear_rainband_chiba.md",
    "B092_linear_rainband_tokyo.md",
    "B093_linear_rainband_osaka.md",
    "B094_linear_rainband_aichi.md",
    "B095_linear_rainband_ishikawa.md",
    "B096_linear_rainband_toyama.md",
    "B098_linear_rainband_kanagawa.md",
]

class LinearRainbandQualityTest(unittest.TestCase):
    def _table_row_count_after_heading(self, text, heading):
        marker = f"## {heading}"
        start = text.find(marker)
        self.assertGreaterEqual(start, 0, heading)
        section = text[start + len(marker):]
        next_heading = section.find("\n## ")
        if next_heading >= 0:
            section = section[:next_heading]
        rows = [
            line for line in section.splitlines()
            if line.startswith("|")
            and not line.startswith("|---")
            and not line.startswith("| ---")
        ]
        # Remove the table header; separator lines are already excluded.
        return max(0, len(rows) - 1)

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
            "## 代表事例",
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
                    "jma.go.jp" in line
                    or "data.jma.go.jp" in line
                    or "jma-net.go.jp" in line,
                    f"{name}: non-JMA source link {line}",
                )


    def test_prefecture_markdown_has_no_raw_br_tags(self):
        for name in PREFECTURE_FILES:
            text = (ARTICLE_DIR / name).read_text(encoding="utf-8")
            self.assertNotIn("<br>", text.lower(), name)
            self.assertNotIn("<br/>", text.lower(), name)
            self.assertNotIn("<br />", text.lower(), name)


    def test_case_focused_history_and_region_pages_keep_five_to_ten_cases(self):
        expected = {
            "B068_linear_rainband_history.md": (
                "直近の線状降水帯・大雨事例",
                "過去の代表的な豪雨・線状降水帯事例",
            ),
            "B073_linear_rainband_kyushu.md": (
                "直近の大雨・線状降水帯事例",
                "過去の代表的な豪雨",
            ),
            "B074_linear_rainband_kanto_koshin.md": (
                "直近の大雨・線状降水帯事例",
                "過去の代表的な豪雨",
            ),
            "B075_linear_rainband_chugoku.md": (
                "直近の大雨・線状降水帯事例",
                "過去の代表的な豪雨",
            ),
            "B076_linear_rainband_shikoku.md": (
                "直近の大雨・線状降水帯事例",
                "過去の代表的な豪雨",
            ),
            "B077_linear_rainband_tokai.md": (
                "直近の大雨・線状降水帯事例",
                "過去の代表的な豪雨",
            ),
        }
        for name, headings in expected.items():
            text = (ARTICLE_DIR / name).read_text(encoding="utf-8")
            for heading in headings:
                count = self._table_row_count_after_heading(text, heading)
                self.assertGreaterEqual(count, 5, f"{name}: {heading}={count}")
                self.assertLessEqual(count, 10, f"{name}: {heading}={count}")

    def test_kanagawa_case_tables_keep_reviewed_case_counts(self):
        text = (ARTICLE_DIR / "B098_linear_rainband_kanagawa.md").read_text(encoding="utf-8")
        recent = self._table_row_count_after_heading(text, "直近の大雨・線状降水帯事例")
        past = self._table_row_count_after_heading(text, "過去の代表的な豪雨")
        self.assertEqual(10, recent)
        self.assertEqual(7, past)

    def test_case_focused_region_markdown_has_no_raw_html_breaks(self):
        for name in (
            "B068_linear_rainband_history.md",
            "B073_linear_rainband_kyushu.md",
            "B074_linear_rainband_kanto_koshin.md",
            "B075_linear_rainband_chugoku.md",
            "B076_linear_rainband_shikoku.md",
            "B077_linear_rainband_tokai.md",
        ):
            text = (ARTICLE_DIR / name).read_text(encoding="utf-8").lower()
            self.assertNotIn("<br>", text, name)
            self.assertNotIn("<br/>", text, name)
            self.assertNotIn("<br />", text, name)


    def test_recent_case_recency_and_local_downpour_regressions(self):
        expectations = {
            "B068_linear_rainband_history.md": [
                "2026年9月20〜23日",
                "2026年8月22日",
                "局地的大雨（いわゆるゲリラ豪雨）",
            ],
            "B074_linear_rainband_kanto_koshin.md": [
                "2026年9月20〜23日",
                "2025年7月10日",
                "2024年8月21日",
            ],
            "B075_linear_rainband_chugoku.md": [
                "2025年9月11日",
                "2024年11月1〜2日",
                "2024年9月11日",
            ],
            "B084_linear_rainband_kumamoto.md": [
                "2024年11月2日",
                "2024年10月19日",
                "2024年9月22日",
            ],
            "B091_linear_rainband_chiba.md": [
                "2026年9月21〜22日",
                "2025年9月12日",
                "2024年9月3日",
                "局地的大雨（いわゆるゲリラ豪雨）",
            ],
            "B092_linear_rainband_tokyo.md": [
                "2025年7月10日",
                "2024年8月21日",
                "2024年7月31日",
                "局地的大雨（いわゆるゲリラ豪雨）",
            ],
            "B096_linear_rainband_toyama.md": [
                "2024年8月25日",
                "146.5mm",
                "局地的大雨（いわゆるゲリラ豪雨）",
            ],
            "B098_linear_rainband_kanagawa.md": [
                "2026年9月20〜23日",
                "2025年9月11日",
                "2025年9月4〜5日",
                "県内で初めて線状降水帯",
                "崖崩れ",
            ],
        }
        for name, phrases in expectations.items():
            text = (ARTICLE_DIR / name).read_text(encoding="utf-8")
            for phrase in phrases:
                self.assertIn(phrase, text, f"{name}: {phrase}")

    def test_public_rules_define_recent_as_newest_first(self):
        rules = (ROOT / "docs" / "CONTENT_CREATION_RULES.md").read_text(encoding="utf-8")
        self.assertIn("「直近」は重大度ではなく新しさを優先する", rules)
        self.assertIn("局地的大雨・短時間強雨", rules)
        self.assertIn("「ゲリラ豪雨」を気象庁の公式分類名として扱わない", rules)

    def test_prefecture_cards_are_ordered_north_to_south(self):
        labels = [row[1] for row in feature_enhance.PREFECTURE_PAGES]
        self.assertEqual(
            [
                "富山県",
                "石川県",
                "東京都",
                "千葉県",
                "神奈川県",
                "愛知県",
                "静岡県",
                "三重県",
                "和歌山県",
                "高知県",
                "大分県",
                "熊本県",
                "長崎県",
                "宮崎県",
                "鹿児島県",
            ],
            labels,
        )

    def test_feature_tables_use_semantic_phrase_emphasis(self):
        style = feature_enhance.FEATURE_STYLE
        self.assertNotIn(
            ".article-body table tbody td:first-child{font-weight:800;color:var(--primary-dark)}",
            style,
        )
        self.assertIn(
            ".article-body table tbody tr:nth-child(even){background:rgba(23,107,104,.035)}",
            style,
        )

        source = (
            "<table><tbody><tr><td>"
            "観測史上1位。大雨特別警報。避難指示。線状降水帯。"
            "</td></tr></tbody></table>"
        )
        highlighted = feature_enhance._highlight_semantic_table_terms(source)
        self.assertIn('<span class="emphasis-record">観測史上1位</span>', highlighted)
        self.assertIn('<span class="emphasis-danger">大雨特別警報</span>', highlighted)
        self.assertIn('<span class="emphasis-caution">避難指示</span>', highlighted)
        self.assertIn('<span class="emphasis-term">線状降水帯</span>', highlighted)
        self.assertEqual(
            highlighted,
            feature_enhance._highlight_semantic_table_terms(highlighted),
        )

        css = (ROOT / "preview" / "bousai_common.css").read_text(encoding="utf-8")
        for css_class in (
            ".emphasis-record",
            ".emphasis-danger",
            ".emphasis-caution",
            ".emphasis-term",
        ):
            self.assertIn(css_class, css)

    def test_prefecture_card_captions_are_not_locked_to_specific_years(self):
        for article_id, label, _href, caption in feature_enhance.PREFECTURE_PAGES:
            self.assertNotIn("19", caption, f"{article_id} {label}: {caption}")
            self.assertNotIn("20", caption, f"{article_id} {label}: {caption}")

    def test_prefecture_public_headers_follow_current_generic_titles(self):
        expected = {
            "B082": "鹿児島県",
            "B083": "宮崎県",
            "B084": "熊本県",
            "B085": "長崎県",
            "B086": "大分県",
            "B087": "高知県",
            "B088": "和歌山県",
            "B089": "三重県",
            "B090": "静岡県",
            "B091": "千葉県",
            "B092": "東京都",
            "B094": "愛知県",
            "B095": "石川県",
            "B096": "富山県",
            "B098": "神奈川県",
        }
        for article_id, prefecture in expected.items():
            title = f"{prefecture}の線状降水帯｜過去の発生履歴・直近事例を一覧で解説"
            html = (ROOT / "preview" / f"article_{article_id.lower()}.html").read_text(encoding="utf-8")
            self.assertIn(f"<title>{title}｜防災くらしガイド</title>", html, article_id)
            self.assertIn(f"<h1>{title}</h1>", html, article_id)
            self.assertIn('<span class="label">台風・水害</span>', html, article_id)
            self.assertIn("線状降水帯の名称だけで判断せず", html, article_id)

    def test_region_pages_do_not_repeat_old_four_stage_template(self):
        for name in FILES[6:]:
            text = (ARTICLE_DIR / name).read_text(encoding="utf-8")
            self.assertNotIn("確認する情報を4段階", text)
            self.assertNotIn("確認する情報を4つに分ける", text)


if __name__ == "__main__":
    unittest.main()
