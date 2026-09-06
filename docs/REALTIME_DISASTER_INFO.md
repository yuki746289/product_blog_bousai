# トップページ「現在の防災情報」運用仕様

更新日: 2026-09-03

## 目的

静的な記事一覧だけでなく、トップページで現在の防災状況を簡潔に確認できる入口を提供する。

表示対象:
- 最新の地震情報
- 主な警報・特別警報
- 台風情報

避難判断の一次情報にはしない。常に気象庁・自治体等の公式情報へのリンクを併記する。

## 情報源

地震・台風は気象庁「防災情報XMLフォーマット」PULL型配信を使用する。

- 公式案内: https://xml.kishou.go.jp/xmlpull.html
- 高頻度/随時: https://www.data.jma.go.jp/developer/xml/feed/extra.xml
- 高頻度/地震火山: https://www.data.jma.go.jp/developer/xml/feed/eqvol.xml
- 長期/随時: https://www.data.jma.go.jp/developer/xml/feed/extra_l.xml
- 長期/地震火山: https://www.data.jma.go.jp/developer/xml/feed/eqvol_l.xml

警報・特別警報は、継続中の情報がAtomの掲載窓から外れることで「現在発表中なのに取得できない」状態を避けるため、気象庁公式サイトの現在表示用R8警報JSONを使用する。

- 全国警報状態: https://www.jma.go.jp/bosai/warning/data/r8/map.json
- 地域コード: https://www.jma.go.jp/bosai/common/const/area.json

気象庁の高頻度Atomフィードは毎分更新・直近少なくとも10分の入電を掲載する。長期フィードは毎時更新・数日間の入電を掲載する。

## 更新構成

```text
気象庁 PULL XML
       ↓
GitHub Actions（約10分間隔）
       ↓
scripts/update_realtime.py
       ↓
realtime.json
       ↓
IPv4/PASV固定のFTPSで /realtime/realtime.json のみ更新
       ↓
トップページJSが表示
```

通常の記事・画像・CSS等を10分ごとに再デプロイしない。

## 状態再構築

高頻度フィードは直近約10分のため、地震・台風の初期状態復元用として次の場合に長期フィードを使う。

- 初回
- 前回確認から20分以上空いた場合
- 6時間ごとの定期再同期

警報は毎回、全国R8警報JSONから現在状態を再構築する。前回JSONの警報状態は、警報JSON取得失敗時のフォールバックとしてのみ使う。

## 取得失敗

取得エラーを「情報なし」として扱わない。

- 一部取得失敗: `partial`
- 全対象取得失敗: `degraded`
- 前回データを保持
- トップページに遅延/取得失敗の警告を表示
- 気象庁への公式リンクを維持

ブラウザ側でも `checked_at` が30分以上古い場合は遅延警告を表示する。

## ブラウザ側更新

トップページを開いた時に `realtime/realtime.json` を取得する。

開いたままの場合は5分間隔でJSONのみ再取得する。

## 警報表示

「注意報」はトップの簡潔表示から除外し、「警報」「特別警報」を表示対象にする。

警報情報はXMLの府県予報区等のHeadline情報を優先し、種類ごとに地域をまとめる。

この表示は簡易サマリーであり、全市町村の詳細表示を目的としない。

## 台風表示

台風関連XMLをEventID単位で管理する。

「熱帯低気圧に変わった」「温帯低気圧に変わった」「消滅」等の終了情報を受けたEventIDは表示対象から外す。

最終情報が24時間以上更新されないEventIDもトップ表示から外す。

## GitHub Actions利用量

リポジトリがprivateの場合、GitHub-hosted runnerはアカウントのActions利用枠を消費し、超過時は課金対象となる可能性がある。

リアルタイム更新は軽量な `ubuntu-slim` を使用し、タイムアウトを3分に制限する。

cronは毎時3/13/23/33/43/53分に設定する。GitHub Actionsのscheduleは高負荷時に遅延・ドロップする可能性があるため、表示上は「約10分間隔」とする。理論上は1日144回、30日で4,320回のworkflow実行になる。GitHubは1分未満のジョブも1分単位に切り上げるため、現在の約20秒ジョブでも最大4,320請求分（分）/30日相当になる。ubuntu-slimの超過単価は2026-09-03確認時点で$0.002/分。private repoの付属枠（Free 2,000分/月、Pro 3,000分/月等）と他workflowの利用量を含めてUsageを定期確認する。

必要に応じて、
- 15分
- 30分
- 60分

へ更新間隔を変更できる。

## 関連ファイル

- `scripts/update_realtime.py`
- `.github/workflows/update-realtime.yml`
- `preview/realtime/realtime.json`
- `preview/index.html`
- `preview/bousai_common.js`
- `preview/bousai_common.css`
- `tests/test_realtime_update.py`


## 通常サイトデプロイとの分離

通常のproduction deployでは `realtime/**` をFTPS対象から除外する。

理由:
- `preview/realtime/realtime.json` はローカルプレビュー・初期ビルド用のplaceholder
- 通常デプロイでplaceholderを本番へ上書きすると、次の定期更新まで「初期化中」に戻る
- 本番の `/realtime/realtime.json` は `update-realtime.yml` だけが更新する

リアルタイム更新のFTPSは軽量runnerで安定させるため、GitHub Actionラッパーではなくcurlを使い、
- IPv4
- explicit FTPS
- passive mode
- EPSV無効
- 最大3回リトライ

で1ファイルだけ転送する。

## 実運用確認

2026-09-03 18:58 JSTの実行で以下を確認した。

- status: ok
- warning_count: 5
- typhoon_count: 2
- earthquake: 取得あり
- errors: 0
- JSON生成: PASS
- FTPS upload: PASS
- 本番JSON smoke: PASS
- 通常production deploy後も `realtime/**` を保持: PASS


## トップページ専用アセット

リアルタイム表示のCSS/JavaScriptは記事共通アセットから分離する。

- `bousai_common.css`: 全ページ共通の基礎スタイル
- `bousai_common.js`: 画像フォールバック、共通クリック計測
- `bousai_home.css`: トップページのリアルタイム情報UI
- `bousai_home.js`: JSON取得、5分再読込、地震・警報・台風の描画

記事ページでは `bousai_home.css` / `bousai_home.js` を読み込まない。

## 台風表示方針

トップページでは気象庁の内部的な資料名をそのまま表示しない。

特に、
- 台風解析・予報情報
- 台風の暴風域に入る確率

は別データ製品であり、利用者にその名称を並べても現在の状況が伝わりにくい。

台風件数の判定には `台風解析・予報情報...` のみを使用し、暴風域に入る確率のXMLは台風件数として数えない。

表示例:
- 0件: 「現在、表示対象の台風・発達する熱帯低気圧は確認されていません。」
- 2件: 「現在、気象庁が台風等2件を解析・予報しています。」

進路・強度等は気象庁公式台風ページへのリンクで確認してもらう。


## 表示デザイン

トップページのリアルタイム領域は記事カードと誤認されないよう、通常記事とは明確に異なる「防災モニター」型UIにする。

- 外枠はサイト配色になじむ淡い青緑の情報パネル
- 強い濃色背景や大きなシャドウは使わない
- 更新間隔は利用者向けUIに表示せず、最終取得時刻のみ小さく表示
- 地震・警報・台風はカードではなく3列のステータス欄として区切る
- 記事カード用の画像・独立カード・大きなCTAとは異なる情報密度にする
- 詳細リンクは各パネル末尾の気象庁公式導線に限定
- モバイルでは縦積みにする

最終取得時刻は `checked_at` を表示し、30分以上古い場合は遅延警告へ切り替える。


## ブラウザからの直接取得

2026-09-03以降、トップページの最新表示はGitHub Actionsのscheduleだけに依存しない。

ページ表示時:
1. サイト内の `realtime/realtime.json` を先に読み、即座に表示する
2. 続けてブラウザから気象庁の公開JSONを直接取得する
3. 直接取得に成功した項目だけ最新値へ置き換える
4. 全項目成功時は `status=ok`、一部成功時は `partial`
5. 開いたままの場合は10分ごとに同じ処理を行う

直接取得対象:
- 地震: `https://www.jma.go.jp/bosai/quake/data/list.json`
- 警報: `https://www.jma.go.jp/bosai/warning/data/r8/map.json`
- 地域名: `https://www.jma.go.jp/bosai/common/const/area.json`
- 台風: `https://www.jma.go.jp/bosai/typhoon/data/targetTc.json`

GitHub Actionsの定期更新は、本番JSONのバックアップキャッシュを更新する補助経路とする。

### 理由

GitHub Actionsの `schedule` はbest-effortであり、GitHub公式も高負荷時の遅延・ジョブ欠落可能性を明記している。実際、2026-09-03の初期運用ではpushイベントは成功した一方、scheduleイベントが予定時刻に生成されない状態を確認した。

そのため「約10分おきにサーバー側で必ず更新される」という前提を置かず、閲覧時の直接取得を主経路とする。
