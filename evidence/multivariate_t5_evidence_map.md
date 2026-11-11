# Evidence map — Module 8.5 Wishart distribution

## Primary examination anchor
- Source: `seed/pyq_j26_full.json`, item `j26-q17` (June 2026 Paper 2 Q17).
- The source defines independent four-dimensional normal vectors: two X columns with covariance Σ₁ and three Y columns with covariance Σ₂.
- Each block is whitened using its own inverse square-root covariance matrix.
- Official key: B, (W_4(5,I_4)).

## Independent derivation
- Each (Sigma_1^{-1/2}X_j) is (N_4(0,I_4)); two independent columns give (W_4(2,I_4)).
- Each (Sigma_2^{-1/2}Y_j) is (N_4(0,I_4)); three independent columns give (W_4(3,I_4)).
- The two blocks are independent and have common scale (I_4).
- By the Wishart addition property, their sum is (W_4(2+3,I_4)=W_4(5,I_4)).

## Scope
- Definition from independent multivariate normal outer products.
- Dimension, degrees of freedom, scale and expected value.
- Addition and congruence transformation properties.
- Whitening and the sample covariance distribution.
- Independence of sample mean and sample covariance under multivariate normality.

## References
- Johnson & Wichern, *Applied Multivariate Statistical Analysis*.
- Rencher & Christensen, *Methods of Multivariate Analysis*.
- Penn State STAT 505, https://online.stat.psu.edu/stat505/.
