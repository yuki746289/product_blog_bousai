# B024 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B024`
- title: 地震後の停電・断水にどう備える？
- content_role: `detail`
- risk_level: `elevated`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-04
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

## 1. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 水・トイレ・照明・充電・発電機・復電・食品・集合住宅まで地震後ライフライン停止を一連で整理 |
| C02 出典・安全性 | PASS | 内閣府・消防庁・農水省・経産省・東京都下水道局・消費者庁の現行一次情報を再照合 |
| C03 画像・視覚要素 | PASS | AI画像は場面理解のみ、給水拠点画像は現実例。安全判断の根拠にしない |
| C04 読みやすさ・UI | PASS | 数量表、用途別章、Q&A、禁止事項で長文を分割 |
| C05 内部リンク | PASS | B007/B004/B003/B023へ接続。B004とは一般停電と地震後複合停止で役割分離 |
| C06 商品導線・商品記事 | PASS | 水・トイレ・ライト・電源の内部比較を各安全説明後に配置。購入を結論にしない |
| C07 Q&A | PASS | 水日数・トイレ回数・停電準備の個別Q&Aへ本文文脈から接続 |
| C08 同期・公開前 | PASS | Markdown/preview/source/registryを2026-09-04監査へ同期 |
| C09 日付・構造化データ | PASS | source_checked_atをregistryへ同期し既存生成機構で出力 |
| C10 デザイン・UX | PASS | 既存共通UI内の表・画像・Q&A・商品導線。新規独自UIなし |
| C11 読者・マーケティング | PASS | 被災直後の安全と平常時備蓄を分け、具体的な週末チェックまで提示 |
| C12 アクセシビリティ | PASS | 数値・危険事項を色に依存せず文章・表・リストで表示 |
| C13 技術品質・信頼性 | PASS | 正本同期ワークフロー内unittest PASS。previewも同期済み |
| C14 計測・グロース | N/A | 計測変更なし |

## 2. 防災サイト固有チェック

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| S01 適用判定 | PASS | 商品内部導線があるためE09を含めE01〜E09,E11〜E14適用 |
| S02 情報設計 | PASS | B004=停電一般、B024=地震後の停電+断水+排水+復電。検索意図を分離 |
| S03 法務・権利等 | PASS | 既存画像権利記録を維持。商品導線を公的推奨に見せない |
| S04 ブランド・トーン | PASS | 不安訴求や「これだけで安心」を避け、安全条件を先に記載 |
| S05 日本向け文脈 | PASS | 日本の備蓄目安、下水道・集合住宅、消費者庁の発電機注意に準拠 |
| S06 運用・ガバナンス | PASS | 3L/日・35回/週を「サイト共通仕様」だけでなく一次情報へ直接紐付け、registry source_idsも同期 |
| S07 セキュリティ・外部依存 | PASS | 新規外部JS/APIなし。公的情報リンクのみ追加 |
| S08 数値 | PASS | 3L/日、5回/日、35回/週の条件と用途を明示し安全保証値へ変換しない |

## 3. 安全・誤判断防止確認

- PASS: 上水道が使えても排水設備確認前にトイレを安易に流さない。
- PASS: 発電機は屋内・物置・車庫など換気の悪い場所で使用しない。
- PASS: 屋外でも窓・換気口等の開口部から離し、風通しを確保する。
- PASS: ベランダを全国一律の法的禁止とは断定せず、排気・距離・管理規約上「安全とは限らない」と説明。
- PASS: 浸水・破損した機器を安易に再通電しない。
- PASS: 冷蔵食品を臭い・見た目だけで安全判断しない。
- PASS: 常用薬・医療機器を自己判断で代替しない。

## 4. 読者・ページ設計

- target_reader: 地震による停電・断水・排水停止に備える家庭
- usage_context: 平常時の備蓄確認〜地震後の在宅避難判断
- reader_problem: 水だけ備えればよいのか、トイレ・電源・復電時に何が危険か分からない
- reader_goal: 1週間を視野に必要量と危険行動を把握する
- page_job: 地震後ライフライン停止のdetail記事
- next_action: 水/トイレ数量確認→照明/充電確認→排水/発電機/復電の安全ルール共有

## 5. 証跡

- sources: `docs/research/B024_SOURCES.md`
- article: `content/articles/B024_earthquake_blackout_water_outage.md`
- preview: `preview/article_b024.html`
- public_path: `earthquake/earthquake-blackout-water-outage.html`
- registry: 2026-09-04同期

## 6. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 数量根拠・排水・発電機・通電火災を一次情報へ直接トレースし、曖昧だった発電機設置場所表現も精密化した。
