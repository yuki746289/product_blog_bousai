# B060 画像調査

- article_id: B060
- image_source_count: 3
- image_status: APPROVED
- checked_at: 2026-09-08

## 判定

既存の商品記事と同じ商品カード方式に合わせ、3商品の実商品画像を表示する。

- 画像は重松製作所の公式製品ページが配信する製品画像を直接参照する。
- 画像クリック先は、型番一致を確認したAmazon商品詳細ページへ統一する。
- Amazonの検索結果ページではなく、ASIN固定の `/dp/ASIN` へ遷移させる。
- 商品画像は自サイトへダウンロード・再ホストしない。
- 画像取得失敗時は既存商品カードと同じ `onerror` フォールバックを使用する。

## 採用画像

| 製品 | Amazon ASIN | 画像配信元 | 画像URL |
|---|---|---|---|
| DD02-S2-2K | `B081YKHRLB` | 重松製作所 | `https://www.sts-japan.com/upload/products_ja/2AQ1UZ6-products_ja_mainimage.png` |
| DD02V-S2-2K | `B079BNC5XQ` | 重松製作所 | `https://www.sts-japan.com/upload/products_ja/2AQ1UZ5-products_ja_mainimage.png` |
| LX-22 | `B08NT64H61` | 重松製作所 | `https://www.sts-japan.com/upload/products_ja/2AQ1V59-products_ja_mainimage.png` |

## 照合

### DD02-S2-2K

- メーカー製品ページ: `https://www.sts-japan.com/products/dd/dd02_s2_2k.php`
- メーカー製品ページ上のメイン画像と型番を照合。
- Amazon商品詳細ページの型番: DD02-S2-2K
- ASIN: `B081YKHRLB`

### DD02V-S2-2K

- メーカー製品ページ: `https://www.sts-japan.com/products/dd/dd02v_s2_2k.php`
- メーカー製品ページ上のメイン画像と型番を照合。
- Amazon商品詳細ページの型番: DD02V-S2-2K
- ASIN: `B079BNC5XQ`

### LX-22

- メーカー製品ページ: `https://www.sts-japan.com/products/eye_protector/lx-22.php`
- メーカー製品ページ上のメイン画像と型番を照合。
- Amazon商品詳細ページの型番: LX-22
- ASIN: `B08NT64H61`

## 表示仕様

各商品カードは次を満たす。

1. 商品画像をカード左側に表示
2. 画像クリックで対応するAmazon商品詳細ページへ遷移
3. CTAも同じAmazon商品詳細ページへ遷移
4. `rel="nofollow sponsored noopener"` を維持
5. `alt` に商品名・型番を含める
6. `loading="lazy"` と既存の画像エラーフォールバックを維持

商品画像は本文画像数へ加算しない。
