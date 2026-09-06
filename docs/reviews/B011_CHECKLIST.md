# B011 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B011`
- title: 台風・洪水で水没した車は車両保険の対象になる？
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
| C01 内容・情報量 | PASS | detail記事として判断条件・例外・事故後手順まで必要十分 |
| C02 出典・安全性 | PASS | 4件。2026年8月の大雨案内と現行車両保険Q&Aまで再確認 |
| C03 画像・視覚要素 | PASS | 既存の日本文脈・権利・関連性レビューを継承。画像を補償判断の根拠にしない |
| C04 読みやすさ・UI | PASS | 表・手順・注意枠・Q&A導線を既存UIで整理 |
| C05 内部リンク | PASS | 関連する車・住宅・保険総論/詳細記事へ接続 |
| C06 商品導線・商品記事 | N/A | 保険商品の販売・比較・見積もり誘導なし |
| C07 Q&A | PASS | 既存個別Q&Aへの文脈リンクと本文結論が整合 |
| C08 同期・公開前 | PASS | article/source/preview/registry/checklistを2026-09-04監査へ同期 |
| C09 日付・構造化データ | PASS | registryの日付を正本としてproduction buildへ反映 |
| C10 デザイン・UX | PASS | 既存記事UIを使用し役割の異なる要素を混同させない |
| C11 読者・マーケティング | PASS | 不安を煽って加入・修理契約へ誘導せず、契約確認と安全行動を次アクションにする |
| C12 アクセシビリティ | PASS | 色依存なし。見出し・表・リンクテキストで意味を伝達 |
| C13 技術品質・信頼性 | PASS | production build/test/smoke対象 |
| C14 計測・グロース | N/A | 計測変更なし |

## 2. 防災サイト固有チェック

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| S01 適用判定 | PASS | 保険・安全記事としてE01〜E07,E11〜E14を適用。E08/E09はN/A |
| S02 情報設計 | PASS | B019総論と役割分離し、この記事固有の損害・契約確認へ絞る |
| S03 法務・権利等 | PASS | 個別契約の支払可否・責任・認定額を断定しない |
| S04 ブランド・トーン | PASS | 安全→事実記録→契約確認の順。過度な不安・販売訴求なし |
| S05 日本向け文脈 | PASS | 日本損害保険協会・金融庁/国民生活センター等の国内資料中心 |
| S06 運用・ガバナンス | PASS | staleなREVIEW_REQUIREDを解消し、出典確認日・台帳・previewを同期 |
| S07 セキュリティ・外部依存 | PASS | 公的・業界公式リンクのみ。新規外部機能なし |
| S08 数値 | PASS | 契約差の大きい金額・免責・認定基準を一律化しない |

## 3. 保険・安全誤認防止確認

- PASS: 台風・洪水・高潮は車両保険の補償例だが契約差を明記
- PASS: 地震・噴火・津波は通常補償と分離し特約確認へ誘導
- PASS: 浸水車を始動させず、冠水区域へ写真撮影のため戻らせない
- PASS: 全損・等級・代車・レッカーを一律断定しない

## 4. 読者・ページ設計

- target_reader: 災害前後に自分の補償範囲や手順を確認したい一般契約者
- usage_context: 平常時の契約確認、被害直後の初動整理
- reader_problem: 災害名や被害の見た目だけで補償可否を判断しやすい
- reader_goal: 原因・対象・契約条件を分け、安全に次の手続きへ進む
- page_job: 台風・洪水・高潮による車両損害を、津波等と分離して契約確認へ導く
- next_action: 車両保険・免責・原因を確認し、危険区域へ戻らず契約先へ連絡

## 5. 証跡

- sources: `docs/research/B011_SOURCES.md`
- article: `content/articles/B011_flooded_car_insurance.md`
- preview: `preview/article_b011.html`

## 6. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 2026-09-04時点の現行補償体系、安全表現、記事役割、出典鮮度、内部導線を再監査し、公開済み正本とレビュー状態を同期。
