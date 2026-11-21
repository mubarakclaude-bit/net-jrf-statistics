# Independent Probability and Regression Mathematical Audit — 14 November 2026

## Base and ownership

- Repository: `mubarakclaude-bit/net-jrf-statistics`
- Base: `main` at `b78be4bf68a02029d4c906a9afa760eb54aec40f`
- Branch: `audit/probability-regression-2026-11-14`
- Scope: Paper 2 only.
- Probability T1 is excluded from edits because draft PR #93 already owns `seed/lesson_pr1.json` and its verifier.
- Statistical Inference PR #94 and Time Series PR #95 are not modified.
- Regression T1–T15 has no overlapping open mathematical-audit PR in the repository at this base.

## Review coverage

- Probability: T2–T13 (12 lesson JSON files), including worked, completion, guided and selected theory scenes; all 12 corresponding mastery pools (240 items) were inspected.
- Regression: T1–T15 (15 lesson JSON files), including all worked, completion and guided scenes; all 15 mastery pools were retrieved and numerical/multi-statement items were targeted for review.
- The audit independently recalculated the numerical examples listed in the verifier and checked assumptions, degrees of freedom, conditional support, parameterisation, and interpretation.
- This is a module-scoped second-pass audit, not certification of every Paper 2 lesson or every Regression mastery item. The unreviewed Regression single-choice items and the remaining Paper 2 modules still require review.

## Confirmed findings and corrections

1. **Probability T7 — Chebyshev sharpness domain.** `seed/probability_t7_mastery.json`, item `pr-t7-m-14`, said the three-point extremal distribution attains Chebyshev's bound at an unrestricted “given k”. Its central mass is (1-1/k^2), which is non-negative only for (k\geq1). For (0<k<1), the bound (1/k^2) exceeds one and is vacuous. The stem and explanation now state (k\geq1).
2. **Probability T7 — positivity assumption.** The tail-integral/Jensen question used (E(1/X)) and (E(\log X)) while describing X only as non-negative. The lesson and mastery stem now require (X>0) almost surely.
3. **Probability T13 — missing sampling-distribution conditions.** The June 2026 Q46-derived statements applied the arcsine law at (n=3) and the uniform law at (n=4) without stating the required bivariate-normal, (\rho=0) null condition. The lesson stem and mastery item `pr-t13-m-07` now state the population model and the null condition for C and D. The high-correlation skew statement is also made precise in terms of population (\rho\).
4. **Probability T13 — incorrect two-sided tail probability.** Mastery item `pr-t13-m-19` stated (P(|r|\geq0.97)=0.06) under (U(-1,1)). Since the density is (1/2), the correct probability is (1-0.97=0.03). The corrected option and explanation now state that this narrowly rejects (\rho=0) at 5% but does not establish that the population correlation is near 0.97.
5. **Regression T2 — omitted covariance assumptions.** Three BLUE mastery stems omitted the uncorrelated/spherical-error condition needed for the stated variance/BLUE calculations. The stems now state the relevant error covariance assumption.

## Independent verification

- Added `verify_probability_regression_math.py`, a standard-library `unittest` verifier with arithmetic regression checks for the corrected findings and the independently recalculated Probability/Regression worked examples.
- The verifier also checks that the corrected assumptions are present in the learner-facing lesson and mastery content.
- GitHub Actions is the authoritative repository-level validation after the draft PR is opened. No claim of CI success or deployment is made in this report.

## Safety and remaining work

- No Paper 1 content, application code, shared manifest, workflow, or infrastructure was changed.
- No Claude-owned files, databases, artifacts, or infrastructure were used.
- No merge or Vercel deployment is authorised or performed.
- Keep the PR in draft until CI passes and the remaining mastery items and Paper 2 modules have been audited.
