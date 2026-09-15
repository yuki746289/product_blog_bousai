from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class B021TyphoonTimeAxisTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_source_and_preview_include_time_axis_and_stop_rules(self) -> None:
        for path in (
            "content/articles/B021_typhoon_day_before_checklist.md",
            "preview/article_b021.html",
        ):
            text = self.read(path)
            with self.subTest(path=path):
                self.assertIn("24時間前", text)
                self.assertIn("12時間前", text)
                self.assertIn("6時間前", text)
                self.assertIn("中止条件", text)
                self.assertIn("6時間前は「まだ外へ出てよい時間」という意味ではありません", text)
                self.assertIn("避難情報", text)
                self.assertIn("屋外作業を中止", text)

    def test_time_axis_does_not_override_safety_information(self) -> None:
        source = self.read("content/articles/B021_typhoon_day_before_checklist.md")
        self.assertIn("残り時間は作業を前倒しするための目安", source)
        self.assertIn(
            "実際には自治体の避難情報、警報・注意報、雨・風・高潮の予想、周囲の状況を優先",
            source,
        )
        self.assertNotIn("6時間前なら外作業", source)
        self.assertNotIn("6時間前までは安全", source)
        self.assertNotIn("3〜6時間前", source)

    def test_b021_uses_current_2026_weather_information_system(self) -> None:
        source = self.read("content/articles/B021_typhoon_day_before_checklist.md")
        sources = self.read("docs/research/B021_SOURCES.md")
        for text in (source, sources):
            self.assertIn("2026年5月29日", text)
            self.assertIn("レベル3大雨警報", text)
            self.assertIn("レベル4大雨危険警報", text)
        self.assertIn("暴風警報", source)
        self.assertNotIn("レベル4暴風警報", source)

    def test_b021_keeps_outdoor_stop_boundary(self) -> None:
        source = self.read("content/articles/B021_typhoon_day_before_checklist.md")
        required = [
            "大雨が降る前、風が強くなる前",
            "自宅対策が途中でも危険が高まったら中止する",
            "屋根・雨どい・ベランダ作業",
            "海・川・用水路の様子を見に行く",
            "冠水した道路へ車で入る",
        ]
        for phrase in required:
            self.assertIn(phrase, source)


if __name__ == "__main__":
    unittest.main()
