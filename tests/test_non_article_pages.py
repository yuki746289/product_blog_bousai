# Updated: 2026-09-10 12:08 JST
import re
import unittest
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "preview"

CATEGORY_FILES = [
    "category_guide.html",
    "category_flood.html",
    "category_earthquake.html",
    "category_vehicle.html",
    "category_home.html",
    "category_insurance.html",
    "category_goods.html",
    "category_outage.html",
    "category_post_disaster.html",
    "category_region.html",
]
HUB_FILES = [
    "category_disaster_situations.html",
    "category_life.html",
    "category_region_qa.html",
]
LEGACY_CATEGORY_FILES = ["category_typhoon.html"]
POLICY_FILES = ["about.html", "disclaimer.html", "privacy.html", "advertising.html"]
PRODUCT_FILES = [
    "goods_water_food.html",
    "goods_toilet_hygiene.html",
    "goods_light_information.html",
    "goods_power_charging.html",
]
MEGA_NAV_LABELS = [
    "災害から探す",
    "暮らし・備えから探す",
    "地域・疑問から探す",
]
CHILD_NAV_LINKS = {
    "category_flood.html": "台風・水害",
    "category_earthquake.html": "地震",
    "category_outage.html": "停電・断水",
    "category_post_disaster.html": "被災後・復旧",
    "category_guide.html": "防災入門",
    "category_vehicle.html": "車と災害",
    "category_home.html": "住宅と災害",
    "category_insurance.html": "保険・お金",
    "category_goods.html": "防災グッズ",
    "category_region.html": "地域別",
    "qa.html": "Q&A",
}


def read(name: str) -> str:
    return (PREVIEW / name).read_text(encoding="utf-8")


def nav_html(html: str) -> str:
    match = re.search(
        r'<nav\b[^>]*\bclass=["\'][^"\']*\bsite-nav\b[^"\']*["\'][^>]*>(.*?)</nav>',
        html,
        flags=re.I | re.S,
    )
    return match.group(1) if match else ""


def mega_nav_labels(html: str) -> list[str]:
    nav = nav_html(html)
    return [
        unescape(re.sub(r"<[^>]+>", "", text).strip())
        for text in re.findall(
            r'<a\b[^>]*class=["\'][^"\']*\bsite-nav__mega-link\b[^"\']*["\'][^>]*>(.*?)</a>',
            nav,
            flags=re.I | re.S,
        )
    ]


class NonArticlePageReviewTest(unittest.TestCase):
    def test_static_pages_have_basic_information_architecture(self):
        for name in ["qa.html", *CATEGORY_FILES, *HUB_FILES, *LEGACY_CATEGORY_FILES, *POLICY_FILES, *PRODUCT_FILES]:
            with self.subTest(name=name):
                html = read(name)
                self.assertRegex(html, r"<title>.+?</title>")
                self.assertRegex(html, r'<meta\s+name="description"\s+content="[^"]+"')
                self.assertEqual(len(re.findall(r"<h1\b", html, flags=re.I)), 1)
                self.assertIn('class="site-nav"', html)
                self.assertIn('<main', html)
                self.assertIn('class="breadcrumb"', html)
                self.assertIn('class="site-footer"', html)

    def test_active_category_pages_have_entry_articles_and_related_paths(self):
        for name in CATEGORY_FILES:
            with self.subTest(name=name):
                html = read(name)
                self.assertIn('class="page-shell category-page"', html)
                self.assertIn('class="category-hero"', html)
                self.assertIn('class="official-bar"', html)
                self.assertGreaterEqual(html.count('class="category-article-link'), 1)
                self.assertIn('class="related-category-grid"', html)

    def test_primary_navigation_has_three_clickable_hubs(self):
        expected_hrefs = [
            "category_disaster_situations.html",
            "category_life.html",
            "category_region_qa.html",
        ]
        for name in ["index.html", "category_flood.html", "category_outage.html", "article_b003.html", *HUB_FILES]:
            with self.subTest(name=name):
                html = read(name)
                nav = nav_html(html)
                self.assertEqual(MEGA_NAV_LABELS, mega_nav_labels(html))
                self.assertEqual(3, nav.count('class="site-nav__mega-group"'))
                self.assertEqual(3, nav.count('class="site-nav__submenu-toggle"'))
                for href, label in zip(expected_hrefs, MEGA_NAV_LABELS):
                    self.assertIn(f'class="site-nav__mega-link" href="{href}">{label}</a>', nav)

    def test_dropdowns_keep_every_individual_category_directly_accessible(self):
        nav = nav_html(read("index.html"))
        self.assertEqual(3, nav.count('class="site-nav__submenu"'))
        self.assertEqual(11, nav.count('class="site-nav__submenu-card"'))
        for href, label in CHILD_NAV_LINKS.items():
            display = label if label != "Q&A" else "Q&amp;A"
            pattern = (
                r'<a\b[^>]*class="site-nav__submenu-card"[^>]*'
                rf'href="{re.escape(href)}"[^>]*>\s*'
                rf'<strong>{re.escape(display)}</strong>.*?</a>'
            )
            self.assertRegex(nav, pattern)
        self.assertNotIn('href="category_typhoon.html"', nav)
        self.assertLess(nav.index("category_goods.html"), nav.index("category_region.html"))

    def test_hub_pages_preview_representative_articles_and_all_article_links(self):
        disaster = read("category_disaster_situations.html")
        life = read("category_life.html")
        region_qa = read("category_region_qa.html")

        self.assertIn("<h1>災害から探す</h1>", disaster)
        for category in ["typhoon-flood", "earthquake", "outage", "post-disaster"]:
            self.assertIn(f'data-hub-category="{category}"', disaster)
        for href in ["category_flood.html", "category_earthquake.html", "category_outage.html", "category_post_disaster.html"]:
            self.assertRegex(disaster, rf'href="{re.escape(href)}">[^<]*すべての記事を見る')
        self.assertGreaterEqual(disaster.count('class="category-article-link"'), 12)

        self.assertIn("<h1>暮らし・備えから探す</h1>", life)
        for category in ["guide", "vehicle", "home", "insurance", "goods"]:
            self.assertIn(f'data-hub-category="{category}"', life)
        for href in ["category_guide.html", "category_vehicle.html", "category_home.html", "category_insurance.html", "category_goods.html"]:
            self.assertRegex(life, rf'href="{re.escape(href)}">[^<]*すべての記事を見る')
        self.assertGreaterEqual(life.count('class="category-article-link"'), 15)

        self.assertIn("<h1>地域・疑問から探す</h1>", region_qa)
        self.assertIn('data-hub-category="region"', region_qa)
        self.assertIn('data-hub-category="qa"', region_qa)
        self.assertIn("地域別のすべての記事を見る", region_qa)
        self.assertIn("Q&amp;Aをすべて見る", region_qa)
        self.assertGreaterEqual(region_qa.count('class="category-article-link"'), 4)
        self.assertIn("qa.html#qa-car-insurance", region_qa)
        self.assertIn("qa.html#qa-home-fire-insurance", region_qa)

    def test_typhoon_flood_category_contains_22_unique_articles(self):
        html = read("category_flood.html")
        ids = re.findall(r'data-article-id="(B\d{3})"', html)
        self.assertEqual(22, len(ids))
        self.assertEqual(22, len(set(ids)))
        expected = {
            "B005", "B006", "B008", "B009", "B010", "B012", "B013", "B014",
            "B015", "B016", "B020", "B021", "B022", "B036", "B037", "B042",
            "B043", "B046", "B049", "B050", "B053", "B059",
        }
        self.assertEqual(expected, set(ids))
        self.assertIn("<h1>台風・水害</h1>", html)
        for heading in [
            "台風接近前・強風・高潮",
            "洪水・河川氾濫・土砂災害",
            "自宅・マンションを守る",
            "車と水害",
            "被災後・保険",
            "地域の災害史から備えを考える",
        ]:
            self.assertIn(heading, html)

    def test_old_typhoon_category_is_only_a_compatibility_entry(self):
        html = read("category_typhoon.html")
        self.assertIn("台風カテゴリは「台風・水害」に統合しました", html)
        self.assertIn('href="category_flood.html"', html)
        self.assertIn('rel="canonical" href="https://bousaikun.ashigaru.jp/flood/"', html)

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
        self.assertIn('data-category="typhoon-flood"', html)
        self.assertIn("台風・水害の記事をすべて見る", html)

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

    def test_mobile_navigation_is_accessible_hamburger_with_category_accordions(self):
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

        self.assertIn("bousai-nav-group-styles", home)
        self.assertIn("bousai-mega-nav-script", home)
        self.assertIn('.site-nav.mobile-nav-enhanced .site-nav__submenu', home)
        self.assertIn('.site-nav.mobile-nav-enhanced .site-nav__mega-group.is-submenu-open > .site-nav__submenu', home)
        self.assertIn("setGroupState", home)
        self.assertIn("closeOtherGroups", home)
        self.assertEqual(3, home.count('class="site-nav__submenu-toggle"'))
        for label in MEGA_NAV_LABELS:
            self.assertIn(label, home)


if __name__ == "__main__":
    unittest.main()
