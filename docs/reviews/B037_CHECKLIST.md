# B037 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B037`
- title: 家が浸水した後の片付け｜清掃・乾燥・消毒の順番と注意点
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
| 防災サイトプロファイル確認 | PASS | 高リスク発災後記事として適用 |
| 必須専門家ロール選定 | PASS | E01〜E08,E11〜E14 |
| 条件付き専門家ロール判定 | PASS | E09/E10はN/A |
| 詳細架空ペルソナ | N/A | 被災状況ベースで読者設定 |
| N/A項目の理由確認 | PASS | 商品販売・A/Bテスト等を行わない |

## 2. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 安全確認→記録→清掃→乾燥→必要な消毒を一連で説明 |
| C02 出典・安全性 | PASS | 厚生労働省を主根拠とし、2026年更新自治体で実務差を確認 |
| C03 画像・視覚要素 | PASS | 無理な被災写真を使わず、作業フロー・表・安全ボックスを使用 |
| C04 読みやすさ・UI | PASS | 作業順と床上/床下/屋外の違いを分離 |
| C05 内部リンク | PASS | 被災後カテゴリと大雨・水害カテゴリに入口を設置。記事内からB015/B005/B012/B013/B014へ回遊可能 |
| C06 商品導線・商品記事 | N/A | 防護具等を販売目的で誘導しない |
| C07 Q&A | N/A | 本文単体で主要判断を完結。必要性が生じた場合のみ追加 |
| C08 同期・公開前 | PASS | Markdown / preview / research / checklist / registry / categoryを同期 |
| C09 日付・構造化データ | PASS | registryから日付・BlogPosting・BreadcrumbListを生成しテストPASS |
| C10 デザイン・UX | PASS | 既存共通UIを使用し、5段階の復旧順を冒頭で明示 |
| C11 読者・マーケティング | PASS | post-disasterの読者に次行動を提示。収益誘導なし |
| C12 アクセシビリティ | PASS | テキスト・表・見出しで意味を伝達。共通アクセシビリティテストPASS |
| C13 技術品質・信頼性 | PASS | build / JS / FTPS / HTTP smokeすべてPASS |
| C14 計測・グロース | N/A | 新規イベントなし |

## 3. 防災サイト固有チェック結果

| サイト固有チェック | 状態 | 根拠・備考 |
|---|---|---|
| S01 サイトプロファイル・適用判定 | PASS | 感電・感染症・けが等の安全をSEOより優先 |
| S02 情報設計・ファインダビリティ | PASS | B015=記録、B037=清掃・乾燥・衛生として明確に役割分離。カテゴリ導線実装 |
| S03 法務・権利・広告表示・プライバシー | PASS | 被災者・個人宅画像を無理に使用せず、広告誘導なし |
| S04 ブランド・トーン・コンテンツデザイン | PASS | 被害を煽らず復旧順序と中止条件を重視 |
| S05 日本向けローカライゼーション | PASS | 厚労省・日本自治体の2026年現行案内に準拠 |
| S06 運用・ガバナンス・保守性 | PASS | 正本registry・research・checklist・previewを同期しCIで検証 |
| S07 セキュリティ・外部依存 | PASS | 本文機能は外部JS/APIに依存せず、公的リンクのみ |
| S08 数値・統計・リアルタイム要約 | PASS | 独自の消毒濃度・衛生安全閾値を作成していない |

## 4. 高リスク追加確認

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| 消毒より清掃・乾燥を先にする | PASS | 厚労省現行案内 |
| 危険な家へ撮影・家財救出目的で入らせない | PASS | B015と整合 |
| 濡れた電気設備へ触れさせない | PASS | 安全確認を最初に配置 |
| 床下・屋外の消毒を一律必須にしない | PASS | 自治体差を明記し地域案内確認 |
| 消毒剤濃度を独自に一律化しない | PASS | 製品表示・公的資料優先 |
| 食品を見た目・臭いだけで安全判断させない | PASS | 公的衛生情報と整合 |
| 医療症状をサイトで診断しない | PASS | 医療機関・相談窓口へ案内 |
| カビ・建材内部の乾燥を家庭作業だけで保証しない | PASS | 施工会社・専門業者相談を明記 |

## 5. 読者・ページ設計の証跡

- target_reader: 自宅が床上/床下浸水した家庭
- usage_context: 水が引いた後〜片付け開始時
- knowledge_level: beginner/basic
- urgency_level: post-disaster
- reader_problem: 片付け・清掃・消毒の順番が分からない
- reader_goal: 安全に復旧初動を進める
- page_job: 清掃・乾燥・必要な消毒の順序を整理
- entry_path: 検索 / 被災後カテゴリ / 大雨・水害カテゴリ / 関連記事
- next_action: 安全確認→記録→清掃→乾燥→必要な消毒
- conversion_path: 復旧行動→保険/住宅関連情報
- design_priority: 作業順を一目で理解し、危険作業を避ける

## 6. 証跡

- brief: `docs/research/B037_FLOOD_CLEANUP_BRIEF.md`
- sources: `docs/research/B037_SOURCES.md`
- images: `docs/research/B037_IMAGES.md`
- article: `content/articles/B037_flood_cleanup_dry_disinfect.md`
- preview: `preview/article_b037.html`
- public_path: `post-disaster/flood-cleanup-dry-disinfect.html`
- content_registry: 登録済み
- categories: `category_post_disaster` / `category_flood`掲載済み
- production_check: GitHub Actionsで tests / build / JS / FTPS / HTTP smoke PASS

## 7. 今後の改善候補

- B015/B005/B012等本文内からの直接コンテキストリンクは、回遊データや記事改稿時に追加を検討する。現在もカテゴリ入口と関連記事導線があり孤立ページではないため、公開ブロッカーとはしない。
- Search Consoleデータ蓄積後、検索意図・表示クエリ・B015とのカニバリを再確認する。

## 8. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 高リスク安全レビュー、一次情報、情報設計、アクセシビリティ、production build、HTTP smokeまで確認済み。
