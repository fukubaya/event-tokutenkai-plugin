# Event & Tokutenkai Flyer Plugin for Antigravity CLI (v0.2.0)

アイドルやアーティストの**リリースイベント（リリイベ）、ミニライブ、特典会（撮影会・お話し会・お渡し会等）**の告知フライヤーや案内資料を作成するための Antigravity CLI プラグインです。

公式サイトや告知ページ（一次情報）から「タイムテーブル」「購入レギュレーション（点数制限・ループ可否）」「会場フロアマップ」「撮可TIMEと撮影会の峻別」「メンバーのイメージカラー」などを厳密かつ的確に構造化し、後から文字やフォント、配色を自由に編集できる印刷用ベクターPDF（A4）および高精細PNG（4K解像度対応）をコードベース（Design as Code）で作成・ビルドします。

さらに **v0.2.0** では、従来のA4単枚印刷フライヤーに加え、スマートフォン・SNS（X/Twitter等）での閲覧に特化した**「SNS告知用 4枚カルーセル戦略」**に完全対応しました。

---

## 主な特徴とドメイン機能

* 📱 **SNS告知用 4枚カルーセル戦略（スマートフォン・縦長画面最適化）**:
  * **1枚目［超集約サマリー］**: タイムテーブルの項目間を詰めて縦を短縮し、来場者の最大関心事である特典会目玉メニュー（お話し会、2shot、グルショ、フリーお手振り等）を特大配置。最下部の冗長な注意事項枠を全廃し、スマホ1画面で要点が即座に伝わる構成。
  * **2枚目［販売〜優先入場］**: 対象商品情報（品番・価格・付与券）、購入上限・ループ可否、キャッシュレス決済ピクト、整理番号入場ステップ、会場フロアマップ（D2ベクターSVG）を体系的に整理。
  * **3枚目［ライブ〜特典会詳細］**: 撮可TIME（スマホ限定・対象曲・動画可否）、観覧マナー、特典会プレビュー行（縦並びカードで視認性向上）、進行フロー、詳細レギュレーション表、手ぶら整列等のマナーストリップを完備。
  * **4枚目［全体が分かる1枚］**: 従来の総合フライヤー（A4 1枚版と同等）を収録。全体のスケジュール・物販・ライブ・特典会・会場マップを網羅。
  * **全スライド単体成立ヘッダー**: どの画像単体で見ても一次情報にアクセスできるよう、タイトル・日程・会場情報に加え、公式告知ページへの短縮URLと印刷用ベクターQRコード（`qr.svg`）をヘッダー右上に統合。スライド番号バッジ（現在地バッジ）を排除して有効面積を最大化。
  * **デッドスペースの徹底排除**: 縦方向の無駄な余白を排除し、A4（210×297mm）縦長画面で文字・表・イラスト・マップを可能な限り大きく配置。

* 🎫 **特典券システムの厳格な峻別と金額表記のスマート化**:
  * **「共通券消費型」と「メニュー別専用券型」の峻別**:
    * **共通券消費型**: 1商品で共通特典券1枚を付与し、メニューごとに1〜3枚消費する方式（スタアカ等）。
    * **メニュー別専用券型**: メニューごとに独立した専用券が存在し、参加時の提出はすべて「専用券 1枚」となる方式（ばってん少女隊等）。購入商品点数（1枚購入で①〜③選択、2枚購入で④グルショ等）との混同を厳格に防止。
  * **露骨な金額表記の排除**: 特典会メニュー枠に直接金額を書かず、販売開始行に付与条件バッジ（例: `Mカード1枚（¥3,000）で専用券1枚進呈`）を設け、各メニューは「専用券 1枚」「券不要」のみに純化。

* 🗺️ **D2 ベクターフロアマップの自動コンパイルと厳格な運用**:
  * **推測による架空マップ作成の絶対禁止**: 公式告知ページにエリア分け図面や配置図が明確に掲載されている場合のみ作成。時間が異なるだけの同一会場を別室のように図解する重大な誤認を防止。
  * **D2スクリプト自動コンパイル**: `floormap1.d2`, `floormap2.d2` から、外枠余白ゼロ（`--pad 0`）かつライトテーマ（`--theme 0`）で高密度・鮮明なベクターSVGを自動生成。
  * **フロアマップと入場案内の配色完全同期**: フロアマップで定義した各エリアのカラー（優先、女性、お子様、フリー、カメラ等）と、入場案内リストのステップ番号バッジ・注記テキストの背景色・文字色を1対1で完全同期。

* 🎤 **イベント・特典会ドメイン知識の体系的適用**:
  * **会場情報のヘッダー統合（独立カード廃止）**: 会場・アクセス情報をヘッダー内の会場行（`.header-loc-row`）に集約し、タイムライン先頭の独立カードを廃止して貴重な縦スペース（約15mm）を確保。
  * **出演者一覧チップとメンバーカラー反映**: 出演者をヘッダー内にチップ形式（`.member-chip`）で配置。公式カラーがある場合は忠実に反映し、未設定グループ（スタプラ研究生等）は組分けチップ（`.team-chip`）で整理。特典会テーブル内やタイムテーブル内のメンバー名もカラーチップで統一。
  * **撮可（撮影可能）TIMEと特典会（撮影会）の厳格な峻別**: ライブ本編中の特例撮影時間（撮可TIME）と、特典券を消費する個別/グループ撮影会を別枠として明確に分離。「指示がない場合での撮影禁止」を「撮可なし・全面禁止」と勝手に決めつける誤読を防止。
  * **一次情報にない事実の推測禁止（事実の厳格性）**: 告知に書かれていない機材制限（「一眼レフ可」等）を勝手に推測・断定せず、公式注意事項（手荷物自己管理、マスク着用義務等）を過不足なく忠実に記載。
  * **新規・先行特典の正式統合**: 「新規・カムバック向けフリーお手振り会」などの無償枠を別枠テキストに逃さず、特典会テーブル最上行に「先行」「券不要」として正式に組み込み。

* ✂️ **徹底した文字削減とピクトグラム／アイコン化**:
  * **自明な定型文の排除**: 「定員に達し次第終了」「なくなり次第終了」などの自明な事務定型文を完全削除し、紙面をスリム化。
  * **ポエム・装飾的惹句の排除（事実の純化）**: 「〜屋上特設ステージでの全開パフォーマンス！」のような修飾文を全廃し、「ミニライブ」など来場者が知るべき事実のみに純化。
  * **ベクターSVGアイコン全29種の活用**: 傘禁止、撮影禁止、スマホ限定、接触禁止、手ぶら・荷物カゴ、キャッシュレス決済などの共通ピクトグラムをベクターSVG（`assets/icons/`）として同梱し、Chromium / Skia PDF レンダラーの絵文字クラッシュを回避しつつ直感的な視覚伝達を実現。

* 📱 **印刷用ベクターQRコードの鮮明出力とスダレ線化バグの恒久防止**:
  * Chromium / Skia PDF レンダラーのサブピクセル丸め誤差による縦ストローク消失（横縞スダレ線化）を防ぐため、`<img>` 自体には直接 `padding`/`border` を付与せず親コンテナ（`.qr-container`）で白座布団を設計。
  * 外部CLI（`npx qrcode` 等）を使わず、Python内製ライブラリで直接ベクターSVGのQRコードを即時生成。

* 🖼️ **特典会共通イラストアセット10種＆リファレンス3種同梱**:
  * **特典会イラスト全10種**:
    1. 全員お見送り会（`tokuten-sendoff.jpg`）
    2. 動画撮影付きお見送り会 / 動画お手振り会（`tokuten-video-sendoff.jpg`）
    3. 個別お話し会（`tokuten-talk.jpg`）
    4. 2ショット撮影会（`tokuten-2shot.jpg`）
    5. パーテーション越し2ショット撮影会（`tokuten-2shot-partition.jpg`）
    6. 後ろ向き推し2shot（`tokuten-back-oshi-2shot.jpg`）
    7. ユニット・グループ集合撮影会（`tokuten-group-shot.jpg`）
    8. フォトセッション / 囲み撮影会（`tokuten-photosession.jpg`）
    9. サイン会（`tokuten-autograph.jpg`）
    10. CD手渡し会・お渡し会（`tokuten-handover.jpg`）
  * **生成・統一用リファレンスシート3種**:
    1. キャラクターモデルシート（`reference-characters.jpg`）: メンバー、参加者、スタッフの服装・頭身基準
    2. 会場備品・道具セット（`reference-props.jpg`）: 長机、椅子、荷物カゴ、スマホ、パーテーション等
    3. アイテム・グッズセット（`reference-goods.jpg`）: 生写真、チェキ、CD、Mカード、ペンライト、タオル等
  * 正方形イラスト（1:1）の上下トリミングを防ぐため、コンテナに十分な高さを確保し `object-fit: contain;` ＋白背景で完全表示。

* 🎨 **デザイントークンによる複数世界観の即時展開**:
  * セマンティックHTMLとデザイントークン（CSS変数）を分離し、シーズン・イベント連動、公式ブランド制服、会場・ロケーション連動など複数のトーン＆マナーを瞬時に切り替え可能。
  * macOS（ヒラギノ各種）および Windows（游ゴシック、游明朝、メイリオ等）のOS標準高品質フォントをスタック上位に配置し、フォント遅延や文字化けを完全防止。

* 🔍 **公式URLからの決定論的情報抽出・正規化ツール (`flyer.py extract`)**:
  * 公式告知URLからHTML構造を解析し、公演概要、出演者組分け、タイムテーブル、対象商品、優先入場案内、特典会、撮可制限、注意事項を決定論的に抽出。要約Markdown（`event_summary.md`）および構造化JSON（`event_data.json`）を自動生成。

* ⚡ **ゼロインストールCLI（`uv run python flyer.py`）による即時ビルド・検証・プレビュー**:
  * 単枚フライヤーの一括ビルド（`all`）、4枚カルーセルの一括ビルド（`carousel`）、ページ数・A4寸法チェック（`pages`）、余白検査（`check-space`）、300dpi高精細PNGレンダリング（`render`）を一気通貫でサポート。

---

## ディレクトリ構成

```text
event-tokutenkai-plugin/
├── plugin.json               # プラグインマニフェスト (v0.2.0)
├── README.md                 # プラグイン説明書
├── rules/
│   └── AGENTS.md             # イベント・特典会デザイン行動原則・厳守ルール
└── skills/
    └── event-tokutenkai/
        ├── SKILL.md          # タイムテーブル・レギュレーション構築＆PDFビルドガイド
        ├── assets/
        │   ├── icons/        # 印刷用ベクターSVGピクトグラム（全29種同梱）
        │   │   ├── bag-basket.svg         # 手ぶら・荷物カゴ
        │   │   ├── camera.svg             # 撮可TIME（静止画）
        │   │   ├── cash.svg               # 現金決済
        │   │   ├── check-ok.svg           # OK・許可
        │   │   ├── cheering.svg           # コール・声出しOK
        │   │   ├── clock.svg              # 時計・時刻
        │   │   ├── credit-card.svg        # クレジットカード決済
        │   │   ├── group-shot.svg         # グループshot
        │   │   ├── hand-wave.svg          # お手振り会
        │   │   ├── location.svg           # 会場ピン・場所
        │   │   ├── mic.svg                # ライブ・ステージ・MC
        │   │   ├── no-camera.svg          # 撮影禁止
        │   │   ├── no-jump.svg            # ジャンプ・リフト禁止
        │   │   ├── no-prop.svg            # 小道具持たせ禁止
        │   │   ├── no-screen-record.svg   # 画面録画・LivePhoto禁止
        │   │   ├── no-sit.svg             # 着席強要・しゃがみ禁止
        │   │   ├── no-stepladder.svg      # 脚立・踏み台禁止
        │   │   ├── no-touch.svg           # 接触禁止
        │   │   ├── no-umbrella.svg        # 傘・日傘禁止
        │   │   ├── no-video.svg           # 録画禁止
        │   │   ├── prohibit.svg           # NG・禁止
        │   │   ├── qr-pay.svg             # QR・電子マネー決済
        │   │   ├── smartphone-only.svg    # スマホ限定
        │   │   ├── sun.svg                # 熱中症対策・屋外案内
        │   │   ├── talk.svg               # 個別お話し会
        │   │   ├── ticket.svg             # 特典券・参加券
        │   │   ├── two-shot.svg           # 2shot撮影
        │   │   ├── video.svg              # 動画可・動画撮影
        │   │   └── warning.svg            # 注意・警告
        │   └── illustrations/# 特典会共通イラスト10種＆リファレンス3種（計13種同梱）
        │       ├── reference-characters.jpg    # キャラクターモデルシート（メンバー/ファン/スタッフ）
        │       ├── reference-props.jpg         # 会場備品・道具セット（長机/椅子/カゴ/スマホ等）
        │       ├── reference-goods.jpg         # アイテム・グッズセット（生写真/チェキ/CD/Mカード等）
        │       ├── tokuten-sendoff.jpg         # 全員お見送り会
        │       ├── tokuten-video-sendoff.jpg   # 動画撮影付きお見送り会（動画お手振り会）
        │       ├── tokuten-talk.jpg            # 個別お話し会
        │       ├── tokuten-2shot.jpg           # 2ショット撮影会
        │       ├── tokuten-2shot-partition.jpg # パーテーション越し2ショット撮影会
        │       ├── tokuten-back-oshi-2shot.jpg # 後ろ向き推し2shot
        │       ├── tokuten-group-shot.jpg      # ユニット・グループ集合撮影会
        │       ├── tokuten-photosession.jpg    # フォトセッション・囲み撮影会
        │       ├── tokuten-autograph.jpg       # サイン会
        │       └── tokuten-handover.jpg        # CD手渡し会・お渡し会
        ├── scripts/
        │   ├── build.sh      # 統一ビルドスクリプト
        │   ├── extract_event.py # 公式URL情報抽出・構造化スクリプト
        │   └── flyer.py      # 一括ビルド・検証・プレビュー・カルーセルCLIツール
        └── templates/
            ├── carousel/     # SNS告知用 4枚カルーセルテンプレート
            │   ├── index.html        # 4枚組スライドHTML（超集約/物販/ライブ特典会/総合）
            │   ├── carousel.css      # スライド分割・大文字・余白最適化スタイル
            │   ├── theme.css         # デザイントークン（カラー・フォント・余白）
            │   ├── theme-autumn.css  # 秋ツアー・ウォームテーマ
            │   ├── theme-academy.css # アカデミー・ネイビー＆ゴールドテーマ
            │   ├── theme-parco.css   # パルコ・ルーフトップテーマ
            │   ├── bg-autumn.svg     # 背景ベクターパターン（秋）
            │   ├── bg-academy.svg    # 背景ベクターパターン（制服チェック）
            │   ├── bg-parco.svg      # 背景ベクターパターン（青空・ポップ）
            │   └── assets/           # アイコン・イラストへのシンボリックリンク
            ├── html-paged/   # 印刷用 A4単枚フライヤーテンプレート
            │   ├── index.html        # セマンティック構造化HTML
            │   ├── layout.css        # A4 1ページ厳守印刷レイアウト
            │   ├── theme.css         # デザイントークン定義
            │   ├── theme-autumn.css  # 秋ツアー・ウォームテーマ
            │   ├── theme-academy.css # アカデミー・ネイビー＆ゴールドテーマ
            │   ├── theme-parco.css   # パルコ・ルーフトップテーマ
            │   ├── bg-autumn.svg
            │   ├── bg-academy.svg
            │   ├── bg-parco.svg
            │   └── qr.svg
            ├── d2/           # 会場フロアマップ用 D2 言語テンプレート
            │   ├── floormap_grid_front.d2   # グリッド箱区切り（前方特設エリア）
            │   ├── floormap_grid_nested.d2  # グリッド箱区切り（多層エリア）
            │   ├── floormap_v_simple.d2     # 縦長シンプル3段（ステージ/優先/フリー）
            │   ├── floormap_v_nested.d2     # 縦長多層（女性限定・左右分割等）
            │   └── floormap_v_tiered.d2     # 縦長前方段状構成
            └── svg/          # 会場フロアマップ ベクターSVGサンプル
                ├── floormap_v_simple.svg
                ├── floormap_v_nested.svg
                ├── floormap_v_tiered.svg
                └── floormap_h_nested.svg
```

---

## インストール方法

### 方法1: グローバルプラグインとして登録（推奨）

ユーザー設定ディレクトリ `~/.gemini/config/plugins/` にクローンします。

```bash
git clone https://github.com/fukubaya/event-tokutenkai-plugin.git ~/.gemini/config/plugins/event-tokutenkai-plugin
```

### 方法2: 特定のプロジェクト（ワークスペース）で使う場合

プロジェクトルートの `.agents/plugins/` 配下にクローンします。

```bash
mkdir -p <project-root>/.agents/plugins
git clone https://github.com/fukubaya/event-tokutenkai-plugin.git <project-root>/.agents/plugins/event-tokutenkai-plugin
```

---

## 使い方・コマンド一覧

本プラグインには、URL情報抽出・PDFビルド・1ページ検証・高精細PNG生成・カルーセル分割生成・ベクターQRコード生成を高速に行う内製CLIツール [`skills/event-tokutenkai/scripts/flyer.py`](file:///skills/event-tokutenkai/scripts/flyer.py) が同梱されています（Python & `uv` 対応）。

### 0. 公式URLからの決定論的情報抽出 (`extract`・必須先行ステップ)

AIが自身の場当たり的な判断で情報を集めるのを防ぎ、公演概要・組分け・タイムテーブル・商品・優先観覧・特典会くじ・注意事項を網羅的に抽出して整理します。

```bash
# 公式URLから情報を抽出し、整理された要約Markdownと構造化JSONを出力
uv run python skills/event-tokutenkai/scripts/flyer.py extract "https://store.battengirls.com/blogs/newstopics/20260926joka-cocoon" \
  -o event_summary.md \
  --json event_data.json
```

---

### 1. 一括ビルド・プレビュー（パイプライン・推奨）

#### A. SNS用 4枚カルーセルの一括生成 (`carousel`) 【v0.2.0 新機能】

スマートフォン・X（Twitter）投稿に特化した「4枚カルーセル（A4縦長 4枚組）」を一括生成します。
Chromiumメモリ制限を自動回避するスライス＆マージパイプラインにより、4ページのPDFと4枚の高精細PNGを一発出力します。

```bash
# カルーセルHTMLから 4ページPDF と 各スライドPNG（-p1〜-p4.png）を一括生成
uv run python skills/event-tokutenkai/scripts/flyer.py carousel carousel.html -o carousel.pdf --preview carousel.png

# 生成される成果物:
# ├── carousel.pdf    # 全4ページ結合ベクターPDF
# ├── carousel-p1.png # 【1枚目】超集約サマリー (300dpi高精細PNG)
# ├── carousel-p2.png # 【2枚目】販売〜優先入場・フロアマップ (300dpi高精細PNG)
# ├── carousel-p3.png # 【3枚目】ライブ〜特典会詳細テーブル (300dpi高精細PNG)
# └── carousel-p4.png # 【4枚目】全体総合フライヤー (300dpi高精細PNG)
```

#### B. A4単枚フライヤーの一括ビルド (`all`)

印刷用のA4単枚フライヤー向けに、「PDFビルド ➔ A4 1ページ厳守判定 ➔ 300dpi（2481×3508px）高精細PNG生成」を一気通貫で実行します。

```bash
# 単枚HTMLからPDFと高精細PNGプレビューを一括生成
uv run python skills/event-tokutenkai/scripts/flyer.py all index.html

# 出力先を明示する場合
uv run python skills/event-tokutenkai/scripts/flyer.py all index.html -o output.pdf --preview output.png --dpi 300
```

---

### 2. 個別機能の利用

#### A. PDF のビルド (`build`)
```bash
# HTML (Vivliostyle)
uv run python skills/event-tokutenkai/scripts/flyer.py build index.html -o output.pdf

# WeasyPrint を明示する場合
uv run python skills/event-tokutenkai/scripts/flyer.py build index.html -o output.pdf --engine weasyprint
```

#### B. ページ数・寸法の検証 (`pages` / `verify`)
チラシ・フライヤーが期待するページ数（A4 1枚、またはカルーセル4枚）に厳密に収まっているかを検査します（超過時は終了コード 1）。
```bash
# 1ページ厳守チェック（A4単枚フライヤー）
uv run python skills/event-tokutenkai/scripts/flyer.py pages output.pdf --expect 1

# 4ページ厳守チェック（SNS用カルーセル）
uv run python skills/event-tokutenkai/scripts/flyer.py pages carousel.pdf --expect 4
```

#### C. 余白・デッドスペース（垂直ギャップ）の検査 (`check-space` / `space`)
PDF 内のテキスト・画像ボックス間の垂直ギャップを自動検出し、余白過多（デッドスペース）がないかを検査します。
```bash
# デフォルト（最大許容ギャップ 20mm）で検査
uv run python skills/event-tokutenkai/scripts/flyer.py check-space output.pdf

# 閾値を指定し、超過時にエラー終了する場合（CI / 自動検証向け）
uv run python skills/event-tokutenkai/scripts/flyer.py check-space output.pdf --max-gap 25.0 --strict
```

#### D. 高解像度 PNG プレビューの生成 (`render` / `preview`)
macOS の `qlmanage` や Swift スクリプトに依存せず、PyMuPDF によりクロスプラットフォームで高速に 300dpi 高解像度 PNG（2481×3508px）を出力します。
```bash
# 第1ページを 300dpi でレンダリング
uv run python skills/event-tokutenkai/scripts/flyer.py render output.pdf -o output.png --dpi 300

# 全ページを一括レンダリング (-p1.png, -p2.png, ...)
uv run python skills/event-tokutenkai/scripts/flyer.py render carousel.pdf -o carousel.png --page all --dpi 300
```

#### E. 印刷用ベクター SVG QR コード生成 (`qr`)
外部CLI（`npx qrcode` 等）を使わず、Python ライブラリで直接ベクター SVG の QR コードを生成します。
```bash
uv run python skills/event-tokutenkai/scripts/flyer.py qr "https://store.battengirls.com/blogs/newstopics/20260926joka-cocoon" -o qr.svg
```

#### F. D2 ベクターフロアマップの生成 (`d2`)
D2 スクリプト（`.d2`）から、外枠余白ゼロ（`--pad 0`）かつライトテーマ（`--theme 0`）で高密度・鮮明なフロアマップ SVG を生成します。
```bash
uv run python skills/event-tokutenkai/scripts/flyer.py d2 floormap1.d2 -o floormap1.svg --theme 0 --pad 0
```
※ `flyer.py all` または `carousel` 実行時は、同ディレクトリ内の `*.d2` を自動検出し、更新差分がある場合のみ自動でSVGへコンパイルします。

---

### 3. シェルスクリプトを使う場合 (`build.sh`)

```bash
# flyer.py のパイプラインをシェルスクリプト経由で実行
./skills/event-tokutenkai/scripts/build.sh auto index.html output.pdf output.png
```

---

## ライセンス

MIT License
