import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AnalyticsCiExclusionTest(unittest.TestCase):
    def test_analytics_skip_ci_audit_requests(self):
        html = (ROOT / "templates" / "partials" / "google_analytics.html").read_text(encoding="utf-8")
        self.assertIn("params.get('ci_audit') === '1'", html)
        self.assertIn("window.__BOUSAI_ANALYTICS_DISABLED__ = true", html)
        self.assertIn("document.createElement('script')", html)
        self.assertIn("window.gtag('config', 'G-XQVLD5HMNG')", html)
        self.assertIn("https://accaii.com/bousaikun/analyze.js", html)

        guard_pos = html.index("params.get('ci_audit') === '1'")
        ga_loader_pos = html.index("script.src = 'https://www.googletagmanager.com/gtag/js?id=G-XQVLD5HMNG'")
        config_pos = html.index("window.gtag('config', 'G-XQVLD5HMNG')")
        accaii_loader_pos = html.index("accaiiScript.src = 'https://accaii.com/bousaikun/analyze.js'")
        self.assertLess(guard_pos, ga_loader_pos)
        self.assertLess(guard_pos, config_pos)
        self.assertLess(guard_pos, accaii_loader_pos)

    def test_lighthouse_urls_are_marked_and_network_verified(self):
        workflow = (ROOT / ".github" / "workflows" / "performance-audit.yml").read_text(encoding="utf-8")
        expected = [
            "https://bousaikun.ashigaru.jp/?ci_audit=1",
            "https://bousaikun.ashigaru.jp/guide/first-disaster-preparedness.html?ci_audit=1",
            "https://bousaikun.ashigaru.jp/goods/portable-power-station-disaster.html?ci_audit=1",
        ]
        for url in expected:
            with self.subTest(url=url):
                self.assertIn(url, workflow)

        self.assertIn("Wait for analytics exclusion on production", workflow)
        self.assertIn('marker_file="${RUNNER_TEMP}/bousai-ci-audit-home.html"', workflow)
        self.assertIn('curl -fsS "https://bousaikun.ashigaru.jp/?ci_audit=1" -o "$marker_file"', workflow)
        self.assertIn('grep -q "__BOUSAI_ANALYTICS_DISABLED__" "$marker_file"', workflow)
        self.assertNotIn('| grep -q "__BOUSAI_ANALYTICS_DISABLED__"', workflow)
        self.assertIn("Verify Lighthouse did not contact analytics", workflow)
        self.assertIn("googletagmanager.com/gtag/js", workflow)
        self.assertIn("google-analytics.com/g/collect", workflow)
        self.assertIn("accaii.com/bousaikun/analyze", workflow)
        self.assertIn("PASS: Lighthouse CI audits made no GA4 or Accaii requests.", workflow)

        self.assertNotIn('"https://bousaikun.ashigaru.jp/"\n', workflow)
        self.assertNotIn('"https://bousaikun.ashigaru.jp/guide/first-disaster-preparedness.html"', workflow)
        self.assertNotIn('"https://bousaikun.ashigaru.jp/goods/portable-power-station-disaster.html"', workflow)


if __name__ == "__main__":
    unittest.main()
