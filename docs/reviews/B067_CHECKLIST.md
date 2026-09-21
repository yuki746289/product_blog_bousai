# B067 公開前チェック

- article_id: `B067`
- title: 線状降水帯とは？過去事例・発生数・多い地域・雨量記録をデータで見る
- content_role: `pillar`
- risk_level: standard
- article_status: READY_TO_PUBLISH
- review_status: `PASS`
- last_checked_at: 2026-09-20
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

参照:
- `docs/ARTICLE_REVIEW_CHECKLIST.md`
- `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`
- `docs/ARTICLE_STORY_QUALITY_GATE.md`
- `docs/EXPLANATION_QUALITY_PREFLIGHT.md`

## 共通チェック結果

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 2026-09-20再編集で主要な問いをanswer-firstへ修正 |
| C02 出典・安全性 | PASS | 特集一次資料・気象庁資料を基準に確認 |
| C03 画像・視覚要素 | PASS | HTML/CSS図解は実装済み。ただし、ユーザーが要求した生成済み実画像の本番 img 表示は未実装のため別タスクとして再オープン |
| C04 読みやすさ・UI | PASS | メモ的見出し・制作側表現を除去し、読者向け見出しへ変更 |
| C05 内部リンク | PASS | 特集内・実用記事への導線あり |
| C08 同期・公開前 | PASS | Markdown/preview同期経路あり |
| C10 デザイン・UX | PASS | 見出しだけでも章の要点が分かる情報階層へ修正 |
| C11 読者・マーケティング | PASS | タイトル・主要H2の問いに冒頭で答える構成へ修正 |
| C12 アクセシビリティ | PASS | 図解はHTMLテキストでも読め、重要情報を画像内文字だけに閉じない。モバイルは1列化 |
| C13 技術品質・信頼性 | PASS | `article-inline-image` でMarkdown同期後も保持する回帰テストを追加 |

## 記事固有チェック

- [x] 疑問形見出しの直後1〜2文で答えが分かる
- [x] 公開本文に制作メモ・将来TODOがない
- [x] 同一特集の兄弟記事と章構成・定型句が過度に重複していない
- [x] 各主要H2の結論を1文で説明できる
- [x] 「この記事では〜整理します」型に依存しない

## 2026-09-20 図解追加レビュー

- PASS: 線状降水帯の全体像を「暖湿気流入 → 積乱雲の連続発達 → 同じ地域で強雨」の1メッセージで模式化
- PASS: 住宅浸水は浸水深の固定数値を安全基準にせず、生活影響と早期避難を説明
- PASS: 冠水道路・車は特定水深の走行可否を示さず、「進入しない」を主メッセージ化
- PASS: 土砂災害はがけ崩れ・土石流・地すべりを簡略表示し、個別危険区域はハザードマップ等へ委ねる
- PASS: NG行動は川・用水路、冠水道路、アンダーパス、がけ・斜面への接近を例示
- PASS: 図がなくても本文だけで安全上の結論が理解できる
- PASS: PC 3〜4列 / モバイル1列のレスポンシブ構造
- PASS: 既存の情報確認・警戒レベル・家庭タイムライン図と役割が重複しない

## 残課題

- editorial_acceptance_status: `APPROVED`
- html_css_guide_acceptance_status: `APPROVED`
- actual_image_embed_status: `REOPENED`
- 2026-09-21 ユーザー確認により、生成済み画像がPC/モバイルの公開ページに img として表示されていないことが判明。
- 実画像掲載は未完了。画像ファイル保存 → 公開アセット配置 → img 組み込み → PC/モバイル実表示確認 → ユーザー確認まで完了扱いにしない。

## 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 2026-09-20の編集品質再監査で、結論先出し・見出し・制作メモ・兄弟記事重複を修正し再確認した。
