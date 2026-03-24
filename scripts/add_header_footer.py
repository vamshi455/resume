#!/usr/bin/env python3
"""Post-process a pandoc-generated docx to remove all headers and footers.

Usage: python3 scripts/add_header_footer.py <input.docx> [output.docx]
If output is omitted, overwrites the input file.
"""
import sys
from docx import Document
from docx.shared import Pt, Emu


def process(input_path, output_path=None):
    if output_path is None:
        output_path = input_path

    doc = Document(input_path)

    for section in doc.sections:
        section.different_first_page_header_footer = False

        # ── Remove header content ──
        header = section.header
        header.is_linked_to_previous = False
        for p in list(header.paragraphs):
            header._element.remove(p._element)
        for t in list(header.tables):
            header._element.remove(t._element)

        # Add empty paragraph to keep header area clean
        hp = header.add_paragraph()
        hp.paragraph_format.space_after = Pt(0)
        hp.paragraph_format.space_before = Pt(0)

        # ── Remove footer content ──
        footer = section.footer
        footer.is_linked_to_previous = False
        for p in list(footer.paragraphs):
            footer._element.remove(p._element)
        for t in list(footer.tables):
            footer._element.remove(t._element)

        # Add empty paragraph to keep footer area clean
        fp = footer.add_paragraph()
        fp.paragraph_format.space_after = Pt(0)
        fp.paragraph_format.space_before = Pt(0)

    doc.save(output_path)
    print(f"Post-processed: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/add_header_footer.py <input.docx> [output.docx]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    process(inp, out)
