# Question Bank audit findings

Audit date: 2026-11-12  
Baseline: repository `main`; remediation branch: `question-bank/completion-audit`.

## Current structural result

<badge>Current branch, not yet merged</badge>

- Original June 2026 Paper 2: 50/50 questions.
- Variant banks: 10 module-scoped files, 500 records total.
- Per-anchor coverage: exactly 10 variants for each of the 50 original questions.
- Variant IDs: unique in the latest independent cross-check.
- Source/module attribution: 0 mismatches in the latest cross-check.
- Declared bank counts agree with item counts.
- Original PYQ master source now has an explicit moduleId per question. It is retained as source data and excluded from generated qsets; ten module-specific original PYQ qsets are generated instead.
- The app loader preserves item-level moduleId where present.
- Sampling now has its own variant-bank seed file. No original June 2026 questions were classified to Design or Stochastic in the current 50-question mapping; this does not mean those modules need no practice banks from other papers.

The latest cross-check found 500 variants and exactly ten for every source question. This is structural coverage, not a mathematical correctness certification.

## Attribution repair

The earlier cross-check identified 158 suspected module/source mismatches. The remediation pass used the actual variant stem and concept to repair source anchors and refile records. The latest comparison against the canonical 50-question mapping found zero remaining file/module mismatches.

Examples repaired:
- Multivariate-normal independence, Wishart and conditional-distribution variants moved out of Probability.
- PCA variants moved from Mathematics to Multivariate.
- Hotelling's T-squared variants moved from Inference to Multivariate.
- Horvitz–Thompson variants moved from Inference to Sampling.
- Regression and matrix algebra variants separated from R Programming.
- Jensen/Markov/Chebyshev variants moved to their probability anchor.
- Rank-correlation and goodness-of-fit variants moved to Non-parametric methods.
- The Q41 exponential order-statistics variants moved to Probability.

## Content-quality audit — still in progress

A conservative automated scan flagged **291 of 500 records** for at least one review signal:
- explanation begins with a numbered fragment that may be the next question;
- explanation references another question or a learner's paper;
- explanation appears truncated or ends mid-calculation;
- explanation is unusually short.

These are review flags, not 291 confirmed errors. Some concise explanations are mathematically sufficient. However, spot checks confirmed genuine defects, including explanations replaced by the next question's stem, incomplete equations, and context-dependent references. The following are examples, not an exhaustive list:
- Probability Q6 variants include explanations beginning with the next question.
- Mathematics Q1 contains an inconsistent rank/nullity arithmetic explanation.
- Regression Q5 and Q15 contain several explanation fragments.
- Inference Q30 and Q39 contain explanation fragments and unrelated question summaries.
- Official Statistics and Sampling also contain explanation fragments.
- Some items refer to "question 1", "Q32", "your paper", or a prior context not visible to a learner using the bank independently.

The new variants authored in this remediation pass were checked for their arithmetic and answer letters. The Q40 bank was replaced with ten self-contained exponential-estimation variants; Q41's two existing items were repaired and eight new order-statistics variants added. A mixed-Poisson answer-key correction was also made.

**Do not mark the bank mathematically verified until all 500 records have been reviewed.** Structural coverage and content correctness are separate statuses.

## Automated controls added

- `tools/audit-question-banks.js` reports source coverage, duplicate IDs, missing fields, module mismatch, and likely explanation contamination.
- `npm run audit:question-bank` runs the validator.
- `.github/workflows/question-bank-audit.yml` runs the structural validator for pushes to the `question-bank/**` branch family.
- `test.js` asserts 50 module-scoped original questions, 500 variants, exactly ten variants per source question, unique IDs, and correct module assignment.

The available GitHub status check currently shows the Vercel rate-limit failure; no successful execution of the new audit workflow has yet been confirmed through the connected GitHub status interface. The repository test suite also has not yet been run in a local checkout during this session.

## Remaining work

1. Review and repair the 291 flagged explanations/stems; distinguish false positives from actual contamination.
2. Independently verify all 500 answer keys and calculations, with particular attention to numerical, multi-statement, matching and order formats.
3. Run `npm run audit:question-bank`, `npm test`, and the hosted/browser acceptance tests in a checkout.
4. Confirm Question Bank module filters, source filters and drill flows with the generated module-scoped qsets.
5. Open/update the PR to `main) only when the checks are green. Keep Vercel deployment separate.
