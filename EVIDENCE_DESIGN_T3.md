# Evidence map — Unit III, Design of Experiments, Topic 3B.3

## Scope and PYQ treatment
- Catalog topic: `design-t3`, “Factorial experiments”.
- Covers full two-level factorial designs (2² and 2³), treatment combinations, marginal main effects, simple effects, interactions, balanced replication and replicated 2² ANOVA.
- Fractional factorial aliasing and confounding are reserved for the later confounding topic.
- No direct official PYQ is claimed; mastery items are original practice.

## Formula claims
- Full 2^k factorial: 2^k treatment combinations and 2^k−1 non-empty factorial effects/treatment df.
- 2² main effect A = average response at A+ minus average response at A−; similarly for B.
- AB interaction contrast = (A effect at B+)−(A effect at B−).
- Balanced replicated 2² with r replicates: total df=4r−1; treatment df=3; pure error df=4(r−1).
- In a balanced replicated 2², orthogonal contrasts partition treatment SS into SS_A+SS_B+SS_AB.

## Exact worked-example checks
- Cell means in order A−B−, A+B−, A−B+, A+B+: (9,13,11,19).
- Main effect A=6; main effect B=4; AB interaction=4.
- Replicated data: (8,10), (12,14), (10,12), (18,20); G=104, N=8, CF=1352, Σy²=1472, total SS=120.
- SS_A=72; SS_B=32; SS_AB=8; pure error SS=8; decomposition 72+32+8+8=120.
- Degrees of freedom: A=1, B=1, AB=1, error=4, total=7; F ratios are 36, 16 and 4.

## Assumptions and limits
- Standard fixed-effects factorial ANOVA assumes independent errors, common variance and normality for exact finite-sample F inference.
- Randomisation is required; balanced replication supports orthogonal contrasts.
- A substantial interaction should be interpreted using cell means/simple effects rather than marginal main effects alone.
- Repeated measurements on one experimental unit are not automatically independent replications.

## Verification
- `verify_design_t3.py` uses exact rational arithmetic and checks effect contrasts, SS decomposition, F ratios, df identities and mastery distributions.
