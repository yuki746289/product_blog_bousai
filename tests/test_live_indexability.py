# Created: 2026-09-14 22:40 JST
import unittest
from email.message import Message

from scripts.check_live_indexability import (
    headers_have_noindex,
    html_has_meta_noindex,
    parse_sitemap_urls,
)


class LiveIndexabilityTests(unittest.TestCase):
    def test_meta_robots_noindex_is_detected(self):
        html = '<html><head><meta name="robots" content="noindex,follow"></head></html>'
        self.assertTrue(html_has_meta_noindex(html))

    def test_googlebot_noindex_with_reversed_attribute_order_is_detected(self):
        html = '<meta content="follow noindex" name="googlebot">'
        self.assertTrue(html_has_meta_noindex(html))

    def test_index_follow_is_not_flagged(self):
        html = '<meta name="robots" content="index,follow">'
        self.assertFalse(html_has_meta_noindex(html))

    def test_visible_noindex_text_is_not_flagged(self):
        html = '<main><p>noindex という文字列を説明する本文</p></main>'
        self.assertFalse(html_has_meta_noindex(html))

    def test_x_robots_tag_noindex_is_detected(self):
        headers = Message()
        headers.add_header("X-Robots-Tag", "noindex, follow")
        self.assertTrue(headers_have_noindex(headers))

    def test_x_robots_tag_index_is_not_flagged(self):
        headers = Message()
        headers.add_header("X-Robots-Tag", "index, follow")
        self.assertFalse(headers_have_noindex(headers))

    def test_sitemap_urls_are_parsed_with_namespace(self):
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
          <url><loc>https://example.com/</loc></url>
          <url><loc>https://example.com/a.html</loc></url>
        </urlset>'''
        self.assertEqual(
            ["https://example.com/", "https://example.com/a.html"],
            parse_sitemap_urls(xml),
        )


if __name__ == "__main__":
    unittest.main()
