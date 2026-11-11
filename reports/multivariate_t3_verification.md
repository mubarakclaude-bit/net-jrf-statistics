# Verification report — Principal Component Analysis (Unit VIII t3)

## June 2026 Paper 2 Q2
- The 3×3 equicorrelation matrix with off-diagonal correlation 1/2 has eigenvalues 2, 1/2 and 1/2.
- The first principal direction is proportional to (1,1,1)′; its unit vector is (1,1,1)′/√3.
- The total variance is the trace, 3. PC1 explains 2/3 = 66.67% of total variance.
- The repeated eigenvalue 1/2 means the remaining two-dimensional eigenspace has no unique preferred orthonormal basis.

## Independent worked-example checks
- Covariance matrix [[4,2],[2,4]] has eigenvalues 6 and 2; PC1 explains 6/8 = 75%.
- Correlation matrix [[1,0.6],[0.6,1]] has eigenvalues 1.6 and 0.4.
- Exact rational eigenvector and trace checks are implemented in `verify_multivariate_t3.py`.

## Content and provenance
- Mastery pool: 20 items; 6 easy, 10 moderate, 4 hard.
- Formats: 12 single-choice, 5 numeric, 3 multi-statement; answer keys balanced A–D.
- Five June 2026 Q2-derived PCA variants were moved from the time-series variant bank to the multivariate variant bank. They remain labelled variants, not additional official questions.
- Original mastery items are practice questions, not official PYQs.

## Verification
- Structural, exact-arithmetic and mastery-pool assertions are encoded in `verify_multivariate_t3.py` and `lesson_multivariate_t3.py`.
- Consolidated repository validation and browser/acceptance checks are tracked on [PR #39](https://github.com/mubarakclaude-bit/net-jrf-statistics/pull/39).
