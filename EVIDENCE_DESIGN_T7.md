# Evidence map — Unit III, Design of Experiments, Topic 3B.7

- Topic: design-t7, Missing plot technique.
- No official PYQ is claimed; mastery items are original practice.
- One missing value in RBD: x̂=(tB+rT−G)/[(t−1)(r−1)], where t treatments, r blocks, B affected block total, T affected treatment total and G grand total; all totals exclude x.
- One missing value in Latin square: x̂=[p(R+C+T)−2G]/[(p−1)(p−2)], where p is square order and R,C,T,G exclude x.
- After estimation, insert x, recompute the relevant ANOVA components and reduce error df by one.
- Multiple missing observations generally require simultaneous or iterative estimation; the one-missing formulas are not applied blindly.
- Classical estimates rely on the design model and may be questionable under informative missingness.
- verify_design_t7.py checks both worked examples and df adjustment; lesson_design_t7.py checks scene and mastery contracts.

- Boundary: the classical Latin-square single-missing-value estimator requires p≥3. At p=2, its denominator and residual error degrees of freedom are zero; the saturated 2×2 layout cannot estimate the missing value by this method.
