# B067 公開前チェック

- article_id: `B067`
- title: 線状降水帯とは？過去事例・発生数・多い地域・雨量記録をデータで見る
- content_role: `pillar`
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
| C01 内容・情報量 | PASS | 2026-09-20再編集で主要な問いをanswer-firstへ修正 |
| C02 出典・安全性 | PASS | 特集一次資料・気象庁資料を基準に確認 |
| C03 画像・視覚要素 | PASS | 図解方針は別バックログで管理 |
| C04 読みやすさ・UI | PASS | メモ的見出し・制作側表現を除去し、読者向け見出しへ変更 |
| C05 内部リンク | PASS | 特集内・実用記事への導線あり |
| C08 同期・公開前 | PASS | Markdown/preview同期経路あり |
| C10 デザイン・UX | PASS | 見出しだけでも章の要点が分かる情報階層へ修正 |
| C11 読者・マーケティング | PASS | タイトル・主要H2の問いに冒頭で答える構成へ修正 |
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
- 判定理由: 2026-09-20の編集品質再監査で、結論先出し・見出し・制作メモ・兄弟記事重複を修正し再確認した。
