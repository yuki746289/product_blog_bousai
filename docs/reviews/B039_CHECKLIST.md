# B039 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B039`
- title: 地震後、自宅に残る？避難所へ行く？在宅避難と避難所の判断基準
- content_role: `practical`
- risk_level: `high`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-04
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

## 1. 適用プロファイル確認

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| 防災サイトプロファイル確認 | PASS | 発災後の生活場所判断に関わるhigh-risk記事として適用 |
| 必須専門家ロール選定 | PASS | E01〜E08,E11〜E14 |
| 条件付き専門家ロール判定 | PASS | E09/E10はN/A |
| 詳細架空ペルソナ | N/A | 地震後に自宅か避難所か迷う状況ベース読者設定 |
| N/A項目の理由確認 | PASS | 商品比較・独自計測を主目的としない |

## 2. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 危険確認→避難場所/避難所の区別→在宅避難条件→支援→切替判断まで一連で整理 |
| C02 出典・安全性 | PASS | 令和8年版防災白書、内閣府の避難場所・避難所・在宅避難者支援資料、消防庁を一次根拠に使用 |
| C03 画像・視覚要素 | PASS | 神戸市の実際の避難所写真1点＋判断フロー・比較表・チェックリスト |
| C04 読みやすさ・UI | PASS | 結論・安全ボックス・比較表・切替サインを上位配置 |
| C05 内部リンク | PASS | B007/B024/B023/B030/B038と地震カテゴリへ接続 |
| C06 商品導線・商品記事 | N/A | 商品購入を主目的にせず、備蓄詳細はB024へ委ねる |
| C07 Q&A | N/A | 本文で主要疑問を完結。重複Q&Aを増やさない |
| C08 同期・公開前 | PASS | Markdown / preview / research / checklist / registry / category / parent導線を同期対象 |
| C09 日付・構造化データ | PASS | registryから公開日・更新日・BlogPosting / BreadcrumbList生成対象 |
| C10 デザイン・UX | PASS | 「危険なら避難」「安全なら在宅も選択肢」「再判断」を上部で理解可能 |
| C11 読者・マーケティング | PASS | 避難所不安を煽らず、生活場所判断と支援アクセスへ誘導 |
| C12 アクセシビリティ | PASS | 横スクロール表へrole/aria-label/tabindex、色依存なし |
| C13 技術品質・信頼性 | PASS | 共通CSS/JSのみ。新規外部スクリプトなし |
| C14 計測・グロース | N/A | 新規イベントなし |

## 3. 防災サイト固有チェック結果

| サイト固有チェック | 状態 | 根拠・備考 |
|---|---|---|
| S01 サイトプロファイル・適用判定 | PASS | 生命安全と公的一次情報を最優先 |
| S02 情報設計・ファインダビリティ | PASS | B007=地震pillar、B024=ライフライン、B039=生活場所判断として役割分離 |
| S03 法務・権利・広告表示・プライバシー | PASS | Commons CC BY 2.1 Japanの作者・出典・ライセンスを保持。広告誘導なし |
| S04 ブランド・トーン・コンテンツデザイン | PASS | 在宅避難と避難所の優劣を煽らず条件で整理 |
| S05 日本向けローカライゼーション | PASS | 日本の指定緊急避難場所・指定避難所・在宅避難者支援制度を使用 |
| S06 運用・ガバナンス・保守性 | PASS | source_checked_at / next_review_at / evidence docsを設定 |
| S07 セキュリティ・外部依存 | PASS | Commons画像はproduction buildでローカル化対象。公的情報は外部リンク |
| S08 数値・統計・リアルタイム要約 | N/A | 独自数値閾値なし。リアルタイム情報を要約しない |

## 4. High-risk追加確認

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| 津波・火災・倒壊等の危険時に在宅避難を優先しない | PASS | 冒頭・安全ボックス・禁止事項で避難優先を明記 |
| 建物の外見だけで安全判定しない | PASS | 専門判定をサイトが代替しないと明記 |
| 指定緊急避難場所と指定避難所を混同しない | PASS | 定義と役割比較表を掲載 |
| 指定避難所が必ず開設・受入可能と保証しない | PASS | 開設・受入は自治体等の最新情報確認と明記 |
| 在宅避難者への支援を否定しない | PASS | 内閣府手引きに基づき支援対象の考え方を説明 |
| 在宅避難者へ物資が必ず自宅配送されると保証しない | PASS | 配布・登録等の地域差を明記 |
| 在宅避難を固定的な選択にしない | PASS | 余震・衛生・健康等で切り替えると明記 |
| マンション高層階を無条件に安全としない | PASS | 給水・排水・エレベーター等の設備停止を説明 |
| 福祉避難所の利用方法を全国一律に断定しない | PASS | 自治体差を明記 |

## 5. 読者・ページ設計の証跡

- target_reader: 大地震後、自宅が住めそうに見えるが避難所へ行くべきか迷う一般生活者
- usage_context: 平時準備 / 発災直後 / 避難生活開始時
- knowledge_level: beginner/basic
- urgency_level: preparing/imminent/post-disaster
- reader_problem: 避難所へ必ず行くべきか、在宅避難を選べる条件が分からない
- reader_goal: 緊急危険・建物安全・生活継続・支援情報を順に確認して生活場所を判断する
- page_job: 指定緊急避難場所・指定避難所・在宅避難を家庭の判断フローへ翻訳する
- entry_path: 検索 / B007 / B024 / 地震カテゴリ
- next_action: 危険確認→必要なら緊急避難→生活継続確認→在宅または避難所→毎日再判断
- conversion_path: 安全行動→B024/B023/B030
- design_priority: 緊急時の誤った残留と「避難所へ行けばよい」の単純化を両方防ぐ

## 6. 証跡

- gap review: `docs/research/EARTHQUAKE_CONTENT_GAP_REVIEW_20260904.md`
- brief: `docs/research/B039_STAY_HOME_OR_SHELTER_BRIEF.md`
- sources: `docs/research/B039_SOURCES.md`
- images: `docs/research/B039_IMAGES.md`
- article: `content/articles/B039_earthquake_stay_home_or_shelter.md`
- preview: `preview/article_b039.html`
- public_path: `earthquake/earthquake-stay-home-or-shelter.html`
- content_registry: 登録対象
- category: `category_earthquake`掲載対象

## 7. 公開後確認

- production build / JS / Commons localization / FTPS / HTTP smokeをPASSさせる。
- Search Console蓄積後、B007/B024とのクエリ競合を確認する。
- 在宅避難・避難所支援制度の改定時はsource reviewを前倒しする。

## 8. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 一次情報、カニバリ、安全上の例外条件、支援制度の誤解防止、権利、UX、アクセシビリティを確認済み。公開時にCI・本番スモークを最終確認する。
