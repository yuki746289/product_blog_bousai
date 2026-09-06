# B040 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B040`
- title: 感震ブレーカーとは？地震の電気火災・通電火災を防ぐ選び方と注意点
- content_role: `detail`
- risk_level: `elevated`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-04
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

## 1. 適用プロファイル確認

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| 防災サイトプロファイル | PASS | 電気火災・復電・医療機器停電を含むelevated記事 |
| 必須専門家ロール | PASS | E01〜E08,E11〜E14 |
| 条件付きロール | PASS | E09/E10=N/A。商品ランキング・独自計測なし |
| 詳細架空ペルソナ | N/A | 家庭の設備状況・医療機器有無という状況ベース |

## 2. 共通チェック C01〜C14

| ID | 状態 | 根拠 |
|---|---|---|
| C01 | PASS | 定義→種類→停电影響→避難→復電→点検まで独立意図を完結 |
| C02 | PASS | 内閣府・政府広報・消防庁・消費者庁・経産省を一次根拠化 |
| C03 | PASS | 誤認しやすい製品写真を避け、比較表・フロー・安全ボックスで視覚化 |
| C04 | PASS | 上部結論、タイプ比較、NG行動、保存チェックリスト |
| C05 | PASS | B007/B024/B023/B039/B004へ役割別導線 |
| C06 | N/A | 商品比較・Amazon直リンクなし |
| C07 | N/A | Q&A重複を追加しない |
| C08 | PASS | article / preview / sources / brief / images / checklist / registry / category / parent導線同期 |
| C09 | PASS | registryから公開日・更新日・BlogPosting/BreadcrumbList生成対象 |
| C10 | PASS | 「有効だが停電する設備」というトレードオフを上部で理解可能 |
| C11 | PASS | 不安や焼失試算を購入圧力に使わない |
| C12 | PASS | 表にrole/aria-label/tabindex、色だけに依存しない |
| C13 | PASS | 共通CSS/JSのみ。新規外部スクリプトなし |
| C14 | N/A | 新規独自イベントなし |

## 3. サイト固有 S01〜S08

| ID | 状態 | 根拠 |
|---|---|---|
| S01 | PASS | safety > accuracy > accessibility > SEOの優先順位を維持 |
| S02 | PASS | B007=地震pillar、B024=ライフライン、B040=電気火災設備として分離 |
| S03 | PASS | 商品広告なし。公的図版を転載せずリンク参照 |
| S04 | PASS | 「通電火災が怖いから必須購入」と煽らず、条件と限界を説明 |
| S05 | PASS | 日本の内閣府・消防庁分類と2026年資料に準拠 |
| S06 | PASS | source_checked_at / next_review_at / evidence docsを設定 |
| S07 | PASS | 外部依存は公的リンクのみ。施工DIYを促さない |
| S08 | PASS | 作動条件を発表震度と単純同一視しない。試算値を販促に使わない |

## 4. Elevatedリスク追加確認

| 項目 | 状態 | 根拠 |
|---|---|---|
| 揺れている最中のブレーカー操作を促さない | PASS | 揺れ後・安全確保後に限定 |
| 津波・火災・倒壊時に操作で避難を遅らせない | PASS | 避難優先を明記 |
| 感震ブレーカーを万能扱いしない | PASS | 他の火災・停電対策との併用を明記 |
| 電気工事DIYを促さない | PASS | 工事必要タイプは自己施工しない |
| 夜間停電リスク | PASS | 足元灯・懐中電灯・ランタンを併用 |
| 医療機器の停電リスク | PASS | 個別判断せずメーカー・医療・施工者等を優先 |
| 水没・損傷機器へ再通電させない | PASS | 復電前NGサインを明記 |
| 焦げ臭等の異常時に継続使用させない | PASS | 遮断・専門家相談を案内 |
| 補助制度を全国共通と書かない | PASS | 自治体差を明記 |
| 作動震度を地域震度と同一視しない | PASS | 設置・製品差を明記 |

## 5. 読者・ページ設計

- target_reader: 感震ブレーカーの導入・見直しを考える一般家庭
- usage_context: 平時の地震火災対策
- knowledge_level: beginner/basic
- urgency_level: preparing
- reader_problem: 種類、効果、デメリット、停電影響が分からない
- reader_goal: 自宅条件に合う方式を検討し、必要な施工・停電対策を確認する
- page_job: 感震ブレーカーを地震火災対策＋停電対策として理解させる
- entry_path: 検索 / B007 / B024 / 地震カテゴリ
- next_action: 分電盤確認→停電させて困る機器確認→タイプ比較→公的資料/施工者確認→点検
- conversion_path: B024停電対策 / B023家具固定 / 公的・専門家確認
- design_priority: 最初の画面で「有効だが停電対策が必要」を理解できること

## 6. 証跡

- brief: `docs/research/B040_SENSITIVE_BREAKER_BRIEF.md`
- sources: `docs/research/B040_SOURCES.md`
- images: `docs/research/B040_IMAGES.md`
- article: `content/articles/B040_earthquake_sensitive_breaker.md`
- preview: `preview/article_b040.html`
- public_path: `earthquake/earthquake-sensitive-breaker.html`

## 7. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 2026年現行一次情報、施工、夜間停電、医療機器、避難優先、復電安全、カニバリ、権利・UXを確認済み。
