# SERP再調査 進捗管理

更新日: 2026-09-11
作業ブランチ: `research/competitor-seo-20260910`

新しいSERP表示品質ルールを、既存のDONE/RESEARCH_DONE対象へ再適用する。
記事本文は調査中に変更しない。

## 初期4記事

| 順位 | 対象 | 再調査状態 | SERP品質 | 主判断 |
|---:|---|---|---|---|
| 1 | B008 車の冠水・水没 | DONE | MONITOR | 安全情報は強い。水没後のレッカー→点検→見積→修理/廃車が局所補強候補。title変更保留 |
| 2 | B019 水害・台風・地震と保険 | DONE | MONITOR | 5段階判断は強い。旧不足候補の多くは現行本文に実装済み。詳細記事との分業維持 |
| 3 | B010 地下駐車場×大雨 | DONE | PASS寄りMONITOR | title/metaは良好。最新一次情報の局所更新価値あり。source/preview差分あり |
| 4 | B022 マンション×台風・水害 | DONE | PASS寄りMONITOR | 階層差・共用設備・生活継続が強み。非常用給水栓等は局所追加候補、GSC HOLD |

## 再調査ファイル

- `docs/research/competitor/B008_SERP_RECHECK_20260911.md`
- `docs/research/competitor/B019_SERP_RECHECK_20260911.md`
- `docs/research/competitor/B010_SERP_RECHECK_20260911.md`
- `docs/research/competitor/B022_SERP_RECHECK_20260911.md`

## 次の順序

既存のサイト全体キーワード調査対象を以下の順に再検証する。

1. B045 停電×冷蔵庫・食品
2. 災害×常用薬（新規記事候補）
3. B003 断水×トイレ
4. B047 停電×熱中症
5. B039 在宅避難×備蓄日数
6. B042 水害×避難タイミング
7. B044 災害×車中泊
8. B022 停電×マンション（B022本体再調査結果と統合）
9. B035 高齢者×避難 / 福祉避難所
10. B033 ペット×同行避難
11. 妊産婦×災害（新規記事候補）

各対象で以下を確認する。

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
