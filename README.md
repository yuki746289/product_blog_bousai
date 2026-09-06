# product_blog_bousai

防災をテーマにしたブログの制作・品質管理・公開管理リポジトリです。

## 基本方針

- 公開できる記事から順次公開する。
- 防災情報は、公的機関・一次情報を優先して確認する。
- 安全判断に影響する記事は、AI生成だけで公開しない。
- 記事ごとに状態・リスク・最終確認日・次回確認日を管理する。
- 目視確認が必要な記事は `REVIEW_REQUIRED` とし、承認後に公開する。
- Amazonアフィリエイト記事は、広告であることを明示し、商品紹介と安全情報を混同しない。
- FTP認証情報などの秘密情報はGitHubへ保存しない。

## 記事状態

`PLANNED` → `RESEARCHING` → `DRAFTED` → `REVIEW_REQUIRED` / `READY_TO_PUBLISH` → `PUBLISHED`

公開後は必要に応じて `REVIEW_DUE` / `SUSPENDED` / `ARCHIVED` へ遷移します。

## 鮮度確認

```bash
python -m unittest discover -s tests -v
python -m bousai_blog.freshness data/content_registry.json
```

定期バッチは `.github/workflows/content-freshness.yml` で実行します。

## 主要ドキュメント

- `docs/BOUSAI_SITE_SPEC.md`: 防災ブログ固有仕様
- `docs/CONTENT_MANAGEMENT.md`: 記事状態・公開ゲート
- `docs/FRESHNESS_POLICY.md`: 情報鮮度・再確認方針
- `docs/AFFILIATE_POLICY.md`: Amazonアフィリエイト運用
- `docs/DEPLOYMENT.md`: FTP公開方針
- `docs/INITIAL_CONTENT_PLAN.md`: 初期記事候補

## 公開

公開対象は原則として `READY_TO_PUBLISH` から生成・確認した静的ファイルのみとします。
FTPユーザー名・パスワードはGitHub Secretsまたはローカル環境変数で管理し、平文でコミットしません。

## サイト構成

- `docs/SITE_STRUCTURE.md`: トップページ・カテゴリ・記事ページ構成
- `docs/PICKUP_AND_DEEP_DIVE_POLICY.md`: ピックアップ記事・深掘り記事の運用
- `config/navigation.json`: グローバルナビ・トップページセクション
- `data/homepage_features.json`: ピックアップ候補と有効枠


## ルールの正本

開発・記事制作・レビューに関するルール正本は、privateリポジトリ `yuki746289/product_blog_rules` で管理します。
このリポジトリの `docs/` にあるルール文書は、実装・レビュー・テスト用の一時作業コピーです。
運用詳細は `docs/RULES_GOVERNANCE.md` を参照してください。
