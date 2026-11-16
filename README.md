# AIMLZG557 – Artificial and Computational Intelligence
## Assignment 2 – Situated Learning (10 marks) · Group `70`

| # | Name | BITS ID | Email |
|---|---|---|---|
| 1 | LAKSHYA KANCHAN | 2025AG05062 | 2025ag05062@wilp.bits-pilani.ac.in |
| 2 | SHREYANSH SHARMA | 2025AG05772 | 2025ag05772@wilp.bits-pilani.ac.in |
| 3 | VINAY PRATAP SINGH BHADAURIA | 2025AG05689 | 2025ag05689@wilp.bits-pilani.ac.in |
| 4 | ABHISHEK GHOSH | 2025AG05076 | 2025ag05076@wilp.bits-pilani.ac.in |
| 5 | SATHIYALATHASHRI N | 2025AG05239 | 2025ag05239@wilp.bits-pilani.ac.in |

> Four Q2 PDFs are present; only SHREYANSH SHARMA's (2025AG05772) is missing.
> The Q1 notebook still has four unexecuted code cells. Complete these items before building the final ZIP.

**Contents**
1. [Manual steps: everything a human still has to do](#1-manual-steps-everything-a-human-still-has-to-do)
2. [What the assignment asks](#2-what-the-assignment-asks)
3. [What has been done, and how](#3-what-has-been-done-and-how)
4. [How to run (reference)](#4-how-to-run-reference)
5. [Status](#5-status)
6. [Q1 rule interpretations and assumptions](#6-q1-rule-interpretations-and-assumptions)
7. [Troubleshooting](#7-troubleshooting)
8. [Repository layout](#8-repository-layout)

---

## 1. Manual steps: everything a human still has to do

The steps are grouped by who does them. Do them in order: A, B, C (all members in parallel), then D.

### A. Repository owner (SHREYANSH SHARMA)

1. Make the GitHub repository private. It is currently public, so anyone, including other groups, can copy
   the Q1 notebook, and every member's workplace content would be published once committed.
   GitHub → `shreyanshsharma88/aci-02` → Settings → General → scroll to Danger Zone → Change
   repository visibility → Make private.
2. Give the other four members access (only if they will use git): Settings → Collaborators →
   Add people → add each member's GitHub username. Members who don't use git can work from a downloaded copy
   (see C.1) and send their PDF to the submitter instead.
3. Pick the submitter, the one person who will build and upload the zip (section D). Tell the group who it is.

### B. Everyone: review Q1, about 15 minutes

Q1 is a group submission, so every member should know what is in it.

1. Open `Question1_Group.ipynb` (on GitHub, or locally with `jupyter notebook Question1_Group.ipynb`).
2. Read Section 2 (rule interpretations) and Section 5 (evaluation function and worked example). These are
   the design decisions the evaluator will look at. They are also summarised in [§6](#6-q1-rule-interpretations-and-assumptions).
3. Optional: play against the computer. In Section 7 set `AUTO_DEMO = False`, then Run All. Type moves like
   `b3 c1`; `moves` lists your legal moves and `quit` stops the game. Set it back to `AUTO_DEMO = True` before
   the final notebook is saved: the submitted file must run without typing.
4. If the group disagrees with an interpretation (for example, the knight's sideways L), change the flag in
   `q1/game.py` (`ALLOW_SIDEWAYS_L`, `NO_MOVE_RULE`, `MAX_PLIES`), then rebuild, execute and test using section 4. Some
   notebook text quotes specific results, so re-read Sections 8–9 after any change.

### C. Outstanding Q2: SHREYANSH SHARMA (2025AG05772)

Only 2025AG05772 still needs an answer and PDF. The writing steps below apply to that member.
The other four members' TODO files now contain only final review and submission checks.
The three supplied PDFs are complete deliverables even though their local answer.md files remain skeletons;
do not rebuild those skeletons over the supplied PDFs.

C.0 Get the files (once)
* With git: `git clone git@github.com:shreyanshsharma88/aci-02.git` (or the HTTPS URL), then `cd aci-02`.
* Without git: GitHub → Code → Download ZIP, then unzip it. (If the repo is private, the owner must add you
  first, or send you the folder.)

C.0b Set up Python (once). You need Python 3.9 or newer.
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
```powershell
# Windows (PowerShell)
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
Run every later command from the repository folder with the venv active (your prompt shows `(.venv)`).

C.1 to C.9, your steps
1. Open `q2/<your BITS ID>/answer.md` in any text editor (VS Code recommended). Read `q2/GUIDE.md` and
   `q2/EXAMPLE.md` first (about 15 min). The example is a toy library policy and is illustration only, so do not
   copy it. Skim `q2/KB_SYNTAX.md`.
2. B.1: fill in your name, ID, industry/domain, organisation type, and the instructor prompt if one was given
   (otherwise write `None given`). Do not change your ID.
3. B.2 Anchor: pick a real rule-governed process from your own workplace, or the industry equivalent if yours
   has none. Describe the context, who is involved, and why decisions follow rules (about 150–250 words).
4. B.3 Apply:
   - write at least 10 business rules in plain English (`BR1` … `BR10`)
   - define your propositions in the table, and write each rule in propositional logic (`PL1` … `PL10`)
   - define your predicates, variables and constants, and rewrite each rule in predicate logic with
     quantifiers (`FOL1` … `FOL10`)
   - write the ```` ```kb ```` block: at least 20 facts and at least 10 inference rules, in the `q2/KB_SYNTAX.md`
     format. Use invented names, not real colleagues' data.
   - write 5 workplace queries and, for each, the answer and the reasoning chain. Include at least one "no" answer
     and one query with a variable.
5. Run the checker. Fix everything it marks `[FAIL]` (missing counts, undefined predicates, queries that don't
   follow) and re-run until it ends with `RESULT: PASS`. `[WARN]` lines are advice, not blockers.
6. B.4 Analyse: explain how predicate logic is more expressive than propositional logic in your scenario, how
   effective your KB is, and what knowledge is missing or what limits it (about 200–300 words).
7. B.5 Reflect: describe the deployment constraints (incomplete knowledge, changing rules, privacy, scale,
   technology), then recommend and justify the single most important improvement (about 200–300 words).
8. Re-run the checker (it must still PASS), then build your PDF. This produces `q2/<ID>/<ID>.pdf`. Open it and
   proofread it: cover (name, ID, domain), all sections, the logic symbols, the tables.
9. Hand over before the agreed cut-off time. Either send `q2/<ID>/<ID>.pdf` to the submitter (WhatsApp, Drive,
   email between members is fine; only the final submission must go through the portal), or, if the repo is
   private, commit and push your work:
   ```bash
   git add q2/<ID>/answer.md q2/<ID>/<ID>.pdf
   git commit -m "Q2 <ID>"
   git pull --rebase && git push
   ```
   Then tell the submitter it's done, and confirm your name and ID on the cover.

**Ready-to-copy commands for the outstanding PDF** (venv active, from the repository folder):

SHREYANSH SHARMA (2025AG05772)
```bash
python q2/check_kb.py q2/2025AG05772/answer.md
python q2/build_pdf.py q2/2025AG05772/answer.md
```

### D. The submitter: build, verify, upload, about 15 minutes, once all 5 are in

1. Collect `q2/2025AG05772/2025AG05772.pdf`. The other four PDFs are already in their matching folders.
   Execute the notebook with `AUTO_DEMO = True` and resolve the remaining submission checks before packaging.
2. See who is still missing: `python q2/status.py`. Chase anyone not at "PDF built". A PDF a member sent you
   directly shows as "pending" here because their answer.md isn't in your copy; that is fine as long as the PDF is
   in place for step 3.
3. Build and verify the zip (Git Bash on Windows):
   ```bash
   GROUP=70 bash make_zip.sh
   ```
   If it says `REFUSING`, it lists exactly whose PDF is missing. Otherwise it builds
   `dist/<GroupNo>_ACI_Assignment2.zip` and runs `check_submission.py` on it. That must end with `RESULT: PASS`:
   exactly 6 files at the top level, each PDF's cover shows the right name and ID, B.2–B.5 have content, and the
   notebook has outputs. Re-check at any time with `python check_submission.py`.
4. Share the zip with all four other members. Each one opens it and confirms that their PDF is inside, is the
   right version, and shows their name and ID. The docx makes all members jointly responsible for this check.
5. Upload `dist/<GroupNo>_ACI_Assignment2.zip` through the assignment portal, before the deadline.
   Email submissions are not accepted. Upload one zip for the whole group; nobody else submits separately.
6. After uploading, download the file back from the portal (if it allows), or take a screenshot of the
   confirmation, and post it in the group chat.

### E. Final checklist (tick before uploading)

- [ ] Repository made private (A.1)
- [ ] Notebook executed, `AUTO_DEMO = True`, `python -m pytest -q` passes
- [ ] LAKSHYA KANCHAN: author confirms supplied PDF is final and proofread
- [ ] SHREYANSH SHARMA: checker PASS, `2025AG05772.pdf` built and proofread
- [ ] VINAY PRATAP SINGH BHADAURIA: author confirms content is accurate and final
- [ ] ABHISHEK GHOSH: author confirms supplied PDF is final and proofread
- [ ] SATHIYALATHASHRI N: author confirms supplied PDF is final and proofread
- [ ] `bash make_zip.sh` → `RESULT: PASS` (6 files)
- [ ] All 5 members confirmed the zip contents
- [ ] Uploaded through the portal before the deadline; confirmation shared

---

## 2. What the assignment asks

**Question 1: Gaming problem (group, 5 marks).** Simulate a small chess variant on the 3×3 board in the assignment
image, with Soldiers (pawns) and Horses (knights). A side wins when the opponent has lost every piece. Design and
justify a static evaluation function (no ML), explain it on a sample game state, and implement Minimax in
Python. One player is a human giving live input; the other is the program.
→ One notebook for the group: `Question1_Group.ipynb`.

**Question 2: Situated learning (individual, 5 marks).** Each member picks a rule-governed process from their own
workplace and represents it with propositional logic, predicate logic and a knowledge base: ≥10 rules in both
logics, ≥20 facts, ≥10 inference rules, 5 queries answered by reasoning. Then they analyse and reflect.
Rubric: Anchor (B.2) 1 · Apply (B.3) 2 · Analyse (B.4) 1 · Reflect (B.5) 1.
→ One PDF per member, named `<BITS_ID>.pdf`.

**Submission rules (from the assignment document)**
* One ZIP per group, with exactly 6 files at the top level: `Question1_Group.ipynb`, `2025AG05062.pdf`,
  `2025AG05772.pdf`, `2025AG05689.pdf`, `2025AG05076.pdf`, `2025AG05239.pdf`.
* Do not submit an incomplete ZIP. A member whose PDF is missing from the ZIP gets no Q2 marks, even if Q1 was
  submitted.
* Portal only; email submissions are not accepted. Late submissions follow course policy.
* All members are jointly responsible for verifying the ZIP before submission.

---

## 3. What has been done, and how

### Q1: implemented; execution still needs completion

* Code: `q1/game.py` is the single source. `q1/build_notebook.py` inlines it into `Question1_Group.ipynb`
   (self-contained; no imports from the repo). The latest submission check found four unexecuted code cells;
   rerun the notebook before packaging.
* Board: 3×3. White S a3 and H b3 (moves down); Black S b1 and H c1 (moves up). Human = White, moves first;
  computer = Black (`HUMAN_SIDE` to change).
* Evaluation function (White's view, White minus Black, hand-set weights, no ML):
  `E = material (S=10, H=30) + 1·mobility + 2·pawn advancement + 3·threats − 0.5·value of each attacked-and-undefended piece`.
  Terminal positions score ±(1000 − ply). Notebook worked example (White S a2, H a1; Black S c2, H b3; White to
  move): material 0, mobility −1, advancement 0, threats +3, safety −10, total −8. A 1-ply search then finds
  H a1xb3 (+13), which shows why the evaluation is used inside Minimax and not on its own.
* Search: plain Minimax is what the computer uses (default depth 8). Alpha-beta returns the same move with
  fewer nodes (depth 8 from the start: 2036 vs 125). White, moving first, has a forced win in 3 plies (H b3xc1).
* Human play: `input()` with validation (`b3 c1`, `b3c1`, `b3-c1`, `moves`, `quit`). `AUTO_DEMO = True` replays
  a scripted human game (the computer wins in 10 plies), so the notebook runs end to end. A second scripted game
  shows the human winning and the pass rule.
* Analysis: depth vs nodes and time (table and plot); full evaluation vs material-only, measured by how often a
  shallow search picks a game-theoretically best move.

### Q2: four PDFs present; one outstanding

Vinay's answer passes the checker and has a rebuilt, visually checked PDF. Lakshya, Abhishek and
Sathiyalathashri supplied PDFs directly; their local answer.md files are still skeletons.
Shreyansh's PDF is the only one not yet present.

| File | Purpose |
|---|---|
| `q2/<ID>/answer.md` | Skeleton per member: every B.1–B.5 heading, table and numbered slot (BR/PL/FOL 1–10, Fact 1–20, Inference rule 1–10, Query 1–5), with guidance in comments that never reach the PDF |
| `q2/<ID>/TODO.md` | That member's checklist with their ID in every command |
| `q2/GUIDE.md` | Rule → propositional → predicate logic; facts vs rules; queries; forward/backward chaining; modus ponens; common mistakes |
| `q2/EXAMPLE.md` | Illustration only (library book loans): 4 rules in both logics, KB, 2 queries with chains |
| `q2/KB_SYNTAX.md` | Syntax of the ```` ```kb ```` and ```` ```query ```` blocks (Horn clauses, `not`, comparisons, `false :-` constraints) |
| `q2/check_kb.py` | Checker. Sections filled and no `TODO` left; counts; one PL and one FOL per BR; undefined propositions and predicates; PL well-formed; quantifiers present; KB syntax; forward chaining (stratified negation, comparisons) with derivation traces; each query's expected answer verified; rules that never fire, unused facts, contradictions. Prints a PASS/FAIL checklist; exit code 1 on FAIL. |
| `q2/build_pdf.py` | Renders answer.md into `<ID>.pdf`: cover (course, name, BITS ID, domain, organisation type, instructor prompt), tables, logic symbols (DejaVu font), page footer. Refuses to build while the checker fails or the ID isn't one of ours. |
| `q2/status.py` | Each member's status from the files present |
| `q2/make_skeletons.py` | Re-creates missing skeletons and TODO files; never overwrites an answer.md |

### Packaging
* `make_zip.sh`: refuses (listing who is missing) unless the notebook and all 5 PDFs exist. Builds a flat zip, then
  runs the checker below.
* `check_submission.py`: checks for exactly the 6 required names at the top level; each PDF opens and its cover
  shows the matching name and BITS ID; B.2–B.5 have content; the notebook is executed with outputs and no errors.

### Audit (second pass): issues found and fixed
| Issue | Fix |
|---|---|
| A comparison or `not` written **before** the condition that binds its variable silently failed or derived wrong facts | Checker now evaluates comparisons and `not` once their variables are bound, in any order. Tested. |
| Query with a variable used only in a comparison returned a silent "no" | Now reported as an error |
| Repeated facts or rules could pad the ≥20 / ≥10 counts | Counted once |
| A stray `TODO` outside the numbered slots could reach the PDF | Any leftover `TODO` is a FAIL, with line numbers |
| `not p(X, _)` (anonymous variable) was rejected | Allowed, meaning "no p(X, anything)" |
| Several files read without UTF-8 (crash on Windows with ∀ →) | All reads and writes are UTF-8; console output can't crash |
| PDF section check could match "B.4" mentioned inside body text | Matches full headings ("B.4 Analyse") |
| `AUTO_DEMO` with `HUMAN_SIDE = "B"` crashed when the script ran out | Falls back to a legal move |
| Notebook had no group number | `GROUP=<n> python q1/build_notebook.py` adds it |
| Full-profile PASS path, and PDF → zip with full-profile PDFs, were never tested | Added end-to-end tests using a synthetic (abstract-symbol) answer |
| Repository is public | Manual step A.1 (needs the owner's GitHub login) |

---

## 4. How to run (reference)

```bash
# setup (once)
python3 -m venv .venv && source .venv/bin/activate     # Windows: py -m venv .venv ; .venv\Scripts\activate
pip install -r requirements.txt

# Q1: rebuild and execute the notebook
GROUP=<GroupNo> python q1/build_notebook.py
jupyter nbconvert --to notebook --execute --inplace Question1_Group.ipynb

# Q1: play interactively
jupyter notebook Question1_Group.ipynb      # Section 7: AUTO_DEMO = False, then Run All

# all tests (Q1, Q2 tooling, packaging)
python -m pytest -q

# Q2
python q2/check_kb.py q2/<ID>/answer.md
python q2/build_pdf.py q2/<ID>/answer.md                  # -> q2/<ID>/<ID>.pdf
python q2/check_kb.py q2/EXAMPLE.md --profile example     # example passes with the reduced profile
python q2/status.py

# packaging
GROUP=<GroupNo> bash make_zip.sh                          # -> dist/<GroupNo>_ACI_Assignment2.zip + verification
python check_submission.py [path/to.zip]
```

---

## 5. Status

Updated 2026-11-16 from local files and checks. `python q2/status.py` reports local source status;
for directly supplied PDFs, also check the PDF files themselves.

| Item | Status |
|---|---|
| Q1 notebook | Implemented; four code cells still need execution |
| Tests | 39 focused checker/PDF tests pass; broader submission checks hit incomplete notebook execution, missing WSL Bash and Windows symlink privileges |
| Q2 tooling, guide, example, skeletons | Done |
| LAKSHYA KANCHAN (2025AG05062) Q2 | Supplied PDF received; author sign-off remains |
| SHREYANSH SHARMA (2025AG05772) Q2 | pending: skeleton only |
| VINAY PRATAP SINGH BHADAURIA (2025AG05689) Q2 | Checker passes; PDF revised with explanatory prose, grouped facts and step-by-step query decisions; author sign-off remains |
| ABHISHEK GHOSH (2025AG05076) Q2 | Supplied PDF received; author sign-off remains |
| SATHIYALATHASHRI N (2025AG05239) Q2 | Supplied PDF received; author sign-off remains |
| Repository private | to do (A.1) |
| Group number | Done (70) |
| Final zip | not built: `make_zip.sh` refuses until all 5 PDFs exist |

---

## 6. Q1 rule interpretations and assumptions

| # | Rule | Interpretation (configurable flag in `q1/game.py`) | Why |
|---|---|---|---|
| D1 | Pawn straight | 1 step forward onto an **empty** square | "only one straight step ahead"; a straight step does not capture |
| D2 | Pawn diagonal | 1 step diagonally forward **only to capture** | "only if opponent coins are available … to attack" |
| D3 | Pawn extras | no double step, no en passant | "only one" step |
| D4 | Knight | full chess L: (±2,±1) and (±1,±2); `ALLOW_SIDEWAYS_L = True` | every L changes the rank, so each is "forward/backward"; standard chess knight. `False` keeps only (±2 ranks, ±1 file). |
| D5 | Knight jump | ignores pieces in between | "only piece that can jump" |
| D6 | Friendly squares | never land on your own piece | chess rule |
| D7 | Win | opponent has no pieces left | the docx's win condition |
| D8 | No legal move | `NO_MOVE_RULE = "pass"`; if neither side can move → draw (`"loss"` / `"draw"` available) | the docx defines only one way to win; pawns get stuck easily on 3×3 |
| D9 | Draws | `MAX_PLIES = 40`, threefold repetition | knights could shuffle forever |
| D10 | Promotion | none: a pawn on the last rank is frozen | not in the docx |
| D11 | King/check | none | no king on this board |

---

## 7. Troubleshooting

| Problem | Fix |
|---|---|
| `python3: command not found` (Windows) | Use `py` instead of `python3`; install Python 3.9+ from python.org and tick "Add to PATH" |
| PowerShell won't run `.venv\Scripts\activate` | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use `cmd` and `.venv\Scripts\activate.bat` |
| `ModuleNotFoundError` (reportlab, pypdf …) | The venv is not active, or `pip install -r requirements.txt` was not run |
| `bash: make_zip.sh` on Windows | Run it in **Git Bash** (comes with Git for Windows) |
| Checker: `predicate 'X' … not defined` | Add `X(...)` to the predicates table in B.3.4 (case and underscores are ignored) |
| Checker: `answer does NOT follow` | The KB disagrees with your `expect:`. Read the printed derivation, then fix a fact, a rule, or the expectation. |
| Checker: `never bound` | A variable appears only in `not …` or a comparison; add the positive condition that supplies it |
| Checker: `PLn is not a well-formed formula` | Write only the formula on the PL line, with balanced brackets and connectives between symbols |
| `build_pdf.py` says `REFUSING` | It lists the checker failures; fix them and run the checker until PASS |
| PDF shows boxes instead of symbols | Reinstall matplotlib (it ships the DejaVu fonts the builder uses) |
| `check_submission.py`: cover does not show the name | B.1 Name must match `q2/members.json` exactly (case ignored) |

---

## 8. Repository layout

```
Question1_Group.ipynb        Q1 deliverable (generated from q1/, executed)
q1/game.py                   engine, evaluation, minimax, alpha-beta, human play
q1/build_notebook.py         builds the notebook from game.py (GROUP env var for the header)
q2/GUIDE.md EXAMPLE.md KB_SYNTAX.md
q2/check_kb.py build_pdf.py status.py make_skeletons.py members.json templates/
q2/<BITS_ID>/answer.md TODO.md      one folder per member
tests/                       pytest suite
make_zip.sh check_submission.py
PLAN.md                      plan, docx audit, status
```
