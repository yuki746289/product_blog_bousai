# ローカルプレビュー手順

## 前提

- Git for Windows がインストールされている
- Apache の DocumentRoot が `C:\server\Apache24\htdocs`
- 本リポジトリをローカルへclone済み
- Apacheが起動している

## 初回clone

Git Bash等で実行する。

```bash
git clone https://github.com/yuki746289/product_blog_bousai.git
cd product_blog_bousai
```

private repositoryのため、GitHub認証が必要。

## 2回目以降

リポジトリ直下の `deploy_local.bat` を実行する。

処理内容:

1. `main` へ切り替え
2. `git pull --ff-only origin main`
3. `preview/` を `C:\server\Apache24\htdocs\bousai_preview\` へ同期
4. `http://localhost/bousai_preview/index.html` を既定ブラウザで開く

## 確認URL

- トップ: `http://localhost/bousai_preview/index.html`
- 記事サンプル: `http://localhost/bousai_preview/article_sample.html`

## 注意

`/MIR` で同期するのは専用ディレクトリ `bousai_preview` のみ。
Apacheのhtdocs直下や他サイトのファイルは削除しない。

`preview/` はレイアウト確認用であり、本番FTP公開対象ではない。
