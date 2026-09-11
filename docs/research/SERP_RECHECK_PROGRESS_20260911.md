# SERP再調査 進捗管理

更新日: 2026-09-12
作業ブランチ: `research/competitor-seo-20260910`

新しいSERP表示品質ルールを、既存のDONE/RESEARCH_DONE対象へ再適用した。
記事本文は調査中に変更していない。

## 最新GSC確定データ

取得日: 2026-09-12
確定期間: 2026-08-12〜2026-09-08（Search Consoleは約3日遅延）

- サイト全体: 237 impressions / 0 clicks / CTR 0%
- B008 車の冠水・水没: 88 impressions / 平均5.22位 / 0 click
- B019 水害・台風・地震と保険: 38 impressions / 平均6.97位 / 0 click
- B010 地下駐車場×大雨: 24 impressions / 平均7.88位 / 0 click
- B022 マンション×台風・水害: 10 impressions / 平均5.4位 / 0 click
- B015 水害後の記録・証拠: 3 impressions / 平均6.67位 / 0 click
- QAページ: 3 impressions / 平均7.67位 / 0 click

GSC上の重要な実測クエリ:
- `自動車保険 車両保険 水害 免責 日本` → B019 / 平均4位
- `自動車保険 車両保険 水災 水没 免責 日本` → B019 / 平均9位

カニバリ候補:
- `水害の備え`
- `水害対策`
- `水害対策 個人でできること`

これらは B005 / floodカテゴリ / B012 が重複露出しており、現時点では表示回数が各1程度のため、即統合せずMONITORとする。

### GSCを踏まえた運用判断

1. B008 / B019 / B010 / B022 は5〜8位付近まで来ているため、title/H1/大構成の変更は保留。
2. 上記4記事は、SERP表示・スニペット・不足情報の局所補強を優先する。
3. 0 clickだが母数が小さいため、CTR 0%だけを理由にタイトル変更しない。
4. B019に出ている車両保険系クエリはB011との役割分担を継続確認する。
5. 50位以下のページは、CTR改善ではなく検索意図・記事役割・内部リンク・インデックス評価を優先する。

## 初期4記事

| 順位 | 対象 | 再調査状態 | SERP品質 | 主判断 |
|---:|---|---|---|---|
| 1 | B008 車の冠水・水没 | DONE | MONITOR | 88表示・平均5.22位。安全情報は強い。水没後のレッカー→点検→見積→修理/廃車を局所補強候補。title変更保留 |
| 2 | B019 水害・台風・地震と保険 | DONE | MONITOR | 38表示・平均6.97位。車両保険系で4位/9位の実測あり。5段階判断は維持し、B011とのカニバリを監視 |
| 3 | B010 地下駐車場×大雨 | DONE | PASS寄りMONITOR | 24表示・平均7.88位。title/metaは良好。最新一次情報の局所更新価値あり。source/preview差分あり |
| 4 | B022 マンション×台風・水害 | DONE | PASS寄りMONITOR | 10表示・平均5.4位。非常用水栓等は局所追加候補。GSC HOLD |

## サイト全体クラスター再調査

| 順位 | 対象 | 再調査状態 | 判定 | 主判断 |
|---:|---|---|---|---|
| 1 | B045 停電×冷蔵庫・食品 | DONE | UPDATE_HIGH / P1 | SERP設計は良好。2026-09-08農水省更新を本文へ反映する価値が高い |
| 2 | 災害×常用薬 | DONE | NEW / P1 | 独立記事候補を維持。ただし「3〜7日分」を全常用薬へ一般化しない |
| 3 | B003 断水×トイレ | DONE | EXISTING + QA / P1 | 本文は強い。通常断水と地震・豪雨時の排水損傷リスクを分け、バケツ洗浄等はQ&A向き |
| 4 | B047 停電×熱中症 | DONE | LIGHT_EXPAND / P1 | 骨格は強い。クーリングシェルターと自治体の開放状況確認を軽微追加候補 |
| 5 | B039 在宅避難×備蓄日数 | DONE | EXPAND / P1 | 最低3日・可能なら1週間程度の公的目安を短く明示し、B025/B026/B003へ内部リンク |
| 6 | B042 水害×避難タイミング | DONE | LIGHT_EXPAND / P1 | 2026新体系対応は強い。マイ・タイムラインへの出口を追加候補 |
| 7 | B044 災害×車中泊 | DONE | LIGHT_EXPAND / P1 | 安全面は強い。2026年の在宅・車中泊避難者支援手引きと自治体受付実務を補強候補 |
| 8 | B022 停電×マンション | DONE | LIGHT_EXPAND / P1 / GSC_HOLD | 非常用水栓・給水方式・非常電源の確認項目を候補化。平均5位台のため大変更保留 |
| 9 | B035 高齢者×避難 / 福祉避難所 | DONE | EXPAND + QA / P2 | 警戒レベル3「高齢者等避難」を軽微補強。福祉避難所の対象・直接避難可否はQ&A向き |
| 10 | B033 ペット×同行避難 | DONE | EXISTING + QA / P2 | 総合記事は十分。同行避難と同室可否、避難所の探し方をQ&A化候補。環境省2026資料は改訂案扱い |
| 11 | 妊産婦×災害 | DONE | NEW / P2 | B034と分離した独立記事候補。妊婦健診継続・母子手帳・分娩施設・避難所配慮に独立需要あり |

## 再調査ファイル

初期4記事:
- `docs/research/competitor/B008_SERP_RECHECK_20260911.md`
- `docs/research/competitor/B019_SERP_RECHECK_20260911.md`
- `docs/research/competitor/B010_SERP_RECHECK_20260911.md`
- `docs/research/competitor/B022_SERP_RECHECK_20260911.md`

サイト全体クラスター:
- `docs/research/serp/B045_SERP_RECHECK_20260911.md`
- `docs/research/serp/NEW_DISASTER_MEDICATION_SERP_RECHECK_20260911.md`
- `docs/research/serp/B003_SERP_RECHECK_20260911.md`
- `docs/research/serp/B047_SERP_RECHECK_20260911.md`
- `docs/research/serp/B039_SERP_RECHECK_20260911.md`
- `docs/research/serp/B042_SERP_RECHECK_20260911.md`
- `docs/research/serp/B044_SERP_RECHECK_20260911.md`
- B022停電×マンションはB022本体再調査と既存キーワード調査へ統合
- `docs/research/serp/B035_SERP_RECHECK_20260911.md`
- B033ペット×同行避難は既存キーワード調査へ統合
- `docs/research/serp/NEW_MATERNAL_DISASTER_SERP_RECHECK_20260911.md`

## 今回の共通確認項目

- GSC実測
- 実SERPタイトル/スニペット（取得できる範囲）
- title/meta/H1と検索意図
- 上位大手/公的ページ
- ニッチページ
- 自サイトとの差
- カニバリ
- A/B/C/D/E
- SERP表示品質
- 実装する/保留する判断

## GSC反映後の実装優先度

### まず実施候補
1. B045 一次情報の鮮度更新
2. B039 備蓄日数の明示と内部リンク
3. B047 クーリングシェルター追記
4. B003 条件分岐型Q&A
5. B042 マイ・タイムライン導線
6. B044 支援受付の補強

### 新規記事設計
7. 災害×常用薬
8. 妊産婦×災害

### Q&A中心
9. B035 福祉避難所Q&A
10. B033 同行避難Q&A

### GSC観察優先
- B008
- B019
- B010
- B022

特にB008/B019/B010/B022は現在5〜8位付近なので、大変更せず、次のGSC更新で表示回数・CTR・クエリの増加を確認してからタイトルや大見出し変更を判断する。
