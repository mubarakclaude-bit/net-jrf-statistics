# Evidence map — stochastic-t2: Stationary distributions

## Scope and source alignment
- Official syllabus: UGC NET Statistics, Unit IX — Stochastic Processes (seed/meta_syllabus.json).
- Catalog topic: stochastic-t2, Stationary distribution (seed/catalog.json).
- Prerequisite lesson: stochastic-t1, Markov-chain transition matrices and n-step probabilities.
- Scope: invariant probability vectors, finite-state existence, irreducibility/uniqueness, periodicity/convergence, and reducible examples.

## Mathematical claims and verification anchors
| Claim | Lesson location | Verification |
|---|---|---|
| π is stationary iff πP=π and π is a probability vector | s2–s3 | Exact matrix multiplication |
| For P=[[0.8,0.2],[0.4,0.6]], π=(2/3,1/3) | s4 | Exact fractions in verifier |
| For P=[[0.7,0.3],[0.2,0.8]], π=(2/5,3/5) | s6 | Exact fractions in verifier |
| Three-state cyclic example has π=(1/3,1/3,1/3) | s8 | Exact fractions in verifier |
| Reducible example has family (t,1−t,0), 0≤t≤1 | s10 | Symbolic reduction and endpoint checks |
| Finite existence; finite irreducibility gives uniqueness; aperiodicity supports convergence | s9, s11 | Standard finite-state Markov-chain theorems |

## Reference basis
- Norris, J. R., Markov Chains, stationary distributions and finite-state chains: https://www.statslab.cam.ac.uk/~james/Markov/
- Ross, S. M., Introduction to Probability Models, Markov-chain chapter.
- Lawler, G. F., Introduction to Stochastic Processes: https://www.math.uchicago.edu/~lawler/

## Limitations
- No June 2026 PYQ is asserted as a direct anchor for this topic.
- No claim is made that a stationary distribution always equals the limiting distribution.
- General countably infinite-state existence/recurrence theory is outside this lesson.
