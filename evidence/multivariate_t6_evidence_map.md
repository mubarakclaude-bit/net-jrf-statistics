# Evidence map — Module 8.6 Canonical correlation

## Official anchor
June 2026 Paper 2 Q20 (`j26-q20`) in `seed/pyq_j26_full.json`. Both within-set covariance blocks are identity matrices and the cross block is B=[[0.5,0],[0.3,0.4]]. Thus canonical correlations are singular values of B. B′B=[[0.34,0.12],[0.12,0.16]], trace .50 and determinant .04; eigenvalues .40 and .10. Maximum correlation √.40=.63246, official option B (0.63).

## Theory references
- Johnson & Wichern, Applied Multivariate Statistical Analysis, canonical correlation analysis.
- Rencher & Christensen, Methods of Multivariate Analysis, canonical roots and variates.
- Penn State STAT 505: https://online.stat.psu.edu/stat505/.

## Checks
C=Σ₁₁⁻¹/²Σ₁₂Σ₂₂⁻¹/²; singular values of C are canonical correlations; eigenvalues of C′C are squared roots; maximum root count is min(p,q). Guided diagonal example gives .5 and 1/3.

## Scope boundary
Covers canonical variates, covariance partition, standardisation, singular values and root interpretation. Wilks' lambda and sequential-root significance tests are outside this lesson's catalog scope.