# Regression T12 evidence map — Logistic regression

- Scope: Unit VI, topic 6.12.
- Logit: log[p/(1−p)]=η=X′β; inverse logit p=1/(1+exp(−η)).
- Odds: p/(1−p); odds ratio for a one-unit increase is exp(β).
- Simple-logit marginal effect: βp(1−p), evaluated at the covariate value.
- Exact anchors: η=1 gives p≈0.7311; η=−1 gives p≈0.2689; p=0.1 with doubled odds gives 2/11≈0.1818.
- At p=0.5 and β=2, marginal effect is 0.5; at p=0.2 and β=1 it is 0.16.
- Log-linear dummy coefficient 0.20 gives exact percentage difference 100(exp(0.20)−1)≈22.14%.
- All numerical anchors and pool contracts are checked in verify_regression_t12.py.
- No June 2026 question is claimed as a direct logistic-regression PYQ.
- References: Wooldridge, Greene and Agresti.
