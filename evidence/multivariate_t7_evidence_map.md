# Evidence map — Module 8.7: MLE of mean vector and covariance

June 2026 Paper 2 Q37 (`j26-q37`) in `seed/pyq_j26_full.json`. Observations (1,2)', (4,4)', (4,3)' from a bivariate normal model. Mean (3,3)'. Centred outer-product sum [[6,3],[3,2]]. Divide by n=3 for MLE [[2,1],[1,2/3]], official option D. Unbiased covariance divides by n−1=2, giving [[3,3/2],[3/2,1]].

Theory: Johnson & Wichern, *Applied Multivariate Statistical Analysis*; Rencher & Christensen, *Methods of Multivariate Analysis*; Penn State STAT 505: https://online.stat.psu.edu/stat505/.

Identities: μ̂=x̄; Σ̂=(1/n)Σ(xᵢ−x̄)(xᵢ−x̄)'; S=(1/(n−1))Σ(xᵢ−x̄)(xᵢ−x̄)'; Σ̂=((n−1)/n)S; rank(Σ̂)≤min(p,n−1).

Scope: normal-model mean and covariance MLEs, unbiased covariance distinction and rank. Shrinkage, regularisation and Bayesian estimation are out of scope.