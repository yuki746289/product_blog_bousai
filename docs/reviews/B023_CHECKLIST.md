# B023 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B023`
- title: 地震の家具転倒対策｜まず優先したい場所
- content_role: `practical`
- risk_level: `elevated`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-04
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

## 1. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 寝室→出口→滞在場所→家具/家電→施工条件→点検の実行順 |
| C02 出典・安全性 | PASS | 消防庁・東京消防庁の現行情報を2026-09-04再確認 |
| C03 画像・視覚要素 | PASS | 画像関連性レビュー済み。施工・安全保証の根拠には使わない |
| C04 読みやすさ・UI | PASS | 優先順位、条件表、30分チェック、禁止事項で実行しやすい |
| C05 内部リンク | PASS | B007/B024/B004へ接続 |
| C06 商品導線・商品記事 | N/A | 個別商品購入導線なし |
| C07 Q&A | N/A | 本文で主要判断を完結 |
| C08 同期・公開前 | PASS | source/article/registryを2026-09-04監査へ同期 |
| C09 日付・構造化データ | PASS | 既存registry・生成機構を使用 |
| C10 デザイン・UX | PASS | 既存記事UI、表・箇条書き中心。新規独自UIなし |
| C11 読者・マーケティング | PASS | 器具購入より危険箇所特定を先にし、読者の次行動が明確 |
| C12 アクセシビリティ | PASS | 色に依存せず文章・表・見出しで優先順位を説明 |
| C13 技術品質・信頼性 | PASS | 正本同期後のunittest PASS。通常CIでも再検証対象 |
| C14 計測・グロース | N/A | 計測変更なし |

## 2. 防災サイト固有チェック

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| S01 適用判定 | PASS | E01〜E08,E11〜E14適用 |
| S02 情報設計 | PASS | B007の家具章を実践詳細化。B007との重複は入口/詳細として整理 |
| S03 法務・権利等 | PASS | 画像権利記録あり。製品性能・施工品質をサイト独自保証しない |
| S04 ブランド・トーン | PASS | 「器具を買えば安心」とせず配置変更・専門相談を含める |
| S05 日本向け文脈 | PASS | 消防庁・東京消防庁、賃貸/管理規約等の日本住宅文脈 |
| S06 運用・ガバナンス | PASS | Markdown statusとsource_checked_atを現行レビューへ同期 |
| S07 セキュリティ・外部依存 | PASS | 新規外部機能なし |
| S08 数値 | PASS | 家具高さは配置確認の目安として扱い、安全保証値へ変換しない |

## 3. 安全確認

- PASS: 家具固定を絶対安全と表現しない。
- PASS: 出入口を塞がない配置を固定器具より先に確認する。
- PASS: 石こうボード等へ下地確認なしで固定させない。
- PASS: 一般収納用突っ張り棒を転倒防止用品の代替にしない。
- PASS: 冷蔵庫・テレビ・電子レンジ等はメーカー指定条件を優先する。
- PASS: 高所作業・大型家具は自己流施工を推奨しない。

## 4. 読者・ページ設計

- target_reader: 家具転倒対策を始めたい家庭、賃貸を含む
- usage_context: 平常時の室内安全改善
- reader_problem: 何から固定するか、器具をどう選ぶか分からない
- reader_goal: 危険度の高い場所から実行可能な対策を始める
- page_job: 家具・家電の転倒/落下/移動対策のpractical記事
- next_action: 寝室と出口を30分チェック→必要に応じ固定/管理者/専門家確認

## 5. 証跡

- sources: `docs/research/B023_SOURCES.md`
- article: `content/articles/B023_earthquake_furniture_safety.md`
- preview: `preview/article_b023.html`
- public_path: `earthquake/earthquake-furniture-safety.html`
- registry: 2026-09-04同期

## 6. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 家具配置・施工条件・誤使用防止を現行一次情報で再確認し、情報設計と正本状態も整合。
