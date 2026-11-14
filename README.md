# AIMLZG557 – Artificial and Computational Intelligence
## Assignment 2 – Situated Learning (10 marks) · Group `<GROUP NO>`

| # | Name | BITS ID | Email |
|---|---|---|---|
| 1 | LAKSHYA KANCHAN | 2025AG05062 | 2025ag05062@wilp.bits-pilani.ac.in |
| 2 | SHREYANSH SHARMA | 2025AG05772 | 2025ag05772@wilp.bits-pilani.ac.in |
| 3 | VINAY PRATAP SINGH BHADAURIA | 2025AG05689 | 2025ag05689@wilp.bits-pilani.ac.in |
| 4 | ABHISHEK GHOSH | 2025AG05076 | 2025ag05076@wilp.bits-pilani.ac.in |
| 5 | SATHIYALATHASHRI N | 2025AG05239 | 2025ag05239@wilp.bits-pilani.ac.in |

---

## 1. What the assignment asks

**Question 1: Gaming problem (group, 5 marks).** Simulate a small chess variant on the 3×3 board in the assignment
image, with Soldiers (pawns) and Horses (knights). A side wins when the opponent has lost every piece. We must
design and justify a **static evaluation function (no ML)**, explain it on a sample game state, and implement
**Minimax** in Python, with one player being a **human giving live input** and the other the program.
→ One notebook for the group: `Question1_Group.ipynb`.

**Question 2: Situated learning (individual, 5 marks).** Each member picks a rule-governed process from **their own
workplace** and represents it with propositional logic, predicate logic and a knowledge base:
≥10 rules in both logics, ≥20 facts, ≥10 inference rules, and 5 queries answered by reasoning. Then they analyse it
and reflect on deployment. Rubric: Anchor 1 · Apply 2 · Analyse 1 · Reflect 1.
→ One PDF per member, named `<BITS_ID>.pdf`.

**Submission rules (from the assignment document)**
* **One ZIP per group** containing **exactly 6 files** at the top level: `Question1_Group.ipynb`, `2025AG05062.pdf`,
  `2025AG05772.pdf`, `2025AG05689.pdf`, `2025AG05076.pdf`, `2025AG05239.pdf`.
* Do not submit an incomplete ZIP. **A member whose PDF is missing from the ZIP gets no Q2 marks.**
* Upload **through the assignment portal only**; email submissions are not accepted. Submit on or before the deadline.
* **Every member** is responsible for checking that the ZIP contains every required document.

---

## 2. What has been done, and how

### Q1 (done and tested)

* **Code:** `q1/game.py` is the single source. `q1/build_notebook.py` inlines it into `Question1_Group.ipynb`, so the
  notebook is self-contained, and the notebook has been executed so it contains all outputs.
* **Board:** 3×3. White S a3, White H b3 (moves down); Black S b1, Black H c1 (moves up).
  **Human = White, moves first; computer = Black** (both configurable).
* **Rule interpretations:** see §8.
* **Evaluation function** (White's view, White minus Black, hand-set weights, no ML):
  `E = material (S=10, H=30) + 1·mobility + 2·pawn advancement + 3·threats − 0.5·value of each attacked-and-undefended piece`.
  Terminal positions score ±(1000 − ply).
  Worked example in the notebook (White S a2, H a1; Black S c2, H b3; White to move):
  material 0, mobility −1, advancement 0, threats +3, safety −10, **total −8**. A 1-ply search then finds
  H a1xb3 (+13), which shows why the evaluation is used inside Minimax and not on its own.
* **Search:** plain **Minimax** (used by the computer player; default depth 8) and **alpha-beta** (same move,
  fewer nodes: at depth 8 from the start, 2036 vs 125 nodes). With these rules, White (moving first) has a forced win
  in 3 plies (H b3xc1).
* **Play:** `input()` loop with validation (`b3 c1`, `moves`, `quit`). `AUTO_DEMO = True` replays a scripted human
  game so the notebook runs end to end.
* **Tests:** `tests/test_game.py` covers move legality for each piece including the edges, knight jumps, pawn diagonal
  only on capture, no landing on a friendly piece, win/pass/draw rules, mate-in-1 for both colours, evaluation
  symmetry, alpha-beta = minimax on random positions, input validation, the scripted game, and the notebook being in
  sync with `game.py` and executed.

### Q2 (preparation only; each member writes their own answer)

Nothing in any member's answer has been written for them: only their **name and BITS ID** are pre-filled.

| File | Purpose |
|---|---|
| `q2/<ID>/answer.md` | Skeleton per member: every B.1–B.5 heading, table and numbered slot (BR1–10, PL1–10, FOL1–10, Fact 1–20, Inference rule 1–10, Query 1–5), with guidance in comments |
| `q2/<ID>/TODO.md` | That member's 9-step checklist with their ID in every command |
| `q2/GUIDE.md` | Business rule → propositional → predicate logic; facts vs rules; queries, forward/backward chaining, modus ponens; common mistakes |
| `q2/EXAMPLE.md` | **Illustration only** (public library book loans): 4 rules in both logics, KB, 2 queries with reasoning chains |
| `q2/KB_SYNTAX.md` | Syntax of the ```` ```kb ```` and ```` ```query ```` blocks (Datalog/Horn clauses, `not`, comparisons) |
| `q2/check_kb.py` | Checker: section completeness, counts, undefined propositions/predicates, PL well-formedness, quantifiers, KB syntax; **forward chaining** with derivation traces; verifies each query's expected answer; warns about rules that never fire and unused facts; flags contradictions. Prints a PASS/FAIL checklist. |
| `q2/build_pdf.py` | Renders answer.md into `<ID>.pdf` (cover with name, ID, domain and organisation type; tables; ∀∃∧∨¬→ in DejaVu fonts). **Refuses to build** while the checker fails. |
| `q2/status.py` | Prints each member's status from the files present |
| `q2/make_skeletons.py` | Re-creates missing skeletons and TODO files (never overwrites an answer.md) |

Tests: `tests/test_check_kb.py`, `tests/test_build_pdf.py`, `tests/test_submission.py`.

---

## 3. How to run

```bash
# setup (once)
python3 -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Q1: rebuild and execute the notebook (outputs saved into the file)
python q1/build_notebook.py
jupyter nbconvert --to notebook --execute --inplace Question1_Group.ipynb

# Q1: play interactively
jupyter notebook Question1_Group.ipynb
#   in Section 7 set AUTO_DEMO = False (HUMAN_SIDE / DEPTH optional), then run all cells.
#   Type moves like:  b3 c1     (also: moves, quit)
#   AUTO_DEMO = True replays the scripted human moves instead (no typing needed).

# tests (Q1 + Q2 tooling + packaging)
python -m pytest -q

# Q2: check and build one member's PDF
python q2/check_kb.py q2/<BITS_ID>/answer.md
python q2/build_pdf.py q2/<BITS_ID>/answer.md        # -> q2/<BITS_ID>/<BITS_ID>.pdf
python q2/check_kb.py q2/EXAMPLE.md --profile example # the example passes with the reduced profile
python q2/status.py

# packaging
GROUP=<GroupNo> bash make_zip.sh                      # -> dist/<GroupNo>_ACI_Assignment2.zip, then verifies it
python check_submission.py                            # re-check the newest zip in dist/
```

---

## 4. **WHAT EACH MEMBER MUST DO FOR Q2**

Q2 is **individual**. Write about **your own workplace**, in your own words. Estimated time: **1.5–2 hours**.

1. Open `q2/<your BITS ID>/answer.md`. Read `q2/GUIDE.md` and `q2/EXAMPLE.md` first (about 15 min).
2. **B.1:** fill in your name, ID, industry/domain, organisation type, and the instructor prompt if one was given.
3. **B.2 Anchor:** pick a real rule-governed process from your own workplace, or the industry equivalent if yours
   has none. Describe the context, who is involved, and why decisions follow rules (about 150–250 words).
4. **B.3 Apply:**
   - write at least 10 business rules in plain English
   - define your propositions and write each rule in propositional logic
   - define your predicates, variables and constants, and rewrite each rule in predicate logic with quantifiers
   - write the KB block: at least 20 facts and at least 10 inference rules, in the `q2/KB_SYNTAX.md` format
   - write 5 workplace queries and, for each, the answer and the reasoning chain
5. Run `python q2/check_kb.py q2/<ID>/answer.md`. Fix everything it flags (missing counts, undefined predicates,
   queries that don't follow) and re-run until it passes.
6. **B.4 Analyse:** explain how predicate logic is more expressive than propositional logic in your scenario, how
   effective your KB is, and what knowledge is missing or what limits it (about 200–300 words).
7. **B.5 Reflect:** describe the deployment constraints (incomplete knowledge, changing rules, privacy, scale,
   technology), then recommend and justify the single most important improvement (about 200–300 words).
8. Run `python q2/build_pdf.py q2/<ID>/answer.md`. This produces `q2/<ID>/<ID>.pdf`. Open it and proofread it.
9. Give the PDF (or your committed answer.md) to the person submitting, and confirm your name and ID on the cover.

Ready-to-copy commands (run from the repository root, after the setup in §3):

**LAKSHYA KANCHAN – 2025AG05062**
```bash
python q2/check_kb.py q2/2025AG05062/answer.md
python q2/build_pdf.py q2/2025AG05062/answer.md
```

**SHREYANSH SHARMA – 2025AG05772**
```bash
python q2/check_kb.py q2/2025AG05772/answer.md
python q2/build_pdf.py q2/2025AG05772/answer.md
```

**VINAY PRATAP SINGH BHADAURIA – 2025AG05689**
```bash
python q2/check_kb.py q2/2025AG05689/answer.md
python q2/build_pdf.py q2/2025AG05689/answer.md
```

**ABHISHEK GHOSH – 2025AG05076**
```bash
python q2/check_kb.py q2/2025AG05076/answer.md
python q2/build_pdf.py q2/2025AG05076/answer.md
```

**SATHIYALATHASHRI N – 2025AG05239**
```bash
python q2/check_kb.py q2/2025AG05239/answer.md
python q2/build_pdf.py q2/2025AG05239/answer.md
```

---

## 5. **WHAT THE SUBMITTER MUST DO**

1. Collect all 5 PDFs into their folders: `q2/<ID>/<ID>.pdf` (or pull each member's committed answer.md and run
   `python q2/build_pdf.py q2/<ID>/answer.md`).
2. Build and verify the zip:
   ```bash
   GROUP=<GroupNo> bash make_zip.sh
   python check_submission.py
   ```
   Both must end with `RESULT: PASS` (6 files; each cover shows the right name and ID; the notebook has outputs).
3. Send the zip to **every member** and have each one open it and confirm their PDF is inside and correct.
4. Upload `dist/<GroupNo>_ACI_Assignment2.zip` **through the assignment portal (not email)** before the deadline.

---

## 6. Status

Status from the files present when this README was written. Run `python q2/status.py` for the live state.

| Item | Status |
|---|---|
| Q1 notebook `Question1_Group.ipynb` | **Done**: executed with outputs; 22 Q1 tests pass |
| Q2 tooling (checker, PDF builder, packaging) | **Done**: tested (54 tests in total pass) |
| LAKSHYA KANCHAN (2025AG05062) Q2 | pending: skeleton only |
| SHREYANSH SHARMA (2025AG05772) Q2 | pending: skeleton only |
| VINAY PRATAP SINGH BHADAURIA (2025AG05689) Q2 | pending: skeleton only |
| ABHISHEK GHOSH (2025AG05076) Q2 | pending: skeleton only |
| SATHIYALATHASHRI N (2025AG05239) Q2 | pending: skeleton only |
| Final zip | not built: `make_zip.sh` refuses until all 5 PDFs exist |

---

## 7. Repository layout

```
Question1_Group.ipynb        Q1 deliverable (generated from q1/, executed)
q1/game.py                   game engine, evaluation, minimax, alpha-beta, human play
q1/build_notebook.py         builds the notebook from game.py
q2/GUIDE.md EXAMPLE.md KB_SYNTAX.md
q2/check_kb.py build_pdf.py status.py make_skeletons.py members.json templates/
q2/<BITS_ID>/answer.md TODO.md   one folder per member
tests/                       pytest suite
make_zip.sh check_submission.py
PLAN.md                      plan, docx audit, status
```

---

## 8. Q1 rule interpretations and assumptions

| # | Rule | Interpretation (configurable flag) | Why |
|---|---|---|---|
| D1 | Pawn straight | 1 step forward onto an **empty** square | "only one straight step ahead"; a straight step does not capture |
| D2 | Pawn diagonal | 1 step diagonally forward **only to capture** | "only if opponent coins are available … to attack" |
| D3 | Pawn extras | no double step, no en passant | "only one" step |
| D4 | Knight | full chess L: (±2,±1) and (±1,±2); `ALLOW_SIDEWAYS_L = True` | every L changes the rank, so it is "forward/backward"; standard chess knight. `False` keeps only (±2 ranks, ±1 file). |
| D5 | Knight jump | ignores pieces in between | "only piece that can jump" |
| D6 | Friendly squares | never land on your own piece | chess rule |
| D7 | Win | opponent has no pieces left | docx win condition |
| D8 | No legal move | `NO_MOVE_RULE = "pass"`; if neither side can move → draw (`"loss"`/`"draw"` available) | the docx defines only one way to win; pawns get stuck easily on 3×3 |
| D9 | Draws | `MAX_PLIES = 40` and threefold repetition | knights could shuffle forever |
| D10 | Promotion | none: a pawn on the last rank is frozen | not in the docx |
| D11 | King/check | none | no king on this board |
