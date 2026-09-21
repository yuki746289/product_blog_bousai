# B089 記事別レビュー記録

- article_id: B089
- title: 三重県の線状降水帯｜2023年6月・2024年8月の発生事例と紀伊半島の大雨
- content_role: detail
- risk_level: standard
- article_status: READY_TO_PUBLISH
- review_status: PASS
- last_checked_at: 2026-09-21
- reviewer: ChatGPT

## 判定

- review_checklist_status: PASS
- READY_TO_PUBLISH: YES
- production_build_status: READY_FOR_DEPLOY
- 本文2,500字以上: PASS
- 県固有の時系列・地形・避難情報: PASS
- 現行統一一覧の期間と、それ以前の豪雨史の区別: PASS
- 洪水・土砂・内水等を地域条件に応じて区別: PASS
- 発生情報だけを避難開始条件にする誤誘導なし: PASS
- 県・市町村公式の避難・ハザード導線: PASS
- 公的情報・一次資料: PASS

- 県固有確認: 2023年県内初発表 / 2024年北中部 / 伊勢志摩・東紀州と北中部の差: PASS

## 共通レビュー

詳細は `docs/reviews/LINEAR_RAINBAND_PREFECTURES_BATCH2_CHECKLIST_20260921.md` を参照。


## 事例品質再監査（2026-09-21）

- C02-07 独立イベント数: PASS（現行発生2件＋関連豪雨史1件）
- C02-08/C02-09 重複確認: PASS
- C02-10 発生実績 / 予測 / 制度・関連豪雨の分類: PASS
- C02-12 直近事例再検索: PASS
- 最新の発生確認: 2024年8月31日
- 修正: 2026年9月21日時点で、より新しい県内発生を一次資料で確認できないため予測だけを追加しない。
- 本番デプロイ・production workflow: **未実行（ユーザー許可制）**
