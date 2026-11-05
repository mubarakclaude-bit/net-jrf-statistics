# Lesson 4.3 — Rao–Blackwell and Lehmann–Scheffé

Complete authored content of one lesson from a UGC-NET Statistics (Code 107) preparation application, extracted from the application's own content files.

| | |
|---|---|
| Content version | 1.3 |
| Scenes | 14 |
| Core scenes | 14 |
| Optional JRF-extension scenes | 0 |
| Estimated learner time | 51 minutes |
| Mastery pool | 20 items |
| Position in the app | Statistical Inference → Point Estimation → Best unbiased estimation |
| Engine | Estimation and inference — sampling distributions, and the variance you remove by conditioning |
| Pool label | Rao–Blackwell and Lehmann–Scheffé — mastery test (unseen) |
| Unit | IV — Statistical Inference |
| Audience | JRF-target candidates, many returning after several years away |

## Before you start: where this lesson sits

This lesson is at content version **1.3**. The application's current authoring standard is 4.1, and three of its requirements are **known** to be unmet here, so please do not spend effort reporting them — they are scheduled work, not findings:

- no short "how to use this lesson" note on the overview;
- a quick check on only some teaching scenes rather than all of them;
- no family-to-statistic style reference table where one would help.

This lesson is also **51 minutes against a house standard of about 90**, so it is thinner than intended. Comments on what is MISSING in substance are therefore especially useful — but please flag omissions rather than proposing to shorten what is there.

It carries 2 references against a minimum of three; suggestions for a free university course page or a standard textbook chapter at this level are welcome.

What follows is the complete authored content as it stands.

## How to review this, and what to send back

Please return **a list of findings, not a rewritten lesson.** The two previous review rounds came back as complete rewrites, and both times material was lost in the re-typing that nobody intended to drop — the exponential-family derivation in one round, a version label left inconsistent in the other. A findings list avoids that entirely.

Each field below carries its **JSON path** in the content file. Please cite it. One finding per item, in this shape:

```
path:      scenes[10].blocks[1].body
severity:  error | imprecision | suggestion
issue:     what is wrong, in one sentence
evidence:  the counterexample, condition or source that shows it
proposed:  the replacement text, if you have one
```

What is most worth your attention, in order:

1. **Mathematical errors and overclaims.** Statements true in the examples shown but false in general; converses asserted; side conditions omitted (sample-size requirements, support conditions, regularity assumptions); steps skipped in a counterexample so that it does not actually establish what it claims.
2. **Items in the mastery pool with more than one defensible answer**, especially any stem asking for "a sufficient statistic" where a distractor is itself sufficient.
3. **Places where the explanation is correct but would not survive contact with a candidate who has been away from the subject for years.**
4. Anything examinable for this syllabus that is missing.

Please do **not** recommend removing depth to make the lesson shorter. The target is JRF, which is decided by the harder theoretical questions, and the optional-extension mechanism already exists for material a bare pass does not need.

Notation is Unicode as the application stores it: `Σxᵢ` is a sum over the sample, `x̄` the sample mean, `x₍₁₎` and `x₍ₙ₎` the smallest and largest observations, `I(·)` an indicator, `∝` proportionality up to a factor free of the parameter, and `⟺` logical equivalence.

---

## Lesson-level fields

**Learning objectives** `objectives[]`

1. State Rao–Blackwell and say why the statistic conditioned on must be sufficient.

2. Compute E[δ(X) | T = t] in the standard cases, using the conditional distribution of the sample given its total.

3. State Lehmann–Scheffé and explain exactly which word turns 'an improvement' into 'the unique best'.

4. Produce a UMVUE by either route — Rao–Blackwellise a crude unbiased estimator, or find an unbiased function of a complete sufficient statistic directly.

5. Say when a UMVUE fails to exist, and when it exists but is absurd.

6. Separate the UMVUE from the MLE, and know which of the two survives a change of parameter.

**Assumed prior knowledge** `prereq[]`

- `prereq[0]` **Sufficiency and the factorisation theorem** — Rao–Blackwell conditions on a sufficient statistic. If T is wrong, E[δ|T] still involves θ and is not an estimator at all.
- `prereq[1]` **Completeness** — It is the single word that upgrades Rao–Blackwell's 'no worse' into Lehmann–Scheffé's 'uniquely best'. Scene 7 leans on it entirely.
- `prereq[2]` **Conditional expectation and the variance decomposition** — Var(δ) = E[Var(δ|T)] + Var(E[δ|T]) is the whole proof of Rao–Blackwell. Know it before scene 3.

**Misconceptions the lesson is built to pre-empt** `traps[]`

- Conditioning on a statistic that is not sufficient, and producing an 'estimator' that still contains θ.

- Reading Rao–Blackwell as a strict improvement. It is ≤, with equality when δ was already a function of T.

- Claiming uniqueness from Rao–Blackwell alone. Uniqueness needs completeness.

- Applying Lehmann–Scheffé in a curved family, where no complete sufficient statistic exists.

- Squaring the UMVUE of θ and calling it the UMVUE of θ². That is MLE invariance, and UMVUEs do not have it.

- Assuming the UMVUE must beat the MLE on mean squared error. For the normal variance it does not.

- Forgetting to subtract the bias term: x̄² estimates μ² + σ²/n, not μ².

**Assessment policy** `mastery`

- 10 items drawn per attempt from a pool of 20, mix 3 easy, 5 moderate, 2 hard
- pass mark 80%, no hints during the test, retest after 7 days
- `mastery.note`: Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the difficulty mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split.

**Sources** `refs[]`

- `refs[0]` **Mathematical Statistics — Unbiased Estimation and Risk Inequalities** — MIT OpenCourseWare 18.655 (Spring 2016), Lecture note 13 (Lecture notes, free). The graduate statement of both theorems with the risk framework around them. Reach for it after scene 7, when you want to see why the conclusion is about convex loss and not only variance.
- `refs[1]` **Properties of a Sufficient Statistic — Completeness and Uniqueness** — Purdue STAT 517, Prof. Michael Levine, 16 April 2015 (Lecture slides, free). Works the same examples this lesson uses — Bernoulli by conditioning, the exponential MVUE, the uniform (n+1)/n·X₍ₙ₎, and N(μ, a²μ²) as a sufficient-but-not-complete case. Read it after scene 6. One caution: the final slide labels the MVUE of a Poisson probability as 'the MVUE of λ', which is a slip — the target there is the probability, not the parameter.

---

## The lesson, scene by scene

### Scene 1 of 14 — Before the lesson — four things it will assume

`scenes[0]` · id `s0` · type `foundation` (prerequisite check) · 6 minutes

**Purpose** `scenes[0].objective`

Rebuild conditional expectation and the variance decomposition, which together are the whole proof of Rao–Blackwell.

**Body** `scenes[0].body[]`

Rao–Blackwell has a reputation for being deep. It is one line of algebra you already know: a variance splits into two non-negative pieces, so throwing one away can only help. The theorem is that observation, applied to E[δ|T].

What makes it feel hard after a gap is conditional expectation — specifically, remembering that E[δ|T] is a random variable and not a number. Three checks on that, one on the topic before this.

**Check 1** `scenes[0].items[0]`

- *asks:* What does the factorisation theorem say, and why must Rao–Blackwell condition on a sufficient statistic specifically?
- *expected answer* `.recall`: If f(x;θ) = g(T(x);θ)h(x) with h free of θ, then T is sufficient. Conditioning on a sufficient T leaves no θ in the conditional distribution, so E[δ|T] is computable from the data alone. Condition on a non-sufficient statistic and the answer still contains θ — it is not an estimator at all.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Sufficiency is doing real work here, not decoration. E[δ|T=t] is an average over the conditional distribution of the data given T=t. If that conditional distribution depends on θ, so does the average, and you cannot compute it without knowing the very thing you are estimating.

> That is the one-sentence reason the theorem is stated for sufficient statistics: sufficiency is exactly the condition that makes the conditional average usable.

**Check 2** `scenes[0].items[1]`

- *asks:* Is E[δ|T] a number or a random variable? And what is E[X₁ | ΣXᵢ = t] for an iid sample?
- *expected answer* `.recall`: A random variable — a function of T. E[δ|T=t] is a number, for each fixed t; E[δ|T] is the whole function, and it has a variance of its own. By symmetry E[X₁|ΣXᵢ=t] = t/n, since the n observations are exchangeable and their conditional means must sum to t.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Keep the two notations apart and most of the confusion goes. E[δ|T=t] means 'average δ over all data sets with T=t' — a number depending on t. E[δ|T] means 'that number, as a function of the random T' — a random variable.

> The symmetry argument is worth having at your fingertips because it appears in exam questions as a one-step answer. If X₁,…,Xₙ are iid and you are told ΣXᵢ = t, no observation is distinguishable from any other, so all n conditional means are equal; they add to t; so each is t/n. No distribution was needed.

> The same move, less obviously: E[X₁X₂|ΣXᵢ=t] is the same for every pair, which turns a hard conditional expectation into counting pairs.

**Check 3** `scenes[0].items[2]`

- *asks:* State the decomposition of Var(δ) in terms of a statistic T.
- *expected answer* `.recall`: Var(δ) = E[Var(δ|T)] + Var(E[δ|T]). Both terms are non-negative, so Var(E[δ|T]) ≤ Var(δ). That single inequality is Rao–Blackwell.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Read it as bookkeeping. The total variability of δ is the variability left inside each level of T, averaged across levels, plus the variability of the level averages themselves. Nothing is created or lost.

> Rao–Blackwell keeps the second term and discards the first. Since E[Var(δ|T)] ≥ 0 always, the replacement estimator E[δ|T] has variance no larger — and strictly smaller unless Var(δ|T) = 0, which means δ was already a function of T.

> The companion fact is the tower property: E[E[δ|T]] = E[δ]. It is what guarantees the new estimator is still unbiased, so you have paid nothing for the variance reduction. Have both lines ready before section 3.

**Check 4** `scenes[0].items[3]`

- *asks:* What does 'unbiased' mean precisely, and what does 'uniformly minimum variance' add to it?
- *expected answer* `.recall`: Unbiased: E[T] = θ for every θ in the parameter space, not just for one convenient value. UMVUE adds that among all unbiased estimators, this one has the smallest variance at every θ simultaneously — no trading good performance at one θ for bad at another.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> The 'for every θ' in unbiasedness is where marks are lost. An estimator that happens to be right on average when θ = 2 is not unbiased.

> The word 'uniformly' carries the same weight. It is easy to find an estimator with tiny variance at one point — the constant 7 has variance zero and is superb if θ really is 7. Requiring unbiasedness rules out that cheat, and requiring minimum variance uniformly rules out the subtler versions of it.

> This is why Lehmann–Scheffé is worth so much: it hands you a single estimator that wins at every θ at once, which is a far stronger statement than winning on average.

---

### Scene 2 of 14 — A terrible estimator, and what to do with it

`scenes[1]` · id `s1` · type `intuition` (intuition) · 5 minutes

**Purpose** `scenes[1].objective`

See conditioning as the act of throwing away noise while keeping the signal.

**Body** `scenes[1].body[]`

You have n observations from a Poisson(λ) and you want to estimate e^(−λ), the probability that a count comes out zero.

Here is an estimator that works: look only at the FIRST observation and score 1 if it was zero, 0 otherwise. Call it δ = 1{X₁ = 0}. Its expectation is exactly P(X₁ = 0) = e^(−λ), so it is unbiased. Correct, and useless — it ignores n−1 observations and can only ever return 0 or 1 while estimating a number strictly between them.

Now ask a different question. Suppose someone tells you the total ΣXᵢ = 7, but not how the sevens were distributed. What is your best guess at δ? That is a conditional expectation: E[δ | ΣXᵢ = 7]. Answering it uses all n observations, because the total did.

Rao–Blackwell says that quantity is still unbiased, and its variance cannot be larger. You have improved the estimator by doing nothing but averaging away the part of the data that was irrelevant.

One condition makes this legal, and it is the reason the previous two topics exist. The conditioning statistic has to be SUFFICIENT. If it were not, the conditional distribution would still depend on λ, and E[δ | T] would contain the unknown you were trying to estimate — not an estimator at all.

**Aside — What is actually being removed** `scenes[1].aside.body`

Var(δ) = E[Var(δ|T)] + Var(E[δ|T]). The first term is the variability of δ among samples that share the same T — pure noise, since those samples are indistinguishable as far as θ is concerned. Conditioning deletes that term. Nothing about θ is lost, because T is sufficient.

**Quick check before moving on** `scenes[1].ask`

- *question:* Why must T be sufficient for E[δ(X) | T] to be usable as an estimator at all?
- *hint on request:* Write down what you would need to know to compute the conditional expectation by hand. Is any of it unknown?

**Optional deep-dive, opened on demand — From a single yes/no to the best estimator there is** `scenes[1].scenario`

*teaser on the closed card:* An insurer needs P(a policy files no claim). The obvious estimator is almost useless.

> A motor insurer models the number of claims a policy files in a year as Poisson(λ) and needs to estimate the probability a policy stays claim-free, g(λ) = e^(−λ). It drives the renewal discount, so the estimate has to be defensible.

> Start with something crude but honest. Look at the FIRST policy only and write δ = 1 if it filed no claims and 0 otherwise. Its expectation is P(X₁ = 0) = e^(−λ), so it is unbiased — and it is also close to worthless, because it throws away every other policy and takes only the values 0 and 1.

> Now Rao–Blackwellise. T = ΣXᵢ is complete sufficient for λ, and conditioning the crude estimator on T gives E[δ | T = t] = ((n−1)/n)^t. The derivation is a binomial-thinning argument, but the conclusion is what matters: one conditioning step turns a coin-flip of an estimator into a smooth function of the entire portfolio.

> Because T is complete and the result is unbiased, Lehmann–Scheffé certifies it as THE uniformly minimum variance unbiased estimator. No better unbiased estimator exists — not merely none has been found.

> The practical lesson transfers to any portfolio problem: the quantity you can easily write down unbiasedly is rarely the one you should report, and conditioning on the sufficient statistic is the mechanical way to improve it without having to be clever.

*think-it-through question* `.q`: The actuary points out that the maximum likelihood estimate is simply e^(−x̄), which is easier to compute. Why not use that?

*what the statistics says* `.answer`: Because it is biased. By Jensen's inequality E[e^(−X̄)] > e^(−λ), so the MLE systematically overstates the claim-free probability — which in this application means systematically over-discounting renewals. ((n−1)/n)^T is unbiased at every portfolio size. The two agree as n grows, so for a large book the difference is immaterial; for a small segment it is not, and that is exactly where the discount decision is riskiest.

*link line* `.link`: The same machinery produces the UMVUE of a reliability function R(t) = e^(−λt) in engineering — the quantity a maintenance interval is built on.

---

### Scene 3 of 14 — The estimator you already know, and the one that is unbiased

`scenes[2]` · id `s2` · type `explore` (interactive visualisation) · 6 minutes

**Purpose** `scenes[2].objective`

See the bias Rao–Blackwell and Lehmann–Scheffé are there to remove.

**Body** `scenes[2].body[]`

This is the exact sampling distribution of the exponential MLE, λ̂ = n/ΣX. The solid line is the true λ; the dashed line is E[λ̂] = nλ/(n−1), sitting stubbornly to the right of it.

That gap is not a sampling accident — it is there at every n. The MLE systematically overstates the rate.

Now ΣX is a complete sufficient statistic for λ, and E[1/ΣX] = λ/(n−1). So (n−1)/ΣX has expectation exactly λ. It is an unbiased function of a complete sufficient statistic, which by Lehmann–Scheffé makes it the UMVUE.

Notice what it is: (n−1)/ΣX = ((n−1)/n) · λ̂. The best unbiased estimator is the MLE shrunk by a factor of (n−1)/n — precisely the factor that removes the gap on screen.

Raise n and watch the two lines converge. The correction gets smaller because the MLE's bias does, which is why the distinction stops mattering asymptotically and matters a great deal at the sample sizes exam questions use.

**Interactive element** `scenes[2].viz` — live plot of type `mle-sampling`, initial state lam=0.5, n=4. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[2].ask`

- *question:* s² is unbiased for σ² and the MLE Σ(xᵢ−x̄)²/n is not. Which of the two has the smaller mean squared error?
- *hint on request:* MSE = variance + bias². Dividing by a larger number shrinks an estimator — what does shrinking do to each of those two terms?

---

### Scene 4 of 14 — Rao–Blackwell, and the one line that proves it

`scenes[3]` · id `s3` · type `theory` (theory) · 7 minutes

**Purpose** `scenes[3].objective`

Hold the theorem with its condition attached, and be able to prove it from the variance decomposition.

**Block 1 — The construction** `scenes[3].blocks[0]` *(type `def`)*

Let δ(X) be any unbiased estimator of g(θ), and let T be sufficient for θ. Define η(T) = E[ δ(X) | T ]. Because T is sufficient, that conditional expectation does not involve θ, so η is a genuine statistic.

**Block 2 — Rao–Blackwell theorem** `scenes[3].blocks[1]` *(type `formula`)*

E_θ[η(T)] = g(θ)   for every θ,   and   Var_θ(η(T)) ≤ Var_θ(δ(X))   for every θ.

**Block 3 — Unbiasedness — the tower property** `scenes[3].blocks[2]` *(type `step`)*

E[η(T)] = E[ E[δ|T] ] = E[δ] = g(θ). One line, no conditions beyond δ being unbiased.

**Block 4 — The variance half — one decomposition** `scenes[3].blocks[3]` *(type `step`)*

Var(δ) = E[ Var(δ | T) ] + Var( E[δ | T] ) = E[ Var(δ|T) ] + Var(η(T)).
The first term is an expectation of a variance, so it is ≥ 0. Therefore Var(η) ≤ Var(δ).

**Block 5 — Sufficiency is not decoration** `scenes[3].blocks[4]` *(type `assume`)*

Drop it and E[δ|T] depends on θ. You would be writing down a function of the unknown parameter and calling it an estimate. Every exam question that offers a non-sufficient statistic to condition on is testing exactly this.

**Block 6 — It is ≤, not <** `scenes[3].blocks[5]` *(type `trap`)*

Equality holds precisely when Var(δ|T) = 0, which means δ was already a function of T. Rao–Blackwellising an estimator that already depends only on T changes nothing. Candidates lose marks asserting a strict improvement.

**Block 7 — What it does NOT give you** `scenes[3].blocks[6]` *(type `note`)*

A best estimator. Start from a different unbiased δ and you may land somewhere else. Rao–Blackwell improves; it does not identify. The next theorem fixes that, and it needs completeness to do it.

**Flow diagram** `scenes[3].flow` — Getting to a UMVUE — the two routes

*alt text* `.alt`: Decision chart for Rao–Blackwell and Lehmann–Scheffé

- row 1: You want the UMVUE of g(θ)
- row 2: Find a complete sufficient statistic T
- row 3: Can you spot an unbiased function of T directly?
- row 4: Take ANY unbiased δ, then compute E[δ | T]  |  Use it — or correct the bias of a convenient function of T
- row 5: Is the result unbiased and a function of T alone?
- row 6: Lehmann–Scheffé: it is THE UMVUE
- row 7: Its variance may still sit above the Cramér–Rao floor
- arrows: You want the UMVUE of g(θ) → Find a complete sufficient statistic T; Find a complete sufficient statistic T → Can you spot an unbiased function of T directly?; Can you spot an unbiased function of T directly? → [no] Take ANY unbiased δ, then compute E[δ | T]; Can you spot an unbiased function of T directly? → [yes] Use it — or correct the bias of a convenient function of T; Take ANY unbiased δ, then compute E[δ | T] → Is the result unbiased and a function of T alone?; Use it — or correct the bias of a convenient function of T → Is the result unbiased and a function of T alone?; Is the result unbiased and a function of T alone? → [yes] Lehmann–Scheffé: it is THE UMVUE; Lehmann–Scheffé: it is THE UMVUE → Its variance may still sit above the Cramér–Rao floor

*note shown under the diagram* `.note`: Rao–Blackwell improves any unbiased estimator; completeness is what upgrades 'improved' to 'best'. Without completeness you stop at the improvement.

**Quick check before moving on** `scenes[3].ask`

- *question:* Which inequality in the Rao–Blackwell argument guarantees that conditioning cannot increase variance, and what conditions do you need?
- *hint on request:* Use Var(E[U|T]) ≤ Var(U); the estimator must have finite variance, and conditioning is on a sufficient statistic.

---

### Scene 5 of 14 — Worked in full — the Poisson zero probability

`scenes[4]` · id `s4` · type `worked` (worked example) · 7 minutes

**Purpose** `scenes[4].objective`

Carry out one conditional expectation end to end, and see where the sufficiency gets used.

**Problem put to the learner** `scenes[4].problem`

X₁,…,Xₙ are iid Poisson(λ). Find the UMVUE of g(λ) = e^(−λ) = P(X = 0).

**Worked steps** `scenes[4].steps[]`

1. `scenes[4].steps[0]` Start from any unbiased estimator, however crude.

   ```
   δ = 1{X₁ = 0},   E[δ] = P(X₁ = 0) = e^(−λ)  ✓
   ```

   Laid out:

   $$δ = 1{X₁ = 0},   E[δ] = P(X₁ = 0) = e^{−λ}  ✓$$

   *why* `.why`: It does not have to be good. It has to be unbiased. The whole method is a machine for turning something unbiased into something unbiased and best.

2. `scenes[4].steps[1]` Name the complete sufficient statistic.

   ```
   T = ΣXᵢ ~ Poisson(nλ), complete and sufficient
   ```

   *why* `.why`: Sufficiency makes the conditioning legal; completeness will make the answer unique. Both were established in the previous two topics.

3. `scenes[4].steps[2]` Identify the conditional distribution of X₁ given T.

   ```
   Given ΣXᵢ = t, (X₁,…,Xₙ) ~ Multinomial(t, 1/n, …, 1/n),  so  X₁ | T = t ~ Binomial(t, 1/n)
   ```

   Laid out:

   $$Given ΣXᵢ = t, (X₁,…,Xₙ) ~ Multinomial(t, \frac{1}{n}, …, \frac{1}{n}),  so  X₁ | T = t ~ Binomial(t, \frac{1}{n})$$

   *why* `.why`: This is the step that does the work. Note there is no λ in it anywhere — that is sufficiency showing up in practice, not as an abstraction.

4. `scenes[4].steps[3]` Compute the conditional expectation.

   ```
   η(t) = E[ 1{X₁=0} | T = t ] = P(X₁ = 0 | T = t) = (1 − 1/n)^t = ((n−1)/n)^t
   ```

   Laid out:

   $$η(t) = E[ 1{X₁=0} | T = t ] = P(X₁ = 0 | T = t) = (1 − \frac{1}{n})^{t} = \frac{(n−1)}{n}^{t}$$

   *why* `.why`: The expectation of an indicator is the probability of the event. A Binomial(t, 1/n) is zero with probability (1−1/n)^t.

5. `scenes[4].steps[4]` Conclude.

   ```
   UMVUE of e^(−λ)  =  ((n−1)/n)^T,  where T = ΣXᵢ
   ```

   Laid out:

   $$UMVUE of e^{−λ}  =  \frac{(n−1)}{n}^{T},  where T = ΣXᵢ$$

   *why* `.why`: It is unbiased by the tower property, and it is a function of a complete sufficient statistic, so Lehmann–Scheffé makes it the unique best unbiased estimator.

6. `scenes[4].steps[5]` Sanity-check the shape.

   ```
   n = 10, T = 7  ⟹  (0.9)⁷ = 0.478,  which lies in (0,1) as a probability must
   ```

   *why* `.why`: Compare with the estimator you started from, which would have returned 0 or 1. Same unbiasedness, enormously less variance.

**What to take from it** `scenes[4].after`

Look back at step 3. Everything turned on knowing the conditional distribution of the sample given its total, and that distribution was free of λ. That is the only place sufficiency was used, and without it the calculation could not have been done at all.

**Quick check before moving on** `scenes[4].ask`

- *question:* In the Poisson example, how do you choose a function of the sufficient statistic whose conditional expectation equals the target estimator?
- *hint on request:* Condition the original unbiased estimator on T and compute its conditional expectation explicitly.

---

### Scene 6 of 14 — Pause and recall

`scenes[5]` · id `s5` · type `recall` (retrieval practice) · 2 minutes

**Purpose** `scenes[5].objective`

Retrieve before reading on — this is where the retention comes from.

**Intro** `scenes[5].intro`

Answer each in your head before revealing. Correcting a wrong retrieval beats re-reading a right answer.

- `scenes[5].items[0]` **Q:** State Rao–Blackwell.  
  **A:** If δ is unbiased for g(θ) and T is sufficient, then η(T) = E[δ|T] is unbiased and has variance no larger than δ's.
- `scenes[5].items[1]` **Q:** Which identity proves the variance half?  
  **A:** Var(δ) = E[Var(δ|T)] + Var(E[δ|T]). The first term is non-negative.
- `scenes[5].items[2]` **Q:** When does Rao–Blackwell leave the estimator unchanged?  
  **A:** When δ is already a function of T, so Var(δ|T) = 0.
- `scenes[5].items[3]` **Q:** What does Rao–Blackwell NOT give you, and what supplies it?  
  **A:** Uniqueness — a single best estimator. Completeness supplies it, through Lehmann–Scheffé.

---

### Scene 7 of 14 — Your turn, with the scaffolding removed — estimating p²

`scenes[6]` · id `s6` · type `completion` (fill in the blanks) · 8 minutes

**Purpose** `scenes[6].objective`

Run a conditional expectation yourself, with a hypergeometric count instead of a binomial one.

**Problem put to the learner** `scenes[6].problem`

X₁,…,Xₙ are iid Bernoulli(p). Find the UMVUE of g(p) = p². Take T = ΣXᵢ, which is complete and sufficient.

**Worked steps** `scenes[6].steps[]`

1. `scenes[6].steps[0]` Find a crude unbiased estimator to start from.

   - *learner is asked:* Write an unbiased estimator of p² using two observations.
   - *accepted answer* `.blank.answer`: X₁X₂
   - *also accepted:* X₁X₂; X1X2; X_1 X_2; x1x2; X₁·X₂; X1*X2; the product of two observations
   - *hint:* X₁ and X₂ are independent, each with mean p. What is the expectation of their product?

   *why* `.why`: E[X₁X₂] = E[X₁]E[X₂] = p². Crude — it uses two observations and returns only 0 or 1 — but unbiased, which is all the method needs.

2. `scenes[6].steps[1]` Recognise what the conditional expectation is asking for.

   ```
   E[X₁X₂ | T = t] = P(X₁ = 1 and X₂ = 1 | ΣXᵢ = t)
   ```

   *why* `.why`: The product of two indicators is itself the indicator of both events happening, so its conditional expectation is a conditional probability.

3. `scenes[6].steps[2]` Count the arrangements.

   - *learner is asked:* Write that probability as a ratio of binomial coefficients.
   - *accepted answer* `.blank.answer`: C(n−2, t−2) / C(n, t)
   - *also accepted:* C(n−2, t−2) / C(n, t); C(n-2,t-2)/C(n,t); (n-2 choose t-2)/(n choose t); C(n-2, t-2)/C(n, t); nCt form: C(n-2,t-2)/C(n,t)
   - *hint:* Given t ones among n positions, every arrangement is equally likely. Fix ones in positions 1 and 2 — how many ways are left to place the rest?

   *why* `.why`: Conditional on the total, the pattern of ones is uniform over all C(n,t) arrangements. Fixing two of them leaves C(n−2,t−2).

4. `scenes[6].steps[3]` Simplify.

   - *learner is asked:* Simplify that ratio.
   - *accepted answer* `.blank.answer`: t(t−1) / (n(n−1))
   - *also accepted:* t(t−1) / (n(n−1)); t(t-1)/(n(n-1)); T(T-1)/(n(n-1)); t(t-1)/n(n-1)
   - *hint:* Write both coefficients as factorials and cancel. Almost everything goes; two factors survive on top and two below.

   *why* `.why`: The factorials collapse to t(t−1)/(n(n−1)) — a clean function of T alone, as it had to be.

5. `scenes[6].steps[4]` Conclude.

   ```
   UMVUE of p²  =  T(T−1) / (n(n−1)),  T = ΣXᵢ
   ```

   Laid out:

   $$UMVUE of p²  = \frac{T(T−1)}{(n(n−1)),  T} = ΣXᵢ$$

   *why* `.why`: Unbiased and a function of a complete sufficient statistic, so Lehmann–Scheffé applies. Note it is NOT p̂² = (T/n)², which is biased upward — the UMVUE is the version with the (T−1) and the (n−1).

**What to take from it** `scenes[6].after`

Both worked examples had the same shape: pick anything unbiased, condition on the total, and let the conditional distribution of the sample given its total do the work. Only the counting changed — binomial for the Poisson, hypergeometric here.

---

### Scene 8 of 14 — Lehmann–Scheffé, and when a UMVUE misbehaves

`scenes[7]` · id `s7` · type `theory` (theory) · 9 minutes

**Purpose** `scenes[7].objective`

See exactly which word upgrades an improvement into the unique best, and learn the limits.

**Block 1 — Lehmann–Scheffé theorem** `scenes[7].blocks[0]` *(type `formula`)*

If T is a COMPLETE sufficient statistic and η(T) is unbiased for g(θ),
then η(T) is the UMVUE of g(θ), and it is unique with probability 1.

**Block 2 — Why completeness gives uniqueness** `scenes[7].blocks[1]` *(type `step`)*

Suppose η₁(T) and η₂(T) are both unbiased for g(θ). Then E[η₁(T) − η₂(T)] = 0 for every θ. So η₁ − η₂ is an unbiased estimator of zero that is a function of T — and completeness says the only such function is zero. Hence η₁ = η₂ almost surely.

**Block 3 — Both routes land in the same place** `scenes[7].blocks[2]` *(type `note`)*

Route A: take any unbiased δ and compute E[δ|T]. Route B: solve E[h(T)] = g(θ) for h directly. Completeness guarantees they give the same answer, so use whichever is less algebra. Route B is usually faster when you can guess the form of h.

**Block 4 — A UMVUE can be absurd** `scenes[7].blocks[3]` *(type `trap`)*

Take a SINGLE Poisson observation, n = 1, and estimate e^(−2λ). Solving E[h(X)] = e^(−2λ) gives h(x) = (−1)^x. So the unique best unbiased estimator alternates between +1 and −1 while estimating a number strictly inside (0,1). It is the UMVUE, and it is nonsense. Unbiasedness is a constraint, not a virtue, and this example is the standard way examiners make that point.

**Block 5 — UMVUEs are not invariant** `scenes[7].blocks[4]` *(type `trap`)*

The MLE of g(θ) is g(θ̂) — that is invariance, and it holds for any g, under the usual induced-likelihood convention, whenever an MLE of θ exists. The UMVUE has no such property. For U(0,θ) the UMVUE of θ is (n+1)/n·X₍ₙ₎, but the UMVUE of θ² is (n+2)/n·X₍ₙ₎², which is NOT the square of the first. Scene 11 makes you derive both.

**Block 6 — No complete sufficient statistic, no theorem** `scenes[7].blocks[5]` *(type `assume`)*

In a curved family such as N(θ,θ²), the minimal sufficient statistic is not complete, so Lehmann–Scheffé is silent. A UMVUE may still exist, but you would need a different argument to find it — and an exam will not expect you to.

**Block 7 — Unbiased is not the same as accurate** `scenes[7].blocks[6]` *(type `note`)*

For N(μ,σ²), s² = Σ(xᵢ−x̄)²/(n−1) is the UMVUE of σ², yet the MLE Σ(xᵢ−x̄)²/n has smaller mean squared error, and Σ(xᵢ−x̄)²/(n+1) is better still. UMVUE means smallest variance among UNBIASED estimators only. Drop the unbiasedness requirement and you can usually do better.

**Quick check before moving on** `scenes[7].ask`

- *question:* What two conditions must be combined to use Lehmann–Scheffé to identify a UMVUE?
- *hint on request:* The estimator must be unbiased and be a function of a complete sufficient statistic.

**Optional deep-dive, opened on demand — Estimating a survival probability you will be held to** `scenes[7].scenario`

*teaser on the closed card:* An SLA promises 99.9% uptime. Someone has to estimate the probability of no crash.

> A platform team runs a service under a contract that specifies availability. The quantity in the contract is a probability — the chance the service survives the next hour without an incident — and the data are the intervals between past incidents, modelled as exponential with unknown rate.

> The obvious estimator is the obvious one for a reason: count how many of the past hours had no incident and take the proportion. It is unbiased and it is almost useless, because it throws away the actual times and reduces a continuous record to a handful of zeros and ones. With only a few incidents on record its variance is enormous.

> Rao–Blackwell repairs it without changing the target. Condition the crude indicator on the total time on test, which is sufficient for the rate, and the result is a smooth function of that total — an estimator with the same expectation and a strictly smaller variance. Completeness then promotes 'smaller' to 'smallest': by Lehmann–Scheffé no unbiased estimator of that probability does better.

> The practical difference is visible in the number the team can defend. The crude estimator is forced into coarse steps and can return exactly zero or exactly one from a short record, which is indefensible in a contract negotiation. The conditioned version moves smoothly with the evidence, which is what a figure in a service agreement has to do.

*closing line:* Rao–Blackwell is not a theoretical refinement here: it is the difference between a number you can defend and one you cannot.

---

### Scene 9 of 14 — Where the complete sufficient statistic is an order statistic

`scenes[8]` · id `s8` · type `explore` (interactive visualisation) · 6 minutes

**Purpose** `scenes[8].objective`

Apply Lehmann–Scheffé by the direct route, with no conditioning at all.

**Body** `scenes[8].body[]`

X₁,…,Xₙ are iid U(0, θ). The likelihood is the cliff on screen, and X₍ₙ₎ is complete and sufficient — both established in the previous two topics.

Here Route B is far easier than conditioning. Write the density of the maximum: f(x) = n x^(n−1)/θⁿ on (0, θ). Then E[X₍ₙ₎] = ∫₀^θ x · n x^(n−1)/θⁿ dx = nθ/(n+1).

So X₍ₙ₎ understates θ by the factor n/(n+1), and multiplying it back gives an unbiased estimator: (n+1)/n · X₍ₙ₎. It is an unbiased function of a complete sufficient statistic, so Lehmann–Scheffé makes it the UMVUE. No conditional expectation was needed anywhere.

Drag the maximum and watch the whole likelihood follow it. Everything the data say about θ is in that one number — which is why an estimator built on it can be best.

Compare with the MLE, which is X₍ₙ₎ itself. It can never exceed θ, so it is biased low at every n. The UMVUE is the same statistic with the bias scaled out, exactly as in the exponential case in scene 2.

**Interactive element** `scenes[8].viz` — live plot of type `unif-likelihood`, initial state n=6, xmax=4.2. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[8].ask`

- *question:* The MLE here is X₍ₙ₎ and the UMVUE is (n+1)/n·X₍ₙ₎. Both are functions of the same statistic. Why is only one of them unbiased?
- *hint on request:* The maximum of n draws from (0,θ) sits below θ with probability 1. What does that force its expectation to be?

---

### Scene 10 of 14 — Now without the steps — the UMVUE of μ²

`scenes[9]` · id `s9` · type `guided` (guided problem) · 8 minutes

**Purpose** `scenes[9].objective`

Choose the direct route yourself, and remember the correction term.

**Problem put to the learner** `scenes[9].problem`

X₁,…,Xₙ are iid N(μ, σ²) with σ² KNOWN. Find the UMVUE of μ².

**Hint ladder, revealed one at a time** `scenes[9].hints[]`

1. Direction — first name the complete sufficient statistic for μ when σ² is known. Then write down the obvious candidate for estimating μ² and ask whether it is actually unbiased, rather than assuming it.
2. Method — Route B. You want h with E[h(X̄)] = μ². Start from E[X̄²] and use the identity E[Y²] = Var(Y) + (E[Y])². The gap you find is the correction you must subtract.
3. Next step — X̄ ~ N(μ, σ²/n), so Var(X̄) = σ²/n. Put that into the identity and read off what has to come off X̄².

**Model solution, hidden until requested** `scenes[9].solution[]`

1. `scenes[9].solution[0]` Complete sufficient statistic.

   ```
   σ² known ⟹ the family is a full-rank one-parameter exponential family, so X̄ is complete and sufficient for μ.
   ```

2. `scenes[9].solution[1]` Test the obvious candidate.

   ```
   E[X̄²] = Var(X̄) + (E[X̄])² = σ²/n + μ²  ≠ μ²
   ```

   Laid out:

   $$E[X̄²] = Var(X̄) + (E[X̄])² = \frac{σ²}{n} + μ²  ≠ μ²$$

3. `scenes[9].solution[2]` Correct the bias.

   ```
   E[ X̄² − σ²/n ] = μ²   ✓
   ```

   Laid out:

   $$E[ X̄² − \frac{σ²}{n} ] = μ²   ✓$$

4. `scenes[9].solution[3]` Apply Lehmann–Scheffé.

   ```
   X̄² − σ²/n is an unbiased function of a complete sufficient statistic ⟹ it is the UMVUE of μ².
   ```

   Laid out:

   $$X̄² − \frac{σ²}{n} is an unbiased function of a complete sufficient statistic ⟹ it is the UMVUE of μ².$$

**Final answer given to the learner** `scenes[9].answer`

The UMVUE of μ² is X̄² − σ²/n.

**Self-check offered** `scenes[9].check`

Two things to verify before you move on. First, the correction term is σ²/n, not σ² — the variance of the MEAN, not of one observation. Second, this estimator can come out negative when x̄² < σ²/n, even though μ² cannot be. That is not an error in your working; it is a genuine wart of unbiased estimation, and a question may ask you to comment on it.

---

### Scene 11 of 14 — Six statements — verdict on each before you look

`scenes[10]` · id `s10` · type `trapcheck` (true/false check) · 6 minutes

**Purpose** `scenes[10].objective`

Practise the per-statement discipline the real multi-statement items demand.

**Intro** `scenes[10].intro`

Give every statement a true or false verdict first. In the exam these six would be one question scored all or nothing, so a verdict you skipped is a mark you gambled.

- `scenes[10].items[0]` **Claim:** Rao–Blackwell requires the conditioning statistic to be sufficient.  
  **Verdict: TRUE.** True, and it is the condition that makes the result a statistic at all. Without sufficiency, E[δ|T] still contains θ.
- `scenes[10].items[1]` **Claim:** Rao–Blackwellising an unbiased estimator can increase its variance.  
  **Verdict: FALSE.** False. Var(δ) = E[Var(δ|T)] + Var(η), and the first term is non-negative, so Var(η) ≤ Var(δ) always.
- `scenes[10].items[2]` **Claim:** Rao–Blackwell applied to a sufficient but not complete statistic still produces an improvement.  
  **Verdict: TRUE.** True — the variance inequality needs only sufficiency. What you lose without completeness is uniqueness: different starting estimators may give different answers, none of them identifiable as best.
- `scenes[10].items[3]` **Claim:** Lehmann–Scheffé requires the statistic to be complete as well as sufficient.  
  **Verdict: TRUE.** True. Completeness is exactly what forces two unbiased functions of T to coincide, which is where uniqueness comes from.
- `scenes[10].items[4]` **Claim:** A UMVUE, when it exists, is always a sensible estimator of the quantity concerned.  
  **Verdict: FALSE.** False. For a single Poisson observation the UMVUE of e^(−2λ) is (−1)^X, which alternates ±1 while estimating a number in (0,1). Unbiasedness is a constraint, not a guarantee of good behaviour.
- `scenes[10].items[5]` **Claim:** If η is the UMVUE of θ, then η² is the UMVUE of θ².  
  **Verdict: FALSE.** False. That is invariance, which the MLE has and the UMVUE does not. For U(0,θ) the UMVUE of θ² is (n+2)/n·X₍ₙ₎², not the square of (n+1)/n·X₍ₙ₎.

---

### Scene 12 of 14 — Transfer — the UMVUE of θ², and why it is not the square

`scenes[11]` · id `s11` · type `guided` (guided problem) · 9 minutes

**Purpose** `scenes[11].objective`

Derive a second UMVUE in the same family, and see invariance fail in front of you.

**Problem put to the learner** `scenes[11].problem`

X₁,…,Xₙ are iid U(0, θ). Scene 8 gave the UMVUE of θ as (n+1)/n · X₍ₙ₎. Now find the UMVUE of θ², and compare it with the square of that estimator.

**Hint ladder, revealed one at a time** `scenes[11].hints[]`

1. Direction — do not square anything yet. Go back to the definition: you need a function of the complete sufficient statistic whose expectation is exactly θ². The natural candidate is a multiple of X₍ₙ₎².
2. Method — Route B again. Compute E[X₍ₙ₎²] from the density of the maximum, then scale it so the expectation lands on θ² exactly.
3. Next step — the density of X₍ₙ₎ is n x^(n−1)/θⁿ on (0, θ). Integrate x² against it; the integral is elementary and the θ's mostly cancel.

**Model solution, hidden until requested** `scenes[11].solution[]`

1. `scenes[11].solution[0]` Expectation of the squared maximum.

   ```
   E[X₍ₙ₎²] = ∫₀^θ x² · n x^(n−1)/θⁿ dx = (n/θⁿ) · [x^(n+2)/(n+2)]₀^θ = n θ² / (n+2)
   ```

   Laid out:

   $$E[X₍ₙ₎²] = ∫₀^{θ} x² · n \frac{x^{n−1}}{θⁿ} dx = \frac{n}{θⁿ} · \frac{x^{n+2}}{(n+2)}₀^{θ} = \frac{n θ²}{(n+2)}$$

2. `scenes[11].solution[1]` Scale it to be unbiased.

   ```
   E[ (n+2)/n · X₍ₙ₎² ] = θ²   ✓
   ```

   Laid out:

   $$E[ \frac{(n+2)}{n} · X₍ₙ₎² ] = θ²   ✓$$

3. `scenes[11].solution[2]` Apply Lehmann–Scheffé.

   ```
   UMVUE of θ²  =  (n+2)/n · X₍ₙ₎²
   ```

   Laid out:

   $$UMVUE of θ²  =  \frac{(n+2)}{n} · X₍ₙ₎²$$

4. `scenes[11].solution[3]` Now square the UMVUE of θ and compare.

   ```
   [ (n+1)/n · X₍ₙ₎ ]² = (n+1)²/n² · X₍ₙ₎²   versus   (n+2)/n · X₍ₙ₎² = n(n+2)/n² · X₍ₙ₎²
   ```

   Laid out:

   $$[ \frac{(n+1)}{n} · X₍ₙ₎ ]² = \frac{(n+1)²}{n²} · X₍ₙ₎²   versus   \frac{(n+2)}{n} · X₍ₙ₎² = \frac{n(n+2)}{n²} · X₍ₙ₎²$$

5. `scenes[11].solution[4]` They differ.

   ```
   (n+1)² = n² + 2n + 1   and   n(n+2) = n² + 2n.   The squared estimator is larger by X₍ₙ₎²/n², so it is biased upward for θ².
   ```

   Laid out:

   $$(n+1)² = n² + 2n + 1   and   n(n+2) = n² + 2n.   The squared estimator is larger by X₍ₙ₎\frac{²}{n²}, so it is biased upward for θ².$$

**Final answer given to the learner** `scenes[11].answer`

The UMVUE of θ² is (n+2)/n · X₍ₙ₎². Squaring the UMVUE of θ gives (n+1)²/n² · X₍ₙ₎², which overstates θ² by X₍ₙ₎²/n² on average and is therefore not the UMVUE.

**Self-check offered** `scenes[11].check`

The comparison was part of the question, not a flourish — answering with the formula alone leaves marks on the table. And notice what this kills: the habit, built up in the MLE topic, of transforming an estimator and keeping the label. The MLE is invariant; the UMVUE is not. If a question asks for the UMVUE of a function of θ, you must derive it from scratch.

---

### Scene 13 of 14 — What you should now be able to do unaided

`scenes[12]` · id `s12` · type `summary` (summary) · 3 minutes

**Purpose** `scenes[12].objective`

Close the loop before the test.

**Body** `scenes[12].body[]`

Write down any unbiased estimator, however crude, and improve it by conditioning on a sufficient statistic.

Prove Rao–Blackwell from the variance decomposition in one line, and say when the inequality is an equality.

Compute E[δ|T] in the standard cases by identifying the conditional distribution of the sample given its total.

State Lehmann–Scheffé and explain that completeness, not sufficiency, is what delivers uniqueness.

Reach for the direct route — solve E[h(T)] = g(θ) — whenever guessing the form of h is easier than conditioning.

Refuse to square a UMVUE and call the result a UMVUE, and refuse to assume a UMVUE beats the MLE on mean squared error.

The mastery test is ten unseen questions across all of this. Hints are off. The pass is 80% overall with 70% floors on the numerical and multi-statement items.

---

### Scene 14 of 14 — Mastery test

`scenes[13]` · id `s13` · type `quiz` (mastery test) · 12 minutes

**Purpose** `scenes[13].objective`

Demonstrate it independently, on unseen questions.

Draws from the pool reproduced below. `scenes[13].setId` = `inference_t3_mastery`

---

## Revision material `revision`

**Revision sheet** `revision.sheet[]` (14 lines)

1. `[0]` Rao–Blackwell: δ unbiased for g(θ), T sufficient ⟹ η(T) = E[δ|T] is unbiased and Var(η) ≤ Var(δ).
2. `[1]` The proof is one line: Var(δ) = E[Var(δ|T)] + Var(E[δ|T]) ≥ Var(η(T)).
3. `[2]` T must be SUFFICIENT, or E[δ|T] still contains θ and is not a statistic.
4. `[3]` The inequality is ≤, not <. It is an equality exactly when δ was already a function of T.
5. `[4]` Lehmann–Scheffé: T complete sufficient and η(T) unbiased ⟹ η(T) is THE UMVUE, unique almost surely.
6. `[5]` Completeness is what gives uniqueness: two unbiased functions of T differ by an unbiased estimator of zero.
7. `[6]` Two routes to a UMVUE: Rao–Blackwellise any crude unbiased δ, or solve E[h(T)] = g(θ) for h directly.
8. `[7]` Poisson, g = e^(−λ):  UMVUE = ((n−1)/n)^T.   Bernoulli, g = p²:  UMVUE = T(T−1)/(n(n−1)).
9. `[8]` Exponential rate λ:  MLE = n/Σxᵢ (biased),  UMVUE = (n−1)/Σxᵢ.
10. `[9]` U(0,θ):  UMVUE of θ = (n+1)/n · x₍ₙ₎.   UMVUE of θ² = (n+2)/n · x₍ₙ₎².
11. `[10]` N(μ,σ²), σ² known:  UMVUE of μ² = x̄² − σ²/n. It can come out negative — UMVUEs are not obliged to be sensible.
12. `[11]` A UMVUE is not invariant: the UMVUE of g(θ) is not g(UMVUE of θ). The MLE is invariant; this is the difference.
13. `[12]` No complete sufficient statistic (curved family) ⟹ Lehmann–Scheffé says nothing.
14. `[13]` Unbiased does not mean smaller MSE. For σ², the MLE beats s² on mean squared error.

**Flashcards** `revision.cards[]`

| Front | Back |
|---|---|
| Rao–Blackwell, in one sentence | Conditioning an unbiased estimator on a sufficient statistic keeps it unbiased and cannot increase its variance. |
| Why T must be sufficient | Otherwise the conditional distribution still depends on θ, so E[δ|T] is not computable from data alone. |
| The one-line proof | Var(δ) = E[Var(δ|T)] + Var(E[δ|T]). The first term is ≥ 0, so Var(E[δ|T]) ≤ Var(δ). |
| When does Rao–Blackwell change nothing? | When δ is already a function of T. Then E[δ|T] = δ and the variance is unchanged. |
| What completeness adds | Uniqueness. Without it you get an improvement; with it you get THE best, and every starting point lands on the same answer. |
| Two routes to a UMVUE | Rao–Blackwellise any unbiased estimator, or solve E[h(T)] = g(θ) directly for h. |
| Is the UMVUE invariant? | No. The UMVUE of θ² is (n+2)/n·x₍ₙ₎², not the square of (n+1)/n·x₍ₙ₎. Only the MLE has invariance. |
| Can a UMVUE be absurd? | Yes. For a single Poisson observation the UMVUE of e^(−2λ) is (−1)^X — it alternates ±1 while estimating a number in (0,1). |

**Memory aids** `revision.tricks[]`

- `[0]` **RB improves, LS certifies** — Rao–Blackwell lowers the variance; completeness is what turns 'better' into 'best'.
- `[1]` **Condition on T, never on θ** — E[δ | T] is computable precisely because T is sufficient. Conditioning on θ would not be a statistic.
- `[2]` **Already a function of T? You are done** — E[δ | T] = δ and there is no improvement left — that is the equality case, and the signal to stop.
- `[3]` **Best unbiased ≠ efficient** — A UMVUE can sit strictly above the Cramér–Rao floor. The exponential rate is the standard case.

**Elimination shortcuts for multiple-choice items** `revision.shortcuts[]`

- `[0]` Guess an unbiased function of T and correct it — completeness means whatever you find IS the UMVUE.
- `[1]` Poisson: UMVUE of λ² is T(T−1)/n²; of e^(−λ) is ((n−1)/n)^T.
- `[2]` Bernoulli: UMVUE of p² is T(T−1)/(n(n−1)).
- `[3]` U(0,θ): UMVUE of θ is (n+1)X₍ₙ₎/n, variance θ²/(n(n+2)) — an n⁻² rate.

**If nothing else is remembered** `revision.remember[]`

- `[0]` Rao–Blackwell needs sufficiency only. Uniqueness needs completeness as well.
- `[1]` The improvement is strict unless the estimator was already a function of T.

**Errors to avoid** `revision.traps[]`


---

## Mastery pool — all 20 items with answer keys `qsets/mastery`

Ten are drawn per attempt at 3 easy / 5 moderate / 2 hard. Keys are distributed five to each option letter. Please check each item for a second defensible answer as well as for the correctness of its stated key and explanation.

### Q1 — `inf-t3-m-01` *(single, easy)*

Rao–Blackwell guarantees that η(T) = E[δ(X) | T] satisfies:

*Options* `.options[]`:

- **A.** η is unbiased and Var(η) ≤ Var(δ), provided T is sufficient  ← key
- **B.** η is the UMVUE, provided T is sufficient
- **C.** η is unbiased and Var(η) < Var(δ), for any statistic T
- **D.** η has smaller mean squared error than δ, provided T is complete

*Explanation* `.explanation`: Unbiasedness comes from the tower property; the variance inequality from Var(δ) = E[Var(δ|T)] + Var(η). Option C overstates it twice: the inequality is not strict, and T must be sufficient or η is not even a statistic. Option B skips completeness, without which there is no uniqueness and so no UMVUE claim.

### Q2 — `inf-t3-m-02` *(numeric, moderate)*

X₁,…,X₅ are iid Poisson(λ) with ΣXᵢ = 3. The UMVUE of e^(−λ) is ((n−1)/n)^T. Give its value.

*Options* `.options[]`:

- **A.** 0.600
- **B.** 0.512  ← key
- **C.** 0.549
- **D.** 0.216

*Explanation* `.explanation`: ((n−1)/n)^T = (4/5)³ = 0.512. Option C is e^(−0.6), the plug-in estimate e^(−λ̂) with λ̂ = x̄ = 0.6 — a perfectly reasonable estimator but a biased one, and not the UMVUE. Option D is (3/5)³ and option A is x̄ itself.

*Arithmetic check* `.check`: The base is (n−1)/n = 4/5, not x̄ and not T/n. Confirm which of n and T goes in the exponent before you compute.

### Q3 — `inf-t3-m-03` *(multi, hard)*

Consider Lehmann–Scheffé and the UMVUEs it produces.

*Statements to judge* `.statements[]`:

- **A.** If T is complete sufficient and η(T) is unbiased for g(θ), then η(T) is the unique UMVUE.
- **B.** Sufficiency of T alone is enough for the uniqueness conclusion.
- **C.** A UMVUE can take values outside the range of the quantity it estimates.
- **D.** The UMVUE of g(θ) need not equal g applied to the UMVUE of θ.

*Options* `.options[]`:

- **A.** A, B and D only
- **B.** A and B only
- **C.** A, C and D only  ← key
- **D.** B and C only

*Explanation* `.explanation`: A is true — that is the statement. B is false: completeness is required, and without it the theorem is silent. C is true, and is the standard pathology. D is true — the UMVUE is not invariant, unlike the MLE.

*Verdict on each statement* `.verdicts`:

- **A — true.** The theorem exactly as stated, with uniqueness holding almost surely.
- **B — false.** Without completeness you get Rao–Blackwell's improvement but no uniqueness.
- **C — true.** X̄² − σ²/n can be negative while μ² cannot; (−1)^X estimates a number in (0,1).
- **D — true.** UMVUEs are not invariant. For U(0,θ), the UMVUE of θ² is (n+2)/n·X₍ₙ₎², not the square of the UMVUE of θ.

### Q4 — `inf-t3-m-04` *(numeric, moderate)*

X₁,…,X₆ are iid Bernoulli(p) with ΣXᵢ = 4. The UMVUE of p² is T(T−1)/(n(n−1)). Give its value, and say how it compares with p̂².

*Options* `.options[]`:

- **A.** 0.444, which equals p̂²
- **B.** 0.400, which is larger than p̂² = 0.333
- **C.** 0.267, which is smaller than p̂² = 0.444
- **D.** 0.400, which is smaller than p̂² = 0.444  ← key

*Explanation* `.explanation`: T(T−1)/(n(n−1)) = 4·3/(6·5) = 12/30 = 0.400, while p̂² = (4/6)² = 0.444. The plug-in estimator is biased upward for p², and the UMVUE sits below it — which is the correction the (T−1) and (n−1) supply.

*Arithmetic check* `.check`: Two parts: the value and the comparison. If you computed only 0.4, confirm p̂² before choosing, because three options carry that same number.

### Q5 — `inf-t3-m-05` *(single, moderate)*

For which situation does Lehmann–Scheffé fail to deliver a UMVUE?

*Options* `.options[]`:

- **A.** N(θ, θ²) with θ > 0, where the minimal sufficient statistic is not complete  ← key
- **B.** U(0, θ), where X₍ₙ₎ is complete sufficient
- **C.** Bernoulli(p), where T = ΣXᵢ is complete sufficient
- **D.** Poisson(λ), where T = ΣXᵢ is complete sufficient

*Explanation* `.explanation`: N(θ,θ²) is a curved exponential family: (ΣXᵢ, ΣXᵢ²) is minimal sufficient but not complete, so the theorem has nothing to act on. A UMVUE may still exist, but Lehmann–Scheffé cannot identify it. The other three are full-rank families whose sufficient statistic is complete.

### Q6 — `inf-t3-m-06` *(numeric, moderate)*

X₁,…,X₈ are iid U(0,θ) with sample maximum x₍₈₎ = 6. Give the UMVUE of θ and the MLE of θ.

*Options* `.options[]`:

- **A.** UMVUE = 6, MLE = 6.75
- **B.** UMVUE = 6.75, MLE = 6  ← key
- **C.** UMVUE = 5.33, MLE = 6
- **D.** UMVUE = 6.75, MLE = 6.75

*Explanation* `.explanation`: The UMVUE is (n+1)/n · x₍ₙ₎ = (9/8)(6) = 6.75; the MLE is x₍ₙ₎ = 6 itself. The UMVUE must exceed the sample maximum, because the maximum can never exceed θ and so understates it. Option C scales the wrong way, making the bias worse.

*Arithmetic check* `.check`: The multiplier is (n+1)/n = 9/8, greater than 1. Any answer below the sample maximum is wrong on sight.

### Q7 — `inf-t3-m-07` *(multi, hard)*

Let δ be an unbiased estimator of g(θ) and let T be a statistic.

*Statements to judge* `.statements[]`:

- **A.** Rao–Blackwellising always strictly reduces the variance.
- **B.** E[E[δ|T]] = g(θ) whenever δ is unbiased.
- **C.** If T is not sufficient, E[δ|T] may depend on θ and so may not be a statistic.
- **D.** A UMVUE has the smallest mean squared error among all estimators.

*Options* `.options[]`:

- **A.** A and B only
- **B.** A, B and C only
- **C.** B and C only  ← key
- **D.** C and D only

*Explanation* `.explanation`: A is false — equality holds whenever δ is already a function of T, so the improvement need not be strict. B is true, by the tower property. C is true, and is the point of requiring sufficiency. D is false: unbiasedness restricts the comparison to unbiased estimators, and a biased estimator can have smaller MSE.

*Verdict on each statement* `.verdicts`:

- **A — false.** It is ≤. Equality when Var(δ|T) = 0, i.e. δ already depends on the data only through T.
- **B — true.** The tower property, needing nothing beyond δ being unbiased.
- **C — true.** Sufficiency is exactly what frees the conditional distribution of θ.
- **D — false.** Smallest variance among UNBIASED estimators only. The MLE of σ² beats s² on MSE.

### Q8 — `inf-t3-m-08` *(numeric, moderate)*

X₁,…,X₆ are iid Exponential with rate λ and Σxᵢ = 24. Give the MLE of λ and the UMVUE of λ.

*Options* `.options[]`:

- **A.** MLE = 0.250, UMVUE = 0.250
- **B.** MLE = 4.000, UMVUE = 4.800
- **C.** MLE = 0.2083, UMVUE = 0.250
- **D.** MLE = 0.250, UMVUE = 0.2083  ← key

*Explanation* `.explanation`: The MLE is n/Σxᵢ = 6/24 = 0.250. Since E[1/ΣX] = λ/(n−1), the unbiased version is (n−1)/Σxᵢ = 5/24 = 0.2083, and ΣX is complete sufficient so Lehmann–Scheffé makes it the UMVUE. Option C swaps them; option B gives the mean 1/λ rather than the rate.

*Arithmetic check* `.check`: The UMVUE is the MLE shrunk by (n−1)/n, so it must be the SMALLER of the two. If your UMVUE came out larger, you scaled the wrong way.

### Q9 — `inf-t3-m-09` *(numeric, hard)*

X₁,…,X₁₀ are iid N(μ, σ²) with σ² = 5 known, and x̄ = 4. Give the UMVUE of μ².

*Options* `.options[]`:

- **A.** 15.5  ← key
- **B.** 16.0
- **C.** 11.0
- **D.** 16.5

*Explanation* `.explanation`: X̄ is complete sufficient for μ. E[X̄²] = Var(X̄) + μ² = σ²/n + μ², so the UMVUE is x̄² − σ²/n = 16 − 5/10 = 15.5. Option B is x̄² itself, which overstates μ² by σ²/n. Option C subtracts σ² rather than σ²/n.

*Arithmetic check* `.check`: The correction is the variance of the MEAN, σ²/n = 0.5, not σ² = 5. Subtracting the wrong one is the commonest slip in this item.

### Q10 — `inf-t3-m-10` *(order, easy)*

To find a UMVUE by Rao–Blackwellisation, arrange these steps in the order they are carried out.

*Steps to order* `.items[]`:

- A. Find any unbiased estimator δ of g(θ), however crude
- B. Invoke Lehmann–Scheffé to declare the result the UMVUE
- C. Identify a complete sufficient statistic T
- D. Compute η(T) = E[δ | T] using the conditional distribution given T

*Options* `.options[]`:

- **A.** A, C, D, B
- **B.** C, A, D, B  ← key
- **C.** C, D, A, B
- **D.** D, C, A, B

*Explanation* `.explanation`: Identify the complete sufficient statistic first — it determines whether the method applies at all and what you will condition on. Then find any unbiased estimator, compute the conditional expectation, and finally invoke Lehmann–Scheffé. Starting by hunting for an unbiased estimator wastes effort if no complete sufficient statistic exists.

### Q11 — `inf-t3-m-11` *(single, easy)*

The Rao–Blackwell theorem requires that:

*Options* `.options[]`:

- **A.** the loss function is squared error and nothing else
- **B.** T is complete, so that the conditional expectation is unique
- **C.** T is sufficient, so that E[δ(X) | T] does not depend on θ  ← key
- **D.** δ is the maximum likelihood estimator

*Explanation* `.explanation`: Sufficiency is what makes E[δ(X) | T] a statistic at all — without it the conditional expectation would still involve θ and could not be computed from the data. Completeness is the extra ingredient Lehmann–Scheffé adds to get uniqueness; Rao–Blackwell alone does not need it. The result holds for any convex loss, squared error being the familiar case.

### Q12 — `inf-t3-m-12` *(numeric, moderate)*

X₁,…,X₄ are iid Poisson(λ) with ΣXᵢ = 8. The UMVUE of λ² is T(T−1)/n². Give its value.

*Options* `.options[]`:

- **A.** 4
- **B.** 4.5
- **C.** 2
- **D.** 3.5  ← key

*Explanation* `.explanation`: T(T−1)/n² = 8(7)/16 = 56/16 = 3.5. The naive x̄² = 2² = 4 is biased upward: E[X̄²] = λ² + λ/n, so the correction subtracts exactly that bias.

*Arithmetic check* `.check`: The UMVUE of λ² should come out BELOW x̄², since x̄² overestimates. If yours is larger, the correction has the wrong sign.

### Q13 — `inf-t3-m-13` *(multi, hard)*

Consider Rao–Blackwellisation and what it delivers.

*Statements to judge* `.statements[]`:

- **A.** Var(E[δ|T]) ≤ Var(δ), with equality only when δ is already a function of T.
- **B.** Rao–Blackwell alone proves the improved estimator is the UMVUE.
- **C.** E[δ|T] is free of θ because T is sufficient.
- **D.** The improvement holds for any convex loss function.

*Options* `.options[]`:

- **A.** A, C and D only  ← key
- **B.** B, C and D only
- **C.** A, B and C only
- **D.** A and B only

*Explanation* `.explanation`: A is true — conditioning on a sufficient statistic cannot increase the variance, and strictly decreases it unless δ was already a function of T. B is false: Rao–Blackwell preserves unbiasedness but gives no uniqueness, which is what Lehmann–Scheffé adds. C is true, and it is why the improved estimator is computable. D is true: the result holds for any convex loss, not only squared error.

*Verdict on each statement* `.verdicts`:

- **A — true.** The conditional variance decomposition: Var(δ) = Var(E[δ|T]) + E[Var(δ|T)].
- **B — false.** Uniqueness needs completeness. Rao–Blackwell improves; Lehmann–Scheffé certifies.
- **C — true.** That is exactly what sufficiency buys — the conditional law is parameter-free.
- **D — true.** Jensen's inequality applied conditionally, so convexity is all that is needed.

### Q14 — `inf-t3-m-14` *(numeric, moderate)*

X₁,…,X₉ are iid N(μ, σ²) with σ² = 18 known, and x̄ = 5. The UMVUE of μ² is X̄² − σ²/n. Give its value.

*Options* `.options[]`:

- **A.** 25
- **B.** 23  ← key
- **C.** 27
- **D.** 2

*Explanation* `.explanation`: X̄² − σ²/n = 25 − 18/9 = 25 − 2 = 23. The subtraction removes the bias in X̄², since E[X̄²] = μ² + σ²/n. X̄ is complete sufficient for μ, so this unbiased function of it is the UMVUE.

*Arithmetic check* `.check`: σ²/n = 2, not σ² = 18. Subtracting the whole variance instead of the variance of the MEAN is the slip the question is built around.

### Q15 — `inf-t3-m-15` *(single, moderate)*

Rao–Blackwellising an estimator that is already a function of the complete sufficient statistic:

*Options* `.options[]`:

- **A.** always strictly reduces the variance
- **B.** makes the estimator biased
- **C.** returns the same estimator, with no improvement  ← key
- **D.** is not permitted by the theorem

*Explanation* `.explanation`: If δ is already a function of T then E[δ|T] = δ, so nothing changes. That is the equality case of the theorem, and it is also the signal that you have already arrived: an unbiased function of the complete sufficient statistic is the UMVUE and cannot be improved.

### Q16 — `inf-t3-m-16` *(numeric, hard)*

X₁,…,Xₙ are iid Bernoulli(p), T = ΣXᵢ. Starting from the crude unbiased estimator δ = X₁ of p, compute E[δ | T = t] and identify the resulting estimator.

*Options* `.options[]`:

- **A.** t, the total
- **B.** t(t−1)/(n(n−1))
- **C.** 1/n
- **D.** t/n, the sample proportion  ← key

*Explanation* `.explanation`: Given T = t, the t successes are equally likely to sit in any of the n positions, so P(X₁ = 1 | T = t) = t/n. Hence E[X₁ | T = t] = t/n = x̄. Rao–Blackwellising the crudest possible unbiased estimator — look at the first observation only — delivers the sample proportion, and since T is complete sufficient, Lehmann–Scheffé certifies it as the UMVUE.

*Arithmetic check* `.check`: Sanity-check unbiasedness at the end: E[T/n] = np/n = p ✓. Option B is the UMVUE of p², not of p.

### Q17 — `inf-t3-m-17` *(multi, moderate)*

Consider Lehmann–Scheffé in practice.

*Statements to judge* `.statements[]`:

- **A.** An unbiased function of a complete sufficient statistic is the unique UMVUE.
- **B.** You may find the UMVUE by correcting the bias of any function of T.
- **C.** The UMVUE produced always attains the Cramér–Rao bound.
- **D.** Without completeness, the uniqueness conclusion fails.

*Options* `.options[]`:

- **A.** A, B and D only  ← key
- **B.** A and C only
- **C.** B and C only
- **D.** A, B and C only

*Explanation* `.explanation`: A is true — that is the theorem's conclusion. B is true: finding ANY unbiased function of the complete sufficient statistic is enough, which is why guessing and correcting works. C is false: a UMVUE need not attain the Cramér–Rao bound, as the exponential rate shows. D is true — without completeness you may have several unbiased functions of T and no way to choose.

*Verdict on each statement* `.verdicts`:

- **A — true.** Lehmann–Scheffé, with uniqueness almost surely.
- **B — true.** Any unbiased function will do — there is only one, so whichever you find is it.
- **C — false.** (n−1)/ΣX has variance λ²/(n−2), strictly above the floor λ²/n.
- **D — true.** Completeness is precisely what rules out a second unbiased function of T.

### Q18 — `inf-t3-m-18` *(numeric, moderate)*

X₁,…,X₁₂ are iid U(0,θ) with x₍₁₂₎ = 9. Give the UMVUE of θ and its variance formula.

*Options* `.options[]`:

- **A.** x₍ₙ₎ = 9, with variance θ²/n
- **B.** (n+1)x₍ₙ₎/n = 9.75, with variance θ²/(n(n+2))  ← key
- **C.** 2x̄, with variance θ²/(3n)
- **D.** (n+1)x₍ₙ₎/n = 9.75, with variance θ²/n

*Explanation* `.explanation`: X₍ₙ₎ is complete sufficient for θ, and (n+1)X₍ₙ₎/n is its unbiased multiple, so Lehmann–Scheffé makes it the UMVUE: (13/12)(9) = 9.75. Its variance is θ²/(n(n+2)), of order n⁻² — faster than the 1/n rate any regular family could manage, which is possible only because the support depends on θ and the Cramér–Rao conditions fail.

*Arithmetic check* `.check`: Two parts here and the second is the one candidates drop. An O(n⁻²) variance is the fingerprint of a boundary-support family.

### Q19 — `inf-t3-m-19` *(single, hard)*

A UMVUE exists and has been found, yet its variance exceeds the Cramér–Rao bound. What does this tell you?

*Options* `.options[]`:

- **A.** A better unbiased estimator exists but has not been found
- **B.** The UMVUE has been computed incorrectly
- **C.** Nothing is wrong — the bound need not be attainable, and the UMVUE is still the best unbiased estimator  ← key
- **D.** The regularity conditions must have failed

*Explanation* `.explanation`: Being the best unbiased estimator and sitting on the Cramér–Rao floor are different achievements. The bound is attained only when the score factorises as A(θ)[T − g(θ)]; when it does not, the floor is simply unreachable and the UMVUE sits above it. The exponential rate is the standard case: UMVUE variance λ²/(n−2) against a floor of λ²/n.

### Q20 — `inf-t3-m-20` *(order, easy)*

To find a UMVUE by Lehmann–Scheffé, arrange these steps.

*Steps to order* `.items[]`:

- A. Produce an unbiased function of that statistic
- B. Verify the statistic is complete
- C. Identify a sufficient statistic for θ
- D. Conclude it is the unique UMVUE

*Options* `.options[]`:

- **A.** A, B, C, D
- **B.** B, C, A, D
- **C.** C, A, B, D
- **D.** C, B, A, D  ← key

*Explanation* `.explanation`: Find the complete sufficient statistic first — everything downstream is stated in terms of it. Then verify completeness, since without it the conclusion is only Rao–Blackwell. Then produce some unbiased function of that statistic, and conclude it is the unique UMVUE.

---

## Authoring and verification record `provenance`

Reproduced verbatim. It records what changed in each version and how each derivation was checked, including the findings of the two previous review rounds and the reasons some of their recommendations were declined.

> Review pass, October 2026: 3 per-scene quick checks added on theory, worked and explore scenes from a third-party module review, each read for correctness before import; a further set offered for completion and guided scenes was declined, since those scenes already end with the learner writing an answer. The same pass qualified an unrelated overclaim the review did not flag: MLE invariance was stated as holding 'always', which needs the existence of an MLE and the induced-likelihood convention. Theory, worked examples and practice authored for this platform against the UGC NET Statistics syllabus. Previous-year questions are stored separately and carry their exam cycle.

