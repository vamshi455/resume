#!/bin/bash
# Export resume markdown to DOCX with header/footer post-processing
# Usage: ./scripts/export_to_pdf.sh [input.md] [output-name] [output-dir]
#
# Examples:
#   ./scripts/export_to_pdf.sh resume/master.md Vamshi_Resume_2026_V10
#   ./scripts/export_to_pdf.sh outputs/2026-03-20-acme/resume-tailored.md Vamshi_Acme_Resume outputs/2026-03-20-acme

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

INPUT="${1:-resume/master.md}"
OUTPUT_NAME="${2:-Vamshi_Resume_$(date +%Y)}"
OUTPUT_DIR="${3:-resume}"

if [ ! -f "$INPUT" ]; then
    echo "Error: Input file '$INPUT' not found"
    exit 1
fi

OUTPUT_PATH="${OUTPUT_DIR}/${OUTPUT_NAME}.docx"

# Step 1: Pandoc md → docx (compact font reference)
echo "Exporting to DOCX..."
pandoc "$INPUT" -f gfm -t docx \
    --reference-doc="${PROJECT_DIR}/resume/reference-compact.docx" \
    -o "$OUTPUT_PATH"

# Step 2: Post-process — inject header, footer, watermark with working hyperlinks
echo "Adding header/footer/watermark..."
python3 "${SCRIPT_DIR}/add_header_footer.py" "$OUTPUT_PATH"

echo "Created: $OUTPUT_PATH"

# Export to PDF (requires pdflatex or wkhtmltopdf)
if command -v wkhtmltopdf &> /dev/null; then
    echo "Exporting to PDF via wkhtmltopdf..."
    pandoc "$INPUT" -f gfm -t html | wkhtmltopdf - "${OUTPUT_DIR}/${OUTPUT_NAME}.pdf"
    echo "Created: ${OUTPUT_DIR}/${OUTPUT_NAME}.pdf"
elif command -v pdflatex &> /dev/null; then
    echo "Exporting to PDF via LaTeX..."
    pandoc "$INPUT" -f gfm -o "${OUTPUT_DIR}/${OUTPUT_NAME}.pdf"
    echo "Created: ${OUTPUT_DIR}/${OUTPUT_NAME}.pdf"
else
    echo "Note: PDF export skipped (install wkhtmltopdf or pdflatex)"
fi

echo "Done."
