# 公開・FTP運用

## 1. 基本

本番公開先はFTPサーバを使用する。
FTPホストは公開設定として管理できるが、ユーザー名・パスワードをソースコードへ直書きしない。

## 2. 認証情報

GitHub Actionsを使用する場合は以下のSecretsを使用する想定。

- `FTP_HOST`
- `FTP_USERNAME`
- `FTP_PASSWORD`

ローカル公開の場合も環境変数から読み込む。

## 3. 公開対象

`public/` 以下のみを公開対象とする。
仕様書、記事台帳、テスト、ソースコード、秘密情報はアップロードしない。

## 4. 公開条件

- 記事状態が `READY_TO_PUBLISH`
- 必須テスト成功
- 目視レビュー対象は承認済み
- 公開前チェックでブロッカーなし

公開後に `PUBLISHED` へ更新し、公開URLと公開日時を台帳へ記録する。


## 5. Analytics公開チェック

すべての公開HTMLについて以下を確認する。

- Google Analyticsタグが `<head>` 内に存在する
- Measurement IDが `G-XQVLD5HMNG` である
- 同じGoogle Analyticsタグが重複していない

Analyticsタグ欠落は公開前テストのエラーとして扱う。

## 6. 本番ファイル生成

本番HTMLは `preview/` を直接FTP送信せず、次のコマンドで `public/` を生成する。

```bash
python scripts/build_public.py
```

生成時に以下を行う。

- `data/content_registry.json` の `planned_public_path` に従って記事をカテゴリ配下へ配置
- preview用 `noindex` を削除
- 制作管理ラベル（記事ID・要目視確認等）を公開HTMLから削除
- Google Analytics `G-XQVLD5HMNG` を各HTMLへ1回だけ挿入
- previewの内部リンクを本番URL構造へ相対変換
- `bousai_common.css` / `bousai_common.js` / ローカル画像をコピー
- 受付停止中の `contact.html` は本番生成対象から除外
- 生成後に内部リンク・GA・noindex等を検証

## 7. GitHub Actions FTP公開

`.github/workflows/deploy-production.yml` で次を実施する。

1. テスト
2. `public/` 生成
3. FTPS Explicit（port 21）でFTP接続直下へ同期

必要なGitHub Secrets:

- `FTP_USERNAME`
- `FTP_PASSWORD`

FTPホストは `config/site.json` の `ftp.homepage.shinobi.jp` を使用する。

忍者ホームページでは転送先フォルダは空欄（FTP接続直下）とする。

## 8. 公開URL

公開URLは忍者ホームページ側の「サイトURL（アカウント + 選択ドメイン）」で決まる。
FTPホストから公開URLは一意に逆算できないため、公開URLは取得後に `config/site.json` の `public_base_url` へ記録する。

## 9. 検索エンジン向けファイル

本番ビルド時に以下を自動生成する。

- `public/sitemap.xml`
- `public/robots.txt`

`sitemap.xml` は本番HTMLルート一覧から生成し、受付停止中の `contact.html` は含めない。
`robots.txt` は全公開ページのクロールを許可し、`https://bousaikun.ashigaru.jp/sitemap.xml` をサイトマップとして指定する。

記事追加・URL変更時は `scripts/build_public.py` の本番ルートから自動反映されるため、手動でURL一覧を編集しない。

## 10. Google Search Console・インデックス運用

新規サイト公開、URL構造変更、サイトマップ・robots変更時は `docs/SEARCH_CONSOLE_INDEXING.md` を実行する。

最低確認:

1. 本番 `sitemap.xml` がHTTP 200
2. 本番 `robots.txt` がHTTP 200
3. Googlebot相当User-Agentでも `sitemap.xml` がHTTP 200
4. Search Consoleプロパティと本番URLが一致
5. Search Consoleへ `sitemap.xml` を送信
6. サイトマップの取得成功を確認
7. インデックス状況は別途「ページのインデックス登録」・URL検査で確認

Search Consoleに404等の過去エラーが残っていても、本番側で現在200を確認できる場合は、まず前回取得時刻・プロパティURL・再取得状況を確認する。

