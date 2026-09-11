# 防災くらしガイド 競合・ニッチサイト比較 進捗管理

更新日: 2026-09-11

作業ブランチ: `research/competitor-seo-20260910`

## 運用方針

- 本ファイルを競合・キーワード調査の進捗正本とする。
- GSC更新時は実測クエリを優先する。
- 調査中は記事本文を変更しない。
- 記事修正は別の実装ブランチで行う。
- GitHub Actions節約のため、この調査ブランチでは原則PR作成・mainマージ・Actions手動実行を行わない。
- 検索ボリューム未確認の語は「需要が大きい」と断定せず、GSC・競合・検索意図・一次情報・カニバリで暫定評価する。

## 初期4記事 競合調査

| 優先 | 記事 | 状態 | 主判断 |
|---:|---|---|---|
| 1 | B008 車の冠水・水没 | `DONE` | 安全情報は強い。水没後実務が改善候補 |
| 2 | B019 水害・台風・地震と保険 | `DONE` | 5段階判断が強み。詳細記事との分業維持 |
| 3 | B010 地下駐車場×大雨 | `DONE` | ニッチ性良好。2026年一次情報更新候補 |
| 4 | B022 マンション×台風・水害 | `DONE` | 階層差+共用設備+生活継続が強み |

## 最新GSCスナップショット

2026-09-11取得。確定データは2026-09-08まで。

| 記事 | 表示回数 | 平均順位 | Click | 扱い |
|---|---:|---:|---:|---|
| B008 | 88 | 5.22 | 0 | 本文変更保留 |
| B019 | 38 | 6.97 | 0 | 本文変更保留 |
| B010 | 24 | 7.88 | 0 | 最新一次情報更新候補 |
| B022 | 10 | 5.40 | 0 | 本文変更保留 |

## 完了済み競合調査

- `docs/research/competitor/B008_COMPETITOR_RESEARCH.md`
- `docs/research/competitor/B019_COMPETITOR_RESEARCH.md`
- `docs/research/competitor/B010_COMPETITOR_RESEARCH.md`
- `docs/research/competitor/B022_COMPETITOR_RESEARCH.md`

## 第2フェーズ: サイト全体キーワード探索

状態: `P1_DETAIL_RESEARCH_COMPLETE`

正本:
- `docs/research/SITEWIDE_KEYWORD_OPPORTUNITIES.md`
- `docs/research/KEYWORD_RESEARCH_PRIORITIES_20260911.md`

### クラスター進捗

| クラスター | 判定 | 状態 | 詳細ファイル |
|---|---|---|---|
| 災害×常用薬 | `NEW / P1` | `RESEARCH_DONE` | `keywords/NEW_DISASTER_MEDICATION_KEYWORD_RESEARCH.md` |
| 停電×冷蔵庫・食品 | `EXPAND B045 / P1` | `RESEARCH_DONE` | `keywords/B045_BLACKOUT_REFRIGERATOR_KEYWORD_RESEARCH.md` |
| 妊産婦×災害 | `NEW / P2` | `RESEARCH_DONE` | `keywords/NEW_PREGNANCY_DISASTER_KEYWORD_RESEARCH.md` |
| 高齢者×避難 / 福祉避難所 | `EXPAND B035 + QA / P2` | `RESEARCH_DONE` | `keywords/B035_SENIOR_WELFARE_SHELTER_KEYWORD_RESEARCH.md` |
| ペット×同行避難 | `B033 + QA / P2` | `RESEARCH_DONE` | `keywords/B033_PET_EVACUATION_QA_KEYWORD_RESEARCH.md` |
| 断水×トイレ | `B003 + QA / P1` | `RESEARCH_DONE` | `keywords/B003_WATER_OUTAGE_TOILET_KEYWORD_RESEARCH.md` |
| 停電×熱中症 | `EXPAND B047 / P1` | `RESEARCH_DONE` | `keywords/B047_BLACKOUT_HEATSTROKE_KEYWORD_RESEARCH.md` |
| 在宅避難×備蓄日数 | `EXPAND B039 / P1` | `RESEARCH_DONE` | `keywords/B039_HOME_EVACUATION_STOCKPILE_KEYWORD_RESEARCH.md` |
| 水害×避難タイミング | `LIGHT_EXPAND B042 / P1` | `RESEARCH_DONE` | `keywords/B042_FLOOD_EVACUATION_TIMING_KEYWORD_RESEARCH.md` |
| 災害×車中泊 | `LIGHT_EXPAND B044 / P1` | `RESEARCH_DONE` | `keywords/B044_VEHICLE_EVACUATION_SUPPORT_KEYWORD_RESEARCH.md` |
| 停電×マンション | `LIGHT_EXPAND B022 / P1 / GSC_HOLD` | `RESEARCH_DONE` | `keywords/B022_APARTMENT_BLACKOUT_WATER_KEYWORD_RESEARCH.md` |

## 主な新規記事候補

### 1. 災害×常用薬 `NEW / P1`

仮タイトル:
`災害時の常用薬は何日分備える？お薬手帳・薬が切れたときの相談先`

専用記事がなく、検索意図と安全上の実用価値が明確。現時点の最有力NEW候補。

### 2. 妊産婦×災害 `NEW / P2`

仮タイトル:
`妊婦・妊産婦の防災｜避難時の持ち物・母子健康手帳・健診をどう備える？`

B034乳幼児備蓄とは主語・検索意図を分離できる。検索ボリューム確定前のためP2。

### WATCH

- 水害マイ・タイムラインの作り方 / P2
- 福祉避難所の総合記事 / P2
- 犬/猫別の避難所記事 / P3

## 主な既存記事拡張候補

| 暫定順位 | 記事 | 主な追加候補 | 備考 |
|---:|---|---|---|
| 1 | B045 | 2026-09-08農水省の停電後食品安全情報 | 鮮度優先 |
| 2 | B039 | 最低3日/推奨1週間＋水/食料/トイレ記事への導線 | 在宅避難ピラー強化 |
| 3 | B047 | クーリングシェルター | 2026の公的運用と相性良い |
| 4 | B003 | バケツで流せる条件をQ&A化 | 本文大改稿不要 |
| 5 | B042 | マイ・タイムライン導線 | 本文は既に強い |
| 6 | B044 | 2026在宅・車中泊避難者支援＋受付方法は自治体差 | 本文は既に強い |
| 7 | B022 | 非常用水栓・給水方式・非常電源の確認項目 | GSC平均5位台につき変更保留 |
| 8 | B035 | 高齢者等避難＋福祉避難所Q&A | P2 |
| 9 | B033 | 同行/同伴避難Q&A | 本文は既に強い |

## Q&A候補

### P1相当

- 断水時、トイレはバケツの水で流してもいいですか？
- 地震の後、水が出るならトイレを流していいですか？
- 断水が復旧したら、すぐトイレを使っていいですか？
- 在宅避難の備蓄は何日分必要ですか？
- 在宅避難でも支援物資は受け取れますか？
- 停電でエアコンが使えないとき、いつ避難した方がいいですか？
- 停電時にクーリングシェルターは使えますか？
- 避難指示が出る前に避難してもいいですか？
- 大雨のとき車で避難してもいいですか？
- 夜に大雨になる予報なら、明るいうちに避難した方がいいですか？
- 車中泊避難でも支援物資は受け取れますか？
- 車中泊避難をするとき、避難所への登録は必要ですか？
- マンションは停電すると水も出なくなりますか？
- マンションの非常用水栓とは何ですか？
- マンションに非常用発電機があれば、エレベーターや水道は使えますか？

### P2相当

- 福祉避難所は誰が入れますか？
- 福祉避難所へ直接避難できますか？
- 高齢者なら全員、福祉避難所を利用できますか？
- ペットの同行避難と同伴避難は何が違いますか？
- 同行避難できる避難所なら、ペットと同じ部屋で過ごせますか？
- ペットを受け入れてくれる避難所はどう探せばいいですか？

## 優先順位ファイル

`docs/research/KEYWORD_RESEARCH_PRIORITIES_20260911.md`

現時点の推奨実装順（まだ実装しない）:

1. B045 最新一次情報更新
2. B039 在宅避難の3日/1週間＋内部リンク
3. B047 クーリングシェルター
4. B003関連Q&A
5. 災害×常用薬 新規記事
6. B042 マイ・タイムライン導線
7. B044 車中泊支援情報
8. 福祉避難所Q&A
9. ペット同行避難Q&A
10. 妊産婦×災害 新規記事
11. B022 非常用水栓等（GSC観察後）

この順番は検索ボリューム確定前の暫定順位。GSC・ラッコキーワード等で更新する。

## 次の調査

P1既存クラスターの詳細調査は一巡した。

次は以下のどちらかを行う。

### A. 新規クラスター探索

- 災害×在宅医療/医療機器
- 災害×アレルギー食
- 災害×女性の衛生/生理
- 災害×認知症
- 避難所×防犯/女性・子ども
- 長期断水×入浴・洗濯

### B. データ追加後の再評価

- 最新GSC実測クエリ
- ラッコキーワード等の検索需要データ
- 上位SERP変化

## 変更履歴

### 2026-09-11

- 初期4記事の競合調査完了。
- 災害×常用薬、停電×冷蔵庫、妊産婦×災害の詳細調査完了。
- 高齢者×避難/福祉避難所の詳細調査完了。
- ペット×同行避難の詳細調査完了。
- 断水×トイレの詳細調査完了。
- 停電×熱中症の詳細調査完了。
- 在宅避難×備蓄日数の詳細調査完了。
- 水害×避難タイミングの詳細調査完了。
- B044 災害×車中泊の詳細調査完了。
- B022 停電×マンションの詳細調査完了。
- P1既存クラスターの詳細調査を一巡。
- `KEYWORD_RESEARCH_PRIORITIES_20260911.md` を作成し、NEW/EXPAND/QA/WATCHの暫定順位を整理。
- すべて記事本文・公開Q&Aは未変更。
