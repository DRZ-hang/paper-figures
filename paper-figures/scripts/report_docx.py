#!/usr/bin/env python3
"""report_docx.py — assemble the stage-7 figure report as a Word (.docx) document.

Builds the bilingual hand-off report: a title, manuscript metadata, an asset index,
then one block per figure/table with the embedded figure image (or inline three-line
table), bilingual caption (中文/English), annotations, in-text citation location, and
a reproducibility note.

    from report_docx import build_report
    build_report("Figure_Report.docx", title="...", meta=[...], items=[...])

Each item is a dict:
  figure: {"kind":"figure", "number":"1", "title":"...", "image":"figures/Fig1.png",
           "width_in":6.0, "claim":"...", "caption_en":"...", "caption_zh":"...",
           "annotations":[("Label","text"), ...] or ["text", ...],
           "citation":"...", "repro":"..."}
  table:  {"kind":"table", "number":"1", "title":"...", "csv":"figures/Table1.csv",
           "table_title":"Table 1. ...", "table_note":"...", (caption/annotations/... same)}

Requires python-docx (and pandas for table CSVs).
"""
from __future__ import annotations

from pathlib import Path

from docx_tables import add_three_line_table


def _heading(doc, text, size, bold=True, space_before=10, space_after=4, color=None):
    from docx.shared import Pt, RGBColor
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)
    return p


def _labelled(doc, label, text, size=10, label_color=(0x1F, 0x4E, 0x79)):
    """A paragraph beginning with a bold coloured label, then normal text."""
    from docx.shared import Pt, RGBColor
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(label)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = RGBColor(*label_color)
    if text:
        t = p.add_run(text)
        t.font.size = Pt(size)
    return p


def build_report(path, title, subtitle=None, meta=None, items=None,
                 base_dir=None, body_font="Calibri", body_pt=10):
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    base = Path(base_dir) if base_dir else Path(".")
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = body_font
    style.font.size = Pt(body_pt)

    # title
    _heading(doc, title, 18, color=(0x1F, 0x4E, 0x79), space_before=0, space_after=2)
    if subtitle:
        _heading(doc, subtitle, 12, bold=False, space_before=0, space_after=8)

    # metadata block
    if meta:
        for label, value in meta:
            _labelled(doc, f"{label}: ", value, size=body_pt)

    # asset index
    if items:
        _heading(doc, "Asset index / 图表清单", 12, space_before=12)
        idx = doc.add_table(rows=1, cols=3)
        idx.style = "Light Grid Accent 1"
        for j, h in enumerate(["#", "File 文件", "Claim 结论"]):
            run = idx.rows[0].cells[j].paragraphs[0].add_run(h)
            run.bold = True
            run.font.size = Pt(body_pt - 1)
        for it in items:
            kind = "Fig" if it["kind"] == "figure" else "Table"
            cells = idx.add_row().cells
            fname = Path(it.get("image") or it.get("csv", "")).name
            vals = [f"{kind} {it['number']}", fname, it.get("claim", "")]
            for j, v in enumerate(vals):
                r = cells[j].paragraphs[0].add_run(v)
                r.font.size = Pt(body_pt - 1)

    # one block per item
    for it in items or []:
        kind = it["kind"]
        head = ("Figure " if kind == "figure" else "Table ") + it["number"]
        if it.get("title"):
            head += f" — {it['title']}"
        _heading(doc, head, 13, color=(0x1F, 0x4E, 0x79), space_before=14)

        if kind == "figure" and it.get("image"):
            img = base / it["image"]
            if img.exists():
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.add_run().add_picture(str(img), width=Inches(it.get("width_in", 6.0)))
        elif kind == "table" and it.get("csv"):
            import pandas as pd
            df = pd.read_csv(base / it["csv"])
            add_three_line_table(doc, df, title=it.get("table_title"),
                                 note=it.get("table_note"))

        if it.get("claim"):
            _labelled(doc, "Claim / 论证: ", it["claim"])
        if it.get("caption_en"):
            _labelled(doc, "Caption (EN): ", it["caption_en"])
        if it.get("caption_zh"):
            _labelled(doc, "图注 (中文): ", it["caption_zh"])

        anns = it.get("annotations")
        if anns:
            _labelled(doc, "Annotations / 标注", "")
            for a in anns:
                p = doc.add_paragraph(style="List Bullet")
                p.paragraph_format.space_after = Pt(1)
                if isinstance(a, (tuple, list)):
                    r = p.add_run(f"{a[0]}: "); r.bold = True; r.font.size = Pt(body_pt)
                    t = p.add_run(a[1]); t.font.size = Pt(body_pt)
                else:
                    p.add_run(a).font.size = Pt(body_pt)

        if it.get("citation"):
            _labelled(doc, "Citation location / 引用位置: ", it["citation"])
        if it.get("repro"):
            _labelled(doc, "Reproducibility / 可复现: ", it["repro"])

    doc.save(str(path))
    return path
