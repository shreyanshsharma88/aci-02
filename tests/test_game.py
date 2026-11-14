import json
import random
from collections import Counter
from pathlib import Path

import pytest

import game as g

ROOT = Path(__file__).resolve().parents[1]


def names(state):
    return sorted(g.move_name(state, m) for m in g.legal_moves(state))


def targets(state, sq):
    return sorted(g.sq_name(j) for j in g.piece_targets(state.board, g.sq_index(sq)))


# ---------- start position ----------
def test_start_position_matches_image():
    b = g.START.board
    assert b[g.sq_index("a3")] == "WS" and b[g.sq_index("b3")] == "WH"
    assert b[g.sq_index("b1")] == "BS" and b[g.sq_index("c1")] == "BH"
    assert sum(p is not None for p in b) == 4
    assert g.START.turn == "W"


def test_start_legal_moves():
    assert names(g.START) == ["H b3-a1", "H b3xc1", "S a3-a2"]
    black = g.State(g.START.board, "B")
    assert names(black) == ["H c1-a2", "H c1xb3", "S b1-b2"]


# ---------- pawn ----------
def test_pawn_straight_only_onto_empty():
    s = g.make_state({"b3": "WS", "b2": "BS"})
    assert targets(s, "b3") == []                      # blocked, cannot capture straight
    s = g.make_state({"b2": "BS", "a1": "WH"}, "B")
    assert targets(s, "b2") == ["b3"]


def test_pawn_diagonal_only_when_capturing():
    s = g.make_state({"b3": "WS", "a2": "BH", "c2": "BS"})
    assert targets(s, "b3") == ["a2", "b2", "c2"]
    s = g.make_state({"b3": "WS", "a2": None, "c1": "BS"})
    assert targets(s, "b3") == ["b2"]                  # no enemy on diagonal -> no diagonal move
    s = g.make_state({"b3": "WS", "a2": "WH", "c2": "BS"})
    assert targets(s, "b3") == ["b2", "c2"]            # never captures a friend


def test_pawn_edges_and_last_rank():
    s = g.make_state({"a3": "WS", "b2": "BS"})
    assert targets(s, "a3") == ["a2", "b2"]            # a-file: only one diagonal exists
    s = g.make_state({"c1": "WS", "b2": "BS"})
    assert targets(s, "c1") == []                      # White pawn on last rank: stuck, no promotion
    s = g.make_state({"a3": "BS", "b2": "WS"}, "B")
    assert targets(s, "a3") == []


def test_black_pawn_moves_up():
    s = g.make_state({"b1": "BS", "a2": "WS", "c2": "WH"}, "B")
    assert targets(s, "b1") == ["a2", "b2", "c2"]


# ---------- knight ----------
def test_knight_moves_from_corner_and_centre():
    s = g.make_state({"a1": "WH"})
    assert targets(s, "a1") == ["b3", "c2"]
    s = g.make_state({"b2": "WH"})
    assert targets(s, "b2") == []                      # centre of 3x3: every L leaves the board


def test_knight_without_sideways_l(monkeypatch):
    monkeypatch.setattr(g, "ALLOW_SIDEWAYS_L", False)
    s = g.make_state({"a1": "WH"})
    assert targets(s, "a1") == ["b3"]


def test_knight_jumps_over_pieces():
    s = g.make_state({"a1": "WH", "a2": "WS", "b2": "BS", "b1": "BS"})
    assert "b3" in targets(s, "a1") and "c2" in targets(s, "a1")


def test_no_move_onto_friendly_piece():
    s = g.make_state({"a1": "WH", "b3": "WS", "c2": "WS"})
    assert targets(s, "a1") == []
    s = g.make_state({"a1": "WH", "b3": "BS", "c2": "WS"})
    assert targets(s, "a1") == ["b3"]


# ---------- game end ----------
def test_win_detection():
    assert g.winner(g.make_state({"a1": "WH"})) == "W"
    assert g.winner(g.make_state({"a1": "BS"})) == "B"
    assert g.winner(g.START) is None
    s = g.apply_move(g.make_state({"b3": "WH", "c1": "BH"}), (g.sq_index("b3"), g.sq_index("c1")))
    assert g.game_result(s, 1, Counter({s: 1})) == "W"


def test_pass_and_dead_position():
    # White pawn stuck on last rank, Black knight can still move -> White passes, game goes on
    s = g.make_state({"c1": "WS", "a3": "BH"}, "W")
    assert g.legal_moves(s) == [] and g.search_moves(s) == [None]
    assert g.game_result(s, 0, Counter({s: 1})) is None
    # nobody can move -> draw
    s = g.make_state({"c1": "WS", "a3": "BS"}, "W")
    assert g.game_result(s, 0, Counter({s: 1})) == "draw"


def test_no_move_rule_loss(monkeypatch):
    monkeypatch.setattr(g, "NO_MOVE_RULE", "loss")
    s = g.make_state({"c1": "WS", "a3": "BH"}, "W")
    assert g.game_result(s, 0, Counter({s: 1})) == "B"


def test_repetition_and_move_cap():
    s = g.START
    assert g.game_result(s, 0, Counter({s: 3})) == "draw"
    assert g.game_result(s, g.MAX_PLIES, Counter({s: 1})) == "draw"


# ---------- search & evaluation ----------
def test_minimax_finds_mate_in_one():
    # White to move; capturing the last black piece wins immediately
    s = g.make_state({"a3": "WS", "b3": "WH", "b2": "BS"}, "W")
    for algo in ("minimax", "alphabeta"):
        move, val, _, _ = g.choose_move(s, 3, algorithm=algo)
        assert g.move_name(s, move) == "S a3xb2"
        assert val == g.WIN_SCORE - 1


def test_black_finds_mate_in_one():
    s = g.make_state({"c2": "WH", "b1": "BS", "a2": "BH"}, "B")
    move, val, _, _ = g.choose_move(s, 4)
    assert g.move_name(s, move) == "S b1xc2" and val == -(g.WIN_SCORE - 1)


def mirror(state):
    """Flip ranks and swap colours: the position seen from the other side."""
    b = [None] * 9
    for i, p in enumerate(state.board):
        if p:
            r, c = divmod(i, 3)
            b[(2 - r) * 3 + c] = g.other(p[0]) + p[1]
    return g.State(tuple(b), g.other(state.turn))


def random_states(n, seed=1):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        s = g.START
        for _ in range(rng.randint(0, 8)):
            if g.winner(s):
                break
            s = g.apply_move(s, rng.choice(g.search_moves(s)))
        out.append(s)
    return out


def test_evaluation_symmetry():
    assert g.evaluate(g.START) == 0
    for s in random_states(200):
        assert g.evaluate(mirror(s)) == -g.evaluate(s)


def test_alphabeta_matches_minimax():
    for s in random_states(60, seed=7):
        if g.game_result(s, 0, Counter({s: 1})):
            continue
        for depth in (1, 2, 3, 4, 5):
            m1, v1, n1, _ = g.choose_move(s, depth, algorithm="minimax")
            m2, v2, n2, _ = g.choose_move(s, depth, algorithm="alphabeta")
            assert (m1, v1) == (m2, v2)
            assert n2 <= n1


def test_parse_move_validation():
    assert g.parse_move("b3 c1", g.START) == (g.sq_index("b3"), g.sq_index("c1"))
    assert g.parse_move("A3-A2", g.START) == (g.sq_index("a3"), g.sq_index("a2"))
    for bad in ["b3 b2", "c3 c2", "b1 b2", "z9 a1", "hello"]:
        with pytest.raises(ValueError):
            g.parse_move(bad, g.START)


def test_scripted_game_runs_to_completion():
    script = iter(["xx", "b3 a1", "a1 b3", "a3 a2", "b3 a1", "a1 c2"])
    result, transcript = g.play("W", depth=8, input_fn=lambda _: next(script), verbose=False)
    assert result == "B" and len(transcript) == 10


# ---------- notebook ----------
def test_notebook_inlines_current_game_code():
    nb = json.loads((ROOT / "Question1_Group.ipynb").read_text())
    code = "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")
    src = (ROOT / "q1" / "game.py").read_text()
    chunks = [c.split("\n", 1)[1].strip() for c in src.split("# %% [")[1:]]
    for chunk in chunks:
        assert chunk in code
    assert "import game" not in code                    # self-contained


def test_notebook_has_outputs_without_errors():
    nb = json.loads((ROOT / "Question1_Group.ipynb").read_text())
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    assert all(c.get("execution_count") for c in code_cells)
    assert not any(o.get("output_type") == "error" for c in code_cells for o in c["outputs"])


def test_human_as_black_with_exhausted_script_does_not_crash():
    script = iter(["b1 b2"])                     # one move, then the script runs out
    result, transcript = g.play("B", depth=4, input_fn=lambda _: next(script, None), verbose=False)
    assert result in ("W", "B", "draw") and transcript
