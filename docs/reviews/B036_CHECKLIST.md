# B036 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B036`
- title: 土砂災害はいつ避難する？土砂キキクルと避難判断の見方
- content_role: `practical`
- risk_level: `high`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-04
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

## 1. 適用プロファイル確認

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| 防災サイトプロファイル確認 | PASS | 高リスク情報記事として適用 |
| 必須専門家ロール選定 | PASS | E01〜E08,E11〜E14 |
| 条件付き専門家ロール判定 | PASS | E09/E10はN/A |
| 詳細架空ペルソナ | N/A | 状況ベース読者設定を使用 |
| N/A項目の理由確認 | PASS | 商品・計測を主目的としない |

## 2. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 区域確認→情報確認→避難判断→次善行動まで一連で整理 |
| C02 出典・安全性 | PASS | 気象庁・国交省/国土地理院・内閣府を一次根拠に使用 |
| C03 画像・視覚要素 | PASS | 日本の実災害Commons画像1点＋色/行動表。権利確認済み |
| C04 読みやすさ・UI | PASS | 色だけに依存せず名称・警戒レベル・行動を併記 |
| C05 内部リンク | PASS | 大雨・水害カテゴリから入口を設け、記事内からB005/B006/B012/B022へ回遊可能。孤立ページではない |
| C06 商品導線・商品記事 | N/A | 商品購入を主目的にしない |
| C07 Q&A | N/A | 本文単体で主要判断を完結。必要性が生じた場合のみ追加 |
| C08 同期・公開前 | PASS | Markdown / preview / research / checklist / registry / categoryを同期 |
| C09 日付・構造化データ | PASS | registryから日付・BlogPosting・BreadcrumbListを生成しテストPASS |
| C10 デザイン・UX | PASS | 既存共通UIを使用し、緊急時の判断順を上部へ配置 |
| C11 読者・マーケティング | PASS | preparing/imminentの読者行動を明確化。収益導線なし |
| C12 アクセシビリティ | PASS | 色だけで意味を表さず、テキスト・表・見出しで補完。共通アクセシビリティテストPASS |
| C13 技術品質・信頼性 | PASS | build / JS / Commons画像ローカル化 / FTPS / HTTP smokeすべてPASS |
| C14 計測・グロース | N/A | 新規イベントなし |

## 3. 防災サイト固有チェック結果

| サイト固有チェック | 状態 | 根拠・備考 |
|---|---|---|
| S01 サイトプロファイル・適用判定 | PASS | high riskとして安全を最優先 |
| S02 情報設計・ファインダビリティ | PASS | B005の水害pillarから独立した土砂災害practicalとして役割分離。カテゴリ導線実装 |
| S03 法務・権利・広告表示・プライバシー | PASS | Commons CC BY-SA 4.0の作者・出典・ライセンスを保持。広告誘導なし |
| S04 ブランド・トーン・コンテンツデザイン | PASS | 恐怖喚起より具体的な行動判断を優先 |
| S05 日本向けローカライゼーション | PASS | 2026年5月29日開始の日本の現行防災気象情報に合わせた |
| S06 運用・ガバナンス・保守性 | PASS | 正本registry・research・checklist・previewを同期しCIで検証 |
| S07 セキュリティ・外部依存 | PASS | Commons画像はproduction buildでローカルWebP化。公的情報は外部リンクとして案内 |
| S08 数値・統計・リアルタイム要約 | PASS | 土砂キキクル10分更新等は一次情報確認。独自雨量閾値を作成していない |

## 4. 高リスク追加確認

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| 黒を避難開始目安にしない | PASS | 黒になる前の避難を明記 |
| 高齢者等は遅くとも赤 | PASS | 気象庁現行説明 |
| 一般の人は遅くとも紫 | PASS | 気象庁現行説明 |
| 一般の人も赤から準備・自主避難検討 | PASS | 気象庁現行説明 |
| 自治体避難情報をキキクルより後回しにしない | PASS | 発令時は速やかな行動を明記 |
| 土砂キキクル単独判断を避ける | PASS | 警戒区域等・自治体情報と併用 |
| 独自雨量閾値を作らない | PASS | 数値による独自避難基準なし |
| 前兆現象を待たせない | PASS | 前兆なしを安全根拠にしない |
| 立退き避難困難時の説明を通常避難と混同しない | PASS | 次善行動であり事前計画ではないと明記 |

## 5. 読者・ページ設計の証跡

- target_reader: 大雨時に崖・急傾斜地・渓流周辺の危険が気になる一般生活者
- usage_context: 大雨予報〜危険度上昇時
- knowledge_level: beginner/basic
- urgency_level: preparing/imminent
- reader_problem: 情報が多く避難開始時点が分かりにくい
- reader_goal: 危険区域と情報を組み合わせて遅れずに避難する
- page_job: 土砂災害情報を家庭の行動順へ整理
- entry_path: 検索 / 大雨・水害カテゴリ / 関連記事
- next_action: 区域確認→キキクル・自治体情報→早期避難
- conversion_path: 安全行動→関連水害記事
- design_priority: 緊急時でも警戒情報と行動を短時間で理解できること

## 6. 証跡

- brief: `docs/research/B036_LANDSLIDE_EVACUATION_BRIEF.md`
- sources: `docs/research/B036_SOURCES.md`
- images: `docs/research/B036_IMAGES.md`
- article: `content/articles/B036_landslide_evacuation_kikikuru.md`
- preview: `preview/article_b036.html`
- public_path: `flood/landslide-evacuation-kikikuru.html`
- content_registry: 登録済み
- category: `category_flood`掲載済み
- production_check: GitHub Actionsで tests / build / JS / Commons localization / FTPS / HTTP smoke PASS

## 7. 今後の改善候補

- B005/B006/B012/B022本文内からの直接コンテキストリンクは、回遊データや記事改稿時に追加を検討する。現在もカテゴリ入口と関連記事導線があり、孤立ページではないため公開ブロッカーとはしない。
- Search Consoleデータ蓄積後、検索意図とカニバリを再確認する。

## 8. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 高リスク安全レビュー、一次情報、権利、情報設計、アクセシビリティ、production build、HTTP smokeまで確認済み。
