# T5 evidence map — Poisson process

## Scope anchor
UGC NET Statistics, Unit IX: Poisson process; inter-arrival and waiting-time distributions. This lesson is intentionally limited to these named syllabus elements.

## Concept-to-lesson map

| Claim / skill | Lesson location | Independent check |
|---|---|---|
| Count law: N(t) ~ Poisson(λt) | s2, s3, s5 | verify_stochastic_t5.py: count probabilities |
| Mean and variance of N(t) equal λt | s4 | exact parameter identity |
| Independent increments | s2, s4 | conceptual statements in mastery items |
| Stationary increments | s2, s4 | increment distribution over t−s |
| First inter-arrival time is Exp(λ) | s6, s7 | survival and CDF identities |
| Exponential mean and variance | s0, s6 | reciprocal-rate identities |
| kth arrival time is Gamma/Erlang | s8, s9 | sum-of-exponentials and count identity |
| P(T_k>t)=P(N(t)≤k−1) | s8, s9 | exact Poisson-tail calculation |
| Memoryless property | s10, mastery item 20 | exponential survival ratio |

## Formula checks

1. Poisson count: P(N(t)=n)=exp(−λt)(λt)^n/n!.
2. No-event probability: P(N(t)=0)=exp(−λt).
3. First arrival survival: P(T₁>t)=exp(−λt).
4. kth arrival survival: P(T_k>t)=Σ(j=0 to k−1) exp(−λt)(λt)^j/j!.
5. Moments: E[T_k]=k/λ and Var(T_k)=k/λ².

## Pedagogical checks
- Foundation recovery revisits rate × duration, Poisson counts and exponential survival.
- Worked examples separate exact counts, at-least-one counts and kth-arrival waiting times.
- Guided practice includes explicit unit conversion.
- Mastery pool has 20 items with 6 easy, 10 moderate and 4 hard items, mixing conceptual and numerical formats.
- This is original practice material, not an official PYQ set.
