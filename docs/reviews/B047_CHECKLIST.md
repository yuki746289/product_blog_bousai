# B047 記事別レビュー記録

- article_id: B047
- risk_level: high
- article_status: READY_TO_PUBLISH
- review_status: PASS
- last_checked_at: 2026-09-06
- target_commit: 作業ブランチ `fix/b047-content-sync-20260906`
- persona_mode: SITUATIONAL_SEGMENT

## 1. 今回の確認範囲

原稿 `content/articles/B047_blackout_heatstroke.md` と公開元 `preview/article_b047.html` を照合し、`scripts/build_public.py` が生成した `public/blackout/blackout-heatstroke.html` まで確認した。

| 項目 | 状態 | 根拠・確認箇所 |
|---|---|---|
| 検索意図・カニバリ | PASS | B004は停電全般、B047は真夏の停電中の熱中症判断。原稿・HTMLのtitle/H1/本文で役割を確認 |
| 一次情報・医療境界 | PASS | `docs/research/B047_SOURCES.md`、原稿、preview、公的情報リンクを確認。独自の一律水分量を示していない |
| 救急判断 | PASS | 原稿・preview・生成publicに「自力で水が飲めない、意識がない場合」の救急要請を確認 |
| 移動判断 | PASS | 原稿・preview・生成publicに、室温上昇時の早期移動と他災害の移動リスクを確認 |
| 発電機 | PASS | 原稿・preview・生成publicに、屋内・車庫・換気不十分な場所で使わない旨を確認 |
| 扇風機の限界 | PASS | 原稿・preview・生成publicに、長時間自宅で大丈夫とは考えない旨を確認 |
| 停電前の準備 | PASS | 原稿の第9章をpreviewへ反映し、生成publicで確認 |
| 内部リンク | PASS | B004・B028・B044への文脈リンクと関連記事をpreview・生成publicで確認 |
| 保存用チェック | PASS | 原稿の9項目をpreviewへ反映し、生成publicで確認 |
| 商品導線 | N/A | 直接Amazon導線なし。安全行動が主目的 |
| 画像 | PASS | `docs/research/B047_IMAGES.md` の0枚とする理由を確認。要点、箇条書き、チェックリストで長文を分節 |

## 2. 専門家・技術確認

- E01〜E08: PASS。文章構成、安全性、検索意図、導線、可読性、アクセシビリティ、トーンを確認。
- E09: N/A。商品記事・直接購入CTAではない。
- E10: N/A。計測施策・独自集計・数値比較を追加していない。
- E11〜E14: PASS。内部リンク変換、外部リンク属性、日本向け表現、日付・台帳を確認。
- 最終HTML回帰検査: `tests/test_public_build.py::PublicBuildTests::test_b047_public_output_keeps_safety_and_preparation_content`。
- 原稿・preview同期検査: `tests/test_b044_b047_keyword_batch.py::KeywordBatchSafetyTests::test_b047_heatstroke_boundaries`。

## 3. 最終判定

- READY_TO_PUBLISH: YES
- 公開前残作業: 通常のテスト、変更レビュー、main反映、必要なデプロイ、本番HTTP確認
- 判定理由: 既知の原稿・公開HTML不整合を解消し、安全条件・準備・内部リンクが最終生成HTMLまで残る回帰検査を追加したため
