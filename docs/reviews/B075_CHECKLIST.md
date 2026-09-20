# B075 公開前チェック

- article_id: `B075`
- title: 中国地方の線状降水帯｜2014年広島・2018年西日本豪雨・2025年山口から見る特徴
- content_role: `detail`
- risk_level: HIGH
- article_status: published
- review_status: `FIX_REQUIRED`
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
| C01 内容・情報量 | FAIL | 他地域記事と似た注意書き構成を、中国地方固有の事例比較へ再構成する。 |
| C02 出典・安全性 | PASS | 特集一次資料・気象庁資料を基準に確認 |
| C03 画像・視覚要素 | PASS | 図解方針は別バックログで管理 |
| C04 読みやすさ・UI | FAIL | 編集品質再監査の修正対象 |
| C05 内部リンク | PASS | 特集内・実用記事への導線あり |
| C08 同期・公開前 | PASS | Markdown/preview同期経路あり |
| C10 デザイン・UX | FAIL | 見出しと情報階層を再編集する |
| C11 読者・マーケティング | FAIL | 読者の問いへの即答性を改善する |
| C12 アクセシビリティ | PASS | 重要情報を画像だけに閉じない |
| C13 技術品質・信頼性 | PASS | 現行ビルド・テスト対象 |

## 記事固有チェック

- [ ] 疑問形見出しの直後1〜2文で答えが分かる
- [ ] 公開本文に制作メモ・将来TODOがない
- [ ] 同一特集の兄弟記事と章構成・定型句が過度に重複していない
- [ ] 各主要H2の結論を1文で説明できる
- [ ] 「この記事では〜整理します」型に依存しない

## 残課題

- 他地域記事と似た注意書き構成を、中国地方固有の事例比較へ再構成する。

## 最終判定

- review_status: `FIX_REQUIRED`
- READY_TO_PUBLISH: `NO`
- 判定理由: 編集品質再監査で修正が必要。
