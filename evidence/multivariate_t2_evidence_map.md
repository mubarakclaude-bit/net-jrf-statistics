# Evidence map — Unit VIII, Partial and Multiple Correlation

## Scope
- Topic: `multivariate-t2` — first-order partial correlation, residual interpretation, multiple correlation and precision-matrix relation.
- No direct official June 2026 PYQ is claimed as an anchor. The lesson's questions are original exam-style practice items.

## Core claims
- First-order partial correlation: r12·3=(r12−r13r23)/sqrt[(1−r13²)(1−r23²)].
- Partial correlation is the correlation between residuals after regressing each target variable on the controlled variable(s).
- General multiple correlation: R²=r' RXX^-1 r; R is the non-negative square root.
- With two predictors: R²=(rY1²+rY2²−2rY1rY2r12)/(1−r12²).
- For a non-singular multivariate normal vector, partial correlation controlling all remaining coordinates is -Kij/sqrt(KiiKjj), K=Σ^-1.
- Zero partial correlation does not generally prove conditional independence without suitable assumptions.

## Independent arithmetic
- Worked partial example: (0.70−0.50×0.40)/sqrt[(1−0.50²)(1−0.40²)] ≈ 0.630.
- Worked multiple example: (0.60²+0.50²−2×0.60×0.50×0.20)/(1−0.20²) ≈ 0.5104; R≈0.7144.
- Uncorrelated predictors: 0.30²+0.40²=0.25; R=0.50.
- Guided partial example: (0.60−0.30×0.20)/sqrt[(1−0.30²)(1−0.20²)] ≈ 0.578.
- Guided multiple example: 0.29/0.91≈0.3187.

## Verification
- `verify_multivariate_t2.py` independently checks the numerical examples and mastery contracts.
- `lesson_multivariate_t2.py` checks stable identity, quiz linkage, difficulty/format/key balance and serializes the JSON files.
