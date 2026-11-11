# Evidence map — Unit VI, 6.5 Multicollinearity

## June 2026 anchor
Repository item `j26-q38`: “Which ... is not a consequence of near multicollinearity on the performance of ordinary least squares estimator?” Official answer C, “Estimates are biased”; response sheet Q74 records the learner marked B. Source: `seed/pyq_j26_full.json`.

Four linked variants are preserved in `seed/regression_pyq_variants.json`: bias source, heteroscedasticity, principal component regression, and inference impact. They remain practice variants and are not relabelled as official PYQs.

## Core claims and evidence
- OLS variance formula: Var(β̂|X)=σ²(X′X)⁻¹ under spherical errors and full rank.
- Exact linear dependence makes X′X singular; near dependence can make the inverse poorly conditioned.
- VIFⱼ=1/(1−Rⱼ²). Exact checks include R²=.80 → VIF=5 and R²=.90 → VIF=10.
- Under exogeneity, multicollinearity alone does not bias OLS; it primarily reduces precision.
- High overall R² can coexist with weak individual t statistics.

## Assessment map
| Skill | Scenes | Mastery items |
|---|---|---|
| Foundations and bias/precision distinction | s0–s1 | 1–6 |
| Perfect versus near collinearity | s2–s3 | 7–10, 17 |
| Standard errors, t tests and VIF | s4–s9 | 11–15, 18, 20 |
| Remedies and prediction versus interpretation | s10–s12 | 16, 19 |
| Negation-style June 2026 anchor | s10–s13 | 17 |

All 20 mastery items are original practice questions, not official PYQs.
