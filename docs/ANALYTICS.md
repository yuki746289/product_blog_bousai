# Google Analytics 運用

## 測定ID

`G-XQVLD5HMNG`

## 実装方針

Google Analyticsのタグは、トップページ、カテゴリページ、記事ページ、固定ページを含むすべての公開HTMLの `<head>` 内に出力する。

共通スニペット:

`templates/partials/google_analytics.html`

ページごとにタグを手書きで複製せず、共通テンプレートから挿入する。

Lighthouseで接続確立コストが確認されたため、Google Tag Manager / Google Analyticsのオリジンへ `preconnect` を設定する。

## イベント計測

共通JS `preview/bousai_common.js` のイベントデリゲーションで、以下を送信する。

| イベント | 発火条件 | 主なパラメータ |
|---|---|---|
| `amazon_click` | `amazon.co.jp` / `*.amazon.co.jp` / `amzn.to` へのクリック | `link_url`, `link_text`, `page_path` |
| `product_guide_click` | 情報記事等から個別の商品紹介ページ（`/goods/*.html`、カテゴリトップ除外）へのクリック | `link_url`, `link_text`, `page_path` |

商品購入完了はAmazon側で発生するため、自サイトのGA4イベントでは計測しない。
`amazon_click` は「Amazonへ送客したクリック」であり、購入・売上を意味しない。

## 公開前チェック

- Google Analyticsタグが `<head>` 内に存在する
- 測定IDが `G-XQVLD5HMNG` である
- 同一ページにタグを重複挿入していない
- `amazon_click` / `product_guide_click` の実装が共通JSに存在する
- GA4 DebugViewまたはリアルタイムでイベント受信を確認する
- 公開HTML以外の管理ページ・テストデータには不要
- 将来Cookie同意等の要件を導入する場合は、その仕様に合わせて発火条件を見直す

## アクセス解析の用途

主に以下を確認する。

- ページビュー
- 人気記事
- 流入ページ
- カテゴリ別アクセス
- ピックアップ記事の閲覧状況
- 深掘り候補の選定
- 情報記事 → 商品紹介ページの遷移
- Amazon送客クリック

アクセス数やクリック数だけで記事品質を判断せず、安全性・鮮度・検索意図との一致も併せて評価する。
