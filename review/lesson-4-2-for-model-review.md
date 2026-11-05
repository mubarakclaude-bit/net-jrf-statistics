# Lesson 4.2 — Completeness, Exponential Families, Ancillarity and Basu

Complete authored content of one lesson from a UGC-NET Statistics (Code 107) preparation application, extracted from the application's own content files.

| | |
|---|---|
| Content version | 1.3 |
| Scenes | 14 |
| Core scenes | 14 |
| Optional JRF-extension scenes | 0 |
| Estimated learner time | 51 minutes |
| Mastery pool | 20 items |
| Position in the app | Statistical Inference → Data Reduction → Completeness |
| Engine | Estimation and inference — likelihood families, and what makes one rich enough to pin an estimator down |
| Pool label | Completeness and Basu — mastery test (unseen) |
| Unit | IV — Statistical Inference |
| Audience | JRF-target candidates, many returning after several years away |

## Before you start: where this lesson sits

This lesson is at content version **1.3**. The application's current authoring standard is 4.1, and three of its requirements are **known** to be unmet here, so please do not spend effort reporting them — they are scheduled work, not findings:

- no short "how to use this lesson" note on the overview;
- a quick check on only some teaching scenes rather than all of them;
- no family-to-statistic style reference table where one would help.

This lesson is also **51 minutes against a house standard of about 90**, so it is thinner than intended. Comments on what is MISSING in substance are therefore especially useful — but please flag omissions rather than proposing to shorten what is there.

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

1. State completeness as a property of a family of distributions, and say why it is not a property of a statistic on its own.

2. Prove a statistic complete by the standard route: set E[g(T)] = 0, and use uniqueness of a power series, a polynomial or an integral.

3. Read completeness off the exponential-family form, and recognise a curved family where that argument fails.

4. Identify an ancillary statistic and apply Basu's theorem to get independence without touching a joint density.

5. Disprove completeness by constructing a non-trivial unbiased estimator of zero.

6. Keep sufficient, minimal, complete and ancillary apart — the exam tests the boundaries, not the definitions.

**Assumed prior knowledge** `prereq[]`

- `prereq[0]` **Sufficiency and the factorisation theorem** — Completeness is always asked about a sufficient statistic. If finding T is still slow, do the sufficiency topic first.
- `prereq[1]` **Expectation of a function of a statistic** — Every completeness proof starts by writing E[g(T)] out as a sum or an integral.
- `prereq[2]` **Power series and polynomial identities** — The proofs all end the same way: a series that vanishes on an interval has every coefficient zero. That step is the whole argument.

**Misconceptions the lesson is built to pre-empt** `traps[]`

- Calling a statistic complete without naming the family it is complete for.

- Assuming minimal sufficient implies complete — curved families are the counterexample.

- Applying the exponential-family criterion to a family whose support moves with θ.

- Forgetting that the natural parameter space must contain an open rectangle, not just two or three points.

- Using Basu without checking that T is complete as well as sufficient.

- Treating 'ancillary' as 'useless' — an ancillary statistic is exactly what Basu needs, and it can still matter when you condition.

- Proving E[g(T)] = 0 for one θ and concluding completeness. It must hold for every θ in Θ.

**Assessment policy** `mastery`

- 10 items drawn per attempt from a pool of 20, mix 3 easy, 5 moderate, 2 hard
- pass mark 80%, no hints during the test, retest after 7 days
- `mastery.note`: Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the difficulty mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split.

**Sources** `refs[]`

- `refs[0]` **The Exponential Criterion** — Penn State STAT 415 online notes, Lesson 24.3 (Course notes, free). Puts Bernoulli, Poisson, Normal, Exponential and Geometric into exponential form one at a time. Read it alongside scene 7 if rearranging a density into h(x)c(θ)exp(Σw t) is the step that slows you down.
- `refs[1]` **Mathematical Statistics — Exponential Families I and II** — MIT OpenCourseWare 18.655 (Spring 2016), Lecture notes 7 and 8 (Lecture notes, free). The natural parameter space and the full-rank condition stated properly. This is the source for the completeness criterion in scene 7, and for why curved families fall outside it.
- `refs[2]` **Mathematical Statistics — Unbiased Estimation and Risk Inequalities** — MIT OpenCourseWare 18.655 (Spring 2016), Lecture note 13 (Lecture notes, free). Where completeness earns its keep: Rao–Blackwell and Lehmann–Scheffé. Reach for it after scene 1, when you want to see the payoff before doing the proofs.

---

## The lesson, scene by scene

### Scene 1 of 14 — Before the lesson — four things it will assume

`scenes[0]` · id `s0` · type `foundation` (prerequisite check) · 6 minutes

**Purpose** `scenes[0].objective`

Check the three pieces of machinery every completeness argument is built from, before the first proof.

**Body** `scenes[0].body[]`

Completeness is the one idea in this module that looks like pure algebra, and that is exactly what it is: you write E[g(T)] = 0 for every θ and then argue that g must have been zero all along. The argument is short. It is also unforgiving if the algebra underneath is rusty.

Three of these four checks are the algebra. The first is the topic that comes before this one — if it is shaky, finish sufficiency first; this lesson will assume you can produce T without thinking.

**Check 1** `scenes[0].items[0]`

- *asks:* What does the factorisation theorem say, and why is completeness always asked about a sufficient statistic?
- *expected answer* `.recall`: If f(x;θ) = g(T(x);θ)h(x) with h free of θ, then T is sufficient. Completeness is a property of the distribution family of T, and it is useful only because of Lehmann–Scheffé — which needs T to be both complete and sufficient.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Sufficiency says nothing was lost. Completeness says nothing is wasted: the family of distributions of T is rich enough that no non-trivial function of T can average to zero at every θ.

> Alone, completeness is a curiosity. Paired with sufficiency it gives uniqueness — one and only one unbiased function of T — and that is what makes an estimator provably best. So every exam question about completeness is really a question about the pair.

> If writing down T is still slow, do the sufficiency topic first. Everything here starts after that step.

**Check 2** `scenes[0].items[1]`

- *asks:* Write E[g(T)] out as an expression, for a discrete T and for a continuous T.
- *expected answer* `.recall`: Discrete: Σ_t g(t)P(T=t), summed over the support. Continuous: ∫ g(t)f_T(t)dt over the support. Every completeness argument begins by writing one of these and ends by asking what 'this is 0 for all θ' forces on g.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Expectation of a function of a random variable does not need the distribution of that function. You weight g(t) by the probability of t and add up: that is the law of the unconscious statistician, and it is why no change of variable is needed.

> Write the binomial case out in full, because the lesson's first proof is exactly this: E[g(T)] = Σ_(t=0)^n g(t)·C(n,t)p^t(1−p)^(n−t).

> And the continuous template, for a one-parameter exponential-family T: E[g(T)] = ∫ g(t)·c(θ)h(t)e^(θt)dt. Setting that to zero for all θ is a statement about a transform of g, which is why these proofs end in a uniqueness argument rather than algebra.

**Check 3** `scenes[0].items[2]`

- *asks:* A power series Σaₖzᵏ equals zero for every z in an interval. What follows about the coefficients?
- *expected answer* `.recall`: Every aₖ is zero. A power series that is not identically zero has isolated roots — at most countably many — so it cannot vanish on a whole interval.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> This is the step that finishes almost every completeness proof, so it is worth having a picture of. A nonzero polynomial of degree m has at most m roots; a nonzero power series behaves the same way locally. Vanishing everywhere on an interval is therefore only possible if there was nothing there to begin with.

> See it used. For binomial completeness, set E[g(T)] = 0 and divide through by (1−p)ⁿ, which is never zero for p in (0,1). With z = p/(1−p), which sweeps all of (0,∞) as p sweeps (0,1), you are left with Σ_(t=0)^n g(t)C(n,t)zᵗ = 0 for every z > 0.

> That is a polynomial in z vanishing on an interval, so every coefficient g(t)C(n,t) is zero, and since C(n,t) > 0, g(t) = 0 for t = 0,…,n. Completeness proved. Notice that the family had to contain enough values of p for z to sweep an interval — the same proof fails if p can only be 1/3 or 1/2.

**Check 4** `scenes[0].items[3]`

- *asks:* What is the support of a distribution, and why is the conclusion 'g(T) = 0 with probability one' rather than 'g is the zero function'?
- *expected answer* `.recall`: The support is the set of values T actually takes with positive probability. Completeness forces g to vanish there and says nothing about g anywhere else, so the honest conclusion is P(g(T)=0) = 1 for every θ.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> For a binomial T the support is {0,1,…,n}: the argument pins down n+1 numbers. g(17.5) is simply never consulted, because T never takes that value.

> This is not pedantry — it is how a question gets set. 'T is complete, g(T) has expectation zero, therefore g ≡ 0' is a false option; the true one says 'almost surely' or 'with probability one'. Read the options for that phrase.

> It also explains why the unbiased function of a complete sufficient statistic is unique only up to sets of probability zero: two estimators that differ nowhere that matters are counted as the same estimator.

---

### Scene 2 of 14 — A family too rich to hide anything in

`scenes[1]` · id `s1` · type `intuition` (intuition) · 5 minutes

**Purpose** `scenes[1].objective`

Meet completeness as a statement about a whole family of distributions.

**Body** `scenes[1].body[]`

Suppose you have a sufficient statistic T, and someone hands you a function g and claims that E[g(T)] = 0. If they mean under one particular θ, that is easy — plenty of non-zero functions average to zero somewhere.

Now make the claim far harder. Insist that E_θ[g(T)] = 0 for EVERY θ in the family. One function, one equation, but the equation has to hold simultaneously across the whole parameter space.

For a rich enough family, that is impossible unless g was zero all along. The distributions of T move around so much as θ varies that no fixed non-zero function can keep averaging to zero against all of them. A family with that property is called complete.

This is why the property belongs to the family and not to T. The same statistic can be complete under one model and fail under another, because what changed was the collection of distributions, not the function of the data.

The payoff is uniqueness. Rao–Blackwell says conditioning an unbiased estimator on a sufficient statistic cannot make it worse. Completeness says there is only one unbiased function of T to land on — so the improvement has a single destination. That is Lehmann–Scheffé, and it is the reason this definition is in the syllabus at all.

**Aside — The phrasing that makes the definition click** `scenes[1].aside.body`

Read E_θ[g(T)] = 0 ∀θ ⟹ g ≡ 0 as: the only unbiased estimator of zero that depends on the data through T is the trivial one. If a second one existed, you could add it to any unbiased estimator and get a different unbiased estimator — and uniqueness would be gone.

**Quick check before moving on** `scenes[1].ask`

- *question:* Why does 'the only unbiased estimator of zero is zero' force the unbiased estimator built on T to be unique?
- *hint on request:* Suppose two different unbiased estimators of θ were both functions of T. What is the expectation of their difference?

**Optional deep-dive, opened on demand — The X̄ chart and the R chart, and why Basu lets you trust both** `scenes[1].scenario`

*teaser on the closed card:* Why a factory runs two control charts, and why they can be read independently.

> A plant machining bearing races measures an internal diameter on five parts every hour. Two charts go up on the wall: an X̄ chart tracking the mean of each sample, and an R chart tracking the range within it. The operator is told to read them separately — a signal on one does not contaminate the other.

> That instruction is Basu's theorem wearing overalls. Treat the process as normal with known spread σ while the mean μ drifts. Then X̄ is a complete sufficient statistic for μ. The range R = X₍₅₎ − X₍₁₎ is unchanged if you shift every measurement by a constant, so its distribution does not involve μ at all — R is ancillary.

> Complete and sufficient on one side, ancillary on the other: Basu gives independence immediately, with no distribution theory at all. The two charts carry non-overlapping information, which is exactly why a shift in the mean does not inflate the range chart and a widening spread does not drag the mean chart off centre.

> The practical payoff is diagnostic. A signal on X̄ alone points at a setting that has moved — tool offset, thermal growth, a changed fixture. A signal on R alone points at variability — a loose spindle, inconsistent material. If the two were dependent you could not read them apart, and every alarm would be ambiguous.

*think-it-through question* `.q`: The quality engineer now says σ is also unknown and must be estimated from the same data. Does the independence argument survive?

*what the statistics says* `.answer`: The conclusion survives, but this argument does not. With σ unknown, R is no longer ancillary — its distribution depends on σ, which is now a parameter — so Basu cannot be applied in that form. Independence of X̄ and S² for the normal is still true, but it needs the direct distributional proof rather than Basu. This is the trap the exam sets: Basu's hypotheses have to be checked against the parameters actually unknown, not the ones you wish were known.

*link line* `.link`: The same structure underlies residual analysis in regression: residuals are ancillary for the regression coefficients, which is why they are free to be used for checking the model that produced them.

---

### Scene 3 of 14 — A family of likelihoods that sweeps the whole line

`scenes[2]` · id `s2` · type `explore` (interactive visualisation) · 5 minutes

**Purpose** `scenes[2].objective`

See the richness that completeness is really asking for.

**Body** `scenes[2].body[]`

This is the exponential sample again: L(λ) = λⁿ e^(−λΣxᵢ). The data reach it only through n and Σxᵢ, so Σxᵢ is sufficient — that much is the previous topic.

Completeness asks something extra, and it is about the curve rather than the data. Drag λ and notice that the family of densities of T = ΣXᵢ really does move: T is Gamma(n, λ), and as λ runs over all of (0, ∞) the natural parameter −λ sweeps an entire open interval.

That sweep is the condition. A one-parameter exponential family whose natural parameter covers an open interval is full rank, and its sufficient statistic is complete. Nothing non-trivial can average to zero against all of those distributions at once.

Contrast it with a family where λ were allowed only two values. Sufficiency would be unchanged — the likelihood still sees only Σxᵢ — but two equations cannot pin a whole function down, and completeness would fail. Same statistic, different family, different answer.

**Interactive element** `scenes[2].viz` — live plot of type `exp-likelihood`, initial state n=4, sumx=16.0. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[2].ask`

- *question:* Sufficiency and completeness are both being claimed for Σxᵢ here. Which of the two would survive if λ were restricted to {1, 2}, and which would not?
- *hint on request:* Does restricting θ change how the data enter the likelihood? Does it change how many equations E[g(T)] = 0 has to satisfy?

---

### Scene 4 of 14 — The definition, and the one proof technique

`scenes[3]` · id `s3` · type `theory` (theory) · 7 minutes

**Purpose** `scenes[3].objective`

Hold the definition precisely, and learn the single argument that closes every proof.

**Block 1 — Completeness** `scenes[3].blocks[0]` *(type `def`)*

A family of distributions {f_T(t; θ) : θ ∈ Θ} is complete if, for every measurable g, E_θ[g(T)] = 0 for all θ ∈ Θ implies P_θ(g(T) = 0) = 1 for all θ ∈ Θ. Loosely, 'T is complete' always means its family is.

**Block 2 — Bounded completeness** `scenes[3].blocks[1]` *(type `note`)*

The same condition restricted to bounded g. It is weaker, and it is all Basu's theorem actually needs. Exam questions use full completeness; be aware the distinction exists.

**Block 3 — The proof route, every time** `scenes[3].blocks[2]` *(type `step`)*

1. Write E_θ[g(T)] = 0 explicitly as a sum or integral over t.   2. Strip off every factor that does not involve t.   3. Recognise what is left as a power series, a polynomial, or an integral that must vanish for all θ.   4. Invoke uniqueness: a series vanishing on an interval has all coefficients zero; an integral vanishing for all upper limits has a zero integrand.   5. Conclude g(t) = 0 at every t the statistic can take.

**Block 4 — The three endings you will actually use** `scenes[3].blocks[3]` *(type `formula`)*

Poisson  →  Σ_t a_t λ^t ≡ 0 on an interval ⟹ every a_t = 0
Binomial →  Σ_t a_t r^t ≡ 0 on an interval ⟹ every a_t = 0  (after r = p/(1−p))
Uniform  →  ∫₀^θ g(x)x^(n−1) dx ≡ 0 for all θ ⟹ differentiate in θ ⟹ g ≡ 0

**Block 5 — For all θ, not for some θ** `scenes[3].blocks[4]` *(type `assume`)*

The quantifier is the whole content. E[g(T)] = 0 at a single θ says almost nothing. Questions are written so that a candidate who drops the quantifier reaches a confident wrong answer.

**Block 6 — Completeness does not follow from sufficiency** `scenes[3].blocks[5]` *(type `trap`)*

Nor from minimal sufficiency. They are separate properties and the exam exploits the gap: a curved exponential family has a minimal sufficient statistic that is not complete. The implication runs the other way — complete and sufficient implies minimal sufficient (Bahadur's theorem) — and the converse is false.

**Quick check before moving on** `scenes[3].ask`

- *question:* In the definition of completeness, why must Eθ[g(T)] = 0 hold for every θ in the parameter space, rather than just one value of θ?
- *hint on request:* A single equation may have many non-zero solutions. Completeness requires the zero-expectation condition across the whole family.

---

### Scene 5 of 14 — Worked in full — Σxᵢ is complete for the Poisson

`scenes[4]` · id `s4` · type `worked` (worked example) · 6 minutes

**Purpose** `scenes[4].objective`

See the five steps executed once, with the uniqueness argument spelled out.

**Problem put to the learner** `scenes[4].problem`

X₁,…,Xₙ are iid Poisson(λ), λ > 0. Show that T = ΣXᵢ is a complete sufficient statistic for λ.

**Worked steps** `scenes[4].steps[]`

1. `scenes[4].steps[0]` Identify the distribution of T.

   ```
   T = ΣXᵢ ~ Poisson(nλ),   P(T = t) = e^(−nλ) (nλ)^t / t!,  t = 0,1,2,…
   ```

   Laid out:

   $$T = ΣXᵢ ~ Poisson(nλ),   P(T = t) = \frac{e^{−nλ} (nλ)^{t}}{t!,  t} = 0,1,2,…$$

   *why* `.why`: Sums of independent Poissons are Poisson with the parameters added. Completeness is a statement about the family of distributions of T, so you need that family written down before anything else.

2. `scenes[4].steps[1]` Write the condition out in full.

   ```
   E_λ[g(T)] = Σ_{t≥0} g(t) · e^(−nλ) (nλ)^t / t! = 0   for every λ > 0
   ```

   Laid out:

   $$E_λ[g(T)] = \frac{Σ_{t≥0} g(t) · e^{−nλ} (nλ)^{t}}{t!} = 0   for every λ > 0$$

   *why* `.why`: Nothing clever — just the definition of expectation for a discrete statistic. The quantifier 'for every λ > 0' is doing all the work and must be carried through.

3. `scenes[4].steps[2]` Strip the factor that does not involve t.

   ```
   e^(−nλ) > 0, so divide it out:   Σ_{t≥0} [ g(t) nᵗ / t! ] λ^t = 0   for every λ > 0
   ```

   *why* `.why`: Dividing by a strictly positive quantity cannot change whether the rest is zero. What remains is a power series in λ with coefficients a_t = g(t)nᵗ/t!.

4. `scenes[4].steps[3]` Apply uniqueness of power series.

   ```
   A power series vanishing on an open interval has every coefficient zero:   g(t) nᵗ / t! = 0  for every t
   ```

   Laid out:

   $$\frac{A power series vanishing on an open interval has every coefficient zero:   g(t) nᵗ}{t!} = 0  for every t$$

   *why* `.why`: This is the step the whole proof exists for. It is only available because the identity holds for a continuum of λ — one value, or even a hundred, would not do it.

5. `scenes[4].steps[4]` Conclude.

   ```
   nᵗ > 0 and t! > 0, so g(t) = 0 for every t = 0,1,2,…   Hence T is complete.
   ```

   *why* `.why`: g vanishes at every point T can take, which is exactly P(g(T) = 0) = 1. Sufficiency came from factorisation in the previous topic, so T is complete AND sufficient.

**What to take from it** `scenes[4].after`

Look back at where the family's richness entered: step 4, and nowhere else. Steps 1 to 3 are bookkeeping. If you ever find a proof of completeness that never uses 'for all θ', you have made an error.

**Quick check before moving on** `scenes[4].ask`

- *question:* For a Poisson sample, what is the key step that turns Eλ[g(T)] = 0 for every λ into a statement that each coefficient must be zero?
- *hint on request:* Write the expectation as an exponential power series in λ and use uniqueness of its coefficients.

---

### Scene 6 of 14 — Pause and recall

`scenes[5]` · id `s5` · type `recall` (retrieval practice) · 2 minutes

**Purpose** `scenes[5].objective`

Retrieve before reading on — this is where the retention comes from.

**Intro** `scenes[5].intro`

Answer each in your head before revealing. Correcting a wrong retrieval beats re-reading a right answer.

- `scenes[5].items[0]` **Q:** State completeness.  
  **A:** E_θ[g(T)] = 0 for every θ in Θ implies g(T) = 0 with probability 1.
- `scenes[5].items[1]` **Q:** Is completeness a property of T, or of something else?  
  **A:** Of the family of distributions of T. The same statistic can be complete under one family and not under another.
- `scenes[5].items[2]` **Q:** Which step of a completeness proof actually uses 'for all θ'?  
  **A:** The uniqueness step — a power series or polynomial vanishing on an interval has every coefficient zero.
- `scenes[5].items[3]` **Q:** Complete sufficient implies minimal sufficient. Does the converse hold?  
  **A:** No. A curved exponential family such as N(θ,θ²) has a minimal sufficient statistic that is not complete.

---

### Scene 7 of 14 — Your turn, with the scaffolding removed — the Bernoulli

`scenes[6]` · id `s6` · type `completion` (fill in the blanks) · 8 minutes

**Purpose** `scenes[6].objective`

Run the same argument where the ending is a polynomial rather than a power series.

**Problem put to the learner** `scenes[6].problem`

X₁,…,Xₙ are iid Bernoulli(p), 0 < p < 1. Show that T = ΣXᵢ is complete.

**Worked steps** `scenes[6].steps[]`

1. `scenes[6].steps[0]` Identify the distribution of T and write the condition.

   ```
   T ~ Binomial(n, p):   E_p[g(T)] = Σ_{t=0}^{n} g(t) C(n,t) p^t (1−p)^(n−t) = 0   for every p ∈ (0,1)
   ```

   Laid out:

   $$T ~ Binomial(n, p):   E_p[g(T)] = Σ_{t=0}^{n} g(t) C(n,t) p^{t} (1−p)^{n−t} = 0   for every p ∈ (0,1)$$

   *why* `.why`: A finite sum this time, not an infinite series — which is why the ending will be a polynomial identity rather than a power series one.

2. `scenes[6].steps[1]` Divide through by (1−p)^n, which is strictly positive on (0,1).

   - *learner is asked:* Write what the sum becomes. Use r for p/(1−p).
   - *accepted answer* `.blank.answer`: Σ g(t) C(n,t) r^t = 0
   - *also accepted:* Σ g(t) C(n,t) r^t = 0; sum g(t) C(n,t) r^t = 0; Σ_{t=0}^n g(t)C(n,t)r^t=0; Σ g(t) nCt r^t = 0; sum_{t=0}^{n} g(t) C(n,t) r^t = 0; Σg(t)C(n,t)r^t=0
   - *hint:* p^t(1−p)^(n−t) ÷ (1−p)^n = p^t(1−p)^(−t) = (p/(1−p))^t. Everything else is unchanged.

   *why* `.why`: The substitution turns a two-variable mess into a clean polynomial in a single variable r.

3. `scenes[6].steps[2]` Note the range of r.

   ```
   As p runs over (0,1), r = p/(1−p) runs over all of (0, ∞)
   ```

   Laid out:

   $$As p runs over (0,1), r = \frac{p}{(1−p)} runs over all of (0, ∞)$$

   *why* `.why`: This is the quantifier arriving in its new clothes. The identity now holds on an open interval of r, which is exactly what the uniqueness argument needs.

4. `scenes[6].steps[3]` Apply uniqueness of polynomials.

   - *learner is asked:* What must be true of every coefficient?
   - *accepted answer* `.blank.answer`: g(t) C(n,t) = 0 for every t
   - *also accepted:* g(t) C(n,t) = 0 for every t; g(t)C(n,t)=0; every coefficient is zero; g(t) C(n,t) = 0; all coefficients are zero; g(t)*C(n,t)=0 for all t
   - *hint:* A polynomial of degree n that vanishes at infinitely many points is the zero polynomial — so every coefficient vanishes.

   *why* `.why`: A non-zero polynomial of degree n has at most n roots. Vanishing on a whole interval leaves only the zero polynomial.

5. `scenes[6].steps[4]` Conclude.

   - *learner is asked:* What does that give for g?
   - *accepted answer* `.blank.answer`: g(t) = 0 for t = 0,1,…,n
   - *also accepted:* g(t) = 0 for t = 0,1,…,n; g(t)=0 for all t; g(t) = 0; g is identically zero; g(t)=0 for t=0..n; g ≡ 0
   - *hint:* C(n,t) is never zero for t between 0 and n, so the other factor must be.

   *why* `.why`: g vanishes at every value T can take, so T is complete. Sufficiency came from factorisation, so T is complete and sufficient — and Lehmann–Scheffé now applies.

**What to take from it** `scenes[6].after`

Poisson ended in a power series, Bernoulli in a polynomial. Same five steps, different uniqueness theorem at the end. When you meet a new family, the only question is which uniqueness result closes it.

---

### Scene 8 of 14 — Exponential families, ancillarity, and Basu

`scenes[7]` · id `s7` · type `theory` (theory) · 9 minutes

**Purpose** `scenes[7].objective`

Get completeness without proving it, and get independence without a joint density.

**Block 1 — k-parameter exponential family** `scenes[7].blocks[0]` *(type `def`)*

f(x; θ) = h(x) · c(θ) · exp( Σ_{j=1}^{k} w_j(θ) t_j(x) ). The vector (w₁(θ),…,w_k(θ)) is the natural parameter, and the set of values it takes as θ ranges over Θ is the natural parameter space.

**Block 2 — The criterion that saves the proof** `scenes[7].blocks[1]` *(type `formula`)*

If the natural parameter space contains an open k-dimensional rectangle, the family is FULL RANK, and
T = ( Σᵢ t₁(xᵢ), …, Σᵢ t_k(xᵢ) )  is complete AND minimal sufficient.

**Block 3 — What full rank is really asking** `scenes[7].blocks[2]` *(type `assume`)*

That the natural parameter genuinely moves in k independent directions. Two isolated values are not an interval; a curve inside a plane is not a rectangle. This is the condition candidates skip, and it is the condition the curved-family questions turn on.

**Block 4 — Curved families** `scenes[7].blocks[3]` *(type `trap`)*

If dim(T) > dim(θ) the natural parameter traces a lower-dimensional curve and the family is not full rank. N(θ, θ²) has T = (ΣXᵢ, ΣXᵢ²) with w₁ = −1/(2θ²), w₂ = 1/θ satisfying w₁ = −w₂²/2 — a curve in the plane, not a rectangle. T stays minimal sufficient and is NOT complete, so Lehmann–Scheffé gives you nothing there.

**Block 5 — Ancillary statistic** `scenes[7].blocks[4]` *(type `def`)*

A statistic A whose distribution does not depend on θ at all. For a location family, the differences Xᵢ − X̄ are ancillary; for a scale family such as U(0,θ), the ratio X₍₁₎/X₍ₙ₎ is ancillary, because θ cancels.

**Block 6 — Basu's theorem** `scenes[7].blocks[5]` *(type `formula`)*

If T is a complete sufficient statistic for θ and A is ancillary, then T and A are independent — for every θ.

**Block 7 — Why Basu is worth memorising** `scenes[7].blocks[6]` *(type `note`)*

It proves independence without anyone computing a joint density. The textbook proof that X̄ and S² are independent for a normal sample is a page of algebra or an orthogonal-transformation argument; Basu does it in three lines. In an exam that is the difference between finishing the question and not.

**Block 8 — Both conditions, every time** `scenes[7].blocks[7]` *(type `trap`)*

Sufficient alone will not do, and complete alone will not do. If a question offers a sufficient statistic that is not complete — a curved family, or U(θ,θ+1) — Basu does not apply and any independence you claim is unjustified.

**Flow diagram** `scenes[7].flow` — Is this statistic complete? And may I use Basu?

*alt text* `.alt`: Decision chart for completeness and Basu's theorem

- row 1: You have a sufficient statistic T
- row 2: Can the density be written in exponential-family form?
- row 3: Check E[g(T)] = 0 ⇒ g ≡ 0 by hand  |  Is it FULL RANK: k natural parameters, k free parameters?
- row 4: Curved family — sufficient but NOT complete  |  T is complete
- row 5: T complete AND sufficient
- row 6: Is the other statistic's distribution free of θ?
- row 7: Basu: the two are independent
- arrows: You have a sufficient statistic T → Can the density be written in exponential-family form?; Can the density be written in exponential-family form? → [no] Check E[g(T)] = 0 ⇒ g ≡ 0 by hand; Can the density be written in exponential-family form? → [yes] Is it FULL RANK: k natural parameters, k free parameters?; Is it FULL RANK: k natural parameters, k free parameters? → [yes] T is complete; Is it FULL RANK: k natural parameters, k free parameters? → [no] Curved family — sufficient but NOT complete; Check E[g(T)] = 0 ⇒ g ≡ 0 by hand → T complete AND sufficient; T is complete → T complete AND sufficient; T complete AND sufficient → Is the other statistic's distribution free of θ?; Is the other statistic's distribution free of θ? → [yes, it is ancillary] Basu: the two are independent

*note shown under the diagram* `.note`: Full rank is the condition people skip. N(θ, θ²) has a two-dimensional natural statistic for one free parameter — curved, so sufficient but not complete, and Basu does not apply.

**Quick check before moving on** `scenes[7].ask`

- *question:* What extra property does completeness add to sufficiency, and why does Basu's theorem need both completeness and sufficiency?
- *hint on request:* Completeness rules out any non-zero function of the statistic whose expectation is zero for every θ. Basu then pairs a COMPLETE sufficient statistic with an ancillary one; drop completeness and the independence conclusion is not available.

**Optional deep-dive, opened on demand — Basu's theorem on a calibration certificate** `scenes[7].scenario`

*teaser on the closed card:* Why a calibration lab can report a mean and a spread as two unrelated numbers.

> A calibration laboratory measures a reference mass ten times and issues a certificate with two numbers: the mean of the readings, and a spread that quantifies the repeatability of the instrument. Everyone treats those two numbers as separate pieces of information — the mean is the measurement, the spread is the uncertainty attached to it.

> That separation is a theorem, not a convention. For a normal sample the sample mean is a complete sufficient statistic for μ when σ is known, and the sample variance is ancillary: its distribution does not involve μ at all, since shifting every reading by the same amount leaves the deviations untouched. Basu's theorem then says the two are independent.

> Independence is what licenses the practice. It means the spread the lab reports is not quietly contaminated by where the mean happened to land — a high reading does not come packaged with an inflated uncertainty. If the two were dependent, the certificate would have to report a joint statement rather than two numbers, and every downstream calculation that combines uncertainties would need rewriting.

> It is also a genuinely normal-distribution fact, not a general one. For an exponential sample the mean and the variance of the sample move together, and no amount of wishing makes them independent. That is why the normality assumption on a calibration certificate is load-bearing rather than decorative.

*closing line:* Ancillary plus complete sufficient gives independence, and independence is what lets two numbers be read separately.

---

### Scene 9 of 14 — Where completeness is proved by hand, and Basu pays off

`scenes[8]` · id `s8` · type `explore` (interactive visualisation) · 6 minutes

**Purpose** `scenes[8].objective`

Watch one family give you completeness, ancillarity and independence together.

**Body** `scenes[8].body[]`

X₁,…,Xₙ are iid U(0, θ). The likelihood is the cliff on screen: θ^(−n) above the sample maximum, zero below. X₍ₙ₎ is sufficient — that was the previous topic — and here it is also complete.

The proof is the third ending from scene 3. X₍ₙ₎ has density n x^(n−1)/θⁿ on (0, θ), so E[g(X₍ₙ₎)] = 0 for all θ becomes ∫₀^θ g(x) x^(n−1) dx = 0 for all θ. Differentiate both sides with respect to θ and you get g(θ)θ^(n−1) = 0 for every θ > 0, so g ≡ 0. The whole argument is one differentiation.

Now look for something ancillary. Take the ratio X₍₁₎/X₍ₙ₎. Scaling every observation by a constant leaves it unchanged, and changing θ is exactly such a scaling — so its distribution cannot involve θ. It is ancillary.

Basu now hands you a fact for free: X₍ₙ₎ and X₍₁₎/X₍ₙ₎ are independent. No joint density, no Jacobian. That is the whole point of the theorem.

Drag the maximum and watch the likelihood move with it while the ratio sits quietly outside the picture, unaffected by θ. Complete sufficient on one side, ancillary on the other, independent by Basu.

**Interactive element** `scenes[8].viz` — live plot of type `unif-likelihood`, initial state n=5, xmax=4.2. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[8].ask`

- *question:* X₍₁₎ on its own is NOT ancillary for U(0,θ), but X₍₁₎/X₍ₙ₎ is. What does the division actually remove?
- *hint on request:* Write X₍₁₎ as θ times a U(0,1) order statistic. Which factor survives the ratio?

---

### Scene 10 of 14 — Now without the steps — independence in the normal sample

`scenes[9]` · id `s9` · type `guided` (guided problem) · 8 minutes

**Purpose** `scenes[9].objective`

Choose Basu yourself, and check both of its conditions before you use it.

**Problem put to the learner** `scenes[9].problem`

X₁,…,Xₙ are iid N(μ, σ²) with σ² KNOWN. Prove that X̄ and S² = Σ(Xᵢ − X̄)²/(n−1) are independent.

**Hint ladder, revealed one at a time** `scenes[9].hints[]`

1. Direction — you are being asked for independence, and you have been given a theorem this week that delivers independence. Before reaching for it, write down what it needs: one complete sufficient statistic, and one ancillary statistic. Decide which of X̄ and S² is which.
2. Method — Basu. X̄ is complete sufficient for μ here, because with σ² known the family is a full-rank one-parameter exponential family. So the work is all on the other side: show that the distribution of S² does not involve μ.
3. Next step — write Xᵢ − X̄ = (Xᵢ − μ) − (X̄ − μ) and look at what S² becomes. The variables Yᵢ = Xᵢ − μ are N(0, σ²), with no μ in them anywhere.

**Model solution, hidden until requested** `scenes[9].solution[]`

1. `scenes[9].solution[0]` Check the first condition.

   ```
   σ² known ⟹ f(x;μ) = h(x)c(μ)exp( (μ/σ²)·Σxᵢ ), a full-rank one-parameter exponential family, so X̄ is complete sufficient for μ.
   ```

   Laid out:

   $$σ² known ⟹ f(x;μ) = h(x)c(μ)exp( \frac{μ}{σ²}·Σxᵢ ), a full-rank one-parameter exponential family, so X̄ is complete sufficient for μ.$$

2. `scenes[9].solution[1]` Rewrite the deviations.

   ```
   Xᵢ − X̄ = (Xᵢ − μ) − (X̄ − μ) = Yᵢ − Ȳ,   where Yᵢ = Xᵢ − μ ~ N(0, σ²)
   ```

3. `scenes[9].solution[2]` Check the second condition.

   ```
   S² = Σ(Yᵢ − Ȳ)²/(n−1), and the distribution of the Yᵢ does not involve μ ⟹ S² is ancillary for μ.
   ```

   Laid out:

   $$S² = \frac{Σ(Yᵢ − Ȳ)²}{(n−1)}, and the distribution of the Yᵢ does not involve μ ⟹ S² is ancillary for μ.$$

4. `scenes[9].solution[3]` Apply Basu.

   ```
   X̄ complete sufficient, S² ancillary ⟹ X̄ ⟂ S², for every μ.
   ```

**Final answer given to the learner** `scenes[9].answer`

X̄ is complete sufficient for μ, S² is ancillary for μ, so Basu's theorem gives their independence immediately.

**Self-check offered** `scenes[9].check`

Two conditions were needed and both had to be verified — stating Basu without showing S² is ancillary answers half the question. Note also what the argument assumed: σ² known. The result is true with σ² unknown as well, but Basu alone does not get you there, because then X̄ is no longer sufficient on its own.

---

### Scene 11 of 14 — Six statements — verdict on each before you look

`scenes[10]` · id `s10` · type `trapcheck` (true/false check) · 6 minutes

**Purpose** `scenes[10].objective`

Practise the per-statement discipline the real multi-statement items demand.

**Intro** `scenes[10].intro`

Give every statement a true or false verdict first. In the exam these six would be one question scored all or nothing, so a verdict you skipped is a mark you gambled.

- `scenes[10].items[0]` **Claim:** Completeness is a property of the statistic T alone, independent of the family of distributions.  
  **Verdict: FALSE.** False, and the misconception the whole topic rests on. Completeness is a property of the family {f_T(t;θ)}. Restrict Θ enough and the same T stops being complete.
- `scenes[10].items[1]` **Claim:** If T is complete and sufficient, then T is minimal sufficient.  
  **Verdict: TRUE.** True — this is Bahadur's theorem, assuming a minimal sufficient statistic exists. Candidates often believe the converse instead, which is false.
- `scenes[10].items[2]` **Claim:** Every minimal sufficient statistic is complete.  
  **Verdict: FALSE.** False. N(θ, θ²) has minimal sufficient (ΣXᵢ, ΣXᵢ²), which is not complete because the family is curved.
- `scenes[10].items[3]` **Claim:** The distribution of an ancillary statistic does not depend on θ.  
  **Verdict: TRUE.** True — that is the definition. Note it says the distribution, not that the statistic is useless: an ancillary statistic is precisely what Basu's theorem needs.
- `scenes[10].items[4]` **Claim:** Basu's theorem requires only that T be sufficient and A be ancillary.  
  **Verdict: FALSE.** False — T must be COMPLETE and sufficient. Drop completeness and the conclusion fails; U(θ,θ+1) is the standard case where sufficiency holds, completeness does not, and no independence follows.
- `scenes[10].items[5]` **Claim:** In a full-rank k-parameter exponential family, the natural sufficient statistic is complete.  
  **Verdict: TRUE.** True, and it is the shortcut worth memorising: full rank means the natural parameter space contains an open k-dimensional rectangle, and then T is complete and minimal sufficient together.

---

### Scene 12 of 14 — Transfer — show that a statistic is NOT complete

`scenes[11]` · id `s11` · type `guided` (guided problem) · 8 minutes

**Purpose** `scenes[11].objective`

Run the argument backwards: construct a counterexample instead of proving a theorem.

**Problem put to the learner** `scenes[11].problem`

X₁,…,Xₙ are iid U(θ, θ+1) with θ ∈ ℝ unknown. The minimal sufficient statistic is T = (X₍₁₎, X₍ₙ₎). Show that T is NOT complete.

**Hint ladder, revealed one at a time** `scenes[11].hints[]`

1. Direction — to disprove completeness you do not argue, you exhibit. You need one specific function g, not identically zero, with E_θ[g(T)] = 0 for every θ. Start by asking which functions of T have an expectation that does not move when θ moves.
2. Method — a function of T whose distribution is free of θ is ancillary, and its mean is therefore some constant c. Subtract the constant and you have your g. So look for an ancillary function of (X₍₁₎, X₍ₙ₎) in this location family.
3. Next step — the range R = X₍ₙ₎ − X₍₁₎ is unchanged when every observation shifts by the same amount, and changing θ is exactly such a shift. Find E[R], then write down g.

**Model solution, hidden until requested** `scenes[11].solution[]`

1. `scenes[11].solution[0]` Find an ancillary function of T.

   ```
   R = X₍ₙ₎ − X₍₁₎. Shifting all Xᵢ by a constant leaves R unchanged, and the family is a location family, so the distribution of R does not involve θ.
   ```

2. `scenes[11].solution[1]` Compute its mean.

   ```
   Write Xᵢ = θ + Uᵢ with Uᵢ iid U(0,1). Then R = U₍ₙ₎ − U₍₁₎, and E[U₍ₙ₎] = n/(n+1), E[U₍₁₎] = 1/(n+1), so E[R] = (n−1)/(n+1).
   ```

   Laid out:

   $$Write Xᵢ = θ + Uᵢ with Uᵢ iid U(0,1). Then R = U₍ₙ₎ − U₍₁₎, and E[U₍ₙ₎] = \frac{n}{(n+1)}, E[U₍₁₎] = \frac{1}{(n+1)}, so E[R] = \frac{(n−1)}{(n+1)}.$$

3. `scenes[11].solution[2]` Build the counterexample.

   ```
   g(T) = (X₍ₙ₎ − X₍₁₎) − (n−1)/(n+1)
   ```

   Laid out:

   $$g(T) = (X₍ₙ₎ − X₍₁₎) − \frac{(n−1)}{(n+1)}$$

4. `scenes[11].solution[3]` Verify both halves.

   ```
   E_θ[g(T)] = E[R] − (n−1)/(n+1) = 0 for EVERY θ, yet g(T) is not identically zero — R is a genuine random variable with positive variance.
   ```

   Laid out:

   $$E_θ[g(T)] = E[R] − \frac{(n−1)}{(n+1)} = 0 for EVERY θ, yet g(T) is not identically zero — R is a genuine random variable with positive variance.$$

5. `scenes[11].solution[4]` Conclude.

   ```
   A non-zero function of T has mean zero for every θ, so T is not complete. Basu's theorem therefore does not apply to this family.
   ```

**Final answer given to the learner** `scenes[11].answer`

g(T) = (X₍ₙ₎ − X₍₁₎) − (n−1)/(n+1) is a non-trivial unbiased estimator of zero, so T = (X₍₁₎, X₍ₙ₎) is not complete.

**Self-check offered** `scenes[11].check`

Two things had to be shown, and a half answer scores nothing: that E[g(T)] = 0 for all θ, AND that g is not identically zero. Candidates routinely produce the function and forget to say why it is non-trivial — which is the half that makes it a counterexample.

---

### Scene 13 of 14 — What you should now be able to do unaided

`scenes[12]` · id `s12` · type `summary` (summary) · 3 minutes

**Purpose** `scenes[12].objective`

Close the loop before the test.

**Body** `scenes[12].body[]`

State completeness with its quantifier intact, and say whose property it is.

Prove completeness for a standard family by setting E[g(T)] = 0 and finishing with the right uniqueness result — power series, polynomial, or differentiation under the integral.

Put a density into exponential form, check whether the natural parameter space holds an open rectangle, and take completeness for free when it does.

Spot a curved family by comparing dim(T) with dim(θ), and refuse to claim completeness there.

Identify an ancillary statistic, check both of Basu's conditions, and use it to get independence in three lines.

Disprove completeness by building an ancillary function of T and subtracting its mean.

The mastery test is ten unseen questions across all of this. Hints are off. The pass is 80% overall with 70% floors on the numerical and multi-statement items.

---

### Scene 14 of 14 — Mastery test

`scenes[13]` · id `s13` · type `quiz` (mastery test) · 12 minutes

**Purpose** `scenes[13].objective`

Demonstrate it independently, on unseen questions.

Draws from the pool reproduced below. `scenes[13].setId` = `inference_t2_mastery`

---

## Revision material `revision`

**Revision sheet** `revision.sheet[]` (12 lines)

1. `[0]` T is complete if E_θ[g(T)] = 0 for every θ forces g(T) = 0 with probability 1.
2. `[1]` Completeness is a property of the FAMILY {f_T(t;θ) : θ ∈ Θ}, never of T by itself.
3. `[2]` In words: the only unbiased estimator of zero that is a function of T is zero itself.
4. `[3]` That uniqueness is what makes Lehmann–Scheffé give ONE best unbiased estimator.
5. `[4]` Proof route: write E[g(T)] = 0, then use uniqueness — power series (Poisson), polynomial (Binomial), differentiate under the integral (Uniform).
6. `[5]` Full-rank k-parameter exponential family ⟹ (Σt₁, …, Σt_k) is complete AND minimal sufficient.
7. `[6]` Full rank means the natural parameter space contains an open k-dimensional rectangle.
8. `[7]` Curved family (dim T > dim θ, e.g. N(θ,θ²)) ⟹ minimal sufficient but NOT complete.
9. `[8]` Ancillary: the distribution of A does not depend on θ at all.
10. `[9]` Basu: T complete sufficient, A ancillary ⟹ T and A are independent, for every θ.
11. `[10]` Complete sufficient ⟹ minimal sufficient (Bahadur). The converse is false.
12. `[11]` To DISPROVE completeness, build one non-zero g with E[g(T)] = 0 for all θ — an ancillary function of T minus its mean does it.

**Flashcards** `revision.cards[]`

| Front | Back |
|---|---|
| Completeness in one sentence | If a function of T averages to zero under every θ in the family, that function must be zero. |
| Whose property is completeness? | The family's, not the statistic's. The same T can be complete under one family and not under another. |
| Why we want it | It makes the unbiased estimator built on T unique, which is what turns Rao–Blackwell into Lehmann–Scheffé. |
| Standard proof ending | A power series or polynomial that vanishes on an interval has every coefficient zero. |
| Exponential-family criterion | Full rank — the natural parameter space holds an open k-dimensional rectangle — gives completeness and minimal sufficiency together. |
| Ancillary statistic | One whose distribution is free of θ. For U(0,θ), X₍₁₎/X₍ₙ₎ is ancillary because θ cancels. |
| Basu's theorem | Complete sufficient T is independent of every ancillary A — no joint density needed. |
| How to disprove completeness | Find a non-trivial g(T) with mean zero for all θ. For U(θ,θ+1), the range minus (n−1)/(n+1) does it. |

**Memory aids** `revision.tricks[]`

- `[0]` **Complete = only zero has zero mean** — E_θ[g(T)] = 0 for every θ forces g ≡ 0. Nothing non-trivial averages to zero at every θ.
- `[1]` **Curved means fat** — More natural statistics than free parameters → sufficient but NOT complete. N(θ, θ²) is the stock example.
- `[2]` **Basu needs all three** — Complete AND sufficient on one side, ancillary on the other. Drop any one and the theorem is gone.
- `[3]` **Ancillary = blind to θ** — Its distribution does not involve θ, so on its own it says nothing about θ — which frees it to check the model.

**Elimination shortcuts for multiple-choice items** `revision.shortcuts[]`

- `[0]` Full-rank k-parameter exponential family ⇒ the natural statistic is complete. That is the quickest route there is.
- `[1]` U(θ, θ+1): minimal sufficient (X₍₁₎, X₍ₙ₎), NOT complete — the range is ancillary and spoils it.
- `[2]` Location families: any difference of observations is ancillary. Scale families: any ratio is.
- `[3]` Completeness is a property of the FAMILY, never of one distribution.

**If nothing else is remembered** `revision.remember[]`

- `[0]` Sufficiency reduces the data; completeness makes the reduction unique. They answer different questions.
- `[1]` Check which parameters are actually unknown before quoting Basu — ancillarity is relative to those.

**Errors to avoid** `revision.traps[]`


---

## Mastery pool — all 20 items with answer keys `qsets/mastery`

Ten are drawn per attempt at 3 easy / 5 moderate / 2 hard. Keys are distributed five to each option letter. Please check each item for a second defensible answer as well as for the correctness of its stated key and explanation.

### Q1 — `inf-t2-m-01` *(single, easy)*

A family of distributions of T is complete when:

*Options* `.options[]`:

- **A.** E_θ[g(T)] = 0 for every θ implies g(T) = 0 with probability 1  ← key
- **B.** E_θ[g(T)] = 0 for some θ implies g(T) = 0 with probability 1
- **C.** Var_θ(T) does not depend on θ
- **D.** The distribution of T does not depend on θ

*Explanation* `.explanation`: That is the definition, and the quantifier 'for every θ' is the whole content — option B weakens it to a single θ, which says almost nothing. Option D describes an ancillary statistic, which is close to the opposite situation. Option C is unrelated to completeness.

### Q2 — `inf-t2-m-02` *(numeric, moderate)*

X₁,…,X₅ are iid U(0,θ). The sample maximum is x₍₅₎ = 3.5. Given E[X₍ₙ₎] = nθ/(n+1), give the UMVUE of θ and its value here.

*Options* `.options[]`:

- **A.** x₍₅₎ = 3.5
- **B.** (6/5)·x₍₅₎ = 4.2  ← key
- **C.** (5/6)·x₍₅₎ = 2.917
- **D.** 2x̄, which cannot be found from x₍₅₎ alone

*Explanation* `.explanation`: X₍ₙ₎ is complete sufficient, and E[X₍ₙ₎] = 5θ/6, so (6/5)X₍ₙ₎ is unbiased. Being an unbiased function of a complete sufficient statistic, Lehmann–Scheffé makes it the UMVUE: (6/5)(3.5) = 4.2. Option A is the MLE, which is biased low; option C scales the wrong way and makes the bias worse.

*Arithmetic check* `.check`: The multiplier is (n+1)/n = 6/5, not n/(n+1). A UMVUE for θ must come out larger than the sample maximum, never smaller.

### Q3 — `inf-t2-m-03` *(multi, hard)*

Consider Basu's theorem and its conditions.

*Statements to judge* `.statements[]`:

- **A.** If T is complete sufficient and A is ancillary, then T and A are independent for every θ.
- **B.** Sufficiency of T alone is enough for the conclusion.
- **C.** For an iid normal sample with σ² known, Basu gives the independence of X̄ and S².
- **D.** Bounded completeness of T is enough for the theorem to hold.

*Options* `.options[]`:

- **A.** A and B only
- **B.** B and C only
- **C.** A, C and D only  ← key
- **D.** A, B and D only

*Explanation* `.explanation`: A is true — that is the statement of the theorem. B is false: completeness is required as well as sufficiency, and dropping it breaks the conclusion. C is true, and is the standard application. D is true — bounded completeness suffices, which is why some texts state it that way.

*Verdict on each statement* `.verdicts`:

- **A — true.** The theorem exactly as stated.
- **B — false.** Completeness is essential. U(θ,θ+1) is sufficient without being complete, and no independence follows.
- **C — true.** X̄ is complete sufficient for μ, S² is ancillary for μ, so they are independent.
- **D — true.** Basu's proof only needs the condition for bounded g, so bounded completeness suffices.

### Q4 — `inf-t2-m-04` *(numeric, hard)*

X₁,…,X₄ are iid U(θ, θ+1). The range is R = X₍₄₎ − X₍₁₎. Give E[R], and say what it shows about the minimal sufficient statistic (X₍₁₎, X₍₄₎).

*Options* `.options[]`:

- **A.** E[R] = 3/5, and it shows the statistic is not sufficient
- **B.** E[R] = 1/5, and it shows the statistic is not complete
- **C.** E[R] = 4/5, and it shows the statistic is ancillary
- **D.** E[R] = 3/5, and it shows the statistic is not complete  ← key

*Explanation* `.explanation`: Writing Xᵢ = θ + Uᵢ with Uᵢ iid U(0,1), R = U₍₄₎ − U₍₁₎ with E[R] = (n−1)/(n+1) = 3/5. Since R is ancillary, g(T) = R − 3/5 is a non-zero function with mean 0 for every θ, so T is not complete. It remains perfectly sufficient — option A confuses the two properties.

*Arithmetic check* `.check`: Two parts: the number and what it demonstrates. (n−1)/(n+1) with n = 4 is 3/5, not 1/5 — that would be E[U₍₁₎].

### Q5 — `inf-t2-m-05` *(single, easy)*

For which family is the minimal sufficient statistic NOT complete?

*Options* `.options[]`:

- **A.** N(θ, θ²) with θ > 0  ← key
- **B.** Poisson(λ) with λ > 0
- **C.** Bernoulli(p) with 0 < p < 1
- **D.** Exponential with rate λ > 0

*Explanation* `.explanation`: N(θ,θ²) is a curved exponential family: the minimal sufficient statistic (ΣXᵢ, ΣXᵢ²) is two-dimensional while θ is one-dimensional, so the natural parameter traces a curve rather than filling an open rectangle. Full rank fails and completeness goes with it. The other three are full-rank one-parameter families whose sufficient statistic is complete.

### Q6 — `inf-t2-m-06` *(numeric, moderate)*

X₁,…,X₄ are iid Bernoulli(p) and Σxᵢ = 3. The UMVUE of p² is T(T−1)/(n(n−1)). Give its value, and say why it is the UMVUE.

*Options* `.options[]`:

- **A.** 0.5625, because it is the square of the MLE
- **B.** 0.5, because it is an unbiased function of a complete sufficient statistic  ← key
- **C.** 0.75, because it is the sample proportion
- **D.** 0.5, because it has the smallest variance among all estimators

*Explanation* `.explanation`: T(T−1)/(n(n−1)) = 3·2/(4·3) = 0.5. It is unbiased because E[T(T−1)] = n(n−1)p², and T is complete sufficient, so Lehmann–Scheffé makes the unbiased function of T the UMVUE. Option A is p̂² = 0.5625, which is biased. Option D overstates the claim — UMVUE means smallest variance among UNBIASED estimators only.

*Arithmetic check* `.check`: The question asked for the value and the reason. 0.5 with the wrong reason is still a wrong answer in a two-part item.

### Q7 — `inf-t2-m-07` *(multi, hard)*

Let T be sufficient for θ in some family.

*Statements to judge* `.statements[]`:

- **A.** If T is sufficient then T is complete.
- **B.** If T is complete and sufficient then T is minimal sufficient.
- **C.** A sufficient statistic is always ancillary.
- **D.** Exhibiting one non-zero g with E_θ[g(T)] = 0 for all θ disproves completeness.

*Options* `.options[]`:

- **A.** A, B and C only
- **B.** C and D only
- **C.** B and D only  ← key
- **D.** A and B only

*Explanation* `.explanation`: A is false — sufficiency does not give completeness; the implication runs the other way. B is true, by Bahadur's theorem. C is false: ancillarity means the distribution is free of θ, which is close to the opposite of sufficiency. D is true, and is exactly how completeness is disproved.

*Verdict on each statement* `.verdicts`:

- **A — false.** No. The whole sample is sufficient and is almost never complete.
- **B — true.** Bahadur's theorem, assuming a minimal sufficient statistic exists.
- **C — false.** Ancillary means the distribution does not involve θ — nearly the reverse of carrying all the information about θ.
- **D — true.** Completeness is a universal claim, so a single counterexample destroys it.

### Q8 — `inf-t2-m-08` *(numeric, moderate)*

X₁,…,Xₙ are iid with f(x;θ) = θ e^(−θx), x > 0. Put the family in exponential form and give the dimension of the natural parameter space together with the complete sufficient statistic.

*Options* `.options[]`:

- **A.** Dimension 2, and T = (Σxᵢ, Σxᵢ²)
- **B.** Dimension 1, and T = x₍ₙ₎
- **C.** Dimension 2, and T = (Σxᵢ, n)
- **D.** Dimension 1, and T = Σxᵢ  ← key

*Explanation* `.explanation`: f = θ·exp(−θx) = h(x)c(θ)exp(w(θ)t(x)) with h = 1, c(θ) = θ, w(θ) = −θ and t(x) = x. One natural parameter, and as θ runs over (0,∞) the value −θ covers an open interval, so the family is full rank. T = Σxᵢ is therefore complete and minimal sufficient.

*Arithmetic check* `.check`: One parameter means a one-dimensional T. If you wrote a pair, check how many distinct t-functions the exponent actually needed.

### Q9 — `inf-t2-m-09` *(numeric, moderate)*

X₁,…,Xₙ are iid Poisson(λ). You must show T = ΣXᵢ is complete. After writing E_λ[g(T)] = 0 and dividing out e^(−nλ), what remains and what closes the argument?

*Options* `.options[]`:

- **A.** A power series in λ that vanishes on an interval, so every coefficient is zero  ← key
- **B.** A polynomial in λ of degree n, so it has at most n roots
- **C.** An integral over (0,λ), so differentiating in λ gives g ≡ 0
- **D.** A moment generating function, so uniqueness of MGFs gives g ≡ 0

*Explanation* `.explanation`: Dividing by e^(−nλ) leaves Σ_t [g(t)nᵗ/t!] λ^t = 0 for every λ > 0 — a power series in λ identically zero on an open interval, so every coefficient vanishes and g(t) = 0 for all t. Option B is the Binomial ending, option C the Uniform ending; both are right arguments applied to the wrong family.

*Arithmetic check* `.check`: The sum over t is infinite for a Poisson, so it is a power series and not a polynomial. Identify the support before choosing which uniqueness result to cite.

### Q10 — `inf-t2-m-10` *(order, moderate)*

To prove a statistic complete, arrange these steps in the order they are carried out.

*Steps to order* `.items[]`:

- A. Write E_θ[g(T)] = 0 explicitly as a sum or integral
- B. Apply the uniqueness result and conclude g ≡ 0
- C. Identify the distribution of T and its support
- D. Divide out every factor that does not involve t

*Options* `.options[]`:

- **A.** D, C, A, B
- **B.** C, A, D, B  ← key
- **C.** A, C, D, B
- **D.** C, D, A, B

*Explanation* `.explanation`: Write the distribution of T first — completeness is a statement about that family, so nothing can start without it. Then write E[g(T)] = 0 in full, strip the factors free of t, and close with the uniqueness result. Reaching for a uniqueness theorem before you know whether the sum is finite or infinite is how candidates pick the wrong one.

### Q11 — `inf-t2-m-11` *(single, easy)*

A statistic T is ancillary for θ when:

*Options* `.options[]`:

- **A.** T is sufficient but not complete
- **B.** T has expectation zero for every θ
- **C.** the distribution of T does not depend on θ  ← key
- **D.** T is independent of every other statistic

*Explanation* `.explanation`: Ancillarity means the distribution of T is the same whatever θ is, so T on its own says nothing about θ. Option B states the condition that appears inside the definition of completeness, not ancillarity, and independence from a complete sufficient statistic is a CONSEQUENCE of ancillarity via Basu, not its definition.

### Q12 — `inf-t2-m-12` *(numeric, moderate)*

X₁,…,X₆ are iid U(0,θ) with sample maximum x₍₆₎ = 4.2. Using E[X₍ₙ₎] = nθ/(n+1), give the unbiased estimator of θ based on the maximum and its value here.

*Options* `.options[]`:

- **A.** x₍ₙ₎ = 4.2
- **B.** 2x̄, which cannot be found from this information
- **C.** n x₍ₙ₎/(n+1) = 3.6
- **D.** (n+1)x₍ₙ₎/n = 4.9  ← key

*Explanation* `.explanation`: E[X₍₆₎] = 6θ/7, so multiplying by 7/6 gives an unbiased estimator: (n+1)X₍ₙ₎/n = (7/6)(4.2) = 4.9. Option C applies the correction the wrong way round and produces an estimate BELOW the largest observation, which is impossible.

*Arithmetic check* `.check`: The correction must push the estimate UP, because the sample maximum always underestimates θ. An answer below 4.2 is wrong on its face.

### Q13 — `inf-t2-m-13` *(multi, hard)*

Consider completeness and the families it holds in.

*Statements to judge* `.statements[]`:

- **A.** T is complete when E_θ[g(T)] = 0 for all θ forces g(T) = 0 almost surely.
- **B.** Completeness is a property of one distribution rather than of a family.
- **C.** In a full-rank k-parameter exponential family, the natural statistic is complete.
- **D.** A minimal sufficient statistic can fail to be complete.

*Options* `.options[]`:

- **A.** A, C and D only  ← key
- **B.** A and B only
- **C.** B and C only
- **D.** A, B and D only

*Explanation* `.explanation`: A is true — that is the definition. B is false: completeness is a property of the FAMILY of distributions of T, not of a single distribution. C is true, and is the standard sufficient condition. D is true: for U(θ, θ+1) the minimal sufficient (X₍₁₎, X₍ₙ₎) is not complete, because the range has a θ-free distribution with non-zero mean that can be centred to give a non-trivial unbiased estimator of zero.

*Verdict on each statement* `.verdicts`:

- **A — true.** The definition, stated in the form you actually verify.
- **B — false.** The quantifier is over θ, so the family is what completeness is about.
- **C — true.** Full rank means the natural parameter space contains an open set; then the natural statistic is complete.
- **D — true.** U(θ, θ+1) is the standard counterexample — the range is ancillary and spoils completeness.

### Q14 — `inf-t2-m-14` *(numeric, moderate)*

X₁,…,Xₙ are iid N(μ, σ²) with σ² known. Put the family in exponential form f(x) = h(x)exp{η(μ)T(x) − A(μ)} and identify the natural parameter η and natural statistic T.

*Options* `.options[]`:

- **A.** η = μ, T(x) = x/σ²
- **B.** η = μ/σ², T(x) = x  ← key
- **C.** η = μ/σ², T(x) = x²
- **D.** η = 1/σ², T(x) = (x−μ)²

*Explanation* `.explanation`: Expanding −(x−μ)²/(2σ²) gives −x²/(2σ²) + μx/σ² − μ²/(2σ²). The term carrying both the parameter and the data is (μ/σ²)·x, so η = μ/σ² and T(x) = x. The −x²/(2σ²) term has no μ and goes into h(x); the −μ²/(2σ²) term has no x and is −A(μ).

*Arithmetic check* `.check`: The natural statistic is whatever multiplies the parameter after expanding. If your T still has σ² in it, you have put part of h(x) in the wrong place.

### Q15 — `inf-t2-m-15` *(single, easy)*

Basu's theorem states that:

*Options* `.options[]`:

- **A.** a complete statistic is always sufficient
- **B.** an ancillary statistic is independent of the parameter
- **C.** a complete sufficient statistic is independent of every ancillary statistic  ← key
- **D.** every sufficient statistic is independent of every ancillary statistic

*Explanation* `.explanation`: All three conditions matter. Sufficiency alone is not enough — completeness is what makes the independence follow — and the theorem says nothing about a complete statistic being sufficient. Option B is a loose restatement of the definition of ancillarity, not of Basu.

### Q16 — `inf-t2-m-16` *(numeric, hard)*

X₁,…,Xₙ are iid N(μ, σ²) with σ² known. Use Basu to decide: are X̄ and S² independent, and what is the argument?

*Options* `.options[]`:

- **A.** No — both are computed from the same sample, so they cannot be independent
- **B.** Yes — but only because the normal density factorises, not by Basu
- **C.** Basu does not apply, because S² is not ancillary
- **D.** Yes — X̄ is complete sufficient for μ and S² is ancillary for μ, so Basu applies  ← key

*Explanation* `.explanation`: With σ² known, X̄ is a complete sufficient statistic for μ. S² = Σ(Xᵢ−X̄)²/(n−1) has a distribution free of μ — shifting every observation by a constant leaves S² unchanged — so it is ancillary for μ. Basu then gives independence immediately, with no distribution theory at all. Sharing a sample is no obstacle to independence.

*Arithmetic check* `.check`: Check both hypotheses explicitly before quoting Basu: complete AND sufficient on one side, ancillary on the other. If σ² were unknown, S² would no longer be ancillary and this argument would fail.

### Q17 — `inf-t2-m-17` *(multi, moderate)*

Let T be a complete sufficient statistic for θ.

*Statements to judge* `.statements[]`:

- **A.** Any unbiased function of T is the UMVUE of its expectation.
- **B.** T is independent of every ancillary statistic.
- **C.** There is at most one unbiased function of T for a given target.
- **D.** Any unbiased function of T attains the Cramér–Rao bound.

*Options* `.options[]`:

- **A.** A, B and C only  ← key
- **B.** A and D only
- **C.** B and C only
- **D.** A, B and D only

*Explanation* `.explanation`: A is true — this is Lehmann–Scheffé. B is true, by Basu. C is true: completeness forces the unbiased function of T to be unique almost surely. D is false — completeness and sufficiency say nothing about attaining the Cramér–Rao bound, which needs the score to be linear in the estimator.

*Verdict on each statement* `.verdicts`:

- **A — true.** Lehmann–Scheffé, in the form you apply it.
- **B — true.** Basu's theorem.
- **C — true.** Two of them would differ by a non-zero function with zero expectation, which completeness forbids.
- **D — false.** The exponential rate's UMVUE sits strictly above the floor. Best unbiased and efficient are different claims.

### Q18 — `inf-t2-m-18` *(numeric, moderate)*

X₁,…,X₅ are iid Poisson(λ) with Σxᵢ = 10. T = ΣXᵢ is complete sufficient. Give the UMVUE of λ and its value.

*Options* `.options[]`:

- **A.** (T+1)/n = 2.2
- **B.** T/n = 2  ← key
- **C.** T = 10
- **D.** T/(n−1) = 2.5

*Explanation* `.explanation`: X̄ = T/n is an unbiased function of the complete sufficient statistic T, so by Lehmann–Scheffé it is the UMVUE of λ. Its value is 10/5 = 2. The other options are unbiased for nothing in particular — T estimates nλ, and T/(n−1) is biased upward by a factor n/(n−1).

*Arithmetic check* `.check`: Confirm unbiasedness before claiming UMVUE: E[T/n] = nλ/n = λ ✓. Completeness and sufficiency do the rest.

### Q19 — `inf-t2-m-19` *(single, moderate)*

For which of these is the minimal sufficient statistic complete?

*Options* `.options[]`:

- **A.** U(θ, θ+1), T = (X₍₁₎, X₍ₙ₎)
- **B.** N(θ, θ²), T = (ΣXᵢ, ΣXᵢ²)
- **C.** Poisson(λ), T = ΣXᵢ  ← key
- **D.** Cauchy location θ, T = the order statistics

*Explanation* `.explanation`: The Poisson is a full-rank one-parameter exponential family, so ΣXᵢ is complete. U(θ, θ+1) fails because the range is ancillary. N(θ, θ²) is a curved exponential family — the two-dimensional natural statistic sits on a curve in a one-parameter problem — and is not complete. The Cauchy order statistics are sufficient but not complete.

*Arithmetic check* `.check`: Full-rank exponential family is the condition to look for. 'Curved' — where the number of natural parameters exceeds the number of free parameters — is the warning sign.

### Q20 — `inf-t2-m-20` *(order, moderate)*

To use Basu's theorem to prove two statistics independent, arrange these steps.

*Steps to order* `.items[]`:

- A. Confirm both hypotheses of the theorem are satisfied
- B. Identify a complete sufficient statistic for θ
- C. Show the second statistic has a distribution free of θ
- D. Conclude the two are independent

*Options* `.options[]`:

- **A.** A, B, C, D
- **B.** C, B, A, D
- **C.** B, A, C, D
- **D.** B, C, A, D  ← key

*Explanation* `.explanation`: Identify the complete sufficient statistic first, since everything else is stated relative to it. Then check the other statistic's distribution is free of θ, confirm both hypotheses hold, and only then conclude independence. Quoting Basu before checking completeness is the commonest way the argument is lost.

---

## Authoring and verification record `provenance`

Reproduced verbatim. It records what changed in each version and how each derivation was checked, including the findings of the two previous review rounds and the reasons some of their recommendations were declined.

> Review pass, October 2026: 3 per-scene quick checks added on theory, worked and explore scenes from a third-party module review, each read for correctness before import; a further set offered for completion and guided scenes was declined, since those scenes already end with the learner writing an answer. Theory, worked examples and practice authored for this platform against the UGC NET Statistics syllabus. Previous-year questions are stored separately and carry their exam cycle.

