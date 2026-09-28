# SERP metadata review 2026-09-28

対象:
- B067 線状降水帯特集
- B094 愛知県・名古屋
- B097 線状降水帯とゲリラ豪雨の違い
- B008 車の冠水・水没
- B019 災害保険

根拠資料:
- `docs/research/SERP_CTR_COMPETITOR_REVIEW_20260928.md`
- `docs/COMMON_SITE_CHECKLIST.md` GC03 / GC03-SERP
- 2026-09-02〜2026-09-27 Search Console基準値

## GC03-SERP 実施結果

| チェック | 判定 | 記録 |
|---|---|---|
| 主クエリ・代表関連クエリ確認 | PASS | GSC実クエリを使用 |
| 上位SERP比較 | PASS | 5対象テーマで公式・企業・解説系を比較 |
| SERPタイトル / snippet確認 | PASS | 検索結果側とページ側設定を分離 |
| ページtitle / H1 / meta description確認 | PASS | mainの現行設定を確認 |
| パンくず / site name / favicon | MONITOR | サイト側実装済み。Google側再クロール後に実表示確認 |
| titleの主検索意図前方配置 | PASS | 5ページとも満たす |
| 競合コピーなし | PASS | 自ページの役割差を維持 |
| descriptionの具体性 | PASS | 5ページとも対象・比較軸・行動等を具体化 |
| 変更前GSC基準値 | PASS | researchファイルへ保存 |
| 変更仮説 | PASS | 各ページへ記録 |
| 直近変更のSERP反映確認 | PARTIAL | B008は反映確認、B067/B094/B097/B019は未確認または旧表示残存 |
| 連続変更回避 | PASS | 明確な誤りがないmetadataは再変更しない |
| 公開後評価条件 | PASS | CTR / 順位 / 表示 / query構成で評価 |

## ページ別判定

| ID | title | description | SERP反映 | 今回判定 |
|---|---|---|---|---|
| B067 | PASS | PASS | 旧title残存 | MONITOR |
| B094 | PASS | PASS | 旧title残存 | MONITOR |
| B097 | PASS | PASS | 旧title残存 | MONITOR |
| B008 | PASS | PASS | 新title確認 | PASS / MONITOR |
| B019 | PASS | PASS | direct表示未確認 | MONITOR |

## 今回の実修正

- B097の関連記事リンクに残っていたB067旧titleを現行titleへ更新。
- title / meta description本体は、直近変更がSERPへ未反映のため追加変更しない。

## 次回再評価

再クロール後、以下を確認してから次のtitle / description変更を判断する。

- B094: `名古屋 線状降水帯` のCTR・順位
- B097: `線状降水帯 ゲリラ豪雨 違い` のCTR・順位
- B008: 平均順位6位前後を維持したままCTRが改善するか
- B019: direct SERP表示とCTR
- B067: 履歴系queryのCTRとpillar全体の表示回数

明確な誤りがない限り、SERP未反映中に再変更しない。
