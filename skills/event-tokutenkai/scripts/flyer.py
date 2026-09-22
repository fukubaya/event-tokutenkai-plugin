#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pymupdf>=1.24.0",
#     "qrcode>=7.4.2",
# ]
# ///
"""
Event & Tokutenkai Flyer Utility Tool
イベント・特典会フライヤー作成・検証用CLIツール

機能:
  build   - HTML (Vivliostyle / WeasyPrint) または Typst から PDF を生成
  pages   - PDF のページ数・寸法（A4 / mm）の検証（1ページ厳守チェック）
  render  - PDF から 300dpi 高解像度 PNG プレビューを生成（macOS qlmanage / Swift代替）
  qr      - URL からベクター SVG QR コードを生成（外部CLI不要）
  all     - ビルド → ページ数検証 → 高解像度PNG生成 を一括実行
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# PyMuPDF と qrcode のインポートチェック
# 'uv run python script.py' のように実行された場合でも
# 透過的に uv run --with で自己解決して再実行する
try:
    import pymupdf
    import qrcode
    import qrcode.image.svg
except ImportError:
    if os.environ.get("_FLYER_REEXEC") != "1" and shutil.which("uv"):
        env = os.environ.copy()
        env["_FLYER_REEXEC"] = "1"
        cmd = [
            "uv",
            "run",
            "--with",
            "pymupdf>=1.24.0",
            "--with",
            "qrcode>=7.4.2",
            "python",
            os.path.abspath(__file__),
            *sys.argv[1:],
        ]
        res = subprocess.run(cmd, env=env)
        sys.exit(res.returncode)
    else:
        print("Error: Missing required dependencies (pymupdf, qrcode). Please run with 'uv run flyer.py'.", file=sys.stderr)
        sys.exit(1)



def format_bytes(size: int) -> str:
    """バイト数を可読性の高い文字列に変換"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


# ----------------------------------------------------------------------
# 1. build コマンド
# ----------------------------------------------------------------------
def cmd_build(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        return 1

    output_path = Path(args.output) if args.output else input_path.with_suffix(".pdf")
    engine = args.engine

    # エンジン自動判定
    if engine == "auto":
        suffix = input_path.suffix.lower()
        if suffix in [".typ"]:
            engine = "typst"
        elif suffix in [".html", ".htm"]:
            engine = "vivliostyle"
        else:
            print(f"Error: Cannot determine engine for '{input_path.name}'. Specify --engine.", file=sys.stderr)
            return 1

    print(f"==> Building PDF with [{engine}]: {input_path} -> {output_path}")

    cmd = []
    if engine in ["vivliostyle", "html-vivliostyle"]:
        cmd = ["npx", "-y", "@vivliostyle/cli", "build", str(input_path), "-o", str(output_path)]
    elif engine in ["weasyprint", "html-weasyprint"]:
        cmd = ["uv", "run", "weasyprint", str(input_path), str(output_path)]
    elif engine == "typst":
        # typst-ts-cli または システムの typst を探す
        if shutil.which("typst"):
            cmd = ["typst", "compile", str(input_path), str(output_path)]
        else:
            cmd = ["npx", "-y", "@myriaddreamin/typst-ts-cli", "compile", str(input_path), str(output_path)]
    else:
        print(f"Error: Unknown engine '{engine}'. Choose vivliostyle, weasyprint, or typst.", file=sys.stderr)
        return 1

    try:
        res = subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Build failed with exit code {e.returncode}", file=sys.stderr)
        return e.returncode
    except FileNotFoundError as e:
        print(f"Error: Required command not found ({e})", file=sys.stderr)
        return 1

    if output_path.exists():
        size = output_path.stat().st_size
        print(f"==> PDF generated: {output_path} ({format_bytes(size)})")
        return 0
    else:
        print(f"Error: Output file '{output_path}' was not generated.", file=sys.stderr)
        return 1


# ----------------------------------------------------------------------
# 2. pages (verify) コマンド
# ----------------------------------------------------------------------
def cmd_pages(args: argparse.Namespace) -> int:
    if pymupdf is None:
        print("Error: PyMuPDF is not installed.", file=sys.stderr)
        return 1

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: PDF file '{pdf_path}' not found.", file=sys.stderr)
        return 1

    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}", file=sys.stderr)
        return 1

    num_pages = len(doc)

    if args.quiet:
        print(num_pages)
        return 0

    print(f"📄 PDF Inspection: {pdf_path}")
    print(f"   Total Pages: {num_pages}")

    for idx, page in enumerate(doc):
        rect = page.rect
        # 1 pt = 0.352778 mm
        w_mm = rect.width * 0.352778
        h_mm = rect.height * 0.352778
        
        # A4判定 (210 x 297 mm ± 2mm)
        is_a4 = abs(w_mm - 210.0) < 2.0 and abs(h_mm - 297.0) < 2.0
        size_note = "A4" if is_a4 else f"{w_mm:.1f}x{h_mm:.1f}mm"
        print(f"   Page {idx + 1}: {rect.width:.1f} x {rect.height:.1f} pt ({w_mm:.1f} x {h_mm:.1f} mm, {size_note})")

    # 期待ページ数チェック
    if args.expect is not None:
        if num_pages == args.expect:
            print(f"   Result: PASS (Exact {args.expect} page(s))")
            return 0
        else:
            print(f"   Result: FAIL (Expected {args.expect} page(s), but found {num_pages} page(s)!)", file=sys.stderr)
            if args.expect == 1:
                print("   [WARNING] フライヤーが1ページに収まっていません！余白やフォントサイズ、行間を調整してください。", file=sys.stderr)
            return 1

    return 0


# ----------------------------------------------------------------------
# 3. render (preview) コマンド
# ----------------------------------------------------------------------
def cmd_render(args: argparse.Namespace) -> int:
    if pymupdf is None:
        print("Error: PyMuPDF is not installed.", file=sys.stderr)
        return 1

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: PDF file '{pdf_path}' not found.", file=sys.stderr)
        return 1

    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}", file=sys.stderr)
        return 1

    total_pages = len(doc)
    if total_pages == 0:
        print(f"Error: PDF '{pdf_path}' has no pages.", file=sys.stderr)
        return 1

    dpi = args.dpi

    # レンダリング対象ページ
    target_pages = []
    if args.page.lower() == "all":
        target_pages = list(range(total_pages))
    else:
        try:
            p_num = int(args.page)
            if p_num < 1 or p_num > total_pages:
                print(f"Error: Page number {p_num} out of range (1-{total_pages}).", file=sys.stderr)
                return 1
            target_pages = [p_num - 1]
        except ValueError:
            print(f"Error: Invalid page argument '{args.page}'. Use an integer or 'all'.", file=sys.stderr)
            return 1

    for p_idx in target_pages:
        page = doc[p_idx]
        pix = page.get_pixmap(dpi=dpi)

        if args.output:
            if len(target_pages) == 1:
                out_file = Path(args.output)
            else:
                out_path_obj = Path(args.output)
                out_file = out_path_obj.with_name(f"{out_path_obj.stem}-p{p_idx+1}{out_path_obj.suffix}")
        else:
            if len(target_pages) == 1 and p_idx == 0:
                out_file = pdf_path.with_suffix(".png")
            else:
                out_file = pdf_path.with_name(f"{pdf_path.stem}-p{p_idx+1}.png")

        pix.save(out_file)
        size_str = format_bytes(out_file.stat().st_size)
        print(f"🖼️  Rendered page {p_idx+1} ({dpi} dpi): {out_file} [{pix.width}x{pix.height} px, {size_str}]")

    return 0


# ----------------------------------------------------------------------
# 4. qr コマンド
# ----------------------------------------------------------------------
def cmd_qr(args: argparse.Namespace) -> int:
    if qrcode is None:
        print("Error: qrcode library is not installed.", file=sys.stderr)
        return 1

    url = args.url
    out_file = Path(args.output) if args.output else Path("qr.svg")

    factory = qrcode.image.svg.SvgPathImage
    qr = qrcode.QRCode(
        version=args.version,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=args.box_size,
        border=args.border,
        image_factory=factory,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image()
    out_file.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_file))

    size_str = format_bytes(out_file.stat().st_size)
    print(f"📱 QR Code (Vector SVG) generated: {out_file} ({size_str}) for URL: {url}")
    return 0


# ----------------------------------------------------------------------
# 5. all (パイプライン) コマンド
# ----------------------------------------------------------------------
def cmd_all(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        return 1

    pdf_out = Path(args.output) if args.output else input_path.with_suffix(".pdf")
    png_out = Path(args.preview) if args.preview else input_path.with_suffix(".png")

    print("==================================================================")
    print(f"🚀 Flyer Pipeline: {input_path.name}")
    print("==================================================================")

    # Step 1: Build PDF
    build_args = argparse.Namespace(
        input=str(input_path),
        output=str(pdf_out),
        engine=args.engine,
    )
    res = cmd_build(build_args)
    if res != 0:
        print("❌ Step 1 (Build) failed!", file=sys.stderr)
        return res

    # Step 2: Verify Pages
    pages_args = argparse.Namespace(
        pdf=str(pdf_out),
        expect=args.expect,
        quiet=False,
    )
    res = cmd_pages(pages_args)
    if res != 0:
        if args.strict:
            print("❌ Step 2 (Verification) failed with strict mode enabled. Aborting.", file=sys.stderr)
            return res
        else:
            print("⚠️  Step 2 (Verification) returned warning, continuing preview generation...")

    # Step 3: Render Preview PNG
    if not args.no_preview:
        render_args = argparse.Namespace(
            pdf=str(pdf_out),
            output=str(png_out),
            dpi=args.dpi,
            page="1" if args.expect == 1 else "all",
        )
        res = cmd_render(render_args)
        if res != 0:
            print("❌ Step 3 (Render preview) failed!", file=sys.stderr)
            return res

    print("==================================================================")
    print(f"✨ All steps completed successfully!")
    print(f"   PDF:     {pdf_out}")
    if not args.no_preview:
        print(f"   Preview: {png_out}")
    print("==================================================================")
    return 0


# ----------------------------------------------------------------------
# 6. extract コマンド
# ----------------------------------------------------------------------
def cmd_extract(args: argparse.Namespace) -> int:
    script_dir = Path(__file__).resolve().parent
    extract_script = script_dir / "extract_event.py"

    cmd = ["uv", "run", "python", str(extract_script), args.source]
    if args.output:
        cmd.extend(["-o", args.output])
    if args.json:
        cmd.extend(["--json", args.json])
    if args.quiet:
        cmd.append("-q")

    res = subprocess.run(cmd)
    return res.returncode


# ----------------------------------------------------------------------
# メイン エントリポイント
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Event & Tokutenkai Flyer Utility CLI (Python & uv)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 1. URL から情報を抽出し、要約 Markdown と JSON を生成
  uv run python flyer.py extract "https://starplanet-academy.com/schedule/item-359/" -o event_summary.md --json event_data.json

  # 2. ビルド・検証・プレビューを一括実行 (推奨)
  uv run python flyer.py all index.html

  # 3. PDF をビルド
  uv run python flyer.py build index.html -o flyer.pdf

  # 4. ページ数・寸法の検証 (1ページチェック)
  uv run python flyer.py pages flyer.pdf --expect 1

  # 5. 高解像度 PNG プレビューを生成 (300dpi)
  uv run python flyer.py render flyer.pdf -o flyer.png --dpi 300

  # 6. ベクター SVG QR コードを生成
  uv run python flyer.py qr "https://example.com" -o qr.svg
""",
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="実行するサブコマンド")

    # --- Subcommand: build ---
    p_build = subparsers.add_parser("build", help="HTML または Typst から PDF をビルド")
    p_build.add_argument("input", help="入力ファイル (.html または .typ)")
    p_build.add_argument("-o", "--output", help="出力PDFファイルパス (省略時: <input>.pdf)")
    p_build.add_argument(
        "--engine",
        choices=["auto", "vivliostyle", "weasyprint", "typst"],
        default="auto",
        help="組版エンジン (デフォルト: auto [拡張子で自動判別])",
    )
    p_build.set_defaults(func=cmd_build)

    # --- Subcommand: pages (verify) ---
    p_pages = subparsers.add_parser("pages", aliases=["verify"], help="PDF のページ数・寸法（A4/mm）を検証")
    p_pages.add_argument("pdf", help="検査対象の PDF ファイル")
    p_pages.add_argument("--expect", type=int, default=1, help="期待するページ数 (デフォルト: 1)")
    p_pages.add_argument("-q", "--quiet", action="store_true", help="ページ数のみを出力")
    p_pages.set_defaults(func=cmd_pages)

    # --- Subcommand: render (preview) ---
    p_render = subparsers.add_parser("render", aliases=["preview"], help="PDF から高解像度 PNG プレビューを生成")
    p_render.add_argument("pdf", help="レンダリング対象の PDF ファイル")
    p_render.add_argument("-o", "--output", help="出力PNGファイルパス (省略時: <pdf>.png)")
    p_render.add_argument("--dpi", type=int, default=300, help="レンダリング解像度 (デフォルト: 300 [A4で約2480x3508px])")
    p_render.add_argument("--page", default="1", help="レンダリング対象ページ ('1', '2', または 'all') (デフォルト: 1)")
    p_render.set_defaults(func=cmd_render)

    # --- Subcommand: qr ---
    p_qr = subparsers.add_parser("qr", help="URL から印刷用ベクター SVG QR コードを生成")
    p_qr.add_argument("url", help="埋め込む URL")
    p_qr.add_argument("-o", "--output", default="qr.svg", help="出力先SVGファイルパス (デフォルト: qr.svg)")
    p_qr.add_argument("--version", type=int, default=None, help="QRバージョン (1-40, 省略時は自動適合)")
    p_qr.add_argument("--box-size", type=int, default=10, help="1モジュールのボックスサイズ (デフォルト: 10)")
    p_qr.add_argument("--border", type=int, default=2, help="余白モジュール数 (デフォルト: 2)")
    p_qr.set_defaults(func=cmd_qr)

    # --- Subcommand: all ---
    p_all = subparsers.add_parser("all", help="ビルド → ページ数検証 → 高解像度プレビュー生成を一気通貫で実行")
    p_all.add_argument("input", help="入力ファイル (.html または .typ)")
    p_all.add_argument("-o", "--output", help="出力PDFファイルパス (省略時: <input>.pdf)")
    p_all.add_argument("--preview", help="出力プレビューPNGファイルパス (省略時: <input>.png)")
    p_all.add_argument("--dpi", type=int, default=300, help="プレビュー解像度 (デフォルト: 300)")
    p_all.add_argument(
        "--engine",
        choices=["auto", "vivliostyle", "weasyprint", "typst"],
        default="auto",
        help="組版エンジン (デフォルト: auto)",
    )
    p_all.add_argument("--expect", type=int, default=1, help="期待するページ数 (デフォルト: 1)")
    p_all.add_argument("--strict", action="store_true", help="ページ数不一致時に処理を中断してエラー終了")
    p_all.add_argument("--no-preview", action="store_true", help="プレビューPNG生成をスキップ")
    p_all.set_defaults(func=cmd_all)

    # --- Subcommand: extract ---
    p_extract = subparsers.add_parser("extract", help="URL または HTML ファイルからイベント・特典会情報を構造化抽出")
    p_extract.add_argument("source", help="抽出元の URL または ローカル HTML/テキストファイル")
    p_extract.add_argument("-o", "--output", help="出力先 Markdown ファイルパス (省略時: 標準出力)")
    p_extract.add_argument("--json", help="出力先 JSON ファイルパス")
    p_extract.add_argument("-q", "--quiet", action="store_true", help="進捗メッセージを抑制")
    p_extract.set_defaults(func=cmd_extract)

    parsed_args = parser.parse_args()
    return parsed_args.func(parsed_args)


if __name__ == "__main__":
    sys.exit(main())
