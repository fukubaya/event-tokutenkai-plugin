// ==============================================================================
// Typst Flyer Template
// カラーセット・余白・フォントの変数化と印刷用ベクターPDF出力
// ==============================================================================

// --- デザイントークン（テーマ設定） ---
#let primary-color = rgb("#1a73e8")
#let primary-dark = rgb("#1557b0")
#let secondary-color = rgb("#ea4335")
#let text-color = rgb("#202124")
#let bg-sub = rgb("#f8f9fa")
#let border-color = rgb("#dadce0")

#let page-margin = 15mm
#let font-base = ("Noto Sans CJK JP", "Noto Sans JP", "Hiragino Kaku Gothic ProN")

// --- ページ設定（A4・マージン） ---
#set page(
  paper: "a4",
  margin: (x: page-margin, y: page-margin),
  header: align(right)[
    #text(size: 8pt, fill: luma(120))[Design as Code Sample]
  ],
  footer: [
    #line(length: 100%, stroke: 0.5pt + border-color)
    #grid(
      columns: (1fr, 1fr),
      text(size: 8pt, fill: luma(120))[株式会社デザイン・システムズ],
      align(right)[#text(size: 8pt, fill: luma(120))[Page 1 / 1]]
    )
  ]
)

#set text(
  font: font-base,
  size: 10.5pt,
  fill: text-color,
  lang: "ja"
)

// --- ドキュメントヘッダー ---
#block(
  width: 100%,
  stroke: (bottom: 2pt + primary-color),
  inset: (bottom: 4mm),
  [
    #grid(
      columns: (1fr, auto),
      [
        #text(size: 24pt, weight: "bold", fill: primary-dark)[次世代デザイン・ソリューション]\
        #v(1mm)
        #text(size: 12pt, fill: luma(100))[Typstによる高精度・モダン組版ドキュメント]
      ],
      align(bottom)[
        #rect(fill: secondary-color, radius: 2mm, inset: (x: 4mm, y: 2mm))[
          #text(fill: white, weight: "bold", size: 9pt)[NEW RELEASE]
        ]
      ]
    )
  ]
)

#v(4mm)

// --- 2カラムカード ---
#grid(
  columns: (1fr, 1fr),
  gutter: 6mm,
  [
    #rect(
      width: 100%,
      stroke: 0.5pt + border-color,
      radius: 2mm,
      fill: bg-sub,
      inset: 4mm
    )[
      #text(weight: "bold", fill: primary-color, size: 12pt)[特長とメリット]\
      #v(2mm)
      AIとコードを組み合わせることで、文字の崩れや曖昧さを排除し、いつでもテキスト・配色・余白を変更可能な印刷用PDFを生成できます。
    ]
  ],
  [
    #rect(
      width: 100%,
      stroke: 0.5pt + border-color,
      radius: 2mm,
      fill: bg-sub,
      inset: 4mm
    )[
      #text(weight: "bold", fill: primary-color, size: 12pt)[主な機能]\
      #v(2mm)
      - 完全ベクター出力（文字・表の無劣化）
      - 変数書き換えによる配色の一括更新
      - 厳密なA4/B5/mmサイズ設定
      - CLI（npx）から即座にPDF化
    ]
  ]
)

#v(4mm)

// --- 料金・仕様一覧（表組み） ---
#text(weight: "bold", fill: primary-color, size: 13pt)[料金・仕様一覧]
#v(2mm)

#table(
  columns: (1.5fr, 2.5fr, 1.2fr, 1.2fr),
  stroke: 0.5pt + border-color,
  fill: (col, row) => if row == 0 { primary-color } else if calc.odd(row) { bg-sub } else { white },
  align: (col, row) => if col == 3 { right } else { left },
  // ヘッダー行
  table.header(
    [*プラン名*], [*対象サイズ*], [*納期*], [*価格 (税抜)*]
  ),
  // データ行
  [ライトプラン], [A4 片面 / デジタルPDF], [最短即日], [¥20,000],
  [スタンダードプラン], [A4 両面 / 商業印刷], [3営業日], [¥45,000],
  [プロフェッショナル], [複数ページ カタログ], [7営業日], [¥98,000],
)
