# B091 記事別レビュー記録

- article_id: B091
- title: 千葉県の線状降水帯｜過去の発生履歴・直近事例を一覧で解説
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

- 県固有確認: 2019/2023/2026年 / 予測なし急変 / 内水・河川・土砂: PASS

## 共通レビュー

詳細は `docs/reviews/LINEAR_RAINBAND_PREFECTURES_BATCH2_CHECKLIST_20260921.md` を参照。


## 事例品質再監査（2026-09-21）

- C02-07 独立イベント数: PASS（現行発生2件＋関連豪雨史1件）
- C02-08/C02-09 重複確認: PASS
- C02-10 発生実績 / 予測 / 制度・関連豪雨の分類: PASS
- C02-12 直近事例再検索: PASS
- 最新の発生確認: 2026年8月13〜14日
- 修正: 2019年を関連豪雨史、2023/2026年を発生確認事例として分離。
- 本番デプロイ・production workflow: **未実行（ユーザー許可制）**


## 事例表構造再監査（2026-09-21）

- C02-16 直近事例 / 過去代表事例の分離: PASS / N/A（過去代表表が不要な記事は無理に作成しない）
- C02-17 直近事例を最新時点まで再確認: PASS（件数合わせなし）
- C02-18 局地的大雨を掲載する場合の現象区別: PASS
- C02-19 日時・雨量・公式発表・被害の確認: PASS（確認できる項目を掲載）
- C02-20 警戒レベルの独自推定なし: PASS
- C02-21 過去事例を代表例へ限定: PASS / N/A
- C02-22 予測・制度のみの情報を実発生と分離: PASS
- C02-23 県別シリーズ対象の実発生確認: PASS
- C02-24 GSCを踏まえた県別title統一: PASS
- 構成: 直近2件＋過去代表1件。2表へ分離。
- 本番デプロイ: 未実行（ユーザー許可制）
