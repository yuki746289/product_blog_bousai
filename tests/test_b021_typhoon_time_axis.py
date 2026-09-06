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
                self.assertIn("3〜6時間前", text)
                self.assertIn("中止条件", text)
                self.assertIn("6時間前は「まだ外へ出てよい時間」という意味ではありません", text)
                self.assertIn("避難情報", text)
                self.assertIn("屋外作業を中止", text)

    def test_time_axis_does_not_override_safety_information(self) -> None:
        source = self.read("content/articles/B021_typhoon_day_before_checklist.md")
        self.assertIn(
            "残り時間は作業を前倒しするための目安",
            source,
        )
        self.assertIn(
            "実際には自治体の避難情報、警報・注意報、雨・風・高潮の予想、周囲の状況を優先",
            source,
        )
        self.assertNotIn("6時間前なら外作業", source)
        self.assertNotIn("6時間前までは安全", source)


if __name__ == "__main__":
    unittest.main()
