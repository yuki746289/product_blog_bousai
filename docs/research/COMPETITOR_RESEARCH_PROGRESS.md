# 防災くらしガイド 競合・ニッチサイト比較 進捗管理

更新日: 2026-09-10

作業ブランチ: `research/competitor-seo-20260910`

## 運用方針

- このファイルを競合調査の進捗正本とする。
- 1記事の調査を開始・完了するたびに更新する。
- Search Consoleで新しいデータが入った場合は、調査開始前にGSC欄と `COMPETITOR_SEARCH_QUERIES.md` を更新する。
- 競合調査中は記事本文を変更しない。まず調査結果とA/B/C/D/E判定を確定する。
- 記事修正は調査結果をユーザーと確認後、別の実装ブランチで行う。
- GitHub Actions節約のため、この調査ブランチでは原則PR作成・mainマージ・Actions手動実行を行わない。調査セットがまとまった段階で必要なら一括PRを作成する。

## ステータス定義

- `WAIT`: 未着手
- `QUERY_READY`: 検索語準備済み
- `SERP`: 上位SERP調査中
- `NICHE`: ニッチサイト調査中
- `COMPARE`: 3方向比較中
- `REVIEW`: A/B/C/D/E判定・修正案レビュー待ち
- `DONE`: 調査完了
- `MONITOR`: 記事修正後のSearch Console経過観察

## 全体進捗

| 優先 | 記事 | GSC確認 | 検索語 | 上位SERP | ニッチ | 3方向比較 | A/B/C/D/E | 修正案 | 状態 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | B008 車の冠水・水没 | 済 | 済 | 未 | 未 | 未 | 未 | 未 | `QUERY_READY` |
| 2 | B019 水害・台風・地震と保険 | 済 | 済 | 未 | 未 | 未 | 未 | 未 | `QUERY_READY` |
| 3 | B010 地下駐車場×大雨 | 済 | 済 | 未 | 未 | 未 | 未 | 未 | `QUERY_READY` |
| 4 | B022 マンション×台風・水害 | 済 | 済 | 未 | 未 | 未 | 未 | 未 | `QUERY_READY` |

## 初期GSCスナップショット

2026-09-10取得分を初期基準とする。データ量が少ないため、値は順位確定値ではなく調査優先順位を決める材料として扱う。

| 記事 | 公開ページ | 表示回数目安 | 平均順位目安 | Click | 初期判断 |
|---|---|---:|---:|---:|---|
| B008 | `/vehicle/car-flood-submersion.html` | 約100 | 約5.2 | 0 | 最優先。高順位・表示ありのためSERP差分確認 |
| B019 | `/insurance/disaster-insurance-overview.html` | 約46 | 約6.8 | 0 | 検索意図と保険子記事との役割分担を確認 |
| B010 | `/vehicle/underground-parking-heavy-rain.html` | 約26 | 約7.7 | 0 | ケース特化型として有望か確認 |
| B022 | `/home/apartment-typhoon-flood.html` | 約13 | 約5.2 | 0 | マンション特化のニッチ性を確認 |

## 調査ファイル

- `docs/research/COMPETITOR_RESEARCH_CHECKLIST.md`
  - 3方向比較のチェックリストとA/B/C/D/E判定ルール
- `docs/research/COMPETITOR_SEARCH_QUERIES.md`
  - 実際に検索するワード一覧
- `docs/research/COMPETITOR_RESEARCH_PROGRESS.md`
  - 本ファイル。進捗正本

今後、記事ごとの調査結果は以下の形式で追加する。

- `docs/research/competitor/B008_COMPETITOR_RESEARCH.md`
- `docs/research/competitor/B019_COMPETITOR_RESEARCH.md`
- `docs/research/competitor/B010_COMPETITOR_RESEARCH.md`
- `docs/research/competitor/B022_COMPETITOR_RESEARCH.md`

## 優先1: B008 車の冠水・水没

- source: `content/articles/B008_car_flood_submersion.md`
- 状態: `QUERY_READY`
- Search Console初期確認: 完了
- 検索語セット: 完了
- 上位SERP: 未着手
- 上位主要ページ詳細: 未着手
- ニッチサイト探索: 未着手
- 上位 vs 自サイト: 未着手
- 上位 vs ニッチ: 未着手
- ニッチ vs 自サイト: 未着手
- カニバリ確認: B009 / B011を重点確認予定
- A/B/C/D/E判定: 未着手
- 修正候補一覧: 未着手

次の作業: `COMPETITOR_SEARCH_QUERIES.md` のB008検索語を使ってSERP調査を開始する。

## 優先2: B019 水害・台風・地震と保険

- source: `content/articles/B019_disaster_insurance_overview.md`
- 状態: `QUERY_READY`
- Search Console初期確認: 完了
- 検索語セット: 完了
- 上位SERP: 未着手
- ニッチサイト探索: 未着手
- カニバリ確認: B011 / B013 / B014 / B016 / B017 / B018 / B051 / B052を重点確認予定
- A/B/C/D/E判定: 未着手
- 修正候補一覧: 未着手

## 優先3: B010 地下駐車場×大雨

- source: `content/articles/B010_underground_parking_heavy_rain.md`
- 状態: `QUERY_READY`
- Search Console初期確認: 完了
- 検索語セット: 完了
- 上位SERP: 未着手
- ニッチサイト探索: 未着手
- カニバリ確認: B008 / B009 / B011を重点確認予定
- A/B/C/D/E判定: 未着手
- 修正候補一覧: 未着手

## 優先4: B022 マンション×台風・水害

- source: `content/articles/B022_apartment_typhoon_flood.md`
- 状態: `QUERY_READY`
- Search Console初期確認: 完了
- 検索語セット: 完了
- 上位SERP: 未着手
- ニッチサイト探索: 未着手
- カニバリ確認: B012 / B020 / B021 / B046を重点確認予定
- A/B/C/D/E判定: 未着手
- 修正候補一覧: 未着手

## 調査1記事あたりの完了条件

以下がすべて満たされたとき `DONE` とする。

- [ ] 最新Search Console確認
- [ ] 検索語一覧更新
- [ ] 主検索語の上位SERP確認
- [ ] 上位3〜5ページの内容比較
- [ ] ニッチサイトを複数探索
- [ ] 上位 vs 自サイト比較
- [ ] 上位 vs ニッチ比較
- [ ] ニッチ vs 自サイト比較
- [ ] 自サイト内カニバリ確認
- [ ] 「なぜ上位か」仮説作成
- [ ] A/B/C/D/E判定
- [ ] 修正候補一覧作成
- [ ] 変更しない項目も理由付きで記録

## 変更履歴

### 2026-09-10

- 競合・ニッチサイト比較の調査運用を開始。
- 初期優先4記事を設定。
- 3方向比較チェックリストを作成。
- GSC連動型の検索ワード一覧を作成。
- 進捗管理を本ファイルに一本化。
