# SEOメタデータ横断監査 2026-09-03

対象: 本番公開対象50 HTML

## 監査前

- titleあり: 50 / 50
- meta descriptionあり: 4 / 50
- meta descriptionなし: 46 / 50
- title完全重複: 0件確認
- 主な問題: description未設定が大半

## 対応

- 46ページへ固有meta descriptionを追加
- 既存4ページも内容整合を確認
- B002 title/H1を「防災リュック 中身・最低限・重さ・置き場所」へ調整
- B003 title/H1を「使い方・処分・衛生」を主軸へ変更
- 携帯トイレ商品ページは「商品選び・回数別比較」へ役割分離
- B026 title/H1を「何日分・3日〜1週間・ローリングストック」へ調整
- build_public.pyへtitle/meta descriptionの欠落・完全重複検証を追加
- tests/test_public_build.pyへ同検証を追加

## 完了条件

GitHub Actionsで本番ビルド・テストがPASSし、公開50 HTMLすべてでtitle/meta descriptionが存在し完全重複がないこと。
