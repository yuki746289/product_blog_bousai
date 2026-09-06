# B048 記事別レビュー記録

- article_id: `B048`
- title: 宮城県ではどんな地震・津波が起きた？1978年宮城県沖地震と東日本大震災から考える備え
- review_date: 2026-09-06
- source_checked_at: 2026-09-06
- content_role: detail / regional history
- risk_level: elevated
- article_status: DRAFTED
- review_status: PASS_WITH_PUBLISH_BLOCKERS

## 読者・役割

- 宮城県の地震・津波史を入口に、現在の公的ハザード情報へ進ませる。
- 全国向けB007/B041の避難・備え説明を複製しない。
- 歴史から将来の発生場所・周期を独自推定しない。

## 事実・一次情報

| 項目 | 状態 | 確認 |
|---|---|---|
| 1978年宮城県沖地震 M7.4 | PASS | 仙台管区気象台・地震本部 |
| 1978年の死者28人・負傷者1,325人 | PASS | 仙台管区気象台。東北全県の人的被害として記述 |
| 2011年、宮城県内最大震度7・津波被害 | PASS | 宮城県「東日本大震災 宮城の記録」 |
| 2026年3月、沿岸15市町の津波災害警戒区域 | PASS | 宮城県、指定範囲は津波浸水想定と同範囲 |
| 2026年3月津波対策ガイドライン改定 | PASS | 宮城県 |
| 市町村ハザードマップへの導線 | PASS | 宮城県2026-08-19掲載ページ |

## 安全性

- PASS: 過去被災範囲を現在の安全保証にしていない。
- PASS: 津波の具体的避難判断はB041と最新公的情報へ接続。
- PASS: 古い地震防災マップには更新時期確認の注意を入れた。
- PASS: 商品・広告導線なし。

## 画像

- PASS: 宮城県名取市の実災害写真。
- PASS: Wikimedia Commons、作者・ライセンス確認済み。
- PASS: 恐怖訴求ではなく地域史説明用。

## 公開前ブロッカー

1. preview HTML作成・意味同期
2. feature画像のfigure/credit実装
3. `data/content_registry.json` 登録
4. 公開パス `region/miyagi/earthquake-tsunami-history.html` のビルド確認
5. トップ「地域の災害史」導線追加
6. CI / public build / smoke確認

## 判定

原稿・出典・安全境界: **PASS**
READY_TO_PUBLISH: **NO（実装工程未完了）**
