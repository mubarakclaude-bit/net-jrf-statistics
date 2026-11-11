# Evidence map — Module 8.4 Hotelling’s T²

## Primary examination anchor
- Source: `seed/pyq_j26_full.json`, item `j26-q04` (June 2026 Paper 2 Q4; response sheet Q113).
- Stem: one-sample test of H0: μ=(3.5,2.5)' using three bivariate observations (1,2)', (4,4)', (4,3)'.
- Official keyed option: C (7.0); candidate marked B.

## Independent arithmetic
- x̄=(3,3)' and d=(-1/2,1/2)'.
- With divisor n−1=2: S=[[3,3/2],[3/2,1]].
- det(S)=3−9/4=3/4.
- S⁻¹=[[4/3,−2],[−2,4]].
- S⁻¹d=(-5/3,3)'.
- d'S⁻¹d=5/6+3/2=7/3.
- T²=n d'S⁻¹d=3×7/3=7.
- F conversion: (3−2)/(2(3−1))×7=7/4=1.75, df=(2,1).

## Scope and claims
- One-sample T² and exact F transformation under multivariate normality.
- Paired test as one-sample test on difference vectors.
- Pooled two-sample formula and distinct transformation are presented as design contrast.
- All numerical examples are checked in `verify_multivariate_t4.py`.

## References
- Johnson & Wichern, *Applied Multivariate Statistical Analysis*, Hotelling T² chapter.
- Rencher & Christensen, *Methods of Multivariate Analysis*, multivariate inference.
- Penn State STAT 505, https://online.stat.psu.edu/stat505/.
