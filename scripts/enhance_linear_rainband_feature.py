# Created: 2026-09-15 09:20 JST
# Updated: 2026-09-21 JST
"""Normalize the linear-rainband special feature's UX, navigation and discovery.

The special pages keep bespoke framing and feature navigation, while reviewed
Markdown now regenerates their article bodies. This pass restores and normalizes
the feature UX after body synchronization and keeps it scalable as regional
child pages grow:

- keep the six core topics in one compact navigation;
- put regional pages in a separate navigation/grid;
- make feature breadcrumbs clickable and hierarchical;
- expose the special from flood and region category hubs;
- align the B067 pillar metadata with its broad "what is it?" search intent;
- normalize the bespoke feature header to the site's shared mega navigation;
- load the shared runtime so mobile navigation and accessibility stay consistent.

The transform is idempotent and is run after the normal preview synchronizer.
"""

from __future__ import annotations

import re
from pathlib import Path

try:  # package import used by tests
    from .sync_previews_from_markdown import apply_site_navigation
except ImportError:  # direct script execution: python scripts/...
    from sync_previews_from_markdown import apply_site_navigation

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "preview"

CORE_PAGES = (
    ("B067", "特集トップ", "article_b067.html"),
    ("B068", "全国年表", "article_b068.html"),
    ("B069", "発生数・頻度", "article_b069.html"),
    ("B070", "地域別", "article_b070.html"),
    ("B071", "雨量記録", "article_b071.html"),
    ("B072", "情報制度史", "article_b072.html"),
)

REGION_PAGES = (
    ("B073", "九州", "article_b073.html", "九州北部豪雨・2020年7月豪雨"),
    ("B074", "関東甲信", "article_b074.html", "2015年豪雨・2026年千葉豪雨"),
    ("B075", "中国地方", "article_b075.html", "広島・西日本豪雨・山口"),
    ("B076", "四国", "article_b076.html", "四国南東斜面・高知・徳島"),
    ("B077", "東海", "article_b077.html", "愛知・静岡・三重・伊豆"),
)

PREFECTURE_PAGES = (
    ("B082", "鹿児島県", "article_b082.html", "1993年8月豪雨・2023〜2025年"),
    ("B083", "宮崎県", "article_b083.html", "2024年10月・2025年9月"),
    ("B084", "熊本県", "article_b084.html", "2012年・2020年豪雨と球磨川"),
    ("B085", "長崎県", "article_b085.html", "1982年長崎大水害・2023〜2024年"),
    ("B086", "大分県", "article_b086.html", "2017年九州北部豪雨・2023〜2024年"),
    ("B087", "高知県", "article_b087.html", "多雨地形・2022〜2023年"),
    ("B088", "和歌山県", "article_b088.html", "紀伊半島大水害・2023年"),
    ("B089", "三重県", "article_b089.html", "2023年初発表・2024年台風10号"),
    ("B090", "静岡県", "article_b090.html", "2022〜2025年の大雨史"),
    ("B091", "千葉県", "article_b091.html", "2023年・2026年千葉豪雨"),
    ("B092", "東京都", "article_b092.html", "2005年都市豪雨・地下空間"),
    ("B093", "大阪府", "article_b093.html", "2012年豪雨・都市型水害"),
    ("B094", "愛知県", "article_b094.html", "東海豪雨・名古屋の水害"),
    ("B095", "石川県", "article_b095.html", "能登・金沢・2023〜2026年"),
    ("B096", "富山県", "article_b096.html", "2023・2026年・急流河川"),
)

CURRENT_LABEL = {
    "B067": "線状降水帯特集",
    "B068": "全国年表",
    "B069": "発生数・頻度",
    "B070": "地域別",
    "B071": "雨量記録",
    "B072": "情報制度史",
    "B073": "九州",
    "B074": "関東甲信",
    "B075": "中国地方",
    "B076": "四国",
    "B077": "東海",
    "B082": "鹿児島県",
    "B083": "宮崎県",
    "B084": "熊本県",
    "B085": "長崎県",
    "B086": "大分県",
    "B087": "高知県",
    "B088": "和歌山県",
    "B089": "三重県",
    "B090": "静岡県",
    "B091": "千葉県",
    "B092": "東京都",
    "B093": "大阪府",
    "B094": "愛知県",
    "B095": "石川県",
    "B096": "富山県",
}

FEATURE_STYLE = """<style id="linear-rainband-feature-review-styles">
.feature-nav{display:flex!important;flex-wrap:wrap;gap:8px;margin:14px 0 24px}
.feature-nav a,.feature-region-nav a{display:inline-flex;align-items:center;min-height:40px;padding:8px 11px;border:1px solid var(--line);border-radius:999px;background:#fff;font-weight:700;text-decoration:none}
.feature-nav a[aria-current="page"],.feature-region-nav a[aria-current="page"]{background:var(--primary-soft);border-color:rgba(23,107,104,.35);color:var(--primary-dark)}
.feature-region-nav{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 26px;padding:12px;border:1px solid var(--line);border-radius:14px;background:#f8fafb}
.feature-region-panel{margin:24px 0 30px;padding:18px;border:1px solid var(--line);border-radius:16px;background:linear-gradient(135deg,#f6fbfb,#fff)}
.feature-region-panel h2{margin-top:0}
.feature-region-panel>p{margin:6px 0 14px;color:var(--muted)}
.feature-region-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.feature-region-card{display:flex;min-height:92px;flex-direction:column;justify-content:center;gap:5px;padding:13px 14px;border:1px solid var(--line);border-radius:12px;background:#fff;color:var(--text);text-decoration:none}
.feature-region-card strong{color:var(--primary-dark)}
.feature-region-card span{font-size:.82rem;line-height:1.45;color:var(--muted)}
.feature-region-card:hover,.feature-region-card:focus-visible{background:var(--primary-soft);border-color:rgba(23,107,104,.3)}
.linear-feature-promo{margin:22px 0 30px;padding:18px;border:1px solid rgba(23,107,104,.24);border-radius:16px;background:linear-gradient(135deg,var(--primary-soft),#fff)}
.linear-feature-promo h2{margin:0 0 8px}
.linear-feature-promo p{margin:0 0 14px}
.linear-feature-promo__actions{display:flex;flex-wrap:wrap;gap:9px}
.linear-feature-promo__actions a{display:inline-flex;align-items:center;min-height:42px;padding:9px 13px;border:1px solid var(--line);border-radius:10px;background:#fff;font-weight:800;text-decoration:none}
.linear-feature-promo .feature-region-grid{margin-top:14px}
@media(max-width:720px){
  .feature-region-grid{grid-template-columns:1fr}
  .feature-region-panel,.linear-feature-promo{padding:15px}
  .feature-nav a,.feature-region-nav a{min-height:44px}
}
</style>"""

NAV_RE = re.compile(
    r'<nav\s+class=["\']feature-(?:region-)?nav["\'][^>]*>.*?</nav>',
    re.IGNORECASE | re.DOTALL,
)
ARTICLE_BODY_OPEN_RE = re.compile(
    r'(<div\s+class=["\'][^"\']*\barticle-body\b[^"\']*["\'][^>]*>)',
    re.IGNORECASE,
)
FEATURE_GLOBAL_NAV_RE = re.compile(
    r'<nav\s+class=["\']feature-global-nav["\'][^>]*>.*?</nav>',
    re.IGNORECASE | re.DOTALL,
)
SITE_NAV_RE = re.compile(
    r'<nav\s+class=["\'][^"\']*\bsite-nav\b[^"\']*["\'][^>]*>',
    re.IGNORECASE,
)
SITE_HEADER_RE = re.compile(
    r'<header\s+class=["\'][^"\']*\bsite-header\b[^"\']*["\'][^>]*>',
    re.IGNORECASE,
)
BREADCRUMB_RE = re.compile(
    r'<nav\s+class=["\']breadcrumb["\'][^>]*>.*?</nav>',
    re.IGNORECASE | re.DOTALL,
)
CATEGORY_HERO_RE = re.compile(
    r'(<header\s+class=["\']category-hero["\'][^>]*>.*?</header>)',
    re.IGNORECASE | re.DOTALL,
)
COMMON_JS_RE = re.compile(
    r'<script\b[^>]*\bsrc=["\'][^"\']*bousai_common\.js["\'][^>]*></script>',
    re.IGNORECASE,
)


def _with_style(html: str) -> str:
    if 'id="linear-rainband-feature-review-styles"' in html:
        return html
    return html.replace("</head>", FEATURE_STYLE + "\n</head>", 1)


def _with_common_runtime(html: str) -> str:
    """Move complete feature pages onto the site's shared header/runtime contract."""
    placeholder = '<nav class="site-nav" aria-label="メインナビゲーション"></nav>'
    if FEATURE_GLOBAL_NAV_RE.search(html):
        html = FEATURE_GLOBAL_NAV_RE.sub(placeholder, html, count=1)
    elif SITE_HEADER_RE.search(html) and not SITE_NAV_RE.search(html):
        # B073-B077 were created with a branded header but no global nav at all.
        # Only complete pages get structural header repair; unit-test HTML
        # fragments without site-header continue through the content transform.
        marker = "</div></header>"
        if marker not in html:
            raise ValueError("site header missing expected closing marker")
        html = html.replace(marker, placeholder + marker, 1)

    if not COMMON_JS_RE.search(html) and "</head>" in html:
        html = html.replace(
            "</head>",
            '<script src="bousai_common.js" defer></script>\n</head>',
            1,
        )
    return html


def _link(href: str, label: str, active: bool = False) -> str:
    current = ' aria-current="page"' if active else ""
    return f'<a href="{href}"{current}>{label}</a>'


def core_nav(current_id: str) -> str:
    links = "".join(
        _link(href, label, article_id == current_id)
        for article_id, label, href in CORE_PAGES
    )
    return (
        '<nav class="feature-nav" aria-label="線状降水帯特集の主要テーマ">'
        + links
        + "</nav>"
    )


def region_nav(current_id: str) -> str:
    links = [
        _link("article_b067.html", "特集トップ"),
        _link("article_b070.html", "地域別トップ"),
    ]
    links.extend(
        _link(href, label, article_id == current_id)
        for article_id, label, href, _caption in REGION_PAGES
    )
    return (
        '<nav class="feature-region-nav" aria-label="線状降水帯の地域別記事">'
        + "".join(links)
        + "</nav>"
    )


def region_panel() -> str:
    cards = "".join(
        f'<a class="feature-region-card" href="{href}"><strong>{label}</strong>'
        f"<span>{caption}</span></a>"
        for _article_id, label, href, caption in REGION_PAGES
    )
    prefecture_cards = "".join(
        f'<a class="feature-region-card" href="{href}"><strong>{label}</strong>'
        f"<span>{caption}</span></a>"
        for _article_id, label, href, caption in PREFECTURE_PAGES
    )
    return (
        '<section class="feature-region-panel" id="linear-rainband-region-panel">'
        "<h2>地域から線状降水帯を見る</h2>"
        "<p>全国傾向を確認した後、地方ごとの主な事例・地域差・防災情報の確認ポイントへ進めます。</p>"
        '<div class="feature-region-grid">'
        + cards
        + "</div>"
        '<p><a href="article_b070.html">地域別の全体像と発生頻度が高い傾向を見る →</a></p>'
        '<h3>都道府県別の発生史を見る</h3>'
        '<p>県ごとに、線状降水帯の公式事例と、それ以前の代表的な豪雨史、避難場所の確認先を分けて整理します。</p>'
        '<div class="feature-region-grid feature-prefecture-grid">'
        + prefecture_cards
        + "</div>"
        "</section>"
    )


def breadcrumb(article_id: str) -> str:
    current = CURRENT_LABEL[article_id]
    prefix = (
        '<nav class="breadcrumb" aria-label="パンくずリスト">'
        '<a href="index.html">トップ</a> &gt; '
        '<a href="category_flood.html">台風・水害</a> &gt; '
    )
    if article_id == "B067":
        return prefix + "線状降水帯特集</nav>"
    if article_id in {"B073", "B074", "B075", "B076", "B077"}:
        return (
            prefix
            + '<a href="article_b067.html">線状降水帯特集</a> &gt; '
            + '<a href="article_b070.html">地域別</a> &gt; '
            + current
            + "</nav>"
        )
    if article_id in {"B082", "B083", "B084", "B085", "B086", "B087", "B088", "B089", "B090", "B091"}:
        return (
            prefix
            + '<a href="article_b067.html">線状降水帯特集</a> &gt; '
            + '<a href="article_b070.html">地域別</a> &gt; '
            + current
            + "</nav>"
        )
    return (
        prefix
        + '<a href="article_b067.html">線状降水帯特集</a> &gt; '
        + current
        + "</nav>"
    )


def _ensure_feature_nav(html: str, nav: str, article_id: str) -> str:
    if NAV_RE.search(html):
        return NAV_RE.sub(nav, html, count=1)
    if not ARTICLE_BODY_OPEN_RE.search(html):
        raise ValueError(f"article-body not found while inserting feature nav: {article_id}")
    return ARTICLE_BODY_OPEN_RE.sub(
        lambda match: match.group(1) + "\n" + nav,
        html,
        count=1,
    )


def enhance_feature_page(html: str, article_id: str) -> str:
    html = _with_common_runtime(_with_style(html))
    html = BREADCRUMB_RE.sub(breadcrumb(article_id), html, count=1)

    desired_nav = (
        region_nav(article_id)
        if article_id in {"B073", "B074", "B075", "B076", "B077", "B082", "B083", "B084", "B085", "B086", "B087", "B088", "B089", "B090", "B091"}
        else core_nav(article_id)
    )
    html = _ensure_feature_nav(html, desired_nav, article_id)

    if article_id in {"B067", "B070"} and 'id="linear-rainband-region-panel"' not in html:
        marker = core_nav(article_id)
        html = html.replace(marker, marker + region_panel(), 1)

    if article_id == "B067":
        html = re.sub(
            r"<title>.*?</title>",
            "<title>線状降水帯とは？過去事例・発生数・多い地域・雨量記録をデータで見る｜防災くらしガイド</title>",
            html,
            count=1,
            flags=re.DOTALL,
        )
        html = re.sub(
            r'<meta\s+name="description"\s+content="[^"]*">',
            '<meta name="description" content="線状降水帯とは何かを、過去事例・発生数・多い地域・雨量記録・情報制度から整理。九州・関東甲信・中国・四国・東海の地域別記事も案内します。">',
            html,
            count=1,
            flags=re.IGNORECASE,
        )
        html = re.sub(
            r"<h1>.*?</h1>",
            "<h1>線状降水帯とは？過去事例・発生数・多い地域・雨量記録をデータで見る</h1>",
            html,
            count=1,
            flags=re.DOTALL,
        )
        html = re.sub(
            r'<p\s+class="article-lead"[^>]*>.*?</p>',
            '<p class="article-lead">線状降水帯とは何かを入口に、<strong>過去事例・発生数・多い地域・雨量記録・情報制度</strong>を整理します。全国像から地域別記事まで、知りたいテーマへ直接進めます。</p>',
            html,
            count=1,
            flags=re.DOTALL | re.IGNORECASE,
        )
    return html


def homepage_feature_promo() -> str:
    return """<section class="home-feature-spotlight" id="linear-rainband-home-feature" aria-labelledby="linear-rainband-home-title">
<div>
<span class="home-feature-spotlight__label">注目特集</span>
<h2 id="linear-rainband-home-title">線状降水帯を知る</h2>
<p>線状降水帯とは何か、過去事例、発生数、地域差、雨量記録、2026年からの情報制度までまとめて確認できます。</p>
</div>
<div class="home-feature-spotlight__actions">
<a href="article_b067.html">特集を見る</a>
<a href="article_b070.html">地域別を見る</a>
</div>
</section>"""


def enhance_homepage(html: str) -> str:
    if 'id="linear-rainband-home-feature"' in html:
        return html
    marker = '  <section class="section">\n    <div class="section-heading"><div><h2>ピックアップ</h2>'
    if marker not in html:
        raise ValueError("homepage pickup marker missing while inserting linear-rainband feature")
    return html.replace(marker, homepage_feature_promo() + "\n\n" + marker, 1)


def flood_category_promo() -> str:
    return """<section class="linear-feature-promo" id="linear-rainband-feature-entry">
<h2>注目特集：線状降水帯</h2>
<p>「線状降水帯とは何か」から、過去事例、発生数、多い地域、雨量記録、情報制度までを一つの特集で整理しています。</p>
<div class="linear-feature-promo__actions">
<a href="article_b067.html">線状降水帯特集を見る</a>
<a href="article_b070.html">地域別に見る</a>
</div>
</section>"""


def region_category_promo() -> str:
    cards = "".join(
        f'<a class="feature-region-card" href="{href}"><strong>{label}</strong>'
        f"<span>{caption}</span></a>"
        for _article_id, label, href, caption in REGION_PAGES
    )
    return (
        '<section class="linear-feature-promo" id="linear-rainband-region-entry">'
        "<h2>線状降水帯を地域から見る</h2>"
        "<p>災害史とは別に、線状降水帯の発生傾向と主な事例を地方別に整理した特集があります。</p>"
        '<div class="linear-feature-promo__actions">'
        '<a href="article_b070.html">地域別の全体像を見る</a>'
        '<a href="article_b067.html">特集トップを見る</a>'
        "</div>"
        '<div class="feature-region-grid">'
        + cards
        + "</div></section>"
    )


def insert_after_category_hero(html: str, block: str, block_id: str) -> str:
    html = _with_style(html)
    if f'id="{block_id}"' in html:
        return html
    return CATEGORY_HERO_RE.sub(lambda m: m.group(1) + "\n" + block, html, count=1)


def enhance_category_flood(html: str) -> str:
    return insert_after_category_hero(
        html, flood_category_promo(), "linear-rainband-feature-entry"
    )


def enhance_category_region(html: str) -> str:
    html = html.replace(
        "現在は8地域・8記事を掲載しています。",
        "災害史記事は現在8地域・8記事を掲載しています。線状降水帯の地域別特集は別枠で案内します。",
    )
    return insert_after_category_hero(
        html, region_category_promo(), "linear-rainband-region-entry"
    )


def _write_if_changed(path: Path, updated: str) -> bool:
    current = path.read_text(encoding="utf-8")
    if current == updated:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def enhance() -> list[str]:
    changed: list[str] = []
    for number in list(range(67, 78)) + list(range(82, 97)):
        article_id = f"B{number:03d}"
        path = PREVIEW / f"article_b{number:03d}.html"
        current = path.read_text(encoding="utf-8")
        if _write_if_changed(path, enhance_feature_page(current, article_id)):
            changed.append(path.name)

    home_path = PREVIEW / "index.html"
    home = home_path.read_text(encoding="utf-8")
    if _write_if_changed(home_path, enhance_homepage(home)):
        changed.append(home_path.name)

    flood_path = PREVIEW / "category_flood.html"
    flood = flood_path.read_text(encoding="utf-8")
    if _write_if_changed(flood_path, enhance_category_flood(flood)):
        changed.append(flood_path.name)

    region_path = PREVIEW / "category_region.html"
    region = region_path.read_text(encoding="utf-8")
    if _write_if_changed(region_path, enhance_category_region(region)):
        changed.append(region_path.name)

    # The feature's old global nav is converted to a site-nav placeholder above.
    # Regional children that had no global nav receive the same placeholder.
    # Render the same three-hub mega navigation and assets used everywhere else.
    for nav_change in apply_site_navigation():
        filename = nav_change.removeprefix("NAV:")
        if filename not in changed:
            changed.append(filename)

    return changed


def main() -> int:
    changed = enhance()
    if changed:
        print("Enhanced linear-rainband feature UX: " + ", ".join(changed))
    else:
        print("Linear-rainband feature UX already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())