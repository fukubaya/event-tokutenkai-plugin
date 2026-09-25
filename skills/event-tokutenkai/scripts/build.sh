#!/usr/bin/env bash
# ==============================================================================
# Build Script for Event & Tokutenkai Flyer PDF & High-Res PNG
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLYER_PY="$SCRIPT_DIR/flyer.py"

usage() {
  echo "Usage: $0 [options] <format: auto|vivliostyle|weasyprint|typst> <input-file> [output-pdf] [output-png]"
  echo ""
  echo "Examples:"
  echo "  $0 auto index.html"
  echo "  $0 vivliostyle index.html output.pdf output.png"
  echo "  $0 typst flyer.typ output.pdf"
  echo ""
  echo "Or run flyer.py directly with uv:"
  echo "  uv run python $FLYER_PY all index.html"
  echo "  uv run python $FLYER_PY pages output.pdf --expect 1"
  echo "  uv run python $FLYER_PY render output.pdf -o output.png --dpi 300"
  echo "  uv run python $FLYER_PY qr 'https://example.com' -o qr.svg"
  exit 1
}

if [ "$#" -lt 2 ]; then
  usage
fi

FORMAT="$1"
INPUT="$2"
OUTPUT_PDF="${3:-${INPUT%.*}.pdf}"
OUTPUT_PNG="${4:-${INPUT%.*}.png}"

ENGINE="auto"
case "$FORMAT" in
  auto)
    ENGINE="auto"
    ;;
  html-vivliostyle|vivliostyle)
    ENGINE="vivliostyle"
    ;;
  html-weasyprint|weasyprint)
    ENGINE="weasyprint"
    ;;
  typst)
    ENGINE="typst"
    ;;
  *)
    echo "Error: Unknown format '$FORMAT'." >&2
    usage
    ;;
esac

# Execute via flyer.py pipeline
uv run python "$FLYER_PY" all "$INPUT" \
  --engine "$ENGINE" \
  -o "$OUTPUT_PDF" \
  --preview "$OUTPUT_PNG" \
  --dpi 300
