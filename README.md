# Event & Tokutenkai Flyer Plugin for Antigravity CLI

アイドルやアーティストの**リリースイベント（リリイベ）、ミニライブ、特典会（撮影会・お話し会・動画撮影等）**の告知フライヤーや案内資料を作成するための Antigravity CLI プラグインです。

公式サイトや告知ページ（一次情報）から「タイムテーブル」「購入レギュレーション（点数制限・ループ可否）」「会場フロアマップ」「撮可TIMEと撮影会の峻別」「メンバーのイメージカラー」などを厳密かつ的確に構造化し、後から文字やフォント、配色を自由に編集できる印刷用ベクターPDF（A4）および高精細PNG（4K解像度対応）をコードベース（Design as Code）で作成・ビルドします。

---

## 主な特徴とドメイン機能

* 🎤 **イベント・特典会ドメイン知識の体系的適用**:
  * **撮可（撮影可能）TIMEと特典会（撮影会）の厳格な峻別**: ライブ本編中の特例撮影時間（撮可TIME）と、特典券を消費する個別/グループ撮影会を別枠として明確に分離。
  * **購入レギュレーションの即応タグ配置**: 1会計の上限点数、対象品番（`BTRC-XXXX` 等）と盤種、買い増し並び直し（ループ）の可否・解除アナウンス手段を目立つアラートタグとして配置。
  * **一次情報にない事実の推測禁止（事実の厳格性）**: 告知に書かれていない機材制限（「一眼レフ可」等）を勝手に推測・断定せず、公式注意事項（手荷物自己管理、マスク着用義務等）を過不足なく忠実に記載。
  * **メンバーイメージカラーの調査とデザイン反映**: 公式プロフィール等からメンバー固有のイメージカラーを抽出し、出演者一覧やレーン案内にカラーチップとして適用。
* 📐 **縦長フロアマップ（会場図面）と入場案内の空間統合**:
  * ステージを上部に配した縦長比率（アスペクト比 3:4 程度）で会場図を再構成し、並列する優先観覧・整理番号入場案内の横幅を確保。
* 🖼️ **特典会共通イラストアセット＆リファレンス同梱**:
  * 全員お見送り会、2ショット撮影、動画撮影付きお見送り、個別お話し会、ユニット集合撮影、後ろ向き推し2shot、サイン会の共通イメージ（イラスト）を同梱。
  * キャラクター（メンバー・参加者・スタッフ）および備品（長机・椅子・パーテーション・スマホ等）のリファレンスシートにより、特殊な特典会も統一スタイルで都度生成可能。
* 🎨 **デザイントークンによる複数世界観の即時展開**:
  * セマンティックHTMLとデザイントークン（CSS変数）を分離し、和モダン、サイバーポップ、スタイリッシュなど複数のトーン＆マナーを瞬時に切り替え可能。
* 🖨️ **完全ベクターPDFと4K解像度PNG出力**:
  * A4サイズ（210×297mm）1枚に美しく収まる組版。
  * 拡大しても文字や罫線がボケないベクターPDF、および4Kディスプレイやスマートフォンでも鮮明に読める高精細PNG（2480×3508px）を出力。
* ⚡ **ゼロインストールCLI（`npx`, `uv`）による即時ビルド**:
  * `npx @vivliostyle/cli` や `uv run weasyprint`、`npx @myriaddreamin/typst-ts-cli` により、環境を汚さずワンライナーでPDF生成。

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
        │   └── illustrations/# 特典会共通イラスト＆リファレンス画像
        │       ├── reference-characters.jpg # キャラクターシート
        │       ├── reference-props.jpg      # 備品・道具セット
        │       ├── tokuten-sendoff.jpg      # 全員お見送り会
        │       ├── tokuten-2shot.jpg        # 2ショット撮影会
        │       ├── tokuten-video-sendoff.jpg# 動画撮影付きお見送り会
        │       ├── tokuten-talk.jpg         # 個別お話し会
        │       ├── tokuten-group-shot.jpg   # ユニット集合撮影
        │       ├── tokuten-back-oshi-2shot.jpg # 後ろ向き推し2shot
        │       └── tokuten-autograph.jpg    # サイン会
        ├── scripts/
        │   └── build.sh      # 統一ビルドスクリプト
        └── templates/
            ├── html-paged/   # HTML/CSS Paged Media テンプレート
            │   ├── index.html
            │   ├── theme.css # デザイントークン（色・余白・メンバーカラー）
            │   └── layout.css# @page、タイムライン、フロアマップ、テーブル
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

### 1. HTML/CSS テンプレートを使う場合

#### Vivliostyle（Node.js / npx）
```bash
# PDFをビルド
npx -y @vivliostyle/cli build index.html -o output.pdf

# ブラウザでプレビュー
npx -y @vivliostyle/cli preview index.html
```

#### WeasyPrint（Python / uv）
```bash
uv run weasyprint index.html output.pdf
```

### 2. Typst テンプレートを使う場合

```bash
npx -y @myriaddreamin/typst-ts-cli compile flyer.typ output.pdf
```

### 3. 付属のビルドスクリプトを使う場合

```bash
# HTML + Vivliostyle
./skills/event-tokutenkai/scripts/build.sh html-vivliostyle index.html output.pdf

# HTML + WeasyPrint
./skills/event-tokutenkai/scripts/build.sh html-weasyprint index.html output.pdf

# Typst
./skills/event-tokutenkai/scripts/build.sh typst flyer.typ output.pdf
```

### 4. 4K解像度（300dpi相当）PNGプレビューの生成 (macOS)

```bash
# PDFから 2480x3508px の高精細PNGをレンダリング
qlmanage -t -s 3508 -o . output.pdf
```

---

## ライセンス

MIT License
