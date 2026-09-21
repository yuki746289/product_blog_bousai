# B087 記事別レビュー記録

- article_id: B087
- title: 高知県の線状降水帯｜2022年7月・2023年6月の発生史と多雨地形
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

- 県固有確認: 2022/2023年事例 / 四国南東斜面 / 夜間避難 / 高知県防災アプリ: PASS

## 共通レビュー

詳細は `docs/reviews/LINEAR_RAINBAND_PREFECTURES_BATCH2_CHECKLIST_20260921.md` を参照。


## 事例品質再監査（2026-09-21）

- C02-07 独立イベント数: PASS（線状降水帯2件（2022旧制度期＋2023現行））
- C02-08/C02-09 重複確認: PASS
- C02-10 発生実績 / 予測 / 制度・関連豪雨の分類: PASS
- C02-12 直近事例再検索: PASS
- 最新の発生確認: 2023年6月2日
- 修正: 2023年6月2日と6月1〜3日の重複を解消。2025年9月は関連大雨・突風として分離。2026年9月21日時点でより新しい県内発生を確認できず。
- 本番デプロイ・production workflow: **未実行（ユーザー許可制）**
