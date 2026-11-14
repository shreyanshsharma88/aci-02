#!/usr/bin/env python3
"""Create q2/<ID>/answer.md (skeleton, name + ID only) and q2/<ID>/TODO.md for every member.
An existing answer.md is never overwritten (it may contain the member's own work)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = (HERE / "templates" / "answer_template.md").read_text(encoding="utf-8")

TODO = """# Q2 TODO for {NAME} ({ID})

Question 2 is **individual**. Everything in your answer.md must be about **your own workplace**, written by you.
Nobody else (and no tool) fills it in for you. Estimated time: 1.5–2 hours.

Your files:
- `q2/{ID}/answer.md`: your answer (only your name and ID are pre-filled)
- `q2/{ID}/{ID}.pdf`: produced in step 8

One-time setup (from the repository root):

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Steps

- [ ] **1. Read first (about 15 min).** Open `q2/{ID}/answer.md`. Read `q2/GUIDE.md` and `q2/EXAMPLE.md`
      (illustration only, do not copy it) and skim `q2/KB_SYNTAX.md`.
- [ ] **2. B.1.** Fill in your Industry / Domain, Organisation Type, and the instructor prompt if one was given
      (otherwise write `None given`). Check that your name and ID are correct.
- [ ] **3. B.2 Anchor.** Pick a real rule-governed process from your own workplace, or the industry equivalent if
      yours has none. Describe the context, who is involved, and why decisions follow rules (about 150–250 words).
- [ ] **4. B.3 Apply.**
  - [ ] write at least 10 business rules in plain English (BR1–BR10)
  - [ ] define your propositions and write each rule in propositional logic (PL1–PL10)
  - [ ] define your predicates, variables and constants, and rewrite each rule in predicate logic with
        quantifiers (FOL1–FOL10)
  - [ ] write the KB block: at least 20 facts and at least 10 inference rules, in the `q2/KB_SYNTAX.md` format
  - [ ] write 5 workplace queries and, for each, the answer and the reasoning chain
- [ ] **5. Check.** Run the checker. Fix everything it flags (missing counts, undefined predicates, queries that
      don't follow) and re-run until it says `RESULT: PASS`.

```bash
python q2/check_kb.py q2/{ID}/answer.md
```

- [ ] **6. B.4 Analyse.** Explain how predicate logic is more expressive than propositional logic in your
      scenario, how effective your KB is, and what knowledge is missing or what limits it (about 200–300 words).
- [ ] **7. B.5 Reflect.** Describe the deployment constraints (incomplete knowledge, changing rules, privacy,
      scale, technology), then recommend and justify the single most important improvement (about 200–300 words).
- [ ] **8. Build the PDF.** This produces `q2/{ID}/{ID}.pdf`. Open it and proofread it.

```bash
python q2/build_pdf.py q2/{ID}/answer.md
```

- [ ] **9. Hand over.** Give `q2/{ID}/{ID}.pdf` to the person submitting (or commit `answer.md` and the PDF, but
      **only once the GitHub repo is private**), and confirm your name and ID on the cover.
- [ ] **10. Verify the zip.** When the submitter shares the final zip, open it and check that `{ID}.pdf` is inside,
      is your latest version, and shows your name and ID. Full instructions: README.md §1.
"""


def main():
    members = json.loads((HERE / "members.json").read_text(encoding="utf-8"))
    for m in members:
        d = HERE / m["id"]
        d.mkdir(exist_ok=True)
        ans = d / "answer.md"
        if ans.exists():
            print(f"keep    {ans.relative_to(HERE.parent)} (already exists)")
        else:
            ans.write_text(TEMPLATE.replace("{NAME}", m["name"]).replace("{ID}", m["id"]),
                           encoding="utf-8")
            print(f"created {ans.relative_to(HERE.parent)}")
        (d / "TODO.md").write_text(TODO.replace("{NAME}", m["name"]).replace("{ID}", m["id"]),
                                   encoding="utf-8")
        print(f"wrote   {(d / 'TODO.md').relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
