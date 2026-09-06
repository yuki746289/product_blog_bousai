# B050 記事別レビュー記録

- article_id: `B050`
- title: 荒川下流の洪水史｜明治43年洪水・カスリーン台風と東京東部低地の水害リスク
- review_date: 2026-09-06
- source_checked_at: 2026-09-06
- content_role: detail / regional history
- risk_level: elevated
- article_status: DRAFTED
- review_status: PASS_WITH_PUBLISH_BLOCKERS

## 読者・役割

- 荒川下流を行政区域ではなく流域・低地の歴史として理解させる。
- 1910年洪水、放水路建設、1947年洪水を現在の洪水浸水想定へ接続する。
- 歴史的氾濫範囲を現在の個別住所の安全・危険判定に流用しない。

## 事実・一次情報

| 項目 | 状態 | 確認 |
|---|---|---|
| 1910年洪水、東京下町の広範囲浸水・死者369 | PASS | 国交省 荒川下流河川事務所 |
| 1911年放水路事業開始、約22km・幅約500m | PASS | 国交省 |
| 1924年岩淵水門完成・全線通水 | PASS | 国交省 |
| 1930年荒川放水路完成 | PASS | 国交省 |
| 1947年カスリーン台風、荒川2か所決壊・死者行方不明109 | PASS | 国交省 荒川ヒストリー |
| 洪水浸水想定区域で浸水深・継続時間等を確認可能 | PASS | 国交省 現行ページ |

## 安全性

- PASS: 放水路・堤防があることを安全保証にしていない。
- PASS: 1910/1947年の浸水図を現在のハザードマップの代用にしていない。
- PASS: 大雨時に川・水門を見に行く行動を明確に否定。
- PASS: 現在の避難判断はB042・公的最新情報へ接続。

## 画像

- PASS: 旧岩淵水門の2026年現地写真。
- PASS: Wikimedia Commons / CC0 1.0。
- PASS: 歴史的治水施設としての説明と本文内容が一致。

## 公開前ブロッカー

1. preview HTML作成・意味同期
2. feature画像のfigure/credit実装
3. `data/content_registry.json` 登録
4. 公開パス `region/arakawa/flood-history.html` のビルド確認
5. トップ「地域の災害史」導線追加
6. CI / public build / smoke確認

## 判定

原稿・出典・安全境界: **PASS**
READY_TO_PUBLISH: **NO（実装工程未完了）**
