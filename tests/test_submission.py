"""Packaging checks. PDFs here are throw-away fixtures built from EXAMPLE.md in a temp folder,
only to exercise check_submission.py; nothing is written into q2/."""
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest

import build_pdf
import check_submission as cs

ROOT = Path(__file__).resolve().parents[1]
MEMBERS = json.loads((ROOT / "q2" / "members.json").read_text())


@pytest.fixture(scope="module")
def fixture_pdfs(tmp_path_factory):
    d = tmp_path_factory.mktemp("pdfs")
    src = (ROOT / "q2" / "EXAMPLE.md").read_text()
    out = {}
    for m in MEMBERS:
        ans = d / m["id"] / "answer.md"
        ans.parent.mkdir()
        ans.write_text(src.replace("| Name | Illustration only |", f"| Name | {m['name']} |")
                          .replace("| ID No | EXAMPLE |", f"| ID No | {m['id']} |"))
        out[m["id"]] = build_pdf.build(ans, d / f"{m['id']}.pdf", profile="example")
    return out


def make_zip(path, files):
    with zipfile.ZipFile(path, "w") as z:
        for arc, src in files.items():
            if isinstance(src, bytes):
                z.writestr(arc, src)
            else:
                z.write(src, arcname=arc)
    return path


def all_files(pdfs):
    f = {"Question1_Group.ipynb": ROOT / "Question1_Group.ipynb"}
    f.update({f"{i}.pdf": p for i, p in pdfs.items()})
    return f


def fails(results):
    return [m for ok, m in results if not ok]


def test_complete_zip_passes(tmp_path, fixture_pdfs):
    z = make_zip(tmp_path / "ok.zip", all_files(fixture_pdfs))
    assert fails(cs.check_zip(z)) == []


def test_missing_pdf_fails(tmp_path, fixture_pdfs):
    f = all_files(fixture_pdfs)
    del f["2025AG05239.pdf"]
    out = " | ".join(fails(cs.check_zip(make_zip(tmp_path / "m.zip", f))))
    assert "MISSING: 2025AG05239.pdf" in out and "exactly 6" in out


def test_extra_and_nested_files_fail(tmp_path, fixture_pdfs):
    f = all_files(fixture_pdfs)
    f["q2/2025AG05062.pdf"] = f.pop("2025AG05062.pdf")
    f["notes.txt"] = b"x"
    out = " | ".join(fails(cs.check_zip(make_zip(tmp_path / "n.zip", f))))
    assert "top level" in out and "unexpected files" in out


def test_pdf_with_wrong_name_on_cover_fails(tmp_path, fixture_pdfs):
    f = all_files(fixture_pdfs)
    f["2025AG05062.pdf"] = fixture_pdfs["2025AG05772"]          # someone else's PDF under this ID
    out = " | ".join(fails(cs.check_zip(make_zip(tmp_path / "w.zip", f))))
    assert "2025AG05062.pdf" in out and "cover does not show" in out


def test_unexecuted_notebook_fails(tmp_path, fixture_pdfs):
    nb = json.loads((ROOT / "Question1_Group.ipynb").read_text())
    for c in nb["cells"]:
        if c["cell_type"] == "code":
            c["outputs"], c["execution_count"] = [], None
    f = all_files(fixture_pdfs)
    f["Question1_Group.ipynb"] = json.dumps(nb).encode()
    out = " | ".join(fails(cs.check_zip(make_zip(tmp_path / "u.zip", f))))
    assert "no outputs" in out and "not executed" in out


def test_make_zip_refuses_when_pdfs_missing(tmp_path):
    work = tmp_path / "repo"
    work.mkdir()
    for name in ("make_zip.sh", "check_submission.py", "Question1_Group.ipynb"):
        shutil.copy(ROOT / name, work / name)
    (work / "q2").mkdir()
    shutil.copy(ROOT / "q2" / "members.json", work / "q2" / "members.json")
    r = subprocess.run(["bash", "make_zip.sh"], cwd=work, capture_output=True, text=True)
    assert r.returncode == 1
    assert "REFUSING" in r.stdout
    for m in MEMBERS:
        assert m["name"] in r.stdout
    assert not (work / "dist").exists()


def test_make_zip_builds_and_checks(tmp_path, fixture_pdfs):
    work = tmp_path / "repo"
    work.mkdir()
    for name in ("make_zip.sh", "check_submission.py", "Question1_Group.ipynb"):
        shutil.copy(ROOT / name, work / name)
    (work / "q2").mkdir()
    shutil.copy(ROOT / "q2" / "members.json", work / "q2" / "members.json")
    for i, p in fixture_pdfs.items():
        (work / "q2" / i).mkdir()
        shutil.copy(p, work / "q2" / i / f"{i}.pdf")
    venv = ROOT / ".venv"
    if venv.exists():
        (work / ".venv").symlink_to(venv)
    r = subprocess.run(["bash", "make_zip.sh"], cwd=work, capture_output=True, text=True,
                       env={"GROUP": "GroupTest", "PATH": "/usr/bin:/bin"})
    assert r.returncode == 0, r.stdout + r.stderr
    z = work / "dist" / "GroupTest_ACI_Assignment2.zip"
    assert sorted(zipfile.ZipFile(z).namelist()) == sorted(
        ["Question1_Group.ipynb"] + [f"{m['id']}.pdf" for m in MEMBERS])
    assert "RESULT: PASS" in r.stdout
