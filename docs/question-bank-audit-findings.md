# Question Bank audit findings

Audit date: 2026-11-12  
Remediation branch: `question-bank/completion-audit`  
Draft PR: https://github.com/mubarakclaude-bit/net-jrf-statistics/pull/82

## Current structural result

- Original June 2026 Paper 2: 50/50 questions.
- Variant banks: 10 module-scoped files, 500 records total.
- Per-anchor coverage: exactly 10 variants for each of the 50 original questions.
- Variant IDs: no duplicates in the latest independent cross-check.
- Source/module attribution: zero mismatches in the latest cross-check.
- Declared bank counts agree with item counts.
- Original PYQ master source has an explicit `moduleId` on each item and is retained as source data, not published as one all-inference qset. Ten module-specific original PYQ qsets are generated instead.
- The app loader preserves item-level module attribution.
- Sampling has its own variant-bank seed file. No original June 2026 questions were classified to Design or Stochastic in this 50-question paper; future-paper practice for those modules is a separate scope.

## Content-quality remediation

A conservative scan initially flagged 291 of 500 records for numbered explanation fragments, cross-question references, suspicious truncation or unusually short explanations. After manual review and repairs, the latest scan flags **zero** records.

**388 explanations or stems were rewritten or repaired** across Probability, Mathematics, Time Series, Inference, Regression, Multivariate Analysis, Official Statistics, R Programming, Non-parametric Methods and Sampling. The other 112 records did not trigger the heuristic scan and were retained after the structural and context scan.

Specific fixes include:
- Repairing malformed question-to-question explanation fragments across all ten module banks.
- Replacing the Q40 exponential-estimation pool with ten self-contained variants.
- Repairing and expanding Q41 exponential order-statistics practice.
- Correcting the Q18-10 ARMA invertibility answer key: the stated MA polynomial has roots outside the unit circle, so the process is stationary and invertible.
- Correcting the mixed-Poisson variance answer key in Q45-10.
- Repairing R-programming source anchors and rewriting its explanations.
- Correcting module attribution for PCA, Wishart, Hotelling's T², Horvitz–Thompson, rank correlation, goodness-of-fit and other mixed concepts.

The latest structural cross-check reports:
- 500 variants.
- Exactly ten per source question.
- Zero duplicate IDs.
- Zero module mismatches.
- No missing required fields or invalid answer letters.
- Zero explanation-fragment heuristic flags.

**Important limitation:** a zero heuristic flag is not proof that all 500 mathematical answers, distractors and explanations are correct. Independent answer-key verification remains outstanding and is a merge blocker. The latest content pass checked the new/rewritten calculations, but not every retained original variant has yet received a separate independent derivation.

## Automated controls added

- `tools/audit-question-banks.js` reports source coverage, duplicate IDs, missing fields, module mismatch and likely explanation contamination.
- `npm run audit:question-bank` runs the validator.
- `.github/workflows/question-bank-audit.yml` is configured for pushes to question-bank branches and pull requests.
- `test.js` asserts 50 module-scoped original questions, 500 variants, exactly ten variants per source question, unique IDs and correct module assignment.

## Verification status

- Independent structural cross-check: passed in this session.
- Local execution of `npm run audit:question-bank`: not confirmed.
- `npm test` / browser acceptance tests: not yet run in a local checkout.
- New GitHub Actions workflow: no successful run confirmed through the connected GitHub workflow interface.
- Vercel deployment: not attempted.

## Remaining work

1. Independently verify every retained answer key and explanation, including numerical arithmetic and all formula conditions.
2. Verify distractors, ambiguity, topic fit and standalone wording for every question.
3. Run `npm run audit:question-bank`, `npm test` and browser/hosted acceptance tests in a checkout.
4. Verify module/source/format filters and drill behaviour against the generated qsets.
5. Update PR #82 and remove draft status only when checks are green. Do not merge or deploy to Vercel without explicit release approval.
