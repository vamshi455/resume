#!/usr/bin/env python3
"""Post-process a pandoc-generated docx:
- Remove all headers and footers
- Convert LinkedIn/GitHub plain text URLs to clickable hyperlinks

Usage: python3 scripts/add_header_footer.py <input.docx> [output.docx]
If output is omitted, overwrites the input file.
"""
import sys
import re
import copy
from docx import Document
from docx.shared import Pt, Emu
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


HYPERLINK_MAP = {
    "linkedin.com/in/vamshi-singam-82963556": "https://linkedin.com/in/vamshi-singam-82963556",
    "github.com/vamshi455": "https://github.com/vamshi455",
}


def make_hyperlink(paragraph, run, url, text):
    """Replace a run with a clickable hyperlink preserving formatting."""
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )

    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    new_run = copy.deepcopy(run._element)
    # Clear text and set new
    for t in new_run.findall(qn("w:t")):
        new_run.remove(t)
    t_elem = OxmlElement("w:t")
    t_elem.text = text
    t_elem.set(qn("xml:space"), "preserve")
    new_run.append(t_elem)

    hyperlink.append(new_run)

    run._element.getparent().replace(run._element, hyperlink)


def linkify_urls(doc):
    """Find plain-text LinkedIn/GitHub URLs in paragraphs and make them hyperlinks."""
    for paragraph in doc.paragraphs:
        for run in list(paragraph.runs):
            for plain_text, url in HYPERLINK_MAP.items():
                if plain_text in run.text:
                    make_hyperlink(paragraph, run, url, run.text)
                    break

    # Also check inside tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in list(paragraph.runs):
                        for plain_text, url in HYPERLINK_MAP.items():
                            if plain_text in run.text:
                                make_hyperlink(paragraph, run, url, run.text)
                                break


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

        fp = footer.add_paragraph()
        fp.paragraph_format.space_after = Pt(0)
        fp.paragraph_format.space_before = Pt(0)

    # Convert plain-text URLs to hyperlinks
    linkify_urls(doc)

    doc.save(output_path)
    print(f"Post-processed: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/add_header_footer.py <input.docx> [output.docx]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    process(inp, out)
