# Q2 TODO for SHREYANSH SHARMA (2025AG05772)

## AI-ASSISTED ASSIGNMENT — COMPLETE EXECUTION REQUIRED

Question 2 is an individual assignment based on the student's workplace or relevant industry domain. **AI assistance is explicitly encouraged and should be used extensively to complete this assignment accurately and thoroughly.**

The AI agent is expected to take an active role in understanding the assignment, analysing the provided reference materials, developing the knowledge base, generating logical representations, validating the answers, fixing errors, and producing the final PDF.

The objective is to produce a complete, logically consistent, well-structured, and academically sound submission. Do not simply generate placeholder content or superficial answers.

### Your files

- `q2/2025AG05772/answer.md` — Main answer document.
- `q2/2025AG05772/2025AG05772.pdf` — Final PDF generated in Step 8.

## Instructions for AI

Before starting, carefully inspect the repository and understand the complete assignment structure.

AI must:

- Read and understand all relevant reference files before writing anything.
- Follow the assignment requirements and formatting conventions.
- Use the provided example only as a structural reference, not copy its content.
- Develop a realistic workplace scenario relevant to the student's professional experience.
- Maintain consistency between business rules, propositional logic, predicate logic, facts, inference rules, and workplace queries.
- Ensure all logical representations are correct and meaningful.
- Execute the provided validation script and resolve every reported issue.
- Generate and verify the final PDF.

**Do not stop after generating the initial answer. Continue reviewing, validating, correcting, and improving the submission until all requirements are satisfied.**

## Steps

### 1. Read and understand the assignment

Read the following files completely:

- `q2/2025AG05772/answer.md`
- `q2/GUIDE.md`
- `q2/EXAMPLE.md`
- `q2/KB_SYNTAX.md`
- `README.md`

Understand the expected structure, logical notation, knowledge-base syntax, and validation requirements before proceeding.

### 2. B.1 — Student and workplace information

Fill in:

- Industry / Domain
- Organisation Type
- Instructor Prompt (write `None given` if no prompt was provided)

Verify that the student's name and ID are correct.

Use relevant workplace context available to the student. If essential information is unavailable, ask for clarification instead of inventing personal workplace experiences.

### 3. B.2 — Anchor

Identify a realistic, rule-governed business process from the student's workplace or an equivalent industry process.

Write approximately 150–250 words covering:

- Business context and purpose.
- People and systems involved.
- The process being governed.
- Why decisions must follow predefined rules.
- What happens when rules are violated.

The scenario should be realistic and sufficiently detailed to support the subsequent logical modelling.

### 4. B.3 — Apply

Complete every subsection carefully.

**A. Business Rules**

Write at least 10 meaningful business rules (BR1–BR10) in plain English.

**B. Propositional Logic**

- Define all propositions clearly.
- Translate each business rule into propositional logic (PL1–PL10).
- Ensure that the expressions accurately represent the original business rules.

**C. First-Order Predicate Logic**

- Define all predicates.
- Define variables and constants.
- Explain the meaning of each predicate.
- Rewrite all 10 business rules using first-order predicate logic (FOL1–FOL10).
- Use appropriate universal and existential quantifiers wherever required.

**D. Knowledge Base**

Create a complete KB block following the exact syntax specified in `q2/KB_SYNTAX.md`.

Requirements:

- At least 20 meaningful facts.
- At least 10 inference rules.
- No undefined predicates or inconsistent terminology.
- Rules must be logically meaningful and usable for inference.
- Facts and rules must support the workplace queries.

**E. Workplace Queries**

Create five realistic workplace queries.

For each query, provide:

- The question.
- The answer derived from the knowledge base.
- The reasoning chain showing which facts and inference rules lead to the conclusion.

Do not provide answers that cannot be derived from the defined knowledge base.

### 5. Validation and correction

Run the provided checker:

```bash
python q2/check_kb.py q2/2025AG05772/answer.md
```

AI must inspect the output carefully.

If validation fails:

1. Identify the exact issue.
2. Inspect the relevant section of `answer.md`.
3. Correct the underlying problem rather than bypassing the checker.
4. Re-run the validation script.
5. Repeat until all checks pass.

<escape>RESULT: PASS</escape> is mandatory before proceeding.

Do not modify the checker simply to force a successful result.

### 6. B.4 — Analyse

Write approximately 200–300 words analysing:

- Why predicate logic is more expressive than propositional logic in the selected scenario.
- How effectively the knowledge base represents the business process.
- What kinds of reasoning the knowledge base supports.
- What information or knowledge is missing.
- Limitations of the current logical representation.

Use examples from the developed knowledge base rather than generic theoretical explanations.

### 7. B.5 — Reflect

Write approximately 200–300 words discussing practical deployment constraints, including:

- Incomplete knowledge.
- Changing business rules.
- Data privacy and security.
- Scalability.
- Technology and integration limitations.

Recommend and justify the single most important improvement needed to make the proposed knowledge-based system more effective in a real workplace.

### 8. Generate the final PDF

Execute:

```bash
python q2/build_pdf.py q2/2025AG05772/answer.md
```

The output must be:

`q2/2025AG05772/2025AG05772.pdf`

After generating the PDF:

- Open and inspect the PDF.
- Check formatting, headings, page breaks, and missing content.
- Verify that logical expressions and KB syntax are displayed correctly.
- Ensure that no sections are missing or truncated.
- Confirm that the name and student ID appear correctly on the cover.

If any issue is identified, fix the Markdown source and regenerate the PDF.

### 9. Final quality review

Before considering the assignment complete, AI must perform a full review.

Verify that:

- Every required section is present.
- All minimum word and item counts are satisfied.
- All 10 business rules have corresponding PL and FOL representations.
- All predicates and constants are properly defined.
- The KB contains at least 20 facts and 10 inference rules.
- All five queries have valid answers and reasoning chains.
- There are no logical contradictions or undefined references.
- The checker returns `RESULT: PASS`.
- The final PDF matches the latest Markdown version.

### 10. Final handover

The final deliverables are:

- `q2/2025AG05772/answer.md`
- `q2/2025AG05772/2025AG05772.pdf`

If the final submission ZIP is available, inspect it and verify that:

- `2025AG05772.pdf` is included.
- It is the latest generated version.
- It displays the correct name and student ID.

Refer to `README.md` §1 for the complete submission instructions.

---

## Important execution instructions for AI

Treat this as an end-to-end assignment completion task, not merely a text-generation exercise.

Do not skip sections, invent unsupported workplace details, produce disconnected logical expressions, or leave validation for the student to perform manually.

**AI is expected to actively create, analyse, validate, debug, and refine the assignment until the complete submission is ready for review and handover.**

The final output should be academically appropriate, technically correct, internally consistent, and ready for submission after the student's review.