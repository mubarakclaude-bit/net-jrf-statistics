# T6 evidence map — Simple Random Walk and Gambler’s Ruin

## Scope anchor
UGC NET Statistics Unit IX explicitly names Gambler’s ruin problem and Simple random walk.

## Concept-to-lesson map

| Skill / result | Lesson location | Independent check |
|---|---|---|
| Random walk increments and drift | s0, s2 | verifier checks E[ΔS]=p−q |
| Binomial number of upward steps | s0, s2, s3 | exact binomial position probabilities |
| First-step gambler’s ruin recurrence | s4, s5 | recurrence and boundary checks |
| Fair upper-barrier probability i/N | s5 | exact rational boundary solutions |
| Biased upper-barrier probability | s6, s7 | exact rational recurrence |
| Expected absorption time, fair case | s8, s9 | m_i=i(N−i) recurrence |
| Expected absorption time, biased case | s8 | exact rational recurrence |
| Distinguish ruin probability and duration | s10, s11 | mastery pool conceptual checks |

## Formula checks
- Position: S_n=S_0+2X−n, X~Binomial(n,p).
- First-step equation: u_i=pu_{i+1}+qu_{i−1}.
- Boundaries for upper success: u_0=0, u_N=1.
- Fair upper success: u_i=i/N.
- Biased upper success: u_i=[1−(q/p)^i]/[1−(q/p)^N], p≠q.
- Expected absorption time: m_i=1+pm_{i+1}+qm_{i−1}, m_0=m_N=0.
- Fair duration: m_i=i(N−i).
- Biased duration: m_i=[i−Nu_i]/(q−p).

## Pedagogical checks
- Foundation recovery rebuilds binomial counting, net displacement and one-step expectation.
- Worked examples separate endpoint probabilities from expected duration.
- Guided practice includes a biased game with exact rational answer.
- Mastery pool contains 20 questions across easy / moderate / hard levels and includes numerical and multi-statement formats.
- Questions are original practice, not official PYQs.

## v4.1 lesson extension
- s12: guided transfer — calculate biased expected absorption time from the exact upper-hit probability.
- s13: summary — distinguish position probabilities, hitting probabilities and expected duration.
- s14: unseen mastery test linked to `stochastic_t6_mastery`.
