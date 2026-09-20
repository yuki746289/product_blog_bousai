# B047 記事別レビュー記録

- article_id: B047
- risk_level: high
- article_status: READY_TO_PUBLISH
- review_status: PASS
- last_checked_at: 2026-09-15
- target_branch: `content/explanation-quality-b018-b024-b040-b043-b047-b052-b058-20260915`
- persona_mode: SITUATIONAL_SEGMENT

## 1. 今回の確認範囲

原稿 `content/articles/B047_blackout_heatstroke.md` と公開元 `preview/article_b047.html`、生成される `public/blackout/blackout-heatstroke.html` の安全境界を確認した。

| 項目 | 状態 | 根拠・確認箇所 |
|---|---|---|
| 検索意図・カニバリ | PASS | B004は停電全般、B047は真夏の停電中の熱中症判断として役割分離 |
| 一次情報・医療境界 | PASS | 厚生労働省の災害時熱中症対策・応急処置、環境省のクーリングシェルター情報を再確認 |
| 救急判断 | PASS | 「自力で水が飲めない、意識がない場合」の救急要請を維持 |
| 移動判断 | PASS | 室温上昇・体調悪化を待たず、冷房のある場所へ移れるうちに移る判断を前面化 |
| 要配慮者 | PASS | 高齢者・乳幼児・持病のある人を本人の申告待ちにしない |
| クーリングシェルター | PASS | 全国一律に自動開設されるとは扱わず、開設状況・移動安全性を確認 |
| 発電機 | PASS | 屋内・車庫・換気不十分な場所で使わない旨を維持 |
| 扇風機の限界 | PASS | 「長時間自宅で大丈夫とは考えません」を生成publicまで回帰確認 |
| 停電前の準備 | PASS | 冷房のある移動先を複数候補化し、移動条件まで平時に確認 |
| 内部リンク | PASS | B004・B025・B028・B044へ文脈リンク |
| 保存用チェック | PASS | 移動・要配慮者・救急・発電機の判断を保存用チェックへ反映 |
| 商品導線 | N/A | 直接Amazon導線なし。安全行動が主目的 |
| 画像 | PASS | 画像0枚の既存判断を維持。見出し・リスト・チェックリストで分節 |

## 2. 専門家・技術確認

- E01〜E08: PASS。文章構成、安全性、検索意図、導線、可読性、アクセシビリティ、トーンを確認。
- E09: N/A。商品記事・直接購入CTAではない。
- E10: N/A。独自の安全温度・一律水分量を追加していない。
- E11〜E14: PASS。内部リンク、外部一次情報、日本向け表現、日付・台帳を確認。
- 最終HTML回帰検査: `tests/test_public_build.py::PublicBuildTests::test_b047_public_output_keeps_safety_and_preparation_content`。
- 原稿・preview同期検査: `tests/test_b044_b047_keyword_batch.py::KeywordBatchSafetyTests::test_b047_heatstroke_boundaries`。

## 3. 最終判定

- READY_TO_PUBLISH: YES
- 判定理由: 停電時に家で耐える前提を外し、冷却・飲水・移動・救急判断の順を明確化しつつ、発電機・他災害時の移動リスクも維持したため。

<!-- content-depth-20260907:metric -->
## 2026-09-07 本文量・読者満足度の再確認

- reader_visible_char_count: **3,386字**
- guideline_minimum: **3,000字**
- length_status: **PASS**
- counting_method: frontmatter・URL・Markdown記号・公的情報/出典一覧を除き、読者が読む本文の非空白文字を同一スクリプトで計測。
- editorial_note: 当時点の履歴として保持。
<!-- /content-depth-20260907:metric -->

## 2026-09-15 説明品質再レビュー

- reader_visible_char_count: **3,034字**
- guideline_minimum: **3,000字**
- length_status: **PASS**
- explanation_quality_priority: **29**（自動品質点ではなく、次回レビュー優先度）
- PASS: 「家で耐える」から、冷房のある場所へ移れるうちに移る判断へ再構成。
- PASS: 高齢者・乳幼児・持病のある人を先に確認する流れを明確化。
- PASS: 自力飲水不可・意識異常時の救急要請を維持。
- PASS: クーリングシェルターは開設状況を確認し、暴風・冠水等がある場合は移動安全性を別に判断。
- PASS: 発電機の一酸化炭素中毒境界を維持。
- editorial_note: 文字数を満たすための水増しではなく、移動先を複数持つことと移動判断の前倒しを実用情報として補足した。

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
