# Created: 2026-09-06T17:23+09:00
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError
from urllib.request import Request

from scripts.localize_commons_images_ci import (
    MAX_DOWNLOAD_WORKERS,
    external_wikimedia_pages,
    read_url,
    retry_after_seconds,
    retry_delay_seconds,
    validate_production_build,
)


class CommonsCiLocalizationTests(unittest.TestCase):
    def test_download_concurrency_is_intentionally_low(self):
        self.assertLessEqual(MAX_DOWNLOAD_WORKERS, 2)

    def test_retry_after_supports_seconds(self):
        error = HTTPError(
            "https://commons.wikimedia.org/test",
            429,
            "Too Many Requests",
            {"Retry-After": "7"},
            None,
        )
        self.assertEqual(7.0, retry_after_seconds(error))
        self.assertEqual(7.0, retry_delay_seconds(0, error))

    def test_retry_after_supports_http_date(self):
        error = HTTPError(
            "https://commons.wikimedia.org/test",
            429,
            "Too Many Requests",
            {"Retry-After": "Sun, 06 Sep 2026 08:00:10 GMT"},
            None,
        )
        now = datetime(2026, 9, 6, 8, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(10.0, retry_after_seconds(error, now=now))

    @patch("scripts.localize_commons_images_ci.time.sleep")
    @patch("scripts.localize_commons_images_ci.urlopen")
    def test_read_url_retries_429_then_succeeds(self, mock_urlopen, mock_sleep):
        error = HTTPError(
            "https://commons.wikimedia.org/test",
            429,
            "Too Many Requests",
            {"Retry-After": "3"},
            None,
        )
        response = MagicMock()
        response.read.return_value = b"ok"
        response.geturl.return_value = "https://upload.wikimedia.org/test.jpg"
        response.__enter__.return_value = response
        response.__exit__.return_value = False
        mock_urlopen.side_effect = [error, response]

        data, final_url = read_url(
            Request("https://commons.wikimedia.org/test"),
            timeout=5,
            retries=2,
        )

        self.assertEqual(b"ok", data)
        self.assertEqual("https://upload.wikimedia.org/test.jpg", final_url)
        mock_sleep.assert_called_once_with(3.0)

    def test_external_wikimedia_pages_detects_only_external_image_src(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "good.html").write_text(
                '<img src="assets/images/commons/local.webp">',
                encoding="utf-8",
            )
            (root / "bad.html").write_text(
                '<img src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Test.jpg">',
                encoding="utf-8",
            )
            (root / "link.html").write_text(
                '<a href="https://commons.wikimedia.org/wiki/File:Test.jpg">source</a>',
                encoding="utf-8",
            )
            self.assertEqual(["bad.html"], external_wikimedia_pages(root))

    def test_validate_production_build_rejects_failed_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                validate_production_build(
                    {
                        "unique_images_failed": 1,
                        "failure_samples": [
                            {"source_url": "https://example.invalid/image.jpg", "error": "HTTPError: 429"}
                        ],
                    },
                    Path(tmp),
                )

    def test_validate_production_build_accepts_complete_local_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text(
                '<img src="assets/images/commons/local.webp">',
                encoding="utf-8",
            )
            validate_production_build({"unique_images_failed": 0}, root)


if __name__ == "__main__":
    unittest.main()
