# B004 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B004`
- title: 停電に備えて準備しておきたいもの｜照明・電源・情報収集を分けて考える
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
| C01 内容・情報量 | PASS | 照明・情報・連絡・充電・生活維持をpillarとして整理し、医療機器・復電火災も扱う |
| C02 出典・安全性 | PASS | 内閣府の現行2026情報に加え、消費者庁の非常用電源・通電火災注意を再確認 |
| C03 画像・視覚要素 | PASS | 既存画像の日本文脈・権利・重複レビュー済み。安全判断の根拠にしない |
| C04 読みやすさ・UI | PASS | 5役割、機器表、10分チェック、実行章に分割 |
| C05 内部リンク | PASS | B003/B024/B002へ接続。B024とは一般停電pillar/地震後複合停止で分離 |
| C06 商品導線・商品記事 | PASS | ライト・電源・水/トイレの内部商品比較を該当説明後に配置し、購入を結論にしない |
| C07 Q&A | PASS | 停電準備Q&Aへ本文説明後の補助導線として接続 |
| C08 同期・公開前 | PASS | source/articleを2026-09-04監査へ更新。registry同期を実施 |
| C09 日付・構造化データ | PASS | registry管理の日付・既存構造化データ生成を使用 |
| C10 デザイン・UX | PASS | 既存共通UI内の表・画像・Q&A・商品導線。新規独自UIなし |
| C11 読者・マーケティング | PASS | 「大容量電源購入」より用途棚卸しを先にして過剰購入誘導を防止 |
| C12 アクセシビリティ | PASS | 色依存なし。表・リスト・テキストで情報を完結 |
| C13 技術品質・信頼性 | PASS | 既存production build/test対象。通常CIで最終検証 |
| C14 計測・グロース | N/A | 計測変更なし |

## 2. 防災サイト固有チェック

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| S01 適用判定 | PASS | 商品導線があるためE09を含めE01〜E09,E11〜E14適用 |
| S02 情報設計 | PASS | B004=停電一般pillar、B024=地震後停電/断水detail。目的と検索意図を分離 |
| S03 法務・権利等 | PASS | 画像権利記録あり。製品を公的推奨・必須品のように見せない |
| S04 ブランド・トーン | PASS | 不安訴求より停電時の役割分解と実行可能性を優先 |
| S05 日本向け文脈 | PASS | 内閣府の備蓄・感震ブレーカー、消費者庁の通電火災情報に準拠 |
| S06 運用・ガバナンス | PASS | staleなREVIEW_REQUIREDを解消し、出典確認を2026-09-04へ更新 |
| S07 セキュリティ・外部依存 | PASS | 新規外部JS/APIなし。公的リンクのみ追加 |
| S08 数値 | PASS | 電源容量を一律推奨せず、必要負荷・時間を商品記事へ分離 |

## 3. 安全・誤認防止確認

- PASS: ポータブル電源を停電対策の必須品としない。
- PASS: 医療機器への外部電源適合をサイト独自に保証しない。
- PASS: 感震ブレーカーだけで地震火災を完全防止できるとしない。
- PASS: 浸水・焦げ・配線損傷等がある場合に何度も通電を試させない。
- PASS: 冷蔵食品を見た目・時間だけで安全と断定しない。
- PASS: 模擬停電は医療機器・冷蔵庫等を無理に停止させない安全な範囲に限定。

## 4. 読者・ページ設計

- target_reader: 台風・地震等による停電へ家庭で備えたい生活者
- usage_context: 平常時の準備〜停電予測時
- reader_problem: 何を買うかから考え、照明・通信・生活維持の優先順位が曖昧
- reader_goal: 家庭で止まる機能を棚卸しし、必要な備えだけ選ぶ
- page_job: 停電クラスタのpillar
- next_action: ライト/通信/充電確認→個別機器確認→必要に応じ商品比較/B024へ分岐

## 5. 証跡

- sources: `docs/research/B004_SOURCES.md`
- article: `content/articles/B004_blackout_preparedness.md`
- preview: `preview/article_b004.html`
- public_path: `blackout/blackout-preparedness.html`

## 6. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 一般停電pillarとして用途分解・安全優先・商品導線・通電火災の現行根拠を再確認し、旧レビューの未完了状態を解消。
