#!/usr/bin/env python3
"""Verify the final submission zip.

Usage:  python check_submission.py [dist/<group>_ACI_Assignment2.zip]
(with no argument, the newest zip in dist/ is checked)

Checks:
  * exactly 6 files at the top level: Question1_Group.ipynb + <BITS_ID>.pdf for each of the 5 members
  * each PDF opens, its cover (page 1) shows the matching name and BITS ID, and B.2-B.5 have content
  * the notebook is valid, every code cell has been executed, and there are outputs and no errors
"""
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import pypdf

ROOT = Path(__file__).resolve().parent
MEMBERS = json.loads((ROOT / "q2" / "members.json").read_text(encoding="utf-8"))
NOTEBOOK = "Question1_Group.ipynb"
SECTIONS = ["B.2 Anchor", "B.3 Apply", "B.4 Analyse", "B.5 Reflect"]


def squash(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def check_pdf(data, member):
    problems = []
    try:
        reader = pypdf.PdfReader(io.BytesIO(data))
        pages = [p.extract_text() or "" for p in reader.pages]
    except Exception as e:                                   # noqa: BLE001
        return [f"cannot open PDF: {e}"]
    cover = squash(pages[0]) if pages else ""
    if squash(member["name"]) not in cover:
        problems.append(f"cover does not show the name '{member['name']}'")
    if member["id"].lower() not in cover:
        problems.append(f"cover does not show the BITS ID {member['id']}")
    text = "\n".join(pages)
    pos = {}
    for s in SECTIONS:                                   # full heading text, e.g. "B.4 Analyse"
        m = list(re.finditer(re.escape(s) + r"\b", text))
        pos[s] = m[0].start() if m else -1
    for i, s in enumerate(SECTIONS):
        if pos[s] < 0:
            problems.append(f"section {s} heading not found")
            continue
        nxt = [pos[t] for t in SECTIONS[i + 1:] if pos[t] > pos[s]]
        chunk = text[pos[s]:min(nxt) if nxt else len(text)]
        words = len(re.findall(r"\w+", chunk))
        if words < 30:
            problems.append(f"section {s} has almost no content ({words} words)")
        if "TODO" in chunk:
            problems.append(f"section {s} still contains TODO")
    return problems


def check_notebook(data):
    try:
        nb = json.loads(data)
    except ValueError as e:
        return [f"notebook is not valid JSON: {e}"]
    code = [c for c in nb.get("cells", []) if c.get("cell_type") == "code"]
    problems = []
    if not code:
        problems.append("notebook has no code cells")
    if not any(c.get("outputs") for c in code):
        problems.append("notebook has no outputs (execute it before zipping)")
    unexec = sum(1 for c in code if not c.get("execution_count"))
    if unexec:
        problems.append(f"{unexec} code cell(s) were not executed")
    errs = sum(1 for c in code for o in c.get("outputs", []) if o.get("output_type") == "error")
    if errs:
        problems.append(f"{errs} cell(s) have error outputs")
    return problems


def check_zip(path):
    results = []                                             # (ok, message)
    try:
        zf = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, FileNotFoundError) as e:
        return [(False, f"cannot open zip {path}: {e}")]
    names = [n for n in zf.namelist() if not n.endswith("/")]
    expected = [NOTEBOOK] + [f"{m['id']}.pdf" for m in MEMBERS]
    nested = [n for n in names if "/" in n or "\\" in n]
    results.append((not nested, "all files at the top level" if not nested
                    else f"files inside folders (must be top level): {', '.join(nested)}"))
    missing = [e for e in expected if e not in names]
    extra = [n for n in names if n not in expected]
    results.append((len(names) == len(expected),
                    f"zip holds {len(names)} file(s); required exactly {len(expected)}"))
    results.append((not missing, "no required file missing" if not missing
                    else "MISSING: " + ", ".join(missing)))
    results.append((not extra, "no unexpected files" if not extra
                    else "unexpected files: " + ", ".join(extra)))
    if NOTEBOOK in names:
        p = check_notebook(zf.read(NOTEBOOK))
        results.append((not p, f"{NOTEBOOK}: " + ("executed, has outputs, no errors" if not p
                                                   else "; ".join(p))))
    for m in MEMBERS:
        fn = f"{m['id']}.pdf"
        if fn in names:
            p = check_pdf(zf.read(fn), m)
            results.append((not p, f"{fn} ({m['name']}): " + ("cover name/ID match, B.2-B.5 have content"
                                                              if not p else "; ".join(p))))
    return results


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        path = Path(argv[0])
    else:
        zips = sorted((ROOT / "dist").glob("*.zip"), key=lambda p: p.stat().st_mtime)
        if not zips:
            print("No zip found in dist/. Run: bash make_zip.sh")
            return 1
        path = zips[-1]
    print(f"Checking {path}\n")
    results = check_zip(path)
    for ok, msg in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {msg}")
    good = all(ok for ok, _ in results)
    print("\nRESULT: " + ("PASS - ready to upload through the portal" if good else
                          "FAIL - do not submit until every item passes"))
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
