from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RakkoExistingArticleUpdateTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def assert_contains_all(self, relative_path: str, *needles: str) -> None:
        text = self.read(relative_path)
        for needle in needles:
            with self.subTest(path=relative_path, needle=needle):
                self.assertIn(needle, text)

    def test_b002_shelter_and_medication_intent_is_covered(self) -> None:
        for path in (
            "content/articles/B002_emergency_bag_basics.md",
            "preview/article_b002.html",
        ):
            self.assert_contains_all(
                path,
                "避難所へ行く場合に追加確認",
                "お薬手帳",
                "持ち物を全部そろえるために避難を遅らせない",
            )
        self.assert_contains_all("preview/article_b002.html", "qa-shelter-minimum-items")

    def test_b004_winter_blackout_intent_is_covered(self) -> None:
        for path in (
            "content/articles/B004_blackout_preparedness.md",
            "preview/article_b004.html",
        ):
            self.assert_contains_all(
                path,
                "冬の停電",
                "体温を逃がさない",
                "携帯発電機",
            )

    def test_b020_linear_rainband_intent_is_covered(self) -> None:
        for path in (
            "content/articles/B020_home_heavy_rain_checklist.md",
            "preview/article_b020.html",
        ):
            self.assert_contains_all(
                path,
                "線状降水帯",
                "発生情報",
                "qa-linear-rainband-evacuate",
            )

    def test_b042_kikikuru_distinctions_are_covered(self) -> None:
        for path in (
            "content/articles/B042_flood_river_evacuation.md",
            "preview/article_b042.html",
        ):
            self.assert_contains_all(
                path,
                "洪水キキクルと浸水キキクル",
                "3時間先",
                "1時間先",
                "qa-inland-flood-river-flood",
            )

    def test_qa_page_has_four_rakko_followup_questions(self) -> None:
        qa = self.read("preview/qa.html")
        expected = {
            "qa-shelter-minimum-items": "避難所へ行くとき、持ち物は最低限何が必要ですか？",
            "qa-linear-rainband-evacuate": "線状降水帯の情報が出たら、すぐ避難すべきですか？",
            "qa-inland-flood-river-flood": "内水氾濫と洪水は何が違いますか？",
            "qa-disaster-oral-care": "災害時、水が少なくても口腔ケアは必要ですか？",
        }
        for anchor, question in expected.items():
            with self.subTest(anchor=anchor):
                self.assertIn(f'id="{anchor}"', qa)
                self.assertIn(question, qa)

        self.assertIn("台風・大雨・避難</h2><p>7件のQ&amp;A", qa)
        self.assertIn("防災バッグ・防災用品</h2><p>7件のQ&amp;A", qa)


if __name__ == "__main__":
    unittest.main()
