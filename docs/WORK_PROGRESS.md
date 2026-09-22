# 防災くらしガイド 作業進捗台帳

更新日: 2026-09-21
管理方針: このファイルをサイト全体の作業進捗の正本とする。

## 状態定義

- `TODO`: 未着手
- `IN_PROGRESS`: 作業中
- `BLOCKED`: 外部要因・データ待ち・ユーザー操作待ち等で停止
- `INTERNAL_CHECK_DONE`: 実装と内部チェックまで終了
- `USER_CONFIRMATION_PENDING`: ユーザー確認待ち
- `DONE`: ユーザー承認済み。正式完了
- `REOPENED`: 完了扱い後に問題が判明し再オープン

## 運用ルール

1. 作業開始前に、この台帳の「承認済み仕様」「完了条件」「次にやること」を確認する。
2. タイムアウト・ツール失敗・接続切断後も、承認済み仕様は変更しない。
3. 再開時は `next_action` から続行し、勝手に別方式へ置き換えない。
4. 実装と内部チェックが終わっても、ユーザー承認前は `USER_CONFIRMATION_PENDING` とする。
5. ユーザー承認後のみ `DONE` にする。
6. 完了後に不具合・仕様不一致が判明した場合は `REOPENED` に戻す。
7. 個別バックログ・記事別チェック・PR等の詳細記録は残し、この台帳から参照する。
8. 進捗報告時は「完了済み / 作業中 / 残作業 / ブロッカー / 次作業 / ユーザー確認待ち」を基準に報告する。

## 現在のサマリー

| ID | 優先 | タスク | 状態 | 次にやること | ユーザー承認 |
|---|:---:|---|---|---|---|
| IMG-001 | A | 線状降水帯の生成画像を実画像として本番表示 | DONE | なし | YES |
| OPS-001 | A | タイムアウト時の仕様不変ルール | USER_CONFIRMATION_PENDING | ユーザー確認 | NO |
| OPS-002 | A | 作業進捗台帳の導入 | DONE | なし | YES |
| PERF-001 | A | PageSpeed / Core Web Vitals継続改善 | IN_PROGRESS | 現行ボトルネックを再計測・整理 | NO |
| GA4-001 | A | Amazon / 商品記事クリックイベントのGA4受信確認 | BLOCKED | GA4管理画面で受信確認 | NO |
| STRUCT-001 | A | Google Rich Results Test外部確認 | BLOCKED | 外部Google検証を実施・結果記録 | NO |
| GSC-001 | A | Search Consoleデータ駆動リライト | IN_PROGRESS | 変更5記事のGSC効果観測 | NO |
| GSC-002 | A | Search Consoleカニバリ監視 | BLOCKED | 同一クエリ複数URLをデータ蓄積後に確認 | NO |
| LINEAR-PREF-001 | A | 線状降水帯県別ページ展開 | USER_CONFIRMATION_PENDING | 実発生確認済み14都県を県別シリーズ化。大阪B093は一般豪雨記事へ変更。ユーザー確認待ち | NO |
| LINEAR-CASE-002 | A | 線状降水帯 全事例表の再構成・高精度化 | USER_CONFIRMATION_PENDING | 県別14記事＋全国/地域別を5件以上目安で再構成し静的QA完了。デプロイ許可待ち | NO |
| LINEAR-DIFF-001 | B | ゲリラ豪雨と線状降水帯の違い 記事＋図解 | USER_CONFIRMATION_PENDING | B097本文・比較表・模式図・一次資料・preview・registry作成済み。ユーザー確認後、公開工程へ | NO |
| LINEAR-SHELTER-001 | A | 県別線状降水帯記事の避難場所・避難所導線 | USER_CONFIRMATION_PENDING | 14都県に公式避難所導線、東京23区/名古屋16区セレクターを追加。デプロイ許可待ち | NO |
| CASE-QUALITY-001 | A | 実在災害事例の全記事品質監査・最新事例補強 | USER_CONFIRMATION_PENDING | 横断監査・本文修正・ルール/チェックリスト更新・静的整合確認完了。修正概要を報告し、明示許可後のみ本番反映 | NO |
| SEO-001 | B | 水害系記事のカニバリ再確認 | TODO | 対象ページ・クエリを整理 | NO |
| CONTENT-001 | B | 長期断水×入浴・洗濯の記事検討 | TODO | 検索意図・既存記事との役割を確認 | NO |
| CONTENT-002 | B | 避難所×防犯／女性・子どもの記事検討 | TODO | 一次情報・検索意図・安全性を調査 | NO |
| CONTENT-003 | C | 内水氾濫と洪水の違いの独立記事化再評価 | TODO | B005/B020とのカニバリ確認 | NO |
| CONTENT-004 | C | 災害時の口腔ケア記事候補 | TODO | 需要・一次情報・商品導線を評価 | NO |
| EXPAND-001 | C | 大雪・寒波、雷・竜巻等の新災害カテゴリ検討 | TODO | IAと記事群の必要数を先に設計 | NO |
| UI-001 | B | サイトファビコン導入 | USER_CONFIRMATION_PENDING | ユーザーがブラウザタブ等の表示を確認 | NO |
| MOBILE-001 | - | モバイル実機レビュー | DONE | なし。線状降水帯の実画像問題はIMG-001で別管理 | YES |

## タスク詳細

### IMG-001 線状降水帯の生成画像を実画像として本番表示

- status: `DONE`
- priority: `A`
- approved_spec: 生成済み画像を実ファイルとして保存し、記事内へ `img` として表示する。PC・モバイル双方で画像が実際に見えること。
- completion_criteria: 公開アセット配置 / img組み込み / 適切な章への配置 / PC表示確認 / モバイル表示確認 / 本番HTTP確認 / ユーザー承認
- done: 生成画像原本1点＋分割5点を保存。5画像を `preview/assets/images/disaster/` に公開アセット化し、B067 / B012 / B009 / B036 の指定位置へ実imgで配置。レスポンシブCSS・アクセシビリティ・非クロップを自動テストし、本番deploy run #85で4ページと5画像のHTTP 200、本番HTML内の実画像参照を確認。2026-09-21にユーザーが本番表示・配置を確認し承認。
- remaining: なし
- next_action: なし
- blocker: なし
- related: `docs/research/LINEAR_RAINBAND_BACKLOG_20260920.md`, `docs/reviews/B067_CHECKLIST.md`, PR #103, PR #104, deploy run #85
- updated_at: `2026-09-21`
- user_approval: `YES`

### OPS-001 タイムアウト時の仕様不変ルール

- status: `USER_CONFIRMATION_PENDING`
- priority: `A`
- approved_spec: タイムアウト・ツール失敗時も承認済み仕様を変えず、実行方法だけを変更する。
- completion_criteria: private正本反映 / public作業コピー反映 / CI退行テストPASS / ユーザー承認
- done: private PR #14、public PR #99をマージ。CI run #215 PASS。
- remaining: ユーザー承認。
- next_action: ユーザー確認を受ける。
- blocker: ユーザー確認待ち
- related: private PR #14, public PR #99
- updated_at: `2026-09-21`
- user_approval: `NO`

### OPS-002 作業進捗台帳の導入

- status: `DONE`
- priority: `A`
- approved_spec: GitHub上の一元台帳を進捗の正本とし、承認済み仕様・完了条件・次作業・承認状態を記録する。
- completion_criteria: `docs/WORK_PROGRESS.md` 作成 / ガバナンス反映 / private正本反映 / CI契約テストPASS / ユーザー承認
- done: `docs/WORK_PROGRESS.md` 作成、publicガバナンス反映、private正本PR #15マージ、CI契約テスト追加、run #218 PASS、2026-09-21ユーザー承認。
- remaining: なし
- next_action: なし
- blocker: なし
- related: `docs/RULES_GOVERNANCE.md`, private PR #15, public PR #101, CI run #218
- updated_at: `2026-09-21`
- user_approval: `YES`

### CASE-QUALITY-001 実在災害事例の全記事品質監査・最新事例補強

- status: `USER_CONFIRMATION_PENDING`
- priority: `A`
- approved_spec: 線状降水帯記事に限定せず、実在する災害・豪雨・地震・噴火等の事例を掲載する全記事を対象に、同一イベント重複、予測/制度と発生実績の混同、日付順、地域適合、最新事例不足を再確認する。直近実事例は一次情報で確認できる範囲で複数件を掲載する。2026-09-21以降、本番デプロイはユーザー明示許可制とし、デプロイ前に修正概要・検証結果・残課題を報告する。
- completion_criteria: 正本ルール更新 / public作業コピー同期 / 事例記事横断抽出 / 独立イベント単位の監査 / 直近事例複数件の補強 / 重複・分類誤り修正 / 記事別レビュー更新 / 静的整合確認 / デプロイ前修正概要報告 / ユーザー明示許可 / 本番反映 / 本番スモーク / ユーザー確認
- done: private正本ルールPR #16〜#19をmainへ反映。B001〜B097を対象に監査し、非線状降水帯の主要災害史と線状降水帯特集・地域・県別記事を再確認。県別線状降水帯は実発生確認済み14都県へ整理し、大阪B093は一般豪雨記事へ変更。重複・予測混在・最新事例不足を修正し、観測史上順位等の記録性も復活。B097比較記事を追加。静的QA・回帰テスト更新・デプロイ前報告まで完了。
- remaining: ユーザー明示許可 / 許可後にmain反映 / workflowによるMarkdown→preview同期 / unit test / production build / FTPS転送 / 本番スモーク / ユーザー確認
- next_action: public PR #126 の内容を提示し、デプロイ許可を受ける。
- blocker: 本番デプロイはユーザー許可待ち
- related: `docs/reviews/DISASTER_CASE_AUDIT_20260921.md`, `docs/reviews/DISASTER_CASE_PREDEPLOY_REPORT_20260921.md`
- updated_at: `2026-09-21`
- user_approval: `NO`

### PERF-001 PageSpeed / Core Web Vitals継続改善

- status: `IN_PROGRESS`
- priority: `A`
- approved_spec: PageSpeed Insights / Core Web Vitalsを継続計測し、LCP・CLS・INP等の主要指標と実装上のボトルネックを確認して改善する。
- completion_criteria: 現状計測 / 主要ボトルネック特定 / 改善実装 / 再計測 / 回帰確認 / ユーザー確認
- done: 継続改善タスクとして台帳化済み。
- remaining: 現状再計測 / ボトルネック整理 / 改善実装 / 再計測 / ユーザー確認
- next_action: 現行ボトルネックを再計測・整理
- blocker: 今回の線状降水帯品質監査とは別タスク
- related: PageSpeed / Core Web Vitals 改善履歴
- updated_at: `2026-09-22`
- user_approval: `NO`


### LINEAR-CASE-002 線状降水帯 全事例表の再構成・高精度化

- status: `USER_CONFIRMATION_PENDING`
- priority: `A`
- approved_spec: 県別だけでなく、全国年表・地域別等の線状降水帯ページで事例を扱う場合、「直近の大雨・線状降水帯事例」と「過去の代表的な豪雨」を原則別表にする。直近＋過去代表を合わせて目安5件以上。ただし信頼できる事例が不足する場合は件数合わせをしない。被害の大きい局地的大雨も現象を区別して掲載可。警戒レベルは公的発表に基づく。県別titleは「○○県の線状降水帯｜過去の発生履歴・直近事例を一覧で解説」。実発生未確認県は県別シリーズから外す。
- completion_criteria: 正本ルール反映 / 県別・全国・地域別の事例表再構成 / 事例分類・重複・最新性確認 / registry同期 / unit test / production build / 本番反映 / 本番スモーク / ユーザー確認
- done: 正本ルールPR #17〜#19を反映。県別14記事のtitle統一。大阪B093は一般の大雨・都市型水害記事へ役割変更し、県別ナビから除外。B068/B073〜B077/B082〜B092/B094〜B096の事例表を直近/過去へ再構成。県別14記事は全て5件以上、B068/B073〜B077も5件以上。東京・愛知を含め、一次資料で確認できる観測史上順位・平年比・被害を補強。表列数、title/H1、literal \n、制作工程語、出典リンクを静的QA済み。registry文字数も再計算・同期済み。
- remaining: ユーザー明示許可 / mainマージ後のworkflowでunit test・production build・FTPS・本番スモーク / ユーザー確認
- next_action: public PR #126 の内容確認後、ユーザーのデプロイ許可を受ける。
- blocker: 本番デプロイはユーザー許可待ち
- related: `docs/reviews/DISASTER_CASE_AUDIT_20260921.md`, `docs/reviews/DISASTER_CASE_PREDEPLOY_REPORT_20260921.md`, PR #126
- updated_at: `2026-09-21`
- user_approval: `NO`

### LINEAR-DIFF-001 ゲリラ豪雨と線状降水帯の違い

- status: `USER_CONFIRMATION_PENDING`
- priority: `B`
- approved_spec: 正式用語として「局地的大雨（いわゆるゲリラ豪雨）」を使用し、線状降水帯との違いを、雨雲の構造、範囲、継続時間、予測、防災情報、典型的な被害で比較する。図解を使用し、1図1メッセージ、誤解を招く安全境界・警戒レベル対応を作らない。
- completion_criteria: 本文・比較表・図解作成 / 一次資料確認 / preview・registry同期 / 内部リンク / unit test / production build / 本番反映 / 本番スモーク / ユーザー確認
- done: B097 `ゲリラ豪雨と線状降水帯の違い｜雨雲・範囲・時間・予測を図で比較` をreader-visible約3,870字で作成。気象庁一次資料6件を確認。比較表、局地的大雨/線状降水帯の模式図SVG、preview HTML、SOURCES、IMAGES、CHECKLIST、registry追加を作成。B067/B092/B094から内部リンクを追加。正本ルールPR #19で災害事例数を「直近＋過去代表で目安5件以上、無ければ水増ししない」へ変更。
- remaining: PR #126のユーザー内容確認 / mainマージ後の本番ビルド・自動テスト / ユーザー明示許可後のみデプロイ / 公開後HTTP・モバイル確認
- next_action: PR #126のデプロイ工程を完了し、本番B097の本文・比較表・図解・内部リンクを確認する。
- blocker: production workflowのテスト失敗を修正中
- related: `content/articles/B097_guerrilla_rain_vs_linear_rainband.md`, `docs/reviews/B097_CHECKLIST.md`, PR #126
- dependency: `LINEAR-CASE-002` の事例拡充と並行可能。公開は品質監査後にまとめて行う。
- updated_at: `2026-09-21`
- user_approval: `NO`



### LINEAR-SHELTER-001 県別線状降水帯記事の避難場所・避難所導線

- status: `USER_CONFIRMATION_PENDING`
- priority: `A`
- approved_spec: 県別記事で避難場所を分かりやすく案内する。指定緊急避難場所と指定避難所を区別し、洪水・内水・土砂等の災害種別への適合と当日の開設状況を自治体一次情報で確認できるようにする。候補が多い都市部は選択UIを使う。一般地図は位置確認の補助に限り、指定・開設状況の正本にはしない。
- completion_criteria: 14都県の公式導線 / GSI導線 / 東京23区・名古屋16区セレクター / モバイル・アクセシビリティ確認 / unit test / production build / 本番表示確認 / ユーザー確認
- done: 14都県に自治体公式ページ＋国土地理院の指定緊急避難場所/指定避難所データへの共通shelter finderを記事上部に追加。東京B092は23区、愛知B094は名古屋16区を選択して各自治体公式ハザードマップを開けるUIを追加。本文側は地域固有の避難ポイントだけ残し、重複していた共通説明を削除。モバイル1列化、キーボード操作、冠水後の遠距離移動注意を実装。正本ルールPR #20をmainへ反映。記事別/共通チェックリストへC02-29〜C02-35相当の確認を記録。
- static_qa: shelter guide 14件 / 東京23区 / 名古屋16区 / GSI導線 / selector script / mobile single-column / 本文側の共通避難説明重複0件を確認。主要公式リンクも2026-09-22時点で再確認。
- remaining: production workflowでMarkdown→preview同期・unit test・build / 本番表示確認 / ユーザー確認
- next_action: PR #126のデプロイ前報告へ追加し、ユーザー明示許可後にmainへマージする。
- blocker: 本番デプロイはユーザー許可待ち
- related: private rules PR #20, public PR #126
- updated_at: `2026-09-22`
- user_approval: `NO`
