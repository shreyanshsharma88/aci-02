import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "q1"), str(ROOT / "q2"), str(ROOT)]


def synthetic_answer(name, sid, n=10):
    """A mechanically generated answer.md that meets every FULL-profile minimum.
    Abstract symbols only (P1, A1(x), a1(o1) ...): test data, not a model answer."""
    filler = lambda k: " ".join(f"synthetic{i}" for i in range(k))
    br = "\n".join(f"- **BR{k}:** If condition {k} holds then condition {k + 1} holds." for k in range(1, n + 1))
    props = "\n".join(f"| P{k} | condition {k} holds |" for k in range(1, n + 2))
    pl = "\n".join(f"- **PL{k}:** P{k} → P{k + 1}" for k in range(1, n + 1))
    preds = "\n".join(f"| A{k}(x) | x satisfies condition {k} |" for k in range(1, n + 2))
    fol = "\n".join(f"- **FOL{k}:** ∀x (A{k}(x) → A{k + 1}(x))" for k in range(1, n + 1))
    facts = "\n".join(f"a1(o{k})." for k in range(1, 21))
    rules = "\n".join(f"a{k + 1}(X) :- a{k}(X)." for k in range(1, n + 1))
    queries = ""
    for q, (goal, exp) in enumerate([("a11(o1)", "yes"), ("a5(o20)", "yes"), ("a2(o21)", "no"),
                                     ("a11(o3)", "yes"), ("a3(o7)", "yes")], 1):
        queries += (f"#### Query {q}\n\n- **Question:** Does {goal} hold?\n\n```query\n?- {goal}.\n"
                    f"expect: {exp}\n```\n\n- **Answer:** {exp}.\n- **Reasoning chain:** chained rules.\n\n")
    return f"""# Q2

## B.1 Submission Form

| Field | Value |
|---|---|
| Name | {name} |
| ID No | {sid} |
| Industry / Domain | Synthetic |
| Organisation Type | Synthetic |
| Instructor prompt | None given |

## B.2 Anchor

{filler(180)}

## B.3 Apply

### B.3.1 Business rules
{br}

### B.3.2 Propositions

| Symbol | Meaning |
|---|---|
{props}

### B.3.3 PL
{pl}

### B.3.4 Predicates

| Predicate | Meaning |
|---|---|
{preds}

| Variable | Ranges over |
|---|---|
| x | objects |

| Constant | Denotes |
|---|---|
| o1, o2 | objects |

### B.3.5 FOL
{fol}

### B.3.6 KB

```kb
{facts}
{rules}
```

### B.3.7 Queries

{queries}
## B.4 Analyse

{filler(230)}

## B.5 Reflect

{filler(230)}
"""
