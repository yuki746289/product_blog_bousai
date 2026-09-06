# Google Search Console・インデックス運用

更新日: 2026-09-03

## 1. 目的

新規公開・URL追加・サイト構造変更後に、Googleが公開ページを発見・取得できる状態を確認する。

重要:

- Search Consoleへのサイトマップ送信は、Googleへサイトマップの場所を通知する操作であり、ファイル自体をGoogleへアップロードする操作ではない。
- サイトマップ取得成功と、各ページのクロール・インデックス登録成功は別に管理する。
- サイトマップ掲載はクロール・インデックス登録を保証しない。
- Search Consoleの過去エラー表示だけを根拠に、本番で正常なファイルを不用意に変更しない。

## 2. 本番側の前提

本番ビルドで以下を自動生成する。

- `/sitemap.xml`
- `/robots.txt`

運用ルール:

- `sitemap.xml` は公開対象HTMLから自動生成する。
- 非公開・公開停止ページをサイトマップへ含めない。
- `robots.txt` へ本番サイトマップURLを記載する。
- サイトマップURL一覧を手作業で二重管理しない。
- 本番URLの基準は `config/site.json` の `public_base_url` とする。

## 3. 初回公開時の手順

1. 本番デプロイを完了する。
2. ブラウザまたはHTTPクライアントで以下が取得できることを確認する。
   - トップページ
   - `sitemap.xml`
   - `robots.txt`
3. `sitemap.xml` がHTTP 200を返すことを確認する。
4. `robots.txt` がHTTP 200を返し、本番の `sitemap.xml` URLを含むことを確認する。
5. Googlebot相当のUser-Agentでも `sitemap.xml` がHTTP 200になることを確認する。
6. Google Search Consoleへサイトを登録し、所有権確認を完了する。
7. Search Consoleで選択しているプロパティが本番URLと一致することを確認する。
   - `http` / `https`
   - ホスト名
   - `www` 有無
   - URLプレフィックス型の場合は末尾のパス
8. 「サイトマップ」から `sitemap.xml` を送信する。
9. ステータスが成功し、検出されたURLが表示されることを確認する。
10. トップページや主要pillar記事は必要に応じてURL検査を行う。

## 4. Search Consoleでサイトマップエラーが出た場合

### 4.1 404 / 「サイトマップを読み込めませんでした」

次の順で切り分ける。

1. Search Consoleに送信したサイトマップURLを確認する。
2. 同じURLを通常ブラウザ・HTTPクライアントで直接開く。
3. HTTPステータスを確認する。
   - 404: 配置先・デプロイ・URLを修正する。
   - 200: 次の確認へ進む。
4. Googlebot相当User-Agentで同じURLを取得し、HTTP 200になるか確認する。
5. `robots.txt` がサイトマップ取得を妨げていないか確認する。
6. XMLが有効で、公開対象URLだけが含まれているか確認する。
7. Search ConsoleのプロパティURLと本番URLが一致しているか確認する。
8. サイト側で現在HTTP 200が確認でき、エラー発生後に修正した場合は、Search Console側の表示が前回取得結果である可能性を考慮する。
9. 必要に応じてサイトマップを再送信する。古いエラー表示だけを理由にURL構造や正常なXMLを変更しない。

### 4.2 「取得できませんでした」だが本番は200

- 本番の通常アクセスとGooglebot相当アクセスを両方確認する。
- Search Consoleのプロパティ不一致を確認する。
- 直前に404から200へ修正した場合は、Search Console側の再取得を待つ。
- 再送信を繰り返さない。まず本番側の再現性ある200確認を優先する。

## 5. サイトマップ成功後

サイトマップ成功は「Googleがサイトマップを取得できた」状態であり、全URLのインデックス登録完了ではない。

確認先:

- Search Console「ページのインデックス登録」
- URL検査
- サイトマップ別の検出URL

新規公開・インデックス登録リクエスト直後は、検索結果への反映に時間がかかるため、即日表示されないことを異常判定しない。

## 6. 継続運用

### 記事追加・URL追加

- 本番ビルドで `sitemap.xml` を自動再生成する。
- デプロイ後にサイトマップのHTTP 200を確認する。
- URL一覧を手作業で追記しない。
- Search Consoleへ毎回サイトマップファイルを作り直して登録し直す運用にはしない。

### URL変更・削除

- 不要な旧URLをサイトマップから除外する。
- 移転先がある場合は適切なリダイレクトを検討する。
- 削除ページをトップページへ無条件転送して404を隠さない。

### 大規模変更

次の場合は `docs/SITE_RELEASE_CHECKLIST.md` と本手順を再実行する。

- ドメイン変更
- `http` / `https` 変更
- URL構造変更
- カテゴリ再編
- sitemap生成処理変更
- robots設定変更

## 7. 本サイトの現在値

- 本番: `https://bousaikun.ashigaru.jp/`
- sitemap: `https://bousaikun.ashigaru.jp/sitemap.xml`
- robots: `https://bousaikun.ashigaru.jp/robots.txt`
- sitemap生成: `scripts/build_public.py`
- Search Console: 登録済み
- sitemap: 送信・取得成功確認済み（2026-09-03）

## 8. 参考

Google公式:

- Search Console サイトマップ レポート
  - https://support.google.com/webmasters/answer/7451001?hl=ja
- URL検査ツール
  - https://support.google.com/webmasters/answer/9012289?hl=ja
- Google検索でページが見つからない場合
  - https://support.google.com/webmasters/answer/7474347?hl=ja
