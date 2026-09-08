# Amazon関連記事・商品導線 作業開始プレフライト

更新日: 2026-09-08
適用先: 防災くらしガイド

## 1. 目的

Amazon関連記事・商品導線の作業で、Amazon専用ルールの参照漏れを防ぐ。

**Amazonに関係する作業は、記事新規作成・既存記事修正を問わず、商品調査・ASIN確定・画像選定・価格確認・HTML実装より前に本プレフライトを実行する。**

過去の会話・記憶・以前読んだルールだけで代替しない。作業単位ごとに、その時点の正本を開いて確認する。

## 2. 適用条件

次のいずれかに該当したら必須とする。

- `content_role=product`
- `affiliate=true`
- Amazonリンクを新規追加・変更・削除する
- ASINを追加・変更・確認する
- Amazonまたはメーカーの商品画像を追加・変更する
- 商品名・型番・入数・容量・価格・仕様を変更する
- 商品の品切れ・販売終了・後継品・差し替えを扱う
- 情報記事から商品記事/Amazonへの導線を変更する
- 既存の商品記事をリライトする

「記事全体は情報記事だからAmazonルールは不要」と判断しない。本文の一部でも具体商品・Amazon導線を扱うなら適用する。

## 3. 作業開始時に必ず読む正本

以下を**この順で**確認する。

1. `docs/AMAZON_WORK_PREFLIGHT.md`（本ファイル）
2. `docs/AFFILIATE_POLICY.md`
3. `docs/AMAZON_PRODUCT_AVAILABILITY_POLICY.md`
4. `docs/CONTENT_CREATION_RULES.md` の商品導線・商品紹介関連（CR-05B / CR-06）
5. `docs/ARTICLE_REVIEW_CHECKLIST.md` の C06 商品導線・商品記事

private正本を直接参照できる作業環境では `yuki746289/product_blog_rules/sites/bousai/rules/` を優先する。public作業コピーと差分がある場合はprivate正本を正とし、同じ作業単位で同期する。

## 4. プレフライト確認項目

商品調査・実装前に次を確認する。

- [ ] Amazon作業に該当するか判定した
- [ ] `AFFILIATE_POLICY.md` の最新版を開いて読んだ
- [ ] `AMAZON_PRODUCT_AVAILABILITY_POLICY.md` の最新版を開いて読んだ
- [ ] 商品記事/商品導線の共通ルール（CR-05B / CR-06）を確認した
- [ ] 記事別チェックリストで C06 を適用対象にした
- [ ] アソシエイトタグの正本が `config/site.json` であることを確認した
- [ ] ASIN未確定時は検索リンク、ASIN確定時は商品詳細リンクという条件を確認した
- [ ] 商品画像の配信元・型番一致・再ホスト禁止・フォールバック条件を確認した
- [ ] Amazon現在価格を静的に固定表示しない条件を確認した
- [ ] 品切れ・販売終了時にASINだけを機械的に差し替えない条件を確認した

## 5. 作業停止条件

以下のいずれかが未確認なら、**商品選定・ASIN確定・商品画像実装・Amazon CTA実装・公開へ進まない。**

- `AFFILIATE_POLICY.md` 未参照
- `AMAZON_PRODUCT_AVAILABILITY_POLICY.md` 未参照
- ASINと商品名/型番の一致が未確認なのに直リンクしようとしている
- 商品画像の配信元または型番一致が未確認
- 価格の根拠・確認日が未確認
- 安全性に関わる商品のメーカー/公的根拠が未確認

ASINや画像が確定できない場合は、専用ルールで認められたフォールバックへ戻す。推測で埋めない。

## 6. 記事別レビューへの証跡

Amazon関連作業では、記事別チェックリストまたは作業レビューに最低限次を残す。

```text
amazon_preflight: PASS
amazon_preflight_checked_at: YYYY-MM-DD
amazon_policy_refs:
  - docs/AMAZON_WORK_PREFLIGHT.md
  - docs/AFFILIATE_POLICY.md
  - docs/AMAZON_PRODUCT_AVAILABILITY_POLICY.md
amazon_scope: new_article / product_update / asin_update / image_update / price_update / replacement / internal_link
```

複数該当する場合、`amazon_scope` は複数記録してよい。

## 7. 最終確認

公開前に次を確認する。

- 商品名・型番・ASIN・画像・本文説明が同一商品を指している
- 画像クリック先とAmazon CTAのリンク先が意図どおり
- アソシエイトタグが正しい
- 検索リンクを使う場合、検索結果であることが文言で分かる
- 商品詳細リンクを使う場合、ASIN一致を確認済み
- 商品画像の404/403・表示崩れを確認した
- 画像失敗時のフォールバックがある
- 参考価格の出典・確認日がある
- Amazon現在価格・在庫はリンク先確認としている
- 高リスク記事では安全情報が商品導線より優先されている

## 8. 運用原則

- Amazon関連作業を始めるたびに、本プレフライトから開始する。
- 「前回確認したから今回は省略」は不可。
- ルールを改善した場合はprivate正本を先に、または同一作業単位で更新する。
- public作業コピーだけを更新して正本を放置しない。
- Amazon関連の不具合や見落としが発生した場合、個別修正だけで終わらせず、本プレフライト・専用ポリシー・チェックリストのどこで検知すべきだったかを見直す。
