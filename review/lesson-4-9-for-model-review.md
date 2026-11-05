# Lesson 4.9 — Neyman–Pearson, Monotone Likelihood Ratio and UMP Tests

Complete authored content of one lesson from a UGC-NET Statistics (Code 107) preparation application, extracted from the application's own content files.

| | |
|---|---|
| Content version | 1.3 |
| Scenes | 14 |
| Core scenes | 14 |
| Optional JRF-extension scenes | 0 |
| Estimated learner time | 56 minutes |
| Mastery pool | 20 items |
| Position in the app | Statistical Inference → Testing of Hypotheses → The best test there is |
| Engine | Testing — fixing one error rate and making the other as small as it can be |
| Pool label | Neyman–Pearson, MLR and UMP tests — mastery test (unseen) |
| Unit | IV — Statistical Inference |
| Audience | JRF-target candidates, many returning after several years away |

## Before you start: where this lesson sits

This lesson is at content version **1.3**. The application's current authoring standard is 4.1, and three of its requirements are **known** to be unmet here, so please do not spend effort reporting them — they are scheduled work, not findings:

- no short "how to use this lesson" note on the overview;
- a quick check on only some teaching scenes rather than all of them;
- no family-to-statistic style reference table where one would help.

This lesson is also **56 minutes against a house standard of about 90**, so it is thinner than intended. Comments on what is MISSING in substance are therefore especially useful — but please flag omissions rather than proposing to shorten what is there.

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

1. State the Neyman–Pearson lemma and use the likelihood ratio to find the most powerful test of one simple hypothesis against another.

2. Turn 'reject when the ratio is large' into an explicit critical region, and fix the constant from the size condition.

3. Recognise a monotone likelihood ratio family and quote Karlin–Rubin to get a UMP test for a one-sided alternative.

4. Say exactly why no UMP test exists for a two-sided alternative, and name what is used instead.

5. Compute size and power for a given test, and read a power function.

**Assumed prior knowledge** `prereq[]`

- `prereq[0]` **The likelihood function** — Every test in this topic is built from the ratio of two likelihoods. If writing L(θ) is still slow, the MLE topic comes first.
- `prereq[1]` **Distribution of the sample mean** — Nearly every critical region here is an inequality on x̄, and the size condition is a normal or chi-square tail probability.
- `prereq[2]` **Type I and Type II errors** — The whole subject is the trade-off between them. You need the two definitions cold before scene 3.

**Misconceptions the lesson is built to pre-empt** `traps[]`

- The critical value never contains μ₁.

- MLR gives one-sided UMP only.

- Discrete data may need randomisation to hit size α exactly.

- Power is computed under H₁, size under H₀.

**Assessment policy** `mastery`

- 10 items drawn per attempt from a pool of 20, mix 3 easy, 5 moderate, 2 hard
- pass mark 80%, no hints during the test, retest after 7 days
- `mastery.note`: Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the difficulty mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split.

**Sources** `refs[]`

- `refs[0]` **Hypothesis Testing: the Neyman–Pearson lemma** — Stanford STATS 200 (Autumn 2016), Lecture 16 (Lecture notes, free). The lemma stated and proved, then applied to the normal and the Bernoulli. Read it after scene 3, when you want to see why the likelihood ratio is forced on you rather than chosen.
- `refs[1]` **Uniformly Most Powerful Tests** — Penn State STAT 415, Lesson 26.1–26.3 (Course notes, free). The one-sided normal case worked in full, with the power function drawn. The clearest free treatment of why 'uniformly' is the hard word in UMP. CC BY-NC, no login.

---

## The lesson, scene by scene

### Scene 1 of 14 — Before the lesson — four things it will assume

`scenes[0]` · id `s0` · type `foundation` (prerequisite check) · 6 minutes

**Purpose** `scenes[0].objective`

Reinstate the two error definitions and the normal tail calculation, which every critical region in this topic ends with.

**Body** `scenes[0].body[]`

Testing is where notation defeats people. The ideas are small — compare two likelihoods, reject when the ratio is large — but every question ends in a tail probability, and every option differs from its neighbours by an α, a β or a square root of n.

Four checks: one on likelihoods, one on the two error types, one on the distribution of X̄, one on turning a ratio into an inequality. None takes more than a minute if it is there.

**Check 1** `scenes[0].items[0]`

- *asks:* Write L(θ) for an iid sample, and the likelihood ratio for testing a simple H₀: θ = θ₀ against a simple H₁: θ = θ₁.
- *expected answer* `.recall`: L(θ) = ∏f(xᵢ;θ). The ratio is Λ(x) = L(θ₁)/L(θ₀) — the likelihood under the alternative over the likelihood under the null. Neyman–Pearson rejects H₀ when Λ is large.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Both likelihoods are the same product, evaluated at two different values of θ. Nothing new is being introduced; you are comparing two heights of one curve.

> Conventions differ and this costs marks. Many books write the ratio the other way up, L(θ₀)/L(θ₁), and reject for small values. Either is correct; mixing them inside one question is not. Decide which way up you write it, and read each exam option for which way it is written.

> Do one. Exponential rate λ, testing λ₀ against λ₁ > λ₀: Λ = (λ₁/λ₀)ⁿ e^(−(λ₁−λ₀)Σxᵢ). Since λ₁ − λ₀ > 0, Λ is decreasing in Σxᵢ, so 'Λ large' is the same event as 'Σxᵢ small'. That translation is the whole technique.

**Check 2** `scenes[0].items[1]`

- *asks:* Define a Type I and a Type II error, and say which probability is α and which is β.
- *expected answer* `.recall`: Type I: rejecting H₀ when H₀ is true; its probability is α, the size or level. Type II: failing to reject H₀ when H₁ is true; its probability is β, and the power is 1 − β.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Fix them by what is true, not by what you did. The label names the state of the world you got wrong: Type I happens only when H₀ is true, Type II only when it is false.

> α = P(reject H₀ | H₀ true) and β = P(accept H₀ | H₁ true). Power = 1 − β = P(reject H₀ | H₁ true) is the quantity Neyman–Pearson maximises, with α held fixed as a constraint.

> The trade-off is the subject of the whole topic. Shrinking the rejection region lowers α and raises β; the only way to improve both at once is more data. Any exam option claiming a test lowers both at fixed n is wrong on principle.

**Check 3** `scenes[0].items[2]`

- *asks:* For an iid N(μ,σ²) sample, what is the distribution of X̄, and how do you turn P(X̄ > c) into a standard normal probability?
- *expected answer* `.recall`: X̄ ~ N(μ, σ²/n). Then P(X̄ > c) = P(Z > (c−μ)/(σ/√n)) = 1 − Φ((c−μ)√n/σ), where Z is standard normal.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> A sum of independent normals is normal, so X̄ is normal; its mean is μ and its variance σ²/n. The √n in the denominator of the standardisation comes from that variance and is the most frequently dropped symbol in the whole paper.

> Standardise by subtracting the mean and dividing by the standard deviation — σ/√n here, not σ. So Z = (X̄−μ)√n/σ.

> The two numbers to carry: Φ(1.645) = 0.95 and Φ(1.96) = 0.975. A one-sided size-0.05 test puts the critical value at μ₀ + 1.645σ/√n; a two-sided one at μ₀ ± 1.96σ/√n. The lesson's power calculations standardise twice — once under H₀ to find c, once under H₁ to find the power at that c.

**Check 4** `scenes[0].items[3]`

- *asks:* If the likelihood ratio Λ is an increasing function of Σxᵢ, what does the rejection region {Λ > k} become?
- *expected answer* `.recall`: {Σxᵢ > c}, where c is chosen so that P(Σxᵢ > c | θ₀) = α. A monotone ratio lets you replace an inequality on Λ by an inequality on the single statistic, and that is the only reason the test is computable.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> If g is strictly increasing then g(t) > k and t > g^(−1)(k) describe the same set of t. So an inequality in Λ becomes an inequality in the statistic, and you never have to find k itself — you find c directly from the size condition.

> Watch the direction. If Λ is decreasing in the statistic, as in the exponential example above, {Λ > k} becomes {Σxᵢ < c} and the size condition is a lower tail. Getting this backwards produces a test of size 1 − α, which is always one of the options.

> Monotonicity is also exactly the condition the lesson later names MLR, and it is what upgrades a test for two simple hypotheses into a UMP test against a one-sided alternative. So this small algebraic step is carrying more weight than it looks.

---

### Scene 2 of 14 — Two ways to be wrong, and only one of them is yours to choose

`scenes[1]` · id `s1` · type `intuition` (intuition) · 5 minutes

**Purpose** `scenes[1].objective`

See why testing is an asymmetric trade rather than a search for truth.

**Body** `scenes[1].body[]`

A test can fail in two ways. It can reject a hypothesis that was true, or it can fail to reject one that was false. Call the first error α and the second β, and notice immediately that you cannot drive both to zero: a test that never rejects has α = 0 and useless β, and a test that always rejects has the reverse.

The Neyman–Pearson answer is to stop pretending the two are symmetric. Fix α at a level you are prepared to live with — conventionally 0.05 or 0.01 — and then, among all tests of that size, take the one with the smallest β. That is the entire programme, and it is why the subject is about POWER rather than about truth.

The asymmetry is deliberate and it reflects where the burden of proof sits. H₀ is the status quo: the drug does nothing, the process is in control, the coin is fair. Rejecting it is a claim, and α is how often you are willing to make that claim wrongly. β is the price you pay for that caution.

What the lemma then adds is startling. For the simplest case — one completely specified hypothesis against another — it does not merely suggest a good test. It proves that the test based on the likelihood ratio is the best possible, and that any other test of the same size has power no greater. You are not choosing a statistic; you are being told which one to use.

Everything after that is an attempt to extend the result. When the alternative is a whole range of values rather than a single one, 'best' has to hold for every one of them at once — uniformly — and that is a far stronger demand. Sometimes it can be met. Often it cannot, and knowing which is which is most of what this topic examines.

**Aside — Why the words matter** `scenes[1].aside.body`

SIMPLE hypothesis: the distribution is fully specified, as in H₀: μ = 5. COMPOSITE: a set of distributions, as in H₀: μ ≤ 5. Neyman–Pearson is a theorem about simple versus simple. Every later result is machinery for getting a composite problem back to that case.

**Suggested question to put to the assistant** `scenes[1].ask` *(legacy shape: a pre-written prompt, not a self-test question — this scene has no quick check)*

- *button label* `.label`: Ask Claude why the asymmetry is defensible
- *prompt* `.prompt`: A UGC NET Statistics (JRF) candidate is starting hypothesis testing. In under 150 words, plain text, explain why the Neyman–Pearson framework treats the two error types asymmetrically — fixing α and minimising β — rather than, say, minimising their sum. Mention what that asymmetry assumes about H₀, and one situation where the assumption is uncomfortable. Do not restate the definitions of α and β.
- *model tier requested* `.tier`: default *(configuration, not content)*

**Optional deep-dive, opened on demand — How a radar decides** `scenes[1].scenario`

*teaser on the closed card:* A radar has milliseconds to decide whether a return is an aircraft or noise.

> A radar transmits a pulse and listens. What comes back is mostly thermal noise, with — sometimes — a faint reflection buried in it. The receiver has to decide, continuously and in real time, between two hypotheses: H₀, noise only, and H₁, noise plus a target echo.

> Both errors have names and costs. Declaring a target when there is none is a false alarm: the system tracks a ghost, and operators lose confidence. Missing a real return is a missed detection, with obvious consequences. The two cannot be minimised together, so the engineering convention is to fix the false-alarm rate — this is literally called the constant false alarm rate, CFAR — and then maximise the probability of detection subject to it.

> That is Neyman–Pearson, implemented in silicon. Fix α, maximise power. And the detector that does it is the likelihood ratio: the receiver forms the ratio of the likelihood of the observed waveform under 'signal present' to that under 'noise only', and compares it with a threshold set by the required false-alarm rate.

> The design consequences follow the mathematics exactly. The threshold is computed from the noise distribution alone — the H₀ side — which is why it does not depend on how strong the target is. Target strength affects only the detection probability, which is the power of the test. And the way to improve detection without accepting more false alarms is to integrate more pulses: the equivalent of raising n.

*think-it-through question* `.q`: An operator complains of too many false alarms and asks for the threshold to be raised. What happens to the two error rates, and what would be the better fix?

*what the statistics says* `.answer`: Raising the threshold lowers α, so false alarms fall — but it moves the cut-off away from the alternative too, so the detection probability falls with it. The two cannot both improve at a fixed amount of data; that is exactly the trade the lemma formalises. The better fix is to integrate more pulses, or to improve the signal-to-noise ratio. Both increase the separation between the two distributions, which raises power at the SAME false-alarm rate — the only thing that buys an improvement in both errors at once.

*link line* `.link`: The same structure runs medical screening: sensitivity is power, one minus specificity is α, and arguing about where to set a diagnostic cut-off is arguing about where on this trade-off to sit.

---

### Scene 3 of 14 — Watch α and power trade against each other

`scenes[2]` · id `s2` · type `explore` (interactive visualisation) · 7 minutes

**Purpose** `scenes[2].objective`

See the two error rates as areas, and find out what actually moves power.

**Body** `scenes[2].body[]`

Two curves: the sampling distribution of x̄ under H₀ on the left, and under H₁ shifted right by the true gap μ₁ − μ₀. The vertical line is the cut-off c. Reject when x̄ lands to its right.

The red area is α — the part of the H₀ curve that falls in the rejection region, which is exactly how often you reject a true null. The amber area is β, the part of the H₁ curve that falls short of the cut-off and so gets missed. Power is everything else under the H₁ curve.

Now experiment, and watch what happens to the two areas. Raise α: the line slides left, the red area grows and the amber shrinks. Lower it: the reverse. At a fixed sample size the two errors are joined at the hip — you are moving one cut-off, and it cannot favour both sides.

Then raise n and watch something different happen. Both curves narrow, because the standard error σ/√n falls. The cut-off moves in, the red area stays exactly where you set it, and the amber area collapses. Sample size is the only control that improves one error without worsening the other.

Finally set the gap to zero. The curves lie on top of each other and power drops to α itself. A test can never do worse than its own size, and when there is nothing to detect, rejecting at rate α is all it does. That is the floor the whole subject is measured against.

**Interactive element** `scenes[2].viz` — live plot of type `np-power`, initial state n=16, d=1.0, alpha=0.05, sd=4. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[2].ask`

- *question:* If the significance level α is fixed, what does power measure and how is it related to Type II error?
- *hint on request:* At a specified alternative, power is 1 − β; α controls the Type I error under the null.

---

### Scene 4 of 14 — The lemma, and how to actually use it

`scenes[3]` · id `s3` · type `theory` (theory) · 9 minutes

**Purpose** `scenes[3].objective`

State it precisely, then turn it into a critical region you can write down.

**Block 1 — Size, power and the power function** `scenes[3].blocks[0]` *(type `def`)*

The size of a test is α = P(reject H₀ | H₀ true). Its power at a particular alternative θ is β(θ) = P(reject H₀ | θ), and the power FUNCTION is that probability read as a function of θ. At θ = θ₀ the power function equals the size.

**Block 2 — The Neyman–Pearson lemma** `scenes[3].blocks[1]` *(type `formula`)*

To test simple H₀: θ = θ₀ against simple H₁: θ = θ₁, the test that rejects when
       Λ(x) = L(θ₁ | x) / L(θ₀ | x)  >  k,
with k chosen so that P(Λ > k | θ₀) = α, is MOST POWERFUL among all tests of size α.

**Block 3 — How to use it, in the order that works** `scenes[3].blocks[2]` *(type `step`)*

1. Write both likelihoods and form the ratio.
2. Cancel everything that does not involve the data.
3. Rearrange Λ > k into an inequality on a single statistic — usually x̄ or Σxᵢ.
4. Fix the constant from the SIZE condition, under H₀.
5. State the region, then compute power under H₁ if asked.

**Block 4 — The direction of the inequality** `scenes[3].blocks[3]` *(type `trap`)*

When you rearrange, dividing or multiplying by a negative quantity flips the inequality. For a one-sided test with θ₁ > θ₀ you should end up rejecting for LARGE values of the natural statistic; if you end up with 'small', re-check the algebra — or check that θ₁ < θ₀, in which case 'small' is correct.

**Block 5 — Randomised tests, and why discrete data need them** `scenes[3].blocks[4]` *(type `assume`)*

For a discrete statistic the achievable sizes are a finite list — for a Binomial(10, 0.5) you can get 0.0107 or 0.0547 but nothing in between. To obtain size exactly α, the test rejects outright above the boundary, rejects with probability γ AT the boundary, and accepts below. The lemma is stated for these randomised tests, which is why it holds in complete generality.

**Block 6 — What the lemma does not do** `scenes[3].blocks[5]` *(type `note`)*

It compares tests of the SAME size. It says nothing about whether α = 0.05 is a sensible choice, and it does not apply directly when either hypothesis is composite. Everything in the second half of this lesson exists to handle that second limitation.

**Flow diagram** `scenes[3].flow` — From two hypotheses to a critical region

*alt text* `.alt`: Flow chart for applying the Neyman–Pearson lemma

- row 1: Simple H₀: θ = θ₀ against simple H₁: θ = θ₁
- row 2: Form the ratio Λ = L(θ₁)/L(θ₀)
- row 3: Simplify: Λ > k becomes an inequality on a statistic T
- row 4: Is the data distribution continuous?
- row 5: Randomise on the boundary to hit size α exactly  |  Solve P(T > c | H₀) = α for c
- row 6: That region is the MOST POWERFUL size-α test
- row 7: Does c turn out free of θ₁?
- row 8: Then the same test is UMP against the whole one-sided alternative
- arrows: Simple H₀: θ = θ₀ against simple H₁: θ = θ₁ → Form the ratio Λ = L(θ₁)/L(θ₀); Form the ratio Λ = L(θ₁)/L(θ₀) → Simplify: Λ > k becomes an inequality on a statistic T; Simplify: Λ > k becomes an inequality on a statistic T → Is the data distribution continuous?; Is the data distribution continuous? → [no] Randomise on the boundary to hit size α exactly; Is the data distribution continuous? → [yes] Solve P(T > c | H₀) = α for c; Randomise on the boundary to hit size α exactly → That region is the MOST POWERFUL size-α test; Solve P(T > c | H₀) = α for c → That region is the MOST POWERFUL size-α test; That region is the MOST POWERFUL size-α test → Does c turn out free of θ₁?; Does c turn out free of θ₁? → [yes] Then the same test is UMP against the whole one-sided alternative

*note shown under the diagram* `.note`: The last diamond is the bridge from Neyman–Pearson to UMP. If the critical region does not depend on which θ₁ you used, the one test is simultaneously most powerful against all of them — which is what 'uniformly' means.

**Quick check before moving on** `scenes[3].ask`

- *question:* What is the central comparison in the Neyman–Pearson lemma for testing a simple null against a simple alternative?
- *hint on request:* Compare the likelihood ratio and reject where evidence in favour of the alternative is sufficiently large, choosing the cutoff to attain size α.

---

### Scene 5 of 14 — Worked in full — the normal mean

`scenes[4]` · id `s4` · type `worked` (worked example) · 7 minutes

**Purpose** `scenes[4].objective`

Run the lemma end to end and get a critical region with a number in it.

**Problem put to the learner** `scenes[4].problem`

X₁,…,X₂₅ are iid N(μ, σ²) with σ = 10 known. Test H₀: μ = 50 against H₁: μ = 55 at α = 0.05. Find the most powerful test, and its power.

**Worked steps** `scenes[4].steps[]`

1. `scenes[4].steps[0]` Write the likelihood ratio, keeping only what involves the data.

   ```
   Λ = exp{ −Σ(xᵢ−55)²/(2σ²) } / exp{ −Σ(xᵢ−50)²/(2σ²) }
  = exp{ [Σ(xᵢ−50)² − Σ(xᵢ−55)²] / (2σ²) }
   ```

   Laid out:

   $$Λ = \frac{exp{ −\frac{Σ(xᵢ−55)²}{(2σ²)} }}{exp{ −\frac{Σ(xᵢ−50)²}{(2σ²)} }} = exp{ [Σ(xᵢ−50)² − Σ(xᵢ−55)²] / (2σ²) }$$

   *why* `.why`: The normalising constants are identical under both hypotheses and cancel. Only the exponent carries information.

2. `scenes[4].steps[1]` Expand the difference of the two sums. The quadratic terms cancel.

   ```
   Σ(xᵢ−50)² − Σ(xᵢ−55)² = 10Σxᵢ − 25n(50+55)/… = 2(55−50)Σxᵢ − n(55² − 50²)
   ```

   *why* `.why`: Σxᵢ² appears in both and disappears. What survives is linear in Σxᵢ — which is why the test ends up being about x̄.

3. `scenes[4].steps[2]` So Λ is an increasing function of Σxᵢ. Therefore Λ > k is the same event as x̄ > c.

   ```
   Λ > k   ⇔   Σxᵢ > k′   ⇔   x̄ > c
   ```

   *why* `.why`: This is the step that matters. You never need the value of k: you only need to know which statistic the ratio is monotone in, and in which direction.

4. `scenes[4].steps[3]` Fix c from the size condition — computed under H₀, not H₁.

   ```
   P(X̄ > c | μ = 50) = 0.05 ,  X̄ ~ N(50, σ²/n) = N(50, 100/25) = N(50, 4)
c = 50 + 1.645(2) = 53.29
   ```

   Laid out:

   $$P(X̄ > c | μ = 50) = 0.05 ,  X̄ ~ N(50, \frac{σ²}{n}) = N(50, \frac{100}{25}) = N(50, 4)
c = 50 + 1.645(2) = 53.29$$

   *why* `.why`: σ/√n = 10/5 = 2. The alternative μ = 55 plays no part here at all — it told us the direction and nothing more.

5. `scenes[4].steps[4]` State the test.

   ```
   Reject H₀ when x̄ > 53.29. This is the most powerful size-0.05 test.
   ```

   *why* `.why`: By the lemma, no other test of size 0.05 has greater power against μ = 55.

6. `scenes[4].steps[5]` Now compute the power, under H₁.

   ```
   Power = P(X̄ > 53.29 | μ = 55) = P(Z > (53.29 − 55)/2) = P(Z > −0.855) = 0.804
   ```

   Laid out:

   $$Power = P(X̄ > 53.29 | μ = 55) = P(Z > \frac{(53.29 − 55)}{2}) = P(Z > −0.855) = 0.804$$

   *why* `.why`: Standardise using the H₁ mean and the same standard error. About 80% — the test will detect a shift of this size four times in five.

**What to take from it** `scenes[4].after`

Notice what the alternative did and did not do. It fixed the DIRECTION of the critical region — reject for large x̄ — and it determined the power. It did not appear in the critical value. That is the observation the next-but-one scene turns into the whole theory of UMP tests.

**Quick check before moving on** `scenes[4].ask`

- *question:* In the normal mean example, why does the most powerful test use a one-sided cutoff on the sample mean?
- *hint on request:* The likelihood ratio is monotone in the sample mean for the specified one-sided alternative.

---

### Scene 6 of 14 — Pause and recall

`scenes[5]` · id `s5` · type `recall` (retrieval practice) · 2 minutes

**Purpose** `scenes[5].objective`

Retrieve before reading on — this is where the retention comes from.

**Intro** `scenes[5].intro`

Answer each in your head before revealing. Correcting a wrong retrieval beats re-reading a right answer.

- `scenes[5].items[0]` **Q:** State the Neyman–Pearson lemma.  
  **A:** For simple H₀ against simple H₁, rejecting when L(θ₁)/L(θ₀) > k, with k set so the size is α, is most powerful among all size-α tests.
- `scenes[5].items[1]` **Q:** Which hypothesis is the critical value computed under?  
  **A:** H₀. The size condition is P(reject | H₀) = α; the alternative affects only the direction and the power.
- `scenes[5].items[2]` **Q:** What is the power function, and what is its value at θ₀?  
  **A:** β(θ) = P(reject | θ). At θ = θ₀ it equals the size α.
- `scenes[5].items[3]` **Q:** Why do discrete problems sometimes need a randomised test?  
  **A:** Because the achievable sizes form a finite set, so no ordinary critical region has size exactly α. Rejecting with probability γ on the boundary closes the gap.

---

### Scene 7 of 14 — Your turn, with the scaffolding removed — the exponential

`scenes[6]` · id `s6` · type `completion` (fill in the blanks) · 8 minutes

**Purpose** `scenes[6].objective`

Run the lemma yourself on a family where the algebra goes the other way.

**Problem put to the learner** `scenes[6].problem`

X₁,…,Xₙ are iid Exponential with mean θ, f(x) = (1/θ)e^(−x/θ). Test H₀: θ = θ₀ against H₁: θ = θ₁ with θ₁ > θ₀, at level α. Find the form of the most powerful test.

**Worked steps** `scenes[6].steps[]`

1. `scenes[6].steps[0]` Write the likelihood for a sample of size n.

   ```
   L(θ) = θ^(−n) exp(−Σxᵢ/θ)
   ```

   Laid out:

   $$L(θ) = θ^{−n} exp(−\frac{Σxᵢ}{θ})$$

   *why* `.why`: The exponential is a one-parameter family and the sample total Σxᵢ is already visible — a good sign that the test will be about it.

2. `scenes[6].steps[1]` Form the ratio and simplify.

   - *learner is asked:* Write Λ = L(θ₁)/L(θ₀), simplified.
   - *accepted answer* `.blank.answer`: (θ₀/θ₁)^n exp{Σxᵢ(1/θ₀ − 1/θ₁)}
   - *also accepted:* (θ₀/θ₁)^n exp{Σxᵢ(1/θ₀ − 1/θ₁)}; (θ0/θ1)^n exp(Sx(1/θ0-1/θ1)); (θ₀/θ₁)^n e^{Σx(1/θ₀−1/θ₁)}; (theta0/theta1)^n exp(sum x (1/theta0 - 1/theta1)); (θ₀/θ₁)^n exp(Σxᵢ(1/θ₀ − 1/θ₁))
   - *hint:* θ₁^(−n)/θ₀^(−n) = (θ₀/θ₁)^n. The exponents combine as −Σx/θ₁ + Σx/θ₀ = Σx(1/θ₀ − 1/θ₁).

   *why* `.why`: The leading constant does not involve the data, so it will be absorbed into k. Everything that matters is in the exponent.

3. `scenes[6].steps[2]` Since θ₁ > θ₀, the coefficient (1/θ₀ − 1/θ₁) is positive, so Λ increases with Σxᵢ. Say what the critical region looks like.

   - *learner is asked:* Complete: reject H₀ when Σxᵢ is …
   - *accepted answer* `.blank.answer`: large
   - *also accepted:* large; big; greater than c; > c; larger; large (Σx > c); high
   - *hint:* A positive coefficient in the exponent means Λ and Σxᵢ move together, so a large ratio is the same event as a large total.

   *why* `.why`: A larger mean makes a larger total more plausible — the direction agrees with intuition, which is always worth a moment's check.

4. `scenes[6].steps[3]` Identify the null distribution you need to fix the constant.

   - *learner is asked:* Under H₀, what is the distribution of ΣXᵢ?
   - *accepted answer* `.blank.answer`: Gamma(n, θ₀)
   - *also accepted:* Gamma(n, θ₀); gamma(n,theta0); Gamma(n,θ0); Gamma with shape n and scale θ₀; gamma(n, scale θ₀); 2ΣX/θ₀ ~ chi-square with 2n df; chi-square 2n
   - *hint:* A sum of n independent exponentials with mean θ₀ is gamma with shape n and scale θ₀. Equivalently 2ΣXᵢ/θ₀ follows a chi-square distribution on 2n degrees of freedom, which is the form the tables are in.

   *why* `.why`: The chi-square form is the useful one in an exam: c is read from a chi-square table rather than computed.

5. `scenes[6].steps[4]` Put the test together.

   ```
   Reject H₀ when Σxᵢ > c, with c fixed by P(ΣXᵢ > c | θ₀) = α,
i.e. 2c/θ₀ = χ²(2n) upper-α point
   ```

   Laid out:

   $$Reject H₀ when Σxᵢ > c, with c fixed by P(ΣXᵢ > c | θ₀) = α,
i.e. \frac{2c}{θ₀} = χ²(2n) upper-α point$$

   *why* `.why`: And note the constant does not involve θ₁ at all.

**What to take from it** `scenes[6].after`

Because c came out free of θ₁, the same test is most powerful against EVERY θ₁ greater than θ₀ — not just the one you started with. That is the definition of a uniformly most powerful test, and it fell out of the algebra rather than being imposed. The next scene explains when you can count on that happening.

---

### Scene 8 of 14 — MLR, Karlin–Rubin, and the wall that two-sided alternatives hit

`scenes[7]` · id `s7` · type `theory` (theory) · 10 minutes

**Purpose** `scenes[7].objective`

Get the general condition for a one-sided UMP test, and the exact reason two-sided fails.

**Block 1 — Monotone likelihood ratio** `scenes[7].blocks[0]` *(type `def`)*

A family {f(x;θ)} has monotone likelihood ratio in the statistic T if, for every pair θ₂ > θ₁, the ratio f(x;θ₂)/f(x;θ₁) is a non-decreasing function of T(x). The ratio may depend on the data only through T, and it must move the same way for every such pair.

**Block 2 — Karlin–Rubin theorem** `scenes[7].blocks[1]` *(type `formula`)*

If the family has MLR in T, then for testing
     H₀: θ ≤ θ₀   against   H₁: θ > θ₀,
the test that rejects when T > c, with c fixed by P(T > c | θ₀) = α, is UNIFORMLY MOST POWERFUL at level α.

**Block 3 — Where MLR comes from in practice** `scenes[7].blocks[2]` *(type `note`)*

Every one-parameter exponential family with a strictly increasing natural parameter has MLR in its natural statistic. That covers the binomial in p, the Poisson in λ, the normal in μ with σ known, and the exponential in its mean. So in the exam the chain is: recognise the exponential family, name the natural statistic, quote Karlin–Rubin, write the region.

**Block 4 — The power function of the one-sided normal test** `scenes[7].blocks[3]` *(type `formula`)*

For N(μ, σ²) with σ known, rejecting when x̄ > μ₀ + z_α σ/√n:
     β(μ) = 1 − Φ( z_α − (μ − μ₀)√n / σ )
β(μ₀) = α, and β increases in both (μ − μ₀) and n.

**Block 5 — Why there is no UMP test for a two-sided alternative** `scenes[7].blocks[4]` *(type `trap`)*

Test H₀: μ = μ₀ against H₁: μ ≠ μ₀. Against a particular μ₁ > μ₀ the most powerful test rejects in the UPPER tail; against a particular μ₁ < μ₀ it rejects in the LOWER tail. A single test cannot be both. Any test that is best against the upper alternatives is beaten on the lower ones, so no test is most powerful uniformly over the whole alternative — and the question 'find the UMP test for H₁: μ ≠ μ₀' has the answer 'none exists'.

**Block 6 — What is used instead** `scenes[7].blocks[5]` *(type `def`)*

UNBIASED test: one whose power never falls below its size, β(θ) ≥ α for every θ in the alternative. Restricting attention to unbiased tests and finding the best among them gives the UMPU test, and for the two-sided normal mean that is the familiar symmetric two-tailed test. The other general-purpose answer is the likelihood ratio test, which is not optimal in general but is always available.

**Block 7 — A second way UMP fails** `scenes[7].blocks[6]` *(type `note`)*

Even one-sided, a UMP test can fail to exist when the family lacks MLR — the Cauchy location family is the standard example, and there the critical region genuinely depends on which alternative you aim at. MLR is what rules that out.

**Quick check before moving on** `scenes[7].ask`

- *question:* What is the extra condition required by the Karlin–Rubin theorem beyond a one-sided hypothesis?
- *hint on request:* The family must have a monotone likelihood ratio in an appropriate statistic, with regularity and parameter-space conditions matching the theorem.

---

### Scene 9 of 14 — Why one cut-off cannot serve both sides

`scenes[8]` · id `s8` · type `explore` (interactive visualisation) · 7 minutes

**Purpose** `scenes[8].objective`

See the two-sided failure as a picture rather than as an assertion.

**Body** `scenes[8].body[]`

Keep the same display, and this time think of the gap slider as moving the alternative around the null rather than fixing it.

With the gap positive, the upper-tail test shown here has good power — the amber missed-detection area is small. Now slide the gap to zero and then imagine it negative. The alternative curve moves to the LEFT of the null, entirely into the acceptance region. This test's power against a downward shift is not merely poor; it is below α, because the alternative curve has almost nothing to the right of the cut-off.

That is the two-sided problem in one observation. A test that is most powerful against upward shifts is actively worse than useless against downward ones. The mirror-image test has the mirror-image defect. No single rejection region can be best against both, which is precisely why no UMP test exists for H₁: μ ≠ μ₀.

A test whose power dips below its own size, as this one does for negative gaps, is called BIASED — you are more likely to reject when the null is true than when that particular alternative is. Ruling those out is what the unbiasedness restriction does, and the symmetric two-tailed test is the best of what remains. That is the UMPU test.

One more thing worth confirming on the slider: at a fixed gap, raising n raises power while α stays put, but it never rescues the direction. Sample size fixes precision, not a critical region pointed the wrong way.

**Interactive element** `scenes[8].viz` — live plot of type `np-power`, initial state n=25, d=2.0, alpha=0.05, sd=10. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[8].ask`

- *question:* Why can a single rejection threshold fail to be uniformly most powerful for a two-sided alternative?
- *hint on request:* The two sides favour opposite tails, so a test best for one direction need not be best for the other.

**Optional deep-dive, opened on demand — Why a trial protocol names α first and n last** `scenes[8].scenario`

*teaser on the closed card:* A regulator fixes the false-positive rate, and the sponsor sizes the trial around it.

> A clinical trial protocol fixes the significance level before anything else. The regulator's interest is asymmetric: approving a drug that does not work is a different kind of failure from missing one that does, and the first is the one the fixed level controls.

> That asymmetry is exactly the Neyman–Pearson framing. The Type I error rate is a constraint, not a quantity to be traded off; subject to it, the sponsor wants the most powerful test available against the alternative that matters clinically. For the comparison the protocol specifies, the likelihood ratio gives that test, and it reduces to a critical value on a single summary statistic.

> Sample size is then the only remaining lever. With α fixed by the regulator and the clinically relevant effect fixed by the question being asked, power is a function of n alone, and the protocol solves for the n that reaches the power the committee requires — typically 80% or 90%. Everything in a power calculation is this one rearrangement.

> Where this gets misread is in what a non-significant result then means. The test was built to control false positives, not to make absence of evidence into evidence of absence, and a trial that failed to reach significance at a sample size chosen for 80% power had, by construction, a one-in-five chance of missing a real effect of that size.

*closing line:* Fix the error you care most about, then buy power with sample size — the whole protocol is that sentence with numbers in it.

---

### Scene 10 of 14 — Now without the steps — a one-sided Bernoulli test

`scenes[9]` · id `s9` · type `guided` (guided problem) · 8 minutes

**Purpose** `scenes[9].objective`

Apply Karlin–Rubin to a discrete family and meet the randomisation issue for real.

**Problem put to the learner** `scenes[9].problem`

X₁,…,X₂₀ are iid Bernoulli(p). Test H₀: p ≤ 0.3 against H₁: p > 0.3 at level α = 0.05. Find the UMP test, give its critical region, and state its exact size. You may use that for T ~ Binomial(20, 0.3): P(T ≥ 10) = 0.0480 and P(T ≥ 9) = 0.1133.

**Hint ladder, revealed one at a time** `scenes[9].hints[]`

1. Direction — the Bernoulli is a one-parameter exponential family. Identify the natural statistic and check which way the likelihood ratio moves as p increases; that tells you MLR and the direction of the region in one step.
2. Method — quote Karlin–Rubin rather than redoing Neyman–Pearson. It gives you the form 'reject when T > c' immediately, and your only remaining job is to choose c from the size condition at the BOUNDARY value p = 0.3.
3. Next step — the size condition cannot be met exactly here, because T is discrete. Look at the two tail probabilities you were given, pick the critical region whose size does not exceed 0.05, and then say what would be needed to achieve 0.05 exactly.

**Model solution, hidden until requested** `scenes[9].solution[]`

1. `scenes[9].solution[0]` Write the family in exponential form to confirm MLR.

   ```
   f(x;p) = p^x(1−p)^(1−x) = (1−p)·exp{ x·log(p/(1−p)) }
T = ΣXᵢ, natural parameter log(p/(1−p)), strictly increasing in p
   ```

   Laid out:

   $$f(x;p) = p^{x}(1−p)^{1−x} = (1−p)·exp{ x·log\frac{p}{(1−p)} }
T = ΣXᵢ, natural parameter log\frac{p}{(1−p)}, strictly increasing in p$$

2. `scenes[9].solution[1]` Increasing natural parameter ⇒ MLR in T. Apply Karlin–Rubin.

   ```
   The UMP level-α test for H₀: p ≤ 0.3 vs H₁: p > 0.3 rejects when T > c
   ```

3. `scenes[9].solution[2]` Fix c at the boundary of the null, p = 0.3, where the size is largest.

   ```
   T ~ Binomial(20, 0.3).  Need P(T ≥ c+1 | p = 0.3) ≤ 0.05
   ```

4. `scenes[9].solution[3]` Read the two given probabilities and choose.

   ```
   P(T ≥ 10) = 0.0480 ≤ 0.05  ✓     P(T ≥ 9) = 0.1133 > 0.05  ✗
So reject when T ≥ 10
   ```

5. `scenes[9].solution[4]` State the exact size.

   ```
   size = P(T ≥ 10 | p = 0.3) = 0.0480, not 0.0500
   ```

6. `scenes[9].solution[5]` Say what exact size 0.05 would require.

   ```
   Reject when T ≥ 10; when T = 9, reject with probability
γ = (0.05 − 0.0480)/(0.1133 − 0.0480) = 0.0020/0.0653 = 0.031
   ```

   Laid out:

   $$Reject when T ≥ 10; when T = 9, reject with probability
γ = \frac{(0.05 − 0.0480)}{(0.1133 − 0.0480)} = 0.\frac{0020}{0}.0653 = 0.031$$

**Final answer given to the learner** `scenes[9].answer`

The Bernoulli is a one-parameter exponential family with increasing natural parameter, so it has MLR in T = ΣXᵢ and Karlin–Rubin applies: the UMP level-0.05 test rejects when T ≥ 10. Its exact size is 0.0480. To obtain size exactly 0.05 the test must be randomised — reject outright when T ≥ 10, and when T = 9 reject with probability γ ≈ 0.031.

**Self-check offered** `scenes[9].check`

Three things an examiner looks for. The size is evaluated at the BOUNDARY p = 0.3, not somewhere inside the null — a composite null takes its size from its worst case. The achieved size 0.0480 is below 0.05 and that is correct for a non-randomised test; claiming 0.05 exactly without randomising is the error. And the word UMP is earned here by citing MLR plus Karlin–Rubin, not by appealing to Neyman–Pearson, which only covers simple against simple.

---

### Scene 11 of 14 — Six statements — verdict on each before you look

`scenes[10]` · id `s10` · type `trapcheck` (true/false check) · 6 minutes

**Purpose** `scenes[10].objective`

Practise the per-statement discipline the real multi-statement items demand.

**Intro** `scenes[10].intro`

Give every statement a true or false verdict first. In the exam these six would be one question scored all or nothing, so a verdict you skipped is a mark you gambled.

- `scenes[10].items[0]` **Claim:** The Neyman–Pearson lemma applies to a simple null against a simple alternative.  
  **Verdict: TRUE.** True, and that restriction is the point. Extending it to composite alternatives is what MLR and Karlin–Rubin are for.
- `scenes[10].items[1]` **Claim:** The critical value of the most powerful test depends on the value specified by the alternative.  
  **Verdict: FALSE.** False. The constant is fixed by the size condition computed under H₀. The alternative determines the DIRECTION of the region and the power, nothing else.
- `scenes[10].items[2]` **Claim:** A UMP test exists for H₀: μ = μ₀ against H₁: μ ≠ μ₀ in the normal family with σ known.  
  **Verdict: FALSE.** False — the standard counterexample. The best test against upper alternatives rejects in the upper tail and the best against lower ones in the lower tail; no single region is best against both. The usual answer is the UMPU two-tailed test.
- `scenes[10].items[3]` **Claim:** If a family has monotone likelihood ratio in T, a UMP test exists for a one-sided alternative.  
  **Verdict: TRUE.** True — that is Karlin–Rubin, and it is the main tool for getting from a simple-versus-simple lemma to a composite alternative.
- `scenes[10].items[4]` **Claim:** Raising the significance level α increases the power of a test.  
  **Verdict: TRUE.** True. A larger α moves the cut-off into the alternative, so power rises — at the cost of more false rejections. It is a trade, not a free gain.
- `scenes[10].items[5]` **Claim:** For discrete data a non-randomised test can always achieve size exactly α.  
  **Verdict: FALSE.** False. The achievable sizes form a finite set; for Binomial(20, 0.3) you can have 0.0480 or 0.1133 but nothing between. Exact size α needs randomisation on the boundary.

---

### Scene 12 of 14 — Transfer — show that no UMP test exists

`scenes[11]` · id `s11` · type `guided` (guided problem) · 9 minutes

**Purpose** `scenes[11].objective`

Produce the standard non-existence argument, which is an exam answer in its own right.

**Problem put to the learner** `scenes[11].problem`

X₁,…,Xₙ are iid N(μ, σ²) with σ² known. Show that no uniformly most powerful level-α test exists for H₀: μ = μ₀ against H₁: μ ≠ μ₀. State what is used instead and why it is the natural replacement.

**Hint ladder, revealed one at a time** `scenes[11].hints[]`

1. Direction — a non-existence proof needs a contradiction. Suppose a UMP test did exist, and compare it with the two one-sided tests on their own home ground.
2. Method — use Neyman–Pearson twice. For a fixed μ₁ > μ₀, identify the unique most powerful size-α test. Then do the same for a fixed μ₂ < μ₀. Notice the two regions are different, and that each is UNIQUE at its own alternative.
3. Next step — a UMP test would have to be at least as powerful as each of them at their own alternative. Uniqueness then forces it to equal both regions at once, which is impossible. Then say which extra condition rescues the situation.

**Model solution, hidden until requested** `scenes[11].solution[]`

1. `scenes[11].solution[0]` Fix an alternative above the null and apply the lemma.

   ```
   For μ₁ > μ₀ the unique MP size-α test rejects when x̄ > μ₀ + z_α σ/√n.  Call this region R₊
   ```

   Laid out:

   $$For μ₁ > μ₀ the unique MP size-α test rejects when x̄ > μ₀ + z_α \frac{σ}{√n}.  Call this region R₊$$

2. `scenes[11].solution[1]` Now fix an alternative below the null and apply the lemma again.

   ```
   For μ₂ < μ₀ the unique MP size-α test rejects when x̄ < μ₀ − z_α σ/√n.  Call this region R₋
   ```

   Laid out:

   $$For μ₂ < μ₀ the unique MP size-α test rejects when x̄ < μ₀ − z_α \frac{σ}{√n}.  Call this region R₋$$

3. `scenes[11].solution[2]` Suppose a UMP level-α test with region R existed. By definition it is at least as powerful as any other size-α test at EVERY alternative.

   ```
   power_R(μ₁) ≥ power_{R₊}(μ₁)  and  power_R(μ₂) ≥ power_{R₋}(μ₂)
   ```

4. `scenes[11].solution[3]` But R₊ is the unique most powerful test at μ₁, so matching its power forces R = R₊. The same argument at μ₂ forces R = R₋.

   ```
   R = R₊  and  R = R₋ ,  yet  R₊ ∩ R₋ = ∅
   ```

5. `scenes[11].solution[4]` Two disjoint non-empty regions cannot be equal. The assumption fails.

   ```
   No UMP level-α test exists for the two-sided alternative. ∎
   ```

6. `scenes[11].solution[5]` Identify the replacement and why it is natural.

   ```
   R₊ is BIASED: its power at μ₂ < μ₀ is below α. Requiring β(μ) ≥ α for all μ ≠ μ₀ excludes both one-sided tests, and the best remaining test — the UMPU test — is the symmetric two-tailed region |x̄ − μ₀| > z_(α/2) σ/√n.
   ```

   Laid out:

   $$R₊ is BIASED: its power at μ₂ < μ₀ is below α. Requiring β(μ) ≥ α for all μ ≠ μ₀ excludes both one-sided tests, and the best remaining test — the UMPU test — is the symmetric two-tailed region |x̄ − μ₀| > z_\frac{α}{2} \frac{σ}{√n}.$$

**Final answer given to the learner** `scenes[11].answer`

Neyman–Pearson gives a unique most powerful test at each simple alternative: the upper-tail region for μ₁ > μ₀ and the lower-tail region for μ₂ < μ₀. A UMP test would have to coincide with both, and they are disjoint, so none exists. Restricting to unbiased tests removes the two one-sided regions, and the best of what remains is the two-tailed test |x̄ − μ₀| > z_(α/2)σ/√n — the UMPU test, and the one actually used.

**Self-check offered** `scenes[11].check`

The structure of this argument is worth more than the result, because it is the template for every non-existence question in this topic: find two alternatives whose optimal tests differ, invoke uniqueness, derive the contradiction. Note also where the word 'unbiased' earns its keep — it is not a decorative condition but exactly the one that eliminates the two offending candidates.

---

### Scene 13 of 14 — What you should now be able to do unaided

`scenes[12]` · id `s12` · type `summary` (summary) · 3 minutes

**Purpose** `scenes[12].objective`

Close the loop before the test.

**Body** `scenes[12].body[]`

Write the likelihood ratio for a simple-versus-simple problem, simplify it to an inequality on a statistic, and fix the constant from the size condition under H₀.

Keep the alternative out of the critical value, and use it only for the direction of the region and for power.

Recognise a one-parameter exponential family, name its natural statistic, and quote MLR plus Karlin–Rubin to write a one-sided UMP test in one line.

Compute a power function, know that β(θ₀) = α, and say how power responds to the gap, to n and to α.

Say immediately that no UMP test exists for a two-sided alternative, give the disjoint-regions reason, and name UMPU and the likelihood ratio test as the replacements.

Handle a discrete problem honestly: pick the region whose size does not exceed α, report the exact size, and give the randomisation probability if exact α is demanded.

The mastery test is ten unseen questions across all of this. Hints are off. The pass is 80% overall with 70% floors on the numerical and multi-statement items.

---

### Scene 14 of 14 — Mastery test

`scenes[13]` · id `s13` · type `quiz` (mastery test) · 12 minutes

**Purpose** `scenes[13].objective`

Demonstrate it independently, on unseen questions.

Draws from the pool reproduced below. `scenes[13].setId` = `inference_t9_mastery`

---

## Revision material `revision`

**Revision sheet** `revision.sheet[]` (13 lines)

1. `[0]` Simple hypothesis: specifies the distribution completely (H₀: θ = θ₀). Composite: a set of values (H₀: θ ≤ θ₀).
2. `[1]` Size α = P(reject H₀ | H₀ true), the Type I error rate you choose. β = P(accept H₀ | H₁ true). Power = 1 − β.
3. `[2]` Neyman–Pearson: for simple vs simple, the most powerful size-α test rejects when L(θ₁)/L(θ₀) > k, with k fixed by P(reject | H₀) = α.
4. `[3]` Always simplify the ratio into an inequality on a statistic, then find the constant from the size condition.
5. `[4]` For discrete data an exact α may need a randomised test: reject with probability γ on the boundary.
6. `[5]` MLR in T: for θ₂ > θ₁ the ratio L(θ₂)/L(θ₁) is a non-decreasing function of T.
7. `[6]` Karlin–Rubin: with MLR in T, 'reject when T > c' is UMP for H₀: θ ≤ θ₀ against H₁: θ > θ₀.
8. `[7]` One-parameter exponential families have MLR in the natural statistic — which is why one-sided UMP tests exist for them.
9. `[8]` No UMP test exists for a two-sided alternative in these families: the one-sided tests point opposite ways and neither beats the other everywhere.
10. `[9]` What is used instead: UMPU (adding the unbiasedness requirement), or the likelihood ratio test.
11. `[10]` Power function β(θ) = P(reject | θ). At θ = θ₀ it equals α; it rises with the gap and with n.
12. `[11]` Normal mean, σ known, one-sided: reject when x̄ > μ₀ + z_α·σ/√n. Power at μ₁ is 1 − Φ(z_α − (μ₁−μ₀)√n/σ).
13. `[12]` Raising n raises power at fixed α. Raising α raises power too — the two errors trade and cannot both shrink at fixed n.

**Flashcards** `revision.cards[]`

| Front | Back |
|---|---|
| State the Neyman–Pearson lemma. | For simple H₀ vs simple H₁, the test rejecting when L(θ₁)/L(θ₀) > k, with k chosen so the size is α, is most powerful among all size-α tests. |
| Why is the likelihood ratio the right statistic? | Because the lemma proves it: no other size-α test can have greater power. It is forced, not chosen. |
| What does MLR mean? | The likelihood ratio for two parameter values is a monotone function of a single statistic T, for every such pair. |
| State Karlin–Rubin. | If the family has MLR in T, then rejecting when T > c is UMP for H₀: θ ≤ θ₀ against H₁: θ > θ₀. |
| Why does no UMP test exist for a two-sided alternative? | The most powerful test against μ > μ₀ rejects in the upper tail; against μ < μ₀ it rejects in the lower. Neither is most powerful on both sides, so no single test is best uniformly. |
| What replaces UMP when it does not exist? | UMPU — restrict to unbiased tests and find the best among those — or fall back on the likelihood ratio test. |
| What is a randomised test and when is one needed? | On the boundary, reject with probability γ rather than always or never. Needed for discrete data, where no non-randomised region has size exactly α. |
| Define the power function. | β(θ) = P(reject H₀ | θ), as a function of the true parameter. It equals α at θ₀ and rises as θ moves into the alternative. |
| One-sided normal test, σ known: the critical region? | Reject when x̄ > μ₀ + z_α σ/√n. |
| How do α, n and power move together? | At fixed n, lowering α lowers power. At fixed α, raising n raises power. Only n buys both. |

**Memory aids** `revision.tricks[]`

- `[0]` **Fix one error, minimise the other** — You cannot make α and β small together at fixed n. Neyman–Pearson fixes α and does the best possible on β.
- `[1]` **Ratio big ⇒ reject** — L(θ₁)/L(θ₀) > k. Large ratio means the data look much more like H₁ than H₀.
- `[2]` **Simplify, then size it** — Turn the ratio into an inequality on a statistic FIRST; only then use P(reject | H₀) = α to pin the constant.
- `[3]` **MLR ⇒ one-sided UMP, and only one-sided** — Karlin–Rubin gives a UMP test for a one-sided alternative. Two-sided kills it, because the two tails disagree.

**Elimination shortcuts for multiple-choice items** `revision.shortcuts[]`

- `[0]` One-parameter exponential family ⇒ MLR in the natural statistic ⇒ a one-sided UMP test exists. That chain answers most UMP questions in one line.
- `[1]` Normal mean, σ known: reject when x̄ > μ₀ + 1.645σ/√n at α = 0.05 one-sided; 1.96 for two-sided.
- `[2]` The critical value never involves the alternative — only μ₀, σ, n and α. The alternative only affects POWER.
- `[3]` If a question says 'two-sided' and asks for a UMP test, the answer is that none exists.

**If nothing else is remembered** `revision.remember[]`

- `[0]` A UMP test for a two-sided alternative does not exist in the standard one-parameter families. Saying so IS the answer.
- `[1]` Size is what you set under H₀; power is what you get under H₁. Never quote one for the other.

**Errors to avoid** `revision.traps[]`

- `[0]` Putting the alternative into the critical value. The cut-off depends on H₀, n and α only.
- `[1]` Forgetting the randomisation on the boundary for discrete data, then claiming size exactly α.
- `[2]` Saying a UMP test exists two-sided because the family is nice. MLR buys one-sided only.
- `[3]` Confusing 'most powerful' (simple vs simple) with 'uniformly most powerful' (over a whole composite alternative).

---

## Mastery pool — all 20 items with answer keys `qsets/mastery`

Ten are drawn per attempt at 3 easy / 5 moderate / 2 hard. Keys are distributed five to each option letter. Please check each item for a second defensible answer as well as for the correctness of its stated key and explanation.

### Q1 — `inf-t9-m-01` *(single, easy)*

The Neyman–Pearson lemma gives the most powerful test for:

*Options* `.options[]`:

- **A.** a simple null against a simple alternative  ← key
- **B.** a simple null against a composite alternative
- **C.** any null against any alternative
- **D.** a composite null against a composite alternative

*Explanation* `.explanation`: The lemma is stated for two completely specified hypotheses. Composite alternatives need monotone likelihood ratio and Karlin–Rubin, and even then only for a one-sided alternative.

### Q2 — `inf-t9-m-02` *(single, easy)*

The size of a test is:

*Options* `.options[]`:

- **A.** P(reject H₀ | H₁ is true)
- **B.** P(reject H₀ | H₀ is true)  ← key
- **C.** 1 − P(reject H₀ | H₁ is true)
- **D.** P(accept H₀ | H₁ is true)

*Explanation* `.explanation`: Size is the Type I error rate, computed entirely under the null. Option A is power, option D is β, and option C is also β written the long way.

### Q3 — `inf-t9-m-03` *(numeric, moderate)*

X₁,…,X₁₆ are iid N(μ, 36) with σ² = 36 known. Test H₀: μ = 10 against H₁: μ = 13 at α = 0.05. Give the critical value for x̄.

*Options* `.options[]`:

- **A.** 11.47
- **B.** 10.62
- **C.** 12.47  ← key
- **D.** 13.00

*Explanation* `.explanation`: σ/√n = √36/√16 = 6/4 = 1.5, so the region is x̄ > 10 + 1.645(1.5) = 10 + 2.47 = 12.47. Option D mistakes the alternative for the critical value — the alternative never appears in the cut-off, and option B uses σ² where σ belongs.

*Arithmetic check* `.check`: The critical value uses μ₀, σ, n and α only. If the number 13 appears in it, the size condition has been computed under the wrong hypothesis.

### Q4 — `inf-t9-m-04` *(numeric, moderate)*

Continuing the previous setting — n = 16, σ = 6, H₀: μ = 10, H₁: μ = 13, reject when x̄ > 12.47. Give the power of the test.

*Options* `.options[]`:

- **A.** 0.846
- **B.** 0.050
- **C.** 0.361
- **D.** 0.639  ← key

*Explanation* `.explanation`: Power = P(X̄ > 12.47 | μ = 13) = P(Z > (12.47 − 13)/1.5) = P(Z > −0.355) = 0.639. Option C is β = 1 − power, the probability of missing a shift of this size.

*Arithmetic check* `.check`: Power must exceed α whenever the alternative differs from the null, and β = 1 − power. An answer of 0.05 means the power was evaluated at μ₀ rather than μ₁.

### Q5 — `inf-t9-m-05` *(multi, hard)*

Consider the Neyman–Pearson lemma and what it delivers.

*Statements to judge* `.statements[]`:

- **A.** The lemma compares tests of the same size α.
- **B.** The critical value depends on the value of the alternative.
- **C.** A randomised test may be needed to attain size exactly α.
- **D.** No size-α test has greater power than the likelihood ratio test.

*Options* `.options[]`:

- **A.** A, C and D only  ← key
- **B.** A and B only
- **C.** B and C only
- **D.** A, B and D only

*Explanation* `.explanation`: A is true — the lemma is a statement about tests of equal size. B is false: the constant is fixed by the size condition under H₀, so the alternative never enters it. C is true, and it is why the lemma holds in full generality for discrete data. D is true — among size-α tests none has greater power.

*Verdict on each statement* `.verdicts`:

- **A — true.** Power is only comparable between tests of equal size; otherwise you could buy power with α.
- **B — false.** P(reject | H₀) = α fixes the constant. The alternative sets the direction and the power only.
- **C — true.** Discrete statistics attain only finitely many sizes; randomising on the boundary closes the gap.
- **D — true.** That is precisely the conclusion of the lemma.

### Q6 — `inf-t9-m-06` *(single, easy)*

Monotone likelihood ratio in T means that:

*Options* `.options[]`:

- **A.** the likelihood itself is a monotone function of θ
- **B.** for every θ₂ > θ₁ the ratio f(x;θ₂)/f(x;θ₁) is a non-decreasing function of T  ← key
- **C.** T is a monotone function of the parameter
- **D.** the power function is monotone in T

*Explanation* `.explanation`: MLR is a condition on the RATIO of two densities, required for every pair of parameter values, and it says the ratio depends on the data only through T and moves one way in T. It is the hypothesis of the Karlin–Rubin theorem.

### Q7 — `inf-t9-m-07` *(single, moderate)*

For which testing problem does a UMP test fail to exist in the N(μ, σ²) family with σ² known?

*Options* `.options[]`:

- **A.** H₀: μ ≤ μ₀ against H₁: μ > μ₀
- **B.** H₀: μ = μ₀ against H₁: μ = μ₁ with μ₁ > μ₀
- **C.** H₀: μ = μ₀ against H₁: μ ≠ μ₀  ← key
- **D.** H₀: μ ≥ μ₀ against H₁: μ < μ₀

*Explanation* `.explanation`: The two-sided alternative is the standard failure. The most powerful test against an alternative above μ₀ rejects in the upper tail and the one against an alternative below rejects in the lower; the two regions are disjoint, so no single test is best against both. The other three are one-sided or simple and all have UMP or MP tests.

### Q8 — `inf-t9-m-08` *(multi, hard)*

Consider uniformly most powerful tests.

*Statements to judge* `.statements[]`:

- **A.** MLR in T gives a UMP test for a one-sided alternative.
- **B.** A one-parameter exponential family has MLR in its natural statistic.
- **C.** Every testing problem has a UMP test if the family is an exponential family.
- **D.** For the two-sided normal mean, the UMPU test is the symmetric two-tailed test.

*Options* `.options[]`:

- **A.** A, B and C only
- **B.** B and C only
- **C.** A and C only
- **D.** A, B and D only  ← key

*Explanation* `.explanation`: A is true — this is Karlin–Rubin. B is true: one-parameter exponential families with increasing natural parameter have MLR in the natural statistic. C is false, and it is the headline failure of the topic: two-sided alternatives admit no UMP test. D is true — the unbiasedness restriction eliminates the one-sided candidates and leaves the two-tailed test as UMPU.

*Verdict on each statement* `.verdicts`:

- **A — true.** Karlin–Rubin, which is how a composite one-sided alternative is handled.
- **B — true.** With a strictly increasing natural parameter, which covers the binomial, Poisson, normal mean and exponential.
- **C — false.** Two-sided alternatives have no UMP test even in the nicest families.
- **D — true.** Unbiasedness rules out both one-sided regions; the symmetric two-tailed test is best among what remains.

### Q9 — `inf-t9-m-09` *(numeric, moderate)*

X₁,…,Xₙ are iid Bernoulli(p). For testing H₀: p ≤ p₀ against H₁: p > p₀, the UMP test rejects when:

*Options* `.options[]`:

- **A.** ΣXᵢ > c, with c fixed by P(ΣXᵢ > c | p₀) = α  ← key
- **B.** ΣXᵢ < c, with c fixed by P(ΣXᵢ < c | p₀) = α
- **C.** ΣXᵢ > c, with c fixed by P(ΣXᵢ > c | p₁) = α
- **D.** |ΣXᵢ − np₀| > c

*Explanation* `.explanation`: The Bernoulli is a one-parameter exponential family with natural parameter log(p/(1−p)), increasing in p, so it has MLR in ΣXᵢ and Karlin–Rubin gives an upper-tail region. The size is evaluated at the boundary p₀, which is where a composite null is worst.

*Arithmetic check* `.check`: For a composite null H₀: p ≤ p₀, the size is the supremum over the null — attained at the boundary p₀. Evaluating anywhere else understates it.

### Q10 — `inf-t9-m-10` *(numeric, moderate)*

A test of H₀: μ = 100 against H₁: μ > 100 rejects when x̄ > 104, with σ = 15 and n = 36. Give the size of the test.

*Options* `.options[]`:

- **A.** 0.945
- **B.** 0.055  ← key
- **C.** 0.159
- **D.** 0.025

*Explanation* `.explanation`: σ/√n = 15/6 = 2.5, so the standardised cut-off is (104 − 100)/2.5 = 1.6 and the size is P(Z > 1.6) = 0.0548. Option A is the complement and option C uses a standard error of 1 rather than 2.5.

*Arithmetic check* `.check`: Size is an upper-tail probability under H₀, so it should be small. Any answer above 0.5 has the tail the wrong way round.

### Q11 — `inf-t9-m-11` *(single, easy)*

The power function β(θ) of a test evaluated at θ = θ₀ equals:

*Options* `.options[]`:

- **A.** zero
- **B.** 1 − α
- **C.** the size α of the test  ← key
- **D.** one

*Explanation* `.explanation`: β(θ) = P(reject | θ), so at the null value it is exactly the Type I error rate. This is the standard consistency check on any power function you derive: if it does not return α at θ₀, the derivation is wrong.

### Q12 — `inf-t9-m-12` *(numeric, hard)*

X₁,…,Xₙ are iid Exponential with mean θ. For H₀: θ = θ₀ against H₁: θ = θ₁ with θ₁ > θ₀, the most powerful test rejects when:

*Options* `.options[]`:

- **A.** Σxᵢ < c, with 2c/θ₀ the lower-α point of χ²(2n)
- **B.** Σxᵢ > c, with 2c/θ₁ the upper-α point of χ²(2n)
- **C.** x̄ > c, with c the upper-α point of N(θ₀, θ₀²/n)
- **D.** Σxᵢ > c, with 2c/θ₀ the upper-α point of χ²(2n)  ← key

*Explanation* `.explanation`: The ratio is (θ₀/θ₁)ⁿ exp{Σxᵢ(1/θ₀ − 1/θ₁)}, and with θ₁ > θ₀ the coefficient is positive, so the ratio increases with Σxᵢ — reject for large totals. Under H₀, ΣXᵢ is Gamma(n, θ₀), equivalently 2ΣXᵢ/θ₀ is χ²(2n), which is the form the tables take. Option B sizes the test under the alternative.

*Arithmetic check* `.check`: Two checks: the direction should agree with intuition (a larger mean makes a larger total plausible), and the constant must be fixed under θ₀.

### Q13 — `inf-t9-m-13` *(multi, moderate)*

Consider the two error types and how they move.

*Statements to judge* `.statements[]`:

- **A.** At a fixed sample size, lowering α raises β.
- **B.** Increasing the sample size raises β at fixed α.
- **C.** A test's power at the null value equals its size.
- **D.** A test is unbiased if its power never falls below its size.

*Options* `.options[]`:

- **A.** A, C and D only  ← key
- **B.** A and B only
- **C.** B and C only
- **D.** A, B and C only

*Explanation* `.explanation`: A is true — at fixed n, moving the cut-off trades one error against the other. B is false: increasing n lowers β at fixed α, which is the whole reason to collect more data. C is true, and is the floor on power. D is true by definition of an unbiased test.

*Verdict on each statement* `.verdicts`:

- **A — true.** One cut-off, two tails: moving it to shrink one area grows the other.
- **B — false.** The opposite. Larger n narrows both sampling distributions, so β falls with α unchanged.
- **C — true.** β(θ₀) = α by definition of the power function.
- **D — true.** β(θ) ≥ α for every θ in the alternative — which the one-sided tests violate on the far side.

### Q14 — `inf-t9-m-14` *(numeric, moderate)*

A one-sided test of a normal mean has power 0.60 at a particular alternative with n = 25. Roughly what sample size would raise the power to about 0.85 at the same alternative and the same α = 0.05?

*Options* `.options[]`:

- **A.** about 100
- **B.** about 50  ← key
- **C.** about 30
- **D.** about 42

*Explanation* `.explanation`: Power depends on the alternative through (μ₁−μ₀)√n/σ. For power 0.60 the quantity z_α − (μ₁−μ₀)√n/σ is about −0.253, giving (μ₁−μ₀)/σ ≈ (1.645 + 0.253)/5 = 0.3796. For power 0.85 we need z_α − (μ₁−μ₀)√n/σ = −1.036, i.e. √n ≈ (1.645 + 1.036)/0.3797 = 7.06, so n ≈ 50. The lesson's point stands: power rises with √n, so doubling the sample is nothing like doubling the power.

*Arithmetic check* `.check`: Power scales with √n, not n. Doubling the sample does not double the power, and the closer power gets to 1 the more each extra point costs.

### Q15 — `inf-t9-m-15` *(single, moderate)*

In testing a discrete parameter, a randomised test is used in order to:

*Options* `.options[]`:

- **A.** increase the power beyond the Neyman–Pearson bound
- **B.** make the test unbiased
- **C.** attain a size exactly equal to α when no ordinary critical region does  ← key
- **D.** avoid having to compute the likelihood ratio

*Explanation* `.explanation`: A discrete statistic attains only finitely many tail probabilities, so an exact size of 0.05 is usually unavailable. Rejecting with probability γ on the boundary interpolates between two achievable sizes. It does not change the lemma's bound, and it has nothing to do with unbiasedness.

### Q16 — `inf-t9-m-16` *(order, easy)*

Arrange the steps of applying the Neyman–Pearson lemma in order.

*Steps to order* `.items[]`:

- A. Simplify the ratio into an inequality on a statistic
- B. Compute the power under H₁
- C. Form the likelihood ratio L(θ₁)/L(θ₀)
- D. Fix the constant from P(reject | H₀) = α

*Options* `.options[]`:

- **A.** A, D, C, B
- **B.** C, D, A, B
- **C.** A, C, D, B
- **D.** C, A, D, B  ← key

*Explanation* `.explanation`: Form the ratio first, then simplify it into an inequality on a statistic — that step tells you which statistic and which direction. Only then fix the constant from the size condition under H₀, and compute power under H₁ last, if the question asks for it.

### Q17 — `inf-t9-m-17` *(numeric, moderate)*

X₁,…,X₉ are iid N(μ, 9) with σ² = 9 known. The test rejects H₀: μ = 0 when |x̄| > 1.96. Give the size of this two-sided test.

*Options* `.options[]`:

- **A.** 0.05  ← key
- **B.** 0.025
- **C.** 0.95
- **D.** 0.10

*Explanation* `.explanation`: σ/√n = 3/3 = 1, so x̄ is standard normal under H₀ and P(|X̄| > 1.96) = 2(0.025) = 0.05. The standard error being exactly 1 is what makes 1.96 the familiar number here.

*Arithmetic check* `.check`: A two-sided region takes α/2 in each tail, so the total is 0.05, not 0.025. Option B is one tail only.

### Q18 — `inf-t9-m-18` *(multi, hard)*

Consider what happens when a UMP test does not exist.

*Statements to judge* `.statements[]`:

- **A.** No UMP test exists two-sided because the two one-sided optimal regions are disjoint.
- **B.** The one-sided test is biased against alternatives on the opposite side.
- **C.** Restricting to unbiased tests yields the symmetric two-tailed test for the normal mean.
- **D.** The likelihood ratio test is uniformly most powerful whenever a UMP test fails to exist.

*Options* `.options[]`:

- **A.** B and C only
- **B.** A, B and C only  ← key
- **C.** A and D only
- **D.** A, C and D only

*Explanation* `.explanation`: A is true — the disjointness of the two one-sided regions is the standard argument. B is true: a one-sided test has power below α on the far side, which is exactly what 'biased' means. C is true, and the UMPU test is the two-tailed one. D is false — the likelihood ratio test is always available but is not optimal in general; that is precisely why UMPU is introduced.

*Verdict on each statement* `.verdicts`:

- **A — true.** Uniqueness of each MP test forces a UMP test to equal both disjoint regions at once.
- **B — true.** Its power dips below α for alternatives on the far side — the definition of a biased test.
- **C — true.** Unbiasedness removes both one-sided candidates; the two-tailed test is best among the rest.
- **D — false.** The LRT is a general-purpose fallback with good asymptotics, not an optimality result.

### Q19 — `inf-t9-m-19` *(single, easy)*

'Uniformly' in uniformly most powerful means the test is most powerful:

*Options* `.options[]`:

- **A.** for every sample size
- **B.** at every significance level α
- **C.** at every value in the alternative, simultaneously  ← key
- **D.** for every family of distributions

*Explanation* `.explanation`: The word quantifies over the alternative. A most powerful test is best against one specified alternative; a uniformly most powerful test is best against all of them at once, which is a far stronger demand and is why such tests often fail to exist.

### Q20 — `inf-t9-m-20` *(numeric, hard)*

A one-parameter family has MLR in T. For testing H₀: θ ≤ θ₀ against H₁: θ > θ₀ at level α, the size of the Karlin–Rubin test is computed at:

*Options* `.options[]`:

- **A.** θ = θ₁, a value in the alternative
- **B.** the value of θ minimising the power
- **C.** any θ in the null, since the size is the same throughout
- **D.** θ = θ₀, the boundary of the null  ← key

*Explanation* `.explanation`: For a composite null the size is the supremum of the rejection probability over the whole null. Under MLR the power function is non-decreasing in θ, so that supremum is attained at the boundary θ₀ — which is why the condition is written P(T > c | θ₀) = α. Option C is false precisely because the power function varies across the null.

*Arithmetic check* `.check`: A composite null takes its size from its worst case. Evaluating anywhere inside the null understates the true Type I error rate.

---

## Authoring and verification record `provenance`

Reproduced verbatim. It records what changed in each version and how each derivation was checked, including the findings of the two previous review rounds and the reasons some of their recommendations were declined.

> Review pass, October 2026: 5 per-scene quick checks added on theory, worked and explore scenes from a third-party module review, each read for correctness before import; a further set offered for completion and guided scenes was declined, since those scenes already end with the learner writing an answer. Theory, worked examples and practice authored for this platform against the UGC NET Statistics syllabus. Previous-year questions are stored separately and carry their exam cycle.

