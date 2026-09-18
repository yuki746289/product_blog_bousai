from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "preview" / "bousai_common.css"


class ArticleLayoutContractTest(unittest.TestCase):
    def test_article_shell_uses_wider_desktop_width(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertIn("--article-width: 980px;", css)
        self.assertNotIn("--article-width: 820px;", css)
        self.assertRegex(
            css,
            re.compile(
                r"\.article-shell\s*\{[^}]*width:\s*min\(calc\(100%\s*-\s*32px\),\s*var\(--article-width\)\)",
                re.DOTALL,
            ),
        )

    def test_global_page_width_remains_separate(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertIn("--max-width: 1120px;", css)


if __name__ == "__main__":
    unittest.main()
