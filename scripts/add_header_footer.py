#!/usr/bin/env python3
"""Post-process a pandoc-generated docx to add LinkedIn/GitHub URLs top-right on every page.

Usage: python3 scripts/add_header_footer.py <input.docx> [output.docx]
If output is omitted, overwrites the input file.
"""
import sys
from docx import Document
from docx.shared import Pt, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml


def process(input_path, output_path=None):
    if output_path is None:
        output_path = input_path

    doc = Document(input_path)

    for section in doc.sections:
        section.different_first_page_header_footer = False
        section.header_distance = Emu(274320)  # 0.216 inches — tight
        section.footer_distance = Emu(274320)

        # ── HEADER AREA: LinkedIn + GitHub, right-aligned, no border ──
        header = section.header
        header.is_linked_to_previous = False

        # Clear all existing header content
        for p in list(header.paragraphs):
            header._element.remove(p._element)
        for t in list(header.tables):
            header._element.remove(t._element)

        # Single right-aligned paragraph with URLs
        hp = header.add_paragraph()
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.paragraph_format.space_after = Pt(0)
        hp.paragraph_format.space_before = Pt(0)

        r = hp.add_run("linkedin.com/in/vamshi-singam-82963556")
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(0x00, 0x77, 0xB5)

        r = hp.add_run("  |  ")
        r.font.size = Pt(7)
        r.font.color.rgb = RGBColor(0xBB, 0xBB, 0xBB)

        r = hp.add_run("github.com/vamshi455")
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

        # ── FOOTER: empty ──
        footer = section.footer
        footer.is_linked_to_previous = False
        for p in list(footer.paragraphs):
            footer._element.remove(p._element)
        for t in list(footer.tables):
            footer._element.remove(t._element)

        # Add empty paragraph to keep footer clean
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
