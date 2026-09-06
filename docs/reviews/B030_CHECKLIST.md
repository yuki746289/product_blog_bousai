# B030 記事別専門家レビュー記録

> 共通専門家: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイトチェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`
>
> 専門家ロール: `docs/EXPERT_REVIEW_FRAMEWORK.md`

- article_id: `B030`
- title: 家族で決めておきたい災害時の連絡・集合ルール
- content_role: `practical`
- risk_level: `elevated`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-04
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`
- detailed_fictional_persona: `N/A`（根拠のない属性を作らず、利用状況・制約で設計）

## 1. 読者・ページ設計

- target_reader: 日本国内で家庭防災を具体化したい一般生活者
- usage_context: 平常時の準備、予報・災害前後の確認、または記事固有の判断が必要な場面
- knowledge_level: 防災の専門知識を前提にしない
- reader_problem: `家族で決めておきたい災害時の連絡・集合ルール` に対応する判断・準備事項を整理したい
- reader_goal: 安全側の条件を理解し、自分の家庭条件へ置き換えて次の行動を決める
- page_job: 具体的な行動手順・準備順序を示し、読者が実行できる状態にする
- entry_path: 検索、カテゴリ、関連記事、Q&A等
- next_action: 記事内の確認・準備を行い、必要なら公的情報・親/詳細記事・商品ガイドへ進む
- conversion_path: 安全理解 → 関連情報 → 必要時のみ商品比較/外部導線
- design_priority: 安全・正確性 → 読みやすさ → 導線 → SEO/CV

## 2. 専門家適用（E01〜E14）

| ID | 判定 | 結果・根拠 |
|---|---|---|
| E01 編集・コンテンツ戦略 | REQUIRED | PASS。記事役割、結論、判断条件、例外、次行動を確認 |
| E02 防災・ファクトチェック・リスク | REQUIRED | PASS。安全情報を購買・SEOより優先し、独自の安全保証を作っていない |
| E03 SEO | REQUIRED | PASS。検索意図、title/H1、既存記事との役割分離、内部リンクを確認 |
| E04 情報アーキテクチャ | REQUIRED | PASS。カテゴリ、親子関係、関連記事導線、公開パスを確認 |
| E05 UX/UI | REQUIRED | PASS。結論先行、表/箇条書き/注意枠等で判断しやすく整理 |
| E06 マーケティング・読者戦略/CRO | REQUIRED | PASS。読者課題→判断材料→次行動の順で、CVを先行させていない |
| E07 アクセシビリティ | REQUIRED | PASS。共通アクセシビリティ実装の対象。意味のあるリンク文言・構造を維持 |
| E08 ブランド/コンテンツデザイン | REQUIRED | PASS。煽りや制作側表現を避け、落ち着いた防災サイトのトーンを維持 |
| E09 商品/アフィリエイト | CONDITIONAL / N/A | N/A | 具体商品を主目的とする記事ではない。必要な場合のみ内部の商品ガイドへ接続 |
| E10 分析/グロース | CONDITIONAL | PASS。GA4/改善評価は共通実装。実データ評価は USER_ACTION_ITEMS の U04〜U07で管理 |
| E11 Web実装/信頼性 | REQUIRED | PASS。静的ビルド、リンク、構造化データ、本番スモークの対象 |
| E12 セキュリティ/法務/権利/プライバシー | REQUIRED | PASS | 出典・画像ライセンス・外部リンク・広告/権利上の誤認がないことを確認 |
| E13 日本向けローカライゼーション | REQUIRED | PASS。日本の制度・公的情報・生活文脈を基準にした |
| E14 運用/ガバナンス | REQUIRED | PASS。Markdown、research、review、registry、preview/公開ビルドの正本関係を維持 |

## 3. C01〜C14

| ID | 状態 | 根拠 |
|---|---|---|
| C01 内容・情報量 | PASS | 検索意図とpage jobに対して必要十分。文字数だけで判定しない |
| C02 出典・安全性 | PASS | 確認済み一次・公的/メーカー情報を優先。source_checked_at=2026-09-04 |
| C03 画像・視覚要素 | PASS | 既存画像レビューを継承し、画像を安全・性能判断の根拠にしていない |
| C04 読みやすさ/UI | PASS | 見出し・表・箇条書き・要点表示を用途に応じ使用 |
| C05 内部リンク | PASS | 親記事・関連記事・Q&A/商品ガイドを必要な文脈で接続 |
| C06 商品導線/商品記事 | N/A | 無理な商品挿入を行わない |
| C07 Q&A | CONDITIONAL PASS | 該当する文脈導線は本文説明の補助として扱い、Q&Aを説明の代替にしない |
| C08 同期/公開前 | PASS | 正本・preview・registry・レビュー状態を同期 |
| C09 日付/構造化データ | PASS | published/modified/source_checked/reviewedの意味を分離。公開ビルドで構造化データ生成 |
| C10 デザイン/UX | PASS | 安全情報が最優先に見え、CTAや商品が不自然に浮かない |
| C11 読者/マーケティング | PASS | SITUATIONAL_SEGMENTで問題・目標・entry/next actionを明確化 |
| C12 アクセシビリティ | PASS | 共通実装とページ構造を適用 |
| C13 技術/信頼性 | PASS | CI、ビルド、JS、外部依存、本番スモークで検証 |
| C14 分析/グロース | CONDITIONAL PASS | 計測実装を維持。実利用データはU04〜U07で後続評価 |

## 4. S01〜S08

| ID | 状態 | 根拠 |
|---|---|---|
| S01 サイトプロファイル/適用判定 | PASS | 防災サイトprofileとpersona_modeを適用 |
| S02 IA/ファインダビリティ | PASS | カテゴリ・親子・URL・関連記事の役割を確認 |
| S03 法務/権利/広告/プライバシー | PASS | 出典・権利・広告/公式情報の主体を区別 |
| S04 ブランド/トーン | PASS | 恐怖訴求や過剰断定ではなく、判断材料を落ち着いて提示 |
| S05 日本向け文脈 | PASS | 日本の制度・住環境・公的機関・表記を優先 |
| S06 運用/ガバナンス | PASS | status/review/source/dateの正本同期と再発防止を確認 |
| S07 セキュリティ/外部依存 | PASS | secret非公開、外部リンク/画像/API依存の安全な扱いを維持 |
| S08 数値/統計/リアルタイム | CONDITIONAL PASS | 数値は単位・前提・公称/仮定を分離し、保証値へ変換しない |

## 5. 最終横断チェック

| 項目 | 状態 |
|---|---|
| X01〜X05 共通最終確認 | PASS |
| SX01 未分類の専門家視点なし | PASS |
| SX02 N/A/条件付き理由あり | PASS |
| SX03 詳細架空ペルソナなしでも読者状況が明確 | PASS |
| SX04 公的/安全情報とサイト/商品情報を混同しない | PASS |
| SX05 日本向け文脈 | PASS |
| SX06 鮮度・更新責任 | PASS |
| SX07 再発問題のルール/テスト化検討 | PASS |

## 6. 証跡・後続事項

- source: `content/articles/B030_family_disaster_contact_plan.md`
- research: `docs/research/B030_SOURCES.md`（存在する場合）
- preview: `preview/article_b030.html`
- production: `guide/family-disaster-contact-plan.html`
- user-side: `docs/USER_ACTION_ITEMS.md`
- U03: 実スマートフォンでの横断UX確認はサイト共通対応事項として継続
- 商品画像のアカウント固有確認: N/A

## 7. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 現在のサイト個別プロファイル、E01〜E14、C01〜C14、S01〜S08で再監査し、記事側の公開ブロッカーはなし。ユーザー側の横断確認事項は `USER_ACTION_ITEMS.md` で継続管理する。
