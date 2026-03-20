#!/bin/bash
# Export resume markdown to PDF/DOCX using pandoc
# Usage: ./scripts/export_to_pdf.sh [input.md] [output-name]
#
# Examples:
#   ./scripts/export_to_pdf.sh resume/master.md Vamshi_Resume_2026_V8
#   ./scripts/export_to_pdf.sh outputs/2026-03-20-acme/resume-tailored.md Vamshi_Acme_Resume

set -euo pipefail

INPUT="${1:-resume/master.md}"
OUTPUT_NAME="${2:-Vamshi_Resume_$(date +%Y)}"

if [ ! -f "$INPUT" ]; then
    echo "Error: Input file '$INPUT' not found"
    exit 1
fi

# Export to DOCX
echo "Exporting to DOCX..."
pandoc "$INPUT" -f gfm -t docx -o "resume/${OUTPUT_NAME}.docx"
echo "Created: resume/${OUTPUT_NAME}.docx"

# Export to PDF (requires pdflatex or wkhtmltopdf)
if command -v wkhtmltopdf &> /dev/null; then
    echo "Exporting to PDF via wkhtmltopdf..."
    pandoc "$INPUT" -f gfm -t html | wkhtmltopdf - "resume/${OUTPUT_NAME}.pdf"
    echo "Created: resume/${OUTPUT_NAME}.pdf"
elif command -v pdflatex &> /dev/null; then
    echo "Exporting to PDF via LaTeX..."
    pandoc "$INPUT" -f gfm -o "resume/${OUTPUT_NAME}.pdf"
    echo "Created: resume/${OUTPUT_NAME}.pdf"
else
    echo "Note: PDF export skipped (install wkhtmltopdf or pdflatex)"
fi

echo "Done."
