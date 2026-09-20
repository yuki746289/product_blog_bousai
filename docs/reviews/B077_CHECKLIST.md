# B077 公開前チェック

- article_id: `B077`
- title: 東海の線状降水帯｜2023年6月豪雨・2025年静岡・2026年伊豆から見る特徴
- content_role: `detail`
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
| C01 内容・情報量 | PASS | 地域固有の事例・特徴を主軸に再構成 |
| C02 出典・安全性 | PASS | 一次資料・公的資料を基準に確認 |
| C03 画像・視覚要素 | PASS | 重要情報を画像だけに閉じない |
| C04 読みやすさ・UI | PASS | 定型的な地域記事見出しを地域固有の結論へ変更 |
| C05 内部リンク | PASS | 関連記事導線あり |
| C08 同期・公開前 | PASS | Markdown/preview同期経路あり |
| C10 デザイン・UX | PASS | 見出しで地域固有の差が分かる構成へ修正 |
| C11 読者・マーケティング | PASS | 読者が自地域の危険へ落とし込める流れへ修正 |
| C12 アクセシビリティ | PASS | 重要情報をテキストでも保持 |
| C13 技術品質・信頼性 | PASS | 現行ビルド・テスト対象 |

## 記事固有チェック

- [x] タイトルの約束を冒頭で回収している
- [x] 各主要H2の結論を1文で説明できる
- [x] 公開本文に制作メモ・将来TODOがない
- [x] 兄弟記事との差が明確
- [x] 定型導入の使い回しに依存していない

## 残課題

- 住宅浸水・冠水車・土砂災害等の追加図解は `docs/research/LINEAR_RAINBAND_BACKLOG_20260920.md` で別管理。本文の公開可否を妨げない。

## 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 2026-09-20の編集品質再監査で、地域固有の事例・見出し・結論へ再構成し、兄弟記事のテンプレ感を解消した。
