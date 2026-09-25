# Event & Tokutenkai Flyer Plugin for Antigravity CLI

アイドルやアーティストの**リリースイベント（リリイベ）、ミニライブ、特典会（撮影会・お話し会・動画撮影等）**の告知フライヤーや案内資料を作成するための Antigravity CLI プラグインです。

公式サイトや告知ページ（一次情報）から「タイムテーブル」「購入レギュレーション（点数制限・ループ可否）」「会場フロアマップ」「撮可TIMEと撮影会の峻別」「メンバーのイメージカラー」などを厳密かつ的確に構造化し、後から文字やフォント、配色を自由に編集できる印刷用ベクターPDF（A4）および高精細PNG（4K解像度対応）をコードベース（Design as Code）で作成・ビルドします。

---

## 主な特徴とドメイン機能

* 🎤 **イベント・特典会ドメイン知識の体系的適用**:
  * **会場情報のヘッダー統合（独立カード廃止）**: 会場・アクセス情報をヘッダー内の会場行（`.header-loc-row`）に集約し、タイムライン先頭の独立カードを廃止して貴重な縦スペース（約15mm）を確保。
  * **出演者一覧チップとメンバーカラー反映**: 出演者をヘッダー内にチップ形式（`.member-chip`）で配置。公式カラーがある場合は忠実に反映し、未設定グループ（スタプラ研究生等）は組分けチップ（`.team-chip`）で整理。
  * **撮可（撮影可能）TIMEと特典会（撮影会）の厳格な峻別**: ライブ本編中の特例撮影時間（撮可TIME）と、特典券を消費する個別/グループ撮影会を別枠として明確に分離。
  * **購入レギュレーションの即応タグ配置**: 1会計の上限点数、対象品番（`BTRC-XXXX` 等）と盤種、買い増し並び直し（ループ）の可否・解除アナウンス手段を目立つアラートタグとして配置。
  * **一次情報にない事実の推測禁止（事実の厳格性）**: 告知に書かれていない機材制限（「一眼レフ可」等）を勝手に推測・断定せず、公式注意事項（手荷物自己管理、マスク着用義務等）を過不足なく忠実に記載。
  * **箇条書きの組版原則（`<ul><li>`）**: 「・」と `<br>` による疑似箇条書きを排除し、セマンティックな `<ul><li>` とぶら下がりインデントを徹底。
* 📐 **縦長フロアマップ（会場図面）と入場案内の空間統合**:
  * ステージを上部に配した縦長比率（アスペクト比 3:4 程度）で会場図（ベクターSVG）を再構成し、並列する優先観覧・整理番号入場案内の横幅を確保。
* ✂️ **徹底した文字削減とピクトグラム／アイコン化**:
  * **自明な定型文の排除**: 「定員に達し次第終了」「なくなり次第終了」などの自明な事務定型文を完全削除し、紙面をスリム化。
  * **ポエム・装飾的惹句の排除（事実の純化）**: 「〜屋上特設ステージでの全開パフォーマンス！」のような修飾文を全廃し、「ミニライブ」など来場者が知るべき事実のみに純化。
  * **進行順カラムの極小化（数字のみ）**: 特典会テーブルの進行順ヘッダーを「#」、セルを数字「1」「2」のみとし、内容・レギュレーション欄の横幅（約67%）を最大限に確保。進行順が不明な場合はカラム自体を省略。
  * **ベクターSVGアイコンの活用**: 傘禁止、撮影禁止、スマホ限定、接触禁止、手ぶら・荷物カゴなどの共通ピクトグラムをベクターSVG（`assets/icons/`）として同梱し、Chromium / Skia PDF レンダラーの絵文字クラッシュを回避しつつ直感的な視覚伝達を実現。
* 📱 **印刷用ベクターQRコードの鮮明出力と免責バー統一**:
  * **スダレ線化バグの恒久防止**: Chromium / Skia PDF レンダラーのサブピクセル丸め誤差による縦ストローク消失（横縞スダレ線化）を防ぐため、`<img>` 自体には直接 `padding`/`border` を付与せず親コンテナ（`.qr-container`）で白座布団を設計。
  * **AI自動生成・非公式案内の免責バー一本化**: ヘッダーのAIバッジを撤廃し、紙面最下部のフッター免責バー（`.footer-disclaimer`）に「【AI生成・非公式】」と元サイト確認案内を集約。
* 🖼️ **特典会共通イラストアセット＆リファレンス同梱**:
  * 全員お見送り会、2ショット撮影、動画撮影付きお見送り、個別お話し会、ユニット集合撮影、後ろ向き推し2shot、サイン会、CD手渡し会・お渡し会の共通イメージ（イラスト8種）を同梱。
  * キャラクター（メンバー・参加者・スタッフ）、会場備品（長机・椅子・カゴ・スマホ・アクリル板撤廃）、アイテム・グッズ（生写真・チェキ・CD・Mカード・ポスター・ペンライト・Tシャツ・タオル等）のリファレンスシートにより、特殊な特典会やグッズも統一スタイルで都度生成可能（ファンのマイク保持禁止・完全手ぶら原則を厳守）。
* 🎨 **デザイントークンによる複数世界観の即時展開**:
  * セマンティックHTMLとデザイントークン（CSS変数）を分離し、和モダン、サイバーポップ、スタイリッシュなど複数のトーン＆マナーを瞬時に切り替え可能。
* 🖨️ **完全ベクターPDFと4K解像度PNG出力**:
  * A4サイズ（210×297mm）1枚に美しく収まる組版。
  * 拡大しても文字や罫線がボケないベクターPDF、および4Kディスプレイやスマートフォンでも鮮明に読める高精細PNG（2480×3508px）を出力。
* 🔍 **公式URLからの決定論的情報抽出・正規化ツール（AI独自判断の排除）**:
  - 公式告知URLからHTML構造・ブロック境界を解析し、公演概要、出演者組分け、タイムテーブル、対象商品、優先入場案内、特典会くじ内訳、撮可制限、注意事項を漏れなく決定論的に抽出。
  - AIの解釈ブレや拾い漏れを防ぎ、自明な定型文の自動フィルタリング、進行順番号の正規化を行った要約Markdown（`event_summary.md`）および構造化JSON（`event_data.json`）を生成。
* 📐 **エリア図の推測配置厳禁と並列・未定注記原則**:
  - 公式情報から位置関係（前方/後方）が断定できないエリア（HAJIMAREエリア、ファミリーエリア等）を勝手に推測配置せず、並列破線枠＋「※実際の配置・区分けは当日の案内看板・係員の指示をご確認ください」の注記を義務化。
* 🎤 **観覧マナー・レギュレーションのミニライブ枠（STEP 3）直接統合**:
  - 入場案内と混同せず、コール声援・ジャンプ禁止・危険行為・滞留禁止などの観覧マナーを「STEP 3: ミニライブ」枠内に直接2カラムFlexboxとして統合。
* 🎁 **特典会詳細枠のデッドスペース完全排除と多層高密度コンポーネント**:
  - 参加5ステップ案内フロー、4大禁止事項、1部・2部差分ダブルテーブル、3レーン割り当て、参加前4大FAQ、注意事項を隙間なく配置し、圧倒的な情報密度と満足度を両立。
* 🛑 **Chromium / Skia PDF レンダラーの内部クラッシュ完全防止**:
  - 特定のOpenType絵文字クラッシュ（`⚠️` 等のフォールバック失敗）の排除、サブピクセル極小境界線（`border: 0.3pt/0.4pt`）の排除、Flexbox内Gridネストの排除により、印刷時のエンジンクラッシュを根本防止。
* 🔍 **余白・デッドスペース自動検出・検証 (`flyer.py check-space`)**:
  - PyMuPDF を用いてテキスト・画像ボックス間の垂直ギャップを自動測定し、閾値（25mm等）を超える空白が存在しないかを決定論的に検査。
* ⚡ **ゼロインストールCLI（`npx`, `uv`, `flyer.py`）による即時ビルド・検証・プレビュー**:
  - `flyer.py all` により、ワンコマンドで「PDFビルド ➔ A4 1ページ厳守判定 ➔ 余白検査 ➔ 300dpi高精細PNGプレビュー生成」を一気通貫で実行。macOS 固有コマンド（`qlmanage`, `mdls`）や外部 Swift 不要。

---

## ディレクトリ構成

```text
event-tokutenkai-plugin/
├── plugin.json               # プラグインマニフェスト
├── README.md                 # プラグイン説明書
├── rules/
│   └── AGENTS.md             # イベント・特典会デザイン行動原則
└── skills/
    └── event-tokutenkai/
        ├── SKILL.md          # タイムテーブル・レギュレーション構築＆PDFビルドガイド
        ├── assets/
        │   ├── icons/        # 印刷用ベクターSVGピクトグラム（Skiaクラッシュ防止）
        │   │   ├── bag-basket.svg     # 手ぶら・荷物カゴ
        │   │   ├── no-camera.svg      # 撮影禁止
        │   │   ├── no-touch.svg       # 接触禁止
        │   │   ├── no-umbrella.svg    # 傘禁止
        │   │   └── smartphone-only.svg# スマホ限定
        │   └── illustrations/# 特典会共通イラスト＆リファレンス画像
        │       ├── reference-characters.jpg # キャラクターモデルシート
        │       ├── reference-props.jpg      # 会場備品・道具セット
        │       ├── reference-goods.jpg      # アイテム・グッズセット（生写真・チェキ・CD・Mカード等）
        │       ├── tokuten-sendoff.jpg      # 全員お見送り会
        │       ├── tokuten-2shot.jpg        # 2ショット撮影会
        │       ├── tokuten-video-sendoff.jpg# 動画撮影付きお見送り会
        │       ├── tokuten-talk.jpg         # 個別お話し会
        │       ├── tokuten-group-shot.jpg   # ユニット集合撮影
        │       ├── tokuten-back-oshi-2shot.jpg # 後ろ向き推し2shot
        │       ├── tokuten-autograph.jpg    # サイン会
        │       └── tokuten-handover.jpg     # CD手渡し会・お渡し会
        ├── scripts/
        │   ├── build.sh      # 統一ビルドスクリプト
        │   ├── extract_event.py # 公式URL情報抽出・構造化スクリプト
        │   └── flyer.py      # 一括ビルド・検証・プレビューCLIツール
        └── templates/
            ├── html-paged/   # HTML/CSS Paged Media テンプレート
            │   ├── assets/icons/ # SVGピクトグラム
            │   ├── index.html
            │   ├── theme.css # デザイントークン（色・余白・メンバーカラー）
            │   ├── layout.css# @page、タイムライン、フロアマップ、テーブル、QR
            │   └── qr.svg    # 印刷用ベクターQRコード（サンプル）
            └── typst/        # Typst テンプレート
                └── flyer.typ # 高速・高精度組版ソース
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

本プラグインには、URL情報抽出・PDFビルド・1ページ検証・高精細PNG生成・ベクターQRコード生成を高速に行う内製CLIツール [`skills/event-tokutenkai/scripts/flyer.py`](file:///skills/event-tokutenkai/scripts/flyer.py) が同梱されています（Python & `uv` 対応）。

### 0. 公式URLからの決定論的情報抽出 (`extract`・必須先行ステップ)

AIが自身の場当たり的な判断で情報を集めるのを防ぎ、公演概要・組分け・タイムテーブル・商品・優先観覧・特典会くじ・注意事項を網羅的に抽出して整理します。

```bash
# 公式URLから情報を抽出し、整理された要約Markdownと構造化JSONを出力
uv run python skills/event-tokutenkai/scripts/flyer.py extract "https://starplanet-academy.com/schedule/item-359/" \
  -o event_summary.md \
  --json event_data.json
```

### 1. ビルド・検証・プレビューの一括実行（パイプライン・推奨）

ワンコマンドで「PDFビルド ➔ A4 1ページ厳守判定 ➔ 300dpi（2481×3508px）高精細PNG生成」を一気通貫で実行します。

```bash
# HTML から PDF と高精細PNGプレビューを一括生成
uv run python skills/event-tokutenkai/scripts/flyer.py all index.html

# 出力ファイル名を明示する場合
uv run python skills/event-tokutenkai/scripts/flyer.py all index.html -o output.pdf --preview output.png --dpi 300
```

### 2. 個別機能の利用

#### A. PDF のビルド (`build`)
```bash
# HTML (Vivliostyle)
uv run python skills/event-tokutenkai/scripts/flyer.py build index.html -o output.pdf

# WeasyPrint を明示する場合
uv run python skills/event-tokutenkai/scripts/flyer.py build index.html -o output.pdf --engine weasyprint

# Typst
uv run python skills/event-tokutenkai/scripts/flyer.py build flyer.typ -o output.pdf
```

#### B. ページ数・A4寸法の検証 (`pages` / `verify`)
チラシ・フライヤーがA4 1枚に美しく収まっているかを厳格に検査します（超過時は終了コード 1）。
```bash
uv run python skills/event-tokutenkai/scripts/flyer.py pages output.pdf --expect 1
```

#### C. 余白・デッドスペース（垂直ギャップ）の検査 (`check-space` / `space`)
PDF 内のテキスト・画像ボックス間の垂直ギャップを自動検出し、余白過多（デッドスペース）がないかを検査します。
```bash
# デフォルト（最大許容ギャップ 20mm）で検査
uv run python skills/event-tokutenkai/scripts/flyer.py check-space output.pdf

# 閾値を指定し、超過時にエラー終了する場合（CI / 自動検証向け）
uv run python skills/event-tokutenkai/scripts/flyer.py check-space output.pdf --max-gap 25.0 --strict
```

#### D. 4K解像度（300dpi相当）PNGプレビューの生成 (`render` / `preview`)
macOS の `qlmanage` や Swift スクリプトに依存せず、PyMuPDF によりクロスプラットフォームで高速に 300dpi 高解像度 PNG（2481×3508px）を出力します。
```bash
uv run python skills/event-tokutenkai/scripts/flyer.py render output.pdf -o output.png --dpi 300
```

#### E. 印刷用ベクター SVG QR コード生成 (`qr`)
外部CLI（`npx qrcode` 等）を使わず、Python ライブラリで直接ベクター SVG の QR コードを生成します。
```bash
uv run python skills/event-tokutenkai/scripts/flyer.py qr "https://starplanet-academy.com/schedule/item-359/" -o qr.svg
```

### 3. シェルスクリプトを使う場合 (`build.sh`)

```bash
# flyer.py のパイプラインをシェルスクリプト経由で実行
./skills/event-tokutenkai/scripts/build.sh auto index.html output.pdf output.png
./skills/event-tokutenkai/scripts/build.sh typst flyer.typ output.pdf output.png
```

---

## ライセンス

MIT License
