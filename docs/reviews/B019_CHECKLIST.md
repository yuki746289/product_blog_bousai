# B019 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B019`
- title: 水害・台風・地震で保険の扱いはどう違う？
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
| C01 内容・情報量 | PASS | 災害名ではなく原因→対象→契約→条件の順で整理し、詳細は専用記事へ分岐。pillarとして必要十分 |
| C02 出典・安全性 | PASS | 日本損害保険協会の自然災害・火災・地震・自動車保険・修理トラブル情報を2026-09-04再確認 |
| C03 画像・視覚要素 | PASS | 日本国内被災画像の既存権利/関連性レビュー済み。補償可否の根拠にしない |
| C04 読みやすさ・UI | PASS | 住宅/車マトリクス、手順、年1回確認表で短時間に俯瞰可能 |
| C05 内部リンク | PASS | B013/B016/B017/B011へ原因別に分岐 |
| C06 商品導線・商品記事 | N/A | 保険商品販売・見積もり誘導なし |
| C07 Q&A | N/A | 総論として本文と詳細記事リンクで完結 |
| C08 同期・公開前 | PASS | source/articleを2026-09-04監査へ更新。registry同期を実施 |
| C09 日付・構造化データ | PASS | registry管理の日付と既存構造化データ生成を使用 |
| C10 デザイン・UX | PASS | 比較表中心で総論向け。新規独自UIなし |
| C11 読者・マーケティング | PASS | 特定保険加入を煽らず、証券棚卸しと詳細確認へ誘導 |
| C12 アクセシビリティ | PASS | 色依存なし。表・手順・リンクテキストで情報を伝達 |
| C13 技術品質・信頼性 | PASS | 既存production build/test対象。通常CIで最終検証 |
| C14 計測・グロース | N/A | 計測変更なし |

## 2. 防災サイト固有チェック

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| S01 適用判定 | PASS | E01〜E08,E11〜E14適用。保険販売をしないためE09はN/A |
| S02 情報設計 | PASS | B019=保険総論pillar、B013=水災、B016=風災、B017=地震、B011=車水没へ分岐。過剰な詳細重複を避ける |
| S03 法務・権利等 | PASS | 一般的な補償体系を説明し、個別契約の支払可否・保険金額を断定しない |
| S04 ブランド・トーン | PASS | 「保険で無料」等の誤認を抑え、契約確認を優先 |
| S05 日本向け文脈 | PASS | 日本損害保険協会の現行商品体系・修理トラブル注意に準拠 |
| S06 運用・ガバナンス | PASS | staleなREVIEW_REQUIREDを解消し、source_checked_atを2026-09-04へ更新 |
| S07 セキュリティ・外部依存 | PASS | 業界公式リンクのみ。新規外部機能なし |
| S08 数値 | PASS | 地震保険30〜50%など必要最小限のみ提示し詳細はB017へ分離 |

## 3. 保険・安全誤認防止確認

- PASS: 「台風なら火災保険」「水没なら車両保険」と災害名だけで断定しない。
- PASS: 火災保険が自然災害すべてを自動補償するとしない。
- PASS: 風災・水災・地震/津波を原因別に分ける。
- PASS: 建物・家財・車を契約対象として分ける。
- PASS: 台風/洪水車両損害と地震/津波車両損害を同一視しない。
- PASS: 修理業者の「保険で無料」勧誘では、契約前に加入先保険会社・代理店へ相談する現行注意喚起と整合。
- PASS: 写真記録のため危険場所へ戻らせない。

## 4. 本文量判定の見直し

旧チェックリストでは約1,760字を理由に `content_depth=FAIL` としていたが、新フレームワークでは**文字数を目的化しない**。本記事の役割は詳細解説ではなく、原因・対象・保険種別を短時間で整理してB013/B016/B017/B011へ分岐させるpillarである。現状はこのpage_jobを満たしており、詳細を追加して各記事と重複させる必要はないためPASSとする。

## 5. 読者・ページ設計

- target_reader: 災害別にどの保険を確認すべきか分からない一般契約者
- usage_context: 平常時の証券棚卸し、災害後の初期確認
- reader_problem: 災害名だけで補償の有無を判断しやすい
- reader_goal: 原因・対象・契約を切り分け、該当詳細記事へ進む
- page_job: 保険クラスタの短い総論pillar
- next_action: 火災/地震/自動車の証券を集め、原因別詳細記事へ進む

## 6. 証跡

- sources: `docs/research/B019_SOURCES.md`
- article: `content/articles/B019_disaster_insurance_overview.md`
- preview: `preview/article_b019.html`
- public_path: `insurance/disaster-insurance-overview.html`

## 7. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 保険総論としての役割、現行補償体系、安全導線、修理勧誘注意を再確認し、旧文字数基準による誤ったFAILを解消。
