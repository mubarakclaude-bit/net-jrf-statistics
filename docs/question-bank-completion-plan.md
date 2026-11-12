# Question Bank completion plan

Baseline: `main`, audited 2026-11-12. This workstream is independent of lesson status and Vercel deployment.

## Acceptance contract

- Exactly 50 original June 2026 Paper 2 questions, IDs `j26-q01` through `j26-q50`.
- Exactly 10 distinct, usable variants linked to each original question by `srcQ` (500 total).
- Every original and variant assigned to the correct syllabus module and topic.
- Every question is standalone, has a complete stem, valid options/answer where applicable, and a self-contained explanation.
- Mathematical answers are independently recalculated; distractors are plausible and unambiguous.
- No accidental duplicate stems, explanation-as-stem records, truncated explanations, or mismatched source anchors.
- The Question Bank UI loads all banks, filters by module/source/format, and drills questions correctly.
- All changes are committed on this branch and validated before a PR to main. Do not deploy to Vercel as part of this workstream.

## Baseline findings

The nine existing variant files contain 481 records across 49 source-question anchors. Per-anchor counts are uneven:
- Below 10: Q1(8), Q2(9), Q5(9), Q11(6), Q14(6), Q20(9), Q23(9), Q25(9), Q27(9), Q29(9), Q30(9), Q34(9), Q38(4), Q41(2), Q42(9), Q44(9), Q45(9), Q48(7), and Q22(0).
- Above 10: Q12(14), Q15(12), Q21(20), Q39(14), Q40(17), Q49(13).
- Exactly 10: 25 source questions.
- Module bank files absent from the current seed set: sampling and design. Stochastic also has no variant file; first confirm whether any original June paper item is assigned to this module before creating an empty bank.

The numerical shortfall to 500 is 19, but exact per-question compliance requires addressing the underfilled anchors and reviewing overfilled anchors. Do not treat excess variants as substitutes for missing variants.

## Phases

1. **Audit controls** — retain this report, add a deterministic structural/count validator, map each source question to module/topic, and flag suspected content defects.
2. **Content repair** — fix misfiled source anchors, incomplete/truncated items, and add only concept-faithful variants to bring each anchor to ten. Review overfilled pools for duplicates and quality; do not delete sound content merely to force a count without recording disposition.
3. **Independent QA** — verify all answer keys and explanations, including numerical calculations and edge conditions. Review option quality and standalone context.
4. **Integration** — correct source-bank metadata and module filtering; test original PYQs and variants separately and together.
5. **Release readiness** — run repository checks and browser tests, summarize exact counts and outstanding caveats, then open a PR to main. Vercel deployment remains a separate explicit step.

## Known high-risk examples from the baseline sample

Initial spot checks found malformed content, so count completion alone is not acceptable:
- A probability Q6 variant has an explanation that appears to contain the next question's stem ("2. For a Poisson distribution...").
- A maths Q1 variant explanation contains inconsistent arithmetic (nullity formula text says 5 − 3 for a 10 × 10, rank-8 example).
- A non-parametric Q33 explanation begins with an unrelated next-question fragment.
- Some records appear to use a source question's module incorrectly; existing project notes already record misfilings. All 50 source anchors need a deliberate mapping review.

## Reporting rule

Report separate numbers for authored, structurally valid, mathematically verified, correctly mapped, integrated in repository, and deployed. Repository readiness must never be conflated with Vercel deployment.

## Execution status — 2026-11-12

### Phase 1 — audit controls: complete
- Dedicated branch: `question-bank/completion-audit`.
- Original PYQ source has question-level module IDs.
- Original questions are split into ten module-scoped qsets for correct filtering.
- Loader preserves item-level module assignment.
- Structural validator and test-fixture assertions added.

### Phase 2 — coverage and attribution: complete on this branch
- 50 original questions.
- 500 variants total.
- Exactly 10 variants for every original question.
- 10 module-scoped variant files, including Sampling.
- Zero duplicate variant IDs and zero source/module mismatches in the latest cross-check.

### Phase 3 — explanation integrity: first pass complete
- Repaired or rewrote 388 explanations/stems with contamination, truncation, missing context or incomplete calculations.
- All 500 records now pass the conservative explanation-fragment heuristic scan.
- This is not equivalent to independent verification of all 500 answer keys. A separate answer-calculation and distractor audit remains mandatory.

### Phase 4 — integration: code changes made; runtime verification pending
- Original question sets are split by module.
- Loader uses the correct module-scoped sets and preserves item-level metadata.
- Test fixture asserts exact counts, unique IDs and module attribution.
- Browser and learner-flow tests have not yet been executed in a local checkout.

### Phase 5 — release readiness: pending
- Draft PR: https://github.com/mubarakclaude-bit/net-jrf-statistics/pull/82
- Do not merge until independent answer verification and automated/browser tests pass.
- Vercel deployment is explicitly excluded.
