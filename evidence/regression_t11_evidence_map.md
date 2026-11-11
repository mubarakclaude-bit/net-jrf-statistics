# Regression T11 evidence map — Dummy variables and qualitative regressors

- Scope: Unit VI, topic 6.11.
- k categories with an intercept use k−1 indicators; the omitted category is the reference group.
- Dummy-variable trap: the sum of all k indicators equals the intercept column.
- Interaction model: y=β₀+β₁x+δD+γDx; group 0 slope β₁, group 1 slope β₁+γ, difference at x is δ+γx.
- Exact worked example: y=5+2x+3D−0.5Dx; group 1 at x=4 predicts 14, baseline predicts 13.
- Log-linear dummy effect: exact percentage difference 100(exp(0.20)−1)≈22.14%.
- All numeric anchors and pool contracts are checked in verify_regression_t11.py.
- No June 2026 question is claimed as a direct dummy-variable PYQ.
- References: Wooldridge, Greene, Stock & Watson.
