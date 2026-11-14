# Question 2 – Situated Learning: Knowledge Representation

<!--
HOW TO USE THIS FILE
- Read q2/GUIDE.md and q2/EXAMPLE.md first (about 15 minutes).
- Replace every "TODO" with your own content. Use your own workplace (or the industry equivalent).
- Text inside these comment markers is guidance. It is removed from the PDF, so you may leave it or delete it.
- Keep the headings, the labels (BR1, PL1, FOL1, Query 1 ...) and the ```kb / ```query fences exactly as they are:
  the checker and the PDF builder look for them.
- Check:  python q2/check_kb.py q2/2025AG05772/answer.md
- Build:  python q2/build_pdf.py q2/2025AG05772/answer.md
-->

## B.1 Submission Form

| Field | Value |
|---|---|
| Name | SHREYANSH SHARMA |
| ID No | 2025AG05772 |
| Industry / Domain | TODO |
| Organisation Type | TODO |
| Instructor prompt | TODO |

<!-- Industry / Domain: e.g. banking, healthcare, IT services, manufacturing ...
     Organisation Type: e.g. private MNC, public sector, start-up, hospital, government agency ...
     Instructor prompt: write the prompt if one was given; otherwise write "None given". -->

## B.2 Anchor

<!-- About 150-250 words. Rubric (1 mark): "Clearly identifies a relevant workplace artifact with sufficient context".
     Name ONE real process from YOUR workplace where decisions follow predefined rules or policies
     (e.g. leave approval, access control, loan approval, incident escalation, QA release sign-off ...).
     If your workplace has none, choose the equivalent process commonly followed in your industry, and say so.
     Cover: what the process is, who is involved (roles), what decision it produces, where the rules come
     from (policy document, SOP, regulation), and why the decisions are rule-based. -->

TODO

## B.3 Apply

<!-- Rubric (2 marks): the core concept (propositional logic, predicate logic, knowledge base) correctly applied
     to your workplace artifact. -->

### B.3.1 Business rules (plain English)

<!-- At least 10. One rule per line, each a condition and a consequence ("If ... then ..."). Add BR11, BR12 ... if you want. -->

- **BR1:** TODO
- **BR2:** TODO
- **BR3:** TODO
- **BR4:** TODO
- **BR5:** TODO
- **BR6:** TODO
- **BR7:** TODO
- **BR8:** TODO
- **BR9:** TODO
- **BR10:** TODO

### B.3.2 Propositions

<!-- Define EVERY symbol you use in B.3.3. A proposition is a statement that is simply true or false
     (e.g. "P1 | The employee has submitted a leave request"). Add rows as needed. -->

| Symbol | Meaning (true when ...) |
|---|---|
| TODO | TODO |

### B.3.3 Rules in propositional logic

<!-- PLn is the propositional form of BRn. Write ONLY the formula on the line.
     Connectives: ¬ (not), ∧ (and), ∨ (or), → (implies), ↔ (iff); ASCII ~ & | -> <-> also work. Use brackets.
     Example format:  - **PL1:** P1 ∧ P2 ∧ ¬P3 → P4 -->

- **PL1:** TODO
- **PL2:** TODO
- **PL3:** TODO
- **PL4:** TODO
- **PL5:** TODO
- **PL6:** TODO
- **PL7:** TODO
- **PL8:** TODO
- **PL9:** TODO
- **PL10:** TODO

### B.3.4 Predicates, variables and constants

<!-- Predicates take arguments, e.g. Employee(x), LeaveBalance(x, d). Every predicate used in B.3.5 AND in the
     KB block must be in this table (names are matched ignoring case and underscores, so LeaveBalance = leave_balance). -->

| Predicate | Meaning |
|---|---|
| TODO | TODO |

| Variable | Ranges over |
|---|---|
| TODO | TODO |

| Constant | Denotes |
|---|---|
| TODO | TODO |

### B.3.5 Rules in predicate logic

<!-- FOLn is the predicate-logic form of the SAME rule BRn, with quantifiers.
     Example format:  - **FOL1:** ∀x ∀d (Employee(x) ∧ Balance(x, d) ∧ d ≥ 1 → CanApply(x)) -->

- **FOL1:** TODO
- **FOL2:** TODO
- **FOL3:** TODO
- **FOL4:** TODO
- **FOL5:** TODO
- **FOL6:** TODO
- **FOL7:** TODO
- **FOL8:** TODO
- **FOL9:** TODO
- **FOL10:** TODO

### B.3.6 Knowledge base

<!-- At least 20 facts and at least 10 inference rules, in the syntax of q2/KB_SYNTAX.md.
     Write each clause on the line after its "% Fact n" / "% Inference rule n" comment. Add more lines as needed.
     The checker runs this block with forward chaining. -->

```kb
% ---------- Facts (at least 20) ----------
% Fact 1:
% Fact 2:
% Fact 3:
% Fact 4:
% Fact 5:
% Fact 6:
% Fact 7:
% Fact 8:
% Fact 9:
% Fact 10:
% Fact 11:
% Fact 12:
% Fact 13:
% Fact 14:
% Fact 15:
% Fact 16:
% Fact 17:
% Fact 18:
% Fact 19:
% Fact 20:

% ---------- Inference rules (at least 10) ----------
% Inference rule 1:
% Inference rule 2:
% Inference rule 3:
% Inference rule 4:
% Inference rule 5:
% Inference rule 6:
% Inference rule 7:
% Inference rule 8:
% Inference rule 9:
% Inference rule 10:

% ---------- Optional consistency constraints ----------
% false :- approved(X), rejected(X).
```

### B.3.7 Workplace queries

<!-- Exactly 5 queries. For each: the question in plain English, the formal query and expected answer
     (the checker verifies it), the answer, and the reasoning chain (which facts and rules, in which order,
     by forward or backward chaining with modus ponens). See EXAMPLE.md. -->

#### Query 1

- **Question:** TODO

```query
?- TODO
expect: TODO
```

- **Answer:** TODO
- **Reasoning chain:** TODO

#### Query 2

- **Question:** TODO

```query
?- TODO
expect: TODO
```

- **Answer:** TODO
- **Reasoning chain:** TODO

#### Query 3

- **Question:** TODO

```query
?- TODO
expect: TODO
```

- **Answer:** TODO
- **Reasoning chain:** TODO

#### Query 4

- **Question:** TODO

```query
?- TODO
expect: TODO
```

- **Answer:** TODO
- **Reasoning chain:** TODO

#### Query 5

- **Question:** TODO

```query
?- TODO
expect: TODO
```

- **Answer:** TODO
- **Reasoning chain:** TODO

## B.4 Analyse

<!-- About 200-300 words. Rubric (1 mark): "Output evaluated against what the workplace actually needs".
     1. How predicate logic improves expressiveness and reasoning over propositional logic IN YOUR SCENARIO.
        Use your own rules as evidence (e.g. one quantified rule replaces N propositional copies, one per employee).
     2. How effective your KB is: which real decisions it answers correctly (refer to your queries).
     3. Missing knowledge or limits that could affect decisions (exceptions, discretion, numbers/dates,
        uncertainty, negation/closed-world assumption ...). -->

TODO

## B.5 Reflect

<!-- About 200-300 words. Rubric (1 mark): "Learning and what would change in real deployment".
     1. Practical constraints on deploying this KB in your organisation: incomplete knowledge, changing business
        rules, privacy, scalability, technology/integration limits ... (pick the ones that really apply).
     2. The SINGLE most important improvement you would make before deployment, and why it comes first. -->

TODO
