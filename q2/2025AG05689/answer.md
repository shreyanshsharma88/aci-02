# Question 2 – Situated Learning: Knowledge Representation

<!--
HOW TO USE THIS FILE
- Read q2/GUIDE.md and q2/EXAMPLE.md first (about 15 minutes).
- Replace every placeholder with your own content. Use your own workplace (or the industry equivalent).
- Text inside these comment markers is guidance. It is removed from the PDF, so you may leave it or delete it.
- Keep the headings, the labels (BR1, PL1, FOL1, Query 1 ...) and the ```kb / ```query fences exactly as they are:
  the checker and the PDF builder look for them.
- Check:  python q2/check_kb.py q2/2025AG05689/answer.md
- Build:  python q2/build_pdf.py q2/2025AG05689/answer.md
-->

## B.1 Submission Form

| Field | Value |
|---|---|
| Name | VINAY PRATAP SINGH BHADAURIA |
| ID No | 2025AG05689 |
| Industry / Domain | IT services (cloud and application support) |
| Organisation Type | Private multinational |
| Instructor prompt | None given |

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

The workplace artifact is the production change-approval process followed by the engineering and operations teams of an IT services organisation. Every change to a production system, such as a patch, a configuration change or a database schema upgrade, is raised as a change request (CR) in the IT service-management tool. The requester, the requester's line manager, the Change Advisory Board (CAB), an emergency approver and the release coordinator all take part.

The process decides who must approve a change, whether that approval is valid, whether the change may be scheduled on the planned day, and whether a post-implementation review is needed. The rules come from the organisation's change-management policy, an SOP aligned with the ITIL change-enablement practice, and customer contracts that forbid unreviewed production changes.

These decisions follow rules because a production change can disrupt a live service, and auditors need evidence of who authorised it. The same facts about a request should lead to the same approval route, whoever handles it. The policy also separates requesting from approving: a CAB member cannot approve their own change. The examples below use invented names, change numbers and dates.

## B.3 Apply

<!-- Rubric (2 marks): the core concept (propositional logic, predicate logic, knowledge base) correctly applied
     to your workplace artifact. -->

### B.3.1 Business rules (plain English)

The rules separate approval from scheduling. A routine, pre-approved patch can take an automatic route, while a critical-system change needs CAB review. Even an approved change may have to wait for a freeze window to end. Emergency changes have an exception, but still need an independent, authorised approver.

<!-- At least 10. One rule per line, each a condition and a consequence ("If ... then ..."). Add BR11, BR12 ... if you want. -->

- **BR1:** If a change request has a rollback plan and test evidence, then it is complete.
- **BR2:** If a complete change matches a pre-approved standard template and does not touch a critical system, then it is auto-approved.
- **BR3:** If a change touches a critical system, then it is high risk.
- **BR4:** If a complete change is high risk and is not an emergency, then Change Advisory Board (CAB) approval is required.
- **BR5:** If a complete change is not standard, not high risk and not an emergency, then its line manager's approval is required.
- **BR6:** If a change is approved by an authorised approver who is not the requester, then the approval is valid.
- **BR7:** If a change has a valid approval or is auto-approved, and its planned day is not in a freeze window, then it may be scheduled.
- **BR8:** If an emergency change has a valid approval, then it may be scheduled even inside a freeze window.
- **BR9:** If a change is an emergency change, then a post-implementation review (PIR) is required.
- **BR10:** If a change was implemented without a valid approval and without auto-approval, then it is a policy breach.

### B.3.2 Propositions

Each proposition is a statement about one fixed change request. For example, P1 says that this request has a rollback plan; it does not identify which change the plan belongs to. A proposition can be true or false. The symbols below let us express the ten policies without repeating their full wording.

<!-- Define EVERY symbol you use in B.3.3. A proposition is a statement that is simply true or false
     (e.g. "P1 | The employee has submitted a leave request"). Add rows as needed. -->

| Symbol | Meaning (true when ...) |
|---|---|
| P1 | The change request has a rollback plan |
| P2 | The change request has test evidence |
| P3 | The change request is complete |
| P4 | The change matches a pre-approved standard template |
| P5 | The change touches a critical system |
| P6 | The change is high risk |
| P7 | The change is an emergency change |
| P8 | CAB approval is required |
| P9 | Line manager approval is required |
| P10 | The change was approved by an authorised approver |
| P11 | The approver is the same person as the requester |
| P12 | The change has a valid approval |
| P13 | The planned day is inside a freeze window |
| P14 | The change may be scheduled |
| P15 | A post-implementation review is required |
| P16 | The change is auto-approved |
| P17 | The change was implemented |
| P18 | The change is a policy breach |

### B.3.3 Rules in propositional logic

<!-- PLn is the propositional form of BRn. Write ONLY the formula on the line.
     Connectives: ¬ (not), ∧ (and), ∨ (or), → (implies), ↔ (iff); ASCII ~ & | -> <-> also work. Use brackets.
     Example format:  - **PL1:** P1 ∧ P2 ∧ ¬P3 → P4 -->

- **PL1:** P1 ∧ P2 → P3
- **PL2:** P3 ∧ P4 ∧ ¬P5 → P16
- **PL3:** P5 → P6
- **PL4:** P3 ∧ P6 ∧ ¬P7 → P8
- **PL5:** P3 ∧ ¬P4 ∧ ¬P6 ∧ ¬P7 → P9
- **PL6:** P10 ∧ ¬P11 → P12
- **PL7:** (P12 ∨ P16) ∧ ¬P13 → P14
- **PL8:** P7 ∧ P12 → P14
- **PL9:** P7 → P15
- **PL10:** P17 ∧ ¬P12 ∧ ¬P16 → P18

Here, ∧ means "and", ∨ means "or", ¬ means "not", and → means "if ... then". PL7 says that either valid approval or auto-approval is sufficient for scheduling, provided the planned day is outside the freeze. PL8 records the emergency exception separately.

This representation works for one request at a time. It cannot directly connect a request to its requester, approver and planned day. In particular, P11 hides the comparison between two people inside a single statement. Predicate logic makes those relationships explicit.

### B.3.4 Predicates, variables and constants

Predicates describe properties and relationships. HasRollback(c) describes a change, while ApprovedBy(c, a) connects a change to the person who approved it. Variables let the same rule apply to different requests and people; constants identify the particular examples stored in the knowledge base.

<!-- Predicates take arguments, e.g. Employee(x), LeaveBalance(x, d). Every predicate used in B.3.5 AND in the
     KB block must be in this table (names are matched ignoring case and underscores, so LeaveBalance = leave_balance). -->

| Predicate | Meaning |
|---|---|
| HasRollback(c) | Change c has a rollback plan |
| HasTestEvidence(c) | Change c has test evidence |
| Complete(c) | Change request c is complete |
| StandardTemplate(c) | Change c matches a pre-approved standard template |
| TouchesCritical(c) | Change c touches a critical system |
| HighRisk(c) | Change c is high risk |
| Emergency(c) | Change c is an emergency change |
| CabRequired(c) | CAB approval is required for change c |
| ManagerRequired(c) | Line manager approval is required for change c |
| AutoApproved(c) | Change c is auto-approved |
| RequestedBy(c, r) | Change c was requested by person r |
| ApprovedBy(c, a) | Change c was approved by person a |
| CabMember(a) | Person a is a CAB member |
| LineManagerOf(a, r) | Person a is the line manager of person r |
| EmergencyApprover(a) | Person a is a designated emergency approver |
| Authorised(a, c) | Person a is authorised to approve change c |
| ValidApproval(c) | Change c has a valid approval |
| PlannedDay(c, d) | Change c is planned for day d |
| FreezeDay(d) | Day d is inside a freeze window |
| Schedulable(c) | Change c may be scheduled |
| PirRequired(c) | A post-implementation review is required for change c |
| Implemented(c) | Change c was implemented |
| PolicyBreach(c) | Change c is a policy breach |

| Variable | Ranges over |
|---|---|
| c | change requests |
| a | approvers (people) |
| r | requesters (people) |
| d | calendar days |

| Constant | Denotes |
|---|---|
| chg101 to chg105 | the five change requests in the KB |
| priya, rahul, meera, sameer, anita | people (requesters, approvers) |
| d_nov10, d_nov12, d_dec24 | calendar days (d_dec24 is in a freeze window) |

### B.3.5 Rules in predicate logic

<!-- FOLn is the predicate-logic form of the SAME rule BRn, with quantifiers.
     Example format:  - **FOL1:** ∀x ∀d (Employee(x) ∧ Balance(x, d) ∧ d ≥ 1 → CanApply(x)) -->

- **FOL1:** ∀c (HasRollback(c) ∧ HasTestEvidence(c) → Complete(c))
- **FOL2:** ∀c (Complete(c) ∧ StandardTemplate(c) ∧ ¬TouchesCritical(c) → AutoApproved(c))
- **FOL3:** ∀c (TouchesCritical(c) → HighRisk(c))
- **FOL4:** ∀c (Complete(c) ∧ HighRisk(c) ∧ ¬Emergency(c) → CabRequired(c))
- **FOL5:** ∀c (Complete(c) ∧ ¬StandardTemplate(c) ∧ ¬HighRisk(c) ∧ ¬Emergency(c) → ManagerRequired(c))
- **FOL6:** ∀c ∀a ∀r (ApprovedBy(c, a) ∧ Authorised(a, c) ∧ RequestedBy(c, r) ∧ a ≠ r → ValidApproval(c))
- **FOL7:** ∀c ∀d ((ValidApproval(c) ∨ AutoApproved(c)) ∧ PlannedDay(c, d) ∧ ¬FreezeDay(d) → Schedulable(c))
- **FOL8:** ∀c (Emergency(c) ∧ ValidApproval(c) → Schedulable(c))
- **FOL9:** ∀c (Emergency(c) → PirRequired(c))
- **FOL10:** ∀c (Implemented(c) ∧ ¬ValidApproval(c) ∧ ¬AutoApproved(c) → PolicyBreach(c))

The symbol ∀ means "for every". FOL6 therefore checks every combination of change, approver and requester: approval is valid only when the approver is authorised and is a different person from the requester (a ≠ r). Being a CAB member does not remove that independence requirement. FOL7 connects the change's planned day to the freeze calendar, so an approval does not automatically make the change schedulable.

### B.3.6 Knowledge base

The KB applies these policies to five example changes. chg101 is a standard patch, chg102 a critical payments database upgrade, chg103 an application configuration change, chg104 an emergency fix, and chg105 a self-approved change that has already been implemented. Together they exercise the normal routes and the exceptions.

There are 31 recorded facts and 14 inference rules. A fact records something known about a request, person or day. A rule derives a further conclusion from those facts. The PDF groups facts by predicate: for example, the tuple (chg102, meera) under approved_by means that Meera approved chg102. The tuples are records, not calculations.

The rules use Prolog-style notation: `:-` reads "if", commas mean "and", and capital letters are variables. IR1 to IR5 implement BR1 to BR5. IR6 to IR9 work out who is authorised and whether approval is valid (BR6). IR10 and IR11 cover the two ordinary scheduling routes (BR7); IR12 to IR14 implement BR8 to BR10.

<!-- At least 20 facts and at least 10 inference rules, in the syntax of q2/KB_SYNTAX.md.
     Write each clause on the line after its "% Fact n" / "% Inference rule n" comment. Add more lines as needed.
     The checker runs this block with forward chaining. -->

```kb
% ---------- Facts (at least 20) ----------
% Fact 1-2: chg101 (standard patch) has rollback and test evidence
has_rollback(chg101). has_test_evidence(chg101).
% Fact 3-4: chg101 uses a standard template and is planned for a normal day
standard_template(chg101). planned_day(chg101, d_nov10).
% Fact 5-6: chg102 (payments DB upgrade) has rollback and test evidence
has_rollback(chg102). has_test_evidence(chg102).
% Fact 7-8: chg102 touches a critical system and was requested by rahul
touches_critical(chg102). requested_by(chg102, rahul).
% Fact 9-10: chg102 was approved by meera and is planned inside the freeze
approved_by(chg102, meera). planned_day(chg102, d_dec24).
% Fact 11-12: chg103 (app configuration change) has rollback and test evidence
has_rollback(chg103). has_test_evidence(chg103).
% Fact 13-14: chg103 was requested by priya and approved by sameer
requested_by(chg103, priya). approved_by(chg103, sameer).
% Fact 15: chg103 is planned for a normal day
planned_day(chg103, d_nov12).
% Fact 16-17: chg104 (emergency fix) has a rollback plan and touches a critical system
has_rollback(chg104). touches_critical(chg104).
% Fact 18-19: chg104 is an emergency requested by rahul
emergency(chg104). requested_by(chg104, rahul).
% Fact 20-21: chg104 was approved by anita and is planned inside the freeze
approved_by(chg104, anita). planned_day(chg104, d_dec24).
% Fact 22-23: chg105 has rollback and test evidence
has_rollback(chg105). has_test_evidence(chg105).
% Fact 24-25: chg105 touches a critical system and was requested by meera
touches_critical(chg105). requested_by(chg105, meera).
% Fact 26-27: chg105 was approved by meera herself and has been implemented
approved_by(chg105, meera). implemented(chg105).
% Fact 28-29: meera is a CAB member and sameer is priya's line manager
cab_member(meera). line_manager_of(sameer, priya).
% Fact 30-31: anita is an emergency approver and d_dec24 is a freeze day
emergency_approver(anita). freeze_day(d_dec24).

% ---------- Inference rules (at least 10) ----------
% Inference rule 1 (BR1): complete
complete(C) :- has_rollback(C), has_test_evidence(C).
% Inference rule 2 (BR2): auto-approval of standard, non-critical changes
auto_approved(C) :- complete(C), standard_template(C), not touches_critical(C).
% Inference rule 3 (BR3): critical systems mean high risk
high_risk(C) :- touches_critical(C).
% Inference rule 4 (BR4): CAB route
cab_required(C) :- complete(C), high_risk(C), not emergency(C).
% Inference rule 5 (BR5): line manager route
manager_required(C) :- complete(C), not standard_template(C), not high_risk(C), not emergency(C).
% Inference rules 6-8 (BR6): who is authorised to approve
authorised(A, C) :- cab_required(C), cab_member(A).
authorised(A, C) :- manager_required(C), line_manager_of(A, R), requested_by(C, R).
authorised(A, C) :- emergency(C), emergency_approver(A).
% Inference rule 9 (BR6): valid approval, approver is not the requester
valid_approval(C) :- approved_by(C, A), authorised(A, C), requested_by(C, R), neq(A, R).
% Inference rules 10-11 (BR7): scheduling outside the freeze window
schedulable(C) :- valid_approval(C), planned_day(C, D), not freeze_day(D).
schedulable(C) :- auto_approved(C), planned_day(C, D), not freeze_day(D).
% Inference rule 12 (BR8): emergency changes may be scheduled in a freeze
schedulable(C) :- emergency(C), valid_approval(C).
% Inference rule 13 (BR9): emergency changes need a review
pir_required(C) :- emergency(C).
% Inference rule 14 (BR10): implemented without approval
policy_breach(C) :- implemented(C), not valid_approval(C), not auto_approved(C).

% ---------- Optional consistency constraints ----------
% false :- approved(X), rejected(X).
```

### B.3.7 Workplace queries

The checker answers these queries by forward chaining. It starts with the recorded facts, applies a rule when its conditions hold, and adds the conclusion as a new fact. This uses modus ponens: knowing A and "if A then B" allows us to conclude B. The process continues until no further facts can be derived.

The executable KB uses negation as failure: `not` succeeds when a statement cannot be derived. This closed-world assumption is stronger than simply saying that a fact is unknown. The examples assume the relevant records are complete; the deployment risks of missing records are discussed in B.4 and B.5.

<!-- Exactly 5 queries. For each: the question in plain English, the formal query and expected answer
     (the checker verifies it), the answer, and the reasoning chain (which facts and rules, in which order,
     by forward or backward chaining with modus ponens). See EXAMPLE.md. -->

#### Query 1

- **Question:** Can the standard patch chg101 be approved automatically, without any approver?

```query
?- auto_approved(chg101).
expect: yes
```

- **Reasoning chain:** The rollback plan and test evidence establish completeness; the standard-template rule then supplies the approval route.

1. chg101 has a rollback plan and test evidence, so IR1 makes it complete.
2. It matches a pre-approved standard template, and there is no recorded critical-system impact.
3. IR2 therefore derives auto_approved(chg101).

- **Answer:** Yes. This standard patch can use the automatic approval route without a named approver. This query establishes approval only; scheduling still depends on the planned day.

#### Query 2

- **Question:** The payments database upgrade chg102 has a CAB approval. Can it be scheduled on its planned day?

```query
?- schedulable(chg102).
expect: no
```

- **Reasoning chain:** Approval and scheduling are separate checks. The approval succeeds, but the freeze prevents the ordinary scheduling route.

1. The rollback plan and test evidence make chg102 complete (IR1). Its critical-system impact makes it high risk (IR3), so this non-emergency change needs CAB approval (IR4).
2. Meera is a CAB member, so IR6 makes her an authorised approver. She approved the request raised by Rahul; because they are different people, IR9 makes the approval valid.
3. The planned day is d_dec24, which is a recorded freeze day. IR10 cannot schedule a change on that day through the ordinary approval route.
4. Auto-approval is unavailable for this critical change (IR2), so IR11 provides no alternative. There is also no emergency fact to support IR12.

- **Answer:** No. The CAB approval is valid, but the change cannot be scheduled on its planned day because that day is inside the freeze and the change is not an emergency in this KB.

#### Query 3

- **Question:** Which implemented changes are policy breaches?

```query
?- policy_breach(C).
expect: C = chg105
```

- **Reasoning chain:** The variable C asks the KB to find any implemented change that lacks both valid approval and auto-approval.

1. chg105 is the only change recorded as implemented.
2. It has rollback and test evidence, touches a critical system and has no emergency fact, so IR1, IR3 and IR4 put it on the CAB route. Meera is a CAB member, making her authorised under IR6.
3. Meera is also the requester. The independence check in IR9 fails because the requester and approver are the same person, so there is no valid approval.
4. Critical-system impact prevents auto-approval under IR2. With neither approval route satisfied, IR14 derives policy_breach(chg105).

- **Answer:** Only chg105. It was implemented after self-approval, which breaches segregation of duties even though the requester is a CAB member.

#### Query 4

- **Question:** Which emergency changes may be scheduled, even inside the freeze window, and also need a post-implementation review?

```query
?- emergency(C), schedulable(C), pir_required(C).
expect: C = chg104
```

- **Reasoning chain:** Working backwards from the question identifies three conditions to check: emergency status, permission to schedule and a required review. The same facts and rules are verified by the forward-chaining checker.

1. chg104 is explicitly recorded as an emergency.
2. Anita is a designated emergency approver, so IR8 authorises her. She approved Rahul's request, and the two people are different, so IR9 establishes valid approval.
3. Emergency status and valid approval satisfy IR12. This scheduling route does not require the planned day to be outside the freeze.
4. IR13 also derives a post-implementation review requirement from the emergency status.

- **Answer:** chg104. The emergency fix may be scheduled during the freeze because it has independent emergency approval, but it must receive a post-implementation review afterwards.

#### Query 5

- **Question:** Who is authorised to approve the configuration change chg103?

```query
?- authorised(A, chg103).
expect: A = sameer
```

- **Reasoning chain:** This query asks for a person rather than a yes/no answer. The KB first determines the approval route, then finds the requester's manager.

1. chg103 has rollback and test evidence, so IR1 makes it complete.
2. No standard-template, high-risk or emergency status is derivable. Under the closed-world assumption, IR5 therefore selects line-manager approval.
3. Priya raised the request, and Sameer is recorded as Priya's line manager. IR7 binds the approver variable A to sameer.
4. The CAB and emergency routes do not supply other approvers because their conditions are not met.

- **Answer:** Sameer, Priya's line manager. The ordinary configuration change follows the manager route; this query identifies who may approve it, separately from whether an approval has already been given.

## B.4 Analyse

<!-- About 200-300 words. Rubric (1 mark): "Output evaluated against what the workplace actually needs".
     1. How predicate logic improves expressiveness and reasoning over propositional logic IN YOUR SCENARIO.
        Use your own rules as evidence (e.g. one quantified rule replaces N propositional copies, one per employee).
     2. How effective your KB is: which real decisions it answers correctly (refer to your queries).
     3. Missing knowledge or limits that could affect decisions (exceptions, discretion, numbers/dates,
        uncertainty, negation/closed-world assumption ...). -->

### B.4.1 Expressiveness in this process

The self-approval example shows why predicate logic is useful. P11 can state that the approver and requester are the same person for one fixed request, but it hides who those people are. FOL6 names both roles and compares them. The same quantified rule checks Meera's self-approval and Anita's independent approval without needing separate rules for each person. FOL7 similarly connects each request to its planned day and the shared freeze calendar. Propositional logic could encode these individual cases, but would need new symbols and repeated rule instances.

### B.4.2 Effectiveness of the knowledge base

The five queries cover decisions that a release coordinator needs. The standard patch takes the automatic route; the configuration change goes to its requester's manager. The critical upgrade has valid CAB approval but still cannot run during the freeze. The emergency fix can run with independent approval and requires a review. The implemented, self-approved change is flagged as a breach. The checker reproduced all five expected answers by forward chaining.

### B.4.3 Missing knowledge and limits

The results depend on complete records. Missing test evidence can hold a change, but a missing freeze-day fact can wrongly permit scheduling. Absence of a fact is not reliable evidence about the workplace. Risk is also reduced to critical-system impact; the model omits change size, customer impact and past failures. Freeze dates must be listed individually. CAB quorum, manager discretion, rejection reasons and rollback after failure are not represented. These gaps limit the KB to a simplified decision assistant.

## B.5 Reflect

<!-- About 200-300 words. Rubric (1 mark): "Learning and what would change in real deployment".
     1. Practical constraints on deploying this KB in your organisation: incomplete knowledge, changing business
        rules, privacy, scalability, technology/integration limits ... (pick the ones that really apply).
     2. The SINGLE most important improvement you would make before deployment, and why it comes first. -->

### B.5.1 Practical deployment constraints

In deployment, the first concern would be the records supplied to the KB. A missing approval and an approval that never happened look the same under negation as failure. Missing criticality or freeze information can be more dangerous because it may allow a change through. The assistant should expose missing information for review instead of treating every absence as a verified negative.

Policies and supporting records also change. The freeze calendar, standard templates and CAB membership need maintenance, or yesterday's facts may produce today's wrong decision. Approval records link people to production systems and customers, so access and logging need privacy controls. Connecting the service-management tool, configuration database and calendar would require reliable identifiers and consistent updates. Larger volumes would need performance testing; the small example does not establish production capacity. Staff must be able to inspect a decision's reasoning and challenge incorrect inputs.

### B.5.2 The most important improvement

Before deployment, I would prioritise automatically feeding verified facts from the source systems into the KB. The integration should check that the required records are present and current before a decision is issued. This directly addresses the largest weakness exposed by the examples: correct rules can still reach an unsafe conclusion from incomplete or stale inputs.

An outdated CAB list could recognise the wrong approver, while a missing freeze entry could allow an otherwise valid change to run at the wrong time. Better risk scoring and exception handling would be useful later, but reliable input records are needed before either can be trusted.
