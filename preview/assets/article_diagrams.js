/* Created: 2026-09-09 09:12 JST
 * Article-specific explanatory diagrams for production pages.
 * Images are AI-generated explanatory illustrations, not official maps/photos.
 */
(function () {
  'use strict';

  var DIAGRAMS = {
    '/guide/first-disaster-preparedness.html': {
      id: 'B001',
      heading: 'ハザードマップは、まずこの順番で開く',
      src: '/assets/images/ai_b001_hazardmap_flow_20260909.webp',
      alt: 'ハザードマップで住所確認、災害種別、危険度、避難所と経路、家族共有まで確認する5ステップの図',
      caption: 'ハザードマップ確認の流れを整理した模式図。実際の区域・凡例・避難場所は国や自治体の公式ハザードマップで確認してください。AI生成図。'
    },
    '/water-outage/portable-toilet-stockpile.html': {
      id: 'B003',
      heading: 'まず「携帯トイレ」と「簡易トイレ」の違いを知る',
      src: '/assets/images/ai_b003_toilet_difference_20260909.webp',
      alt: '既存便器に袋を付ける携帯トイレと組み立て式の簡易トイレの違いと使い方を比較した図',
      caption: '携帯トイレと簡易トイレの違いと基本的な使い方を整理した模式図。製品ごとの使用手順・処分方法は取扱説明書と自治体案内に従ってください。AI生成図。'
    },
    '/blackout/blackout-preparedness.html': {
      id: 'B004',
      heading: '停電対策を5つの役割で確認する',
      src: '/assets/images/ai_b004_outage_five_roles_20260909.webp',
      alt: '停電時の備えを照明、情報、連絡、充電、生活維持の5つの役割に分けた図',
      caption: '停電時の備えを照明・情報・連絡・充電・生活維持の5役割で整理した図。AI生成図。'
    },
    '/home/home-flood-preparedness.html': {
      id: 'B012',
      heading: '土のう・止水板は「どこを、何cmふさぐか」から決める',
      src: '/assets/images/ai_b012_sandbag_placement_20260909.webp',
      alt: '住宅の玄関、勝手口、車庫シャッター、低い窓や通気口に土のうを置く位置と積み方を示した図',
      caption: '住宅で土のうを置く位置と積み方の考え方を示した模式図。浸水が始まった後や危険な状況では作業せず、避難を優先してください。AI生成図。'
    },
    '/post-disaster/after-flood-record-evidence.html': {
      id: 'B015',
      heading: '同じ場所を「遠景・中景・近景」で撮る',
      src: '/assets/images/ai_b015_damage_photo_steps_20260909.webp',
      alt: '浸水被害を全景、中景、近景の3段階で撮影し浸水高さも記録する方法を示した図',
      caption: '被害写真を全景・中景・近景で残す手順と浸水高さの記録例。危険な場所へ撮影のために近づかないでください。AI生成図。'
    },
    '/typhoon/typhoon-day-before-checklist.html': {
      id: 'B021',
      heading: '残り時間で考える：24時間前・12時間前・6時間前は「目安」',
      src: '/assets/images/ai_b021_typhoon_timeline_20260909.webp',
      alt: '台風接近の24時間前、12時間前、6時間前、当日に準備と安全確認を切り替えるタイムライン図',
      caption: '台風接近時に24時間前・12時間前・6時間前・当日で作業を切り替える目安を整理した図。実際の行動は最新の気象・避難情報を優先してください。AI生成図。'
    },
    '/home/apartment-typhoon-flood.html': {
      id: 'B022',
      heading: '結論：自宅の階だけでなく「建物全体で何が止まるか」を確認する',
      src: '/assets/images/ai_b022_apartment_flood_points_20260909.webp',
      alt: 'マンションの窓、ベランダ排水口、共用廊下、エントランス、地下駐車場や機械室の水害確認箇所を示した図',
      caption: 'マンションで確認したい窓・ベランダ排水口・共用廊下・エントランス・地下設備などを整理した模式図。共用部は管理会社・管理組合の指示に従ってください。AI生成図。'
    },
    '/goods/portable-power-station-disaster.html': {
      id: 'B028',
      heading: '容量Whと出力Wを分けて考える',
      src: '/assets/images/ai_b028_wh_w_guide_20260909.webp',
      alt: 'ポータブル電源のWhは蓄えられる電力量、Wは家電の消費電力や出力であることを比較した図',
      caption: 'ポータブル電源のWh（容量）とW（消費電力・出力）の違いを整理した図。実際の使用時間は機器・変換効率・使用条件で変わります。AI生成図。'
    },
    '/earthquake/tsunami-evacuation.html': {
      id: 'B041',
      heading: '「海から遠ざかる」だけではなく、高い安全な場所を目指す',
      src: '/assets/images/ai_b041_tsunami_evacuation_20260909.webp',
      alt: '津波時に海岸や川沿い、低い場所から高台や津波避難ビルへ避難する考え方を示した図',
      caption: '津波時に海岸・川沿い・低地から高台や津波避難ビルへ移動する考え方を示した模式図。実際の避難先・経路は自治体の指定を確認してください。AI生成図。'
    }
  };

  function normalize(value) {
    return (value || '').replace(/\s+/g, '').replace(/^\d+[.．]\s*/, '');
  }

  function currentConfig() {
    var path = window.location.pathname.replace(/\/{2,}/g, '/');
    return DIAGRAMS[path] || null;
  }

  function findHeading(root, expected) {
    var needle = normalize(expected);
    var headings = root.querySelectorAll('h2, h3');
    for (var i = 0; i < headings.length; i += 1) {
      if (normalize(headings[i].textContent).indexOf(needle) !== -1) return headings[i];
    }
    return null;
  }

  function buildFigure(config) {
    var figure = document.createElement('figure');
    figure.className = 'article-inline-image article-diagram';
    figure.setAttribute('data-article-diagram', config.id);

    var image = document.createElement('img');
    image.src = config.src;
    image.alt = config.alt;
    image.loading = 'lazy';
    image.decoding = 'async';
    image.width = 1200;
    image.height = 900;

    var caption = document.createElement('figcaption');
    caption.textContent = config.caption;

    figure.appendChild(image);
    figure.appendChild(caption);
    return figure;
  }

  function injectDiagram() {
    var config = currentConfig();
    if (!config) return;
    if (document.querySelector('[data-article-diagram="' + config.id + '"]')) return;

    var body = document.querySelector('.article-body');
    if (!body) return;

    var heading = findHeading(body, config.heading);
    if (!heading) {
      console.warn('[bousai] diagram heading not found:', config.id, config.heading);
      return;
    }

    heading.insertAdjacentElement('afterend', buildFigure(config));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectDiagram, { once: true });
  } else {
    injectDiagram();
  }
}());
