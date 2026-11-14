"""Mini-chess on a 3x3 board (AIMLZG557 Assignment 2, Question 1).

This file is the single source of the game code. `q1/build_notebook.py` copies
each marked section (lines starting "# %%") into Question1_Group.ipynb, so the notebook stays
self-contained, and pytest tests exactly the code that is submitted.
"""

# %% [config]
from collections import Counter, namedtuple
import time

ROWS, COLS = 3, 3          # board from the assignment image
FILES = "abc"              # files a..c left to right; ranks 1..3 bottom to top

# Interpretation flags (see the rules table in the notebook)
ALLOW_SIDEWAYS_L = True    # knight may also move (1 rank, 2 files); False = only (2 ranks, 1 file)
NO_MOVE_RULE = "pass"      # side with no legal move: "pass" | "loss" | "draw"
MAX_PLIES = 40             # move cap -> draw
REPETITION_LIMIT = 3       # same position (board + side to move) seen 3 times -> draw

# Evaluation weights (hand-designed, no machine learning)
PIECE_VALUE = {"S": 10, "H": 30}
W_MOBILITY = 1
W_ADVANCE = 2
W_THREAT = 3
SAFETY_FRACTION = 0.5      # penalty = 50% of a hanging piece's value
WIN_SCORE = 1000

# %% [state]
# board: tuple of ROWS*COLS cells, index = row*COLS + col, row 0 = rank 3 (top).
# Each cell is None or a 2-char piece code: colour ('W'/'B') + kind ('S'/'H').
State = namedtuple("State", "board turn")


def other(color):
    return "B" if color == "W" else "W"


def sq_name(i):
    r, c = divmod(i, COLS)
    return f"{FILES[c]}{ROWS - r}"


def sq_index(name):
    name = name.strip().lower()
    if len(name) != 2 or name[0] not in FILES or not name[1].isdigit():
        raise ValueError(f"bad square '{name}'")
    c, rank = FILES.index(name[0]), int(name[1])
    if not 1 <= rank <= ROWS:
        raise ValueError(f"bad square '{name}'")
    return (ROWS - rank) * COLS + c


def make_state(pieces, turn="W"):
    """pieces: dict like {'a3': 'WS', 'b3': 'WH'}"""
    board = [None] * (ROWS * COLS)
    for sq, p in pieces.items():
        board[sq_index(sq)] = p
    return State(tuple(board), turn)


START = make_state({"a3": "WS", "b3": "WH", "b1": "BS", "c1": "BH"}, "W")


def forward(color):
    return 1 if color == "W" else -1    # White starts on top and moves down


def render(state):
    lines = ["     " + "    ".join(FILES)]
    for r in range(ROWS):
        cells = [state.board[r * COLS + c] or " . " for c in range(COLS)]
        cells = [x if x == " . " else f"{x[0]}-{x[1]}" for x in cells]
        lines.append(f"{ROWS - r} | " + "  ".join(cells) + " |")
    lines.append(f"to move: {'White' if state.turn == 'W' else 'Black'}")
    return "\n".join(lines)


# %% [moves]
def knight_deltas():
    d = [(2, 1), (2, -1), (-2, 1), (-2, -1)]
    if ALLOW_SIDEWAYS_L:
        d += [(1, 2), (1, -2), (-1, 2), (-1, -2)]
    return d


def on_board(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def piece_targets(board, i):
    """Legal destination squares for the piece on square i."""
    color, kind = board[i]
    r, c = divmod(i, COLS)
    out = []
    if kind == "S":
        r2 = r + forward(color)
        if on_board(r2, c) and board[r2 * COLS + c] is None:
            out.append(r2 * COLS + c)                     # straight step: empty only
        for dc in (-1, 1):
            if on_board(r2, c + dc):
                t = board[r2 * COLS + c + dc]
                if t is not None and t[0] != color:       # diagonal: capture only
                    out.append(r2 * COLS + c + dc)
    else:
        for dr, dc in knight_deltas():                     # jumps: squares between are ignored
            if on_board(r + dr, c + dc):
                t = board[(r + dr) * COLS + c + dc]
                if t is None or t[0] != color:
                    out.append((r + dr) * COLS + c + dc)
    return out


def attacked_squares(board, i):
    """Squares the piece on i could capture on, if an enemy stood there."""
    color, kind = board[i]
    r, c = divmod(i, COLS)
    if kind == "S":
        r2 = r + forward(color)
        return [r2 * COLS + c + dc for dc in (-1, 1) if on_board(r2, c + dc)]
    return [(r + dr) * COLS + c + dc for dr, dc in knight_deltas() if on_board(r + dr, c + dc)]


def pieces_of(board, color):
    return [i for i, p in enumerate(board) if p and p[0] == color]


def legal_moves(state):
    """List of (from, to) moves. Captures first (same order for every search)."""
    board, moves = state.board, []
    for i in pieces_of(board, state.turn):
        for j in piece_targets(board, i):
            moves.append((i, j))
    moves.sort(key=lambda m: (board[m[1]] is None, m))
    return moves


def apply_move(state, move):
    """move = (from, to) or None for a pass."""
    if move is None:
        return State(state.board, other(state.turn))
    i, j = move
    b = list(state.board)
    b[j], b[i] = b[i], None
    return State(tuple(b), other(state.turn))


def move_name(state, move):
    if move is None:
        return "pass"
    i, j = move
    cap = "x" if state.board[j] else "-"
    return f"{state.board[i][1]} {sq_name(i)}{cap}{sq_name(j)}"


def winner(state):
    """Colour that has eliminated every opposing piece, else None."""
    w, b = pieces_of(state.board, "W"), pieces_of(state.board, "B")
    if not b and w:
        return "W"
    if not w and b:
        return "B"
    return None


def game_result(state, ply, history):
    """'W' / 'B' / 'draw' if the game is over at this node, else None.
    ply = plies played so far; history = Counter of positions seen (incl. this one)."""
    w = winner(state)
    if w:
        return w
    if history.get(state, 0) >= REPETITION_LIMIT or ply >= MAX_PLIES:
        return "draw"
    if not legal_moves(state):
        if NO_MOVE_RULE == "loss":
            return other(state.turn)
        if NO_MOVE_RULE == "draw":
            return "draw"
        if not legal_moves(State(state.board, other(state.turn))):
            return "draw"                                   # pass rule: nobody can move
    return None


def search_moves(state):
    """Moves to search: legal moves, or [None] (a pass) when stuck under the pass rule."""
    return legal_moves(state) or [None]


# %% [evaluation]
def eval_terms(state):
    """Each evaluation term for White and Black. Positive total = good for White."""
    board = state.board
    terms = {}
    attacks = {col: Counter(sq for i in pieces_of(board, col) for sq in attacked_squares(board, i))
               for col in "WB"}
    for col in "WB":
        mine = pieces_of(board, col)
        enemy = other(col)
        material = sum(PIECE_VALUE[board[i][1]] for i in mine)
        mobility = W_MOBILITY * sum(len(piece_targets(board, i)) for i in mine)
        advance = 0
        for i in mine:
            if board[i][1] == "S":
                r = i // COLS
                advance += W_ADVANCE * (r if col == "W" else ROWS - 1 - r)
        threats = W_THREAT * sum(1 for j in pieces_of(board, enemy) if attacks[col][j])
        safety = -sum(SAFETY_FRACTION * PIECE_VALUE[board[i][1]]
                      for i in mine if attacks[enemy][i] and not attacks[col][i])
        terms[col] = {"material": material, "mobility": mobility, "advancement": advance,
                      "threats": threats, "safety": safety}
    return terms


def evaluate(state):
    t = eval_terms(state)
    return sum(t["W"].values()) - sum(t["B"].values())


def eval_table(state):
    t = eval_terms(state)
    rows = [(k, t["W"][k], t["B"][k], t["W"][k] - t["B"][k]) for k in t["W"]]
    total = sum(r[3] for r in rows)
    out = [f"{'term':<12}{'White':>8}{'Black':>8}{'W - B':>8}"]
    out += [f"{k:<12}{w:>8g}{b:>8g}{d:>8g}" for k, w, b, d in rows]
    out.append(f"{'TOTAL':<12}{'':>8}{'':>8}{total:>8g}")
    return "\n".join(out)


# %% [search]
class Stats:
    def __init__(self):
        self.nodes = 0


def _terminal_score(result, depth_from_root):
    if result == "draw":
        return 0
    s = WIN_SCORE - depth_from_root          # prefer faster wins, slower losses
    return s if result == "W" else -s


def minimax(state, depth, ply=0, history=None, stats=None, _d=0, eval_fn=None):
    """Plain Minimax. Returns (value, best_move); value is from White's view.
    White maximises, Black minimises."""
    history = Counter({state: 1}) if history is None else history
    stats = stats or Stats()
    stats.nodes += 1
    result = game_result(state, ply, history)
    if result:
        return _terminal_score(result, _d), None
    if depth == 0:
        return (eval_fn or evaluate)(state), None
    maximizing = state.turn == "W"
    best_val, best_move = (float("-inf") if maximizing else float("inf")), None
    for m in search_moves(state):
        child = apply_move(state, m)
        history[child] += 1
        val, _ = minimax(child, depth - 1, ply + 1, history, stats, _d + 1, eval_fn)
        history[child] -= 1
        if (maximizing and val > best_val) or (not maximizing and val < best_val):
            best_val, best_move = val, m
    return best_val, best_move


def alphabeta(state, depth, ply=0, history=None, stats=None, alpha=float("-inf"),
              beta=float("inf"), _d=0, eval_fn=None):
    """Minimax with alpha-beta pruning. Same value and move as minimax, fewer nodes."""
    history = Counter({state: 1}) if history is None else history
    stats = stats or Stats()
    stats.nodes += 1
    result = game_result(state, ply, history)
    if result:
        return _terminal_score(result, _d), None
    if depth == 0:
        return (eval_fn or evaluate)(state), None
    maximizing = state.turn == "W"
    best_val, best_move = (float("-inf") if maximizing else float("inf")), None
    for m in search_moves(state):
        child = apply_move(state, m)
        history[child] += 1
        val, _ = alphabeta(child, depth - 1, ply + 1, history, stats, alpha, beta, _d + 1,
                           eval_fn)
        history[child] -= 1
        if maximizing:
            if val > best_val:
                best_val, best_move = val, m
            alpha = max(alpha, val)
        else:
            if val < best_val:
                best_val, best_move = val, m
            beta = min(beta, val)
        if alpha >= beta:
            break
    return best_val, best_move


def choose_move(state, depth, ply=0, history=None, algorithm="minimax", eval_fn=None):
    stats = Stats()
    t0 = time.perf_counter()
    fn = minimax if algorithm == "minimax" else alphabeta
    val, move = fn(state, depth, ply, Counter(history or {state: 1}), stats, eval_fn=eval_fn)
    return move, val, stats.nodes, time.perf_counter() - t0


# %% [play]
def parse_move(text, state):
    """'b3 c1', 'b3c1' or 'b3-c1' -> legal (from, to). Raises ValueError with a reason."""
    t = text.strip().lower().replace("-", " ").replace("x", " ")
    parts = t.split() if " " in t else [t[:2], t[2:]]
    if len(parts) != 2:
        raise ValueError("type two squares, e.g. 'b3 c1'")
    i, j = sq_index(parts[0]), sq_index(parts[1])
    p = state.board[i]
    if p is None:
        raise ValueError(f"no piece on {parts[0]}")
    if p[0] != state.turn:
        raise ValueError(f"the piece on {parts[0]} is not yours")
    if (i, j) not in legal_moves(state):
        legal = ", ".join(sq_name(b) for a, b in legal_moves(state) if a == i) or "none"
        raise ValueError(f"illegal move; {p[1]} on {parts[0]} can go to: {legal}")
    return i, j


def play(human_side="W", depth=6, input_fn=input, algorithm="minimax", verbose=True):
    """Human vs computer. input_fn supplies the human's moves (input() when interactive).
    Returns (result, transcript)."""
    state, ply = START, 0
    history = Counter({state: 1})
    transcript = []
    say = print if verbose else (lambda *a, **k: None)
    say(render(state), "\n")
    while True:
        result = game_result(state, ply, history)
        if result:
            break
        moves = legal_moves(state)
        who = "Human" if state.turn == human_side else "Computer"
        if not moves:
            move, info = None, "no legal move -> pass"
        elif state.turn == human_side:
            while True:
                raw = input_fn(f"Your move ({'White' if human_side == 'W' else 'Black'}), "
                               "e.g. 'b3 c1' | 'moves' | 'quit': ")
                if raw.strip().lower() == "quit":
                    say("Game abandoned.")
                    return "abandoned", transcript
                if raw.strip().lower() == "moves":
                    say("Legal:", ", ".join(move_name(state, m) for m in moves))
                    continue
                try:
                    move = parse_move(raw, state)
                    break
                except ValueError as e:
                    say("  Invalid:", e)
            info = ""
        else:
            move, val, nodes, secs = choose_move(state, depth, ply, history, algorithm)
            info = f"eval={val:g}, nodes={nodes}, {secs * 1000:.1f} ms"
        name = move_name(state, move)
        state = apply_move(state, move)
        ply += 1
        history[state] += 1
        transcript.append({"ply": ply, "player": who, "move": name, "info": info,
                           "board": render(state)})
        say(f"Ply {ply}: {who} plays {name}" + (f"   [{info}]" if info else ""))
        say(render(state), "\n")
    msg = {"W": "White wins", "B": "Black wins", "draw": "Draw"}[result]
    say("RESULT:", msg)
    return result, transcript


# %% [analysis]
def material_only(state):
    """Baseline evaluation used for comparison: material difference only."""
    t = eval_terms(state)
    return t["W"]["material"] - t["B"]["material"]


def self_play(depth_w, depth_b, eval_w=None, eval_b=None, start=START, algorithm="alphabeta"):
    """Computer vs computer, used only for the analysis section. Returns (result, moves)."""
    state, ply, history, moves = start, 0, Counter({start: 1}), []
    while not game_result(state, ply, history):
        w = state.turn == "W"
        move, *_ = choose_move(state, depth_w if w else depth_b, ply, history, algorithm,
                               eval_w if w else eval_b)
        moves.append(move_name(state, move))
        state = apply_move(state, move)
        ply += 1
        history[state] += 1
    return game_result(state, ply, history), moves
