# 非記事ページ横断レビュー

更新日: 2026-09-04

## 1. 対象

本記録は、記事 B001〜B037 以外の主要公開面を `docs/BOUSAI_SITE_REVIEW_PROFILE.md`、`docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`、`docs/EXPERT_REVIEW_FRAMEWORK.md` に基づいて横断監査した結果を記録する。

対象:

- トップページ
- カテゴリページ 10種
  - 防災入門
  - 台風
  - 大雨・水害
  - 地震
  - 車と災害
  - 住宅と災害
  - 保険・お金
  - 防災グッズ
  - 停電・断水
  - 被災後・復旧
- Q&A
- 固定ページ
  - 運営方針
  - 免責事項
  - プライバシーポリシー
  - 広告について
- 商品比較ページ 4種
  - 水・非常食
  - 携帯トイレ・衛生用品
  - ライト・ラジオ
  - ポータブル電源
- トップページのリアルタイム防災情報
- 共通 CSS / JavaScript / ナビゲーション / アクセシビリティ / GA4導線計測

persona_mode は記事と同じく `SITUATIONAL_SEGMENT` とし、架空の詳細ペルソナは作成しない。

## 2. ページ群別判定

| ページ群 | 主な役割 | 判定 | 主な確認事項 |
|---|---|---|---|
| トップ | 全体入口、現在情報、主要導線 | PASS | 公的情報優先、カテゴリ分岐、ピックアップ、リアルタイム失敗時の安全表示 |
| カテゴリ 10種 | 情報アーキテクチャ、記事発見 | PASS | H1/説明、入口記事、用途別まとまり、関連カテゴリ、孤立回避 |
| Q&A | 疑問起点の入口 | PASS | 短い回答→詳細記事。概要であることを明記し、重要判断は公式・詳細情報へ接続 |
| 固定ページ | 信頼・法務・透明性 | PASS | 運営方針、免責、GA4、広告/アフィリエイトの実装との整合 |
| 防災グッズカテゴリ | 情報→商品比較への分岐 | PASS | 商品比較を情報記事と区別し、購入導線を安全情報より前へ出さない |
| 商品比較 4ページ | 選び方・比較・Amazon導線 | PASS_WITH_FOLLOW_UP | 用途→判断基準→商品。U09の商品画像利用条件確認は継続 |
| リアルタイム情報 | JMA公開データの参考表示 | PASS | 取得失敗を「警報なし・台風なし」と表示しない。部分取得時に古い欄を最新取得時刻として扱わない |
| 共通UI | ナビ・アクセシビリティ・計測 | PASS | skip link、aria-current、breadcrumb、reduced motion、GA4クリック計測 |

## 3. E01〜E14 横断判定

| ID | 判定 | 結果 |
|---|---|---|
| E01 編集・コンテンツ戦略 | REQUIRED / PASS | ページ群ごとの役割を分離し、トップ・カテゴリ・Q&A・固定・商品比較が同じ役割になっていない |
| E02 防災・ファクトチェック・リスク | REQUIRED / PASS | 公的情報優先。リアルタイム取得失敗時の誤認経路を修正 |
| E03 SEO | REQUIRED / PASS | title/meta description、公開時noindex除去、カテゴリURL、内部リンク、sitemapをビルドで確認 |
| E04 情報アーキテクチャ | REQUIRED / PASS | 主要カテゴリ、関連カテゴリ、Q&A、商品比較の役割を分け、記事へ接続 |
| E05 UX/UI | REQUIRED / PASS | 結論・入口・用途別導線を優先。リアルタイムUIは独立パネルで過度に浮かせない |
| E06 マーケティング・読者戦略/CRO | REQUIRED / PASS | 安全理解→関連記事→必要時のみ商品比較/Amazonの順を維持 |
| E07 アクセシビリティ | REQUIRED / PASS | skip link、focus-visible、aria-current、breadcrumb、表領域、reduced motionを共通実装 |
| E08 ブランド/コンテンツデザイン | REQUIRED / PASS | 恐怖訴求・過剰な販売訴求を避け、公的情報とサイト要約を区別 |
| E09 商品/アフィリエイト | CONDITIONAL / PASS_WITH_FOLLOW_UP | 商品ページ・商品カテゴリのみ適用。U09を継続 |
| E10 分析/グロース | CONDITIONAL / PASS | `amazon_click` / `product_guide_click` を計測。実データ評価は U04〜U07 |
| E11 Web実装/信頼性 | REQUIRED / PASS | production build、JS syntax、link validation、FTPS、HTTP smokeで確認 |
| E12 セキュリティ/法務/権利/プライバシー | REQUIRED / PASS_WITH_FOLLOW_UP | GA4でリンクURL/文言を送る実装をprivacyへ明記。商品画像条件はU09 |
| E13 日本向けローカライゼーション | REQUIRED / PASS | 気象庁・自治体・日本の制度/保険/生活文脈を基準に構成 |
| E14 運用/ガバナンス | REQUIRED / PASS | 非記事ページの回帰要件を `tests/test_non_article_pages.py` へ追加 |

## 4. S01〜S08 横断判定

| ID | 判定 | 結果 |
|---|---|---|
| S01 サイトプロファイル/適用判定 | PASS | 非記事ページも防災サイトprofileを適用 |
| S02 IA/ファインダビリティ | PASS | カテゴリ、Q&A、関連カテゴリ、商品比較の役割を確認 |
| S03 法務/権利/広告/プライバシー | PASS_WITH_FOLLOW_UP | 広告表示、GA4説明を実装と同期。U09のみ継続 |
| S04 ブランド/トーン | PASS | 落ち着いた説明、過度な恐怖・購買誘導なし |
| S05 日本向け文脈 | PASS | 日本の公的情報・制度を優先 |
| S06 運用/ガバナンス | PASS | build/test/smokeと本監査記録を正本化 |
| S07 セキュリティ/外部依存 | PASS | 外部取得失敗を安全側へ表示し、secretを公開HTMLへ出さない |
| S08 数値/統計/リアルタイム | PASS | 取得失敗≠0件を明示。部分更新で古い欄を新しい取得時刻に見せない |

## 5. 今回の修正

### R01 リアルタイム取得失敗の誤認防止

修正前は、キャッシュ取得失敗時に `warnings.active_count=0`、`typhoons=[]` を仮置きしていたため、全体には取得失敗が表示されても個別欄で「確認されていません」と見える経路があった。

修正後:

- 取得不能は `warnings=null` / `typhoons=null`
- 警報欄は「情報を取得できていません」と表示
- 台風欄も「情報を取得できていません」と表示
- JMA直接更新が3系統すべて成功した場合のみ `checked_at` を現在時刻へ更新
- 部分成功では古いキャッシュ部分を「今取得した情報」のように扱わない

### R02 運営方針とリアルタイム機能の整合

「リアルタイム情報を配信するサイトではない」という旧説明を、トップページではJMA公開データを参考表示するが公式配信を代替しない、という現在の実装に合わせた。

### R03 GA4説明の透明性

`bousai_common.js` は `amazon_click` / `product_guide_click` で `link_url` / `link_text` / `page_path` を送信する。プライバシーポリシーを実装に合わせ、リンククリック・リンク先URL・リンク文言等をイベント情報として送信する場合があることを明記した。

### R04 Q&Aの役割明確化

Q&Aは短い回答だけで安全・制度・保険判断を完結させず、詳細記事と公式/契約先情報へ接続する入口であることを冒頭に明記した。

## 6. 恒久回帰チェック

`tests/test_non_article_pages.py` で以下を確認する。

- 全カテゴリ/固定/Q&A/商品ページのtitle、meta description、H1、main、nav、breadcrumb、footer
- 全10カテゴリの入口記事・関連カテゴリ導線
- 商品4ページのproduct-page、official-bar、affiliate-note、Amazon導線
- 制作者向けラベル（商品候補、当サイトが選定、採用理由）の再混入防止
- Q&Aの概要入口表記とdetails構造
- トップページから `自動更新` / `約10分間隔` を再表示しない
- リアルタイム取得失敗を0件表示へ変換しない
- 運営方針・privacy・免責・広告ページと実装の整合
- 共通アクセシビリティとGA4導線計測

## 7. 残課題

記事監査と同じく、ユーザー側の横断事項は `docs/USER_ACTION_ITEMS.md` を正とする。

特に:

- U01: GA4 DebugView / Realtime
- U02: Rich Results Test
- U03: 実スマートフォンUX
- U04〜U07: Search Console / GA4実データ
- U09: Amazon / メーカー商品画像の利用条件

これらを理由に通常のコンテンツ改善を停止しない。
