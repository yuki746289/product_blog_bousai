# B073 公開前チェック

- article_id: `B073`
- title: 九州の線状降水帯｜なぜ多い？九州北部豪雨など過去事例と大雨への備え
- content_role: `detail`
- risk_level: HIGH
- article_status: published
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
| C01 内容・情報量 | PASS | 地域固有の事例・特徴を主軸に再構成 |
| C02 出典・安全性 | PASS | 特集一次資料・気象庁資料を基準に確認 |
| C03 画像・視覚要素 | PASS | 図解方針は別バックログで管理 |
| C04 読みやすさ・UI | PASS | 定型的な地域記事見出しを地域固有の結論へ変更 |
| C05 内部リンク | PASS | 特集内・実用記事への導線あり |
| C08 同期・公開前 | PASS | Markdown/preview同期経路あり |
| C10 デザイン・UX | PASS | 見出しで地域固有の差が分かる構成へ修正 |
| C11 読者・マーケティング | PASS | 読者が自地域の危険へ落とし込める流れへ修正 |
| C12 アクセシビリティ | PASS | 重要情報を画像だけに閉じない |
| C13 技術品質・信頼性 | PASS | 現行ビルド・テスト対象 |

## 記事固有チェック

- [x] 疑問形見出しの直後1〜2文で答えが分かる
- [x] 公開本文に制作メモ・将来TODOがない
- [x] 同一特集の兄弟記事と章構成・定型句が過度に重複していない
- [x] 各主要H2の結論を1文で説明できる
- [x] 「この記事では〜整理します」型に依存しない

## 残課題

- 住宅浸水・冠水車・土砂災害等の追加図解は `docs/research/LINEAR_RAINBAND_BACKLOG_20260920.md` で別管理。本文の公開可否を妨げない。

## 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 2026-09-20の編集品質再監査で、地域固有の事例・見出し・結論へ再構成し、兄弟記事のテンプレ感を解消した。
