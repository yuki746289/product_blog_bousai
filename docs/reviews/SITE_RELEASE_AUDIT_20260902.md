# 防災ブログ サイト横断公開監査

監査日: 2026-09-02  
対象: `preview/` 全HTML、共通CSS、固定ページ、共通フッター、公開前仕様

## 1. 結論

静的なHTML/CSS・リンク監査では、今回対象とした問題は解消済み。

- HTMLページ総数: **51**
- 既存プレビュー: **46**
- 新規固定ページ: **5**
- 静的監査PASS: **51 / 51**

ただし、ローカルブラウザでの実表示確認、本番ページ化、Google Analytics本番挿入等が未完了のため、サイト全体の `READY_TO_PUBLISH` は **NO** とする。

## 2. 新規固定ページ

| ページ | ファイル | 状態 |
|---|---|---|
| 運営方針 | `preview/about.html` | PASS |
| 免責事項 | `preview/disclaimer.html` | PASS |
| プライバシーポリシー | `preview/privacy.html` | PASS |
| 広告について | `preview/advertising.html` | PASS |
| お問い合わせ | `preview/contact.html` | PASS |

お問い合わせは実在しない連絡先を仮作成せず、現在は一般向け受付を開始していないことを明示している。

## 3. 全51ページ横断リンク監査

| チェック | 結果 |
|---|---|
| 「準備中」表記 | PASS / 0件 |
| `href="#"` | PASS / 0件 |
| `title-link--planned` | PASS / 0件 |
| `category-article-link--planned` | PASS / 0件 |
| フッター欠落 | PASS / 0件 |
| 固定ページ5リンク欠落 | PASS / 0件 |
| Amazonアソシエイト共通表示欠落 | PASS / 0件 |
| 存在しない内部HTMLへのリンク | PASS / 0件 |

監査中、以下の3カテゴリに実ページリンク済みなのにplannedクラスが残っていることを検出し、修正後に再確認した。

- `preview/category_home.html`
- `preview/category_insurance.html`
- `preview/category_post_disaster.html`

## 4. 共通フッター

全ページで次のリンクへ統一した。

- 運営方針
- 免責事項
- プライバシーポリシー
- 広告について
- お問い合わせ
- 気象庁 防災情報

さらに全ページの共通フッターへ次のAmazonアソシエイト表示を統一した。

> Amazonのアソシエイトとして、当サイトは適格販売により収入を得ています。

元々フッター自体がなかった一部記事ページにも共通フッターを追加した。

## 5. CSS semantic role 再チェック

`preview/bousai_common.css` を再確認。

| UI役割 | 状態 |
|---|---|
| 章見出し / section role | PASS |
| 要点・結論 / summary role | PASS |
| 注意 / warning role | PASS |
| 危険・禁止 / danger role | PASS |
| 出典 / info role | PASS |
| 商品紹介記事CTA / product role | PASS |
| Amazon購入CTA / purchase role | PASS |
| 関連記事 / related role | PASS |
| 表ヘッダー / table role | PASS |
| フッター補足表示 | PASS |
| CSS波括弧の対応 | PASS |

商品紹介記事CTAは紫系、章見出しは緑系、Amazon購入CTAは濃い青系として分離されている。

## 6. 仕様・チェックリスト反映

反映済み:

- `docs/BOUSAI_SITE_SPEC.md`
- `docs/SITE_STRUCTURE.md`
- `docs/ARTICLE_REVIEW_CHECKLIST.md`
- `docs/reviews/ARTICLE_CHECKLIST_TEMPLATE.md`
- `docs/SITE_RELEASE_CHECKLIST.md`
- `docs/reviews/SITE_UI_LINK_AUDIT_20260902.md`

追加した主なルール:

- 記事本数をサイト完成条件にしない
- 固定ページを記事IDとは別管理する
- 共通フッターから固定ページへ到達可能にする
- 存在しないページを `href="#"` のまま公開しない
- Amazonアソシエイト表示を共通位置へ置く
- CSSは意味上の役割ごとに色・見た目を分離する
- サイト全体の公開判定は記事別チェックとは別に行う

## 7. 残課題

### 静的監査では確認できない項目

- ローカルブラウザでの実際の色味
- hover / focus時の見え方
- PC幅のレイアウト
- スマートフォン幅のレイアウト
- 商品画像の実ロード状態
- 外部画像の403/404/ホットリンク制限
- 本番ページのGoogle Analytics
- previewの `noindex` を本番公開時に適切に扱うこと
- 本番URLへ変換後の最終リンク確認

## 8. 最終判定

- HTML/CSS静的監査: **PASS**
- 固定ページ・共通フッター: **PASS**
- CSS役割分離: **PASS**
- ローカル実ブラウザ確認: **TODO**
- 本番実装確認: **TODO**
- READY_TO_PUBLISH: **NO**

## 9. UI形状・Q&A文脈導線の追補（2026-09-02）

### CSS

色だけではなく形状でも役割を分離した。

- 章見出し: 塗りつぶし帯を廃止し、左アクセントバー + 下罫線
- 要点: 「!」丸アイコン付きコールアウト
- 注意・危険: 警告アイコン + 上罫線の警告パネル
- 商品紹介CTA: 「商品」バッジ + 矢印 + 浮き上がりカード
- Q&A CTA: 「Q」丸アイコン + 点線枠の疑問解決リンク
- Amazon購入CTA: 独立した購入ボタン

CSS波括弧・主要selectorを静的確認しPASS。

### Q&A本文導線

既存25件のQ&Aを基準にB001〜B030を横断確認した。

- Q&A本文導線を追加: **24記事**
- 追加したQ&A個別アンカーリンク: **38件**
- 存在しないQ&Aアンカー: **0件**
- 同一記事内の同一Q&A重複: **0件**
- HTML / Markdown同期: **PASS**
- 記事別チェックリスト同期: **PASS**

既存Q&Aと直接対応する質問がないため、無理に導線を追加しなかった記事:

- B007
- B016
- B017
- B018
- B019
- B023

記事から `qa.html#qa-...` へ遷移した場合、対象の `details` を自動で開く処理もQ&Aページへ追加した。

実ブラウザでの最終的な見た目・スクロール位置・スマートフォン表示は引き続きTODO。

## 10. 最終画像・問い合わせ導線再監査（2026-09-02）

### 問い合わせ

一般向け受付を開始していないため、`contact.html` はファイルを残したまま `noindex` とし、全ページのフッターから「お問い合わせ」リンクを削除した。

- 公開フッターの固定ページ: 運営方針 / 免責事項 / プライバシーポリシー / 広告について
- `contact.html` への公開導線: **0件**

### 画像

ユーザーの実ブラウザ確認で画像リンク切れがあったため、外部画像依存を再監査した。

修正:

- 国土地理院ハザードマップの外部バナー画像を4ページから削除し、公式サイトへのテキストCTAへ変更
- B023の消防庁直画像をローカルAI画像へ置換し、重複AI画像を削除
- B024の消防庁直画像をローカルAI画像へ置換し、重複AI画像を削除
- B027の水戸市直画像を削除し、既存Wikimedia画像をヒーローへ移動
- B029の国交省直画像2点を削除。商品記事のため商品カード画像を主視覚要素とする
- 全ページへ `bousai_common.js` を追加し、将来の外部画像ロード失敗時に壊れた画像アイコンではなく代替メッセージを表示
- 商品カードは既存の商品専用画像フォールバックを維持

既知の脆弱URL（GSIバナー / FDMA images_pre / 水戸市9766 / MLIT carsafety画像）はHTMLから **0件**。

## 11. 最終静的チェック結果（2026-09-02）

全51 HTMLページを再走査。

| 項目 | 結果 |
|---|---|
| HTMLページ | 51 / 51 PASS |
| 共通 `bousai_common.js` 読み込み | 51 / 51 PASS |
| `contact.html` への公開リンク | 0件 |
| 「準備中」 | 0件 |
| `href="#"` | 0件 |
| plannedクラス | 0件 |
| 画像タグ | 127件 |
| alt欠落 | 0件 |
| 存在しないローカル画像 | 0件 |
| 既知の脆弱外部画像URL | 0件 |

商品関連8ページ:

- 商品カード: **29件**
- 商品画像欠落: 0
- alt欠落: 0
- `referrerpolicy="no-referrer"` 欠落: 0
- 商品専用 `onerror` フォールバック欠落: 0

B029「尾西の車載用防災ミニボックス」は、検索で確認できた同商品のプレス画像 `img_340096_2.jpg` へ差し替えた。

### 判定

- 静的HTML/CSS/JS監査: **PASS**
- 画像構成・フォールバック: **PASS**
- お問い合わせ非表示: **PASS**
- **READY_TO_UPLOAD: YES**
- READY_TO_PUBLISH: アップロード後に本番URLで画像・リンク・PC/スマホ表示をスモークテストして最終確定

## 12. 本番アップロード・公開後スモークテスト（2026-09-03）

GitHub Actions `Deploy production site` から忍者ホームページへFTPSアップロードを実施。

- 本番生成: PASS
- 単体・公開ビルドテスト: PASS
- FTPSアップロード: PASS
- 公開URL HTTPスモークテスト: PASS
- 公開URL: `https://bousaikun.ashigaru.jp/`

公開後に取得確認した対象:

- トップページ
- `qa.html`
- `guide/first-disaster-preparedness.html`
- `vehicle/car-flood-submersion.html`
- `goods/portable-power-station-disaster.html`
- `bousai_common.css`
- `bousai_common.js`

最終判定:

- READY_TO_UPLOAD: **YES / 完了**
- READY_TO_PUBLISH: **YES**
- DEPLOYMENT_STATUS: **PUBLISHED**

