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
| LINEAR-PREF-001 | A | 線状降水帯15都道府県ページ展開 | USER_CONFIRMATION_PENDING | ユーザーが15都道府県ページの表示・内容を確認 | NO |
| LINEAR-CASE-002 | A | 線状降水帯 全事例表の再構成・高精度化 | IN_PROGRESS | 県別・地域別・全国年表を直近/過去で分離し、直近事例の一次資料・雨量・警報・被害を再確認 | NO |
| LINEAR-DIFF-001 | B | ゲリラ豪雨と線状降水帯の違い 記事＋図解 | TODO | LINEAR-CASE-002完了後に作成。現象・範囲・継続・予測・被害を図解比較 | NO |
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

### PERF-001 PageSpeed / Core Web Vitals継続改善

- status: `USER_CONFIRMATION_PENDING`
- priority: `A`
- approved_spec: 線状降水帯記事に限定せず、実在する災害・豪雨・地震・噴火等の事例を掲載する全記事を対象に、同一イベント重複、予測/制度と発生実績の混同、日付順、地域適合、最新事例不足を再確認する。直近実事例は一次情報で確認できる範囲で複数件を掲載する。2026-09-21以降、本番デプロイはユーザー明示許可制とし、デプロイ前に修正概要・検証結果・残課題を報告する。
- completion_criteria: 正本ルール更新 / public作業コピー同期 / 事例記事横断抽出 / 独立イベント単位の監査 / 直近事例複数件の補強 / 重複・分類誤り修正 / 記事別レビュー更新 / 静的整合確認 / デプロイ前修正概要報告 / ユーザー明示許可 / 本番反映 / 本番スモーク / ユーザー確認
- done: private正本ルール5ファイル更新・PR #16でmainへ正式反映。public作業コピー4ファイル同期。96記事を横断抽出し、非線状降水帯の主要災害史8記事と線状降水帯特集・地方・15都道府県記事を再監査。B076/B087等の重複、B083/B092/B094等の予測・制度混在、B082/B084/B085/B086/B088/B090/B094等の最新事例不足、B096の重複を修正。20記事でtitle/H1一致、Markdown表列、literal \\n、編集工程語を静的確認。気象庁一次資料で2026年主要事例と名古屋確定雨量を再確認。
- remaining: ユーザーへのデプロイ前修正概要報告 / ユーザー明示許可 / 許可後にmain反映 / workflowによるMarkdown→preview同期 / unit test / production build / FTPS転送 / 本番スモーク / ユーザー確認
- next_action: 修正概要・検証結果・既知の残課題をユーザーへ報告し、デプロイ可否の明示判断を受ける。
- blocker: 本番デプロイはユーザー許可待ち
- related: `docs/reviews/DISASTER_CASE_AUDIT_20260921.md`, `docs/CONTENT_CREATION_RULES.md`, `docs/ARTICLE_REVIEW_CHECKLIST.md`, `docs/FRESHNESS_POLICY.md`, `docs/SITE_RELEASE_CHECKLIST.md`
- updated_at: `2026-09-21`
- user_approval: `NO`


### LINEAR-CASE-002 線状降水帯 全事例表の再構成・高精度化

- status: `IN_PROGRESS`
- approved_spec: 県別だけでなく、全国年表・地域別等の線状降水帯ページで事例を扱う場合、「直近の大雨・線状降水帯事例」と「過去の代表的な豪雨」を原則別表にする。直近は最新時点まで再検索し、原則3〜5件を目安とするが件数合わせはしない。被害の大きい局地的大雨（いわゆるゲリラ豪雨）も掲載可。ただし線状降水帯とは別現象として明記。警戒レベルは雨量から独自推定せず、実際の公的発表に基づく。県別titleは「○○県の線状降水帯｜過去の発生履歴・直近事例を一覧で解説」。実発生未確認県は県別シリーズから外す。
- done: 正本ルールPR #17をmainへ反映。public側ルール・共通チェックリスト同期。県別14記事のtitle統一。大阪B093は一般の大雨・都市型水害記事へ役割変更し、registry上の親をB005へ変更。県別記事B082〜B096、全国年表B068、地域別B073〜B077の事例表を直近/過去へ再構成。記事別・特集・地域別・3バッチチェックリストへ新基準を反映。
- remaining: 各直近事例についてユーザー提示サンプル相当の粒度（日付/現象/実測雨量/公式発表/被害）を一次資料中心に再照合し、空欄・弱い行を補強。全記事横断QA。デプロイ前修正概要報告。ユーザー許可後のみ本番反映。
- next_action: 直近事例の高精度ソース監査を県別・地域別に実行する。
- blocker: 本番デプロイはユーザー許可待ち
- updated_at: `2026-09-21`
- user_approval: `NO`

### LINEAR-DIFF-001 ゲリラ豪雨と線状降水帯の違い

- status: `TODO`
- priority: `B`
- approved_spec: LINEAR-CASE-002完了後に別ページを作成する。正式用語として「局地的大雨（いわゆるゲリラ豪雨）」を使用し、線状降水帯との違いを、雨雲の構造、範囲、継続時間、予測、防災情報、典型的な被害で比較する。図解を使用し、1図1メッセージ、誤解を招く安全境界・警戒レベル対応を作らない。
- remaining: 一次資料調査 / 構成 / 図解作成 / 本文作成 / レビュー / ユーザー確認 / 許可後デプロイ
- dependency: `LINEAR-CASE-002`
- updated_at: `2026-09-21`
- user_approval: `NO`
