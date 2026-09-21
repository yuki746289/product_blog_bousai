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
| LINEAR-PREF-001 | A | 線状降水帯15都道府県ページ展開 | IN_PROGRESS | Batch 1（鹿児島・宮崎・熊本・長崎・大分）を作成 | NO |
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

- status: `IN_PROGRESS`
- priority: `A`
- approved_spec: 既存機能や表示を壊さず、実測ベースで性能ボトルネックを改善する。
- completion_criteria: 代表ページ再計測 / 主要ボトルネック記録 / 実装可能な改善反映 / 再計測 / ユーザー確認
- done: 既存Lighthouse監査と一部画像最適化を実施済み。
- remaining: 現行状態の再計測と継続改善。
- next_action: トップ・代表記事の現行値を再監査する。
- blocker: なし
- related: `docs/SITE_IMPROVEMENT_BACKLOG.md`
- updated_at: `2026-09-21`
- user_approval: `NO`

### GA4-001 Amazon / 商品記事クリックイベントのGA4受信確認

- status: `BLOCKED`
- priority: `A`
- approved_spec: 実装済み `amazon_click` / `product_guide_click` がGA4で受信できることを確認する。
- completion_criteria: DebugViewまたはリアルタイムでイベント受信確認 / 結果記録 / ユーザー承認
- done: 共通JS実装・自動テスト済み。
- remaining: GA4管理画面で受信確認。
- next_action: GA4側の受信結果を確認する。
- blocker: GA4管理画面へのユーザー側確認が必要
- related: `docs/SITE_IMPROVEMENT_BACKLOG.md`
- updated_at: `2026-09-21`
- user_approval: `NO`

### STRUCT-001 Google Rich Results Test外部確認

- status: `BLOCKED`
- priority: `A`
- approved_spec: 本番BlogPosting / BreadcrumbListをGoogle外部検証でも確認する。
- completion_criteria: Rich Results Test等で主要ページを確認 / エラー有無を記録 / 必要修正 / ユーザー承認
- done: CIと本番HTTPでJSON-LD構文・主要項目を自動検証済み。
- remaining: Google外部検証。
- next_action: 代表ページをRich Results Testで確認する。
- blocker: 外部Google検証
- related: `docs/SITE_IMPROVEMENT_BACKLOG.md`
- updated_at: `2026-09-21`
- user_approval: `NO`

### GSC-001 Search Consoleデータ駆動リライト

- status: `IN_PROGRESS`
- priority: `A`
- approved_spec: 実検索データを基に、表示回数・CTR・順位・クエリから必要な記事だけを改善する。
- completion_criteria: 十分なデータ取得 / 優先記事選定 / 修正 / 効果確認 / ユーザー承認
- done: GSC導入・初期データ確認済み。2026-09-21エクスポート（9/2〜9/20、9/20単日、過去24時間）を分析し、線状降水帯のニュース需要増と、B008 / B019 / B010 / B022 / B015等の上位表示・低CTR候補を抽出。`docs/research/GSC_ANALYSIS_20260921.md` に記録。B008はSERPとB009との役割分離を確認し、title/H1/meta descriptionを検索意図が伝わる形へ調整。PR #108をマージし、deploy run #87で新タイトルの本番HTTP反映を確認。B019はSERP・役割分離を確認したが、匿名クエリが多く主検索意図を十分特定できないため現行titleを維持。B010はSERP・記事役割を確認し、title/H1/meta descriptionを「車を移すべきか」が伝わる形へ調整。B022はSERP・公的情報・記事役割を確認し、title/H1を高層階の停電・断水と地下浸水が伝わる形へ調整。B015は公的情報と検索意図を確認し、title/H1を「片付け前に写真を撮る」が伝わる形へ調整。B045は平均11.70位からの1ページ目到達を狙い、title/H1を「冷蔵庫は何時間もつ？」へ調整。
- remaining: B008/B010/B022/B015/B045変更後の順位・CTR効果確認、線状降水帯のニュース流入の継続観測。
- next_action: 次回GSCエクスポートで変更5記事の順位・表示回数・CTRと、線状降水帯のニュース後推移を比較する。
- blocker: なし
- related: `docs/SITE_IMPROVEMENT_BACKLOG.md`, `docs/research/GSC_ANALYSIS_20260921.md`
- updated_at: `2026-09-21`
- user_approval: `NO`

### GSC-002 Search Consoleカニバリ監視

- status: `BLOCKED`
- priority: `A`
- approved_spec: 同一クエリで複数URLが競合している場合のみ、統合・内部リンク・title等を検討する。
- completion_criteria: 十分なGSCデータ / 競合候補抽出 / 対応判断 / 必要修正 / ユーザー承認
- done: 監視方針定義済み。
- remaining: データ蓄積後の実測確認。
- next_action: GSCクエリ×ページデータが十分になったら抽出する。
- blocker: データ蓄積待ち
- related: `docs/SITE_IMPROVEMENT_BACKLOG.md`
- updated_at: `2026-09-21`
- user_approval: `NO`

### LINEAR-PREF-001 線状降水帯15都道府県ページ展開

- status: `IN_PROGRESS`
- priority: `A`
- approved_spec: 全国的な発生傾向・重要事例を持つ10県に、ユーザー指定の東京・大阪・愛知（名古屋重点）・石川・富山を加えた15都道府県を対象とする。県別の時系列発生史を厚くし、ページごとの差別化を行い、避難場所・ハザード情報への実用導線を持たせる。
- completion_criteria: 15都道府県の一次情報調査 / B082〜B096のMarkdown・preview・registry / 県固有年表 / 避難導線 / 地方・全国記事との内部リンク / テンプレ過多防止レビュー / CI / 本番スモーク / ユーザー確認
- done: 15都道府県とB082〜B096のID、3バッチ構成、歴史データの扱い、避難場所ポリシーを `docs/research/LINEAR_RAINBAND_PREFECTURE_PLAN_20260921.md` に定義。
- remaining: Batch 1（鹿児島・宮崎・熊本・長崎・大分）、Batch 2（高知・和歌山・三重・静岡・千葉）、Batch 3（東京・大阪・愛知・石川・富山）の作成・検証。
- next_action: Batch 1の一次情報を記事化し、県別ナビ・registry・テストを追加する。
- blocker: なし
- related: `docs/research/LINEAR_RAINBAND_PREFECTURE_PLAN_20260921.md`, B067〜B077
- updated_at: `2026-09-21`
- user_approval: `NO`

### SEO-001 水害系記事のカニバリ再確認

- status: `TODO`
- priority: `B`
- approved_spec: 実データと検索意図を見て、機械的な統合はしない。
- completion_criteria: 対象ページ整理 / 意図比較 / GSCデータがあれば照合 / 対応判断 / ユーザー確認
- done: 候補として記録済み。
- remaining: 調査一式。
- next_action: 水害系の近接テーマを一覧化する。
- blocker: なし
- related: `docs/research/SEO_IMPLEMENTATION_STATUS_20260912.md`
- updated_at: `2026-09-21`
- user_approval: `NO`

### CONTENT-001 長期断水×入浴・洗濯の記事検討

- status: `TODO`
- priority: `B`
- approved_spec: 新規記事化前に検索意図・既存記事・一次情報を確認する。
- completion_criteria: 調査 / カニバリ確認 / brief判断 / 必要なら記事作成・レビュー・ユーザー承認
- done: 候補登録のみ。
- remaining: 調査。
- next_action: 既存断水記事との役割差を確認する。
- blocker: なし
- related: `docs/research/SEO_IMPLEMENTATION_STATUS_20260912.md`
- updated_at: `2026-09-21`
- user_approval: `NO`

### CONTENT-002 避難所×防犯／女性・子どもの記事検討

- status: `TODO`
- priority: `B`
- approved_spec: 安全性と一次情報を優先し、センシティブな内容を煽情的に扱わない。
- completion_criteria: 一次情報調査 / 検索意図 / リスクレビュー / brief判断 / 必要なら記事作成・ユーザー承認
- done: 候補登録のみ。
- remaining: 調査。
- next_action: 公的ガイド・既存記事との重複を確認する。
- blocker: なし
- related: `docs/research/SEO_IMPLEMENTATION_STATUS_20260912.md`
- updated_at: `2026-09-21`
- user_approval: `NO`

### CONTENT-003 内水氾濫と洪水の違いの独立記事化再評価

- status: `TODO`
- priority: `C`
- approved_spec: B005/B020とのカニバリを避け、独立した読者意図がある場合だけ記事化する。
- completion_criteria: 検索意図 / 既存記事比較 / 独立価値判断 / ユーザー確認
- done: 候補登録のみ。
- remaining: 調査。
- next_action: B005/B020の既存カバー範囲を確認する。
- blocker: なし
- related: `docs/research/SITEWIDE_CONTENT_GAP_REVIEW_20260905.md`
- updated_at: `2026-09-21`
- user_approval: `NO`

### CONTENT-004 災害時の口腔ケア記事候補

- status: `TODO`
- priority: `C`
- approved_spec: 医療・衛生上の重要主張は一次情報で確認し、商品紹介を主目的にしない。
- completion_criteria: 需要調査 / 一次情報 / 既存記事比較 / 記事化判断 / ユーザー確認
- done: 候補登録のみ。
- remaining: 調査。
- next_action: 公的情報と検索需要を確認する。
- blocker: なし
- related: `docs/research/SITEWIDE_CONTENT_GAP_REVIEW_20260905.md`
- updated_at: `2026-09-21`
- user_approval: `NO`

### EXPAND-001 大雪・寒波、雷・竜巻等の新災害カテゴリ検討

- status: `TODO`
- priority: `C`
- approved_spec: 単発記事ではなく、ナビゲーション・カテゴリ・関連記事群を含むIAを先に設計する。
- completion_criteria: 対象災害選定 / 需要・一次情報調査 / IA案 / 記事群案 / ユーザー承認
- done: 候補登録のみ。
- remaining: 企画判断。
- next_action: 既存カテゴリ構成との整合を評価する。
- blocker: なし
- related: `docs/research/SITEWIDE_CONTENT_GAP_REVIEW_20260905.md`
- updated_at: `2026-09-21`
- user_approval: `NO`

### UI-001 サイトファビコン導入

- status: `USER_CONFIRMATION_PENDING`
- priority: `B`
- approved_spec: 防災くらしガイドのブランドに合う正方形ファビコンを実ファイルで配置し、全公開ページから安定URLで参照する。
- completion_criteria: favicon実ファイル / 全公開HTMLのlink rel=icon / 64x64確認 / ビルド・テストPASS / 本番HTTP確認 / ユーザー確認
- done: 現行ブランド色を基準に「盾＋家」案の64x64 PNGを追加。全公開HTMLへ `/favicon.png` を自動挿入し、64x64 PNG・全HTML参照の回帰テストを追加。PR #108をマージし、deploy run #86でテスト・ビルド・FTPSデプロイ・本番スモークまでPASS。
- remaining: ユーザーによるブラウザタブ等での表示確認とデザイン承認。
- next_action: ユーザーが本番ファビコン表示とデザインを確認する。
- blocker: ユーザー確認待ち
- related: `scripts/build_public.py`, `tests/test_public_build.py`, PR #108, deploy run #86
- updated_at: `2026-09-21`
- user_approval: `NO`

### MOBILE-001 モバイル実機レビュー

- status: `DONE`
- priority: `-`
- approved_spec: 実スマートフォンで主要画面の操作感と表示崩れを確認する。
- completion_criteria: ユーザー実機確認 / 問題有無の報告 / 問題は別タスク化
- done: 2026-09-21 ユーザーから「モバイル画面は問題なさそう」と確認。線状降水帯の実画像未掲載はIMG-001として別管理。
- remaining: なし
- next_action: なし
- blocker: なし
- related: `docs/SITE_IMPROVEMENT_BACKLOG.md`
- updated_at: `2026-09-21`
- user_approval: `YES`
