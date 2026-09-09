# Created: 2026-09-09 09:38 JST
# Updated: 2026-09-09 10:08 JST
"""Inject approved explanatory infographic images into selected production articles.

The reviewed article text remains Markdown. Production HTML receives one approved
PNG infographic after the heading where visual explanation is most useful.
Images live under ``preview/assets/images`` and are copied into ``public/assets``
by the normal production build.
"""

from __future__ import annotations

import html
import posixpath
import re


DIAGRAM_STYLE = r"""
<style data-article-diagram-style>
.article-explainer--image{margin:30px 0 34px}
.article-explainer--image img{display:block;width:100%;height:auto;border:1px solid #d7e2ea;border-radius:16px;background:#fff;box-shadow:0 8px 24px rgba(29,65,93,.08)}
.article-explainer--image figcaption{margin-top:10px;color:#667785;font-size:.79rem;line-height:1.65;text-align:center}
@media(max-width:600px){.article-explainer--image{margin:24px 0 28px}.article-explainer--image img{border-radius:12px}}
</style>
""".strip()


_BASE_DIAGRAMS = {
    "guide/first-disaster-preparedness.html": {
        "article_id": "B001",
        "heading": "ハザードマップは、まずこの順番で開く",
        "image": "ai_b001_hazard_map_flow_20260909.png",
        "alt": "ハザードマップを住所確認、災害種別、凡例、避難先と経路、家族共有の5段階で確認する手順図",
        "caption": "ハザードマップ確認の5ステップ。実際の区域・凡例・避難場所は国や自治体の公式ハザードマップで確認してください。",
    },
    "water-outage/portable-toilet-stockpile.html": {
        "article_id": "B003",
        "heading": "まず「携帯トイレ」と「簡易トイレ」の違いを知る",
        "image": "ai_b003_portable_toilet_20260909.png",
        "alt": "既存便器へ袋を付ける携帯トイレと、組み立て式便座を使う簡易トイレの違いと使い方を示す比較図",
        "caption": "携帯トイレと簡易トイレの基本構造と使い分け。製品ごとの手順・処分方法は取扱説明書と自治体案内に従ってください。",
    },
    "blackout/blackout-preparedness.html": {
        "article_id": "B004",
        "heading": "停電対策を5つの役割で確認する",
        "image": "ai_b004_blackout_roles_20260909.png",
        "alt": "停電時の備えを照明、情報、連絡、充電、生活維持の5つの役割に分けた図",
        "caption": "停電時の備えを5つの役割で整理した図解。家庭条件に合わせて必要な手段を組み合わせます。",
    },
    "home/home-flood-preparedness.html": {
        "article_id": "B012",
        "heading": "土のう・止水板は「どこを、何cmふさぐか」から決める",
        "image": "ai_b012_sandbag_layout_20260909.png",
        "alt": "玄関、勝手口、車庫シャッター、低い窓や通気口への土のう配置と積み方の基本を示す住宅水害対策図",
        "caption": "住宅の開口部と土のう配置を整理した模式図。自治体や製品の設置案内を優先してください。",
    },
    "post-disaster/after-flood-record-evidence.html": {
        "article_id": "B015",
        "heading": "同じ場所を「遠景・中景・近景」で撮る",
        "image": "ai_b015_flood_photo_record_20260909.png",
        "alt": "水害後の被害を全景、中景、近景の順で撮影し、浸水高さも記録する方法を示す図",
        "caption": "被害写真を全景・中景・近景で残す基本手順。安全を確認し、片付け前の状態も記録します。",
    },
    "typhoon/typhoon-day-before-checklist.html": {
        "article_id": "B021",
        "heading": "残り時間で考える：24時間前・12時間前・6時間前は「目安」",
        "image": "ai_b021_typhoon_timeline_20260909.png",
        "alt": "台風接近の24時間前、12時間前、6時間前、当日に準備内容を切り替えるタイムライン図",
        "caption": "台風接近時の準備タイムライン。時刻は目安とし、最新の気象・避難情報と安全条件を優先してください。",
    },
    "home/apartment-typhoon-flood.html": {
        "article_id": "B022",
        "heading": "結論：自宅の階だけでなく「建物全体で何が止まるか」を確認する",
        "image": "ai_b022_apartment_flood_20260909.png",
        "alt": "マンションの窓、ベランダ排水口、共用廊下、エントランス、地下駐車場や機械室など水害時に確認する場所を示す図",
        "caption": "マンション水害対策で確認したい専有部・共用部・地下設備。管理側の案内と避難情報を優先してください。",
    },
    "goods/portable-power-station-disaster.html": {
        "article_id": "B028",
        "heading": "容量Whと出力Wを分けて考える",
        "image": "ai_b028_wh_w_difference_20260909.png",
        "alt": "ポータブル電源の容量Whと消費電力Wの違い、使用時間の目安と選び方を示す図",
        "caption": "Whは容量、Wは出力・消費電力を見る指標です。実際の使用時間は製品、温度、変換効率、機器の動作で変わります。",
    },
    "earthquake/tsunami-evacuation.html": {
        "article_id": "B041",
        "heading": "「海から遠ざかる」だけではなく、高い安全な場所を目指す",
        "image": "ai_b041_tsunami_evacuation_20260909.png",
        "alt": "海岸や低地から高台または津波避難ビルへ移動し、遠さだけでなく高さを優先する津波避難の模式図",
        "caption": "津波避難では水平距離だけでなく、より高い安全な場所を目指します。地域の避難計画と指定避難先を確認してください。",
    },
}


def _image_src(output_path: str, filename: str) -> str:
    parent = posixpath.dirname(output_path) or "."
    return posixpath.relpath(f"assets/images/{filename}", start=parent)


def _figure(article_id: str, src: str, alt: str, caption: str) -> str:
    aria = f"{alt}。{caption}"
    return (
        f'<figure class="article-explainer--image" data-article-diagram="{html.escape(article_id, quote=True)}" '
        f'role="group" aria-label="{html.escape(aria, quote=True)}">'
        f'<img src="{html.escape(src, quote=True)}" alt="{html.escape(alt, quote=True)}" '
        'width="1448" height="1086" loading="lazy" decoding="async">'
        f'<figcaption>{html.escape(caption)}</figcaption></figure>'
    )


DIAGRAMS: dict[str, dict[str, str]] = {}
for _output_path, _spec in _BASE_DIAGRAMS.items():
    _entry = dict(_spec)
    _entry["src"] = _image_src(_output_path, _entry["image"])
    _entry["figure"] = _figure(
        _entry["article_id"], _entry["src"], _entry["alt"], _entry["caption"]
    )
    DIAGRAMS[_output_path] = _entry


def _normalize_heading(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"^\s*\d+[.．]\s*", "", value)
    return re.sub(r"\s+", "", value)


def inject_article_diagram(document: str, output_path: str) -> str:
    """Insert one configured approved image immediately after its target heading."""
    spec = DIAGRAMS.get(output_path)
    if not spec or f'data-article-diagram="{spec["article_id"]}"' in document:
        return document

    expected = _normalize_heading(spec["heading"])
    pattern = re.compile(
        r"<h(?P<level>[23])(?P<attrs>[^>]*)>(?P<body>.*?)</h(?P=level)>", re.I | re.S
    )

    for match in pattern.finditer(document):
        actual = _normalize_heading(match.group("body"))
        if expected not in actual and actual not in expected:
            continue
        document = document[: match.end()] + "\n" + spec["figure"] + document[match.end() :]
        if "data-article-diagram-style" not in document:
            document = document.replace("</head>", DIAGRAM_STYLE + "\n</head>", 1)
        return document

    raise ValueError(
        f'Article diagram heading not found for {spec["article_id"]}: {spec["heading"]}'
    )
