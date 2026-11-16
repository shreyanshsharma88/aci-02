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
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (CondPageBreak, KeepTogether, Paragraph, Preformatted, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_kb  # noqa: E402

COURSE = "AIMLZG557 – Artificial and Computational Intelligence"
ASSIGNMENT = "Assignment 2 – Question 2 (Individual): Situated Learning"


# ------------------------------------------------------------------ fonts & styles
def register_fonts():
    ttf = Path(matplotlib.get_data_path()) / "fonts" / "ttf"   # DejaVu ships with matplotlib
    for name, file in (("DV", "DejaVuSans.ttf"), ("DV-B", "DejaVuSans-Bold.ttf"),
                       ("DV-I", "DejaVuSans-Oblique.ttf"), ("DV-BI", "DejaVuSans-BoldOblique.ttf"),
                       ("DVM", "DejaVuSansMono.ttf")):
        pdfmetrics.registerFont(TTFont(name, str(ttf / file)))
    pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-BI")


def styles():
    base = dict(fontName="DV", fontSize=9.5, leading=14,
                textColor=colors.HexColor("#263238"))
    return {
        "body": ParagraphStyle("body", **base, spaceAfter=5),
        "small": ParagraphStyle("small", **{**base, "fontSize": 8.5, "leading": 12}),
        "table_header": ParagraphStyle("table_header", fontName="DV-B", fontSize=8.5,
                                      leading=12, textColor=colors.white),
        "eyebrow": ParagraphStyle("eyebrow", fontName="DV-B", fontSize=8, leading=12,
                                 textColor=colors.HexColor("#12675f"), spaceAfter=7),
        "subtitle": ParagraphStyle("subtitle", **base, spaceAfter=7),
        "quote": ParagraphStyle("quote", **{**base, "fontName": "DV-I"}, leftIndent=10,
                                spaceAfter=5),
        "bullet": ParagraphStyle("bullet", **base, spaceAfter=2),
        "h1": ParagraphStyle("h1", fontName="DV-B", fontSize=22, leading=28, spaceBefore=4,
                             spaceAfter=7, alignment=TA_LEFT, keepWithNext=True),
        "h2": ParagraphStyle("h2", fontName="DV-B", fontSize=13, leading=17, spaceBefore=12,
                             spaceAfter=8, textColor=colors.HexColor("#12675f"),
                             keepWithNext=True),
        "h3": ParagraphStyle("h3", fontName="DV-B", fontSize=11, leading=15, spaceBefore=8,
                             spaceAfter=6, textColor=colors.HexColor("#263238"),
                             keepWithNext=False),
        "h4": ParagraphStyle("h4", fontName="DV-B", fontSize=10, leading=14, spaceBefore=6,
                             spaceAfter=4, keepWithNext=True),
        "query_heading": ParagraphStyle("query_heading", fontName="DV-B", fontSize=10,
                           leading=14, textColor=colors.white,
                           backColor=colors.HexColor("#12675f"),
                           borderPadding=(5, 8), leftIndent=8, rightIndent=8,
                           spaceBefore=12, spaceAfter=12, keepWithNext=True),
        "question": ParagraphStyle("question", **{**base, "fontName": "DV-B"},
                      spaceAfter=7, keepWithNext=True),
        "reasoning": ParagraphStyle("reasoning", **base, spaceBefore=5, spaceAfter=6),
        "decision": ParagraphStyle("decision", **base,
                      backColor=colors.HexColor("#f0f6f5"),
                      borderColor=colors.HexColor("#b9d1cd"), borderWidth=0.5,
                      borderPadding=8, leftIndent=8, rightIndent=8,
                      spaceBefore=12, spaceAfter=14),
        "discussion_heading": ParagraphStyle("discussion_heading", fontName="DV-B", fontSize=11,
                            leading=15, textColor=colors.HexColor("#12675f"),
                            spaceBefore=12, spaceAfter=7, keepWithNext=True),
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
        if re.match(r"^#{3,4}\s+Query\s+\d+\b", s):
            flush()
            end = i + 1
            while end < len(lines) and not re.match(r"^#{1,4}\s+", lines[end].strip()):
                end += 1
            content = [Paragraph(inline(re.sub(r"^#{3,4}\s+", "", s)), st["query_heading"])]
            content.extend(md_flowables("\n".join(lines[i + 1:end]), st, width))
            flow.extend([KeepTogether(content), Spacer(1, 10)])
            i = end
            continue
        if s.startswith("```"):
            flush()
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            code = "\n".join(lines[i + 1:j]).strip("\n")
            if code:
                if s == "```kb":
                    flow.extend(kb_flowables(code, st, width))
                else:
                    flow.append(Preformatted(code, st["code"], maxLineLength=96, newLineChars="  ↪ "))
            i = j + 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            flush()
            lvl = len(m.group(1))
            if lvl == 2:
                flow.append(CondPageBreak(55 * mm))
            elif lvl == 3:
                flow.append(CondPageBreak(30 * mm))
            heading_style = st[f"h{max(lvl, 2) if lvl > 1 else 1}"]
            if lvl == 3 and re.match(r"^B\.[45]\.\d+\b", m.group(2)):
                heading_style = st["discussion_heading"]
            flow.append(Paragraph(inline(m.group(2)), heading_style))
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
        if re.match(r"^\s*[-*]\s+\*\*(?:BR|PL|FOL|IR|C)\d+:\*\*", line):
            flush()
            rows = []
            while i < len(lines):
                rule = re.match(r"^\s*[-*]\s+\*\*((?:BR|PL|FOL|IR|C)\d+):\*\*\s*(.*)$", lines[i])
                if not rule:
                    break
                rows.append([Paragraph(rule.group(1), st["eyebrow"]),
                             Paragraph(inline(rule.group(2)), st["body"])])
                i += 1
            table = Table(rows, colWidths=[19 * mm, width - 19 * mm], hAlign="LEFT")
            table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1),
                 [colors.HexColor("#f0f6f5"), colors.white]),
                ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#d7e3e0")),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            flow.extend([table, Spacer(1, 6)])
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
            field = re.match(r"^\*\*(Question|Reasoning(?: chain)?|Answer):\*\*\s*(.*)$",
                             " ".join(item))
            if field:
                label = field.group(1)
                style_name = {"Question": "question", "Answer": "decision"}.get(label, "reasoning")
                displayed_label = "Decision" if label == "Answer" else label
                flow.append(Paragraph(inline(f"**{displayed_label}:** {field.group(2)}"), st[style_name]))
                continue
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


def kb_flowables(source, st, width):
    facts, rules, errors = check_kb.parse_kb(source)
    if errors:
        raise ValueError("\n".join(errors))
    unique_facts = list(dict.fromkeys(atom for atom, _ in facts))
    groups = {}
    for atom in unique_facts:
        values = "(" + ", ".join(check_kb.fmt_term(argument) for argument in atom.args) + ")"
        groups.setdefault(atom.pred, []).append(values)
    flow = []
    if groups:
        rows = [["Predicate", "Recorded tuples", "Count"]]
        rows.extend([predicate, "; ".join(values), str(len(values))]
                    for predicate, values in groups.items())
        flow.extend([CondPageBreak(30 * mm),
                     Paragraph(f"Recorded facts ({len(unique_facts)})", st["h3"]),
                     make_table(rows, st, width, [width * 0.3, width * 0.6, width * 0.1]),
                     Spacer(1, 8)])
    if rules:
        numbered_rules = []
        constraint_count = 0
        for rule in rules:
            if rule.head.pred == "false":
                constraint_count += 1
                label = f"C{constraint_count}"
            else:
                label = f"IR{rule.number}"
            numbered_rules.append(f"- **{label}:** `{rule.text}.`")
        flow.extend([CondPageBreak(30 * mm), Paragraph("Inference rules", st["h3"])])
        flow.extend(md_flowables("\n".join(numbered_rules), st, width))
    return flow


def make_table(rows, st, width, col_widths=None):
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    data = [[Paragraph(inline(c), st["table_header"] if index == 0 else st["small"])
             for c in row] for index, row in enumerate(rows)]
    lens = [max(len(r[c]) for r in rows) + 4 for c in range(ncol)]
    widths = [width * l / sum(lens) for l in lens]
    if ncol == 2:                                   # key/value or symbol/meaning tables
        widths = [max(width * 0.28, min(widths[0], width * 0.45)), 0]
        widths[1] = width - widths[0]
    t = Table(data, colWidths=col_widths if col_widths is not None else widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#d7e3e0")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12675f")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.HexColor("#f0f6f5"), colors.white]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def cover(st):
    return [Paragraph(inline(COURSE), st["eyebrow"]),
        Paragraph("Assignment 2: Situated Learning", st["h1"]),
        Paragraph("Question 2 · Knowledge Representation · Individual Assignment", st["subtitle"]),
        Spacer(1, 10)]


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
        canvas.setStrokeColor(colors.HexColor("#b9d1cd"))
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, 15 * mm, A4[0] - 18 * mm, 15 * mm)
        canvas.setFillColor(colors.HexColor("#52615e"))
        canvas.setFont("DV", 8)
        canvas.drawString(18 * mm, 10 * mm, f"AIMLZG557  ·  {sid}")
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {d.page}")
        if d.page > 1:
            canvas.setFont("DV", 7)
            canvas.drawString(18 * mm, A4[1] - 10 * mm, "SITUATED LEARNING · QUESTION 2")
        canvas.restoreState()

    doc.build(cover(st) + md_flowables(body, st, width),
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
