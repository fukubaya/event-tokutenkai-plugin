# Print Design Plugin for Antigravity CLI

印刷（PDF）を前提としたチラシ、ポスター、帳票、表組みなどを、**「後から文字やフォント、配色を自由に編集でき、印刷に耐えうる高品質ベクターPDFを出力する（Design as Code）」** ための Antigravity CLI プラグインです。

---

## 特徴と要件への対応

* ✍️ **文字・文章・フォント・イラストの後編集**:
  * ラスタ画像ではなく、HTML/CSS または Typst コードとして管理。
  * テキスト修正やフォント差し替え、SVGイラストの変更がいつでも可能。
* 🖨️ **印刷に耐えうるベクターPDF出力**:
  * 文字や罫線が拡大してもぼやけない完全ベクター形式。
  * 商業印刷向けのトンボ（crop marks）、断ち落とし（bleed: 3mm）に対応。
* 📐 **厳密な印刷サイズ指定**:
  * CSSの `@page { size: A4; margin: 15mm; }` や Typst の `#set page(paper: "a4", margin: 15mm)` でミリ単位のサイズ制御が可能。
* 🎨 **カラーセット・余白の一括変更（デザイントークン）**:
  * CSS変数（`--color-primary`, `--page-margin` 等）や Typst 変数により、1箇所の数値を変更するだけで全体のトーン＆マナーを瞬時に切り替え。
* ⚡ **指定CLIツール（`uv`, `npx`）での実行**:
  * Node.js環境: `npx @vivliostyle/cli build` または `npx @myriaddreamin/typst-ts-cli compile`
  * Python環境: `uv run weasyprint`
  * 事前インストール不要でワンライナー実行可能。

---

## ディレクトリ構成

```text
print-design-plugin/
├── plugin.json               # プラグインマニフェスト
├── README.md                 # プラグイン説明書
├── rules/
│   └── AGENTS.md             # 印刷物デザイン時の行動ルール（AI一発出しの禁止、トークン分離）
└── skills/
    └── print-design/
        ├── SKILL.md          # デザイン〜PDFビルド手順ガイド
        ├── scripts/
        │   └── build.sh      # 統一ビルドスクリプト
        └── templates/
            ├── html-paged/   # HTML/CSS Paged Media テンプレート
            │   ├── index.html
            │   ├── theme.css # デザイントークン（色・余白・フォント）
            │   └── layout.css# @page、グリッド、表組みスタイル
            └── typst/        # Typst テンプレート
                └── flyer.typ # 高速・高精度組版ソース
```

---

## プラグインの登録・有効化

本プラグインを Antigravity CLI で使用するには、以下のいずれかの方法で配置・登録します。

### 方法1: グローバルプラグインとして登録（推奨）
ユーザー設定ディレクトリ `~/.gemini/config/plugins/` にシンボリックリンクを貼るか配置します。

```bash
mkdir -p ~/.gemini/config/plugins
ln -s ~/.gemini/config/plugins/event-tokutenkai-plugin ~/.gemini/config/plugins/print-design-plugin
```

### 方法2: 特定のプロジェクト（ワークスペース）で使う場合
プロジェクトルートの `.agents/plugins/` 配下に配置またはリンクします。

```bash
mkdir -p <project-root>/.agents/plugins
ln -s ~/.gemini/config/plugins/event-tokutenkai-plugin <project-root>/.agents/plugins/event-tokutenkai-plugin
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
./skills/print-design/scripts/build.sh html-vivliostyle index.html output.pdf

# HTML + WeasyPrint
./skills/print-design/scripts/build.sh html-weasyprint index.html output.pdf

# Typst
./skills/print-design/scripts/build.sh typst flyer.typ output.pdf
```
