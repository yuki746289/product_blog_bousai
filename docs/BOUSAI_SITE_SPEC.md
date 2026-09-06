# 防災ブログ固有仕様

更新日: 2026-09-03

本ファイルは**防災ブログというサイト固有の実装・情報設計だけ**を定義する。
記事作成の共通ルールは `docs/CONTENT_CREATION_RULES.md` を正とし、本ファイルへ重複記載しない。

## 1. 初期・運用方針

- ストック型の防災記事を中心にする。
- リアルタイム警報サイトとして運用しない。
- 緊急時は気象庁・自治体等の公的情報を優先する。
- 避難判断、津波、応急対応等の高リスク内容は目視レビュー必須。
- 記事本数をサイト完成条件にしない。

## 2. 情報設計

読者が次の3方向から記事へ到達できる構造とする。

1. 災害別
2. 困りごと別
3. 準備別

記事役割:

- pillar
- detail
- practical
- product

役割分担・分割基準は `docs/PICKUP_AND_DEEP_DIVE_POLICY.md` を参照する。

トップページの基本順:

1. ピックアップ
2. 防災入門
3. 災害別
4. 困りごと別
5. 防災グッズ
6. Q&A
7. 新着・更新
8. 公的情報

詳細なページ構造は `docs/SITE_STRUCTURE.md` を正とする。

## 3. 出典・安全性のサイト追加条件

共通ルール CR-02 に加え、防災分野では以下を優先する。

- 気象庁
- 内閣府
- 消防庁
- 国土交通省
- 自治体
- 制度所管官庁
- メーカー一次情報（商品仕様）

自動処理は「要確認の抽出」であり、記事内容の正しさを自動保証しない。

## 4. 商品・広告

- Amazonアソシエイトを利用する。
- 商品記事の詳細条件は `docs/AFFILIATE_POLICY.md` を正とする。
- 共通の商品文脈導線は `CONTENT_CREATION_RULES.md` CR-05B / CR-06 を適用する。
- 一般情報記事を広告主体にしない。

## 5. Q&Aページ

- トップページには代表Q&Aを3〜5件程度表示する。
- Q&A一覧はカテゴリ分類する。
- `details/summary` 等、キーボード操作可能な開閉UIを優先する。
- 回答末尾から詳細記事へ接続する。
- 記事本文からQ&Aへの導線は共通ルール CR-07B を適用する。
- 個別アンカー遷移時は該当Q&Aを開いた状態にする。

## 6. アクセス解析

- Google Analyticsを全公開ページで使用する。
- Measurement ID: `G-XQVLD5HMNG`
- 共通テンプレート: `templates/partials/google_analytics.html`
- ページ単位の手書きコピーを避ける。
- 詳細: `docs/ANALYTICS.md`

## 7. 共通CSS/UI実装

共通ルール CR-04C の役割分離を、`preview/bousai_common.css` で実装する。

現在の意味役割:

- section: 章見出し
- summary: 要点・結論
- warning: 注意
- danger: 危険
- info: 出典・公的情報・Q&A補助
- product: 商品紹介記事への内部CTA
- purchase: Amazon購入CTA
- related: 関連記事
- table: 表ヘッダー

主要UIは色だけでなく形状でも区別する。

## 8. 固定ページ・フッター

公開固定ページ:

- `about.html`
- `disclaimer.html`
- `privacy.html`
- `advertising.html`

`contact.html`:

- 受付窓口を公開するときだけ導線を表示
- 受付停止中は `noindex` のまま保持してよい
- 受付停止中はフッター・ナビゲーションから非表示
- 実在しないメール・フォームを仮作成しない

共通フッター:

- 公開固定ページ
- Amazonアソシエイト参加表示
- 気象庁等の公的情報リンク

## 9. 記事・レビュー管理

- 正式な記事状態は `data/content_registry.json` を正とする。
- 共通作成ルール: `docs/CONTENT_CREATION_RULES.md`
- 共通レビュー: `docs/ARTICLE_REVIEW_CHECKLIST.md`
- 記事別記録: `docs/reviews/Bxxx_CHECKLIST.md`
- 記事別ファイルには共通ルール本文をコピーしない。
- 変更時の同期範囲は共通ルール CR-08 を適用する。

## 10. 情報鮮度

- `last_reviewed_at` と `next_review_at` を管理する。
- 詳細は `docs/FRESHNESS_POLICY.md` を正とする。

## 11. 本番・完成条件

記事数ではなく、以下が満たされていることを完成条件とする。

- 必要なカテゴリ・固定ページ・Q&Aがある
- 内部リンク切れがない
- 共通CSS/UIが役割どおり
- 商品表示・広告表示が適切
- GA・noindex等の本番設定が正しい
- 画像・CSS・JSが本番で取得できる
- 公開後スモークテストがPASS

最終サイト判定は `docs/SITE_RELEASE_CHECKLIST.md` を正とする。

## 12. 検索エンジン・インデックス運用

- `sitemap.xml` と `robots.txt` は本番ビルドで自動生成する。
- Search Consoleの初回登録・サイトマップ送信・エラー切り分けは `docs/SEARCH_CONSOLE_INDEXING.md` を正とする。
- サイトマップは公開URLの発見支援であり、クロール・インデックス登録の保証として扱わない。
- Search Consoleの表示と現在の本番HTTP状態が食い違う場合は、本番URLを通常アクセスとGooglebot相当アクセスの両方で検証してから修正判断する。
- URL一覧を手動でサイトマップへ二重管理しない。

## 13. SEO・記事企画運用

- 新規記事テーマの選定では `docs/KEYWORD_RESEARCH_POLICY.md` を適用する。
- ラッコキーワード等の外部調査は「検索者の困りごと発見」に使用し、1キーワード1記事の量産には使用しない。
- キーワード候補は既存記事・Q&A・商品記事と照合し、既存記事強化を新規記事より先に検討する。
- 公開後の実データ評価はGoogle Search Consoleを使用する。
- 季節性の強いテーマは需要ピークの1〜2か月前に調査・リライトを検討する。
- 現在の改善対応一覧は `docs/SITE_IMPROVEMENT_BACKLOG.md` で管理する。

