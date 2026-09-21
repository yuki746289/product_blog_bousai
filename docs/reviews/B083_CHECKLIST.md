# B083 記事別レビュー記録

- article_id: B083
- title: 宮崎県の線状降水帯｜2024年10月・2025年9月の発生史と山沿い・河川の備え
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
- 2023-05-25以降の公式事例と、それ以前の豪雨史の区別: PASS
- 洪水・土砂災害に対応する避難場所の確認導線: PASS
- 発生情報を待って避難を開始する誤誘導なし: PASS
- 公式情報・一次資料: PASS

## 共通レビュー

詳細は `docs/reviews/LINEAR_RAINBAND_PREFECTURES_BATCH1_CHECKLIST_20260921.md` を参照。


## 事例品質再監査（2026-09-21）

- C02-07 独立イベント数: PASS（発生確認2件）
- C02-08/C02-09 重複確認: PASS
- C02-10 発生実績 / 予測 / 制度・関連豪雨の分類: PASS
- C02-12 直近事例再検索: PASS
- 最新の発生確認: 2025年9月4〜5日
- 修正: 2025年8月10〜11日は予測・大雨として分離し、発生件数に含めない。時系列順を修正。
- 本番デプロイ・production workflow: **未実行（ユーザー許可制）**
