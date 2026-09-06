# B038 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B038`
- title: 大地震で電車が止まったら帰宅する？帰宅困難者がまず取る行動と備え
- content_role: `practical`
- risk_level: `elevated`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-04
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

## 1. 適用プロファイル確認

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| 防災サイトプロファイル確認 | PASS | 帰宅判断に関わるelevated情報記事として適用 |
| 必須専門家ロール選定 | PASS | E01〜E08,E11〜E14 |
| 条件付き専門家ロール判定 | PASS | E09/E10はN/A |
| 詳細架空ペルソナ | N/A | 通勤・通学・買い物等の状況ベース読者設定 |
| N/A項目の理由確認 | PASS | 商品比較・独自計測を主目的としない |

## 2. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 発災直後→待機→施設→72時間→分散帰宅→平時準備まで一連で整理 |
| C02 出典・安全性 | PASS | 令和8年1月内閣府ガイドライン、令和8年版防災白書、政府広報を一次根拠に使用 |
| C03 画像・視覚要素 | PASS | 日本の実災害Commons画像1点＋行動フロー・施設比較表を使用 |
| C04 読みやすさ・UI | PASS | 結論・安全ボックス・比較表・チェックリストを配置 |
| C05 内部リンク | PASS | B007/B030/B002/B024と地震カテゴリから回遊設計 |
| C06 商品導線・商品記事 | N/A | 商品購入を主目的にしない |
| C07 Q&A | N/A | 本文で主要疑問に回答。重複Q&Aを増やさない |
| C08 同期・公開前 | PASS | Markdown / preview / research / checklist / registry / category / parent導線を同期対象とした |
| C09 日付・構造化データ | PASS | registryから公開日・更新日・BlogPosting / BreadcrumbList生成対象 |
| C10 デザイン・UX | PASS | 緊急時に「すぐ帰らない」「危険なら避難」を上部で理解できる |
| C11 読者・マーケティング | PASS | 不安を商品購入へ誘導せず、安全行動と家族ルールへ接続 |
| C12 アクセシビリティ | PASS | 横スクロール表へrole/aria-label/tabindexを付与し、色依存なし |
| C13 技術品質・信頼性 | PASS | 共通CSS/JSのみ利用。新規外部スクリプトなし |
| C14 計測・グロース | N/A | 新規イベントなし |

## 3. 防災サイト固有チェック結果

| サイト固有チェック | 状態 | 根拠・備考 |
|---|---|---|
| S01 サイトプロファイル・適用判定 | PASS | 安全・一次情報をSEOや回遊より優先 |
| S02 情報設計・ファインダビリティ | PASS | B007=地震pillar、B030=家族連絡、B038=本人の外出先移動判断として分離 |
| S03 法務・権利・広告表示・プライバシー | PASS | Commons CC BY-SA 3.0の作者・出典・ライセンス表示。商品広告なし |
| S04 ブランド・トーン・コンテンツデザイン | PASS | 家族不在の不安を煽らず、行動順を具体化 |
| S05 日本向けローカライゼーション | PASS | 日本の内閣府制度用語と2026年改定ガイドラインに合わせた |
| S06 運用・ガバナンス・保守性 | PASS | source_checked_at / next_review_at / evidence docsを設定 |
| S07 セキュリティ・外部依存 | PASS | Commons画像は既存production buildでローカル化対象。公的情報は外部リンク |
| S08 数値・統計・リアルタイム要約 | PASS | 72時間の意味を一次情報で確認し、独自距離閾値を作成していない |

## 4. Elevatedリスク追加確認

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| 「むやみに移動しない」を危険場所への残留と誤解させない | PASS | 火災・津波・建物危険時は生命を守る避難優先と明記 |
| 72時間を全国一律の絶対待機時間にしない | PASS | ガイドラインの前提と例外を明記 |
| 4日目なら必ず帰宅できると書かない | PASS | 交通・道路等の安全保証ではないと明記 |
| 独自の徒歩帰宅距離基準を作らない | PASS | ○km基準なし |
| 一時滞在施設と駅を同一視しない | PASS | すべての駅が施設ではないと明記 |
| 帰宅支援ステーションを帰宅開始の合図にしない | PASS | 混乱収拾後の徒歩帰宅支援と説明 |
| 施設開設・支援提供を保証しない | PASS | 被害・地域・営業状況等で異なると明記 |
| 子どもの迎えを無条件に促さない | PASS | 自治体・学校・保育施設の引き渡しルールと経路安全を優先 |
| SNSだけで交通再開を判断させない | PASS | 公的機関・交通事業者・施設管理者を優先 |

## 5. 読者・ページ設計の証跡

- target_reader: 通勤・通学・買い物・観光等で自宅から離れているときに大地震へ遭う可能性がある一般生活者
- usage_context: 平時準備 / 大地震発生直後 / 公共交通停止時
- knowledge_level: beginner/basic
- urgency_level: preparing/imminent/post-disaster
- reader_problem: 徒歩帰宅すべきか、72時間とは何か、どこで待つか分からない
- reader_goal: 現在地の安全を優先し、待機・一時滞在・帰宅開始を適切に判断する
- page_job: 2026年現行の帰宅困難者対策を個人の行動順へ翻訳する
- entry_path: 検索 / B007 / 地震カテゴリ / B030
- next_action: 安全確認→待機先確認→安否連絡→公的情報→分散帰宅
- conversion_path: 安全行動→B030/B002/B024
- design_priority: 緊急時でも上部だけで誤行動を避けられること

## 6. 証跡

- gap review: `docs/research/EARTHQUAKE_CONTENT_GAP_REVIEW_20260904.md`
- brief: `docs/research/B038_STRANDED_COMMUTER_BRIEF.md`
- sources: `docs/research/B038_SOURCES.md`
- images: `docs/research/B038_IMAGES.md`
- article: `content/articles/B038_earthquake_stranded_commuter.md`
- preview: `preview/article_b038.html`
- public_path: `earthquake/earthquake-stranded-commuter.html`
- content_registry: 登録対象
- category: `category_earthquake`掲載対象

## 7. 公開後確認

- production build / JS / Commons localization / FTPS / HTTP smokeをPASSさせる。
- Search Console蓄積後、B007/B030とのクエリ競合を確認する。
- 制度改定、一時滞在施設・帰宅支援制度の大幅変更があればsource reviewを前倒しする。

## 8. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 一次情報、カニバリ、安全上の例外条件、72時間の誤解防止、権利、UX、アクセシビリティを確認済み。公開時にCI・本番スモークを最終確認する。
