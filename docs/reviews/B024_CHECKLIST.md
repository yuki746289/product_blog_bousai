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
- last_checked_at: 2026-09-15
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

## 1. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 水・トイレ・照明・充電・発電機・復電・食品・集合住宅・在宅避難終了条件を一連で整理 |
| C02 出典・安全性 | PASS | 内閣府・消防庁等の公的情報を基準に安全境界を維持 |
| C03 画像・視覚要素 | PASS | 安全判断を画像へ依存させない |
| C04 読みやすさ・UI | PASS | ライフライン別の判断単位へ再構成 |
| C05 内部リンク | PASS | B007/B004/B003/B023/B039/B040へ役割別導線 |
| C06 商品導線・商品記事 | PASS | 水・トイレ・ライト・電源の内部比較を安全説明後に配置 |
| C07 Q&A | N/A | 本文で主要疑問を完結 |
| C08 同期・公開前 | PASS | Markdown/preview/registryを2026-09-15レビューへ同期 |
| C09 日付・構造化データ | PASS | registry更新対象 |
| C10 デザイン・UX | PASS | 見出し・リスト・関連記事で判断順を明確化 |
| C11 読者・マーケティング | PASS | 被災直後の安全と平常時備蓄を分離 |
| C12 アクセシビリティ | PASS | 危険事項を文章・リストで表示 |
| C13 技術品質・信頼性 | PASS | CI回帰テスト対象 |
| C14 計測・グロース | N/A | 計測変更なし |

## 2. 防災サイト固有チェック

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| S01 適用判定 | PASS | 商品内部導線があるためE09を含めE01〜E09,E11〜E14適用 |
| S02 情報設計 | PASS | B004=停電一般、B024=地震後の停電+断水+排水+復電として分離 |
| S03 法務・権利等 | PASS | 商品導線を公的推奨に見せない |
| S04 ブランド・トーン | PASS | 不安訴求や「これだけで安心」を避ける |
| S05 日本向け文脈 | PASS | 国内の備蓄・排水・集合住宅・発電機注意を前提 |
| S06 運用・ガバナンス | PASS | 数量目安を一律安全保証へ変換しない |
| S07 セキュリティ・外部依存 | PASS | 新規外部JS/APIなし |
| S08 数値 | PASS | 3L/日、5回/日、35回/週は用途・前提付きで維持 |

## 3. 安全・誤判断防止確認

- PASS: 上水道が使えても排水設備確認前にトイレを安易に流さない。
- PASS: 発電機は屋内・物置・車庫など換気の悪い場所で使用しない。
- PASS: 避難を遅らせてブレーカー操作を行わせない。
- PASS: 浸水・破損した機器を安易に再通電しない。
- PASS: 復電時の火災防止を導入段階から明示。
- PASS: 冷蔵食品を臭い・見た目だけで安全判断しない。
- PASS: 備蓄が残っていても建物・衛生・医療・暑寒リスクが高まれば在宅避難継続を前提にしない。

## 4. 読者・ページ設計

- target_reader: 地震による停電・断水・排水停止に備える家庭
- usage_context: 平常時の備蓄確認〜地震後の在宅避難判断
- reader_problem: 水だけ備えればよいのか、トイレ・電源・復電時に何が危険か分からない
- reader_goal: 必要量と危険行動、在宅避難の終了条件を把握する
- page_job: 地震後ライフライン停止のdetail記事
- next_action: 水/トイレ数量確認→照明/充電確認→排水/発電機/復電の安全ルール共有

## 5. 証跡

- sources: `docs/research/B024_SOURCES.md`
- article: `content/articles/B024_earthquake_blackout_water_outage.md`
- preview: `preview/article_b024.html`
- public_path: `earthquake/earthquake-blackout-water-outage.html`
- registry: 2026-09-15同期

## 6. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 停電・断水・排水・復電・一酸化炭素・在宅避難終了条件を一つの判断経路へ整理し、安全境界を維持。

<!-- content-depth-20260907:metric -->
## 2026-09-07 本文量・読者満足度の再確認

- reader_visible_char_count: **2,863字**
- guideline_minimum: **2,500字**
- length_status: **PASS**
- editorial_note: 当時点の履歴として保持。
<!-- /content-depth-20260907:metric -->

## 2026-09-15 説明品質再レビュー

- reader_visible_char_count: **2,825字**
- guideline_minimum: **2,500字**
- length_status: **PASS**
- explanation_quality_priority: **46**（自動品質点ではなく、次回レビュー優先度）
- PASS: 導入で「停電・断水」と「復電時の火災防止」を明示。
- PASS: 備蓄量だけでなく、設備を使えるか・在宅避難を続けられるかの判断へ再構成。
- PASS: 発電機・復電・排水の安全境界を維持。
- editorial_note: 旧版より文字数はわずかに減ったが、重複を減らし判断単位を明確化したためPASS。

<!-- sitewide-editorial-rereview-20260920 -->
## 2026-09-20 全記事編集品質再レビュー
- sitewide_editorial_rereview: `PASS`
- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- title_h1_answer_alignment: `PASS`
- heading_reader_facing: `PASS`
- answer_first: `PASS`
- ai_template_review: `PASS`
- production_memo_review: `PASS`
- checklist_refs: `docs/ARTICLE_REVIEW_CHECKLIST.md`, `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`, `docs/EXPLANATION_QUALITY_PREFLIGHT.md`, `docs/ARTICLE_STORY_QUALITY_GATE.md`
- review_note: タイトル/H1、導入、主要H2、章冒頭、制作メモ混入、同系記事との定型重複を再確認。読者への結論が早い段階で分かるためPASS。
<!-- /sitewide-editorial-rereview-20260920 -->
