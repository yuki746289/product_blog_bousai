# Created: 2026-09-09 14:52 JST
# Updated: 2026-09-10 12:05 JST
"""Compatibility wrapper around the preview synchronizer.

Markdown is the editorial source of truth. The reviewed core regenerates full
article bodies only for pages where that is safe. Some preview pages retain
bespoke hand-built bodies, but their public ``article-lead`` must still follow
the reviewed Markdown introduction rather than drift as a separate copy.

This wrapper therefore:

1. extends full-body synchronization for reviewed articles omitted from the
   original core set;
2. synchronizes the lead for every B001-B060 page from its Markdown intro;
3. normalizes every article breadcrumb so its category is a real, clickable
   published category rather than an unlinked display-only label;
4. inserts a breadcrumb when an older bespoke preview omitted it entirely;
5. presents three clickable top-level discovery hubs and exposes their child
   categories through desktop hover/focus and mobile accordion controls;
6. presents desktop child categories as horizontal summary cards that wrap to
   two rows when needed, while keeping the mobile accordion compact;
7. merges the user-facing 台風 / 大雨・水害 routes into one 台風・水害 category;
8. keeps article breadcrumbs flat so users can still move directly between
   individual categories and articles without a mandatory hub-page layer.

There are no article-specific lead overrides. If an article lead needs editorial
improvement, update the Markdown introduction itself so source, review and public
output remain a single chain of truth.
"""

from __future__ import annotations

import argparse
import html as html_lib
import re
from pathlib import Path

try:  # package import used by tests
    from . import sync_previews_core as _core
    from .sync_previews_core import *  # noqa: F401,F403
except ImportError:  # direct script execution: python scripts/...
    import sync_previews_core as _core
    from sync_previews_core import *  # type: ignore # noqa: F401,F403

EXTRA_SYNC_ARTICLE_IDS = {"B003", "B008", "B010", "B058"}
_core.SYNC_ARTICLE_IDS.update(EXTRA_SYNC_ARTICLE_IDS)
SYNC_ARTICLE_IDS = _core.SYNC_ARTICLE_IDS
ALL_ARTICLE_IDS = {f"B{i:03d}" for i in range(1, 61)}

# Three discovery hubs keep the always-visible header compact. Each hub is a
# normal clickable page; its child categories are also reachable directly from
# the dropdown/accordion, so the hub layer is never mandatory.
SITE_NAV_GROUPS = (
    (
        "災害から探す",
        "category_disaster_situations.html",
        (
            ("台風・水害", "category_flood.html", "強風・大雨・洪水・高潮"),
            ("地震", "category_earthquake.html", "揺れ・津波・家具転倒"),
            ("停電・断水", "category_outage.html", "電源・飲料水・携帯トイレ"),
            ("被災後・復旧", "category_post_disaster.html", "記録・片付け・保険確認"),
        ),
    ),
    (
        "暮らし・備えから探す",
        "category_life.html",
        (
            ("防災入門", "category_guide.html", "備蓄・持ち出し・家族の備え"),
            ("車と災害", "category_vehicle.html", "冠水・車中泊・車載用品"),
            ("住宅と災害", "category_home.html", "浸水・マンション・家具"),
            ("保険・お金", "category_insurance.html", "火災保険・地震保険・補償"),
            ("防災グッズ", "category_goods.html", "電源・ラジオ・衛生用品"),
        ),
    ),
    (
        "地域・疑問から探す",
        "category_region_qa.html",
        (
            ("地域別", "category_region.html", "地域の災害史と備え"),
            ("Q&A", "qa.html", "よくある疑問から素早く確認"),
        ),
    ),
)
SITE_NAV_LINKS = tuple(
    (label, href)
    for _group_label, _hub, links in SITE_NAV_GROUPS
    for label, href, _caption in links
)

# Canonical visible article-category destinations in preview. Both internal
# typhoon/flood taxonomies now resolve to the same user-facing category.
CATEGORY_PREVIEW_BREADCRUMBS = {
    "guide": ("防災入門", "category_guide.html"),
    "water-outage": ("停電・断水", "category_outage.html"),
    "blackout": ("停電・断水", "category_outage.html"),
    "flood": ("台風・水害", "category_flood.html"),
    "typhoon": ("台風・水害", "category_flood.html"),
    "earthquake": ("地震", "category_earthquake.html"),
    "vehicle": ("車と災害", "category_vehicle.html"),
    "insurance": ("保険・お金", "category_insurance.html"),
    "home": ("住宅と災害", "category_home.html"),
    "post-disaster": ("被災後・復旧", "category_post_disaster.html"),
    "goods": ("防災グッズ", "category_goods.html"),
}

# Individual category pages remain top-level article destinations.
# category_typhoon is retained only as a compatibility landing page for the
# historical /typhoon/ URL. Hub pages intentionally do not become article
# breadcrumb parents.
CATEGORY_PAGE_HIERARCHY = {
    "category_guide.html": (None, None, "防災入門"),
    "category_typhoon.html": (None, None, "台風"),
    "category_flood.html": (None, None, "台風・水害"),
    "category_earthquake.html": (None, None, "地震"),
    "category_outage.html": (None, None, "停電・断水"),
    "category_post_disaster.html": (None, None, "被災後・復旧"),
    "category_vehicle.html": (None, None, "車と災害"),
    "category_home.html": (None, None, "住宅と災害"),
    "category_insurance.html": (None, None, "保険・お金"),
    "category_goods.html": (None, None, "防災グッズ"),
    "category_region.html": (None, None, "地域別"),
}

BREADCRUMB_RE = re.compile(
    r'<nav\s+class=["\']breadcrumb["\'][^>]*>(?P<body>.*?)</nav>',
    re.IGNORECASE | re.DOTALL,
)
SITE_NAV_RE = re.compile(
    r'<nav\s+class=["\']site-nav["\'][^>]*>.*?</nav>',
    re.IGNORECASE | re.DOTALL,
)
NAV_STYLE_RE = re.compile(
    r'<style\s+id=["\']bousai-nav-group-styles["\']>.*?</style>',
    re.IGNORECASE | re.DOTALL,
)
NAV_SCRIPT_RE = re.compile(
    r'<script\s+id=["\']bousai-mega-nav-script["\']>.*?</script>',
    re.IGNORECASE | re.DOTALL,
)
HOME_TY_FLOOD_CARDS_RE = re.compile(
    r'<article class="topic-card">\s*'
    r'<a class="topic-card__thumb" href="category_typhoon\.html".*?</article>\s*'
    r'<article class="topic-card">\s*'
    r'<a class="topic-card__thumb" href="category_flood\.html".*?</article>',
    re.IGNORECASE | re.DOTALL,
)
MAIN_OPEN_RE = re.compile(r"<main\b[^>]*>", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")

NAV_GROUP_STYLE = """<style id="bousai-nav-group-styles">
.site-nav { overflow: visible; gap: 10px; }
.site-nav__mega-group { position: relative; display: inline-block; }
.site-nav__mega-head { display: flex; align-items: center; gap: 2px; }
.site-nav__mega-link {
  display: inline-flex;
  min-height: 40px;
  align-items: center;
  padding: 7px 8px;
  border-radius: 8px;
}
.site-nav__mega-link:hover,
.site-nav__mega-link:focus-visible,
.site-nav__mega-link[aria-current] { background: var(--primary-soft); color: var(--primary-dark); }
.site-nav__submenu-toggle {
  display: inline-flex;
  min-width: 34px;
  min-height: 34px;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: 0;
  border-radius: 8px;
  background: transparent;
  color: var(--muted);
  font: inherit;
  cursor: pointer;
}
.site-nav__submenu-toggle:hover,
.site-nav__submenu-toggle:focus-visible,
.site-nav__submenu-toggle[aria-expanded="true"] { background: var(--primary-soft); color: var(--primary-dark); }
.site-nav__submenu-toggle:focus-visible { outline: 3px solid rgba(23,107,104,.24); outline-offset: 2px; }
.site-nav__submenu-toggle span { transition: transform .16s ease; }
.site-nav__submenu-toggle[aria-expanded="true"] span { transform: rotate(180deg); }
.site-nav__submenu {
  position: absolute;
  z-index: 60;
  top: calc(100% + 2px);
  left: 0;
  display: none;
  width: min(720px, calc(100vw - 32px));
  padding: 12px;
  gap: 9px;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 14px;
  box-shadow: 0 14px 34px rgba(31,42,48,.15);
  white-space: normal;
}
.site-nav__mega-group[data-items="2"] .site-nav__submenu {
  width: min(460px, calc(100vw - 32px));
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
.site-nav__mega-group[data-items="4"] .site-nav__submenu {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}
.site-nav__mega-group[data-items="5"] .site-nav__submenu {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}
.site-nav__mega-group:nth-child(2) .site-nav__submenu { left: 50%; transform: translateX(-50%); }
.site-nav__mega-group:last-child .site-nav__submenu { left: auto; right: 0; transform: none; }
.site-nav__submenu-card {
  display: flex;
  min-width: 0;
  min-height: 82px;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  padding: 12px 13px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: #fff;
  color: var(--text);
  line-height: 1.4;
}
.site-nav__submenu-card strong { font-size: .94rem; color: var(--primary-dark); }
.site-nav__submenu-caption { display: block; font-size: .78rem; color: var(--muted); font-weight: 500; line-height: 1.45; }
.site-nav__submenu-card:hover,
.site-nav__submenu-card:focus-visible,
.site-nav__submenu-card[aria-current] { background: var(--primary-soft); border-color: rgba(23,107,104,.28); color: var(--primary-dark); }
.site-nav__mega-group:hover > .site-nav__submenu,
.site-nav__mega-group:focus-within > .site-nav__submenu,
.site-nav__mega-group.is-submenu-open > .site-nav__submenu { display: grid; }
.hub-category-jump {
  display: grid;
  gap: 10px;
  margin: 20px 0 30px;
}
.hub-category-jump[data-items="2"] { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.hub-category-jump[data-items="4"] { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.hub-category-jump[data-items="5"] { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.hub-category-jump__card {
  display: flex;
  min-height: 92px;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  padding: 14px 15px;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 4px 14px rgba(31,42,48,.05);
  color: var(--text);
}
.hub-category-jump__card strong { color: var(--primary-dark); font-size: 1rem; }
.hub-category-jump__card span { color: var(--muted); font-size: .82rem; line-height: 1.5; }
.hub-category-jump__card:hover,
.hub-category-jump__card:focus-visible { background: var(--primary-soft); border-color: rgba(23,107,104,.3); }
.category-hub .category-section[id] { scroll-margin-top: 105px; }
@media (min-width: 721px) and (max-width: 920px) {
  .site-nav__mega-group[data-items] .site-nav__submenu {
    width: min(620px, calc(100vw - 28px));
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .hub-category-jump[data-items="4"],
  .hub-category-jump[data-items="5"] { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 720px) {
  .site-nav.mobile-nav-enhanced { overflow: visible; }
  .site-nav.mobile-nav-enhanced .site-nav__mega-group {
    display: block;
    width: 100%;
    border-bottom: 1px solid var(--line);
  }
  .site-nav.mobile-nav-enhanced .site-nav__mega-head {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 48px;
    gap: 0;
  }
  .site-nav.mobile-nav-enhanced .site-nav__mega-link {
    min-height: 48px;
    padding: 12px 10px;
    border-bottom: 0;
    border-radius: 0;
    font-weight: 800;
  }
  .site-nav.mobile-nav-enhanced .site-nav__submenu-toggle {
    width: 48px;
    min-width: 48px;
    min-height: 48px;
    border-left: 1px solid var(--line);
    border-radius: 0;
  }
  .site-nav.mobile-nav-enhanced .site-nav__submenu,
  .site-nav.mobile-nav-enhanced .site-nav__mega-group[data-items] .site-nav__submenu {
    position: static;
    display: none;
    width: auto;
    min-width: 0;
    padding: 6px 8px 9px 18px;
    grid-template-columns: 1fr;
    gap: 5px;
    background: #f8fafb;
    border: 0;
    border-top: 1px solid var(--line);
    border-radius: 0;
    box-shadow: none;
    transform: none;
  }
  .site-nav.mobile-nav-enhanced .site-nav__mega-group:hover > .site-nav__submenu,
  .site-nav.mobile-nav-enhanced .site-nav__mega-group:focus-within > .site-nav__submenu { display: none; }
  .site-nav.mobile-nav-enhanced .site-nav__mega-group.is-submenu-open > .site-nav__submenu { display: grid; }
  .site-nav.mobile-nav-enhanced .site-nav__submenu-card {
    min-height: 54px;
    padding: 9px 10px;
    border: 0;
    border-bottom: 1px solid var(--line);
    border-radius: 0;
    background: transparent;
  }
  .site-nav.mobile-nav-enhanced .site-nav__submenu-card:last-child { border-bottom: 0; }
  .site-nav.mobile-nav-enhanced .site-nav__submenu-caption { font-size: .76rem; }
  .hub-category-jump[data-items] { grid-template-columns: 1fr; }
  .hub-category-jump__card { min-height: 76px; padding: 12px 13px; }
}
@media (prefers-reduced-motion: reduce) {
  .site-nav__submenu-toggle span { transition: none; }
}
</style>"""

NAV_GROUP_SCRIPT = """<script id="bousai-mega-nav-script">
(function () {
  function setGroupState(group, expanded) {
    if (!group) return;
    var button = group.querySelector('.site-nav__submenu-toggle');
    var isExpanded = Boolean(expanded);
    group.classList.toggle('is-submenu-open', isExpanded);
    if (button) {
      button.setAttribute('aria-expanded', isExpanded ? 'true' : 'false');
      var label = group.getAttribute('data-group-label') || 'カテゴリ';
      button.setAttribute('aria-label', label + (isExpanded ? 'のカテゴリを閉じる' : 'のカテゴリを開く'));
    }
  }

  function closeOtherGroups(current) {
    document.querySelectorAll('.site-nav__mega-group.is-submenu-open').forEach(function (group) {
      if (group !== current) setGroupState(group, false);
    });
  }

  function initMegaNavigation() {
    var groups = Array.prototype.slice.call(document.querySelectorAll('.site-nav__mega-group'));
    groups.forEach(function (group) {
      var button = group.querySelector('.site-nav__submenu-toggle');
      if (!button || button.dataset.megaNavBound === '1') return;
      button.dataset.megaNavBound = '1';
      button.addEventListener('click', function (event) {
        event.preventDefault();
        event.stopPropagation();
        var expanded = button.getAttribute('aria-expanded') === 'true';
        closeOtherGroups(group);
        setGroupState(group, !expanded);
      });
    });

    document.addEventListener('click', function (event) {
      groups.forEach(function (group) {
        if (!group.contains(event.target)) setGroupState(group, false);
      });
    });

    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape') return;
      var active = document.activeElement;
      var activeGroup = active && active.closest ? active.closest('.site-nav__mega-group') : null;
      groups.forEach(function (group) { setGroupState(group, false); });
      if (activeGroup) {
        var button = activeGroup.querySelector('.site-nav__submenu-toggle');
        if (button) button.focus();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMegaNavigation);
  } else {
    initMegaNavigation();
  }
})();
</script>"""

HOME_TY_FLOOD_CARD = """<article class="topic-card" data-category="typhoon-flood">
        <a class="topic-card__thumb" href="category_flood.html"><img src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Bavi%202026-07-05%200620Z.png?width=960" alt="台風の衛星画像" loading="lazy"></a>
        <h3><a href="category_flood.html">台風・水害</a></h3><p>強風・大雨・洪水・高潮・浸水をまとめて確認。</p>
        <div class="topic-card__articles">
          <a href="article_b006.html">台風が来る前に何をする？</a>
          <a href="article_b005.html">大雨・水害にどう備える？</a>
          <a href="article_b042.html" data-article-id="B042">河川氾濫はいつ避難する？</a>
        </div>
        <a class="topic-card__more" href="category_flood.html">台風・水害の記事をすべて見る →</a>
      </article>"""


def _replace_lead(preview: str, rendered: str, article_id: str, preview_path: Path) -> str:
    match = _core.LEAD_RE.search(preview)
    if not match:
        raise ValueError(f"article-lead not found for {article_id}: {preview_path}")
    return (
        preview[: match.start()]
        + match.group("open")
        + rendered
        + match.group("close")
        + preview[match.end() :]
    )


def apply_markdown_leads() -> list[str]:
    """Synchronize every B001-B060 public lead from its Markdown introduction."""
    registry = _core.load_registry(_core.REGISTRY)
    aliases = _core.preview_aliases(registry)
    by_id = {article["article_id"]: article for article in registry["articles"]}
    missing = ALL_ARTICLE_IDS - set(by_id)
    if missing:
        raise ValueError(f"registry missing article ids: {sorted(missing)}")

    changed: list[str] = []
    for article_id in sorted(ALL_ARTICLE_IDS):
        article = by_id[article_id]
        source_path = _core.ROOT / article["source_path"]
        preview_path = _core.ROOT / article["preview_path"]
        markdown = source_path.read_text(encoding="utf-8")
        intro, _ = _core.parse_source(markdown)
        if not intro:
            raise ValueError(f"Markdown introduction is empty for {article_id}: {source_path}")

        preview = preview_path.read_text(encoding="utf-8")
        rendered = _core.inline_markup(intro, aliases)
        updated = _replace_lead(preview, rendered, article_id, preview_path)
        if updated != preview:
            preview_path.write_text(updated, encoding="utf-8")
            changed.append(article_id)
    return changed


def _current_breadcrumb_label(match: re.Match[str], article: dict) -> str:
    """Keep the concise current-page crumb while replacing its category parent."""
    visible = html_lib.unescape(TAG_RE.sub("", match.group("body")))
    parts = [part.strip() for part in visible.split(">") if part.strip()]
    if len(parts) >= 2:
        return parts[-1]
    return article["title"]


def _breadcrumb_markup(category_name: str, category_preview: str, current_label: str) -> str:
    return (
        '<nav class="breadcrumb" aria-label="パンくずリスト">'
        '<a href="index.html">トップ</a> &gt; '
        f'<a href="{category_preview}">{html_lib.escape(category_name)}</a> &gt; '
        f"{html_lib.escape(current_label)}</nav>"
    )


def apply_article_breadcrumbs() -> list[str]:
    """Link or insert every article breadcrumb to its canonical published category."""
    registry = _core.load_registry(_core.REGISTRY)
    by_id = {article["article_id"]: article for article in registry["articles"]}
    missing = ALL_ARTICLE_IDS - set(by_id)
    if missing:
        raise ValueError(f"registry missing article ids: {sorted(missing)}")

    changed: list[str] = []
    for article_id in sorted(ALL_ARTICLE_IDS):
        article = by_id[article_id]
        category = article.get("category")
        category_info = CATEGORY_PREVIEW_BREADCRUMBS.get(category)
        if not category_info:
            raise ValueError(f"breadcrumb category mapping missing for {article_id}: {category!r}")
        category_name, category_preview = category_info
        category_path = _core.ROOT / "preview" / category_preview
        if not category_path.exists():
            raise FileNotFoundError(
                f"breadcrumb category page missing for {article_id}: {category_path}"
            )

        preview_path = _core.ROOT / article["preview_path"]
        preview = preview_path.read_text(encoding="utf-8")
        match = BREADCRUMB_RE.search(preview)
        if match:
            current_label = _current_breadcrumb_label(match, article)
            replacement = _breadcrumb_markup(category_name, category_preview, current_label)
            updated = preview[: match.start()] + replacement + preview[match.end() :]
        else:
            main_match = MAIN_OPEN_RE.search(preview)
            if not main_match:
                raise ValueError(f"main element not found for {article_id}: {preview_path}")
            replacement = _breadcrumb_markup(category_name, category_preview, article["title"])
            updated = preview[: main_match.end()] + replacement + preview[main_match.end() :]

        if updated != preview:
            preview_path.write_text(updated, encoding="utf-8")
            changed.append(article_id)
    return changed


def _site_nav_markup() -> str:
    chunks: list[str] = []
    for index, (group_label, group_href, links) in enumerate(SITE_NAV_GROUPS, start=1):
        submenu_id = f"site-nav-submenu-{index}"
        child_links = "".join(
            '<a class="site-nav__submenu-card" href="{href}">'
            '<strong>{label}</strong><span class="site-nav__submenu-caption">{caption}</span></a>'.format(
                href=href,
                label=html_lib.escape(label),
                caption=html_lib.escape(caption),
            )
            for label, href, caption in links
        )
        chunks.append(
            f'<div class="site-nav__mega-group" data-group-label="{html_lib.escape(group_label)}" data-items="{len(links)}">'
            '<div class="site-nav__mega-head">'
            f'<a class="site-nav__mega-link" href="{group_href}">{html_lib.escape(group_label)}</a>'
            f'<button class="site-nav__submenu-toggle" type="button" aria-expanded="false" '
            f'aria-controls="{submenu_id}" aria-label="{html_lib.escape(group_label)}のカテゴリを開く">'
            '<span aria-hidden="true">⌄</span></button>'
            '</div>'
            f'<div class="site-nav__submenu" id="{submenu_id}">{child_links}</div>'
            '</div>'
        )
    return '<nav class="site-nav" aria-label="メインナビゲーション">' + "".join(chunks) + "</nav>"


def _apply_nav_assets(html: str) -> str:
    if NAV_STYLE_RE.search(html):
        html = NAV_STYLE_RE.sub(NAV_GROUP_STYLE, html, count=1)
    elif "</head>" in html:
        html = html.replace("</head>", NAV_GROUP_STYLE + "\n</head>", 1)
    else:
        raise ValueError("missing </head> while adding mega navigation styles")

    if NAV_SCRIPT_RE.search(html):
        return NAV_SCRIPT_RE.sub(NAV_GROUP_SCRIPT, html, count=1)
    if "</head>" not in html:
        raise ValueError("missing </head> while adding mega navigation behavior")
    return html.replace("</head>", NAV_GROUP_SCRIPT + "\n</head>", 1)


def apply_site_navigation() -> list[str]:
    """Render three clickable hubs with responsive child-category cards."""
    preview_dir = _core.ROOT / "preview"
    replacement = _site_nav_markup()
    changed: list[str] = []

    for path in sorted(preview_dir.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        if not SITE_NAV_RE.search(html):
            continue
        updated = SITE_NAV_RE.sub(replacement, html, count=1)
        updated = _apply_nav_assets(updated)
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            changed.append(f"NAV:{path.name}")
    return changed


def apply_homepage_typhoon_flood_card() -> list[str]:
    """Replace the two old homepage category cards with one combined entry."""
    path = _core.ROOT / "preview" / "index.html"
    html = path.read_text(encoding="utf-8")
    if 'data-category="typhoon-flood"' in html:
        return []
    match = HOME_TY_FLOOD_CARDS_RE.search(html)
    if not match:
        raise ValueError("homepage typhoon/flood category cards not found")
    updated = html[: match.start()] + HOME_TY_FLOOD_CARD + html[match.end() :]
    path.write_text(updated, encoding="utf-8")
    return ["HOME:typhoon-flood"]


def apply_merged_category_links() -> list[str]:
    """Route every normal internal typhoon-category link to the combined page."""
    preview_dir = _core.ROOT / "preview"
    changed: list[str] = []
    for path in sorted(preview_dir.glob("*.html")):
        if path.name == "category_typhoon.html":
            continue
        html = path.read_text(encoding="utf-8")
        updated = html.replace('href="category_typhoon.html"', 'href="category_flood.html"')
        updated = updated.replace('<strong>台風</strong>', '<strong>台風・水害</strong>')
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            changed.append(f"MERGE:{path.name}")
    return changed


def _category_page_breadcrumb(parent_label: str | None, parent_href: str | None, current_label: str) -> str:
    parts = ['<a href="index.html">トップ</a>']
    if parent_label and parent_href:
        parts.append(f'<a href="{parent_href}">{html_lib.escape(parent_label)}</a>')
    parts.append(html_lib.escape(current_label))
    return '<nav class="breadcrumb" aria-label="パンくずリスト">' + " &gt; ".join(parts) + "</nav>"


def apply_category_page_breadcrumbs() -> list[str]:
    """Keep individual category breadcrumbs flat: top -> category."""
    preview_dir = _core.ROOT / "preview"
    changed: list[str] = []

    for filename, (parent_label, parent_href, current_label) in CATEGORY_PAGE_HIERARCHY.items():
        path = preview_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"category hierarchy page missing: {path}")
        html = path.read_text(encoding="utf-8")
        match = BREADCRUMB_RE.search(html)
        if not match:
            raise ValueError(f"category breadcrumb missing: {path}")
        replacement = _category_page_breadcrumb(parent_label, parent_href, current_label)
        updated = html[: match.start()] + replacement + html[match.end() :]
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            changed.append(f"CATEGORY:{filename}")
    return changed


def sync() -> list[str]:
    changed = _core.sync()
    changed.extend(apply_markdown_leads())
    changed.extend(apply_article_breadcrumbs())
    changed.extend(apply_homepage_typhoon_flood_card())
    changed.extend(apply_merged_category_links())
    changed.extend(apply_site_navigation())
    changed.extend(apply_category_page_breadcrumbs())
    return sorted(set(changed))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if synchronization would change tracked preview files.",
    )
    args = parser.parse_args()

    originals: dict[Path, str] = {}
    if args.check:
        preview_dir = _core.ROOT / "preview"
        for path in sorted(preview_dir.glob("*.html")):
            originals[path] = path.read_text(encoding="utf-8")

    changed = sync()
    print("Synchronized preview content: " + (", ".join(changed) if changed else "none"))

    if args.check and changed:
        for path, original in originals.items():
            path.write_text(original, encoding="utf-8")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())