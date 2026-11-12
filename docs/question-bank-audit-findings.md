# Question Bank audit findings

Audit date: 2026-11-12  
Baseline: repository `main`; remediation branch: `question-bank/completion-audit`.

## Confirmed repository facts

- The original June 2026 Paper 2 file contains 50 records.
- Nine variant-bank seed files exist and contain 481 records in total.
- The 481 records cover 49 source-question numbers; Q22 has no variants.
- Only 25 of the 50 source-question numbers have exactly ten variants.
- Eighteen anchors are below ten, including Q22 at zero; six anchors exceed ten.
- The total count is not a reliable completion measure because overfilled anchors mask underfilled anchors.

## Attribution audit

A cross-check of each variant file's declared `moduleId` against the syllabus module associated with its `srcQ` found 158 records whose current file/module assignment does not agree with the original question's subject. Treat these as suspected misattributions until each variant's actual stem is checked; some variants also have incorrect `srcQ` values, so changing the file alone is not sufficient.

Examples observed:
- Multivariate-normal independence, Wishart and conditional-distribution variants occur in the Probability file.
- PCA variants for Q2 occur in Mathematics rather than Multivariate.
- Hotelling's T-squared variants for Q4 occur in Inference rather than Multivariate.
- Horvitz–Thompson variants for Q8 occur in Inference rather than Sampling.
- Matrix-algebra variants for Q21 and R-programming variants are mixed in the R Programming bank.
- Jensen/Markov/Chebyshev variants are tagged as Q30 even though their concept is Q31.
- Rank-correlation variants for Q35 occur in Mathematics rather than Non-parametric methods.
- Exponential order-statistics variants are present in Non-parametric although Q41 is mapped to Probability.

The master paper now carries an explicit `moduleId` on each original item, and the app loader preserves an item's own module assignment when present. This fixes the known parent-document attribution defect for original PYQs. It does not automatically repair the variant banks.

## Content-quality defects found by spot check

The following examples are sufficient to reject a count-only completion claim:
- Probability Q6 variant `j26v-q06-01` has an explanation that appears to be the next question's stem.
- Mathematics Q1 variant `j26v-q01-01` has a 10x10 rank-8 example but an explanation using inconsistent values.
- Non-parametric Q33 variant `j26v-q33-01` begins its explanation with a fragment of another question.
- Several variants have incomplete explanations, context-dependent references such as "in question 1", or question numbering fragments.

All 481 records require a structured content audit; examples above are not an exhaustive defect list.

## Next remediation actions

1. Build a per-record canonical source-question and syllabus-module manifest using the actual stem/concept, not the current `srcQ` or file name alone.
2. Correct mis-tagged source anchors and move each record into the correct module bank.
3. Repair malformed stems/explanations and verify every key independently.
4. Generate only the missing variants needed for exactly ten usable variants per original question.
5. Run the structural validator and app/browser regression tests.
6. Keep authored, structurally valid, mathematically verified, correctly mapped and production-deployed counts separate.

## Important mapping caveat

The master-paper module mapping is an editorial classification based on the subject matter of each question. Borderline cross-unit questions (for example, rank correlation, goodness-of-fit and order statistics) should be reviewed against the official Statistics syllabus before final acceptance.
