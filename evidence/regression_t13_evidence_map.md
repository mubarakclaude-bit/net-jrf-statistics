# Regression T13 evidence map — Restricted regression

- Scope: Unit VI, topic 6.13.
- Linear restrictions: Rβ=r; independent restriction count q=rank(R).
- Restricted LS: minimise RSS subject to Rβ=r; RSS_R≥RSS_U.
- Extra-sum F: [(RSS_R−RSS_U)/q]/[RSS_U/(n−k)].
- One restriction: classical F=t².
- Exact restrictions are fixed equalities; stochastic restrictions allow a random deviation with covariance Ω; mixed estimation combines sample and external information.
- Exact worked anchors: β̂=(2,3), β₁+β₂=4, X′X=I gives β̂_R=(1.5,2.5); F examples yield 2 and 1.2.
- All exact anchors and mastery contracts are checked in verify_regression_t13.py.
- No June 2026 question is claimed as a direct restricted-regression PYQ.
- References: Wooldridge, Greene, Johnston & DiNardo.
