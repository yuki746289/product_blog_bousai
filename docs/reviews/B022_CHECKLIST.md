# B022 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 説明品質プレフライト: `docs/EXPLANATION_QUALITY_PREFLIGHT.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B022`
- title: マンションの台風・水害対策｜戸建てとの違い
- content_role: `detail`
- risk_level: `elevated`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-08
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`
- explanation_quality_review: `PASS`

## 1. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 主要章を「結論→理由→具体的方法→条件/確認先」で再構成。本文約4,576字 |
| C02 出典・安全性 | PASS | 既存4件の公的情報を維持。高層マンション地下受変電設備の浸水リスク等を既存一次資料に基づき説明 |
| C03 画像・視覚要素 | PASS | 日本文脈の既存5画像を維持。画像を安全判断の根拠には使用しない |
| C04 読みやすさ・UI | PASS | 短いH2の乱立を減らし、表・チェックリスト・関連導線を維持 |
| C05 内部リンク | PASS | B010/B012/B004に加え、養生テープの文脈からB046へ自然に接続 |
| C06 商品導線・商品記事 | PASS | 既存の水・トイレ・電源商品ガイドへ文脈接続。窓用品は専用商品記事未作成のためAmazonへ直接誘導しない |
| C07 Q&A | PASS | 車退避・飲料水のQ&Aを本文説明の補助として維持 |
| C08 同期・公開前 | PASS | Markdown / preview / registry update / checklistを2026-09-08修正へ同期 |
| C09 日付・構造化データ | PASS | modified_at / review日をregistry update patchで2026-09-08へ更新 |
| C10 デザイン・UX | PASS | 安全判断を先、商品導線を後に配置。既存UIを維持 |
| C11 読者・マーケティング | PASS | 一般生活者が実際に取る行動順へ修正し、管理側と住民側の役割を分離 |
| C12 アクセシビリティ | PASS | 色依存なし。見出し・表・リンクテキストで意味を伝達 |
| C13 技術品質・信頼性 | PASS | production build / tests / smoke対象 |
| C14 計測・グロース | N/A | 計測変更なし |

## 2. 説明品質・生活者リアリティレビュー

適用:
- Q01 テクニカルライター / インストラクショナルデザイナー視点
- Q02 生活者UX / 行動リアリティ編集視点

| 指摘テーマ | 旧状態 | 修正後 |
|---|---|---|
| ベランダの物 | 「室内へ移すか安全に固定」だけ | 飛散による窓・人への危険を説明。室内移動を第一選択とし、移せない設備は取説・管理ルールに従う |
| 排水口 | 「平常時に掃除」だけ | ごみ・泥の詰まり→ベランダ滞水→サッシ側への浸水につながる因果を説明 |
| 窓際の家具 | 人を近づけない配置との因果が不明 | ガラス片・雨水による二次被害と、窓際へ作業に行く必要を減らす目的を説明 |
| テープ | 「テープ」が突然登場 | 「窓へ養生テープを貼る方法」という前提から説明し、限界を示してB046へ接続 |
| 共用部の土のう | 個人が設置する前提に読める | 共用部は管理会社・管理組合の運用確認が基本と明示。個人は専有部対策へ集中 |
| 避難判断 | 「自治体情報と建物条件」で抽象的 | 避難情報、想定浸水深、家屋倒壊等氾濫想定区域、高潮、土砂災害、建物防災計画を具体化 |
| 在宅避難 | 抽象的なチェック項目中心 | ごみ、携帯トイレ、オートロック、階段移動、要介護者・ペットまで生活場面へ展開 |

判定: **PASS**。単純な文字数増量ではなく、因果・方法・判断材料・生活者の行動順を補った。

## 3. 防災サイト固有チェック

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| S01 適用判定 | PASS | 既存専門家視点に加え説明品質Q01/Q02を適用 |
| S02 情報設計 | PASS | マンション固有の低層浸水・地下設備・高層生活停止へ整理 |
| S03 法務・権利等 | PASS | 公的情報とサイト解説を分離し、管理責任を一律断定しない |
| S04 ブランド・トーン | PASS | 恐怖訴求ではなく、理由と行動を具体的に説明 |
| S05 日本向け文脈 | PASS | 管理会社・管理組合、ハザードマップ等の日本の集合住宅文脈で説明 |
| S06 運用・ガバナンス | PASS | 新しい説明品質プレフライトのパイロット適用記事として証跡を記録 |
| S07 セキュリティ・外部依存 | PASS | 新規外部機能なし |
| S08 数値 | PASS | 階数等を独自の安全基準として断定していない |

## 4. 商品語・内部導線確認

- `養生テープ`: B046「台風の窓ガラス対策」へ本文中で接続。
- 現時点で「台風の窓対策用品」専用商品記事は存在しないため、B022からAmazonへ直接リンクしない。
- 将来、養生テープ・飛散防止フィルム等の商品記事を作る場合は、検索意図・商品選定価値を確認し、`AMAZON_WORK_PREFLIGHT.md` を実行してから実装する。
- 水・非常食、携帯トイレ、モバイルバッテリーは既存商品ガイドへ自然に接続。

## 5. 読者・ページ設計

- target_reader: 日本国内のマンション居住者で、台風・大雨前に自宅と建物の対策を確認したい人
- usage_context: 平常時の準備、大雨・台風予報時、避難判断時、被災後
- knowledge_level: 一般生活者。設備・防災制度の専門知識を前提にしない
- reader_problem: 自分で行う対策と管理会社が行う対策、低層と高層のリスク、避難判断の材料が分かりにくい
- reader_goal: 自宅階・建物設備・家族条件に合わせて、何を確認し何を先に行うか決める
- page_job: マンション特有の水害・停電・強風リスクを生活者の行動へ翻訳する
- next_action: ハザードマップ、管理会社の防災案内、ベランダ・窓、駐車場、給水・非常電源を確認する

## 6. 証跡

- sources: `docs/research/B022_SOURCES.md`
- article: `content/articles/B022_apartment_typhoon_flood.md`
- preview: `preview/article_b022.html`
- explanation rule: `docs/EXPLANATION_QUALITY_PREFLIGHT.md`
- registry patch: `data/content_registry_updates_20260908.json`

## 7. 本文量

- reader_visible_char_count: **4,576字**
- role: `detail`
- standard_guideline: 2,500〜3,500字程度
- length_status: **PASS_EDITORIAL_EXCEPTION_ABOVE_GUIDELINE**
- counting_method: frontmatter・URL・Markdown記号・公的情報/出典一覧を除く、読者可視の非空白文字。
- exception_reason: 全体文字数の上限目安は超えるが、マンション固有の「ベランダ・窓・低層浸水・地下駐車場・高層停電断水・避難判断」の別論点を具体化した結果であり、同義反復による水増しではない。

## 8. 最終判定

- review_status: `PASS`
- explanation_quality_review: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 説明不足・抽象表現・生活者として不自然な行動を修正し、主要章で理由・具体的方法・確認先を読者が追える状態にした。
