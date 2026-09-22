# Created: 2026-09-03
# Updated: 2026-09-23 JST
"""Article date display and JSON-LD generation for production builds."""

from __future__ import annotations

import html as html_lib
import json
import re
from urllib.parse import urljoin

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ARTICLE_META_RE = re.compile(
    r'<div\s+class=["\']article-meta["\'][^>]*>(?P<body>.*?)</div>',
    re.IGNORECASE | re.DOTALL,
)
SPAN_RE = re.compile(r"<span>(?P<body>.*?)</span>", re.IGNORECASE | re.DOTALL)
DESCRIPTION_RE = re.compile(
    r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
FEATURE_IMAGE_RE = re.compile(
    r'<figure\s+class=["\']article-feature-image["\'][^>]*>.*?'
    r'<img[^>]+src=["\']([^"\']+)["\']',
    re.IGNORECASE | re.DOTALL,
)
GENERATED_JSONLD_RE = re.compile(
    r'<script\s+type=["\']application/ld\+json["\']\s+'
    r'data-generated=["\']article-structured-data["\']>.*?</script>\s*',
    re.IGNORECASE | re.DOTALL,
)

CATEGORY_BREADCRUMBS = {
    "guide": ("防災入門", "guide/index.html"),
    "evacuation": ("避難・避難生活", "evacuation/index.html"),
    "pet": ("避難・避難生活", "evacuation/index.html"),
    "water-outage": ("停電・断水", "outage/index.html"),
    "blackout": ("停電・断水", "outage/index.html"),
    "flood": ("台風・水害", "flood/index.html"),
    "typhoon": ("台風・水害", "flood/index.html"),
    "earthquake": ("地震", "earthquake/index.html"),
    "vehicle": ("車と災害", "vehicle/index.html"),
    "insurance": ("保険・お金", "insurance/index.html"),
    "home": ("住宅と災害", "home/index.html"),
    "post-disaster": ("被災後・復旧", "post-disaster/index.html"),
    "goods": ("防災グッズ", "goods/index.html"),
}

REGION_BREADCRUMB = ("地域別", "region/index.html")
LINEAR_RAINBAND_BREADCRUMB = ("線状降水帯", "special/linear-rainband/index.html")
REGION_ARTICLE_IDS = {"B048", "B049", "B050", "B053", "B054", "B055", "B056", "B059"}

ARTICLE_BREADCRUMB_NAMES = {
    "B001": "防災を始める",
    "B002": "防災リュック",
    "B003": "携帯トイレ",
    "B004": "停電への備え",
    "B005": "大雨・水害の備え",
    "B006": "台風前の備え",
    "B007": "地震への備え",
    "B008": "車の冠水・水没",
    "B009": "冠水道路の運転",
    "B010": "地下駐車場の浸水",
    "B011": "水没車と車両保険",
    "B012": "自宅の浸水対策",
    "B013": "火災保険の水災補償",
    "B014": "家財の水災補償",
    "B015": "浸水被害の記録",
    "B016": "台風の風災補償",
    "B017": "地震保険の基本",
    "B018": "地震と自動車保険",
    "B019": "災害と保険",
    "B020": "大雨前の自宅チェック",
    "B021": "台風前日の備え",
    "B022": "マンションの台風・水害対策",
    "B023": "家具転倒対策",
    "B024": "地震後の停電・断水",
    "B025": "飲料水の備蓄",
    "B026": "非常食の備蓄",
    "B027": "防災ラジオ",
    "B028": "ポータブル電源",
    "B029": "車載防災用品",
    "B030": "家族の連絡・集合ルール",
    "B031": "非常食の賞味期限",
    "B032": "防災リュックの容量",
    "B033": "ペットの防災",
    "B034": "赤ちゃんの防災",
    "B035": "高齢者の防災",
    "B036": "土砂災害と避難",
    "B037": "浸水後の片付け",
    "B038": "帰宅困難者",
    "B039": "在宅避難と避難所",
    "B040": "感震ブレーカー",
    "B041": "津波避難",
    "B042": "洪水・河川氾濫の避難",
    "B043": "高潮避難",
    "B044": "災害時の車中泊",
    "B045": "停電時の冷蔵庫",
    "B046": "台風の窓ガラス対策",
    "B047": "停電時の熱中症",
    "B048": "宮城県の地震・津波史",
    "B049": "広島市の土砂災害史",
    "B050": "荒川下流の洪水史",
    "B051": "火災保険10社比較",
    "B052": "地震保険の会社差",
    "B053": "名古屋市の水害史",
    "B054": "神戸市の地震災害史",
    "B055": "高知の地震・津波史",
    "B056": "桜島の噴火史",
    "B057": "地震直後の行動",
    "B058": "火山噴火・降灰の初動",
    "B059": "真備地区の水害史",
    "B060": "火山灰対策グッズ",
    "B061": "常用薬の備え",
    "B062": "妊婦・妊産婦の防災",
    "B063": "在宅医療機器の電源",
    "B064": "食物アレルギーの備蓄",
    "B065": "女性の防災",
    "B066": "認知症の人の防災",
    "B067": "線状降水帯",
    "B068": "過去事例",
    "B069": "発生回数・将来予測",
    "B070": "地域別",
    "B071": "雨量記録",
    "B072": "用語・情報の歴史",
    "B073": "九州",
    "B074": "関東甲信",
    "B075": "中国地方",
    "B076": "四国",
    "B077": "東海",
    "B078": "ペットと避難所",
    "B079": "ペットと車中泊",
    "B080": "犬の防災",
    "B081": "猫の防災",
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
    "B093": "大阪府の大雨・都市型水害",
    "B094": "愛知県",
    "B095": "石川県",
    "B096": "富山県",
    "B097": "ゲリラ豪雨との違い",
}


def article_breadcrumb_name(article: dict, output_path: str) -> str:
    """Return the concise user-facing label used in Google breadcrumb markup."""
    article_id = article.get("article_id", "")
    if output_path.startswith("special/linear-rainband/prefecture/") and article_id != "B093":
        title = article.get("title", "")
        match = re.match(r"^(.+?[都道府県])の線状降水帯", title)
        if match:
            return match.group(1)
    name = ARTICLE_BREADCRUMB_NAMES.get(article_id)
    if not name:
        raise ValueError(f"{article_id or '?'}: breadcrumb short name missing")
    return name


def article_breadcrumb_items(article: dict, output_path: str, site_config: dict) -> list[dict]:
    """Build a short, human-readable breadcrumb hierarchy independent of URL depth."""
    base_url = site_config["public_base_url"].rstrip("/") + "/"
    site_name = site_config.get("site_name", "防災くらしガイド")
    page_url = urljoin(base_url, output_path)
    article_id = article.get("article_id", "")
    leaf_name = article_breadcrumb_name(article, output_path)

    hierarchy: list[tuple[str, str]] = [(site_name, base_url)]

    if article_id == "B067":
        hierarchy.append((leaf_name, page_url))
    elif article_id == "B093":
        hierarchy.append((REGION_BREADCRUMB[0], urljoin(base_url, REGION_BREADCRUMB[1])))
        hierarchy.append((leaf_name, page_url))
    elif output_path.startswith("special/linear-rainband/"):
        hierarchy.append(
            (
                LINEAR_RAINBAND_BREADCRUMB[0],
                urljoin(base_url, LINEAR_RAINBAND_BREADCRUMB[1]),
            )
        )
        hierarchy.append((leaf_name, page_url))
    elif article_id in REGION_ARTICLE_IDS or output_path.startswith("region/"):
        hierarchy.append((REGION_BREADCRUMB[0], urljoin(base_url, REGION_BREADCRUMB[1])))
        hierarchy.append((leaf_name, page_url))
    else:
        category = CATEGORY_BREADCRUMBS.get(article.get("category"))
        if not category:
            raise ValueError(
                f"{article_id or '?'}: breadcrumb category mapping missing: "
                f"{article.get('category')!r}"
            )
        hierarchy.append((category[0], urljoin(base_url, category[1])))
        hierarchy.append((leaf_name, page_url))

    return [
        {
            "@type": "ListItem",
            "position": position,
            "name": name,
            "item": item,
        }
        for position, (name, item) in enumerate(hierarchy, start=1)
    ]


def _required_date(article: dict, field: str) -> str:
    value = article.get(field)
    if not isinstance(value, str) or not DATE_RE.fullmatch(value):
        raise ValueError(f"{article.get('article_id', '?')}: invalid or missing {field}: {value!r}")
    return value


def _jp_date(value: str) -> str:
    year, month, day = (int(part) for part in value.split("-"))
    return f"{year}年{month}月{day}日"


def normalize_article_meta(html: str, article: dict) -> str:
    published = _required_date(article, "published_at")
    modified = _required_date(article, "modified_at")
    checked = _required_date(article, "source_checked_at")

    def replace_meta(match: re.Match[str]) -> str:
        extras: list[str] = []
        for span in SPAN_RE.finditer(match.group("body")):
            raw = span.group(0)
            text = re.sub(r"<[^>]+>", "", span.group("body")).strip()
            if ("商品" in text or "Amazon" in text) and ("確認" in text or "価格" in text):
                extras.append(raw)

        core = [
            f'<span>公開日: <time datetime="{published}">{_jp_date(published)}</time></span>',
            f'<span>最終更新日: <time datetime="{modified}">{_jp_date(modified)}</time></span>',
            f'<span>情報確認日: <time datetime="{checked}">{_jp_date(checked)}</time></span>',
        ]
        return '<div class="article-meta">' + "".join(core + extras) + "</div>"

    if not ARTICLE_META_RE.search(html):
        raise ValueError(f"{article.get('article_id', '?')}: article-meta not found")
    return ARTICLE_META_RE.sub(replace_meta, html, count=1)


def _description(html: str) -> str:
    match = DESCRIPTION_RE.search(html)
    if not match:
        raise ValueError("meta description not found for article structured data")
    return html_lib.unescape(match.group(1).strip())


def _absolute(base_url: str, page_url: str, url: str) -> str:
    if url.startswith(("http://", "https://")):
        return url
    if url.startswith("/"):
        return urljoin(base_url, url.lstrip("/"))
    return urljoin(page_url, url)


def build_structured_data(html: str, article: dict, output_path: str, site_config: dict) -> dict:
    published = _required_date(article, "published_at")
    modified = _required_date(article, "modified_at")
    base_url = site_config["public_base_url"].rstrip("/") + "/"
    page_url = urljoin(base_url, output_path)
    site_name = site_config.get("site_name", "防災くらしガイド")
    language = site_config.get("content_language", "ja-JP")

    organization = {
        "@type": "Organization",
        "name": site_name,
        "url": base_url,
    }
    posting = {
        "@type": "BlogPosting",
        "headline": article["title"],
        "description": _description(html),
        "datePublished": published,
        "dateModified": modified,
        "inLanguage": language,
        "url": page_url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": page_url},
        "author": organization,
        "publisher": organization,
    }

    image_match = FEATURE_IMAGE_RE.search(html)
    if image_match:
        posting["image"] = [_absolute(base_url, page_url, image_match.group(1))]

    breadcrumb = {
        "@type": "BreadcrumbList",
        "itemListElement": article_breadcrumb_items(article, output_path, site_config),
    }

    return {
        "@context": "https://schema.org",
        "@graph": [posting, breadcrumb],
    }


def inject_structured_data(html: str, article: dict, output_path: str, site_config: dict) -> str:
    html = GENERATED_JSONLD_RE.sub("", html)
    payload = build_structured_data(html, article, output_path, site_config)
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    script = (
        '<script type="application/ld+json" '
        'data-generated="article-structured-data">'
        + serialized
        + "</script>\n"
    )
    if "</head>" not in html:
        raise ValueError(f"{article.get('article_id', '?')}: missing </head>")
    return html.replace("</head>", script + "</head>", 1)


def apply_article_metadata(html: str, article: dict, output_path: str, site_config: dict) -> str:
    html = normalize_article_meta(html, article)
    return inject_structured_data(html, article, output_path, site_config)


def validate_article_output(html: str, article: dict, output_path: str, site_config: dict) -> list[str]:
    errors: list[str] = []
    article_id = article.get("article_id", "?")

    try:
        published = _required_date(article, "published_at")
        modified = _required_date(article, "modified_at")
        checked = _required_date(article, "source_checked_at")
    except ValueError as exc:
        return [str(exc)]

    expected_tokens = [
        f'公開日: <time datetime="{published}">',
        f'最終更新日: <time datetime="{modified}">',
        f'情報確認日: <time datetime="{checked}">',
    ]
    for token in expected_tokens:
        if token not in html:
            errors.append(f"{article_id}: missing visible article date token: {token}")

    scripts = re.findall(
        r'<script\s+type=["\']application/ld\+json["\']\s+'
        r'data-generated=["\']article-structured-data["\']>(.*?)</script>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if len(scripts) != 1:
        errors.append(f"{article_id}: generated JSON-LD script count != 1")
        return errors

    try:
        payload = json.loads(scripts[0])
    except json.JSONDecodeError as exc:
        errors.append(f"{article_id}: invalid JSON-LD: {exc}")
        return errors

    graph = payload.get("@graph", [])
    posting = next((node for node in graph if node.get("@type") == "BlogPosting"), None)
    breadcrumb = next((node for node in graph if node.get("@type") == "BreadcrumbList"), None)
    if not posting:
        errors.append(f"{article_id}: BlogPosting missing")
    else:
        if posting.get("headline") != article.get("title"):
            errors.append(f"{article_id}: BlogPosting headline mismatch")
        if posting.get("datePublished") != published:
            errors.append(f"{article_id}: BlogPosting datePublished mismatch")
        if posting.get("dateModified") != modified:
            errors.append(f"{article_id}: BlogPosting dateModified mismatch")

    if not breadcrumb:
        errors.append(f"{article_id}: BreadcrumbList missing")
    else:
        items = breadcrumb.get("itemListElement", [])
        try:
            expected_items = article_breadcrumb_items(article, output_path, site_config)
        except ValueError as exc:
            errors.append(str(exc))
            expected_items = []
        if items != expected_items:
            errors.append(f"{article_id}: BreadcrumbList hierarchy mismatch")

    return errors
