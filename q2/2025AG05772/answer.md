# Question 2 – Situated Learning: Knowledge Representation

## B.1 Submission Form

| Field | Value |
|---|---|
| Name | SHREYANSH SHARMA |
| ID No | 2025AG05772 |
| Industry / Domain | Information technology: software product development |
| Organisation Type | Private software start-up (buntikki) |
| Instructor prompt | None given |

## B.2 Anchor

I work as a product software engineer at buntikki, a software start-up, where I build and maintain product
features end to end, covering backend services, APIs, the user interface and deployment. For this question I
modelled our production release approval process, which I deal with from both sides: I raise pull requests for my
own changes and review pull requests from other engineers.

Each change goes in as a pull request and is linked to a change request (CR) on the release calendar. Two peers
have to approve it, and a tech lead has to sign off anything marked high risk. Changes to the payments service also
need a security reviewer. The release manager owns the calendar and declares freeze windows, and after a release
the on-call engineer for that service keeps an eye on it. Checks run in CI (tests and coverage), a security scanner and
staging.

Each CR ends up either approved for deployment or held. The release policy lists the conditions for approval,
because production carries real customer traffic and payments, and one untested change can take a service down or
break checkout. When a condition fails, for example the scanner finds a critical vulnerability or the release is
booked into a freeze window, the CR goes back to its author. A bad change that gets through is rolled back. The policy combines roles, numeric thresholds, risk levels, calendar windows and
exceptions, so it maps well onto rules over facts.

## B.3 Apply

### B.3.1 Business rules (plain English)

- **BR1:** If a change has been approved by at least two different reviewers, neither of whom is its author, then the change is peer-reviewed.
- **BR2:** If all CI tests for a change pass and its code coverage is at least 80%, then the change is build-verified.
- **BR3:** If the security scan reports a critical vulnerability in a change, then the change is security-blocked.
- **BR4:** If a change modifies the payments service and has no security sign-off, then the change is security-blocked.
- **BR5:** If a change is classified as low risk, then its risk is cleared.
- **BR6:** If a change is classified as high risk, has been approved by a senior engineer who is not its author, and has a documented rollback plan, then its risk is cleared.
- **BR7:** If a change is peer-reviewed, build-verified, not security-blocked, risk-cleared and verified on staging, then it is release-ready.
- **BR8:** If a change is release-ready and its planned release window is not under a release freeze, then it is approved for production deployment.
- **BR9:** If a change is release-ready and is a hotfix for a severity-1 (sev1) incident, then it is approved for production deployment, even during a freeze.
- **BR10:** If a change has been requested for release but is not approved for deployment, then it is held.
- **BR11:** If a high-risk change is approved for deployment, then the on-call engineer of the service it modifies must be paged to monitor the release.

### B.3.2 Propositions

All symbols describe one fixed change request.

| Symbol | Meaning (true when ...) |
|---|---|
| TA | the change has two approvals from two different reviewers who are not its author |
| PR | the change is peer-reviewed |
| CI | all CI tests for the change pass |
| CV | the change's code coverage is at least 80% |
| BV | the change is build-verified |
| VC | the security scan reports a critical vulnerability in the change |
| PM | the change modifies the payments service |
| SS | the change has a security sign-off |
| SB | the change is security-blocked |
| LR | the change is classified as low risk |
| HR | the change is classified as high risk |
| SA | a senior engineer who is not the author has approved the change |
| RP | the change has a documented rollback plan |
| RC | the change's risk is cleared |
| SV | the change has been verified on staging |
| RR | the change is release-ready |
| FZ | the change's planned release window is under a release freeze |
| HF | the change is a hotfix for a sev1 incident |
| DA | the change is approved for production deployment |
| RQ | the change has been requested for release |
| HD | the change is held |
| OC | the on-call engineer of the modified service must be paged |

### B.3.3 Rules in propositional logic

- **PL1:** TA → PR
- **PL2:** CI ∧ CV → BV
- **PL3:** VC → SB
- **PL4:** PM ∧ ¬SS → SB
- **PL5:** LR → RC
- **PL6:** HR ∧ SA ∧ RP → RC
- **PL7:** PR ∧ BV ∧ ¬SB ∧ RC ∧ SV → RR
- **PL8:** RR ∧ ¬FZ → DA
- **PL9:** RR ∧ HF → DA
- **PL10:** RQ ∧ ¬DA → HD
- **PL11:** DA ∧ HR → OC

Read together, PL3 and PL4 say (VC ∨ (PM ∧ ¬SS)) → SB, and PL8 and PL9 say
(RR ∧ (¬FZ ∨ HF)) → DA. Each proposition describes a single change. To cover six change requests, every symbol and
every rule would need six copies (PR_cr201, PR_cr202, ...).

### B.3.4 Predicates, variables and constants

| Predicate | Meaning |
|---|---|
| ReleaseRequested(c) | change request c has been submitted for a production release |
| Author(c, p) | person p wrote change c |
| ApprovedBy(c, p) | person p approved the pull request of change c |
| PeerReviewed(c) | change c has two independent non-author approvals |
| CiPassed(c) | all CI tests for change c pass |
| Coverage(c, n) | the code coverage of change c is n percent |
| BuildVerified(c) | change c passed CI with enough coverage |
| CriticalVuln(c) | the security scanner reports a critical vulnerability in change c |
| Modifies(c, s) | change c modifies service s |
| SecuritySignoff(c) | the security reviewer has signed off change c |
| SecurityBlocked(c) | change c may not be released for a security reason |
| Risk(c, l) | change c is classified at risk level l |
| Senior(p) | person p is a senior engineer (tech lead) |
| RollbackPlan(c) | change c has a documented rollback plan |
| RiskCleared(c) | the risk of change c has been accepted under the policy |
| StagingVerified(c) | change c has been tested on the staging environment |
| ReleaseReady(c) | change c meets every pre-release condition |
| ReleaseWindow(c, w) | change c is planned for release window w |
| Freeze(w) | release window w is under a release freeze |
| HotfixFor(c, i) | change c fixes incident i |
| Severity(i, v) | incident i has severity v |
| DeployApproved(c) | change c is approved for production deployment |
| Held(c) | change c is held and returned to its author |
| OnCall(s, p) | person p is the on-call engineer for service s |
| PageOnCall(c, p) | on-call engineer p must be paged to monitor the release of change c |

| Variable | Ranges over |
|---|---|
| c | change requests |
| p, a, r, r1, r2 | people (developers, reviewers, engineers) |
| s | services |
| n | coverage percentages (integers 0 to 100) |
| l | risk levels |
| w | release windows |
| i | incidents |
| v | incident severities |

| Constant | Denotes |
|---|---|
| cr201, cr202, cr203, cr204, cr205, cr206 | six change requests (invented) |
| arjun, meera, kabir, nisha, rohan, tara, vikram | seven engineers (invented names) |
| payments, catalogue, notifications | three application services |
| low, high | risk levels |
| wk46_thu, wk47_fri | two release windows (Thursday of week 46, Friday of week 47) |
| inc77 | a production incident |
| sev1 | the highest incident severity |
| 80 | the minimum coverage percentage |

### B.3.5 Rules in predicate logic

- **FOL1:** ∀c ∀a (Author(c, a) ∧ ∃r1 ∃r2 (ApprovedBy(c, r1) ∧ ApprovedBy(c, r2) ∧ r1 ≠ r2 ∧ r1 ≠ a ∧ r2 ≠ a) → PeerReviewed(c))
- **FOL2:** ∀c ∀n (CiPassed(c) ∧ Coverage(c, n) ∧ n ≥ 80 → BuildVerified(c))
- **FOL3:** ∀c (CriticalVuln(c) → SecurityBlocked(c))
- **FOL4:** ∀c (Modifies(c, payments) ∧ ¬SecuritySignoff(c) → SecurityBlocked(c))
- **FOL5:** ∀c (Risk(c, low) → RiskCleared(c))
- **FOL6:** ∀c ∀a (Risk(c, high) ∧ Author(c, a) ∧ ∃r (ApprovedBy(c, r) ∧ Senior(r) ∧ r ≠ a) ∧ RollbackPlan(c) → RiskCleared(c))
- **FOL7:** ∀c (PeerReviewed(c) ∧ BuildVerified(c) ∧ ¬SecurityBlocked(c) ∧ RiskCleared(c) ∧ StagingVerified(c) → ReleaseReady(c))
- **FOL8:** ∀c ∀w (ReleaseReady(c) ∧ ReleaseWindow(c, w) ∧ ¬Freeze(w) → DeployApproved(c))
- **FOL9:** ∀c (ReleaseReady(c) ∧ ∃i (HotfixFor(c, i) ∧ Severity(i, sev1)) → DeployApproved(c))
- **FOL10:** ∀c (ReleaseRequested(c) ∧ ¬DeployApproved(c) → Held(c))
- **FOL11:** ∀c ∀s ∀p (DeployApproved(c) ∧ Risk(c, high) ∧ Modifies(c, s) ∧ OnCall(s, p) → PageOnCall(c, p))

FOL1, FOL6 and FOL9 use ∃ because one suitable reviewer, senior approver or incident is enough. FOL1 expresses
"two different reviewers" with r1 ≠ r2, which propositional logic can only state as one opaque symbol (TA).

### B.3.6 Knowledge base

```kb
% ---------- Facts ----------
% Change requests submitted for release
release_requested(cr201).  release_requested(cr202).  release_requested(cr203).
release_requested(cr204).  release_requested(cr205).  release_requested(cr206).

% Authors and the services each change modifies
author(cr201, arjun).   modifies(cr201, catalogue).
author(cr202, meera).   modifies(cr202, payments).
author(cr203, kabir).   modifies(cr203, notifications).
author(cr204, nisha).   modifies(cr204, payments).
author(cr205, rohan).   modifies(cr205, catalogue).
author(cr206, arjun).   modifies(cr206, catalogue).

% Pull-request approvals
approved_by(cr201, meera).  approved_by(cr201, kabir).
approved_by(cr202, tara).   approved_by(cr202, arjun).
approved_by(cr203, nisha).  approved_by(cr203, rohan).
approved_by(cr204, tara).   approved_by(cr204, vikram).
approved_by(cr205, meera).  approved_by(cr205, arjun).
approved_by(cr206, vikram). approved_by(cr206, meera).
senior(tara).  senior(vikram).

% CI results and code coverage (%)
ci_passed(cr201). ci_passed(cr202). ci_passed(cr203). ci_passed(cr204). ci_passed(cr205). ci_passed(cr206).
coverage(cr201, 86).  coverage(cr202, 91).  coverage(cr203, 72).
coverage(cr204, 88).  coverage(cr205, 83).  coverage(cr206, 81).

% Security scan and security sign-off
critical_vuln(cr203).
security_signoff(cr202).

% Risk classification and rollback plans
risk(cr201, low).  risk(cr202, high).  risk(cr203, low).
risk(cr204, high). risk(cr205, low).   risk(cr206, low).
rollback_plan(cr202).  rollback_plan(cr204).

% Staging verification
staging_verified(cr201). staging_verified(cr202). staging_verified(cr204).
staging_verified(cr205). staging_verified(cr206).

% Release calendar, freeze and incidents
release_window(cr201, wk46_thu).  release_window(cr202, wk46_thu).  release_window(cr203, wk46_thu).
release_window(cr204, wk46_thu).  release_window(cr205, wk47_fri).  release_window(cr206, wk47_fri).
freeze(wk47_fri).
hotfix_for(cr206, inc77).
severity(inc77, sev1).

% On-call rota
on_call(payments, rohan).  on_call(catalogue, kabir).  on_call(notifications, nisha).

% ---------- Inference rules ----------
% Inference rule 1 (BR1): two different non-author approvals
peer_reviewed(C) :- author(C, A), approved_by(C, R1), approved_by(C, R2), neq(R1, R2), neq(R1, A), neq(R2, A).
% Inference rule 2 (BR2)
build_verified(C) :- ci_passed(C), coverage(C, N), ge(N, 80).
% Inference rule 3 (BR3)
security_blocked(C) :- critical_vuln(C).
% Inference rule 4 (BR4)
security_blocked(C) :- modifies(C, payments), not security_signoff(C).
% Inference rule 5 (BR5)
risk_cleared(C) :- risk(C, low).
% Inference rule 6 (BR6)
risk_cleared(C) :- risk(C, high), author(C, A), approved_by(C, R), senior(R), neq(R, A), rollback_plan(C).
% Inference rule 7 (BR7)
release_ready(C) :- peer_reviewed(C), build_verified(C), not security_blocked(C), risk_cleared(C), staging_verified(C).
% Inference rule 8 (BR8)
deploy_approved(C) :- release_ready(C), release_window(C, W), not freeze(W).
% Inference rule 9 (BR9): sev1 hotfix exception to the freeze
deploy_approved(C) :- release_ready(C), hotfix_for(C, I), severity(I, sev1).
% Inference rule 10 (BR10)
held(C) :- release_requested(C), not deploy_approved(C).
% Inference rule 11 (BR11)
page_on_call(C, P) :- deploy_approved(C), risk(C, high), modifies(C, S), on_call(S, P).

% ---------- Consistency constraints ----------
false :- deploy_approved(C), security_blocked(C).
false :- deploy_approved(C), held(C).
```

### B.3.7 Workplace queries

#### Query 1

- **Question:** Can change cr202, a high-risk change to the payments service, be deployed to production in this week's Thursday window?

```query
?- deploy_approved(cr202).
expect: yes
```

- **Answer:** Yes.
- **Reasoning chain:** By forward chaining with modus ponens:
  1. author(cr202, meera), approved_by(cr202, tara) and approved_by(cr202, arjun) are facts, and tara ≠ arjun, tara ≠ meera, arjun ≠ meera, so inference rule 1 gives peer_reviewed(cr202).
  2. ci_passed(cr202) and coverage(cr202, 91) are facts and 91 ≥ 80, so inference rule 2 gives build_verified(cr202).
  3. critical_vuln(cr202) is not a fact, so inference rule 3 does not fire. modifies(cr202, payments) holds, but security_signoff(cr202) is a fact, so inference rule 4 does not fire either. Under the closed-world assumption, `not security_blocked(cr202)` holds.
  4. risk(cr202, high), approved_by(cr202, tara), senior(tara), tara ≠ meera and rollback_plan(cr202) hold, so inference rule 6 gives risk_cleared(cr202).
  5. With steps 1 to 4 and staging_verified(cr202), inference rule 7 gives release_ready(cr202).
  6. release_window(cr202, wk46_thu) holds and freeze(wk46_thu) is not a fact, so inference rule 8 gives deploy_approved(cr202).

#### Query 2

- **Question:** Can change cr204, another high-risk payments change with a senior approval and a rollback plan, be deployed?

```query
?- deploy_approved(cr204).
expect: no
```

- **Answer:** No. It has no security sign-off, so it is security-blocked.
- **Reasoning chain:** Backward chaining from deploy_approved(cr204):
  1. Both rules for deploy_approved (inference rules 8 and 9) need release_ready(cr204).
  2. Inference rule 7 needs `not security_blocked(cr204)`. But modifies(cr204, payments) is a fact and security_signoff(cr204) is not, so inference rule 4 derives security_blocked(cr204). The sub-goal fails.
  3. The other conditions do hold: peer_reviewed(cr204) (tara and vikram, author nisha), build_verified(cr204) (88 ≥ 80), risk_cleared(cr204) (senior tara and rollback_plan(cr204)). BR4 is the only reason it is refused.
  4. release_ready(cr204) cannot be proved, so deploy_approved(cr204) cannot be proved. Answer: no.

#### Query 3

- **Question:** Which change requests are held this cycle?

```query
?- held(C).
expect: C = cr203; C = cr204; C = cr205
```

- **Answer:** cr203, cr204 and cr205.
- **Reasoning chain:** Inference rule 10 is applied to each release_requested(C) fact. A change is held when deploy_approved(C) cannot be derived:
  - cr203: coverage(cr203, 72) fails ge(72, 80), so build_verified fails. critical_vuln(cr203) makes it security_blocked by inference rule 3, and staging_verified(cr203) is missing. It is not release-ready, so it is held.
  - cr204: security-blocked by inference rule 4 (Query 2), so it is held.
  - cr205: release_ready(cr205) is derived (approvals by meera and arjun, author rohan; 83 ≥ 80; low risk by inference rule 5; staging verified). But release_window(cr205, wk47_fri) and freeze(wk47_fri) make inference rule 8 fail, and cr205 is not a hotfix, so inference rule 9 fails. It is held.
  - cr201, cr202 and cr206 are deploy-approved (Queries 1 and 4), so `not deploy_approved` fails for them.

#### Query 4

- **Question:** Which changes are approved for a window that is under a release freeze, and which window is it?

```query
?- deploy_approved(C), release_window(C, W), freeze(W).
expect: C = cr206, W = wk47_fri
```

- **Answer:** Only cr206, in the frozen window wk47_fri, because it is a sev1 hotfix.
- **Reasoning chain:** By forward chaining:
  1. author(cr206, arjun), approved_by(cr206, vikram) and approved_by(cr206, meera) give peer_reviewed(cr206) by inference rule 1.
  2. ci_passed(cr206), coverage(cr206, 81) and 81 ≥ 80 give build_verified(cr206) by inference rule 2.
  3. No critical vulnerability and no payments change, so `not security_blocked(cr206)` holds. risk(cr206, low) gives risk_cleared(cr206) by inference rule 5.
  4. With staging_verified(cr206), inference rule 7 gives release_ready(cr206).
  5. Inference rule 8 fails because freeze(wk47_fri) holds. hotfix_for(cr206, inc77) and severity(inc77, sev1) are facts, so inference rule 9 gives deploy_approved(cr206).
  6. release_window(cr206, wk47_fri) and freeze(wk47_fri) complete the query. cr205 is in the same window but is not deploy-approved (Query 3), so it is not an answer.

#### Query 5

- **Question:** Which on-call engineers must be paged to monitor a deployment, and for which change?

```query
?- page_on_call(C, P).
expect: C = cr202, P = rohan
```

- **Answer:** Rohan, the payments on-call engineer, must monitor cr202.
- **Reasoning chain:** Inference rule 11 needs deploy_approved(C) and risk(C, high).
  1. The deploy-approved changes are cr201, cr202 and cr206 (Queries 1, 3 and 4).
  2. Of these, only cr202 has risk(cr202, high). cr201 and cr206 are low risk, so the rule does not fire for them. cr204 is high risk but not deploy-approved.
  3. modifies(cr202, payments) and on_call(payments, rohan) give page_on_call(cr202, rohan). This chains five rules (1, 2, 6, 7, 8) before rule 11.

## B.4 Analyse

PL7 describes one unnamed change. To cover the six CRs in the knowledge base, every symbol and every rule would
need six copies. FOL7 handles all of them, and any future change, with a
single ∀c. Propositional logic also hides what a condition means. In PL1, TA is one yes/no symbol, while FOL1
spells out that there are two approvers with r1 ≠ r2 and that neither of them is the author. FOL2 keeps the actual
coverage figure, Coverage(c, n) with n ≥ 80, so raising the threshold to 85 means editing one constant instead of
redefining CV. Relations such as Modifies(c, s) and OnCall(s, p) let FOL11 work out who to page.

The knowledge base gets our release decisions right. It approves cr201 and
cr202 and holds cr203, cr204 and cr205, and Query 3 shows a different reason for each hold: cr203 has low coverage
and a critical vulnerability, cr204 has no security sign-off, and cr205 is booked into a freeze. It applies the sev1
hotfix exception to cr206 (Query 4) and names the engineer to page (Query 5). Forward chaining evaluates a whole
release batch at once, and backward chaining explains a single refusal, as in Query 2.

Some things are missing. There are no dates, so the knowledge base cannot work out whether a window falls inside a
freeze or whether a staging run is too old; freezes are typed in as facts. Risk level is given, not derived from
what the change touches. Under the closed-world assumption, a missing security_signoff fact blocks a release, which
is the safe outcome, but a missing critical_vuln fact (say, because the scan never ran) is read as "no
vulnerability". Discretionary approvals, staged rollouts and the content of a rollback plan are not modelled.

## B.5 Reflect

Putting this into our release pipeline would run into a few problems. The facts would have to come from the Git
platform, the CI server, the security scanner and the release calendar, and any of those can be slow, down or out
of sync. With the closed-world assumption, a scanner outage would look like a clean scan. The rules change
too. Coverage thresholds, freeze dates around client launches and the list of sensitive services get revised
every few months, and each revision has to go into the rule base as well as the policy document, or the two will
disagree.

The facts name engineers and approvers, and the derived facts show which services have blocked or vulnerable
changes, so access to the knowledge base should be restricted and logged. Scale is not a concern for
a batch of six changes, but with many services and teams the rules would need to be split per service and
re-evaluated incrementally on each pull-request event. Integration is the hardest part technically. Each tool has
its own API and data format, and all of them have to be mapped onto one set of change IDs, people and services.
Developers will also want to know why a change was held, so the derivation trace should be posted back on the pull
request.

The improvement I would make first is to pull the facts automatically from the source systems at decision time,
with an explicit "unknown" state for anything that could not be fetched, instead of entering them by hand. Stale or
hand-typed facts are the most likely way for this knowledge base to approve an unsafe change. With an "unknown"
state, a missing scan result blocks the release until the scan comes in, which closes the gap left by the
closed-world assumption.
