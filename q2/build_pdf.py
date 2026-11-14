#!/usr/bin/env python3
"""Render a Q2 answer.md into <BITS_ID>.pdf. Refuses to build if check_kb.py fails.

Usage:
    python q2/build_pdf.py q2/<BITS_ID>/answer.md            # -> q2/<BITS_ID>/<BITS_ID>.pdf
    python q2/build_pdf.py q2/EXAMPLE.md --profile example -o /tmp/example.pdf
"""
import argparse
import html
import re
import sys
from pathlib import Path

import matplotlib
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, Paragraph, Preformatted, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_kb  # noqa: E402

COURSE = "AIMLZG557 – Artificial and Computational Intelligence"
ASSIGNMENT = "Assignment 2 – Question 2 (Individual): Situated Learning"
COURSE_INFO = "Instructor In-charge: Dr. V Indumathi  ·  Semester: S1-26  ·  Component: EC-1"


# ------------------------------------------------------------------ fonts & styles
def register_fonts():
    ttf = Path(matplotlib.get_data_path()) / "fonts" / "ttf"   # DejaVu ships with matplotlib
    for name, file in (("DV", "DejaVuSans.ttf"), ("DV-B", "DejaVuSans-Bold.ttf"),
                       ("DV-I", "DejaVuSans-Oblique.ttf"), ("DV-BI", "DejaVuSans-BoldOblique.ttf"),
                       ("DVM", "DejaVuSansMono.ttf")):
        pdfmetrics.registerFont(TTFont(name, str(ttf / file)))
    pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-BI")


def styles():
    base = dict(fontName="DV", fontSize=10, leading=14)
    return {
        "body": ParagraphStyle("body", **base, spaceAfter=5),
        "small": ParagraphStyle("small", **{**base, "fontSize": 9, "leading": 12}),
        "quote": ParagraphStyle("quote", **{**base, "fontName": "DV-I"}, leftIndent=10,
                                textColor=colors.HexColor("#444444"), spaceAfter=5),
        "bullet": ParagraphStyle("bullet", **base, spaceAfter=2),
        "h1": ParagraphStyle("h1", fontName="DV-B", fontSize=16, leading=20, spaceBefore=4,
                             spaceAfter=6, alignment=TA_CENTER),
        "h2": ParagraphStyle("h2", fontName="DV-B", fontSize=13, leading=17, spaceBefore=12,
                             spaceAfter=6, textColor=colors.HexColor("#1f3864")),
        "h3": ParagraphStyle("h3", fontName="DV-B", fontSize=11, leading=15, spaceBefore=8,
                             spaceAfter=4, textColor=colors.HexColor("#2f5496")),
        "h4": ParagraphStyle("h4", fontName="DV-B", fontSize=10, leading=14, spaceBefore=6,
                             spaceAfter=3),
        "center": ParagraphStyle("center", **base, alignment=TA_CENTER),
        "code": ParagraphStyle("code", fontName="DVM", fontSize=8.3, leading=10.5,
                               backColor=colors.HexColor("#f3f3f3"), borderPadding=4,
                               leftIndent=4, rightIndent=4, spaceBefore=4, spaceAfter=8),
    }


def inline(text):
    """Markdown inline -> reportlab mini-HTML."""
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for p in parts:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append(f'<font name="DVM">{html.escape(p[1:-1])}</font>')
            continue
        p = html.escape(p, quote=False)
        p = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", p)
        p = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", p)
        out.append(p)
    return "".join(out)


# ------------------------------------------------------------------ markdown -> flowables
def md_flowables(text, st, width):
    lines = text.splitlines()
    flow, i, para = [], 0, []

    def flush():
        if para:
            flow.append(Paragraph(inline(" ".join(l.strip() for l in para)), st["body"]))
            para.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            flush()
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            code = "\n".join(lines[i + 1:j]).strip("\n")
            if code:
                flow.append(Preformatted(code, st["code"], maxLineLength=96, newLineChars="  ↪ "))
            i = j + 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            flush()
            lvl = len(m.group(1))
            flow.append(Paragraph(inline(m.group(2)), st[f"h{max(lvl, 2) if lvl > 1 else 1}"]))
            i += 1
            continue
        if s.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            flow.append(make_table(rows, st, width))
            flow.append(Spacer(1, 6))
            continue
        if s.startswith(">"):
            flush()
            q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(lines[i].strip()[1:].strip())
                i += 1
            flow.append(Paragraph(inline(" ".join(q)), st["quote"]))
            continue
        m = re.match(r"^(\s*)([-*]|\d+[.)])\s+(.*)$", line)
        if m:
            flush()
            indent = len(m.group(1).replace("\t", "    "))
            item = [m.group(3)]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(
                    r"^(\s*)([-*]|\d+[.)])\s+|^\s*(#|\||```|>)", lines[i]):
                item.append(lines[i].strip())
                i += 1
            bullet = "•" if m.group(2) in "-*" else m.group(2)
            style = ParagraphStyle("b", parent=st["bullet"], leftIndent=14 + indent * 5,
                                   bulletIndent=3 + indent * 5)
            flow.append(Paragraph(inline(" ".join(item)), style, bulletText=bullet))
            continue
        if not s:
            flush()
        else:
            para.append(s)
        i += 1
    flush()
    return flow


def make_table(rows, st, width):
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    data = [[Paragraph(inline(c), st["small"]) for c in r] for r in rows]
    lens = [max(len(r[c]) for r in rows) + 4 for c in range(ncol)]
    widths = [width * l / sum(lens) for l in lens]
    if ncol == 2:                                   # key/value or symbol/meaning tables
        widths = [max(width * 0.28, min(widths[0], width * 0.45)), 0]
        widths[1] = width - widths[0]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dde4f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def cover(meta, st, width):
    rows = [["Name", meta.get("Name", "")], ["BITS ID", meta.get("ID No", "")],
            ["Industry / Domain", meta.get("Industry / Domain", "")],
            ["Organisation Type", meta.get("Organisation Type", "")],
            ["Instructor prompt", meta.get("Instructor prompt", "")]]
    t = Table([[Paragraph(f"<b>{html.escape(k)}</b>", st["body"]),
                Paragraph(html.escape(v), st["body"])] for k, v in rows],
              colWidths=[width * 0.3, width * 0.7])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#1f3864")),
                           ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#aaaaaa")),
                           ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef2f8")),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return [Paragraph(COURSE, st["center"]), Paragraph(ASSIGNMENT, st["h1"]),
            Paragraph(COURSE_INFO, st["center"]), Spacer(1, 10), t, Spacer(1, 14)]


# ------------------------------------------------------------------ build
def build(answer, out=None, profile="full", force_meta=None):
    rep = check_kb.check(answer, profile)
    meta = rep.meta
    sid = (meta.get("ID No") or "").strip()
    problems = rep.failures()
    members = check_kb.load_members()
    if profile == "full" and sid not in members:
        problems.append(f"B.1 ID No '{sid}' is not one of the group's BITS IDs in q2/members.json")
    if problems:
        msg = ["REFUSING to build the PDF: check_kb.py reports problems in " + str(answer) + ":"]
        msg += [f"  - {p}" for p in problems]
        msg.append(f"Fix them, then run: python q2/check_kb.py {answer}")
        raise SystemExit("\n".join(msg))

    out = Path(out) if out else Path(answer).parent / f"{sid}.pdf"
    register_fonts()
    st = styles()
    doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=16 * mm,
                            title=f"{sid} – AIMLZG557 Assignment 2 Q2", author=meta.get("Name", ""))
    width = A4[0] - 36 * mm
    body = check_kb.strip_comments(Path(answer).read_text(encoding="utf-8"))
    body = re.sub(r"^#\s+.*\n", "", body, count=1)          # the title is on the cover

    def footer(canvas, d):
        canvas.saveState()
        canvas.setFont("DV", 8)
        canvas.drawString(18 * mm, 10 * mm, f"{meta.get('Name', '')}  ·  {sid}")
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {d.page}")
        canvas.restoreState()

    doc.build(cover(meta, st, width) + md_flowables(body, st, width),
              onFirstPage=footer, onLaterPages=footer)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("answer")
    ap.add_argument("-o", "--out", help="output path (default: <answer folder>/<BITS_ID>.pdf)")
    ap.add_argument("--profile", choices=check_kb.PROFILES, default="full")
    a = ap.parse_args(argv)
    out = build(a.answer, a.out, a.profile)
    print(f"Built {out}. Open it and proofread it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
