# B028 画像・視覚要素メモ

確認日: 2026-09-02

## 方針

B028は特定商品の写真を記事冒頭へ置くと、情報記事より広告記事に見えやすいため、外部の商品写真をヒーロー画像として採用しない。

一方、本文画像が0枚のままでは4,000字超・20章の記事として視覚要素が不足するため、商品性能の証明にならない一般的な場面・単体物の自由利用可能画像を本文へ4点追加する。

本文では以下を主要な視覚要素とする。

- 容量Wh / 定格出力W / 重量の比較表
- 小型・中容量・1kWh級の用途別商品カード
- リチウムイオン電池の安全注意ボックス
- 定期点検チェックリスト
- 本文中の一般イメージ画像4点

正式なAmazonアソシエイト商品表示を実装する際に、Amazon側の商品画像を商品カード内へ表示する。

## IMG-B028-001 スマートフォンをモバイルバッテリーで充電する場面

- 用途: 「向く家庭・優先度が低い家庭」節の補助
- Source: https://commons.wikimedia.org/wiki/File:Charging_a_smartphone_with_a_USB_power_bank.jpg
- Image: https://commons.wikimedia.org/wiki/Special:Redirect/file/Charging%20a%20smartphone%20with%20a%20USB%20power%20bank.jpg?width=1280
- Author: Malcolm Koo / Mk2010
- License: CC BY-SA 4.0
- 内容: スマートフォンをUSBモバイルバッテリーで充電している写真
- 採用理由: スマホ充電だけなら大型ポータブル電源が不要な場合がある、という記事の判断軸を視覚的に補助できる
- 注意: ポータブル電源そのものの写真ではなく、代替手段の例としてのみ使用する
- 安全判断用途: 使用しない

## IMG-B028-002 ポータブル電源の一般例

- 用途: 用途別商品比較の後
- Source: https://commons.wikimedia.org/wiki/File:BLUETTI_2026-08-12.jpg
- Image: https://commons.wikimedia.org/wiki/Special:Redirect/file/BLUETTI%202026-08-12.jpg?width=1280
- Author: P1898
- License: CC BY 4.0
- 内容: 複数サイズのポータブル電源
- 採用理由: 容量・サイズ・重量が機種によって大きく異なる製品カテゴリであることをイメージしやすい
- 注意: 記事内で選定したAnker / Jackery製品とは別製品。商品比較、推奨、性能証明には使用しない
- 安全判断用途: 使用しない

## IMG-B028-003 LEDランタン

- 用途: 「停電時に残す電力の優先順位」付近
- Source: https://commons.wikimedia.org/wiki/File:Enbrighten_LED_Camping_Lantern.jpg
- Image: https://commons.wikimedia.org/wiki/Special:Redirect/file/Enbrighten%20LED%20Camping%20Lantern.jpg?width=1280
- Author: TaurusEmerald
- License: CC BY-SA 4.0
- 内容: LEDランタン単体
- 採用理由: 停電時に電力を残したい用途の一つである照明を、製品性能と切り離して示せる
- 注意: 特定ランタンを推奨する画像ではない
- 安全判断用途: 使用しない

## IMG-B028-004 ソーラー充電対応の携帯電源

- 用途: 「ソーラーは補充手段」節
- Source: https://commons.wikimedia.org/wiki/File:Portable_solar_power_generator-battery_for_charging_USB_devices_(21286441344).jpg
- Image: https://commons.wikimedia.org/wiki/Special:Redirect/file/Portable%20solar%20power%20generator-battery%20for%20charging%20USB%20devices%20%2821286441344%29.jpg?width=1280
- Author: Robert Ashworth
- License: CC BY 2.0
- 内容: ソーラーパネル付き携帯電源でUSB機器を充電する例
- 採用理由: ソーラー充電が「補充手段」であり、発電量は条件に左右されるという節の場面理解を補助できる
- 注意: 発電量・充電時間・防災性能の根拠には使用しない
- 安全判断用途: 使用しない

## 日本文脈

- 海外住宅・海外避難所等、生活環境の国差が大きい画像は使用しない。
- 今回追加する画像は、スマホ充電、ポータブル電源、LEDランタン、ソーラー充電という国差の小さい単体物・利用場面に限定する。
- 日本国内向けメーカー仕様、日本の経済産業省・消費者庁情報を本文の根拠とする。
- AI生成で実在製品に似せた画像は、商品性能・外観を誤認させるため使用しない。

## 重複確認

- B001〜B030の既存登録画像とファイル名・用途を照合し、同一画像の使い回しは避ける。
- B028専用の本文画像として扱う。

## 安全判断用途

画像・商品カードのみで、使用可能時間、医療機器対応、安全性、リコール有無を判断させない。容量・出力・安全性は本文、公的情報、メーカー公式仕様で確認する。

## 2026-09-02 関連性優先の再レビュー

- 新基準: 推奨画像数より、配置章との直接関連性を優先する。
- 記事で選定していないBLUETTI製品群の写真は、Anker/Jackery候補と混同するおそれがあるため本文から削除。スマホ充電、LEDランタン、ソーラー充電の一般場面3点を残す。
- 関連性の弱い実画像を枚数合わせで復活させない。
