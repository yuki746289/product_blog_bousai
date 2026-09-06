# B020 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B020`
- title: 大雨の前に自宅で確認すること｜浸水対策チェックリスト
- content_role: `practical`
- risk_level: `elevated`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-04
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

## 1. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 記事役割に必要な判断条件・例外・安全行動・次アクションを満たす |
| C02 出典・安全性 | PASS | 3件。気象庁・ハザードマップ・国交省正式版ガイドラインを2026-09-04再確認 |
| C03 画像・視覚要素 | PASS | 既存の日本文脈・権利・関連性レビューを継承。画像を安全判断の根拠にしない |
| C04 読みやすさ・UI | PASS | 表・手順・チェックリスト・注意枠を既存UIで整理 |
| C05 内部リンク | PASS | 同一クラスタの基礎/詳細/被災後記事とQ&Aへ文脈接続 |
| C06 商品導線・商品記事 | PASS | 文脈に沿う内部商品ガイドのみ。安全・避難情報より後段に配置 |
| C07 Q&A | PASS | 本文説明を残した上で個別Q&Aへ補助導線を配置 |
| C08 同期・公開前 | PASS | article/source/preview/registry/checklistを2026-09-04監査へ同期 |
| C09 日付・構造化データ | PASS | registryの日付を正本としてproduction buildへ反映 |
| C10 デザイン・UX | PASS | 既存共通UIを利用し、安全情報と商品導線の役割を分離 |
| C11 読者・マーケティング | PASS | 不安を煽らず、平時準備・安全行動・公的情報確認を次アクションにする |
| C12 アクセシビリティ | PASS | 色依存なし。見出し・表・リンクテキストで意味を伝達 |
| C13 技術品質・信頼性 | PASS | production build/test/smoke対象 |
| C14 計測・グロース | N/A | 計測変更なし |

## 2. 防災サイト固有チェック

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| S01 適用判定 | PASS | E01〜E08,E11〜E14を適用。E09を条件適用 |
| S02 情報設計 | PASS | pillar/practical/detailの役割を維持し、近接記事との重複を抑制 |
| S03 法務・権利等 | PASS | 公的情報とサイト解説を分け、保険・設備・管理責任を一律断定しない |
| S04 ブランド・トーン | PASS | 安全→判断→準備の順。恐怖訴求や購買誘導を優先しない |
| S05 日本向け文脈 | PASS | 気象庁・国交省・内閣府・損保協会等の国内一次情報中心 |
| S06 運用・ガバナンス | PASS | staleなREVIEW_REQUIREDを解消し、出典・台帳・previewを同期 |
| S07 セキュリティ・外部依存 | PASS | 公的・業界公式リンク中心。新規外部機能なし |
| S08 数値 | PASS | 目安・備蓄期間・対策効果を安全保証として扱わない |

## 3. 安全誤認防止確認

- PASS: 3〜7日前等は目安であり危険時に作業継続させない
- PASS: 簡易水防を深い浸水対策として過信させない
- PASS: 冠水後の側溝清掃・電気操作・車移動を促さない
- PASS: 商品リンクは備蓄説明後に限定

## 4. 読者・ページ設計

- target_reader: 日本国内で大雨・台風・浸水への家庭対応を確認したい一般生活者
- usage_context: 平常時の準備、予報悪化時、被災直後
- reader_problem: 家や物を守る作業と人の安全行動の優先順位が曖昧になりやすい
- reader_goal: 自宅条件に応じて、やること・やめること・次に確認する先を決める
- page_job: 大雨前の作業を時系列で整理し、危険が高まる前に屋外作業から避難判断へ切り替えさせる
- next_action: 数日前から排水・家財・備蓄を整え、当日は新規屋外作業をせず情報・避難判断へ切り替える

## 5. 証跡

- sources: `docs/research/B020_SOURCES.md`
- article: `content/articles/B020_home_heavy_rain_checklist.md`
- preview: `preview/article_b020.html`

## 6. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 2026-09-04時点の公的情報、安全表現、記事役割、内部導線、サイト固有チェックを再監査し、公開正本とレビュー状態を同期。
