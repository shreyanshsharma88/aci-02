#!/usr/bin/env python3
"""Print each member's Q2 status from the files actually present:
pending (checker fails) / checked (checker passes, no PDF yet) / PDF built."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_kb  # noqa: E402

print(f"| {'Member':<30} | {'BITS ID':<11} | Q2 status |")
print(f"|{'-' * 32}|{'-' * 13}|-----------|")
for m in json.loads((HERE / "members.json").read_text(encoding="utf-8")):
    d = HERE / m["id"]
    rep = check_kb.check(d / "answer.md")
    if (d / f"{m['id']}.pdf").exists() and rep.passed:
        s = "PDF built"
    elif rep.passed:
        s = "checked (PDF not built)"
    else:
        s = f"pending ({len(rep.failures())} checker items open)"
    print(f"| {m['name']:<30} | {m['id']:<11} | {s} |")
