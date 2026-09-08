# B060 記事別レビュー

- article_id: B060
- review_status: PASS
- last_checked_at: 2026-09-08
- risk_level: elevated
- READY_TO_PUBLISH: YES

## 検索意図・役割

- PASS: B056の地域災害史、B058の発災時行動と検索意図を分離し、B060は選び方・比較・購入判断を主役にした。
- PASS: `情報記事 → 商品記事 → Amazon` の導線を維持。
- PASS: 商品一覧を後付けせず、用途・選び方の説明直後に商品例を配置。

## 安全・公的情報

- PASS: 気象庁の「多量（1mm以上）では外出・運転を控える」を商品紹介より先に表示。
- PASS: DS2を気象庁の必須指定規格と誤記していない。
- PASS: マスクは重松製作所の火山灰用途・国家検定情報を確認。
- PASS: シールチェックをメーカー案内で確認し、密着性を強調。
- PASS: LX-22の火山灰用途、換気口なし、眼鏡併用、規格をメーカー公式で確認。
- PASS: 屋根・高所清掃を一般家庭へ勧めず、転落リスク境界を明記。
- PASS: 鹿児島市の克灰袋制度を全国共通制度として扱っていない。

## 商品選定

- PASS: 3商品に限定し、数合わせをしていない。
- PASS: DD02-S2-2K = 基本備蓄、DD02V-S2-2K = 排気弁付き、LX-22 = 目の保護、と用途を分離。
- PASS: 通常型と排気弁付きを両方買う必要があるとは表現していない。
- PASS: 主要仕様はメーカー公式で確認。
- PASS: 参考価格はAmazon価格ではなく、2026-09-08のモノタロウ販売価格として出典を明示。
- PASS: Amazon現在価格・在庫はリンク先確認とした。

## Amazon・アフィリエイト

- PASS: アソシエイト開示あり。
- PASS: 3商品のAmazon商品詳細ページと型番一致を確認し、ASINを記録。
- PASS: DD02-S2-2K = `B081YKHRLB`、DD02V-S2-2K = `B079BNC5XQ`、LX-22 = `B08NT64H61`。
- PASS: CTAは検索結果ではなく `https://www.amazon.co.jp/dp/ASIN/ref=nosim?tag=yukitaka83-22` の商品詳細ページへ直接遷移。
- PASS: 画像クリック先もCTAと同じAmazon商品詳細ページに統一。
- PASS: アソシエイトタグは `config/site.json` の `yukitaka83-22` と一致。
- PASS: 商品購入を安全保証・避難行動の代替として表現していない。

## 画像

- PASS: 3商品とも重松製作所の公式製品ページが配信する製品画像を採用。
- PASS: 商品名・型番とメーカー製品ページの画像を照合。
- PASS: 商品画像を自サイトへ再ホストしていない。
- PASS: `alt` に商品名・型番を含めた。
- PASS: `loading="lazy"` と既存商品カードの `onerror` フォールバックを維持。
- PASS: `docs/research/B060_IMAGES.md` に画像URL・配信元・ASIN・表示仕様を記録。

## UX・内部リンク

- PASS: B060 → B058で発災時の安全行動へ戻れる。
- PASS: B060 → B056で地域情報へ戻れる。
- PASS: B056/B058からB060への文脈リンクあり。
- PASS: category_goodsへB060掲載済み。
- PASS: 商品画像とCTAのどちらからでも同一商品へ到達できる。

## 本文量・読者満足度

- reader_visible_char_count: **3,602字**（現行監査ロジック）
- guideline_minimum: 固定数値ルールなし（content_role=product）
- length_status: **PASS_NO_NUMERIC_RULE**
- editorial_note: 商品数ではなく、選び方、安全境界、具体仕様、弱点、清掃、購入後確認、次の行動まで含むことを優先。

## 最終判定

公開可能。商品情報は2026-12-08までを次回レビュー目安とし、販売継続・ASIN・価格出典・画像URLを再確認する。
