import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "preview"

CATEGORY_FILES = [
    "category_guide.html",
    "category_typhoon.html",
    "category_flood.html",
    "category_earthquake.html",
    "category_vehicle.html",
    "category_home.html",
    "category_insurance.html",
    "category_goods.html",
    "category_outage.html",
    "category_post_disaster.html",
]
POLICY_FILES = ["about.html", "disclaimer.html", "privacy.html", "advertising.html"]
PRODUCT_FILES = [
    "goods_water_food.html",
    "goods_toilet_hygiene.html",
    "goods_light_information.html",
    "goods_power_charging.html",
]


def read(name: str) -> str:
    return (PREVIEW / name).read_text(encoding="utf-8")


class NonArticlePageReviewTest(unittest.TestCase):
    def test_static_pages_have_basic_information_architecture(self):
        for name in ["qa.html", *CATEGORY_FILES, *POLICY_FILES, *PRODUCT_FILES]:
            with self.subTest(name=name):
                html = read(name)
                self.assertRegex(html, r"<title>.+?</title>")
                self.assertRegex(html, r'<meta\s+name="description"\s+content="[^"]+"')
                self.assertEqual(len(re.findall(r"<h1\b", html, flags=re.I)), 1)
                self.assertIn('class="site-nav"', html)
                self.assertIn('<main', html)
                self.assertIn('class="breadcrumb"', html)
                self.assertIn('class="site-footer"', html)

    def test_all_category_pages_have_entry_articles_and_related_paths(self):
        for name in CATEGORY_FILES:
            with self.subTest(name=name):
                html = read(name)
                self.assertIn('class="page-shell category-page"', html)
                self.assertIn('class="category-hero"', html)
                self.assertIn('class="official-bar"', html)
                self.assertGreaterEqual(html.count('class="category-article-link'), 1)
                self.assertIn('class="related-category-grid"', html)

    def test_product_pages_keep_information_before_commerce_scaffolding(self):
        forbidden_producer_labels = ["商品候補", "当サイトが選定", "採用理由"]
        for name in PRODUCT_FILES:
            with self.subTest(name=name):
                html = read(name)
                self.assertIn('class="article-shell product-page"', html)
                self.assertIn('class="official-bar"', html)
                self.assertIn('class="affiliate-note"', html)
                self.assertIn('class="amazon-link"', html)
                self.assertIn('class="site-nav"', html)
                for label in forbidden_producer_labels:
                    self.assertNotIn(label, html)

    def test_qa_is_marked_as_summary_entry_point(self):
        html = read("qa.html")
        self.assertIn("Q&amp;Aは概要を素早く確認するための入口", html)
        self.assertGreaterEqual(html.count('class="qa-item"'), 10)
        for block in re.findall(r'<details class="qa-item".*?</details>', html, flags=re.S):
            self.assertRegex(block, r'id="qa-[^"]+"')
            self.assertIn("<summary>", block)
            self.assertIn('class="qa-answer"', block)

    def test_homepage_realtime_copy_and_layout_do_not_regress(self):
        html = read("index.html")
        self.assertIn("data-realtime-root", html)
        self.assertIn("いま確認できる防災情報", html)
        self.assertIn('class="official-bar"', html)
        self.assertNotIn("自動更新", html)
        self.assertNotIn("約10分間隔", html)

    def test_realtime_failure_is_not_rendered_as_no_warning(self):
        js = read("bousai_home.js")
        self.assertIn("warnings: null", js)
        self.assertIn("typhoons: null", js)
        self.assertIn("警報・特別警報の情報を取得できていません", js)
        self.assertIn("台風情報を取得できていません", js)
        self.assertIn("if (successCount === 3)", js)
        self.assertIn("data.checked_at = new Date().toISOString();", js)

    def test_policy_pages_match_actual_site_behavior(self):
        about = read("about.html")
        privacy = read("privacy.html")
        disclaimer = read("disclaimer.html")
        advertising = read("advertising.html")
        self.assertIn("公式の警報・避難情報配信を代替するものではありません", about)
        self.assertIn("リンク先URLやリンク文言", privacy)
        self.assertIn("最新情報を優先", disclaimer)
        self.assertIn("Amazonのアソシエイトとして", advertising)
        self.assertIn("安全情報を商品リンクより優先", advertising)

    def test_common_ui_keeps_accessibility_and_tracking_contract(self):
        js = read("bousai_common.js")
        css = read("bousai_common.css")
        self.assertIn("enhanceAccessibility", js)
        self.assertIn("skip-link", js)
        self.assertIn("aria-current", js)
        self.assertIn('sendAnalyticsEvent("amazon_click"', js)
        self.assertIn('sendAnalyticsEvent("product_guide_click"', js)
        self.assertIn(".skip-link", css)
        self.assertIn("prefers-reduced-motion", css)

    def test_font_size_controls_are_accessible_persistent_and_sitewide(self):
        js = read("bousai_common.js")
        self.assertIn('FONT_SIZE_STORAGE_KEY = "bousai-font-size"', js)
        self.assertIn('label: "普通"', js)
        self.assertIn('label: "大"', js)
        self.assertIn('label: "特大"', js)
        self.assertIn('scale: "112.5%"', js)
        self.assertIn('scale: "125%"', js)
        self.assertIn('group.setAttribute("role", "group")', js)
        self.assertIn('group.setAttribute("aria-label", "文字サイズ")', js)
        self.assertIn('button.setAttribute("aria-pressed"', js)
        self.assertIn("window.localStorage.setItem", js)
        self.assertIn('headerTop.appendChild(group)', js)

    def test_mobile_navigation_is_accessible_hamburger_on_small_screens(self):
        js = read("bousai_common.js")
        home = read("index.html")
        self.assertIn('MOBILE_NAV_MEDIA_QUERY = "(max-width: 720px)"', js)
        self.assertIn('button.className = "mobile-nav-toggle"', js)
        self.assertIn('button.setAttribute("aria-controls", nav.id)', js)
        self.assertIn('button.setAttribute("aria-expanded", "false")', js)
        self.assertIn('button.setAttribute("aria-label", "メニューを開く")', js)
        self.assertIn('nav.classList.add("mobile-nav-enhanced")', js)
        self.assertIn('nav.classList.toggle("is-open", isExpanded)', js)
        self.assertIn('event.key !== "Escape"', js)
        self.assertIn('min-width: 44px', js)
        self.assertIn('.site-nav.mobile-nav-enhanced.is-open', js)
        for label in [
            "防災入門",
            "台風",
            "大雨・水害",
            "地震",
            "車と災害",
            "住宅と災害",
            "保険・お金",
            "防災グッズ",
            "Q&amp;A",
        ]:
            self.assertIn(label, home)


if __name__ == "__main__":
    unittest.main()
