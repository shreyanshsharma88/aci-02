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


def test_build_refuses_failing_answer(tmp_path):
    with pytest.raises(SystemExit) as e:
        build_pdf.build(EXAMPLE, tmp_path / "x.pdf", profile="full")   # 4 rules < 10
    assert "REFUSING" in str(e.value) and "4/10" in str(e.value)
    assert not (tmp_path / "x.pdf").exists()


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
