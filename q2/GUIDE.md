# Q2 guide: knowledge representation with propositional logic, predicate logic and a knowledge base

Read this, then `q2/EXAMPLE.md` (illustration only), then fill in your own `q2/<ID>/answer.md`.

## 0. Choose the process (B.2)

Pick one process from your own workplace where decisions follow written rules: an SOP, policy, regulation or
system configuration. Good candidates have:
* a clear decision (approve/reject, escalate, grant access, release, flag, ...)
* several conditions that combine (role, amount, status, dates, thresholds)
* many cases (employees, tickets, orders, patients, transactions), so predicate logic has something to quantify over

If your workplace has no such process, use the equivalent process common in your industry, and say so.

## 1. From business rule to propositional logic

1. Write the rule in plain English as condition(s) → consequence:
   *BR1: If an employee has completed probation and has enough leave balance, the leave request can be auto-approved.*
2. Give each atomic true/false statement a symbol, and define it in the propositions table:

   | Symbol | Meaning (true when ...) |
   |---|---|
   | C | the employee has completed probation |
   | B | the employee's leave balance covers the request |
   | A | the request can be auto-approved |

3. Join them with connectives:

   | Connective | Symbol (ASCII) | Use for |
   |---|---|---|
   | not | ¬ (`~`) | "is not", "has no" |
   | and | ∧ (`&`) | all conditions needed |
   | or | ∨ (`\|`) | any one condition is enough |
   | implies | → (`->`) | "if ... then ..." |
   | iff | ↔ (`<->`) | "exactly when" |

   PL1: C ∧ B → A

4. Each rule is an implication. Its left side is the antecedent (conditions) and its right side the
   consequent (decision). Use brackets when you mix ∧ and ∨: `(P ∨ Q) ∧ R → S`.

Limitation to note in B.4: a proposition is about *one* fixed case. "Alice has completed probation" and
"Bob has completed probation" need two different symbols. Numbers and comparisons ("balance ≥ requested days")
can only be frozen into one yes/no proposition.

## 2. Lift it into predicate logic (first-order logic)

| Element | What it is | Example |
|---|---|---|
| Predicate | a property or relation, with arguments | `CompletedProbation(e)`, `Balance(e, d)`, `ManagerOf(m, e)` |
| Variable | stands for any object of a type | `e` (employee), `d` (days), `m` (manager) |
| Constant | one specific object | `alice`, `finance`, `3` |
| ∀ (for all) | the rule applies to every object | `∀e (...)` |
| ∃ (there exists) | at least one object satisfies it | `∃t OpenTicket(e, t)` |

FOL1: ∀e ∀d ∀r (Employee(e) ∧ CompletedProbation(e) ∧ Balance(e, d) ∧ Requested(e, r) ∧ d ≥ r → AutoApprove(e))

Tips:
* Use `∀` for the general rule. Use `∃` when one example is enough ("has any overdue invoice").
* Same rule, both logics. PLn and FOLn must express BRn. The checker requires a PL and a FOL for every BR.
* Put every predicate in the predicates table, with its arguments: `Balance(e, d)`.
* Usual pattern: `∀x (Conditions(x) → Conclusion(x))`. Not `∀x (Conditions(x) ∧ Conclusion(x))`, which claims
  that everything satisfies the conditions.

## 3. Facts vs inference rules (the knowledge base)

| | Fact | Inference rule |
|---|---|---|
| What | a specific, known truth about your domain today | general knowledge: how new truths follow from others |
| Variables | none (ground) | yes |
| Example | `leave_balance(alice, 12).` | `sufficient(E) :- leave_balance(E, B), requested(E, D), ge(B, D).` |
| Comes from | records, HR system, tickets, inventory | the policy / business rules |

* Your inference rules are your FOL rules written in Horn-clause form (see `KB_SYNTAX.md`). You can add helper
  rules too (e.g. `senior(E) :- years_of_service(E, Y), ge(Y, 5).`).
* Your facts describe a realistic, made-up-but-plausible snapshot of your workplace. Use invented names, never
  real people's data (privacy). Include cases that are approved and cases that are rejected, so the KB is tested
  both ways.
* At least 20 facts and at least 10 inference rules. A rule that never fires, or a fact no rule uses, is a sign
  something is missing (the checker warns you).

## 4. Queries and reasoning chains

A query asks the KB a workplace question: *"Can Alice's 2-day leave be auto-approved?"* → `?- auto_approve(alice).`
With a variable it asks *"which ones?"*: `?- needs_manager(E, M).`

Show the reasoning chain using one of two methods:

* Forward chaining (data-driven): start from the facts, apply every rule whose conditions hold
  (modus ponens: from `P` and `P → Q`, conclude `Q`), add the new facts, and repeat until the goal appears or
  nothing changes.
* Backward chaining (goal-driven): start from the goal, find a rule that concludes it, and turn its conditions
  into sub-goals. A sub-goal is proved when it is a fact or can itself be proved by a rule.

Write the chain as numbered steps, each naming the facts and the rule used:

1. `employee(alice)`, `completed_probation(alice)` are facts.
2. `leave_balance(alice, 12)`, `requested(alice, 2)`, and 12 ≥ 2, so by inference rule 3: `sufficient(alice)`.
3. Steps 1–2 and inference rule 5 give `auto_approve(alice)`. Answer: yes.

For a "no" answer, explain which condition fails. The checker prints the derivation for every query; use it to
confirm your chain, but write the explanation in your own words.

Include variety in your five queries: at least one "no" answer, at least one query with a variable, and at least
one answer that needs two or more chained rules.

## 5. Common mistakes

1. Undefined symbols. A proposition or predicate used in a rule but missing from its table. (FAIL)
2. Different rules in the two logics. PL5 and FOL5 must both express BR5.
3. Propositions with arguments. `P(x)` is predicate logic. Propositional symbols are plain: `P1`, `Q`.
4. No quantifiers. Every FOL rule with variables needs `∀` / `∃`.
5. ∀ with ∧ instead of →. `∀x (Employee(x) ∧ Approved(x))` says *everyone* is an approved employee.
6. Variables in facts. `employee(X).` is not a fact. Facts are ground.
7. Uppercase constants in the KB. `Alice` is a *variable*; write `alice`.
8. Queries that don't follow. The expected answer must actually follow from your facts and rules. The checker
   catches this; fix the KB or the expectation, whichever is wrong.
9. Only "yes" cases. A KB that never rejects anything is not tested. Include facts that make some conditions fail.
10. Generic Anchor / Reflect. B.2, B.4 and B.5 are marked on your workplace. Name the process, roles, systems
    and constraints you actually see at work.
11. Real personal data. Use invented names and IDs in facts.
12. Leaving `TODO` anywhere. The checker treats any `TODO` as unfilled.
