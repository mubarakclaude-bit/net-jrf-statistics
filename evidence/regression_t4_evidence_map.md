# Evidence map — Unit VI, 6.4 R², adjusted R² and model comparison

## Repository-linked June 2026 practice cluster
The repository links ten variants to June 2026 Paper 2 Q9. The cluster includes:
- Adjusted R² calculation: n=50, k=5, R²=0.55; answer 0.51.
- Effect of adding an irrelevant regressor.
- Possibility of negative adjusted R².
- Definition of R².
- Other items on ANOVA/F, multicollinearity and residual variance.

The adjusted-R² items are related variants, not the direct official Q9 stem. The direct Q9 asks for the overall F statistic. This lesson keeps that distinction explicit.

## Mathematical claims
- R²=RegSS/TSS=1−RSS/TSS for OLS with an intercept.
- For nested OLS models on the same response and observations, adding predictors cannot increase optimized RSS; ordinary R² cannot decrease.
- Adjusted R²=1−[RSS/(n−k)]/[TSS/(n−1)].
- Equivalent formula: 1−(1−R²)(n−1)/(n−k), where k includes the intercept.
- Adjusted R² may decrease and may be negative.
- R² and adjusted R² are in-sample fit measures, not proofs of causality or out-of-sample predictive performance.

## Verification
The exact verifier uses Fraction arithmetic for adjusted-R² examples, including a negative adjusted-R² case. The mastery pool contract is checked for count, difficulty, format, balanced answer keys, numeric checks and multi-statement verdict checks.
