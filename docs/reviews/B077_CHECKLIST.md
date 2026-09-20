# B077 公開前チェック

- article_id: `B077`
- title: 東海の線状降水帯｜2023年6月豪雨・2025年静岡・2026年伊豆から見る特徴
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
| C01 内容・情報量 | FAIL | 注意事項の列挙感を減らし、太平洋側の暖湿気と県内対象地域の移動を主軸にする。 |
| C02 出典・安全性 | PASS | 一次資料・公的資料を基準に確認 |
| C03 画像・視覚要素 | PASS | 重要情報を画像だけに閉じない |
| C04 読みやすさ・UI | FAIL | 編集品質再監査の修正対象 |
| C05 内部リンク | PASS | 関連記事導線あり |
| C08 同期・公開前 | PASS | Markdown/preview同期経路あり |
| C10 デザイン・UX | FAIL | 情報階層を再編集する |
| C11 読者・マーケティング | FAIL | 読者の問いへの即答性を改善する |
| C12 アクセシビリティ | PASS | 重要情報をテキストでも保持 |
| C13 技術品質・信頼性 | PASS | 現行ビルド・テスト対象 |

## 記事固有チェック

- [ ] タイトルの約束を冒頭で回収している
- [ ] 各主要H2の結論を1文で説明できる
- [ ] 公開本文に制作メモ・将来TODOがない
- [ ] 兄弟記事との差が明確
- [ ] 定型導入の使い回しに依存していない

## 残課題

- 注意事項の列挙感を減らし、太平洋側の暖湿気と県内対象地域の移動を主軸にする。

## 最終判定

- review_status: `FIX_REQUIRED`
- READY_TO_PUBLISH: `NO`
- 判定理由: 編集品質再監査で修正が必要。
