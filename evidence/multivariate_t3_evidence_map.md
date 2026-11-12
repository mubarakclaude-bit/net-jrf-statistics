# Evidence map — Multivariate T3: Principal Component Analysis

## Scope
UGC NET Statistics Unit VIII, Multivariate Analysis. Catalog topic: multivariate-t3. Primary PYQ anchor: June 2026 Paper 2 Q2. Scope: PCA optimisation, covariance/correlation matrices, eigenpairs, scores, explained variance, repeated eigenvalues and interpretation.

## Claim-to-lesson map
| Claim | Lesson scene | Independent check |
|---|---|---|
| First PC maximises aᵀΣa subject to aᵀa=1 | s2 | Rayleigh quotient/eigenvector argument |
| PC score variance equals its eigenvalue | s2 | Exact substitution |
| June 2026 Q2 eigenvalues are 2, 1/2, 1/2 | s3 | Exact rational matrix-vector checks |
| First direction is (1,1,1)/√3 | s3 | Exact multiplication |
| PC1 explains 2/3 = 66.67% | s3 | Trace and eigenvalue sum |
| [[4,2],[2,4]] has eigenvalues 6,2 | s5 | Exact characteristic roots |
| Correlation matrix [[1,.6],[.6,1]] has eigenvalues 1.6,.4 | s9 | Sum/difference eigenvectors |
| Correlation PCA eigenvalues sum to p | s6 | Trace identity |

## PYQ bank repair
Five PCA items with srcQ=2 were misfiled in the time-series variant bank. They now live in the multivariate variant bank under their original IDs (j26v-q03-01…05), preserving historical attempt linkage. The time-series bank retains only AR/Yule–Walker material.

## Verification
Run `python verify_multivariate_t3.py`. Exact fractions check the June 2026 matrix and worked examples. Structural checks cover lesson-to-pool wiring, 20-item mastery composition, difficulty distribution, numerical checks and multi-statement verdicts.

## References
- Johnson & Wichern, *Applied Multivariate Statistical Analysis*, PCA chapter.
- James et al., *An Introduction to Statistical Learning*, Chapter 12: https://www.statlearning.com/
- Penn State STAT 505: https://online.stat.psu.edu/stat505/

## Limitations
PCA is not causal analysis; uncorrelated components are not generally independent. Mastery items are original practice, not official PYQs.
