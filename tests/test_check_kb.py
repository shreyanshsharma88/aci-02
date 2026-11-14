from pathlib import Path

import pytest

import check_kb as ck

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "q2" / "EXAMPLE.md"
SKELETON = ROOT / "q2" / "templates" / "answer_template.md"


def statuses(rep, needle):
    return [s for s, m in rep.items if needle in m]


def variant(tmp_path, old, new):
    text = EXAMPLE.read_text()
    assert old in text, old
    p = tmp_path / "answer.md"
    p.write_text(text.replace(old, new))
    return p


# ---------- parsing & counting ----------
def test_example_passes_with_example_profile():
    rep = ck.check(EXAMPLE, "example")
    assert rep.passed, rep.render()


def test_example_fails_full_profile_only_on_counts():
    rep = ck.check(EXAMPLE, "full")
    assert not rep.passed
    fails = rep.failures()
    assert all(any(k in f for k in ("4/10", "queries:")) for f in fails), fails


def test_counts_are_parsed():
    rep = ck.check(EXAMPLE, "example")
    msgs = " | ".join(m for _, m in rep.items)
    assert "business rules (plain English): 4/4" in msgs
    assert "KB facts: 23/6" in msgs
    assert "KB inference rules: 4/4" in msgs
    assert "propositions defined: 10" in msgs and "predicates defined: 14" in msgs


def test_b1_meta_is_read():
    rep = ck.check(EXAMPLE, "example")
    assert rep.meta["Name"] == "Illustration only" and rep.meta["ID No"] == "EXAMPLE"


def test_parse_kb_multiple_clauses_per_line_and_decimals():
    facts, rules, errors = ck.parse_kb("a(x). b(2.5).  % comment\nc(X) :- a(X), not d(X).\n")
    assert not errors
    assert [str(f) for f, _ in facts] == ["a(x)", "b(2.5)"]
    assert len(rules) == 1 and rules[0].number == 1


def test_parse_kb_errors():
    _, _, errors = ck.parse_kb("employee(X).\nfoo(X) :- not bar(X).\nunterminated(a)")
    assert len(errors) == 3
    assert "ground" in errors[0] and "positive" in errors[1] and "terminated" in errors[2]


def test_propositional_parser():
    assert ck.pl_parse("(P1 ∧ ¬P2) ∨ Q → R") == {"P1", "P2", "Q", "R"}
    assert ck.pl_parse("A & ~B -> C <-> D") == {"A", "B", "C", "D"}
    for bad in ("P ∧", "(P → Q", "P Q", ""):
        with pytest.raises(ValueError):
            ck.pl_parse(bad)


def test_fol_quantifier_not_mistaken_for_predicate():
    preds = ck.fol_predicates("∀b (Book(b) ∧ ∃m Holds(m, b) → Lent(b))")
    assert preds == [("Book", 1), ("Holds", 2), ("Lent", 1)]


# ---------- forward chaining ----------
def test_forward_chaining_derivations_and_negation():
    facts, rules, errors = ck.parse_kb(
        "p(a). p(b). q(b). n(1). n(5).\n"
        "r(X) :- p(X), not q(X).\n"
        "s(X) :- r(X).\n"
        "big(N) :- n(N), gt(N, 3).\n")
    kb = ck.KB(facts, rules).run()
    assert kb.model["r"] == {("a",)} and kb.model["s"] == {("a",)}
    assert kb.model["big"] == {(5,)}
    trace = "\n".join(kb.trace(ck.Atom("s", ("a",))))
    assert "inference rule 2" in trace and "inference rule 1" in trace and "[fact]" in trace


def test_unstratifiable_negation_is_reported():
    facts, rules, _ = ck.parse_kb("a(x).\np(X) :- a(X), not q(X).\nq(X) :- a(X), not p(X).\n")
    with pytest.raises(ValueError):
        ck.KB(facts, rules).run()


def test_query_that_does_not_follow_is_flagged(tmp_path):
    p = variant(tmp_path, "?- eligible(M).\nexpect: M = asha", "?- eligible(M).\nexpect: M = asha; M = ravi")
    rep = ck.check(p, "example")
    assert not rep.passed
    assert any("Query 2: answer does NOT follow" in f for f in rep.failures())


def test_wrong_yes_no_is_flagged(tmp_path):
    p = variant(tmp_path, "?- approved(asha, b101).\nexpect: yes", "?- approved(ravi, b101).\nexpect: yes")
    rep = ck.check(p, "example")
    assert any("Query 1: answer does NOT follow" in f for f in rep.failures())


def test_undefined_predicate_is_flagged(tmp_path):
    p = variant(tmp_path, "- **FOL3:** ∀m ∀b (Eligible(m)", "- **FOL3:** ∀m ∀b (Eligibl(m)")
    rep = ck.check(p, "example")
    assert any("predicate 'Eligibl' used in FOL3 but not defined" in f for f in rep.failures())


def test_undefined_kb_predicate_is_flagged(tmp_path):
    p = variant(tmp_path, "unpaid_fine(M) :- overdue(M, B).", "unpaid_fine(M) :- overdew(M, B).")
    rep = ck.check(p, "example")
    fails = " | ".join(rep.failures())
    assert "'overdew' is used in a rule body but is never a fact" in fails
    assert "'overdew/2' is not defined in the predicates table" in fails


def test_undefined_proposition_is_flagged(tmp_path):
    p = variant(tmp_path, "- **PL4:** O → F", "- **PL4:** O ∧ Z → F")
    rep = ck.check(p, "example")
    assert any("proposition 'Z' used in PL4" in f for f in rep.failures())


def test_contradiction_is_flagged(tmp_path):
    p = variant(tmp_path, "on_loan(b102).", "on_loan(b102). on_loan(b101).\napproved(asha, b101).")
    rep = ck.check(p, "example")
    assert any(f.startswith("contradiction") for f in rep.failures())


def test_neg_pair_contradiction(tmp_path):
    p = variant(tmp_path, "on_loan(b102).", "on_loan(b102). neg_on_loan(b102).")
    p.write_text(p.read_text().replace("| Overdue(m, b) |", "| NegOnLoan(b) | b is known not to be on loan |\n| Overdue(m, b) |"))
    rep = ck.check(p, "example")
    assert any("both on_loan(b102) and neg_on_loan(b102) hold" in f for f in rep.failures())


def test_rule_never_fires_and_unused_fact_warn(tmp_path):
    p = variant(tmp_path, "overdue(meena, b102).", "overdue(meena, b102). book_club(asha).")
    p.write_text(p.read_text().replace("approved(M, B) :- eligible(M), requests(M, B), available(B).",
                                       "approved(M, B) :- eligible(M), requests(M, B), available(B).\n"
                                       "vip(M) :- member(M), holds(M, N), gt(N, 50).")
                 .replace("| Overdue(m, b) |", "| BookClub(m) | m is in the book club |\n| Vip(m) | m is a VIP |\n| Overdue(m, b) |"))
    rep = ck.check(p, "example")
    warns = [m for s, m in rep.items if s == "WARN"]
    assert any("never fires" in w and "vip" in w for w in warns)
    assert any("never used" in w and "book_club(asha)" in w for w in warns)


def test_skeleton_fails_with_fill_in_list(tmp_path):
    p = tmp_path / "answer.md"
    p.write_text(SKELETON.read_text().replace("{NAME}", "TEST").replace("{ID}", "X1"))
    rep = ck.check(p, "full")
    fails = " | ".join(rep.failures())
    assert not rep.passed
    for needle in ("B.2 Anchor", "B.4 Analyse", "B.5 Reflect", "0/10", "KB facts: 0/20",
                   "Query 5: fill in"):
        assert needle in fails


def test_member_skeletons_exist_and_fail():
    for d in (ROOT / "q2").glob("2025AG*"):
        rep = ck.check(d / "answer.md")
        assert rep.meta["ID No"] == d.name
        if "TODO" in (d / "answer.md").read_text():
            assert not rep.passed


def test_cli_exit_codes():
    assert ck.main([str(EXAMPLE), "--profile", "example"]) == 0
    assert ck.main([str(EXAMPLE)]) == 1


# ---------- audit fixes ----------
from conftest import synthetic_answer  # noqa: E402


def test_full_profile_passes_for_complete_answer(tmp_path):
    p = tmp_path / "answer.md"
    p.write_text(synthetic_answer("Test Person", "T001"), encoding="utf-8")
    rep = ck.check(p, "full")
    assert rep.passed, rep.render()
    assert not [m for s, m in rep.items if s == "WARN" and "words" in m]


def test_comparison_written_before_binder():
    facts, rules, errors = ck.parse_kb("bal(a, 5). req(a, 3). bal(b, 1). req(b, 3).\n"
                                       "ok(E) :- ge(B, D), bal(E, B), req(E, D).")
    assert not errors
    assert ck.KB(facts, rules).run().model["ok"] == {("a",)}


def test_negation_written_before_binder():
    facts, rules, _ = ck.parse_kb("p(a). p(b). q(a).\nr(X) :- not q(X), p(X).")
    assert ck.KB(facts, rules).run().model["r"] == {("b",)}


def test_negation_with_anonymous_variable():
    facts, rules, _ = ck.parse_kb("e(a). e(b). owns(a, car).\nwalker(X) :- e(X), not owns(X, _).")
    assert ck.KB(facts, rules).run().model["walker"] == {("b",)}


def test_unbound_query_variable_is_reported(tmp_path):
    p = variant(tmp_path, "?- eligible(M).\nexpect: M = asha", "?- gt(M, 3).\nexpect: none")
    rep = ck.check(p, "example")
    assert any("never bound" in f for f in rep.failures())


def test_duplicate_facts_count_once(tmp_path):
    text = synthetic_answer("Test Person", "T001")
    text = text.replace("\n".join(f"a1(o{k})." for k in range(11, 21)), "a1(o1).\n" * 10)
    p = tmp_path / "answer.md"
    p.write_text(text, encoding="utf-8")
    rep = ck.check(p, "full")
    assert any("KB facts: 10/20" in f for f in rep.failures())


def test_leftover_todo_is_flagged(tmp_path):
    p = tmp_path / "answer.md"
    p.write_text(synthetic_answer("Test Person", "T001").replace("| o1, o2 | objects |",
                                                                  "| o1, o2 | objects |\n| TODO | TODO |"),
                 encoding="utf-8")
    rep = ck.check(p, "full")
    assert any("'TODO' still appears" in f for f in rep.failures())
