# B007 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B007`
- title: 地震に備えて最初に確認したいこと
- content_role: `pillar`
- risk_level: `elevated`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-04
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

## 1. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 揺れる前・最中・後、家具、津波、停電断水、家族連絡までpillarとして整理 |
| C02 出典・安全性 | PASS | 気象庁・消防庁・内閣府の現行一次情報を再照合。津波・大地震後活動も直接出典化 |
| C03 画像・視覚要素 | PASS | 関連性再レビュー済み。画像を安全判断の根拠にしない |
| C04 読みやすさ・UI | PASS | 行動順、表、箇条書き、関連記事で長文を分割 |
| C05 内部リンク | PASS | B023/B024/B017/B030へ役割分担して接続 |
| C06 商品導線・商品記事 | PASS | 水・トイレ・ライト・電源の内部商品比較のみ。安全説明後に配置し購入を結論にしない |
| C07 Q&A | N/A | 本記事はpillar本文と関連記事で主要疑問を処理 |
| C08 同期・公開前 | PASS | source/research/article/registryを2026-09-04監査へ同期 |
| C09 日付・構造化データ | PASS | registry管理の公開日・更新日・情報確認日と既存生成機構を使用 |
| C10 デザイン・UX | PASS | 既存共通UI内のテキスト・表・画像のみ。新規独自UIなし |
| C11 読者・マーケティング | PASS | 「何から始めるか」に対し室内安全→生活継続→関連詳細の順で次行動を提示 |
| C12 アクセシビリティ | PASS | 色依存なし。既存見出し・リスト・共通アクセシビリティ実装を使用 |
| C13 技術品質・信頼性 | PASS | 正本同期ワークフロー内の全unittest PASS。通常CIでも再検証対象 |
| C14 計測・グロース | N/A | 新規計測変更なし |

## 2. 防災サイト固有チェック

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| S01 適用判定 | PASS | E01〜E09,E11〜E14を適用。商品内部導線があるためE09も確認 |
| S02 情報設計 | PASS | B007=地震pillar、B023=家具、B024=地震後ライフライン、B017=保険と役割分離 |
| S03 法務・権利等 | PASS | 公的出典・既存画像権利記録を維持。商品を公的推奨のように表示しない |
| S04 ブランド・トーン | PASS | 恐怖訴求ではなく行動優先。地震予知等を断定しない |
| S05 日本向け文脈 | PASS | 気象庁・消防庁・内閣府の日本向け現行案内に準拠 |
| S06 運用・ガバナンス | PASS | Markdownの古いREVIEW_REQUIREDを解消し、registry・source_checked_at・source_idsを同期 |
| S07 セキュリティ・外部依存 | PASS | 公的リンクと既存画像のみ。新規外部JS/APIなし |
| S08 数値 | PASS | 3日〜1週間は公的根拠。地震予測の独自数値・安全閾値なし |

## 3. 高リスク・誤判断防止確認

- PASS: 揺れ中は火元へ走らず、まず身の安全を確保する。
- PASS: 海岸付近で強い揺れ・長くゆっくりした揺れを感じた場合は、津波警報待ちを前提にしない。
- PASS: 「地震が来たら必ず外へ出る」と固定しない。
- PASS: 感震ブレーカーを設置しただけで地震火災対策完了としない。
- PASS: 大地震後の具体的な日時・場所を予測できるように表現しない。
- PASS: 建物耐震性と家具固定を代替関係にしない。

## 4. 読者・ページ設計

- target_reader: 地震対策を何から始めるか分からない一般家庭
- usage_context: 平常時の準備〜地震直後の基本確認
- reader_problem: 備蓄品購入に偏り、室内安全・避難・ライフライン対策の優先順位が分からない
- reader_goal: 最初の行動と次に読む詳細記事を把握する
- page_job: 地震クラスタの入口となるpillar
- next_action: 寝室・出口確認→家族ルール→B023/B024等の詳細対策

## 5. 証跡

- sources: `docs/research/B007_SOURCES.md`
- article: `content/articles/B007_earthquake_preparedness_basics.md`
- preview: `preview/article_b007.html`
- public_path: `earthquake/earthquake-preparedness-basics.html`
- registry: 2026-09-04同期

## 6. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 一次情報・安全表現・情報設計・商品導線・正本同期まで再監査し、重大な矛盾なし。
