# Created: 2026-09-09 09:38 JST
"""Inject lightweight explanatory infographics into selected production articles.

The editorial source remains Markdown.  Production HTML receives responsive,
text-based infographic figures after the heading where the visual explanation
is most useful.  The figures are intentionally implemented as HTML/CSS rather
than external binary images so Japanese text remains sharp, selectable and
accessible at every viewport size.
"""

from __future__ import annotations

import html
import re


DIAGRAM_STYLE = r"""
<style data-article-diagram-style>
.article-explainer{margin:30px 0;padding:20px;border:1px solid #c9dce8;border-radius:20px;background:#fbfdff;box-shadow:0 8px 24px rgba(29,65,93,.08)}
.article-explainer__title{margin:0 0 5px;color:#0d3763;font-size:clamp(1.35rem,3vw,2rem);line-height:1.3;text-align:center;font-weight:850}
.article-explainer__lead{margin:0 0 18px;color:#52616a;text-align:center;font-size:.95rem;line-height:1.65}
.article-explainer__grid{display:grid;grid-template-columns:repeat(var(--cols,3),minmax(0,1fr));gap:12px}
.article-explainer__card{min-width:0;padding:14px;border-radius:15px;background:var(--card,#eef7ff);border:1px solid rgba(38,92,127,.12)}
.article-explainer__icon{display:flex;align-items:center;justify-content:center;width:42px;height:42px;margin:0 auto 8px;border-radius:50%;background:#fff;color:#0d3763;font-size:1.35rem;font-weight:850;box-shadow:0 2px 8px rgba(29,65,93,.08)}
.article-explainer__card h4{margin:0 0 7px;color:#143a63;font-size:1rem;line-height:1.45;text-align:center}
.article-explainer__card p{margin:0;color:#334e68;font-size:.89rem;line-height:1.65}
.article-explainer__note{margin:14px 0 0;padding:12px 14px;border-radius:13px;background:#fff4cf;color:#5a4710;font-weight:700;line-height:1.65}
.article-explainer__warning{margin:14px 0 0;padding:12px 14px;border:1px solid #ef9a9a;border-radius:13px;background:#fff1f1;color:#9b1c1c;font-weight:800;line-height:1.65}
.article-explainer__formula{margin:14px 0 0;padding:14px;border-radius:13px;background:#edf8ef;color:#1d5e37;text-align:center;font-size:clamp(1rem,2.5vw,1.25rem);font-weight:850;line-height:1.55}
.article-explainer figcaption{margin-top:12px;color:#667785;font-size:.79rem;line-height:1.6;text-align:center}
@media(max-width:760px){.article-explainer{padding:15px}.article-explainer__grid{grid-template-columns:1fr 1fr}.article-explainer__card:last-child:nth-child(odd){grid-column:1/-1}}
@media(max-width:480px){.article-explainer__grid{grid-template-columns:1fr}.article-explainer__card:last-child:nth-child(odd){grid-column:auto}}
</style>
""".strip()


def _card(icon: str, title: str, text: str, color: str) -> str:
    return (
        f'<section class="article-explainer__card" style="--card:{color}">'
        f'<div class="article-explainer__icon" aria-hidden="true">{html.escape(icon)}</div>'
        f'<h4>{html.escape(title)}</h4><p>{html.escape(text)}</p></section>'
    )


def _figure(
    article_id: str,
    title: str,
    lead: str,
    cards: list[tuple[str, str, str, str]],
    caption: str,
    *,
    note: str | None = None,
    warning: str | None = None,
    formula: str | None = None,
) -> str:
    card_html = ''.join(_card(*card) for card in cards)
    extras = ''
    if formula:
        extras += f'<div class="article-explainer__formula">{html.escape(formula)}</div>'
    if note:
        extras += f'<div class="article-explainer__note">{html.escape(note)}</div>'
    if warning:
        extras += f'<div class="article-explainer__warning">⚠ {html.escape(warning)}</div>'
    aria = f'{title}。{lead}'
    return (
        f'<figure class="article-explainer" data-article-diagram="{article_id}" role="group" '
        f'aria-label="{html.escape(aria, quote=True)}">'
        f'<h3 class="article-explainer__title">{html.escape(title)}</h3>'
        f'<p class="article-explainer__lead">{html.escape(lead)}</p>'
        f'<div class="article-explainer__grid" style="--cols:{min(len(cards),5)}">{card_html}</div>'
        f'{extras}<figcaption>{html.escape(caption)}</figcaption></figure>'
    )


DIAGRAMS = {
    'guide/first-disaster-preparedness.html': {
        'article_id': 'B001',
        'heading': 'ハザードマップは、まずこの順番で開く',
        'figure': _figure(
            'B001', 'ハザードマップの使い方 5ステップ',
            '地図を開くだけで終わらず、避難先と経路まで確認します。',
            [
                ('1', '住所・現在地を確認', 'まず自宅・勤務先・学校など、確認したい場所を地図上で特定します。', '#e8f5ff'),
                ('2', '災害の種類を選ぶ', '洪水・土砂災害・高潮・津波など、地域で確認したい災害を切り替えます。', '#eaf8ec'),
                ('3', '色分けと凡例を見る', '色だけで判断せず、浸水深や区域の意味を凡例で読みます。', '#fff3dc'),
                ('4', '避難先・経路を確認', '災害種別に対応した避難先と、危険箇所を避ける経路を確認します。', '#e8f1ff'),
                ('5', '家族で共有・保存', '印刷やスマホ保存など、停電・通信障害時でも見直せる形を用意します。', '#fdebef'),
            ],
            '当サイト作成の操作フロー図。実際の区域・凡例・避難場所は国や自治体の公式ハザードマップで確認してください。',
            note='見るポイント：自宅周辺の危険区域／避難所までの行き方／夜・大雨時の避難タイミング',
        ),
    },
    'water-outage/portable-toilet-stockpile.html': {
        'article_id': 'B003',
        'heading': 'まず「携帯トイレ」と「簡易トイレ」の違いを知る',
        'figure': _figure(
            'B003', '携帯トイレと簡易トイレの違い',
            '「袋だけでよいか」「便座そのものが必要か」を先に分けます。',
            [
                ('A', '携帯トイレ', '既存の洋式便器などに袋と凝固剤を取り付けて使います。自宅の便器が使える断水時に備えやすい方式です。', '#e8f5ff'),
                ('B', '簡易トイレ', '組立式の便座・箱・椅子型の本体へ袋をセットします。便器がない場所も想定できます。', '#eaf8ec'),
                ('1', 'セット', '袋を便器または簡易便座へ確実に取り付けます。', '#fff4da'),
                ('2', '使用・凝固', '製品説明に従って凝固剤・吸水材を使います。', '#f4edff'),
                ('3', '密閉・保管', '使用後は袋を閉じ、防臭と一時保管場所まで考えます。', '#fdebef'),
            ],
            '携帯トイレと簡易トイレの基本構造を整理した図解。製品ごとの手順・処分方法は取扱説明書と自治体案内に従ってください。',
            warning='排水設備の安全確認前は、水が出ても自己判断で水洗トイレを流さない。',
        ),
    },
    'blackout/blackout-preparedness.html': {
        'article_id': 'B004',
        'heading': '停電対策を5つの役割で確認する',
        'figure': _figure(
            'B004', '停電時に役立つ5つの役割',
            '最初の3つを優先し、その後5分類で準備漏れを確認します。',
            [
                ('1', '照明', 'ライトで足元と移動経路を確保する。', '#fff1c9'),
                ('2', '情報', 'ラジオや防災情報で状況を確認する。', '#e8f5ff'),
                ('3', '連絡', '家族との連絡手段とルールを残す。', '#fdebef'),
                ('4', '充電', 'スマホ・モバイルバッテリー等を使い続ける。', '#eaf8ec'),
                ('5', '生活維持', '水・食料・トイレ・暑さ寒さ・医療を考える。', '#f1eaff'),
            ],
            '停電対策を5つの役割で整理した図解。',
            note='最初にそろえたいのは「ライト・情報手段・連絡手段」。充電と生活維持は家庭条件に合わせて追加します。',
            warning='ろうそく等の裸火を主な照明にせず、電池式ライトを基本にする。',
        ),
    },
    'home/home-flood-preparedness.html': {
        'article_id': 'B012',
        'heading': '土のう・止水板は「どこを、何cmふさぐか」から決める',
        'figure': _figure(
            'B012', '土のうを置く場所の基本',
            '水が入りやすい開口部を平時に確認し、必要数と運び方まで試します。',
            [
                ('1', '玄関・勝手口', '出入口の幅と段差を測り、避難を妨げない位置を確認します。', '#fdebef'),
                ('2', '車庫シャッター', '周囲より低い場合は、シャッター下からの流入を想定します。', '#eaf8ec'),
                ('3', '低い窓・通気口', '低い位置の開口部が水の入口にならないかを確認します。', '#e8f5ff'),
                ('4', '積み方', '袋を平らにし、すき間を減らし、複数段では継ぎ目をずらします。', '#fff3dc'),
            ],
            '住宅の開口部と土のう配置を整理した模式図。自治体・製品の設置案内を優先してください。',
            note='必要数は「開口幅 ÷ 1袋の有効幅」を出発点にし、端部・重ねしろ・段数を考慮します。',
            warning='水が深くなった後や強い流れがある状況では追加作業をせず、避難を優先する。',
        ),
    },
    'post-disaster/after-flood-record-evidence.html': {
        'article_id': 'B015',
        'heading': '同じ場所を「遠景・中景・近景」で撮る',
        'figure': _figure(
            'B015', '被害写真の撮り方 3ステップ',
            '同じ被害を距離を変えて残すと、場所と損傷の関係を説明しやすくなります。',
            [
                ('1', '全景', '建物・部屋全体を撮り、被害が起きた場所を残します。', '#e8f5ff'),
                ('2', '中景', '家具・壁・床など、周辺との位置関係が分かる範囲を撮ります。', '#eaf8ec'),
                ('3', '近景', 'ひび、破損、浸水痕、家電の型番など細部を残します。', '#fff3dc'),
            ],
            '被害を全景・中景・近景で記録する流れを整理した図解。',
            note='浸水線は清掃前に、物差し等と一緒に撮ると高さを説明しやすくなります。片付け前後も同じ方向から残します。',
            warning='撮影のために倒壊・感電・ガス・汚水などの危険がある場所へ入らない。',
        ),
    },
    'typhoon/typhoon-day-before-checklist.html': {
        'article_id': 'B021',
        'heading': '残り時間で考える：24時間前・12時間前・6時間前は「目安」',
        'figure': _figure(
            'B021', '台風接近時の準備タイムライン',
            '時間が進むほど「作業」から「安全確認・避難判断」へ比重を移します。',
            [
                ('24h', '24時間前まで', '予報・ハザード、避難先、車、屋外物、停電対策を確認します。', '#eaf8ec'),
                ('12h', '12時間前まで', '屋外作業を終え、窓・充電・水・食料・トイレを整えます。', '#fff3dc'),
                ('6h', '6時間前を目安', '屋内の最終確認。情報・連絡・照明を切らさない状態にします。', '#e8f5ff'),
                ('当日', '風雨が強まったら', '新しい屋外作業をせず、避難情報と身の安全を最優先します。', '#fdebef'),
            ],
            '台風接近時の作業切替を時間軸で整理した図解。時刻は目安で、最新の気象・避難情報を優先してください。',
            warning='暴風・強い雨・冠水・避難情報などの中止条件があれば、残り時間に関係なく屋外作業を中止する。',
        ),
    },
    'home/apartment-typhoon-flood.html': {
        'article_id': 'B022',
        'heading': '結論：自宅の階だけでなく「建物全体で何が止まるか」を確認する',
        'figure': _figure(
            'B022', 'マンション水害対策の見る場所',
            '専有部と共用部を分け、自分がすることと管理側がすることを整理します。',
            [
                ('1', '窓・サッシ', '飛来物と吹き込みに備え、窓際から人・家財を離します。', '#e8f5ff'),
                ('2', 'ベランダ排水口', '落ち葉・ごみは平常時に取り除き、避難経路を塞ぎません。', '#eaf8ec'),
                ('3', '共用廊下・入口', '物を置かず、止水設備の運用は管理会社・管理組合へ確認します。', '#fdebef'),
                ('4', '地下駐車場', '車の退避ルールと、危険になってから取りに行かない条件を決めます。', '#f1eaff'),
                ('5', '機械室・給水設備', '地下設備の浸水が上階の停電・断水・エレベーター停止につながる点を確認します。', '#fff3dc'),
            ],
            'マンションで確認したい専有部・共用部・地下設備を整理した図解。',
            warning='大雨・強風の最中にベランダや共用部へ出て作業せず、管理側の案内と避難情報を優先する。',
        ),
    },
    'goods/portable-power-station-disaster.html': {
        'article_id': 'B028',
        'heading': '容量Whと出力Wを分けて考える',
        'figure': _figure(
            'B028', 'WhとWの違い',
            'ポータブル電源では「どれだけためられるか」と「どれだけ出せるか」を分けて確認します。',
            [
                ('Wh', '容量 Wh', 'どれだけの電力量を蓄えられるか。必要な使用時間を考える数字です。', '#e8f5ff'),
                ('W', '定格出力 W', '同時にどれだけの電力を出せるか。使いたい機器の消費電力と照合します。', '#fff0df'),
                ('例', '使用時間の概算', '500Whの電源で50Wの機器なら単純計算は10時間ですが、実際は変換損失等があります。', '#eaf8ec'),
            ],
            'WhとWの役割を整理した図解。実際の使用時間は製品・温度・変換効率・機器の動作で変わります。',
            formula='概算：使用可能時間 ≒ 容量(Wh) × 利用効率 ÷ 消費電力(W)',
            note='選ぶ順番：使いたい家電のWを確認 → 必要時間を決める → Whを考える → 同時使用時の合計Wを確認。',
        ),
    },
    'earthquake/tsunami-evacuation.html': {
        'article_id': 'B041',
        'heading': '「海から遠ざかる」だけではなく、高い安全な場所を目指す',
        'figure': _figure(
            'B041', '津波避難で大切なこと',
            '水平距離だけでなく、より高い安全な場所へ移ることを優先します。',
            [
                ('海', '海岸・川沿い', '強い揺れや津波警報等を合図に、その場を離れて避難を開始します。', '#e8f5ff'),
                ('低', '低い場所', '津波は低地や川沿いへ入り込むため、海から離れるだけで止まりません。', '#fdebef'),
                ('高', '高台', '時間と経路が許す範囲で、より高い安全な場所へ移ります。', '#eaf8ec'),
                ('ビル', '津波避難ビル', '近くに高台がない場合は、自治体が指定する津波避難ビル等を確認します。', '#e8f1ff'),
            ],
            '津波避難で「遠く」だけでなく「高い安全な場所」を目指す考え方を整理した模式図。',
            note='避難の基本：強い揺れを感じたらすぐ避難／徒歩を原則／家族を迎えに危険区域へ戻らない。',
            warning='強い揺れや弱くても長い揺れを感じた場合、津波警報等の発表を待って避難判断を始めない。',
        ),
    },
}


def _normalize_heading(value: str) -> str:
    value = re.sub(r'<[^>]+>', '', value)
    value = html.unescape(value)
    value = re.sub(r'^\s*\d+[.．]\s*', '', value)
    return re.sub(r'\s+', '', value)


def inject_article_diagram(document: str, output_path: str) -> str:
    """Insert one configured infographic immediately after its target heading."""
    spec = DIAGRAMS.get(output_path)
    if not spec or f'data-article-diagram="{spec["article_id"]}"' in document:
        return document

    expected = _normalize_heading(spec['heading'])
    pattern = re.compile(r'<h(?P<level>[23])(?P<attrs>[^>]*)>(?P<body>.*?)</h(?P=level)>', re.I | re.S)

    for match in pattern.finditer(document):
        actual = _normalize_heading(match.group('body'))
        if expected not in actual and actual not in expected:
            continue
        insertion = '\n' + spec['figure']
        document = document[:match.end()] + insertion + document[match.end():]
        if 'data-article-diagram-style' not in document:
            document = document.replace('</head>', DIAGRAM_STYLE + '\n</head>', 1)
        return document

    raise ValueError(f'Article diagram heading not found for {spec["article_id"]}: {spec["heading"]}')
