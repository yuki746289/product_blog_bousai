# B018 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B018`
- title: 地震で車が壊れた場合、自動車保険はどう考える？
- content_role: `detail`
- risk_level: `elevated`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-04
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

## 1. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 原因区分、通常車両保険、地震等特約、安全確保、記録、ローン/リースまで整理 |
| C02 出典・安全性 | PASS | 日本損害保険協会の現行自動車保険Q&A・自然災害情報・2026年熊本地震案内を再確認 |
| C03 画像・視覚要素 | PASS | 国内津波被災車画像の用途を関連章に限定し、補償・修理可否の根拠にしない |
| C04 読みやすさ・UI | PASS | 原因別表、平常時確認、時系列記録で手続きを整理 |
| C05 内部リンク | PASS | B017/B008/B011へ接続し、住宅地震保険・水没安全・洪水車両保険と分離 |
| C06 商品導線・商品記事 | N/A | 保険商品販売・比較・見積もり導線なし |
| C07 Q&A | N/A | 本文と業界情報で主要疑問を完結 |
| C08 同期・公開前 | PASS | source/article/registryを2026-09-04監査へ同期 |
| C09 日付・構造化データ | PASS | registryのsource_checked_atと既存生成機構を使用 |
| C10 デザイン・UX | PASS | 既存共通UI、表・画像・リスト中心。新規独自UIなし |
| C11 読者・マーケティング | PASS | 特約加入を煽らず「車を失った時の家計影響」で判断軸を提示 |
| C12 アクセシビリティ | PASS | 画像に依存せず本文・表・見出しで判断可能 |
| C13 技術品質・信頼性 | PASS | 正本同期ワークフロー内unittest PASS。通常CIでも再検証対象 |
| C14 計測・グロース | N/A | 計測変更なし |

## 2. 防災サイト固有チェック

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| S01 適用判定 | PASS | E01〜E08,E11〜E14適用。保険販売をしないためE09はN/A |
| S02 情報設計 | PASS | B018=地震由来車損害、B011=台風/洪水水没、B017=住宅/家財地震保険と明確に分離 |
| S03 法務・権利等 | PASS | 一般的な免責・特約を説明し、個別契約の支払可否を断定しない |
| S04 ブランド・トーン | PASS | 車両保全より人の避難を優先し、特約を万能補償と見せない |
| S05 日本向け文脈 | PASS | 日本損害保険協会の現行商品体系・2026年災害案内に準拠 |
| S06 運用・ガバナンス | PASS | 古いREVIEW_REQUIREDとsource_checked_atを同期 |
| S07 セキュリティ・外部依存 | PASS | 業界リンクのみ。新規外部機能なし |
| S08 数値 | PASS | 特約の金額・条件を商品共通の一律値にせず、約款確認を促す |

## 3. 保険・安全誤認防止確認

- PASS: 通常の車両保険では地震・噴火・これらによる津波が主な免責であることを確認。
- PASS: 地震等特約が存在しても、通常の車両保険同様の修理費全額払いとは断定しない。
- PASS: 台風・洪水・高潮による水没と地震津波による水没を同一扱いにしない。
- PASS: 住宅の地震保険に自動車を含めない。
- PASS: 津波警報後に車を守るため低地・海側へ戻らせない。
- PASS: 津波・浸水車を点検前に始動させない。
- PASS: EV/PHEV/HVの高電圧系統へ自己判断で触れさせない。
- PASS: 2026年熊本地震に関する損保協会案内の存在・時点を再確認。

## 4. 読者・ページ設計

- target_reader: 地震・津波で車が損傷した場合の保険を確認したい車所有者
- usage_context: 平常時の契約確認〜被災後の事故連絡
- reader_problem: 車両保険に入っていれば地震損害も出ると思いやすい
- reader_goal: 原因区分、特約、安全確保、記録方法を把握する
- page_job: 地震による車両損害の保険detail記事
- next_action: 証券で地震等特約・支払条件を確認し、被害時は安全な場所から契約先へ連絡

## 5. 証跡

- sources: `docs/research/B018_SOURCES.md`
- article: `content/articles/B018_earthquake_car_insurance.md`
- preview: `preview/article_b018.html`
- public_path: `insurance/earthquake-car-insurance.html`
- registry: 2026-09-04同期

## 6. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 現行の車両保険免責・地震等特約を再確認し、安全確保と個別契約確認を優先する構成に問題なし。
