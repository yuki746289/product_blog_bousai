# Production Lighthouse performance audit

実施日: 2026-09-03  
方式: GitHub Actions / Lighthouse 12.8.2 / mobile emulation  
Baseline run: 33727160529

## 判定上の注意

Lighthouseはラボ計測であり、実ユーザーのCore Web Vitalsそのものではない。
実ユーザーのLCP / INP / CLSは、CrUXやSearch ConsoleのCore Web Vitalsで別途確認する。

GoogleのCore Web Vitals基準:
- LCP: 2.5秒以下が良好、4.0秒超は不良
- INP: 200ms以下が良好、500ms超は不良
- CLS: 0.1以下が良好、0.25超は不良
- 実ユーザーデータでは75パーセンタイルで評価

参考:
- https://web.dev/articles/lcp?hl=ja
- https://web.dev/articles/cls?hl=ja
- https://web.dev/articles/defining-core-web-vitals-thresholds

## Baseline

| URL | Performance | FCP | LCP | CLS | TBT | Speed Index |
|---|---:|---:|---:|---:|---:|---:|
| トップ | 70 | 3.2s | 4.6s | 0 | 250ms | 4.9s |
| B001 防災入門 | 56 | 4.3s | 7.2s | 0 | 300ms | 5.8s |
| B028 ポータブル電源 | 68 | 4.0s | 4.9s | 0 | 220ms | 4.4s |

## 主なLighthouse指摘

### トップ
- Preconnect to required origins: 約476ms
- Reduce unused JavaScript: 約450ms
- TTFB: 約110msで大きな問題なし

### B001
- Preconnect to required origins: 約612ms
- Reduce unused JavaScript: 約490ms
- Properly size images: 約330ms / 67KiB
- Reduce unused CSS: 約240ms
- Enable text compression: 約240ms
- TTFB: 約110ms

### B028
- Reduce unused JavaScript: 約750ms
- Eliminate render-blocking resources: 約507ms
- Preconnect to required origins: 約368ms
- TTFB: 約110ms

## 初回対応

1. Wikimedia Commons画像のローカルWebP化、width/height付与、feature imageのfetchpriorityは実装済み。
2. Google Tag Manager / Google Analyticsへpreconnectを追加。
3. Google Analyticsは計測上必要なため、Lighthouseのunused JavaScriptだけを理由に削除しない。
4. CLSは3ページとも0であり、現時点では優先的な追加修正は不要。
5. サーバー側text compressionはホスティング側制約を確認せずに設定ファイルを追加しない。
6. CSSの非同期化はFOUCやレイアウト崩れのリスクがあるため、単純なmedia=print方式は採用しない。

## 残確認

- preconnect追加後のLighthouse再計測
- B001のLCP要素・画像サイズの追加分析
- Search Console / CrUXに十分なデータが出た後、実ユーザーLCP / INP / CLSを確認


## LCP要素の詳細

### トップ
LCPは画像ではなくhero内の説明文。LCP 4.59sのうち約81%がrender delay。
Lighthouseでunused JavaScriptとして以下が確認された。

- Google gtag
- `cnobi.jp/v1/asumi/prebid/...`
- `j.amoad.com/js/n.js`

`cnobi.jp` と `amoad.com` はリポジトリ内に参照がなく、本番ホスティング側で挿入されている第三者広告スクリプトと判断できる。サイトコードからは削除しない。

### B001
LCPは記事メイン画像 `commons_c6700ec800ec2e86.webp`。
表示380pxに対して960px画像を取得しており、Lighthouseは約67KiBの削減余地を指摘。
対応として720pxのresponsive WebP variantと`srcset` / `sizes`を本番画像生成へ追加した。

### B028
LCPはH1テキストで、LCP 4.87sの約87%がrender delay。
一方、Anker商品画像が約1.2MB取得され、responsive image auditで約1.18MBの削減余地が出ていたため、メーカーCDNへ480px幅を要求するURLへ変更した。

## 追加対応（再計測前）

- GAオリジンへのpreconnect
- Commons記事画像の720px responsive variant
- トップ・カテゴリのCommonsサムネイルを640px要求へ縮小
- Anker / Jackeryの商品画像を480px要求へ縮小
- ホスティング注入広告JSはサイトリポジトリでは制御不能として切り分け


## 再計測（Run 33734028796）

Lighthouse 12.8.2 / mobile emulation。

| URL | Performance | FCP | LCP | CLS | TBT | Speed Index |
|---|---:|---:|---:|---:|---:|---:|
| トップ | 53 | 3.2s | 5.6s | 0 | 560ms | 6.7s |
| B001 防災入門 | 71 | 3.5s | 5.1s | 0 | 150ms | 4.2s |
| B028 ポータブル電源 | 74 | 3.6s | 4.7s | 0 | 70ms | 3.8s |

### 解釈

- B001は初回 score 56 → 71、LCP 7.2s → 5.1sへ改善。
- B028は初回 score 68 → 74、TBT 220ms → 70msへ改善。
- B001の画像最適化余地は約67KiB → 約13KiBへ縮小。
- B028で初回に出ていた約1.18MBの商品画像削減指摘は解消。
- preconnect指摘は解消。
- CLSは全3ページで0を維持。
- トップは計測変動と第三者広告JavaScriptの影響が大きく、単発scoreだけで悪化判定しない。
- `cnobi.jp` / `amoad.com` はリポジトリ内参照がなく、ホスティング側注入と切り分け済み。
- 実ユーザーINP/LCP/CLSはSearch Console / CrUXの75パーセンタイルで別途判断する。
