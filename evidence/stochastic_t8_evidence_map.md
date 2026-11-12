# T8 evidence map — Branching Processes

## Scope and model
This lesson introduces the classical Galton–Watson branching process as the standard discrete-generation branching model. It is labelled stochastic-t8 in the repository backlog. Examples and mastery questions are original practice, not official PYQs.

## Concept-to-lesson map
| Competency | Lesson scene | Check |
|---|---|---|
| Offspring random variable and PGF | s0–s3 | Construct f(s), verify f(1)=1 |
| Mean offspring and expected generation size | s4 | E[Z_n]=Z_0m^n |
| Fixed-point extinction probability | s6 | Exact roots and smallest-root selection |
| Finite-generation extinction | s7–s8 | q_0=0, q_{n+1}=f(q_n) |
| Criticality and degenerate cases | s9–s11 | Subcritical/critical/supercritical classification |

## Mathematical verification targets
- PGF normalisation and derivative at one.
- Binomial(2,p) offspring PGF and mean.
- Exact extinction root for p=0.6: q=4/9.
- Two-generation extinction for f(s)=1/2+s²/2: q₂=5/8.
- Offspring law (0.1,0.2,0.7): m=1.6 and q=1/7.
- Degenerate K=1 almost surely: q=0.

## Learner design
Foundation recovery precedes symbols; worked derivations are followed by guided recursion and a transfer problem; interpretation distinguishes expected growth from extinction probability.
