# Evidence map — Regression T2: Gauss–Markov, BLUE and estimability

## Source anchor
Repository June 2026 Paper 2 item **j26-q11**, linked to six variants **j26v-q11-01…06**. The stored official answer is B; the response record says the candidate marked D. The stem and options are transcribed in `seed/pyq_j26_full.json`.

## Independently verified anchor calculation
X = [[1,1],[2,0],[1,-1]].
X′X = [[6,0],[0,2]], and X′y = (y₁+2y₂+y₃, y₁−y₃)′.
Therefore β̂₁=(y₁+2y₂+y₃)/6 and β̂₂=(y₁−y₃)/2. This is option B.

**Assumption caution:** The Gauss–Markov result uses V(u|X)=σ²I, not merely equal marginal variances. The transcribed question states V(uᵢ)=σ²; the standard exam interpretation additionally assumes uncorrelated errors. The lesson makes this condition explicit rather than silently treating equal variances as sufficient.

## Competency map
| Competency | Scene | Assessment |
|---|---|---|
| Matrix/expectation/rank foundations | s0 | foundation checks |
| Meaning and comparison class of BLUE | s1–s3 | conceptual items |
| OLS derivation and unbiasedness | s4–s6 | completion and numeric checks |
| Minimum-variance argument | s7 | hard multi-statement |
| Estimability by row space | s8–s9 | rank-deficient transfer |
| June 2026 anchor computation | s10 | guided problem and linked PYQ variants |
| Assumptions and common traps | s11–s13 | trapcheck and mastery pool |

All mastery questions are original practice items, not official PYQs.
