# PLAN — AIMLZG557 ACI Assignment 2 (Situated Learning, 10 marks)

Source of truth: `aci.docx` (read in full, board image `word/media/image1.png` inspected).

## 1. Assignment summary (from the docx)

### Submission rules
- Q1 (5 marks) is a **group** task: one Jupyter notebook per group (`Question1_Group.ipynb`).
- Q2 (5 marks) is **individual**: every member completes it independently, as a separate PDF named by BITS ID (`2025XXXXXX.pdf`).
- One ZIP per group with 1 IPYNB + one PDF per member. Our group has 5 members, so the zip holds **6 files**.
- No incomplete ZIP. A member whose PDF is missing gets **no Q2 marks**. Email submissions are not accepted. Upload via the portal on or before the deadline. All members are jointly responsible for checking the ZIP.

### Q1 requirements (docx wording)
1. "Simulate the working of chess with the below sample smaller game board."
2. Win: "A player with any piece/coin standing where its opponent sacrifices all the piece/coin is a win for the first player."
3. Soldier/Pawn (S): "only one straight step ahead. Only if opponent coins are available, it can move in diagonally one step forward to attack."
4. Horse/Knight (H): "either forward/backward in L-shaped strides covering exactly 3 tiles. It is the only piece that can jump over other coins."
5. Own static evaluation function, **justified**, **explained with a sample game state**, **no ML**.
6. One player is a **human with dynamic input**; the other is simulated by the program.
7. Python implementation using the **Minimax algorithm**.

### Q2 rubric (Section A.5) and tasks
| Component | Section | Marks | What it needs |
|---|---|---|---|
| Anchor | B.2 | 1.0 | Real rule-governed workplace process with enough context (or industry equivalent) |
| Apply | B.3 | 2.0 | ≥10 rules in propositional logic (propositions defined); same rules in predicate logic (predicates, variables, constants, quantifiers); KB with ≥20 facts and ≥10 inference rules; 5 workplace queries answered by reasoning |
| Analyse | B.4 | 1.0 | Predicate vs propositional expressiveness in the scenario; KB effectiveness; missing knowledge and limits |
| Reflect | B.5 | 1.0 | Deployment constraints (incomplete knowledge, changing rules, privacy, scale, technology); single most important improvement, justified |
B.1 is the submission form: Name, ID, Industry/Domain, Organisation Type, Instructor prompt.

### Deliverables checklist
- [ ] `Question1_Group.ipynb` with outputs
- [ ] `2025AG05062.pdf` LAKSHYA KANCHAN
- [ ] `2025AG05772.pdf` SHREYANSH SHARMA
- [ ] `2025AG05689.pdf` VINAY PRATAP SINGH BHADAURIA
- [ ] `2025AG05076.pdf` ABHISHEK GHOSH
- [ ] `2025AG05239.pdf` SATHIYALATHASHRI N
- [ ] one zip with exactly these 6 files at top level, uploaded through the portal

## 2. Q1 game analysis (from the board image)

Board: **3 columns × 3 rows** (checkered). Files `a b c` left→right, ranks `1 2 3` bottom→top.

| Square | Piece |
|---|---|
| a3 | White Soldier (S) |
| b3 | White Horse (H) |
| b1 | Black Soldier (S) |
| c1 | Black Horse (H) |
Every other square is empty (rank 2 is empty).

- White starts on rank 3 and moves **down** (toward rank 1). Black starts on rank 1 and moves **up**.
- Default: **Human = White, moves first** (chess convention: White moves first). **Computer = Black.** Both are configurable (`HUMAN_SIDE`).

### Interpretation decisions (each one a config flag)
| # | Decision | Choice | Justification |
|---|---|---|---|
| D1 | Pawn straight move | 1 step forward, onto an **empty** square only | "only one straight step ahead"; a straight move cannot capture, as in chess |
| D2 | Pawn diagonal | 1 step diagonally forward **only to capture** | "Only if opponent coins are available … diagonally … to attack" |
| D3 | Pawn double step / en passant | Not allowed | Docx says "only one" step |
| D4 | Knight geometry | The standard L: (±2 ranks, ±1 file) **and** (±1 rank, ±2 files). Flag `ALLOW_SIDEWAYS_L=True` | An L "covering exactly 3 tiles" is the chess knight's 2+1 stride. Every L has a non-zero rank change, so each one is "forward or backward". The phrase contrasts the knight with the pawn, which only goes forward. "Simulate the working of chess" favours the standard knight. Setting the flag to False keeps only the (±2 ranks, ±1 file) moves, the strict reading of "forward/backward". |
| D5 | Knight jumping | Ignores pieces in between; may land on an empty or enemy square | "only piece that can jump over other coins" |
| D6 | Friendly squares | No piece may move onto a friendly piece | Chess rule |
| D7 | Win | The side that removes all opposing pieces wins | Docx win condition |
| D8 | No legal move | `NO_MOVE_RULE="pass"` (default): the side passes. If **both** sides have no move, the game is a draw. Options: `"loss"`, `"draw"` | The docx defines only one way to win (opponent has no pieces). Treating "no move" as a loss would add a win condition the docx does not state. Pawns get stuck easily on a 3×3 board, so a pass keeps the game going while a knight can still move. |
| D9 | Draws | Move cap `MAX_PLIES=40` and **threefold repetition** → draw | Two knights can shuffle forever. This guarantees every game ends. |
| D10 | Promotion | **None**. A pawn on the last rank stays there and cannot move | The docx does not mention promotion |
| D11 | Check/king | None. There is no king | No king exists on the board |

## 3. Q1 notebook plan (`Question1_Group.ipynb`)
Code lives in `q1/game.py` (the single source, tested with pytest). `q1/build_notebook.py` inlines its sections into notebook cells, so the notebook is self-contained, then nbconvert executes it.

1. Problem statement and board: text board plus a matplotlib grid
2. Rules and interpretation table (D1–D11)
3. State: immutable `(board tuple of 9 cells, side_to_move)`. Cells hold `'WS','WH','BS','BH'` or `None`.
4. Move generation, with asserts on the start position's legal moves
5. Evaluation (from White's view, no ML):
   `E = Material + Mobility + Advancement + Threats + Safety` (White minus Black)
   - Material: S=10, H=30 (chess 1:3 ratio). This term dominates because removing all pieces is the goal.
   - Mobility: 1 per legal move. It rewards options and is weighted low so it cannot outweigh a piece.
   - Advancement: 2 per rank a pawn has advanced. This pushes pawns toward capture squares.
   - Threats: 3 per enemy piece attacked
   - Safety: −half the piece's value for each own piece that is attacked and not defended (a "hanging" piece)
   - Terminal: ±1000 ∓ ply (win sooner, lose later). Draw = 0.
   - Worked example: a fixed mid-game state, printing a term-by-term table and the total
6. `minimax(state, depth)` and `alphabeta(state, depth, α, β)`, with node counters and a node-count comparison
7. Human vs computer: `play(human_side, depth, input_fn)`. Uses `input()` with validation (format `b3 c1`, plus `moves`/`quit`). `AUTO_DEMO=True` replays a scripted human move list.
8. Full game transcript, with the board after every ply
9. Analysis: depth vs nodes and time for minimax and alpha-beta; the effect of the evaluation (full eval vs material-only)
10. Conclusion

Tests (`tests/test_game.py`): legality of each piece including edges, knight jump, pawn diagonal only on capture, no friendly landing, win detection, mate-in-1, evaluation symmetry under a colour mirror, alpha-beta move = minimax move, notebook code in sync with `game.py`.

## 4. Q2 preparation plan (Claude prepares only; members write all content)
- `q2/GUIDE.md`: business rule → propositional logic → predicate logic; facts vs inference rules; queries and reasoning chains (forward/backward chaining, modus ponens); common mistakes
- `q2/EXAMPLE.md`: **illustration only** (public library book loans): 4 rules in both logics, facts, rules, 2 queries with chains. Written in answer.md format, so the checker passes it with `--profile example`.
- `q2/KB_SYNTAX.md`: Datalog/Horn syntax in a ```` ```kb ```` block, queries in ```` ```query ```` blocks with `expect:`
- `q2/check_kb.py`: section completeness, counts, undefined propositions and predicates, propositional syntax, forward chaining with traces, query verification, rules that never fire, unused facts, contradictions (`false :- …` and `p`/`neg_p` pairs). PASS/FAIL checklist; exit code 1 on fail.
- `q2/build_pdf.py`: reportlab with DejaVu fonts (bundled with matplotlib) for ∀∃∧∨¬→↔. Cover block, tables, logic notation. Refuses to build if the checker fails.
- `q2/<ID>/answer.md` (skeleton, only name and ID filled) and `q2/<ID>/TODO.md` for all 5 members
- `q2/members.json`: the single list of name, ID and email, used by the tools
- Tests: `tests/test_check_kb.py` and `tests/test_build_pdf.py`

## 5. Packaging
- `make_zip.sh`: refuses and lists missing members if any PDF is absent. Builds `dist/<GROUP>_ACI_Assignment2.zip` (flat, 6 files), then runs `check_submission.py`.
- `check_submission.py`: exactly 6 named files at top level; each PDF opens (pypdf) and shows the matching name and ID with content in B.2–B.5; the notebook has outputs.
- `requirements.txt`: jupyter, nbconvert, matplotlib, pytest, reportlab, plus **pypdf**. A reader is needed because reportlab cannot read PDFs, and check_submission must verify the name and ID on each cover.

## 6. File layout
```
Question1_Group.ipynb       (generated + executed)
q1/game.py  q1/build_notebook.py
q2/GUIDE.md EXAMPLE.md KB_SYNTAX.md check_kb.py build_pdf.py members.json
q2/<ID>/answer.md TODO.md   (x5)
tests/test_game.py test_check_kb.py test_build_pdf.py test_submission.py
check_submission.py make_zip.sh README.md PLAN.md requirements.txt .gitignore
```

## 7. Timeline (due today)
1. Q1 engine + tests → notebook → execute (core first)
2. Q2 tooling + tests → guide/example/syntax → skeletons/TODOs
3. Packaging scripts → README → verify everything → git push
Manual tasks (humans): each member fills in answer.md, runs the checker, builds the PDF. The submitter zips, every member verifies, and the zip is uploaded via the portal.

## 8. Audit against the docx (line by line) — fixes
| Docx line | Gap found in first draft | Fix |
|---|---|---|
| "Implement Python code … using Minimax Algorithm" | Risk that alpha-beta is used in play and plain Minimax looks secondary | Computer player uses `minimax` by default (`ALGORITHM="minimax"`). Alpha-beta is an extra, proven to give the same move. |
| "explain with a sample game state" | Evaluation example could be a trivial start position | Use a non-trivial mid-game state with threats and a hanging piece; print each term |
| "must get dynamic inputs from us" | AUTO_DEMO might hide that the game is interactive | Separate interactive cell calling `input()` (guarded by `AUTO_DEMO`); README explains how to play |
| "Do not use any machine learning model" | — | Hand-set weights only; this is stated in the notebook |
| "PDF … named using the student's BITS ID" | Builder must name the file from the ID, not the folder | Builder reads the ID from B.1 and checks it matches `members.json` |
| "ZIP … containing the group assignment and all members' individual assignments" | Must not build a partial zip | make_zip.sh refuses when any PDF is missing |
| "Email submissions will NOT be accepted" | — | README submitter steps say portal only |
| B.1 "[Instructor prompt]" | Skeleton missing this field | Added to the B.1 table (write "None given" if none) |
| B.3 "clearly defining each proposition" | Checker needed to verify definitions | Undefined-symbol check for both logics |
| B.3 "Convert the **same** rules" | Counts alone don't prove a one-to-one mapping | Checker requires PLi and FOLi for every BRi |
| B.3 "five workplace queries" | Could be satisfied with ≥5 | Checker requires exactly 5 |
| A.3 "Support logical inference" | — | Forward chaining verifies each query |
| Example profile | A 4-rule example fails ≥10 counts | `--profile example` lowers minimums for EXAMPLE.md only |

## 9. Status (end of Phase 3, 2026-11-14)
| Item | State |
|---|---|
| Q1 engine + notebook | Done. `Question1_Group.ipynb` executed via nbconvert, no errors; AUTO_DEMO game ends with Black (computer) winning in 10 plies |
| Q1 tests | 22 pass (`tests/test_game.py`) |
| Q2 tooling | check_kb.py, build_pdf.py, status.py, make_skeletons.py; GUIDE, EXAMPLE, KB_SYNTAX; 5 skeletons + 5 TODOs |
| Q2 tooling tests | 21 checker + 4 builder tests pass |
| Packaging | check_submission.py + make_zip.sh; 7 tests pass. A real `make_zip.sh` run refuses (all 5 PDFs missing), as expected |
| EXAMPLE.md | `check_kb.py --profile example` → PASS; full profile → FAIL on counts only (by design) |
| Skeleton | `check_kb.py q2/2025AG05062/answer.md` → FAIL with 19 fill-in items |
| Members' Q2 | **pending** for all 5 (manual) |
| Group number | unknown: placeholder `<GROUP NO>` in README; pass `GROUP=...` to make_zip.sh |
| Git | pushed to origin/main (see the final message) |

Deviations from the brief: `pypdf` was added to requirements, because check_submission must read each cover and reportlab cannot read PDFs. `--profile example` exists so the 4-rule example can pass the checker.
