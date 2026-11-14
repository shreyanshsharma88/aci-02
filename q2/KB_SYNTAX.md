# KB syntax (machine-checkable)

`q2/check_kb.py` reads two kinds of fenced block in your `answer.md`: one ```` ```kb ```` block (B.3.6) and one
```` ```query ```` block per query (B.3.7). The syntax is a small subset of Prolog/Datalog: facts and Horn-clause
rules with variables, evaluated by **forward chaining**.

## Terms

| Kind | Written as | Examples |
|---|---|---|
| Constant | starts lowercase, or a number, or quoted | `alice`, `hr_dept`, `12`, `4.5`, `'Ward 3B'` |
| Variable | starts **Uppercase** or `_` | `X`, `Emp`, `Days`, `_` (anonymous) |

## Facts: ground atoms ending in `.`

```kb
employee(alice).
department(alice, finance).
leave_balance(alice, 12).
manager_of(bob, alice).
on_probation(carol).
```

* The predicate name starts lowercase: `name(arg1, arg2, ...)`. A predicate with no arguments is written bare: `system_online.`
* Facts contain no variables.
* Several clauses may share a line. `%` starts a comment to the end of the line.

## Inference rules: `head :- condition1, condition2, ... .`

```kb
can_apply_leave(E) :- employee(E), not on_probation(E).
sufficient_balance(E) :- leave_balance(E, B), requested_days(E, D), ge(B, D).
auto_approve(E) :- can_apply_leave(E), sufficient_balance(E), requested_days(E, D), le(D, 3).
needs_manager(E, M) :- requested_days(E, D), gt(D, 3), manager_of(M, E).
```

* The comma means **AND**. For **OR**, write two rules with the same head.
* The head is one positive atom (Horn clause). Every variable in the head must appear in a positive body condition.
* `not p(...)` is **negation as failure** (closed-world assumption): it is true when `p(...)` cannot be derived.
  Each of its variables must also appear in a positive condition of the same rule (in any position). `_` means
  "anything": `not owns(X, _)` = X owns nothing. Do not make `p` depend on `not p`.
* Comparison built-ins: `lt(X,Y)` <, `le(X,Y)` ≤, `gt(X,Y)` >, `ge(X,Y)` ≥, `eq(X,Y)` =, `neq(X,Y)` ≠. Their variables
  must also appear in a positive condition. The checker evaluates comparisons and `not` after the variables are
  bound, so the order you write the conditions in does not matter.

## Optional consistency constraints

```kb
false :- approved(E), rejected(E).
```

If the body of a `false` rule can be satisfied, the checker reports a **contradiction**. The checker also flags a
contradiction if both `p(...)` and `neg_p(...)` hold. Constraints do not count towards the 10 inference rules.

## Counting

* **Facts** = distinct ground clauses in the kb block (at least 20; a repeated fact counts once).
* **Inference rules** = distinct clauses with `:-` whose head is not `false` (at least 10).

## Queries (one block per query in B.3.7)

```query
?- auto_approve(alice).
expect: yes
```

```query
?- needs_manager(E, M).
expect: E = dave, M = bob; E = erin, M = bob
```

* `?-` is followed by one or more conditions, separated by commas (the same syntax as a rule body).
* `expect:` is `yes` or `no` for a query without variables. With variables, list **all** expected answers as
  `Var = value`, separated by `;`, or write `none`.
* The checker runs the KB and reports PASS only if the KB gives exactly your expected answer. It also prints the
  derivation (which rule, which facts), which you can use for your **Reasoning chain**.

## Linking the KB to your predicate table

Every predicate in the kb block must appear in the predicates table (B.3.4). Names are matched ignoring case and
underscores: `leave_balance/2` matches `LeaveBalance(e, d)`. Comparison built-ins don't need a table row.

## What the checker reports

| Check | Level |
|---|---|
| B.1–B.5 present and filled; no `TODO` left anywhere | FAIL |
| ≥10 BR, ≥10 PL, ≥10 FOL, with a PL and a FOL for every BR | FAIL |
| ≥20 facts, ≥10 inference rules, exactly 5 complete queries | FAIL |
| proposition in PL not in the propositions table; predicate in FOL/KB not in the predicates table | FAIL |
| PL formula not well-formed; no quantifier in any FOL rule | FAIL |
| KB syntax error; body predicate that is never a fact or head | FAIL |
| query answer does not follow from the KB; query variable used only in a comparison/`not` | FAIL |
| contradiction (`false :-` satisfied, or `p` and `neg_p` both hold) | FAIL |
| inference rule never fires; fact never read by a rule or query; arity mismatch; word count outside the guide | WARN |
