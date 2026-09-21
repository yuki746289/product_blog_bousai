# B092 記事別レビュー記録

- article_id: B092
- title: 東京都の線状降水帯｜過去の発生履歴・直近事例を一覧で解説
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
- 現行統一一覧と、それ以前の豪雨史の区別: PASS
- 洪水・土砂・内水等を地域条件に応じて区別: PASS
- 発生情報だけを避難開始条件にする誤誘導なし: PASS
- 都府・区市町村公式の避難・ハザード導線: PASS
- 公的情報・一次資料: PASS

- 県固有確認: 2005/2019年 / 内水・地下空間 / 23区東部と西部山地: PASS

## 共通レビュー

詳細は `docs/reviews/LINEAR_RAINBAND_PREFECTURES_BATCH3_CHECKLIST_20260921.md` を参照。


## 事例品質再監査（2026-09-21）

- C02-07 独立イベント数: PASS（発生確認2件＋関連豪雨史2件。2026年9月は発生件数外）
- C02-08/C02-09 重複確認: PASS
- C02-10 発生実績 / 予測 / 制度・関連豪雨の分類: PASS
- C02-12 直近事例再検索: PASS
- 最新の発生確認: 2023年9月8日（線状降水帯）／2026年9月6〜8日（直近大雨・予測）
- 修正: 制度説明行を削除。2022年8月13日・2023年9月8日の実発生を追加。2026年9月は記録的大雨・直前予測と実発生を分離。
- 本番デプロイ・production workflow: **未実行（ユーザー許可制）**


## 事例表構造再監査（2026-09-21）

- C02-16 直近事例 / 過去代表事例の分離: PASS / N/A
- C02-17 直近事例を最新時点まで再確認: PASS（件数合わせなし）
- C02-18 局地的大雨を掲載する場合の現象区別: PASS
- C02-19 日時・雨量・公式発表・被害の確認: PASS（確認できる項目を掲載）
- C02-20 警戒レベルの独自推定なし: PASS
- C02-21 過去事例を代表例へ限定: PASS / N/A
- C02-22 予測・制度のみの情報を実発生と分離: PASS
- C02-23 県別シリーズ対象の実発生確認: PASS
- C02-24 GSCを踏まえた県別title統一: PASS
- 構成: 直近3行（実発生2件＋2026年記録的大雨/予測1件）＋過去代表2件。
- 本番デプロイ: 未実行（ユーザー許可制）
