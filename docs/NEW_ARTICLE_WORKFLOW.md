# キーワード調査から新規記事を作る標準手順

更新日: 2026-09-04

## 1. 目的

ラッコキーワード等で見つけた語句をそのまま記事数へ変換せず、検索意図・既存記事・安全性・内部リンクを確認して、本当に必要な記事だけを追加する。

この手順は、新規記事群を追加するときに繰り返し使用する。

上位レビュー設定:

- 共通専門家フレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
- 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
- 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

## 2. 開始条件

次のいずれかで開始する。

- 新しいカテゴリ・テーマを追加したい
- ラッコキーワード等で未対応の疑問を発見した
- Search Consoleで既存記事では十分に答えられない検索意図を発見した
- 季節前の調査で不足テーマが見つかった
- 既存pillarを深掘りする必要がある

## 3. Step 0: サイトプロファイル確認

本文企画前に `docs/BOUSAI_SITE_REVIEW_PROFILE.md` を確認する。

必須:

- ページ種別に必要な専門家ロールを確認
- `CONDITIONAL` の適用条件を確認
- 現在 `N/A` の視点に関係する新機能がないか確認
- persona_mode が `SITUATIONAL_SEGMENT` であることを確認

防災サイトでは詳細な架空ペルソナを作らない。
代わりに、状況・制約・目的に基づく読者設定を行う。

## 4. Step 1: キーワード取得

基点キーワードを決め、必要に応じて以下を使用する。

1. ラッコキーワード等のサジェスト
2. Google Trends
3. Google検索結果（SERP）
4. Keyword Planner（補助）
5. Search Console（公開後データがある場合）

生データは加工前のJSON / CSVを保管できる場合は保管する。

## 5. Step 2: 検索意図でクラスタリング

表記違いではなく「読者が何を知りたいか」でまとめる。

例:

- 防災リュック 20L
- 防災リュック 30L
- 防災リュック 何リットル

→ 「防災リュックの容量」という1クラスタとして扱う。

## 6. Step 3: 既存ページと照合

次を必ず検索する。

- 既存記事
- Q&A
- 商品記事
- カテゴリページ

判定:

- 既存ページで十分 → 新規記事を作らない
- 既存ページへ1〜2章追加で答えられる → 既存記事強化
- 短い回答で十分 → Q&A
- 購入判断が中心 → 商品記事
- 独立した判断・行動を十分説明できる → 新規記事

## 7. Step 4: カニバリを防ぐ

新規記事を作る場合、既存ページとの役割を1文で説明できること。

briefへ次を記録する。

- このページが答えること
- 既存ページが答えること
- このページでは扱わないこと

情報記事と商品記事が近い場合:

- 情報記事: 理解、判断、使い方、安全、運用
- 商品記事: 選び方、仕様比較、容量比較、購入判断

に分ける。

## 8. Step 5: 記事briefを作る

`docs/research/NEW_ARTICLE_BRIEF_TEMPLATE.md` を使用する。

最低限確定する項目:

- provisional article ID
- title案
- slug / planned public path
- content_role
- parent / related articles
- target_reader
- usage_context
- knowledge_level
- urgency_level（必要な場合）
- reader_problem
- reader_goal
- page_job
- entry_path
- next_action
- conversion_path
- design_priority
- primary search intent
- keyword cluster
- included intent
- excluded intent
- article conclusion
- source plan
- image plan
- product/Q&A/internal-link plan
- risk level
- review conditions
- applicable expert roles

詳細架空ペルソナの氏名・年齢・年収等は、現在の防災サイトでは作成しない。

**brief承認前に本文を書き始めない。**

## 9. Step 6: 出典・安全性調査

CR-02に従う。

特に防災・食品・保険・安全行動では、検索上位記事を根拠にしない。
検索上位記事は検索意図・構成の参考に限定し、重要主張は公的・一次情報で確認する。

E02 防災・ファクトチェック / リスクレビューを必須とする。

数値・集計・比較を扱う場合は `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md` のS08も適用する。

## 10. Step 7: title / H1 / meta description

本文作成前に仮案を作り、本文完成後に再確認する。

- title: 主検索意図を自然に表す
- H1: titleと意味を一致させる
- meta description: ページ固有の内容を簡潔に説明
- キーワード羅列をしない
- 既存ページとの完全重複を避ける

## 11. Step 8: 記事作成

作成・同期対象:

- `content/articles/Bxxx_*.md`
- `docs/research/Bxxx_SOURCES.md`
- `docs/research/Bxxx_IMAGES.md`
- 必要なら `docs/research/Bxxx_PRODUCTS.md`
- `preview/article_*.html`
- `docs/reviews/Bxxx_CHECKLIST.md`
- `data/content_registry.json`

記事台帳の日付は役割を分ける。

- `published_at`: 初回本番公開時に確定し、その後は原則変更しない
- `modified_at`: 記事本文を更新した日に更新
- `source_checked_at`: 本文根拠を再確認した日に更新
- `last_reviewed_at`: 内部レビューを実施した日に更新

レビューのみで本文を変更していない場合、`modified_at` は更新しない。

商品記事の場合は `docs/AFFILIATE_POLICY.md` とE09を追加適用する。

## 12. Step 9: 内部リンク・情報設計

公開前に次を設計する。

- 親pillar → 新規記事
- 新規記事 → 親pillar
- 関連detail/practical
- 対応Q&A
- 自然な商品記事導線
- カテゴリ
- パンくず
- URLとページ役割

新規記事を孤立ページにしない。

E04 情報設計 / ファインダビリティ、およびS02を確認する。

## 13. Step 10: レビュー

以下を実行する。

1. `docs/ARTICLE_REVIEW_CHECKLIST.md`
2. `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`
3. `docs/EXPERT_REVIEW_FRAMEWORK.md`
4. `docs/reviews/ARTICLE_CHECKLIST_TEMPLATE.md` に沿った記事別記録

### 情報記事の最低専門家レビュー

- E01 編集者
- E02 防災・ファクトチェック
- E03 SEO
- E04 情報設計
- E05 UX/UI
- E06 読者戦略・CRO
- E07 アクセシビリティ
- E08 ブランド / コンテンツデザイン
- E11 Webエンジニア
- E12 セキュリティ / 法務・権利・プライバシー
- E13 日本向けローカライゼーション
- E14 運用・ガバナンス

条件付き:

- 商品・Amazon導線 → E09
- 計測・数値分析・改善施策 → E10

必須確認:

- 検索意図
- カニバリ
- 出典
- 安全性
- オリジナリティ
- title / meta description
- 画像
- 内部リンク
- 情報設計
- 商品/Q&A条件
- デザイン / UX
- 読者設計
- アクセシビリティ
- ブランド / トーン
- 法務 / 権利 / プライバシー
- 日本向け文脈
- 技術品質
- 運用保守性
- 同期

## 14. Step 11: 本番テスト・公開

1. 本番ビルド
2. title / meta description欠落・重複テスト
3. 内部リンク
4. 画像
5. GA
6. sitemap
7. robots
8. 公開日・最終更新日・情報確認日の表示
9. BlogPosting / BreadcrumbList JSON-LD
10. JavaScript構文
11. 主要アセットHTTP
12. HTTPスモークテスト
13. 外部API・リアルタイム機能（該当時）

を変更範囲に応じてPASSさせる。

共通UIや実装を変更した場合は `docs/SITE_RELEASE_CHECKLIST.md` も実行する。

## 15. Step 12: 公開後

- sitemapへ自動反映されたことを確認
- 必要ならSearch Console URL検査
- Search Consoleにデータが蓄積した後、クエリ・CTR・順位を確認
- 想定と違う検索意図で表示されている場合はtitle/見出し/内容を修正
- 同一クエリで複数記事が競合していないか確認
- 新規機能で外部依存や運用負荷が増えた場合はE11/E12/E14を再評価

## 16. 定期運用

キーワード調査は1回で終わりにしない。

目安:

- 季節テーマ: 需要ピークの1〜2か月前
- 通年テーマ: 半年〜1年単位で再調査
- Search Console: データ量が十分になった後は定期確認

再調査時も「新規記事を増やす」ことを目的にせず、既存記事強化・統合・Q&A追加を含めて判断する。

サイト機能を追加した場合は、先に `docs/BOUSAI_SITE_REVIEW_PROFILE.md` の `N/A / CONDITIONAL / REQUIRED` を再評価する。