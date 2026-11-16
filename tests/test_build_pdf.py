from pathlib import Path

import pypdf
import pytest

import build_pdf

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "q2" / "EXAMPLE.md"


def test_build_succeeds_for_passing_answer(tmp_path):
    out = build_pdf.build(EXAMPLE, tmp_path / "EXAMPLE.pdf", profile="example")
    reader = pypdf.PdfReader(str(out))
    text = "\n".join(p.extract_text() for p in reader.pages)
    first = reader.pages[0].extract_text()
    assert "Illustration only" in first and "EXAMPLE" in first
    for heading in ("B.1 Submission Form", "B.2 Anchor", "B.3 Apply", "B.4 Analyse", "B.5 Reflect"):
        assert heading in text
    assert "∀m" in text and "→" in text and "¬" in text          # logic notation survives
    assert "approved(M, B) :- eligible(M)" in text               # KB block rendered
    assert "TODO" not in text and "<!--" not in text
    assert first.count("Industry / Domain") == 1
    for page in reader.pages:
        last_line = page.extract_text().strip().splitlines()[-1]
        assert not last_line.startswith(("B.1 ", "B.2 ", "B.3", "B.4 ", "B.5 ", "Query "))


def test_numbered_rules_render_as_two_column_rows(tmp_path):
    build_pdf.register_fonts()
    flow = build_pdf.md_flowables(
        "- **PL1:** P1 ∧ P2 → P3\n- **PL2:** ¬P3 → P4", build_pdf.styles(), 480)
    table = flow[0]
    assert isinstance(table, build_pdf.Table)
    out = tmp_path / "rules.pdf"
    build_pdf.SimpleDocTemplate(str(out)).build(flow)
    text = "\n".join(page.extract_text() for page in pypdf.PdfReader(out).pages)
    assert "PL1" in text and "P1 ∧ P2 → P3" in text
    assert "PL2" in text and "¬P3 → P4" in text


def test_kb_renders_grouped_facts_and_preserves_rules(tmp_path):
    build_pdf.register_fonts()
    source = """```kb
% A comment is not a recorded fact.
item('a.b', 1.5). item('a,b', 2). item('a.b', 1.5).
ready.
approved(X) :- item(X, N), gt(N, 1).
false :- approved(X), blocked(X).
```"""
    out = tmp_path / "grouped.pdf"
    build_pdf.SimpleDocTemplate(str(out)).build(
        build_pdf.md_flowables(source, build_pdf.styles(), 480))
    text = "\n".join(page.extract_text() for page in pypdf.PdfReader(out).pages)
    assert "Recorded facts (3)" in text
    assert "Recorded tuples" in text and "Count" in text
    assert "('a.b', 1.5); ('a,b', 2)" in text
    assert "ready" in text and "()" in text
    assert "IR1" in text and "approved(X) :- item(X, N), gt(N, 1)." in text
    assert "C1" in text and "false :- approved(X), blocked(X)." in text
    assert "A comment" not in text


def test_build_refuses_failing_answer(tmp_path):
    with pytest.raises(SystemExit) as e:
        build_pdf.build(EXAMPLE, tmp_path / "x.pdf", profile="full")   # 4 rules < 10
    assert "REFUSING" in str(e.value) and "4/10" in str(e.value)
    assert not (tmp_path / "x.pdf").exists()


def test_short_query_stays_on_one_page(tmp_path):
    build_pdf.register_fonts()
    steps = "\n".join(f"{number}. " + "The recorded facts satisfy this condition. " * 7
                      for number in range(1, 5))
    source = ("#### Query 1\n\n- **Question:** May this change proceed?\n\n"
              "```query\n?- schedulable(chg101).\nexpect: yes\n```\n\n"
              f"- **Reasoning chain:** Check the conditions in order.\n\n{steps}\n\n"
              "- **Answer:** Yes, the change may proceed.")
    out = tmp_path / "query.pdf"
    flow = [build_pdf.Spacer(1, 500)]
    flow.extend(build_pdf.md_flowables(source, build_pdf.styles(), 450))
    build_pdf.SimpleDocTemplate(str(out)).build(flow)
    pages = [page.extract_text() for page in pypdf.PdfReader(out).pages]
    assert len(pages) == 2
    assert "Query 1" not in pages[0]
    assert "Query 1" in pages[1] and "Yes, the change may proceed." in pages[1]
    assert "Decision:" in pages[1]


@pytest.mark.parametrize("label, expected_style, displayed_label", [
    ("Question", "question", "Question:"),
    ("Reasoning chain", "reasoning", "Reasoning chain:"),
    ("Answer", "decision", "Decision:"),
])
def test_query_fields_have_dedicated_styles(label, expected_style, displayed_label):
    flow = build_pdf.md_flowables(f"- **{label}:** A workplace explanation.", build_pdf.styles(), 480)
    paragraph = flow[0]
    assert paragraph.style.name == expected_style
    assert paragraph.getPlainText().startswith(displayed_label)
    assert paragraph.bulletText is None


def test_discussion_subheadings_match_accent_and_stay_with_text():
    palette = build_pdf.styles()
    flow = build_pdf.md_flowables(
        "### B.4.1 Expressiveness in this process\n\nAn explanation of the policy.", palette, 480)
    headings = [item for item in flow if isinstance(item, build_pdf.Paragraph)]
    assert headings[0].style.textColor == palette["h2"].textColor
    assert headings[0].style.keepWithNext


def test_build_refuses_skeleton(tmp_path):
    skel = ROOT / "q2" / "2025AG05062" / "answer.md"
    if "TODO" not in skel.read_text():
        pytest.skip("member has started filling in the answer")
    with pytest.raises(SystemExit) as e:
        build_pdf.build(skel, tmp_path / "y.pdf")
    assert "B.2 Anchor" in str(e.value)


def test_build_refuses_unknown_id_in_full_profile(tmp_path, monkeypatch):
    rep = build_pdf.check_kb.Report()
    rep.meta = {"ID No": "2099XX00000"}
    monkeypatch.setattr(build_pdf.check_kb, "check", lambda *a, **k: rep)
    with pytest.raises(SystemExit) as e:
        build_pdf.build(EXAMPLE, tmp_path / "z.pdf")
    assert "members.json" in str(e.value)
