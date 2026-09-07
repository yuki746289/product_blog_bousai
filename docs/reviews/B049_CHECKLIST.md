# B049 記事別レビュー記録

- article_id: `B049`
- title: 広島市の土砂災害史｜1999年・2014年・2018年の豪雨から考える備え
- review_date: 2026-09-06
- source_checked_at: 2026-09-06
- content_role: detail / regional history
- risk_level: elevated
- article_status: DRAFTED
- review_status: PASS_WITH_PUBLISH_BLOCKERS

## 読者・役割

- 広島市で繰り返された豪雨・土砂災害を、現在のハザード確認へつなぐ。
- 過去の被災地区を「次に危険な場所」として予測しない。
- 全国向けB036/B042の避難判断を複製せず、地域史から導線を作る。

## 事実・一次情報

| 項目 | 状態 | 確認 |
|---|---|---|
| 1999年6・29豪雨 最大時間雨量81mm | PASS | 広島県 |
| 1999年 死者31・行方不明1、土石流等139、がけ崩れ186 | PASS | 広島県 |
| 2014年 死亡77人、4,389世帯・10,711人 | PASS | 広島市、2026-06-24更新ページ |
| 2018年 死者28・行方不明2、住家被害 | PASS | 広島市 |
| 2026年土砂災害ハザードマップ | PASS | 広島市、2026-06-29更新 |
| 警戒区域外にも被害が広がる場合がある | PASS | 広島市ハザードマップ学習面 |

## 安全性

- PASS: 過去の雨量を将来の安全閾値にしていない。
- PASS: 大雨時に斜面・沢を見に行く行動を勧めていない。
- PASS: 現在の避難場所は固定表示せず最新市情報へ接続。
- PASS: 土砂だけでなく洪水・内水等の複合リスクを明示。

## 画像

- PASS: 2014年広島土砂災害の現地写真。
- PASS: Wikimedia Commons / CC BY-SA 4.0 / 作者確認済み。
- PASS: 被災写真を煽り目的に使用しない。

## 公開前ブロッカー

1. preview HTML作成・意味同期
2. feature画像のfigure/credit実装
3. `data/content_registry.json` 登録
4. 公開パス `region/hiroshima/landslide-history.html` のビルド確認
5. トップ「地域の災害史」導線追加
6. CI / public build / smoke確認

## 判定

原稿・出典・安全境界: **PASS**
READY_TO_PUBLISH: **NO（実装工程未完了）**

<!-- content-depth-20260907:metric -->
## 2026-09-07 本文量・読者満足度の再確認

- reader_visible_char_count: **4,024字**
- guideline_minimum: **2,500字**
- length_status: **PASS**
- counting_method: frontmatter・URL・Markdown記号・公的情報/出典一覧を除き、読者が読む本文の非空白文字を同一スクリプトで計測。
- editorial_note: 文字数そのものではなく、判断条件・具体例・生活への置き換え・次の行動の充足を優先して再確認。
<!-- /content-depth-20260907:metric -->
