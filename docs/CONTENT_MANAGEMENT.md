# 記事状態・公開管理仕様

## 1. 目的

GitHub上で、記事の制作状態・レビュー状態・公開可否・鮮度を一元管理する。

## 2. 状態

| 状態 | 意味 | 公開可否 |
|---|---|---|
| `PLANNED` | 記事候補 | 不可 |
| `RESEARCHING` | 一次情報・公的情報を調査中 | 不可 |
| `DRAFTED` | 下書き作成済み | 不可 |
| `REVIEW_REQUIRED` | 目視確認が必要 | 不可 |
| `READY_TO_PUBLISH` | 公開条件をすべて満たした | 可 |
| `PUBLISHED` | 本番公開済み | 公開中 |
| `REVIEW_DUE` | 再確認期限到来 | 要確認 |
| `SUSPENDED` | 安全性・事実性等の理由で公開停止 | 不可 |
| `ARCHIVED` | 廃止済み | 不可 |

## 3. 公開ゲート

記事を `READY_TO_PUBLISH` にするには、少なくとも以下を満たす。

- 必須出典が確認済み
- 主要な事実に確認日がある
- `publish_blockers` が空
- 必要な目視レビューが完了
- 高リスク記事では公的・一次情報が確認済み
- アフィリエイト記事では広告表示が確認済み
- 価格・在庫等の変動情報を不適切に固定表示していない
- 画像の出典・権利・対象一致が確認済み
- 内部リンク・外部リンクが有効
- HTML/構造チェックに合格

## 4. 目視レビュー

`manual_review_required=true` の記事は、`manual_review_status=APPROVED` になるまで公開不可。

原則として以下は目視確認対象とする。

- 避難行動、安全判断、応急対応
- 火気、発電機、電源、燃料等の事故リスクを伴う説明
- 備蓄量等の数量を強く断定する内容
- 医療・薬・衛生上の判断を含む内容
- 商品を「安全」「絶対必要」等と強く推奨する内容

## 5. 正本

正式な記事状態は `data/content_registry.json` を正とする。
記事本文の変更と状態変更は同じPRで確認できる形を原則とする。

## 6. ルール・チェックリストの管理

ルール正本はprivateリポジトリ `yuki746289/product_blog_rules` で管理する。詳細と対応表は `docs/RULES_GOVERNANCE.md` を参照する。

public側の作業コピー・サイト固有記録:

- 共通記事作成ルール作業コピー: `docs/CONTENT_CREATION_RULES.md`
- 共通レビュー項目作業コピー: `docs/ARTICLE_REVIEW_CHECKLIST.md`
- 記事別レビュー記録: `docs/reviews/Bxxx_CHECKLIST.md`（このリポジトリで管理）
- 記事別テンプレート作業コピー: `docs/reviews/ARTICLE_CHECKLIST_TEMPLATE.md`

記事別レビュー記録には共通ルール本文をコピーせず、共通チェックIDの判定・根拠と記事固有事項だけを記録する。

複数記事で同じ追加確認が必要になった場合は、記事別ルールを増やすのではなく共通ルールへの昇格を検討する。

## 7. キーワード起点の新規記事作成

新規記事を追加する場合は、原則として以下の順で進める。

1. `docs/KEYWORD_RESEARCH_POLICY.md` で需要・検索意図を調査
2. 既存記事・Q&A・商品ページとの重複を確認
3. `docs/NEW_ARTICLE_WORKFLOW.md` で記事briefを作成
4. 出典・画像・商品情報を調査
5. Markdown / preview HTML / review / registryを同期
6. 共通チェックリストを実行
7. 本番ビルド・スモークテスト
8. 公開後はsitemap / Search Console / GA4で確認

繰り返し作業では `docs/research/NEW_ARTICLE_BRIEF_TEMPLATE.md` を使用する。

