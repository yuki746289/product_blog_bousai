# Created: 2026-09-01 09:00 JST

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT_ID = "G-XQVLD5HMNG"


class AnalyticsConfigurationTests(unittest.TestCase):
    def test_site_config_has_expected_measurement_id(self):
        config = json.loads((ROOT / "config" / "site.json").read_text(encoding="utf-8"))
        analytics = config["analytics"]
        self.assertTrue(analytics["enabled"])
        self.assertTrue(analytics["required_on_all_public_pages"])
        self.assertEqual(MEASUREMENT_ID, analytics["measurement_id"])

    def test_google_analytics_partial_contains_measurement_id_once_per_call(self):
        html = (ROOT / "templates" / "partials" / "google_analytics.html").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            f"https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}",
            html,
        )
        self.assertIn(f"gtag('config', '{MEASUREMENT_ID}');", html)
        self.assertEqual(1, html.count("googletagmanager.com/gtag/js"))
        self.assertIn('rel="preconnect" href="https://www.googletagmanager.com"', html)
        self.assertIn('rel="preconnect" href="https://www.google-analytics.com"', html)

    def test_temporary_accaii_loader_is_in_common_analytics_partial(self):
        html = (ROOT / "templates" / "partials" / "google_analytics.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("https://accaii.com/bousaikun/analyze.js", html)
        self.assertEqual(1, html.count("https://accaii.com/bousaikun/analyze.js"))
        self.assertIn("var accaiiScript = document.createElement('script');", html)
        self.assertIn("accaiiScript.async = true", html)
        self.assertIn("Remove this loader when U11", html)

    def test_click_tracking_is_in_common_js(self):
        js = (ROOT / "preview" / "bousai_common.js").read_text(encoding="utf-8")
        self.assertIn('"amazon_click"', js)
        self.assertIn('"product_guide_click"', js)
        self.assertIn('transport_type: "beacon"', js)
        self.assertIn('host.endsWith(".amazon.co.jp")', js)


if __name__ == "__main__":
    unittest.main()
