# Created: 2026-09-14 22:40 JST
# Updated: 2026-09-17 22:17 JST
import unittest
from email.message import Message

from scripts.check_live_indexability import (
    headers_have_noindex,
    html_has_meta_noindex,
    parse_sitemap_urls,
    region_mega_nav_failures,
)


VALID_REGION_NAV = '''
<nav class="site-nav">
  <div class="site-nav__mega-group" data-group-label="地域・疑問から探す" data-items="2">
    <div class="site-nav__mega-head">
      <a class="site-nav__mega-link" href="region/index.html">地域・疑問から探す</a>
    </div>
    <div class="site-nav__submenu" id="site-nav-submenu-3">
      <a class="site-nav__submenu-card" href="region/index.html">
        <strong>地域別</strong><span class="site-nav__submenu-caption">地域の災害史と備え</span>
      </a>
      <a class="site-nav__submenu-card" href="qa/index.html">
        <strong>Q&amp;A</strong><span class="site-nav__submenu-caption">よくある疑問から素早く確認</span>
      </a>
    </div>
  </div>
</nav>
'''


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

    def test_region_mega_nav_valid_structure_passes(self):
        self.assertEqual([], region_mega_nav_failures(VALID_REGION_NAV))

    def test_region_mega_nav_detects_legacy_bare_region_link(self):
        html = VALID_REGION_NAV.replace(
            '</div>\n  </div>\n</nav>',
            '</div><a href="region/index.html">地域別</a>\n  </div>\n</nav>',
        )
        failures = region_mega_nav_failures(html)
        self.assertTrue(any("legacy bare 地域別 link" in failure for failure in failures))

    def test_region_mega_nav_detects_legacy_bare_link_outside_target_group(self):
        html = VALID_REGION_NAV.replace(
            '<nav class="site-nav">',
            '<nav class="site-nav"><a href="region/index.html">地域別</a>',
        )
        failures = region_mega_nav_failures(html)
        self.assertTrue(any("legacy bare 地域別 link" in failure for failure in failures))

    def test_region_mega_nav_detects_duplicate_region_card(self):
        duplicate = '''<a class="site-nav__submenu-card" href="region/index.html">
          <strong>地域別</strong><span>重複</span></a>'''
        html = VALID_REGION_NAV.replace(
            '</div>\n  </div>\n</nav>',
            duplicate + '</div>\n  </div>\n</nav>',
        )
        failures = region_mega_nav_failures(html)
        self.assertTrue(any("card count must be 2" in failure for failure in failures))
        self.assertTrue(any("地域別 card count must be 1" in failure for failure in failures))

    def test_region_mega_nav_detects_wrong_layout_contract(self):
        html = VALID_REGION_NAV.replace('data-items="2"', 'data-items="3"')
        failures = region_mega_nav_failures(html)
        self.assertTrue(any("data-items" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
