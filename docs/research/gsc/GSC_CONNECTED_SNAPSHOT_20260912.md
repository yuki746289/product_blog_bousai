# 接続GSCスナップショット 2026-09-12

取得日: 2026-09-12
データ種別: SMEPost接続GSCの確定データ
対象プロパティ: `https://bousaikun.ashigaru.jp/`
対象期間: 2026-08-13〜2026-09-09
比較期間: 2026-07-16〜2026-08-12

## 1. サイト全体

- Clicks: 1
- Impressions: 288
- CTR: 0.347%
- Average position: 22.32
- 比較期間は実質データなし

Search Console UIの9/11までのエクスポートとは対象期間が異なるため、数値を単純比較しない。

## 2. 上位露出ページ

| ページ | Clicks | Impressions | CTR | Avg position | 判断 |
|---|---:|---:|---:|---:|---|
| B008 `vehicle/car-flood-submersion.html` | 0 | 103 | 0% | 5.21 | GSC_HOLD / MONITOR |
| B019 `insurance/disaster-insurance-overview.html` | 0 | 50 | 0% | 6.74 | GSC_HOLD / MONITOR |
| B010 `vehicle/underground-parking-heavy-rain.html` | 0 | 27 | 0% | 7.52 | GSC_HOLD / MONITOR |
| B022 `home/apartment-typhoon-flood.html` | 0 | 15 | 0% | 5.53 | GSC_HOLD / MONITOR |
| B015 `post-disaster/after-flood-record-evidence.html` | 0 | 8 | 0% | 6.13 | GSC_HOLD / MONITOR |
| `qa.html` | 0 | 4 | 0% | 6.25 | WATCH |
| B034 `guide/baby-disaster-stockpile.html` | 0 | 1 | 0% | 10.0 | WATCH |

## 3. 初クリック

検索クエリ: `水害対策`

- Query total: 4 impressions / 1 click / CTR 25% / avg position 67
- 主クリック先: `/flood/flood-preparedness-basics.html`
- ページ total: 16 impressions / 1 click / CTR 6.25% / avg position 70.56

母数が極小なのでCTR改善成功とは断定しない。
ただし、実検索流入が発生した事実として記録する。

## 4. 重要クエリ

### 車両保険系

- `自動車保険 車両保険 水害 免責 日本` → B019 / 1 impression / position 4
- `自動車保険 車両保険 水災 水没 免責 日本` → B019 / 2 impressions / position 9

B019が総合保険ピラーでありながら車両保険系にも露出している。
B011との役割分担を監視するが、現時点ではB019へ車両保険詳細を増やさない。

### 冠水道路系

B009:
- `冠水 した 道路を 車で 走る` → position 85
- `冠水 道路 車` → position 81
- `冠水した道路を車で走る` → position 86

B008/B009の役割分担は確認できる。

### 台風・水害一般

- `台風 備え` → B006系 / position 95.5
- `台風 防災` → position 97
- `大雨 対策 できること` → flood basics / position 86
- `大雨 浸水 対策` → home flood preparedness / position 100
- `水害 対策` → flood hub / position 42

一般語ではまだ順位が低く、CTR改善より検索意図・記事役割・内部リンクが優先。

## 5. カニバリ候補

### `水害対策`

- flood basics → 3 impressions / position 77.33 / 1 click
- flood hub → 1 impression / position 72
- home flood preparedness → 1 impression / position 53

### `水害の備え`

- flood basics → position 93
- flood hub → position 83
- home flood preparedness → position 66

### `水害対策 個人でできること`

- flood basics → position 92〜93
- home flood preparedness → position 69〜70

各ページ1〜3 impressions程度のため、現時点では統合・title変更を行わずMONITOR。

## 6. 低CTR候補の扱い

接続GSCでは低CTR候補として以下が出る。

- B008: 103 impressions / avg 5.21 / CTR 0%
- B019: 50 impressions / avg 6.74 / CTR 0%

ただし母数はまだ小さい。上位露出が増加している段階なので、0%だけでtitle/H1を変更しない。

優先順位:
1. 実SERP表示の確認
2. 検索意図との差分確認
3. 局所的な本文補強候補を洗い出す
4. 十分なGSC母数がたまってからtitle/metaを再判断

## 7. 実装方針への影響

### 保護優先
- B008
- B019
- B010
- B022
- B015

### 低順位ページ
40〜100位台のページはCTRより以下を優先する。
- 検索意図
- 記事役割
- 内部リンク
- インデックス状態
- 上位競合との情報差

### 既存の実装候補
GSC上位露出ページを大きく触らず、B045/B039/B047/B003/B042/B044等の局所改善を優先する方針を維持する。
