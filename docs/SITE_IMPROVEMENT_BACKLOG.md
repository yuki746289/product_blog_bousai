# サイト改善・対応事項

更新日: 2026-09-03

Geminiレビュー、現サイト監査、SEO運用上の改善点を統合した対応事項。
一般論をそのまま採用せず、現サイトとの差分だけを管理する。

## 状態

- `TODO`: 未対応
- `PLANNED`: 方針確定・実施待ち
- `IN_PROGRESS`: 対応中
- `WAITING_DATA`: データ蓄積後に実施
- `DONE`: 対応済み
- `REJECTED`: 現仕様では採用しない

## 担当

- **ChatGPT**: リポジトリ修正、Web調査、記事分析、実装、監査までこちらで対応可能
- **ユーザー**: Google等のログイン済み管理画面・実機操作が必要
- **共同**: ユーザーが取得・操作し、こちらが分析・実装する

## 実施順

| 順番 | 優先 | 対応事項 | 状態 | 担当 | 実施内容・完了条件 |
|---:|:---:|---|---|---|---|
| 1 | A | キーワード調査を記事企画の標準工程へ追加 | DONE | ChatGPT | `docs/KEYWORD_RESEARCH_POLICY.md` を正本化済み |
| 1A | A | 新規記事作成手順を標準化 | DONE | ChatGPT | `docs/NEW_ARTICLE_WORKFLOW.md` とbriefテンプレートを作成 |
| 2 | A | ラッコキーワード等による需要・疑問調査 | DONE | 共同 | ユーザーが取得した結果の共有、または公開情報として取得可能な範囲をこちらで調査。検索意図でクラスタリングする |
| 3 | A | Google Trendsで季節性を確認 | DONE | ChatGPT | 台風・大雨・停電・非常食等の需要時期を確認し、公開・リライト時期へ反映 |
| 4 | A | 実際のGoogle検索結果（SERP）調査 | DONE | ChatGPT | 候補キーワードごとに上位ページ、検索意図、記事形式、公的機関の有無を確認 |
| 5 | B | Google Keyword Plannerで検索需要を補足 | PLANNED | 共同 | Google Ads管理画面で検索ボリューム等をユーザーが取得し、こちらで候補評価へ反映。必須ではない |
| 6 | A | 既存30記事・Q&A・商品記事との重複/カニバリ確認 | DONE | ChatGPT | キーワードクラスタを「既存記事強化 / 新規記事 / Q&A / 商品導線 / 見送り」に分類 |
| 7 | A | title・meta description横断監査 | DONE | ChatGPT | 全公開ページの重複、内容一致、検索意図との整合、過度な類似を監査・修正 |
| 8 | A | 公開日・最終更新日・情報確認日の明示 | DONE | ChatGPT | `published_at` / `modified_at` / `source_checked_at` を台帳で分離し、本番記事へ共通生成 |
| 9 | A | Article/BlogPosting + BreadcrumbList構造化データ | DONE | ChatGPT | 本番ビルドでBlogPosting + BreadcrumbListを台帳からJSON-LD共通生成 |
| 10 | A | 構造化データ検証 | IN_PROGRESS | 共同 | Python/CIのJSON-LD構文・型・日付・パンくず検証に加え、本番配信HTMLでBlogPosting/BreadcrumbListをデプロイ後に自動確認。Google Rich Results Test等の外部Google検証のみ残る |
| 11 | A | PageSpeed / Core Web Vitals監査 | IN_PROGRESS | 共同 | Lighthouse mobileでトップ/B001/B028を実測。Baseline score 70/56/68、CLSは全て0。LCP遅延・過大画像・GA接続・ホスティング注入広告JSを切り分け、コード側追加改善を反映中。実ユーザーINP等はSearch Console/CrUX待ち |
| 12 | A | 外部画像依存の縮小・WebP等の画像最適化 | DONE | ChatGPT | Commons記事画像75出現/74ユニークを本番ビルドでローカルWebP化、失敗0。960px本体＋720px responsive variant、width/height・fetchpriorityを付与。商品/メーカー画像は外部参照維持 |
| 13 | A | モバイル実機レビュー | TODO | ユーザー | 実スマホで横スクロールナビ、Q&A、表、商品CTA、文字サイズ、タップ領域を確認。指摘後の修正はChatGPT |
| 14 | B | 出典リンク表示名の統一 | DONE | ChatGPT | 全35記事・商品/固定ページを監査。生URL表示を「機関名『資料名』」へ統一し、source-box内の生URL表示をCIで禁止 |
| 15 | B | 実用チェックリストの横断強化 | DONE | ChatGPT | practical記事を横断監査。B033〜B035を含む全practical記事に保存用行動チェックを持たせ、欠落防止ルールと自動テストを追加 |
| 16 | B | 商品記事へ数量・容量・稼働時間等の概算例を追加 | DONE | ChatGPT | 水・非常食、携帯トイレ、ポータブル電源の商品記事へ条件付き計算式と具体例を追加。仮定値・個人差・変換ロス等を明示し、保証表現を回避 |
| 17 | B | GA4でAmazonリンククリック計測を実装 | IN_PROGRESS | 共同 | `amazon_click` と `product_guide_click` の共通JS実装・自動テストは完了。GA4 DebugView/リアルタイムでの受信確認が残る |
| 18 | B | 季節前のリライト・記事公開サイクル | PLANNED | ChatGPT | Google Trends・季節性を基に需要ピークの1〜2か月前に候補を出す |
| 19 | C | ペット・乳幼児・高齢者等の属性別テーマ調査 | DONE | ChatGPT | 調査後、B033ペット/B034乳幼児/B035高齢者をbrief→本文→一次情報→レビュー→内部リンク→本番公開まで実装 |
| 20 | C | 困りごと・ネガティブ検索語の調査 | DONE | ChatGPT | 「重すぎる/いらない/期限切れ/捨てる/固まらない/臭い」を評価し、B002/B003/B031の既存強化へ分類。`docs/research/NEGATIVE_INTENT_RESEARCH_20260903.md` |
| 21 | C | 競合・類似防災サイトのコンテンツギャップ調査 | DONE | ChatGPT | 公的機関・小売/ブランド・防災専門通販と比較し、属性別/困りごと/自宅避難等の不足領域を整理。`docs/research/CONTENT_GAP_RESEARCH_20260903.md` |
| 22 | 後日 | Search Consoleデータ駆動リライト | WAITING_DATA | 共同 | ユーザーがSearch Consoleデータを取得/共有し、ChatGPTが表示回数・CTR・順位・クエリを分析して改修 |
| 23 | 後日 | Search Consoleでカニバリ監視 | WAITING_DATA | 共同 | 同一クエリで複数URLが表示されるケースを抽出し、統合・内部リンク・タイトル等を検討 |
| 24 | 後日 | GA4で記事→商品→Amazonの導線評価 | WAITING_DATA | 共同 | GA4データ蓄積後、記事別クリック率・導線別成果を分析 |
| 25 | 後日 | 自然被リンク獲得の検討 | WAITING_DATA | 共同 | コンテンツが蓄積してから参照されやすい資料・チェックリスト等を検討。リンク購入は行わない |
| 26 | - | FAQPageリッチリザルト獲得目的の実装 | REJECTED | - | Googleの現行検索仕様では優先施策にしない |

## キーワード調査から記事公開まで

```text
ラッコキーワード等
  ＋ Google Trends
  ＋ Keyword Planner（補助）
  ＋ 実際のGoogle検索結果
        ↓
検索意図でクラスタリング
        ↓
既存記事・Q&A・商品記事と照合
        ↓
既存記事強化 / 新規記事 / Q&A / 商品導線 / 見送り
        ↓
pillar / detail / practical / productへ配置
        ↓
公開
        ↓
Search Console + GA4で実績検証
        ↓
リライト・統合・内部リンク改善
```

詳細は `docs/KEYWORD_RESEARCH_POLICY.md` を参照する。

## 手動操作が必要な主な項目

ユーザー操作が必要なのは主に、ログイン済みアカウント・実機に依存する部分。

- Google Keyword Plannerのアカウント内データ取得
- Search Consoleの検索パフォーマンスデータ取得・エクスポート
- GA4管理画面でのイベント受信・レポート確認
- 実スマートフォンでの操作感確認

上記以外のリポジトリ修正、公開Web調査、記事・SEO監査、コード実装、本番デプロイは原則ChatGPT側で対応可能。


## ユーザー向けキーワード調査手順

ラッコキーワード等でユーザー側が取得するデータと共有方法は `docs/KEYWORD_RESEARCH_USER_GUIDE.md` を参照する。

初回は「防災リュック」「携帯トイレ」「非常食」の3語から開始し、JSON（AI向け）またはCSVを加工せず共有する。


## 初回キーワード調査結果

「防災リュック」「携帯トイレ」「非常食」の初回調査は完了。

- 取得: 1,736件
- ユニーク: 1,735件
- 結果: `docs/research/KEYWORD_RESEARCH_REPORT_20260903.md`

優先候補:
1. 非常食の賞味期限切れ・入替（新規detail）
2. 防災リュック容量/何L（新規detail）
3. B003携帯トイレ既存記事強化
4. B002 title/meta/検索意図調整
5. 家族構成別防災リュック（新規practical）


## 初回キーワード起点の新規記事実装

標準手順 `docs/NEW_ARTICLE_WORKFLOW.md` を実際に使用して、初回2記事を作成。

| 記事 | 検索意図 | 状態 |
|---|---|---|
| B031 | 非常食の賞味期限切れ・入れ替え | DONE |
| B032 | 防災リュックの容量・何L | DONE |

親記事B026/B002および防災入門カテゴリから内部リンクを追加し、カニバリを避けて役割分離した。


## 日付・構造化データ実装（2026-09-03）

記事の日付は用途を分離した。

- `published_at`: 本番で初めて公開された日
- `modified_at`: 記事内容の最終更新日
- `source_checked_at`: 公的・一次情報等を最後に確認した日
- `last_reviewed_at`: 内部レビュー日。公開上の「最終更新日」には流用しない

B001〜B030の公開日は、現行GitHub Actionsで確認できる最初の本番デプロイ（2026-09-02）を基準に固定した。B031/B032は追加・本番デプロイ日の2026-09-03。

本番ビルドでは `scripts/article_metadata.py` が記事台帳を正本として、次を共通生成する。

- 公開日 / 最終更新日 / 情報確認日の表示
- `BlogPosting` JSON-LD
- `BreadcrumbList` JSON-LD

JSON-LDを記事HTMLへ個別に手書きしない。構文、記事タイトル、`datePublished`、`dateModified`、パンくず3階層はビルド/テストで自動確認する。


## 画像最適化実装（2026-09-03）

- 対象: 記事本文内でWikimedia Commons帰属が明示されている画像
- 本番ビルド後にMediaWiki API等で取得し、960px WebP＋720px responsive variantへ変換して `assets/images/commons/` からローカル配信
- 画像へ `width` / `height` / `decoding="async"` を付与
- `loading="eager"` の記事メイン画像には `fetchpriority="high"` を付与
- 元画像ページへのWikimedia Commonsリンクをfigcaptionへ補完
- Amazon・メーカーの商品画像は権利・更新性を考慮しローカルコピーしない
- 取得失敗時は元の外部画像URLを残してページ公開を継続
- GitHub Actionsのproduction deployとHTTP smoke testで検証済み


## 属性別3記事の実装（2026-09-03）

公開SERP・公的一次情報・既存記事とのカニバリ確認を行い、次の3記事を標準新規記事フローで実装した。

| 記事 | 役割 | リスク | 本番パス |
|---|---|---|---|
| B033 ペット防災 | practical | standard | `guide/pet-disaster-preparedness.html` |
| B034 赤ちゃんの防災備蓄 | practical | elevated | `guide/baby-disaster-stockpile.html` |
| B035 高齢者の防災 | practical | elevated | `guide/senior-disaster-preparedness.html` |

共通実施:
- brief作成
- 一次情報確認
- Markdown / preview HTML
- SOURCES / IMAGES / CHECKLIST
- B001からの属性別内部リンク
- 防災入門カテゴリ掲載
- content registry登録
- BlogPosting / BreadcrumbList自動生成
- 本番HTTP/構造化データスモーク対象化

B034は厚労省・農水省・内閣府、B035は内閣府・農水省・厚労省等を根拠にし、医療・栄養・福祉の一律断定を避けた。
