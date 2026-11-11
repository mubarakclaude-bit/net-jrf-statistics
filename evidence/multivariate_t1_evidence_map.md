# Evidence map — Unit VIII, Multivariate Normal: marginals and conditionals

## Scope
- Topic: `multivariate-t1` — multivariate normal distribution, marginal distributions and conditional distributions.
- No direct official June 2026 question is claimed as an anchor for this lesson.
- June 2026 Q24 includes conditional-covariance and partial-correlation practice variants in `seed/multivariate_pyq_variants.json`; these are labelled variants and are not represented as a direct official question on the multivariate-normal block formula.

## Core claims and independent checks
- If X~N_p(μ,Σ), any subvector is multivariate normal with the corresponding entries of μ and principal covariance submatrix.
- For the partition X=(X₁′,X₂′)′ and Σ=[[Σ₁₁,Σ₁₂],[Σ₂₁,Σ₂₂]], the marginal X₂ has covariance Σ₂₂.
- The conditional mean is μ₂+Σ₂₁Σ₁₁⁻¹(x₁−μ₁).
- The conditional covariance is the Schur complement Σ₂₂−Σ₂₁Σ₁₁⁻¹Σ₁₂.
- The conditional covariance does not depend on the observed value x₁.
- For jointly multivariate normal blocks, zero cross-covariance is equivalent to independence.
- For a non-singular multivariate normal vector, conditional independence of coordinates i and j given all remaining coordinates is equivalent to a zero (i,j) entry in the precision matrix Σ⁻¹.

## Arithmetic examples
- Bivariate example: Var(X)=4, Var(Y)=9, Cov(X,Y)=2, μX=10, μY=20. Given X=12, conditional mean=20+(2/4)(2)=21 and conditional variance=9−4/4=8.
- Matrix example: Σ₁₁=[4], Σ₁₂=[2 0], Σ₂₁=[2;0], Σ₂₂=[[9,1],[1,5]]. The Schur complement is [[8,1],[1,5]].
- Hard mastery example: Σ₁₁=[2], Σ₂₁=[[2],[4]], Σ₂₂=[[5,1],[1,12]]. Conditional covariance is [[3,−3],[−3,4]].

## Verification
- Exact rational arithmetic and mastery-contract checks: `verify_multivariate_t1.py`.
- Authoring structure audit: `lesson_multivariate_t1.py`.
