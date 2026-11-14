# Q2 TODO for SATHIYALATHASHRI N (2025AG05239)

Question 2 is **individual**. Everything in your answer.md must be about **your own workplace**, written by you.
Nobody else (and no tool) fills it in for you. Estimated time: 1.5–2 hours.

Your files:
- `q2/2025AG05239/answer.md`: your answer (only your name and ID are pre-filled)
- `q2/2025AG05239/2025AG05239.pdf`: produced in step 8

One-time setup (from the repository root):

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

- [ ] **1. Read first (about 15 min).** Open `q2/2025AG05239/answer.md`. Read `q2/GUIDE.md` and `q2/EXAMPLE.md`
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
python q2/check_kb.py q2/2025AG05239/answer.md
```

- [ ] **6. B.4 Analyse.** Explain how predicate logic is more expressive than propositional logic in your
      scenario, how effective your KB is, and what knowledge is missing or what limits it (about 200–300 words).
- [ ] **7. B.5 Reflect.** Describe the deployment constraints (incomplete knowledge, changing rules, privacy,
      scale, technology), then recommend and justify the single most important improvement (about 200–300 words).
- [ ] **8. Build the PDF.** This produces `q2/2025AG05239/2025AG05239.pdf`. Open it and proofread it.

```bash
python q2/build_pdf.py q2/2025AG05239/answer.md
```

- [ ] **9. Hand over.** Give `q2/2025AG05239/2025AG05239.pdf` to the person submitting (or commit `answer.md` and the PDF, but
      **only once the GitHub repo is private**), and confirm your name and ID on the cover.
- [ ] **10. Verify the zip.** When the submitter shares the final zip, open it and check that `2025AG05239.pdf` is inside,
      is your latest version, and shows your name and ID. Full instructions: README.md §1.
