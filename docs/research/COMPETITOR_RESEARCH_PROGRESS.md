# 防災くらしガイド 競合・ニッチサイト比較 進捗管理

更新日: 2026-09-11

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
| 1 | B008 車の冠水・水没 | 済 | 済 | 済 | 済 | 済 | 済 | 済 | `DONE` |
| 2 | B019 水害・台風・地震と保険 | 済 | 済 | 済 | 済 | 済 | 済 | 済 | `DONE` |
| 3 | B010 地下駐車場×大雨 | 済 | 済 | 未 | 未 | 未 | 未 | 未 | `QUERY_READY` |
| 4 | B022 マンション×台風・水害 | 済 | 済 | 未 | 未 | 未 | 未 | 未 | `QUERY_READY` |

## 最新GSCスナップショット

2026-09-11取得。GSC確定データは2026-09-08まで。

| 記事 | 公開ページ | 表示回数 | 平均順位 | Click | 現在の扱い |
|---|---|---:|---:|---:|---|
| B008 | `/vehicle/car-flood-submersion.html` | 88 | 5.22 | 0 | 調査完了・本文変更は保留 |
| B019 | `/insurance/disaster-insurance-overview.html` | 38 | 6.97 | 0 | 調査完了・本文変更は保留 |
| B010 | `/vehicle/underground-parking-heavy-rain.html` | 24 | 7.88 | 0 | 次の調査対象 |
| B022 | `/home/apartment-typhoon-flood.html` | 10 | 5.40 | 0 | B010後に調査 |

※GSC APIの確定データは約3日遅延するため、ユーザー提供CSV等と時点差が生じる。

## 調査ファイル

- `docs/research/COMPETITOR_RESEARCH_CHECKLIST.md`
- `docs/research/COMPETITOR_SEARCH_QUERIES.md`
- `docs/research/COMPETITOR_RESEARCH_PROGRESS.md`
- `docs/research/competitor/B008_COMPETITOR_RESEARCH.md`
- `docs/research/competitor/B019_COMPETITOR_RESEARCH.md`

今後追加:

- `docs/research/competitor/B010_COMPETITOR_RESEARCH.md`
- `docs/research/competitor/B022_COMPETITOR_RESEARCH.md`

## 優先1: B008 車の冠水・水没

- 状態: `DONE`
- GSC確認: 完了
- CORE / INTENT / NICHE: 完了
- 上位 vs 自サイト: 完了
- 上位 vs ニッチ: 完了
- ニッチ vs 自サイト: 完了
- カニバリ: B009 / B011との役割分担整理済み
- A/B/C/D/E: 完了
- 修正候補: 完了

### 結論

安全情報は十分強い。改善余地は、水没後のロードサービス、点検・見積、修理/廃車判断等の実務フロー。title / descriptionはGSC蓄積待ち。

詳細: `docs/research/competitor/B008_COMPETITOR_RESEARCH.md`

## 優先2: B019 水害・台風・地震と保険

- 状態: `DONE`
- GSC確認: 完了
- CORE / INTENT / NICHE: 完了
- 上位 vs 自サイト: 完了
- 上位 vs ニッチ: 完了
- ニッチ vs 自サイト: 完了
- カニバリ: B011 / B013 / B014 / B016 / B017 / B018 / B051 / B052を確認済み
- A/B/C/D/E: 完了
- 修正候補: 完了

### GSCで注目する実測語

- `自動車保険 車両保険 水害 免責 日本`: position 4 / 1 impression
- `自動車保険 車両保険 水災 水没 免責 日本`: position 9 / 1 impression

### 結論

B019は `原因→被害物→契約→補償→条件` の5段階判断が独自の強み。大幅修正は不要。

改善候補は以下。

- 被災後の保険確認5ステップを短く追加
- 契約更新時にハザードマップを使う判断フロー
- 修理業者/保険金請求代行トラブルへの注意

現行の `B019=総合入口 / B013等=詳細` の役割分担は妥当。車両保険系クエリがB019に出ているためB011とのGSC重複を今後観察する。

title / descriptionと本文修正は現時点では保留。

詳細: `docs/research/competitor/B019_COMPETITOR_RESEARCH.md`

## 優先3: B010 地下駐車場×大雨

- source: `content/articles/B010_underground_parking_heavy_rain.md`
- 状態: `QUERY_READY`
- Search Console: 24 impressions / average position 7.88 / click 0
- 検索語セット: 完了
- 上位SERP: 未着手
- ニッチサイト探索: 未着手
- カニバリ: B008 / B009 / B011を重点確認予定
- A/B/C/D/E: 未着手
- 修正候補: 未着手

**次の作業:** B010のCORE→INTENT→NICHE→カニバリを調査する。

## 優先4: B022 マンション×台風・水害

- source: `content/articles/B022_apartment_typhoon_flood.md`
- 状態: `QUERY_READY`
- Search Console: 10 impressions / average position 5.40 / click 0
- 検索語セット: 完了
- 上位SERP: 未着手
- ニッチサイト探索: 未着手
- カニバリ: B012 / B020 / B021 / B046を重点確認予定
- A/B/C/D/E: 未着手
- 修正候補: 未着手

## 調査1記事あたりの完了条件

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

### 2026-09-11

- 最新GSC確定データ（〜9/8）を確認。
- B019のCORE / INTENT / NICHE検索を実施。
- B019とB011/B013/B014/B016/B017/B018/B051/B052の役割分担を確認。
- B019の3方向比較、A/B/C/D/E判定、修正候補整理を完了。
- B019を `DONE` に更新。本文変更は保留。

### 2026-09-10

- 競合・ニッチサイト比較の調査運用を開始。
- 初期優先4記事を設定。
- 3方向比較チェックリストを作成。
- GSC連動型の検索ワード一覧を作成。
- B008「車の冠水・水没」の競合・ニッチサイト比較を完了。
