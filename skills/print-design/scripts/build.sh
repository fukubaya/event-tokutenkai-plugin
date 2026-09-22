#!/usr/bin/env bash
# ==============================================================================
# Build Script for Print Design PDF
# 支持: Vivliostyle (npx), WeasyPrint (uv), Typst (npx)
# ==============================================================================

set -euo pipefail

usage() {
  echo "Usage: $0 <format: html-vivliostyle|html-weasyprint|typst> <input-file> [output-file]"
  echo ""
  echo "Examples:"
  echo "  $0 html-vivliostyle index.html output.pdf"
  echo "  $0 html-weasyprint index.html output.pdf"
  echo "  $0 typst flyer.typ output.pdf"
  exit 1
}

if [ "$#" -lt 2 ]; then
  usage
fi

FORMAT="$1"
INPUT="$2"
OUTPUT="${3:-output.pdf}"

if [ ! -f "$INPUT" ]; then
  echo "Error: Input file '$INPUT' does not exist." >&2
  exit 1
fi

case "$FORMAT" in
  html-vivliostyle|vivliostyle)
    echo "==> Building PDF with Vivliostyle (npx)..."
    npx -y @vivliostyle/cli build "$INPUT" -o "$OUTPUT"
    ;;
  html-weasyprint|weasyprint)
    echo "==> Building PDF with WeasyPrint (uv)..."
    uv run weasyprint "$INPUT" "$OUTPUT"
    ;;
  typst)
    echo "==> Building PDF with Typst (npx)..."
    npx -y @myriaddreamin/typst-ts-cli compile "$INPUT" "$OUTPUT"
    ;;
  *)
    echo "Error: Unknown format '$FORMAT'." >&2
    usage
    ;;
esac

echo "==> Successfully generated '$OUTPUT'"
