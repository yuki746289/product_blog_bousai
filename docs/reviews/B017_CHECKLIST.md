# B017 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B017`
- title: 地震保険の基本｜火災保険との違いを整理
- content_role: `pillar`
- risk_level: `elevated`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-04
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

## 1. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 制度概要、建物/家財、保険金額、損害区分、割引、被災後手続きまでpillarとして整理 |
| C02 出典・安全性 | PASS | 財務省・日本損害保険協会の現行制度を2026-09-04再確認 |
| C03 画像・視覚要素 | PASS | 制度説明に不要な被災写真を削減した既存関連性レビューを維持 |
| C04 読みやすさ・UI | PASS | 原因表、損害区分表、契約確認チェックを使用 |
| C05 内部リンク | PASS | B007/B018/B019へ接続し、地震一般・車・保険総論と役割分担 |
| C06 商品導線・商品記事 | N/A | 保険商品販売・見積もり誘導を行わない |
| C07 Q&A | N/A | 本文と公的/業界情報で主要論点を完結 |
| C08 同期・公開前 | PASS | source/article/registryを2026-09-04監査へ同期 |
| C09 日付・構造化データ | PASS | registryのsource_checked_atと既存構造化データ生成を使用 |
| C10 デザイン・UX | PASS | 制度数字を表で整理し、新規独自UIなし |
| C11 読者・マーケティング | PASS | 加入を煽らず「被災後の資金不足」で考える判断軸を提示 |
| C12 アクセシビリティ | PASS | 表・見出し・文章で情報を伝え色依存なし |
| C13 技術品質・信頼性 | PASS | 正本同期ワークフロー内unittest PASS。通常CIでも再検証対象 |
| C14 計測・グロース | N/A | 計測変更なし |

## 2. 防災サイト固有チェック

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| S01 適用判定 | PASS | E01〜E08,E11〜E14適用。保険販売をしないためE09はN/A |
| S02 情報設計 | PASS | B017=住宅/家財の地震保険pillar、B018=車、B019=災害保険総論と分離 |
| S03 法務・権利等 | PASS | 制度一般を説明し、個別契約の補償可否をサイト独自に断定しない |
| S04 ブランド・トーン | PASS | 「加入すべき」と一律誘導せず、制度の限界と資金不足を説明 |
| S05 日本向け文脈 | PASS | 日本の政府再保険制度・地震保険制度の現行内容に準拠 |
| S06 運用・ガバナンス | PASS | 古いREVIEW_REQUIREDを解消しsource_checked_atも同期 |
| S07 セキュリティ・外部依存 | PASS | 公的・業界リンクのみ。新規外部機能なし |
| S08 数値 | PASS | 30〜50%、5,000万円/1,000万円、100/60/30/5%を現行制度で再確認 |

## 3. 制度・誤認防止確認

- PASS: 地震保険は火災保険にセットして契約する。
- PASS: 地震による火災・損壊を通常の火災保険だけで自動補償と説明しない。
- PASS: 保険金額は火災保険金額の30〜50%、限度額は建物5,000万円・家財1,000万円。
- PASS: 現行4区分を全損100%、大半損60%、小半損30%、一部損5%として確認。
- PASS: 自動車を地震保険の家財に含めない。
- PASS: サイト上で個別損害を全損/半損等と認定しない。
- PASS: 地震火災費用保険金と地震保険を同一視しない。

## 4. 読者・ページ設計

- target_reader: 火災保険と地震保険の違いを確認したい持家・賃貸の生活者
- usage_context: 平常時の契約確認、被災後の制度確認
- reader_problem: 火災保険だけで地震損害も補償されると思いやすい
- reader_goal: 対象・金額・損害区分・契約確認点を把握する
- page_job: 地震保険クラスタのpillar
- next_action: 証券で建物/家財・保険金額・連絡先を確認し、車はB018へ分岐

## 5. 証跡

- sources: `docs/research/B017_SOURCES.md`
- article: `content/articles/B017_earthquake_insurance_basics.md`
- preview: `preview/article_b017.html`
- public_path: `insurance/earthquake-insurance-basics.html`
- registry: 2026-09-04同期

## 6. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 現行制度の主要数値・対象範囲を政府/業界一次情報で再確認し、個別契約を断定しない安全な説明を維持。
