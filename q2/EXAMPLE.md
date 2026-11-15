# Question 2 – Situated Learning: Knowledge Representation

> Illustration only. Do not copy.
> This is a toy example about a public library's book-loan policy. It shows the format and depth expected in
> each part of your answer.md. It is deliberately short: 4 rules and 2 queries, where the assignment needs at
> least 10 rules and exactly 5 queries. It is not anyone's workplace. Your answer must use your own
> workplace process, rules, facts and queries.
> Check it with: `python q2/check_kb.py q2/EXAMPLE.md --profile example`

## B.1 Submission Form

| Field | Value |
|---|---|
| Name | Illustration only |
| ID No | EXAMPLE |
| Industry / Domain | Public libraries (toy example) |
| Organisation Type | Municipal public library (toy example) |
| Instructor prompt | None given |

## B.2 Anchor

A public library lends books to registered members at its front desk. A staff member scans the member's card and
the book, and the library system approves or refuses the loan. The decision is not up to the desk staff: it follows
the written lending policy. A member must have an active membership, no unpaid fines, and fewer books on loan than
the limit for their category (students 3, staff 5). The book must not already be on loan and must not be
reference-only. A member who keeps a book past its due date gets a fine, which blocks further loans. Because the
same rules apply to every member and every book, the process is a natural fit for a rule-based knowledge base.

*(A real answer would give more context here: about 150–250 words.)*

## B.3 Apply

### B.3.1 Business rules (plain English)

- **BR1:** If a member's membership is active, the member has no unpaid fine, and the number of books they hold is below the loan limit for their category, then the member is eligible to borrow.
- **BR2:** If a book is not on loan and is not reference-only, then the book is available.
- **BR3:** If a member is eligible, has requested a book, and that book is available, then the loan is approved.
- **BR4:** If a member holds a book past its due date, then the member has an unpaid fine.

### B.3.2 Propositions

| Symbol | Meaning (true when ...) |
|---|---|
| A | the member's membership is active |
| F | the member has an unpaid fine |
| U | the member holds fewer books than their category's limit |
| E | the member is eligible to borrow |
| L | the book is on loan |
| R | the book is reference-only |
| V | the book is available |
| Q | the member has requested the book |
| P | the loan is approved |
| O | the member holds an overdue book |

### B.3.3 Rules in propositional logic

- **PL1:** A ∧ ¬F ∧ U → E
- **PL2:** ¬L ∧ ¬R → V
- **PL3:** E ∧ Q ∧ V → P
- **PL4:** O → F

Note the limitation: each proposition is about *one* fixed member and *one* fixed book. Covering three members and
three books would need a separate copy of each proposition (A_asha, A_ravi, ...) and of each rule.

### B.3.4 Predicates, variables and constants

| Predicate | Meaning |
|---|---|
| Member(m) | m is a registered member |
| Active(m) | m's membership is active |
| Category(m, c) | member m belongs to category c |
| Holds(m, n) | member m currently holds n books |
| Limit(c, k) | category c may hold at most k − 1 books before borrowing again (limit k) |
| UnpaidFine(m) | member m has an unpaid fine |
| Eligible(m) | member m is eligible to borrow |
| Book(b) | b is a book in the catalogue |
| OnLoan(b) | book b is currently on loan |
| ReferenceOnly(b) | book b may not leave the library |
| Available(b) | book b can be lent |
| Requests(m, b) | member m asks to borrow book b |
| Approved(m, b) | the loan of book b to member m is approved |
| Overdue(m, b) | member m holds book b past its due date |

| Variable | Ranges over |
|---|---|
| m | members |
| b | books |
| c | membership categories |
| n, k | non-negative integers |

| Constant | Denotes |
|---|---|
| asha, ravi, meena | three members |
| b101, b102, b103 | three books |
| student, staff | membership categories |

### B.3.5 Rules in predicate logic

- **FOL1:** ∀m ∀c ∀n ∀k (Member(m) ∧ Active(m) ∧ ¬UnpaidFine(m) ∧ Category(m, c) ∧ Holds(m, n) ∧ Limit(c, k) ∧ n < k → Eligible(m))
- **FOL2:** ∀b (Book(b) ∧ ¬OnLoan(b) ∧ ¬ReferenceOnly(b) → Available(b))
- **FOL3:** ∀m ∀b (Eligible(m) ∧ Requests(m, b) ∧ Available(b) → Approved(m, b))
- **FOL4:** ∀m (∃b Overdue(m, b) → UnpaidFine(m))

One quantified rule now covers every member and every book. FOL4 uses ∃: one overdue book is enough.

### B.3.6 Knowledge base

```kb
% ---------- Facts ----------
member(asha).  member(ravi).  member(meena).
active(asha).  active(ravi).  active(meena).
category(asha, student).  category(ravi, staff).  category(meena, student).
holds(asha, 1).  holds(ravi, 5).  holds(meena, 2).
limit(student, 3).  limit(staff, 5).
book(b101).  book(b102).  book(b103).
on_loan(b102).
reference_only(b103).
overdue(meena, b102).
requests(asha, b101).  requests(ravi, b101).  requests(asha, b103).

% ---------- Inference rules ----------
% Inference rule 1 (BR4)
unpaid_fine(M) :- overdue(M, B).
% Inference rule 2 (BR1)
eligible(M) :- member(M), active(M), not unpaid_fine(M), category(M, C), holds(M, N), limit(C, K), lt(N, K).
% Inference rule 3 (BR2)
available(B) :- book(B), not on_loan(B), not reference_only(B).
% Inference rule 4 (BR3)
approved(M, B) :- eligible(M), requests(M, B), available(B).

% ---------- Consistency constraint ----------
false :- approved(M, B), on_loan(B).
```

### B.3.7 Workplace queries

#### Query 1

- **Question:** Is Asha's request to borrow book b101 approved?

```query
?- approved(asha, b101).
expect: yes
```

- **Answer:** Yes.
- **Reasoning chain:** By forward chaining with modus ponens:
  1. overdue(asha, _) is not a fact, so inference rule 1 does not derive unpaid_fine(asha). Under the closed-world assumption, `not unpaid_fine(asha)` holds.
  2. member(asha), active(asha), category(asha, student), holds(asha, 1), limit(student, 3) and 1 < 3 hold, so inference rule 2 gives eligible(asha).
  3. book(b101) holds, and neither on_loan(b101) nor reference_only(b101) is a fact, so inference rule 3 gives available(b101).
  4. eligible(asha), requests(asha, b101) and available(b101) hold, so inference rule 4 gives approved(asha, b101).

#### Query 2

- **Question:** Which members are currently eligible to borrow?

```query
?- eligible(M).
expect: M = asha
```

- **Answer:** Only Asha.
- **Reasoning chain:** Inference rule 2 is tried for each member (backward chaining from eligible(M)):
  - M = asha succeeds (steps 1–2 of Query 1).
  - M = ravi fails at lt(5, 5): Ravi already holds the staff limit of 5 books.
  - M = meena fails at `not unpaid_fine(meena)`: overdue(meena, b102) holds, so inference rule 1 derives unpaid_fine(meena).

## B.4 Analyse

Predicate logic lets one rule (FOL1) speak about *every* member through ∀m. The propositional version (PL1) only
describes one anonymous member, so it would need a copy for each member. Predicates also carry relationships
(Requests(m, b)) and numbers (Holds(m, n), n < k) that propositions cannot express. The KB correctly approves Asha
and refuses Ravi and Meena, each for the policy reason. It is missing due dates (overdue is entered as a fact, not
computed from dates) and fine amounts, so it cannot handle "fines under ₹10 are ignored".

*(A real answer: about 200–300 words, using your own rules and queries as evidence.)*

## B.5 Reflect

Deploying this would need live data from the library system (membership status, loans, dates). Policy changes, such
as new limits, must be updated in the rules, and member data is personal and must be protected. The single most
important improvement is to derive overdue status from loan dates automatically instead of entering it by hand.
Stale overdue facts would wrongly block or allow loans.

*(A real answer: about 200–300 words, specific to your organisation.)*
