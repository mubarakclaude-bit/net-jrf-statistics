# Evidence map — Unit VI, 6.1 Hat matrix, residual maker and quadratic forms

## Scope and PYQ provenance
The repository catalog defines regression-t1 as “Hat matrix, residual maker, quadratic forms”. The June 2026 Q9 variant cluster is not treated as a direct anchor: its items concern adjusted R², overall F, R² and multicollinearity. The backlog explicitly flags Q9's topic assignment as uncertain. No direct official PYQ is claimed for this lesson.

## Core mathematical claims
- OLS: β̂=(X′X)⁻¹X′y for full-column-rank X.
- Hat matrix: H=X(X′X)⁻¹X′; ŷ=Hy.
- Residual maker: M=I−H; e=My.
- Symmetry/idempotence: H′=H, H²=H; M′=M, M²=M.
- Complementarity: H+M=I and HM=MH=0.
- Trace/rank: tr(H)=rank(H)=k; tr(M)=rank(M)=n−k.
- Residual orthogonality: X′e=0.
- Residual sum of squares: e′e=y′My.

## Verification approach
A numerical full-rank design is used to check symmetry, idempotence, orthogonality, rank-trace values and projection complementarity. Mastery-pool structure and answer balance are checked separately. The 20 mastery items are original practice questions, not official PYQs.
