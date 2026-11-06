# Learner experience, accessibility and assessment standard

Version 1.0. This standard supplements SPEC.md; it does not weaken its mathematical, JRF or schema requirements.

## Product promise

A learner with a genuine prerequisite gap must be able to start, understand what is being taught, repair the gap, and progress toward independent UGC NET/JRF-level problem solving. Simplicity means removing avoidable cognitive friction, not removing mathematical depth.

The product serves at least three starting states:
1. **Rusty returner:** studied the subject before, but definitions, notation or algebra have faded.
2. **Uneven foundation:** understands some prerequisites but has specific gaps.
3. **JRF-ready learner:** wants precise conditions, proofs, edge cases, discriminating questions and advanced extensions.

A lesson must not assume that every learner begins at state 3. It must also not trap state 3 in a shallow treatment.

## Required learning path

For each major objective, the author and reviewers should be able to trace:

`diagnostic → prerequisite repair → intuition/concrete example → formal definition → derivation → worked example → fading support → independent transfer → retrieval → exam-style assessment`

- Diagnose specific prerequisites; do not use a discouraging pass/fail gate for the lesson.
- For each shaky prerequisite, provide a useful refresh that actually teaches the missing tool.
- Introduce purpose and plain-language meaning before dense notation.
- Define every symbol and name each theorem or method when first used.
- Carry algebraic and logical steps. Never hide a material step behind “clearly”, “obviously” or “recall”.
- Use a worked example, then completion, then guided transfer with progressively lighter hints.
- Include a core route and clearly labelled optional JRF extension where appropriate. Optional must not mean mathematically careless or irrelevant.
- Give each teaching scene a useful self-check and feedback that explains the reasoning.

## Three specialised review agents

### A. Prerequisite and learner-accessibility auditor

This reviewer must be independent of the author and ask:
- Can a learner who has forgotten the assumed prerequisite still enter the lesson?
- Does the foundation diagnostic test exactly the tools later used?
- Does each shaky answer lead to a self-contained, correct refresh, not merely a link or a repeated definition?
- Is there a bridge from words and concrete examples to symbols?
- Are notation, vocabulary, algebra, diagrams and instructions explained at the point of need?
- Are there unexplained jumps, hidden prerequisites, overloaded paragraphs, ambiguous pronouns or excessive simultaneous concepts?
- Can the learner tell what is core, what is optional JRF depth, and what they should be able to do after each section?
- Do hints support thinking without revealing the answer?
- Is feedback corrective and respectful, with a route to repair a misconception?
- Does the lesson remain rigorous enough for JRF after accessibility improvements?

Test at least two reading paths: a rusty learner who uses the refreshes, and a confident learner who takes the core route and optional extension. Record exact scene paths and examples. Do not merely score “readability”.

### B. Visual, chart and interactive-learning auditor

Inspect every visual asset, chart, graph, flow diagram, table, simulation and interactive control in its rendered form where the tools allow. Check:
- The visual answers a named learning question and is explained in adjacent prose.
- Axes, scales, units, legends, categories, symbols, labels and reference values are correct and readable.
- Geometry and plotted values agree with the verified mathematics and data.
- No misleading truncation, scale, colour-only encoding, clipping, overlap, hidden controls or unexplained animation.
- A flow diagram has a logically valid direction, complete branches, correct labels and a meaningful start/end.
- A chart is not decorative; the learner is told what to notice and why it matters.
- Interactive controls have sensible ranges, defaults, units, keyboard/focus affordances where supported, and stable outputs at boundaries.
- Every control combination avoids NaN, Infinity, undefined, stale values and broken SVG/HTML.
- The visual remains useful on a narrow/mobile viewport and does not replace the explanation with an inaccessible picture.
- If a visual cannot be rendered or tested, mark it unverified; do not claim visual QA passed.

Prefer a small number of well-chosen, reusable, mathematically faithful visuals over decorative diagrams. Reuse registered visualisations from SPEC.md when they genuinely fit. Any new visualisation must be registered, validated and tested under the existing app contract.

### C. Question-bank and mock-exam auditor

Review the generated mastery pool and the wider bank/mock experience, not just the item count:
- Every objective has appropriate assessment coverage; every relevant PYQ variant is mapped or explicitly excluded with a reason.
- Preserve the exact PYQ stem, source/year/variant provenance and official key separately from the learner's marked answer. Flag uncertain extraction.
- Each item is standalone, unambiguous, has exactly one defensible key for its stated task, plausible distractors and a teaching explanation.
- Numericals are recalculated independently and have a useful sanity/check line. Multi-statement items have complete A-D verdicts.
- Check format mix, topic coverage, difficulty calibration, key distribution, duplicate/near-duplicate items, accidental clues and answer leakage.
- Distinguish mastery pools, practice-bank items, PYQs, generated variants and mock items. Never label generated variants as actual PYQs.
- Check that mock allocation respects the intended paper/module mark distribution and format mix, and report any missing-content redistribution to the learner.
- Timed mocks must be scorable under their stated conditions. Write-in numerical items may be excluded from timed mocks only if the product clearly routes learners to the question bank for those items.
- Verify unanswered questions, navigation, answer hiding before submit, review after submit, timing, scoring, history, weak-module/wrong-only modes and question-bank links.
- Never imply that a platform pass threshold is an official NTA/JRF cut-off unless a verified official source supports that statement.

## Existing lessons and product behaviour are reference material

Before reviewing a new lesson, compare it with:
- `SPEC.md` as the binding structural and authoring standard.
- `review/lesson-4-1-for-model-review.md` and the corresponding current `seed/lesson_t1.json` as a detailed example of a returning-learner path, careful mathematical revision, prerequisite scaffolding, optional JRF extension and findings-based review.
- At least two other relevant, approved lessons from the same or adjacent module, selected by the orchestrator. Inspect their actual JSON, not only their titles.
- `src/52-bank.js` and `src/54-mock.js` as the current question-bank and mock-exam behaviour contract.
- The relevant PYQ source/variant files and `seed/meta_syllabus.json`.

Use exemplars to identify proven patterns and regressions. Do not blindly copy their prose, structure, errors, question stems or outdated versions. A previous lesson is evidence of an implementation pattern, not proof of mathematical correctness. If exemplar content conflicts with SPEC.md, the canonical syllabus, a verified source or a newer review finding, report the conflict and follow the higher-authority source.

## LLM-assisted learning requirements

AI assistance is a learning aid, not an answer-key authority. Where an LLM feature exists or is proposed, review:
- It is grounded in the current lesson, approved notes, formulas and relevant question context.
- It can explain at multiple levels: intuition, step-by-step derivation, exam method and JRF extension.
- It offers graduated hints, asks the learner to attempt a step, diagnoses a specific misconception and adapts the explanation without silently changing the mathematics.
- It distinguishes a source-backed fact from an inference and says when context is insufficient.
- It never fabricates PYQs, official keys, references, syllabus claims, formulas or citations.
- It does not expose hidden answer keys before submission in a mock or mastery assessment.
- It does not provide misleading certainty when a question is ambiguous or extracted incompletely.
- It protects learner data; no personal marks or identifiable data are sent to an external provider without an approved data-minimisation and consent design.
- Model/provider, prompt version, source context, failure behaviour and usage limits are documented.
- The product remains usable when the LLM is unavailable; deterministic lessons, bank and mocks must still work.

No external LLM API, credential, autonomous agent runtime or learner-data transfer is authorised by this standard. Those require separate explicit design and approval.

## Review evidence and decisions

Each reviewer must return findings, not a wholesale rewrite. Every finding includes:
- exact file and JSON path / scene / item / visual ID;
- severity: Critical, High, Medium or Low;
- concrete learner or correctness impact;
- evidence or reproduction steps;
- a specific correction or test.

A review must report what it could not inspect. “Looks good”, “easy to understand” and “visuals are fine” are not evidence.

Release is blocked by any Critical or High finding, any unverified central formula/key, missing syllabus/PYQ mapping, broken required interaction, or untested visual claimed as passed. Medium findings need resolution or explicit human acceptance. The author cannot approve their own work.
