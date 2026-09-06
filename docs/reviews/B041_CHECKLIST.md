# B041 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B041`
- title: 津波からどう避難する？警報を待たない判断・徒歩避難・避難先の考え方
- content_role: `practical`
- risk_level: `high`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-05
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

## 1. 適用プロファイル確認

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| 防災サイトプロファイル | PASS | 津波避難は生命安全に直結するhigh-risk記事 |
| 必須専門家ロール | PASS | E01〜E08,E10〜E14を適用 |
| 条件付きロール | N/A | E09商品/affiliateなし |
| 詳細架空ペルソナ | N/A | 沿岸・川沿い・旅行先・要配慮者等の状況ベース |

## 2. 共通チェック C01〜C14

| ID | 状態 | 根拠 |
|---|---|---|
| C01 | PASS | 警報待ち禁止→警報区分→避難先→徒歩/車→解除までを一ページで完結 |
| C02 | PASS | 気象庁・内閣府・消防庁の一次情報を根拠化 |
| C03 | PASS | 日本の津波避難ルート標識を採用。衝撃的災害写真や海外標識は不使用 |
| C04 | PASS | 冒頭に6ステップ、警報区分表、保存チェック、NG行動を配置 |
| C05 | PASS | B007/B039/B038/B030/B023へ役割別導線 |
| C06 | N/A | 商品導線なし |
| C07 | N/A | Q&A新設なし |
| C08 | PASS | article/preview/brief/sources/images/checklist/registry/category/parent導線を同期対象 |
| C09 | PASS | BlogPosting/BreadcrumbList生成対象 |
| C10 | PASS | 最初の画面で「警報待ち禁止・高い場所・徒歩原則・解除まで戻らない」を理解可能 |
| C11 | PASS | 津波映像・恐怖表現を煽りや購入圧力に利用しない |
| C12 | PASS | 表・チェックリスト・文字情報で色だけに依存しない |
| C13 | PASS | 新規外部JSなし、Commons画像のみ |
| C14 | N/A | 新規独自イベントなし |

## 3. サイト固有 S01〜S08

| ID | 状態 | 根拠 |
|---|---|---|
| S01 | PASS | safety > accuracy > accessibility > SEO |
| S02 | PASS | B007=地震pillar、B041=津波避難practicalとして分離 |
| S03 | PASS | CC BY-SA 4.0画像を出典・著者・ライセンス付きで使用 |
| S04 | PASS | 不安を煽らず「迷わない行動順」を中心に設計 |
| S05 | PASS | 日本のJMA警報区分・指定緊急避難場所・徒歩原則を採用 |
| S06 | PASS | source_checked_at/next_review_at/evidence docsを設定 |
| S07 | PASS | 公的リンクのみ。位置情報・外部アプリを必須化しない |
| S08 | PASS | 独自の安全標高・距離・時間を作らない |

## 4. High-risk追加確認

| 項目 | 状態 | 根拠 |
|---|---|---|
| 強い揺れ/弱くても長い揺れで警報待ちさせない | PASS | 冒頭・本文・NG行動で明記 |
| 揺れの最中に危険な移動を促さない | PASS | まず落下物・転倒物から身を守る |
| 大津波警報/津波警報で沿岸・川沿いを避難対象化 | PASS | JMA区分準拠 |
| 津波注意報を警報と同一扱いしない | PASS | 海中から上がり海岸から離れる区分を保持 |
| 徒歩原則 | PASS | 令和8年版防災白書を根拠化 |
| 車を全国一律絶対禁止にしない | PASS | 地域・要配慮者・距離等の例外は事前計画として説明 |
| ハザードマップを安全保証にしない | PASS | 想定外浸水可能性を明記 |
| 第一波後に戻らせない | PASS | 後続波・長時間継続・解除まで避難を明記 |
| 家族・荷物・写真のため戻らせない | PASS | 危険区域への戻り禁止 |
| 到達予想時刻を猶予保証にしない | PASS | 待ち時間に使わないと明記 |
| 独自安全閾値を作らない | PASS | 標高/距離/時間の独自基準なし |

## 5. 読者・ページ設計

- target_reader: 沿岸部・川沿いに住む/働く/訪れる一般生活者
- usage_context: 平時の準備、および地震・津波警報直後の確認
- knowledge_level: beginner/basic
- urgency_level: urgent-capable
- reader_problem: いつ逃げるか、どこへ、徒歩か車か、いつ戻れるかが分からない
- reader_goal: 迷わず避難開始し、地域ルールに沿った安全な避難先へ移動する
- page_job: 津波避難の行動順と誤解しやすい例外を整理する
- entry_path: 検索 / B007 / 地震カテゴリ
- next_action: 自治体ハザードマップ確認→津波対応避難場所確認→徒歩経路を実際に歩く→家族ルール共有
- conversion_path: B030家族連絡 / B007地震全体 / 公的情報
- design_priority: 緊急時でも冒頭だけで「待たない・高い場所・徒歩原則・解除まで戻らない」を把握できること

## 6. 証跡

- brief: `docs/research/B041_TSUNAMI_EVACUATION_BRIEF.md`
- sources: `docs/research/B041_SOURCES.md`
- images: `docs/research/B041_IMAGES.md`
- article: `content/articles/B041_tsunami_evacuation.md`
- preview: `preview/article_b041.html`
- public_path: `earthquake/tsunami-evacuation.html`

## 7. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 2026年現行一次情報で、警報待ち禁止、警報区分、徒歩原則、車避難の例外、避難先、解除までの継続、独自数値禁止を確認済み。
