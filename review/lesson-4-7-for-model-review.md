# Lesson 4.7 — Bayesian Estimation and Conjugate Priors

Complete authored content of one lesson from a UGC-NET Statistics (Code 107) preparation application, extracted from the application's own content files.

| | |
|---|---|
| Content version | 1.1 |
| Scenes | 14 |
| Core scenes | 14 |
| Optional JRF-extension scenes | 0 |
| Estimated learner time | 93 minutes |
| Mastery pool | 20 items |
| Position in the app | Statistical Inference → Estimation → Bayesian estimation and conjugate priors |
| Engine | Estimation and inference — prior and likelihood pooled, and the loss that picks a number |
| Pool label | Bayesian Estimation and Conjugate Priors — mastery test (unseen) |
| Unit | IV — Statistical Inference |
| Audience | JRF-target candidates, many returning after several years away |

## Before you start: where this lesson sits

This lesson is at content version **1.1**. The application's current authoring standard is 4.1, and three of its requirements are **known** to be unmet here, so please do not spend effort reporting them — they are scheduled work, not findings:

- no short "how to use this lesson" note on the overview;
- a quick check on only some teaching scenes rather than all of them;
- no family-to-statistic style reference table where one would help.

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

1. Write a posterior as proportional to prior times likelihood and recognise the resulting kernel.

2. State and apply the Beta–Binomial, Gamma–Poisson, Gamma–Exponential and Normal–Normal conjugate updates.

3. Express a posterior mean as a weighted average of the prior mean and the MLE, and give the weight.

4. Give the Bayes estimator under squared-error, absolute-error and 0–1 loss, and say when they differ.

5. Construct a credible interval and distinguish its interpretation from that of a confidence interval.

6. State Jeffreys' prior, compute it for a Bernoulli probability, and say what an improper prior requires.

**Assumed prior knowledge** `prereq[]`

- `prereq[0]` **Bayes' theorem for a parameter** — The whole topic is one application of it, with the normalising constant dropped.
- `prereq[1]` **The Beta and Gamma densities, with means and modes** — These are the kernels that have to be recognised on sight, and the mode exists only under conditions.
- `prereq[2]` **Likelihoods for the Bernoulli and the Poisson** — Conjugacy is visible only once the likelihood is stripped to what involves the parameter.
- `prereq[3]` **Loss functions and expected loss** — The posterior is the answer; a single number requires a loss, and the three standard losses give three different summaries.

**Misconceptions the lesson is built to pre-empt** `traps[]`

- Gamma–Poisson adds Σx to the shape; Gamma–Exponential adds n to the shape. They are reversed.

- A uniform prior equates the posterior MODE with the MLE, not the posterior mean.

- Jeffreys' prior for a Bernoulli probability is Beta(½, ½), not the uniform prior.

- Precisions add in the Normal–Normal update; variances do not.

- The second Beta parameter takes the failures, n − x, not n.

- A credible interval is a probability statement about θ; a confidence interval is not.

- Mean, median and mode of a posterior differ unless it is symmetric, and the loss decides which to report.

- 'The Bayes estimator' is undefined until a loss function is named.

**Assessment policy** `mastery`

- 10 items drawn per attempt from a pool of 20, mix 3 easy, 5 moderate, 2 hard
- pass mark 80%, no hints during the test, retest after 7 days
- `mastery.note`: Platform settings, not an NTA rule. Ten drawn from a pool of twenty at 3 easy / 5 moderate / 2 hard; a retake draws again, holding the mix and pulling back items previously got wrong.

**Sources** `refs[]`

- `refs[0]` **Bayes estimation** — Berkeley STAT 210A course reader, Bayes risk, Bayes estimators, loss functions and conjugate priors (Graduate course reader, free). Derives the posterior mean as the squared-error Bayes estimator and works the beta-binomial and normal-normal cases in the same order this lesson does, with the exponential-family account of why conjugacy happens.
- `refs[1]` **Mathematical Statistics 18.655 — lecture notes** — MIT OpenCourseWare, Session 3 Bayesian Models; Session 11 Bayes Procedures (Graduate lecture notes (PDF), free). Session 11 is the one to read for how a Bayes procedure relates to admissibility and minimaxity, which is the bridge from this topic into 4.8.
- `refs[2]` **Statistical Inference** — NPTEL / SWAYAM — IIT Delhi, Prof. Niladri Chatterjee, Estimation, including Bayesian estimation (Free video course with assignments, free). Indian and free, at this syllabus's level and notation.
- `refs[3]` **Statistical Inference, 2nd edition** — Casella and Berger, Section 7.2.3 Bayes estimators; Section 7.3.4 loss function optimality (Textbook). Section 7.2.3 gives the conjugate updates in the form this lesson states them; 7.3.4 is where the three losses are matched to mean, median and mode.
- `refs[4]` **Theory of Point Estimation, 2nd edition** — Lehmann and Casella, Chapter 4, Average risk optimality (Textbook). The definitive treatment of Bayes estimators, including the conditions under which the posterior mean is admissible. Harder than NET requires; the right place to settle a doubt the lesson leaves open.

---

## The lesson, scene by scene

### Scene 1 of 14 — Before the lesson — four things it will assume

`scenes[0]` · id `s0` · type `foundation` (prerequisite check) · 5 minutes

**Purpose** `scenes[0].objective`

Have Bayes' theorem, the standard densities and the idea of a loss function ready, so the conjugate machinery is bookkeeping rather than new mathematics.

**Body** `scenes[0].body[]`

This topic is less new mathematics than it looks. Bayes' theorem you already have; the Beta and Gamma densities you already have; what is new is pointing them at a parameter instead of at data, and noticing that certain prior-likelihood pairs leave the algebra in the same family it started in.

The four checks below are the pieces. If they are solid, every conjugate update in this lesson is a matter of adding two numbers to two numbers.

**Check 1** `scenes[0].items[0]`

- *asks:* State Bayes' theorem in the form used for a parameter, and say which piece is usually not computed.
- *expected answer* `.recall`: π(θ | x) = f(x | θ) π(θ) / ∫ f(x | θ) π(θ) dθ, or simply posterior ∝ likelihood × prior. The denominator — the marginal or prior predictive m(x) — is a constant in θ and is usually left out, because it only normalises.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> The numerator is the whole of the statistical content: the likelihood you already know how to write, multiplied by whatever you were willing to assume before seeing the data. The denominator does not involve θ at all, so it cannot change the SHAPE of the posterior, only its scale.

> That is why the working symbol is ∝ rather than =. You multiply prior by likelihood, recognise the resulting kernel as a standard density, and read off its parameters. The normalising constant comes free with the recognition.

> When the kernel is not recognisable, the integral has to be done or approximated, and that is where computational Bayes begins. The syllabus stays on the conjugate cases, where recognition always works.

**Check 2** `scenes[0].items[1]`

- *asks:* Write the Beta(α, β) and Gamma(α, β) densities, with their means.
- *expected answer* `.recall`: Beta: f(θ) ∝ θ^(α−1)(1 − θ)^(β−1) on (0,1), with mean α/(α+β) and, for α, β > 1, mode (α−1)/(α+β−2). Gamma in the rate parameterisation: f(λ) ∝ λ^(α−1) e^(−βλ) on (0,∞), with mean α/β, variance α/β² and, for α > 1, mode (α−1)/β.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> These two densities are the ones that absorb binomial and Poisson data without changing family, so their kernels have to be instantly recognisable. In each case the kernel is a power of the variable times something simple, and the parameters are read off the exponents.

> Watch the Gamma parameterisation. In the rate form the second parameter multiplies λ in the exponential and the mean is α/β; in the scale form the mean is αβ. Indian textbooks use both, and an exam answer should state which one it is using. This lesson uses the rate form throughout.

> For the Beta, note that mean and mode are different, and that the mode exists only when both parameters exceed 1. Which one you report is not a matter of taste; it is decided by the loss function, as the lesson will show.

**Check 3** `scenes[0].items[2]`

- *asks:* For a Bernoulli and a Poisson sample, write the likelihood as a function of the parameter, keeping only what depends on it.
- *expected answer* `.recall`: Bernoulli: L(p) ∝ p^(Σxᵢ) (1 − p)^(n − Σxᵢ). Poisson: L(λ) ∝ λ^(Σxᵢ) e^(−nλ). In both cases the sum of the observations is all the data contribute — it is the sufficient statistic.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Dropping the factors that do not involve the parameter is not laziness; it is the same step as writing the posterior with ∝. The binomial coefficient and the factorials carry no information about p or λ.

> Having stripped them, look at what is left. The Bernoulli likelihood is a power of p times a power of (1 − p) — which is exactly the Beta kernel. The Poisson likelihood is a power of λ times e^(−nλ) — exactly the Gamma kernel in rate form.

> That is the whole explanation of conjugacy. The prior and the likelihood have the same algebraic shape, so multiplying them adds the exponents, and the result is the same shape again with larger parameters.

**Check 4** `scenes[0].items[3]`

- *asks:* What is a loss function, and what are the three standard ones?
- *expected answer* `.recall`: A function L(θ, θ̂) measuring the penalty for estimating θ̂ when the truth is θ. The three standard choices are squared-error loss (θ − θ̂)², absolute-error loss |θ − θ̂|, and 0–1 loss, which charges 1 unless the estimate is exactly right.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> The loss function is not decoration. In the Bayesian framework the estimate is whatever minimises the expected loss computed under the posterior, so changing the loss changes the estimator even though the posterior is unchanged.

> The three results worth memorising: squared error gives the posterior MEAN, absolute error gives the posterior MEDIAN, and 0–1 loss gives the posterior MODE. Nothing else in this topic is as reliably examined.

> This is also where decision theory, which is the next topic, joins on. Risk is expected loss averaged over the data; Bayes risk averages it over the prior as well. The vocabulary is shared and the exam moves between them freely.

---

### Scene 2 of 14 — A prior is a sample you have already seen

`scenes[1]` · id `s1` · type `intuition` (intuition) · 5 minutes

**Purpose** `scenes[1].objective`

Read the conjugate update as pooling two batches of evidence, which makes every formula in the topic predictable.

**Body** `scenes[1].body[]`

The formal statement of Bayesian estimation is about degrees of belief. The useful mental picture is more concrete: a conjugate prior is a record of data you are pretending to have already collected.

Take a Beta(α, β) prior for a probability. Its kernel is θ^(α−1)(1 − θ)^(β−1), which is the likelihood of α − 1 successes and β − 1 failures. So Beta(3, 7) carries the same information as a previous sample of 2 successes and 6 failures — eight observations' worth of opinion. Beta(1, 1), the uniform prior, carries zero successes and zero failures: no opinion at all.

Now the update needs no derivation. Observe x successes in n trials and you simply pool the two batches: the posterior is Beta(α + x, β + n − x). The posterior mean, (α + x)/(α + β + n), is the total successes over the total trials — including the imaginary ones.

Everything else follows from that reading. The posterior mean must lie between the prior mean and the sample proportion, because a pooled average lies between the two averages being pooled. The prior's influence must fade as n grows, because α + β stays fixed while n does not. And the weight on the prior must be (α + β)/(α + β + n) — its share of the total sample. That formula is not something to memorise; it is a count.

The same reading works for every conjugate pair in the syllabus. In the Gamma–Poisson case, Gamma(α, β) behaves like α events observed in β units of exposure, and the update adds Σxᵢ events and n units. In the Normal–Normal case, what gets added is precision rather than counts, but the structure is identical.

**Aside — The sentence to carry into the exam** `scenes[1].aside.body`

A conjugate prior is a pretend sample; the update pools it with the real one; the posterior mean is a weighted average with weight equal to the pretend sample's share of the total.

**Quick check before moving on** `scenes[1].ask`

- *question:* If the posterior mean is always between the prior mean and the MLE, can a Bayes estimator ever be better than the MLE at every value of the parameter?
- *hint on request:* Think about what happens at a parameter value far from the prior mean, and whether 'better' has been defined yet.

**Optional deep-dive, opened on demand — Where the prior comes from, and why it is not cheating** `scenes[1].scenario`

*teaser on the closed card:* Two statisticians, the same data, different answers — and both are right.

> A quality inspector tests 10 items from a new supplier and finds 7 acceptable. A frequentist reports p̂ = 0.7. A Bayesian with a Beta(2, 3) prior reports 0.6. A second Bayesian, who has worked with this supplier's industry for years and uses Beta(20, 30), reports 0.54. The data are identical.

> The objection writes itself: the answer depends on who is answering. The reply is that the dependence is explicit and quantified, which is the opposite of a defect. The first Bayesian has declared five observations' worth of prior opinion; the second has declared fifty. Both have published the weight their opinion carries — (α + β)/(α + β + n), which is 1/3 and 5/6 respectively — and both answers converge to the data as n grows. The frequentist has declared no opinion, which is itself the choice Beta(1, 1) makes, and one that nobody would defend as sensible if the supplier were known to be reputable.

> There are three defensible routes to a prior, and an exam answer should be able to name them. An informative prior encodes real previous evidence, which is what the second Bayesian is doing. A weakly informative prior deliberately carries little weight, so the data dominate but the estimate stays away from impossible values. And a non-informative or reference prior tries to let the data speak entirely — of which Jeffreys' prior, proportional to √I(θ), is the principled version, giving Beta(½, ½) for a Bernoulli probability.

> Note what the three Bayesians agree on. For the conjugate families in this scene the posterior mean lies between the prior mean and the MLE, because it is a weighted average of the two; and the prior washes out as n grows, provided it puts positive density near the true value — a prior whose support excludes the truth never does. And every one of them can state exactly how much their prior contributed. The disagreement is a declared parameter of the analysis, not a hidden one.

> For the exam, the examinable content of all this is small and specific: posterior ∝ prior × likelihood, the posterior mean as a weighted average, the weight formula, and Jeffreys' prior as √I(θ). The philosophy is context, not content.

*closing line:* A Bayesian answer carries its assumptions in its arithmetic, where they can be inspected and, as n grows, watched to stop mattering.

---

### Scene 3 of 14 — Watch a prior meet a sample

`scenes[2]` · id `s2` · type `explore` (interactive visualisation) · 6 minutes

**Purpose** `scenes[2].objective`

See the posterior sit between the prior mean and the MLE, and the prior's weight fall as n grows.

**Body** `scenes[2].body[]`

Three curves: the Beta prior in teal, the rescaled binomial likelihood dotted in ochre, and the Beta posterior as the solid line. The three vertical marks are the prior mean, the MLE and the posterior mean.

Start as it opens — Beta(2, 2) with 7 successes in 10. The posterior mean sits strictly between the other two marks, and the readout gives the weight on the prior as 0.286. Now raise n, keeping the proportion roughly fixed: take n to 20 with x near 14, then n to 40 with x near 28. The posterior mark slides towards the MLE and the weight falls. That is the prior washing out, and the readout quantifies it.

Next, set α = β = 1. The prior is flat, and the readout reports that the posterior MODE equals the MLE exactly. This is the precise sense in which a uniform prior recovers maximum likelihood — the mode, not the mean, and the distinction matters because the posterior mean of Beta(1 + x, 1 + n − x) is (x + 1)/(n + 2), which is Laplace's rule of succession, not x/n.

Finally push the prior hard: α = 20, β = 20 with n = 10. The weight on the prior goes above 0.8 and the posterior barely moves off 0.5 whatever the data do. A strong prior is not a neutral choice, and the readout makes the strength visible as a number rather than leaving it as a matter of opinion.

**Interactive element** `scenes[2].viz` — live plot of type `beta-posterior`, initial state a=2, b=2, n=10, x=7. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[2].ask`

- *question:* With α = β = 1 and n = 10, x = 7, the posterior mode is 0.7 but the posterior mean is 8/12 = 0.667. Which would you report, and on what grounds?
- *hint on request:* The grounds are not statistical taste. Ask what you are being penalised for getting wrong.

---

### Scene 4 of 14 — The conjugate pairs, and the update rule for each

`scenes[3]` · id `s3` · type `theory` (theory) · 9 minutes

**Purpose** `scenes[3].objective`

Carry the five pairs in the syllabus with their updates, and derive any one of them on demand.

**Block 1 — What conjugacy means** `scenes[3].blocks[0]` *(type `def`)*

A family of priors is conjugate to a likelihood if the posterior stays in that family for every possible sample. It is a property of the PAIR, not of the prior alone: Beta is conjugate to the binomial and not to anything else in this syllabus. Conjugacy buys two things — the posterior is available in closed form, and its parameters are a simple function of the prior's parameters and the sufficient statistic.

**Block 2 — Beta–Binomial** `scenes[3].blocks[1]` *(type `formula`)*

Prior θ ~ Beta(α, β); data x successes in n Bernoulli trials. Posterior θ | x ~ Beta(α + x, β + n − x). Posterior mean (α + x)/(α + β + n); posterior mode (α + x − 1)/(α + β + n − 2) when both exceed 1. The sufficient statistic is x, and nothing else about the sample enters.

**Block 3 — Gamma–Poisson** `scenes[3].blocks[2]` *(type `formula`)*

Prior λ ~ Gamma(α, β) in the rate parameterisation; data x₁,…,xₙ iid Poisson(λ). Posterior λ | x ~ Gamma(α + Σxᵢ, β + n). Posterior mean (α + Σxᵢ)/(β + n). Read α as prior events and β as prior exposure, and the update is pooling again.

**Block 4 — Gamma–Exponential** `scenes[3].blocks[3]` *(type `formula`)*

Prior λ ~ Gamma(α, β); data x₁,…,xₙ iid Exponential(λ) with rate λ. Posterior λ | x ~ Gamma(α + n, β + Σxᵢ). Note which slot each piece lands in: here the COUNT adds to the shape and the TOTAL TIME adds to the rate, the reverse of the Poisson case. Getting these two the wrong way round is the single commonest error in the topic.

**Block 5 — Normal–Normal, variance known** `scenes[3].blocks[4]` *(type `formula`)*

Prior μ ~ N(μ₀, τ²); data x̄ from n observations with known variance σ². Precisions add: 1/σₙ² = 1/τ² + n/σ². And the posterior mean is the precision-weighted average μₙ = (μ₀/τ² + n x̄/σ²) / (1/τ² + n/σ²). Posterior μ | x ~ N(μₙ, σₙ²). The structure is the same weighted average as before, with precision in place of counts.

**Block 6 — The other two the syllabus may name** `scenes[3].blocks[5]` *(type `def`)*

Inverse-Gamma is conjugate to the normal VARIANCE with the mean known, and Dirichlet is conjugate to the multinomial — the multi-category generalisation of Beta–Binomial, updating Dirichlet(α₁,…,α_k) to Dirichlet(α₁ + n₁,…,α_k + n_k). Both are worth recognising by name even if the algebra is not asked.

**Block 7 — How to derive any of them in two lines** `scenes[3].blocks[6]` *(type `step`)*

Write the prior kernel and the likelihood kernel, keeping only what involves the parameter. Multiply, which adds exponents. Recognise the result. For Gamma–Poisson: λ^(α−1)e^(−βλ) × λ^(Σx)e^(−nλ) = λ^(α+Σx−1)e^(−(β+n)λ), which is the Gamma(α + Σx, β + n) kernel. There is no integration anywhere in that, which is the point of the whole device.

**Block 8 — Which summary of the posterior to report** `scenes[3].blocks[7]` *(type `trap`)*

The posterior is the answer; a single number is a decision. Squared-error loss gives the posterior MEAN, absolute-error loss the posterior MEDIAN, and 0–1 loss the posterior MODE. For a symmetric posterior all three coincide, which is why the Normal–Normal case hides the distinction; for a skewed Beta or Gamma posterior they are three different numbers and the question has to say which loss applies.

**Flow diagram** `scenes[3].flow` — One procedure, five pairs: what gets added to what

- row 1: Prior kernel in θ  |  Likelihood kernel in θ
- row 2: Multiply — exponents add; no integration
- row 3: Beta(α+x, β+n−x)  |  Gamma(α+Σx, β+n)  |  Gamma(α+n, β+Σx)  |  N: precisions add
- row 4: Summarise by the loss: mean · median · mode
- arrows: Prior kernel in θ → Multiply — exponents add; no integration; Likelihood kernel in θ → Multiply — exponents add; no integration; Multiply — exponents add; no integration → Beta(α+x, β+n−x); Multiply — exponents add; no integration → Gamma(α+Σx, β+n); Multiply — exponents add; no integration → Gamma(α+n, β+Σx); Multiply — exponents add; no integration → N: precisions add; Beta(α+x, β+n−x) → Summarise by the loss: mean · median · mode; Gamma(α+Σx, β+n) → Summarise by the loss: mean · median · mode; Gamma(α+n, β+Σx) → Summarise by the loss: mean · median · mode; N: precisions add → Summarise by the loss: mean · median · mode

**Quick check before moving on** `scenes[3].ask`

- *question:* For a Beta prior and binomial data, which two counts update the prior parameters, and why?
- *hint on request:* The posterior adds observed successes to α and observed failures to β; the likelihood contributes those counts.

---

### Scene 5 of 14 — Worked in full — a Beta prior and a binomial sample

`scenes[4]` · id `s4` · type `worked` (worked example) · 7 minutes

**Purpose** `scenes[4].objective`

Produce the posterior, its three summaries, and the weighted-average decomposition, in one pass.

**Problem put to the learner** `scenes[4].problem`

A prior for a success probability θ is Beta(2, 3). In n = 10 independent trials, x = 7 successes are observed. Find the posterior; give the Bayes estimate under squared-error loss and under 0–1 loss; and express the first as a weighted average of the prior mean and the MLE.

**Worked steps** `scenes[4].steps[]`

1. `scenes[4].steps[0]` Write the two kernels, dropping everything free of θ.

   ```
   prior ∝ θ^(2−1)(1−θ)^(3−1) = θ(1−θ)²;   likelihood ∝ θ⁷(1−θ)³
   ```

   Laid out:

   $$prior ∝ θ^{2−1}(1−θ)^{3−1} = θ(1−θ)²;   likelihood ∝ θ⁷(1−θ)³$$

   *why* `.why`: The binomial coefficient C(10,7) does not involve θ, so it cannot affect the posterior's shape and is discarded at the start rather than carried and cancelled later.

2. `scenes[4].steps[1]` Multiply; the exponents add.

   ```
   posterior ∝ θ^(1+7)(1−θ)^(2+3) = θ⁸(1−θ)⁵
   ```

   Laid out:

   $$posterior ∝ θ^{1+7}(1−θ)^{2+3} = θ⁸(1−θ)⁵$$

   *why* `.why`: This is the whole of the computation. No integral is done, because the result is about to be recognised.

3. `scenes[4].steps[2]` Recognise the kernel and read off the parameters.

   ```
   θ^(A−1)(1−θ)^(B−1) with A − 1 = 8, B − 1 = 5  ⟹  posterior = Beta(9, 6)
   ```

   Laid out:

   $$θ^{A−1}(1−θ)^{B−1} with A − 1 = 8, B − 1 = 5  ⟹  posterior = Beta(9, 6)$$

   *why* `.why`: Check against the rule: Beta(α + x, β + n − x) = Beta(2 + 7, 3 + 10 − 7) = Beta(9, 6). ✓ Deriving it and quoting the rule should always agree; if they do not, the exponents were mismatched by one.

4. `scenes[4].steps[3]` Squared-error loss wants the posterior mean.

   ```
   E[θ | x] = A/(A+B) = 9/15 = 0.6
   ```

   Laid out:

   $$E[θ | x] = \frac{A}{(A+B)} = \frac{9}{15} = 0.6$$

   *why* `.why`: Compare the MLE of 0.7 and the prior mean of 2/5 = 0.4. The posterior mean lies strictly between them, as a pooled average must.

5. `scenes[4].steps[4]` 0–1 loss wants the posterior mode.

   ```
   mode = (A−1)/(A+B−2) = 8/13 = 0.6154
   ```

   Laid out:

   $$mode = \frac{(A−1)}{(A+B−2)} = \frac{8}{13} = 0.6154$$

   *why* `.why`: Both parameters exceed 1, so the mode exists and is interior. It is above the mean here because Beta(9, 6) is left-skewed — for a Beta with A > B the mode sits to the right of the mean.

6. `scenes[4].steps[5]` Decompose the mean as a weighted average.

   ```
   w = (α+β)/(α+β+n) = 5/15 = 1/3;   0.6 = (1/3)(0.4) + (2/3)(0.7)
   ```

   Laid out:

   $$w = \frac{(α+β)}{(α+β+n)} = \frac{5}{15} = \frac{1}{3};   0.6 = \frac{1}{3}(0.4) + \frac{2}{3}(0.7)$$

   *why* `.why`: Exactly 0.6, with no rounding. The prior carried five observations' worth of opinion against ten real observations, so it gets one third of the weight — and that is a count, not a formula to memorise.

7. `scenes[4].steps[6]` State what would change with more data.

   ```
   n = 100, x = 70  ⟹  Beta(72, 33), mean 0.6857, w = 5/105 = 0.0476
   ```

   Laid out:

   $$n = 100, x = 70  ⟹  Beta(72, 33), mean 0.6857, w = \frac{5}{105} = 0.0476$$

   *why* `.why`: Same prior, same proportion, ten times the data: the posterior mean has moved from 0.600 to 0.686, closing most of the gap to 0.7. This is consistency of the Bayes estimator, visible in two lines of arithmetic.

**What to take from it** `scenes[4].after`

Four numbers worth carrying from this: posterior Beta(9, 6), mean 0.6, mode 0.6154, prior weight 1/3. And one habit: always check the derived posterior against the standard update rule, because they must agree.

**Quick check before moving on** `scenes[4].ask`

- *question:* With a Beta(α, β) prior and x successes in n trials, write the posterior distribution and its mean.
- *hint on request:* Combine the prior kernel with p^x(1−p)^(n−x), then identify the updated Beta parameters.

---

### Scene 6 of 14 — Pause and recall

`scenes[5]` · id `s5` · type `recall` (retrieval practice) · 3 minutes

**Purpose** `scenes[5].objective`

Retrieve the five updates and the three loss results before the harder material.

**Intro** `scenes[5].intro`

Answer aloud, then look. Everything here was in the last two scenes.

- `scenes[5].items[0]` **Q:** Give the Beta–Binomial update and the posterior mean.  
  **A:** Beta(α, β) with x successes in n trials gives Beta(α + x, β + n − x), posterior mean (α + x)/(α + β + n).
- `scenes[5].items[1]` **Q:** Give the Gamma–Poisson and the Gamma–Exponential updates, and say how they differ.  
  **A:** Poisson: Gamma(α + Σxᵢ, β + n) — the total of the counts adds to the shape and the sample size to the rate. Exponential: Gamma(α + n, β + Σxᵢ) — the sample size adds to the shape and the total time to the rate. They are the reverse of each other.
- `scenes[5].items[2]` **Q:** In the Normal–Normal case with known variance, what adds?  
  **A:** Precisions: 1/σₙ² = 1/τ² + n/σ², and the posterior mean is the precision-weighted average of μ₀ and x̄.
- `scenes[5].items[3]` **Q:** Which posterior summary does each of the three standard losses give?  
  **A:** Squared error → posterior mean. Absolute error → posterior median. 0–1 loss → posterior mode.
- `scenes[5].items[4]` **Q:** What weight does the posterior mean place on the prior mean in the Beta–Binomial case?  
  **A:** (α + β)/(α + β + n) — the prior's share of the pooled sample size.
- `scenes[5].items[5]` **Q:** What is Jeffreys' prior, and what is it for a Bernoulli probability?  
  **A:** π(θ) ∝ √I(θ). For a Bernoulli, I(p) = 1/(p(1−p)), so Jeffreys' prior is ∝ p^(−½)(1−p)^(−½), the Beta(½, ½) kernel.

---

### Scene 7 of 14 — Your turn, with the scaffolding removed — four updates

`scenes[6]` · id `s6` · type `completion` (fill in the blanks) · 7 minutes

**Purpose** `scenes[6].objective`

Produce each conjugate update and summary without being shown the pattern first.

**Problem put to the learner** `scenes[6].problem`

Fill in each blank. The arithmetic is small; what is being tested is which quantity lands in which slot.

**Worked steps** `scenes[6].steps[]`

1. `scenes[6].steps[0]` A Beta(4, 6) prior meets 12 successes in 20 trials.

   - *learner is asked:* The posterior, and its mean?
   - *accepted answer* `.blank.answer`: Beta(16, 14), mean 16/30 = 0.5333
   - *also accepted:* Beta(16,14), 0.5333; Beta(16, 14) mean 0.533; Beta(16,14) and 8/15; Beta(16,14), mean = 0.5333; Beta(16,14) mean 16/30
   - *hint:* Add x to the first parameter and n − x to the second.

   *why* `.why`: The base case. Everything else in this topic is this step with different letters.

2. `scenes[6].steps[1]` A Gamma(3, 2) prior, rate form, meets a Poisson sample with Σxᵢ = 14 from n = 7.

   - *learner is asked:* The posterior?
   - *accepted answer* `.blank.answer`: Gamma(17, 9)
   - *also accepted:* Gamma(17,9); Gamma (17, 9); Gamma(17, 9) rate form; gamma 17 9
   - *hint:* The total of the counts goes to the shape; the sample size goes to the rate.

   *why* `.why`: Poisson is the case where the SUM adds to the shape — the opposite of the exponential.

3. `scenes[6].steps[2]` A Gamma(3, 2) prior meets an exponential sample with n = 7 and Σxᵢ = 14.

   - *learner is asked:* The posterior?
   - *accepted answer* `.blank.answer`: Gamma(10, 16)
   - *also accepted:* Gamma(10,16); Gamma (10, 16); Gamma(10, 16) rate form; gamma 10 16
   - *hint:* Here the sample SIZE goes to the shape and the total time to the rate — the reverse of the Poisson case.

   *why* `.why`: Same prior and same two numbers as the previous blank, and a different answer. This pair is the most productive confusion in the topic, which is why they appear back to back.

4. `scenes[6].steps[3]` A prior μ ~ N(50, 16) meets n = 4 observations with known σ² = 8 and x̄ = 56.

   - *learner is asked:* The posterior variance and mean?
   - *accepted answer* `.blank.answer`: variance 8/3 = 2.667, mean 55
   - *also accepted:* 2.667 and 55; variance 2.6667, mean 55; 8/3 and 55; var = 2.667, mean = 55; posterior variance 2.667 posterior mean 55
   - *hint:* Precisions add: 1/16 + 4/8. Then take the precision-weighted average of 50 and 56.

   *why* `.why`: The arithmetic: 1/16 + 1/2 = 9/16, so the variance is 16/9… but check it against the weighted mean, because one of the two is easier to get wrong than the other.

5. `scenes[6].steps[4]` The posterior from the first blank is Beta(16, 14), which is close to symmetric but not exactly so.

   - *learner is asked:* Under 0–1 loss, what is the estimate?
   - *accepted answer* `.blank.answer`: the posterior mode, 15/28 = 0.5357
   - *also accepted:* posterior mode 0.5357; mode = 15/28; the mode, 0.5357; posterior mode, 15/28; mode 15/28 = 0.536
   - *hint:* (A − 1)/(A + B − 2), with A = 16 and B = 14.

   *why* `.why`: Mean 0.5333 against mode 0.5357: close, but not the same number. A question that specifies the loss is specifying which of these it wants.

**What to take from it** `scenes[6].after`

If the second and third blanks came out the same, go back to them: that is the error the exam is built to catch. Poisson sends the sum to the shape; the exponential sends the count to the shape.

---

### Scene 8 of 14 — Credible intervals, Jeffreys priors, and what can go wrong

`scenes[7]` · id `s7` · type `theory` (theory) · 8 minutes

**Purpose** `scenes[7].objective`

Separate a credible interval from a confidence interval, and know what an improper prior is for.

**Block 1 — Credible intervals** `scenes[7].blocks[0]` *(type `def`)*

A 95% credible interval is any set C with ∫_C π(θ | x) dθ = 0.95. The equal-tailed version cuts 2.5% from each tail of the posterior; the highest posterior density, or HPD, interval is the shortest such set, and contains every θ with posterior density above some threshold. For a symmetric unimodal posterior the two coincide; for a skewed one the HPD is strictly shorter, which is why it is preferred when it can be found.

**Block 2 — Credible against confidence — the distinction that is actually examined** `scenes[7].blocks[1]` *(type `trap`)*

A credible interval is a probability statement about θ given the data: P(θ ∈ C | x) = 0.95. A confidence interval is a probability statement about the PROCEDURE over repeated samples: 95% of such intervals would contain the fixed θ. The Bayesian statement is the one people wrongly make about confidence intervals, and the exam tests exactly that slip. They are numerically close in large samples with a weak prior, and they mean different things in every sample.

**Block 3 — Jeffreys' prior** `scenes[7].blocks[2]` *(type `formula`)*

π(θ) ∝ √I(θ), where I(θ) is the Fisher information. Its merit is invariance: the same rule applied after reparameterising gives the prior you would get by transforming the original, which no flat prior does. For a Bernoulli probability, I(p) = 1/(p(1−p)), so Jeffreys' prior is ∝ p^(−½)(1−p)^(−½), the Beta(½, ½) kernel — which puts MORE mass near 0 and 1 than the uniform prior, not less.

**Block 4 — Improper priors** `scenes[7].blocks[3]` *(type `def`)*

A prior that does not integrate to a finite value — π(μ) ∝ 1 on the whole real line, or π(σ) ∝ 1/σ on the positive half-line, which is Jeffreys' prior for a scale parameter. These are not probability distributions, and they are used anyway, because the posterior they produce is often perfectly proper. The obligation they create is to CHECK that properness; an improper prior with too little data can give an improper posterior, and then there is no answer at all.

**Block 5 — Why a flat prior is not neutral** `scenes[7].blocks[4]` *(type `step`)*

A uniform prior on θ is not uniform on θ² or on log θ, so 'no information' expressed as flatness depends on the parameterisation chosen — which is information. This is the whole motivation for Jeffreys' rule. A second point: a uniform prior on a probability is Beta(1, 1), which behaves like one success and one failure already observed, so even the flat prior is a pretend sample of size two. Laplace's rule of succession, (x + 1)/(n + 2), is exactly that prior's posterior mean.

**Block 6 — Predictive distributions** `scenes[7].blocks[5]` *(type `formula`)*

The prior predictive m(x) = ∫ f(x | θ) π(θ) dθ is the denominator of Bayes' theorem, and is used to compare models. The posterior predictive, ∫ f(x_new | θ) π(θ | x) dθ, is what a Bayesian uses to forecast a new observation — it averages the sampling distribution over the posterior rather than plugging in a point estimate, and is therefore wider than the plug-in version. For Beta–Binomial the prior predictive is the beta-binomial distribution, which is the name worth recognising.

**Block 7 — Three things that look like results and are not** `scenes[7].blocks[6]` *(type `trap`)*

First, the posterior mean is not always between the prior mean and the MLE for non-conjugate problems; the weighted-average reading is a property of these particular families. Second, a Bayes estimator is generally BIASED in the frequentist sense, and that is not a criticism of it — it is optimising a different criterion. Third, 'the Bayes estimator' is not well defined until the loss is stated, so a question asking for it without naming a loss is asking for the posterior mean by convention.

**Quick check before moving on** `scenes[7].ask`

- *question:* What is the difference between a credible interval and a frequentist confidence interval?
- *hint on request:* A credible interval assigns posterior probability to the parameter conditional on data; a confidence procedure has repeated-sampling coverage.

---

### Scene 9 of 14 — A flat prior, a sharp prior, and what each costs

`scenes[8]` · id `s8` · type `explore` (interactive visualisation) · 6 minutes

**Purpose** `scenes[8].objective`

See that no prior is neutral, and watch the posterior mode and mean separate on a skewed posterior.

**Body** `scenes[8].body[]`

It opens on the uniform prior, Beta(1, 1), with 9 successes in 10. The readout confirms that the posterior mode is exactly 0.9, the MLE — a flat prior recovers maximum likelihood at the mode. But the posterior MEAN is 10/12 = 0.8333, which is Laplace's rule of succession. Two defensible answers from one posterior, separated only by the loss function.

Now set α = β = 0.5, which is Jeffreys' prior for this problem. Notice something counter-intuitive: the prior puts more mass at the ends than the uniform did, so with 9 of 10 successes the posterior mean moves UP, to about 0.864, rather than being dragged towards 0.5. A non-informative prior is not the same thing as a prior that pulls towards the middle, and the readout is the quickest way to see it.

Next, test the extreme. Set x = 10, n = 10 — ten successes out of ten. The MLE is 1.0, which asserts that failure is impossible on the strength of ten trials. With Beta(1, 1) the posterior mean is 11/12 = 0.917, and with Jeffreys it is about 0.955. Neither is 1. Keeping the estimate off the boundary with no real prior information is the practical argument for a weakly informative prior, and here it is a one-line calculation.

Finally make the prior dominate: α = 15, β = 15 with n = 10. The weight on the prior exceeds 0.75 and the posterior sits near 0.57 however strong the data. Compare that with the same prior at n = 200: the weight falls below 0.14. The prior has not changed; only its share of the pooled evidence has.

**Interactive element** `scenes[8].viz` — live plot of type `beta-posterior`, initial state a=1, b=1, n=10, x=9. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[8].ask`

- *question:* With 10 successes in 10 trials, the MLE is 1.0 and every Bayes estimate is strictly below it. Is the MLE wrong here, or is the criticism of it something other than wrongness?
- *hint on request:* Ask what the MLE is optimising, and whether 'the value that makes the data most likely' was ever meant to be a statement about the next trial.

---

### Scene 10 of 14 — Now without the steps — a normal mean with a normal prior

`scenes[9]` · id `s9` · type `guided` (guided problem) · 8 minutes

**Purpose** `scenes[9].objective`

Run the precision-weighted update and produce a credible interval unaided.

**Problem put to the learner** `scenes[9].problem`

A measurement process has known variance σ² = 36. Prior belief about its mean is μ ~ N(100, 25). A sample of n = 9 gives x̄ = 112. Find the posterior distribution of μ, give the Bayes estimate under squared-error loss, and construct a 95% equal-tailed credible interval.

**Hint ladder, revealed one at a time** `scenes[9].hints[]`

1. Work in precisions, not variances: the reciprocals are what add.
2. The posterior mean is the precision-weighted average of the prior mean and the sample mean — check it lies between 100 and 112.
3. For the interval, the posterior is normal, so the equal-tailed and HPD intervals coincide and 1.96 posterior standard deviations each way is correct.

**Model solution, hidden until requested** `scenes[9].solution[]`

1. `scenes[9].solution[0]` Write the two precisions.

   ```
   prior precision = 1/τ² = 1/25 = 0.04;   data precision = n/σ² = 9/36 = 0.25
   ```

   Laid out:

   $$prior precision = \frac{1}{τ²} = \frac{1}{25} = 0.04;   data precision = \frac{n}{σ²} = \frac{9}{36} = 0.25$$

2. `scenes[9].solution[1]` Add them for the posterior precision, then invert for the variance.

   ```
   1/σₙ² = 0.04 + 0.25 = 0.29  ⟹  σₙ² = 1/0.29 = 3.4483,  σₙ = 1.8570
   ```

   Laid out:

   $$\frac{1}{σₙ²} = 0.04 + 0.25 = 0.29  ⟹  σₙ² = \frac{1}{0}.29 = 3.4483,  σₙ = 1.8570$$

3. `scenes[9].solution[2]` Take the precision-weighted average for the posterior mean.

   ```
   μₙ = (100 × 0.04 + 112 × 0.25)/0.29 = (4 + 28)/0.29 = 32/0.29 = 110.3448
   ```

   Laid out:

   $$μₙ = \frac{(100 × 0.04 + 112 × 0.25)}{0}.29 = \frac{(4 + 28)}{0}.29 = \frac{32}{0}.29 = 110.3448$$

4. `scenes[9].solution[3]` Check it by reading off the weight on the prior.

   ```
   w = 0.04/0.29 = 0.1379;   0.1379 × 100 + 0.8621 × 112 = 110.3448 ✓
   ```

   Laid out:

   $$w = 0.\frac{04}{0}.29 = 0.1379;   0.1379 × 100 + 0.8621 × 112 = 110.3448 ✓$$

5. `scenes[9].solution[4]` State the posterior and the point estimate.

   ```
   μ | x ~ N(110.3448, 3.4483);   squared-error Bayes estimate = 110.3448
   ```

6. `scenes[9].solution[5]` Build the interval from the posterior standard deviation.

   ```
   110.3448 ± 1.96 × 1.8570 = 110.3448 ± 3.6397  ⟹  (106.705, 113.984)
   ```

7. `scenes[9].solution[6]` Note what the interval means, because this is where marks are lost.

   ```
   P(106.705 < μ < 113.984 | x) = 0.95 — a statement about μ, not about the procedure
   ```

**Final answer given to the learner** `scenes[9].answer`

μ | x ~ N(110.345, 3.448), so σₙ = 1.857. The squared-error Bayes estimate is 110.345, and the 95% credible interval is (106.705, 113.984). Because the posterior is normal and symmetric, the mean, median and mode coincide, so all three standard losses give the same point estimate here.

**Self-check offered** `scenes[9].check`

Two checks. The posterior mean must lie between 100 and 112, and 110.345 does. And the posterior variance must be SMALLER than both 25 and σ²/n = 4, because adding information cannot increase uncertainty — 3.448 is below both. If your variance came out above 4, you averaged variances instead of adding precisions.

**Optional deep-dive, opened on demand — Why the frequentist interval here is (108.08, 115.92) and the Bayesian one is narrower** `scenes[9].scenario`

*teaser on the closed card:* The same interval, computed two ways, meaning two different things.

> Take the same numbers and do the frequentist calculation. With σ² = 36 known and n = 9, the standard error is 6/3 = 2, and the 95% confidence interval for μ is 112 ± 1.96 × 2 = (108.08, 115.92). The Bayesian credible interval was (106.705, 113.984). The two differ in centre and in width, and both are correct.

> The centre differs because the prior pulled the estimate down from 112 towards 100, by an amount the weight 0.1379 made explicit. The width differs because the prior contributed information: posterior variance 3.448 is below σ²/n = 4, so the credible interval is shorter — width 7.279 against 7.840. Information from any source narrows an interval, and a prior is a source.

> Now the part that is actually examined. The confidence statement is about the procedure: if this experiment were repeated indefinitely with μ fixed, 95% of the intervals so constructed would contain it. Nothing is being asserted about this particular interval, which either contains μ or does not. The credible statement is about μ: given the prior and these data, there is a 0.95 posterior probability that μ lies in the stated range. Only the second statement is a probability about the parameter, and it is available only because a prior was supplied.

> The exam exploits the fact that most people state the Bayesian interpretation while computing the frequentist interval. If a question gives you a confidence interval and four readings of it, the one that says 'there is a 95% probability that μ lies in this interval' is wrong — and the one that says it about a credible interval is right.

> A last observation worth carrying: as n grows with the prior fixed, the weight on the prior goes to zero, the posterior variance approaches σ²/n, and the two intervals converge. The disagreement is a small-sample phenomenon, which is exactly when a prior is worth having and exactly when it is worth declaring.

*closing line:* Same data, two intervals: one is a statement about the parameter, the other about the method, and only the prior makes the first available.

---

### Scene 11 of 14 — Six statements — verdict on each before you look

`scenes[10]` · id `s10` · type `trapcheck` (true/false check) · 6 minutes

**Purpose** `scenes[10].objective`

Meet the specific errors this topic generates.

**Intro** `scenes[10].intro`

Each is either a standard result or a plausible-looking corruption of one.

- `scenes[10].items[0]` **Claim:** With a Beta(α, β) prior and x successes in n trials, the posterior is Beta(α + x, β + n − x).  
  **Verdict: TRUE.** The exponents add: θ^(α−1)(1−θ)^(β−1) × θ^x(1−θ)^(n−x). Note the second parameter takes n − x, the failures, not n.
- `scenes[10].items[1]` **Claim:** For a Gamma(α, β) prior and an exponential sample, the posterior is Gamma(α + Σxᵢ, β + n).  
  **Verdict: FALSE.** That is the POISSON update. For the exponential it is Gamma(α + n, β + Σxᵢ): the sample size adds to the shape and the total time to the rate. The two are reversed, and this is the most productive trap in the topic.
- `scenes[10].items[2]` **Claim:** A uniform prior on a probability makes the Bayes estimator identical to the MLE.  
  **Verdict: FALSE.** It makes the posterior MODE identical to the MLE. The posterior mean, which is the estimator under squared-error loss, is (x + 1)/(n + 2) — Laplace's rule of succession. The claim is true only if 0–1 loss is specified.
- `scenes[10].items[3]` **Claim:** Under absolute-error loss the Bayes estimator is the posterior median.  
  **Verdict: TRUE.** Squared error gives the mean, absolute error the median, 0–1 loss the mode. For a symmetric posterior all three agree, which is why the normal case does not reveal the distinction.
- `scenes[10].items[4]` **Claim:** Jeffreys' prior for a Bernoulli probability is the uniform prior on (0, 1).  
  **Verdict: FALSE.** Jeffreys' prior is ∝ √I(θ), and I(p) = 1/(p(1−p)), giving ∝ p^(−½)(1−p)^(−½) — the Beta(½, ½) kernel, which puts more mass near 0 and 1 than the uniform does. The uniform is Beta(1, 1), a different prior.
- `scenes[10].items[5]` **Claim:** A 95% credible interval and a 95% confidence interval both say there is a 0.95 probability that the parameter lies in the computed interval.  
  **Verdict: FALSE.** Only the credible interval says that. The confidence statement is about the procedure under repeated sampling — 95% of such intervals would cover the fixed parameter. Making the Bayesian statement about a confidence interval is the single commonest error in inference, and it is examined directly.

---

### Scene 12 of 14 — Transfer — a skewed posterior and a loss that is not squared error

`scenes[11]` · id `s11` · type `guided` (guided problem) · 7 minutes

**Purpose** `scenes[11].objective`

Handle a case where the three posterior summaries differ, and justify the one you report.

**Problem put to the learner** `scenes[11].problem`

Counts of defects per batch are modelled as Poisson(λ). A Gamma(3, 2) prior, rate form, is used. A sample of n = 7 batches gives Σxᵢ = 14. Find the posterior, then give the Bayes estimate under squared-error loss, under 0–1 loss, and under absolute-error loss. Which differs most from the MLE, and why are they not all equal?

**Hint ladder, revealed one at a time** `scenes[11].hints[]`

1. The posterior is a Gamma, and the Poisson update sends the sum of the counts to the shape.
2. Mean and mode of a Gamma(A, B) in rate form are A/B and (A − 1)/B. The median has no closed form, but a standard approximation is (A − 1/3)/B.
3. A Gamma is right-skewed, so order the three summaries before computing them and use that as your check.

**Model solution, hidden until requested** `scenes[11].solution[]`

1. `scenes[11].solution[0]` Apply the Poisson update.

   ```
   posterior = Gamma(α + Σxᵢ, β + n) = Gamma(3 + 14, 2 + 7) = Gamma(17, 9)
   ```

2. `scenes[11].solution[1]` Squared-error loss — the posterior mean.

   ```
   A/B = 17/9 = 1.8889
   ```

   Laid out:

   $$\frac{A}{B} = \frac{17}{9} = 1.8889$$

3. `scenes[11].solution[2]` 0–1 loss — the posterior mode.

   ```
   (A − 1)/B = 16/9 = 1.7778
   ```

   Laid out:

   $$\frac{(A − 1)}{B} = \frac{16}{9} = 1.7778$$

4. `scenes[11].solution[3]` Absolute-error loss — the posterior median, by the standard approximation.

   ```
   (A − 1/3)/B = (17 − 0.3333)/9 = 1.8519   [exact value 1.8520]
   ```

   Laid out:

   $$\frac{(A − \frac{1}{3})}{B} = \frac{(17 − 0.3333)}{9} = 1.8519   [exact value 1.8520]$$

5. `scenes[11].solution[4]` Order them and check against the skew.

   ```
   mode 1.7778 < median 1.8519 < mean 1.8889 — the right-skewed ordering ✓
   ```

6. `scenes[11].solution[5]` Compare with the MLE and decompose the mean.

   ```
   MLE = Σx/n = 14/7 = 2.0;  w = β/(β+n) = 2/9 = 0.2222;  0.2222(1.5) + 0.7778(2.0) = 1.8889 ✓
   ```

   Laid out:

   $$MLE = \frac{Σx}{n} = \frac{14}{7} = 2.0;  w = \frac{β}{(β+n)} = \frac{2}{9} = 0.2222;  0.2222(1.5) + 0.7778(2.0) = 1.8889 ✓$$

7. `scenes[11].solution[6]` Answer the 'why' part.

   ```
   mean − mode = 1/9 = 0.1111, the skew of Gamma(17,9) expressed in the summaries
   ```

   Laid out:

   $$mean − mode = \frac{1}{9} = 0.1111, the skew of Gamma(17,9) expressed in the summaries$$

**Final answer given to the learner** `scenes[11].answer`

Posterior Gamma(17, 9). Squared-error estimate 1.889, 0–1 estimate 1.778, absolute-error estimate 1.852. The mode differs most from the MLE of 2.0. They are not equal because the Gamma posterior is right-skewed, and mean, median and mode coincide only for a symmetric posterior — so the loss function genuinely changes the answer here, unlike in the normal case.

**Self-check offered** `scenes[11].check`

Three checks that catch most errors. All three summaries must lie between the prior mean 1.5 and the MLE 2.0. They must come in the order mode < median < mean for a right-skewed posterior. And the weighted-average decomposition must reproduce the mean exactly — if it does not, the shape and rate were swapped in the update.

---

### Scene 13 of 14 — What you should now be able to do unaided

`scenes[12]` · id `s12` · type `summary` (summary) · 4 minutes

**Purpose** `scenes[12].objective`

Compress the topic to the updates, the loss results and the one distinction that is always examined.

**Body** `scenes[12].body[]`

The mechanism. Posterior ∝ likelihood × prior; the denominator normalises and is dropped. Write both kernels in the parameter, multiply so the exponents add, and recognise the result. No integration is needed in any conjugate case, which is what conjugacy is for.

The five updates. Beta(α, β) with x of n → Beta(α + x, β + n − x). Gamma(α, β) with a Poisson sample → Gamma(α + Σxᵢ, β + n). Gamma(α, β) with an exponential sample → Gamma(α + n, β + Σxᵢ) — the reverse, and the commonest error in the topic. Normal prior with known variance → precisions add, 1/σₙ² = 1/τ² + n/σ², and the mean is the precision-weighted average. Dirichlet with a multinomial sample → add the category counts.

The weighted average. In each case the posterior mean is w × (prior mean) + (1 − w) × (MLE), with w the prior's share of the pooled evidence: (α + β)/(α + β + n) for Beta–Binomial, β/(β + n) for Gamma–Poisson, and the precision share for Normal–Normal. The posterior mean therefore lies between the prior mean and the MLE, and the prior washes out as n grows.

The loss results. Squared error → posterior mean. Absolute error → posterior median. 0–1 loss → posterior mode. For a symmetric posterior all three coincide; for a skewed Beta or Gamma they are three different numbers and the ordering follows the skew. Asked for 'the Bayes estimator' with no loss named, give the posterior mean.

Priors. Jeffreys' prior is ∝ √I(θ), which is invariant to reparameterisation; for a Bernoulli it is Beta(½, ½), not the uniform. A uniform prior on a probability is Beta(1, 1) and behaves like one success and one failure, so its posterior mean is Laplace's (x + 1)/(n + 2). Improper priors do not integrate but may still give proper posteriors, which must be checked.

The distinction. A credible interval is a probability statement about the parameter given the data; a confidence interval is a statement about the procedure over repeated samples. They converge in large samples and mean different things in every sample, and the exam tests this directly.

The habit. Derive the posterior from the kernels, then check it against the standard update rule. The two must agree, and when they do not, the exponents are out by one or the shape and rate have been swapped.

---

### Scene 14 of 14 — Mastery test

`scenes[13]` · id `s13` · type `quiz` (mastery test) · 12 minutes

**Purpose** `scenes[13].objective`

Ten unseen questions, drawn 3 easy / 5 moderate / 2 hard.

Draws from the pool reproduced below. `scenes[13].setId` = `inference_t7_mastery`

---

## Revision material `revision`

**Revision sheet** `revision.sheet[]` (19 lines)

1. `[0]` Posterior ∝ likelihood × prior; the marginal m(x) only normalises and is dropped.
2. `[1]` Beta(α,β) + x of n  →  Beta(α+x, β+n−x); mean (α+x)/(α+β+n); mode (α+x−1)/(α+β+n−2).
3. `[2]` Gamma(α,β) + Poisson (Σx, n)  →  Gamma(α+Σx, β+n); mean (α+Σx)/(β+n).
4. `[3]` Gamma(α,β) + Exponential (n, Σx)  →  Gamma(α+n, β+Σx). THE REVERSE OF POISSON.
5. `[4]` Normal prior N(μ₀,τ²), known σ²: 1/σₙ² = 1/τ² + n/σ²; μₙ = (μ₀/τ² + nx̄/σ²)/(1/τ² + n/σ²).
6. `[5]` Dirichlet(α₁..α_k) + multinomial  →  Dirichlet(α₁+n₁, …, α_k+n_k).
7. `[6]` Inverse-Gamma is conjugate to the normal variance with the mean known.
8. `[7]` Posterior mean = w(prior mean) + (1−w)(MLE); w = (α+β)/(α+β+n), or β/(β+n), or the precision share.
9. `[8]` Squared-error loss → posterior MEAN. Absolute-error → posterior MEDIAN. 0–1 loss → posterior MODE.
10. `[9]` Symmetric posterior: mean = median = mode. Right-skewed Gamma: mode < median < mean.
11. `[10]` Gamma(A,B) rate form: mean A/B, mode (A−1)/B, median ≈ (A−1/3)/B.
12. `[11]` Uniform prior on a probability = Beta(1,1); posterior mean (x+1)/(n+2), Laplace's rule of succession.
13. `[12]` A flat prior makes the posterior MODE equal the MLE, not the posterior mean.
14. `[13]` Jeffreys' prior ∝ √I(θ); for Bernoulli, Beta(½,½) — more mass at the ends than uniform.
15. `[14]` Improper prior: does not integrate (π(μ)∝1, π(σ)∝1/σ). The posterior may still be proper — check it.
16. `[15]` Credible interval: P(θ ∈ C | x) = 0.95, a statement about θ. HPD is the shortest such set.
17. `[16]` Confidence interval: a statement about the procedure under repeated sampling, not about θ.
18. `[17]` A Bayes estimator is generally biased in the frequentist sense; it optimises a different criterion.
19. `[18]` Posterior predictive averages the sampling distribution over the posterior, so it is wider than plug-in.

**Flashcards** `revision.cards[]`

| Front | Back |
|---|---|
| Beta(α,β) prior, x successes in n | Beta(α + x, β + n − x) |
| Gamma prior with a Poisson sample | Gamma(α + Σxᵢ, β + n) — the sum goes to the shape |
| Gamma prior with an exponential sample | Gamma(α + n, β + Σxᵢ) — the count goes to the shape |
| Normal prior, known variance | Precisions add: 1/σₙ² = 1/τ² + n/σ² |
| Weight on the prior mean, Beta–Binomial | (α + β)/(α + β + n) |
| Squared-error loss gives | The posterior mean |
| Absolute-error loss gives | The posterior median |
| 0–1 loss gives | The posterior mode |
| Jeffreys' prior | π(θ) ∝ √I(θ); Beta(½, ½) for a Bernoulli p |
| Uniform prior posterior mean for a probability | (x + 1)/(n + 2) — Laplace's rule of succession |
| Credible versus confidence | Probability about θ versus probability about the procedure |
| Gamma(A,B) rate form: mean, mode, median | A/B, (A−1)/B, ≈ (A−1/3)/B |

**Memory aids** `revision.tricks[]`

- `[0]` **A conjugate prior is a pretend sample** — Beta(α,β) is α−1 successes and β−1 failures already seen. Every update is then pooling, and every weight is a share of a total sample size.
- `[1]` **Poisson sends the sum; the exponential sends the count** — Gamma(α+Σx, β+n) for Poisson; Gamma(α+n, β+Σx) for the exponential. The two are mirror images and the exam puts them side by side.
- `[2]` **Precisions add, variances do not** — In the Normal–Normal case the reciprocals add. If your posterior variance came out larger than either input, you averaged variances.
- `[3]` **Squared, absolute, zero-one: mean, median, mode** — Three losses, three summaries, in that order. It is the most reliably examined fact in the topic.
- `[4]` **Flat gives the mode, not the mean** — A uniform prior makes the posterior mode equal the MLE. Its posterior mean is (x+1)/(n+2).
- `[5]` **Credible is about θ; confidence is about the method** — Only the Bayesian interval licenses a probability statement about the parameter.

**Elimination shortcuts for multiple-choice items** `revision.shortcuts[]`

- `[0]` Check any posterior mean against the prior mean and the MLE: it must lie between them.
- `[1]` Check any posterior variance in the normal case: it must be below both τ² and σ²/n.
- `[2]` For a right-skewed Gamma or Beta posterior, order the summaries mode < median < mean before computing them.
- `[3]` Asked for 'the Bayes estimator' with no loss stated, give the posterior mean.
- `[4]` Any option claiming a flat prior makes the posterior MEAN equal the MLE is wrong.
- `[5]` Any option offering a 0.95 probability statement about θ for a CONFIDENCE interval is wrong.

**If nothing else is remembered** `revision.remember[]`

- `[0]` Derive the posterior from the kernels, then check it against the standard update rule — they must agree.
- `[1]` State the parameterisation when you use a Gamma, because the mean is α/β in rate form and αβ in scale form.

**Errors to avoid** `revision.traps[]`

- `[0]` Swapping the Poisson and exponential updates — the single most productive error in the topic.
- `[1]` Putting n rather than n − x into the second Beta parameter.
- `[2]` Saying a uniform prior makes the Bayes estimator the MLE, without specifying 0–1 loss.
- `[3]` Averaging variances instead of adding precisions in the Normal–Normal case.
- `[4]` Taking Jeffreys' prior for a probability to be the uniform prior.
- `[5]` Reporting a posterior mean when the question states absolute-error or 0–1 loss.
- `[6]` Giving a credible interpretation to a confidence interval, or the reverse.
- `[7]` Treating the bias of a Bayes estimator as evidence that it is wrong.
- `[8]` Assuming mean, median and mode coincide on a skewed posterior because they did in the normal case.

---

## Mastery pool — all 20 items with answer keys `qsets/mastery`

Ten are drawn per attempt at 3 easy / 5 moderate / 2 hard. Keys are distributed five to each option letter. Please check each item for a second defensible answer as well as for the correctness of its stated key and explanation.

### Q1 — `inference-t7-m-01` *(numeric, easy)*

A Beta(2, 3) prior is used for a success probability θ. In 8 independent trials, 5 successes are observed. The posterior distribution is:

*Options* `.options[]`:

- **A.** Beta(7, 6)  ← key
- **B.** Beta(7, 11)
- **C.** Beta(5, 3)
- **D.** Beta(10, 6)

*Explanation* `.explanation`: Beta(α + x, β + n − x) = Beta(2 + 5, 3 + 8 − 5) = Beta(7, 6). The option Beta(7, 11) is what you get by adding n rather than n − x to the second parameter, which is the standard slip; Beta(10, 6) adds n to the first parameter instead of x.

*Arithmetic check* `.check`: First parameter takes the successes, second takes the failures. 2+5 = 7 and 3+3 = 6, and the two parameters must sum to α+β+n = 13.

### Q2 — `inference-t7-m-02` *(single, easy)*

Under squared-error loss, the Bayes estimator of a parameter is:

*Options* `.options[]`:

- **A.** The posterior mode
- **B.** The posterior median
- **C.** The maximum likelihood estimate
- **D.** The posterior mean  ← key

*Explanation* `.explanation`: Squared-error loss gives the posterior mean, absolute-error loss the posterior median, and 0–1 loss the posterior mode. The MLE is not a Bayes estimator at all, though it coincides with the posterior mode when the prior is flat.

### Q3 — `inference-t7-m-03` *(single, easy)*

In the expression posterior ∝ likelihood × prior, the omitted denominator ∫ f(x | θ) π(θ) dθ is omitted because it:

*Options* `.options[]`:

- **A.** Is always equal to one
- **B.** Cannot be computed for conjugate families
- **C.** Depends only on the prior and not on the data
- **D.** Does not depend on θ and so only normalises  ← key

*Explanation* `.explanation`: The marginal, or prior predictive, is a constant in θ, so it cannot change the shape of the posterior — only its scale. It is generally not equal to one, it is precisely in the conjugate case that it CAN be computed, and it depends on both the prior and the data.

### Q4 — `inference-t7-m-04` *(numeric, easy)*

A Gamma(2, 1) prior in the rate parameterisation is used for a Poisson mean λ. A sample of n = 5 gives Σxᵢ = 10. The posterior mean is:

*Options* `.options[]`:

- **A.** 1.67
- **B.** 2.40
- **C.** 2.00  ← key
- **D.** 1.20

*Explanation* `.explanation`: The Poisson update gives Gamma(α + Σxᵢ, β + n) = Gamma(12, 6), with mean 12/6 = 2.00. Here it happens to equal the MLE of Σx/n = 2 exactly, because the prior mean α/β = 2 is also 2 — a useful reminder that the posterior mean is a weighted average of two numbers and coincides with both when they agree.

*Arithmetic check* `.check`: Gamma(A, B) in rate form has mean A/B. The posterior mean must lie between the prior mean 2 and the MLE 2, so it can only be 2.

### Q5 — `inference-t7-m-05` *(single, easy)*

Which prior family is conjugate to the binomial likelihood?

*Options* `.options[]`:

- **A.** Gamma
- **B.** Normal
- **C.** Inverse-Gamma
- **D.** Beta  ← key

*Explanation* `.explanation`: Beta is conjugate to the binomial, because the Beta kernel θ^(α−1)(1−θ)^(β−1) has the same algebraic shape as the binomial likelihood in θ. Gamma is conjugate to the Poisson and the exponential, Normal to a normal mean with known variance, and Inverse-Gamma to a normal variance with the mean known.

### Q6 — `inference-t7-m-06` *(single, easy)*

A 95% credible interval (a, b) licenses the statement:

*Options* `.options[]`:

- **A.** 95% of intervals constructed this way would contain θ
- **B.** The sample mean lies in (a, b) with probability 0.95
- **C.** θ lies in (a, b) in 95% of future samples
- **D.** θ lies in (a, b) with probability 0.95, given the data and the prior  ← key

*Explanation* `.explanation`: A credible interval is a probability statement about θ conditional on the data. The repeated-sampling option — 95% of intervals constructed this way would contain θ — is the correct reading of a CONFIDENCE interval, which is a statement about the procedure rather than about the parameter, and attaching it to a credible interval, or the reverse, is the error this topic is built to catch.

### Q7 — `inference-t7-m-07` *(numeric, moderate)*

With a uniform prior on θ and 9 successes in 10 trials, the Bayes estimate under squared-error loss is:

*Options* `.options[]`:

- **A.** 0.9000
- **B.** 0.8333  ← key
- **C.** 0.9167
- **D.** 0.8182

*Explanation* `.explanation`: A uniform prior is Beta(1, 1), so the posterior is Beta(10, 2) with mean 10/12 = 0.8333 — Laplace's rule of succession, (x + 1)/(n + 2). The value 0.9000 is the MLE, which equals the posterior MODE under a flat prior but not the posterior mean, and that distinction is the whole point of the question.

*Arithmetic check* `.check`: Flat prior: posterior mode = MLE, posterior mean = (x+1)/(n+2). The question names squared-error loss, so it wants the mean.

### Q8 — `inference-t7-m-08` *(single, moderate)*

A Gamma(α, β) prior in rate form is used for the rate λ of an exponential sample x₁,…,xₙ. The posterior is:

*Options* `.options[]`:

- **A.** Gamma(α + Σxᵢ, β + n)
- **B.** Gamma(α + n, β + n)
- **C.** Gamma(α + Σxᵢ, β + Σxᵢ)
- **D.** Gamma(α + n, β + Σxᵢ)  ← key

*Explanation* `.explanation`: For the exponential, the sample SIZE adds to the shape and the TOTAL TIME adds to the rate: Gamma(α + n, β + Σxᵢ). The first option is the Poisson update, where the roles are reversed — the sum goes to the shape and n to the rate. These two cases are mirror images and this is the most productive confusion in the topic.

### Q9 — `inference-t7-m-09` *(multi, moderate)*

Consider the following statements about conjugate updating.

*Statements to judge* `.statements[]`:

- **A.** Conjugacy is a property of the prior-likelihood pair, not of the prior alone.
- **B.** In the Normal–Normal case with known variance, the posterior variance is the sum of the prior variance and σ²/n.
- **C.** The posterior mean in the Beta–Binomial case lies between the prior mean and the MLE.
- **D.** Deriving a conjugate posterior requires no integration.

*Options* `.options[]`:

- **A.** A and B only
- **B.** A, B and C only
- **C.** A, C and D only  ← key
- **D.** A, B, C and D

*Explanation* `.explanation`: A, C and D hold. B is false: in the Normal–Normal case it is the PRECISIONS that add, not the variances — indeed the posterior variance must be smaller than both inputs, since adding information cannot increase uncertainty.

*Verdict on each statement* `.verdicts`:

- **A — true.** Beta is conjugate to the binomial and to nothing else in this syllabus.
- **B — false.** Precisions add: 1/σₙ² = 1/τ² + n/σ². The posterior variance is below both τ² and σ²/n.
- **C — true.** It is a weighted average of the two, with weight (α+β)/(α+β+n) on the prior mean.
- **D — true.** Multiply the two kernels, add the exponents, recognise the family. That is the whole point of conjugacy.

### Q10 — `inference-t7-m-10` *(numeric, moderate)*

A prior μ ~ N(μ₀, 4) is used for a normal mean with known variance σ² = 9. A sample of n = 3 is taken. The posterior variance is:

*Options* `.options[]`:

- **A.** 7.0000
- **B.** 1.7143  ← key
- **C.** 3.0000
- **D.** 0.5833

*Explanation* `.explanation`: Precisions add: 1/4 + 3/9 = 0.25 + 0.3333 = 0.5833, so the posterior variance is 1/0.5833 = 1.7143, or exactly 12/7. The value 0.5833 is the posterior PRECISION, offered because candidates stop one step early, and 7.0000 adds the two variances, which is the error the arithmetic is designed to expose.

*Arithmetic check* `.check`: The posterior variance must be below both the prior variance 4 and σ²/n = 3. Only 1.7143 passes that test.

### Q11 — `inference-t7-m-11` *(single, moderate)*

Jeffreys' prior for the success probability p of a Bernoulli trial is proportional to:

*Options* `.options[]`:

- **A.** p^(−½)(1 − p)^(−½)  ← key
- **B.** 1 on (0, 1)
- **C.** p(1 − p)
- **D.** p^(−1)(1 − p)^(−1)

*Explanation* `.explanation`: Jeffreys' prior is ∝ √I(θ), and for a Bernoulli I(p) = 1/(p(1−p)), so the prior is ∝ p^(−½)(1−p)^(−½) — the Beta(½, ½) kernel. Note that this puts MORE mass near 0 and 1 than the uniform prior does, so a non-informative prior is not the same thing as one that pulls towards the middle.

### Q12 — `inference-t7-m-12` *(match, moderate)*

Match the item in List I with its counterpart in List II.

*Pairs to match* `.pairs[]`:

| Left | Right |
|---|---|
| A. Squared-error loss | I. The posterior mode |
| B. Absolute-error loss | II. Conjugate to the Poisson likelihood |
| C. 0–1 loss | III. The posterior mean |
| D. The Gamma family | IV. The posterior median |

*Options* `.options[]`:

- **A.** A-III, B-IV, C-I, D-II  ← key
- **B.** A-I, B-III, C-IV, D-II
- **C.** A-III, B-I, C-IV, D-II
- **D.** A-IV, B-III, C-I, D-II

*Explanation* `.explanation`: Squared-error loss gives the posterior mean; absolute-error loss the posterior median; 0–1 loss the posterior mode; and the Gamma family is conjugate to the Poisson likelihood. Each wrong option moves at least two pairs, so the mapping has to be checked rather than inferred from one recognised entry.

*Arithmetic check* `.check`: Fix the three losses first — mean, median, mode in that order — and the fourth pair follows by elimination.

### Q13 — `inference-t7-m-13` *(numeric, moderate)*

A Beta(3, 7) prior is combined with a sample of n = 40 trials. The weight the posterior mean places on the prior mean is:

*Options* `.options[]`:

- **A.** 0.7500
- **B.** 0.2000  ← key
- **C.** 0.8000
- **D.** 0.0750

*Explanation* `.explanation`: The weight is (α + β)/(α + β + n) = 10/(10 + 40) = 0.2000. Read it as a share of a pooled sample: the prior carries ten observations' worth of opinion against forty real observations, so it gets one fifth of the weight. The option 0.8000 is the weight on the MLE, which is the complement.

*Arithmetic check* `.check`: The weight on the prior plus the weight on the MLE must be 1, and with n four times α+β the prior share has to be 1/5.

### Q14 — `inference-t7-m-14` *(single, moderate)*

With a uniform prior on a probability, the maximum likelihood estimate coincides exactly with:

*Options* `.options[]`:

- **A.** The posterior mode  ← key
- **B.** The posterior mean
- **C.** The posterior median
- **D.** All three posterior summaries

*Explanation* `.explanation`: A flat prior makes the posterior proportional to the likelihood, so the posterior is maximised where the likelihood is — the posterior MODE equals the MLE. The posterior mean is (x + 1)/(n + 2), a different number, and the three summaries coincide only when the posterior is symmetric, which Beta(1 + x, 1 + n − x) generally is not.

### Q15 — `inference-t7-m-15` *(multi, moderate)*

Consider the following statements about interval estimates.

*Statements to judge* `.statements[]`:

- **A.** A credible interval is a probability statement about the parameter given the data.
- **B.** A confidence interval is a statement about the procedure under repeated sampling.
- **C.** For a skewed posterior the HPD interval is longer than the equal-tailed interval.
- **D.** A credible interval and a confidence interval converge as the sample size grows with the prior fixed.

*Options* `.options[]`:

- **A.** A and B only
- **B.** B and C only
- **C.** A, B and D only  ← key
- **D.** A, C and D only

*Explanation* `.explanation`: A, B and D hold. C is false: the HPD interval is the SHORTEST set of the required posterior probability, so for a skewed posterior it is strictly shorter than the equal-tailed interval, not longer; the two coincide only when the posterior is symmetric and unimodal.

*Verdict on each statement* `.verdicts`:

- **A — true.** P(θ ∈ C | x) = 0.95, which is the statement people wrongly make about confidence intervals.
- **B — true.** 95% of such intervals would cover the fixed θ; nothing is asserted about the one in hand.
- **C — false.** The HPD is the shortest such set by construction, so it is never longer — equal only under symmetry.
- **D — true.** The weight on the prior tends to zero and the posterior variance approaches σ²/n.

### Q16 — `inference-t7-m-16` *(single, moderate)*

For the conjugate families in the syllabus, the posterior mean is always:

*Options* `.options[]`:

- **A.** Between the prior mean and the MLE  ← key
- **B.** Equal to the MLE
- **C.** Equal to the prior mean
- **D.** Outside the range of the prior mean and the MLE

*Explanation* `.explanation`: It is a weighted average of the prior mean and the MLE with weights summing to one, so it must lie between them, coinciding with one only if the two already agree or a weight is zero. Note the qualifier: this is a property of these conjugate families, not a general theorem about Bayesian estimation.

### Q17 — `inference-t7-m-17` *(numeric, hard)*

A Gamma(2, 3) prior in rate form is used for the rate λ of an exponential sample with n = 10 and Σxᵢ = 5. Under 0–1 loss, the Bayes estimate of λ is:

*Options* `.options[]`:

- **A.** 1.5000
- **B.** 1.3750  ← key
- **C.** 1.4583
- **D.** 2.0000

*Explanation* `.explanation`: The exponential update gives Gamma(α + n, β + Σxᵢ) = Gamma(12, 8). Under 0–1 loss the estimate is the posterior MODE, (A − 1)/B = 11/8 = 1.3750. The value 1.5000 is the posterior mean, which squared-error loss would give, and 1.4583 is the posterior median for absolute-error loss — all three are in the options because the question turns on which loss was named.

*Arithmetic check* `.check`: For a right-skewed Gamma the order is mode < median < mean: 1.3750 < 1.4583 < 1.5000. 0–1 loss wants the smallest of the three.

### Q18 — `inference-t7-m-18` *(numeric, hard)*

Ten items are tested and all ten pass. Using a uniform prior and squared-error loss, the Bayes estimate of the pass probability is:

*Options* `.options[]`:

- **A.** 1.0000
- **B.** 0.9545
- **C.** 0.9167  ← key
- **D.** 0.9091

*Explanation* `.explanation`: The posterior is Beta(1 + 10, 1 + 0) = Beta(11, 1), with mean 11/12 = 0.9167 — Laplace's rule of succession. The MLE of 1.0000 asserts that failure is impossible on the strength of ten trials, which is the practical argument for not reporting it; 0.9545 is the Jeffreys-prior answer, 21/22, and 0.9091 is 10/11, which is neither.

*Arithmetic check* `.check`: (x+1)/(n+2) = 11/12. Any estimate of exactly 1 should be suspected: no finite sample can rule out failure.

### Q19 — `inference-t7-m-19` *(single, hard)*

A statement reads: 'Because the Bayes estimator under squared-error loss is biased in the frequentist sense, it is inferior to the unbiased estimator.' What is wrong with it?

*Options* `.options[]`:

- **A.** The Bayes estimator under squared-error loss is in fact unbiased
- **B.** Bias is irrelevant because Bayesian estimators are not random variables
- **C.** The two optimise different criteria, so bias does not establish inferiority  ← key
- **D.** Nothing is wrong; unbiasedness is the stronger requirement

*Explanation* `.explanation`: The premise is correct — a Bayes estimator generally is biased — but the inference is not. The Bayes estimator minimises expected posterior loss, and shrinking towards the prior mean buys a variance reduction at the cost of bias, which can lower mean squared error overall. Unbiasedness is a constraint, not a measure of quality, and declaring one estimator inferior requires first naming the criterion.

### Q20 — `inference-t7-m-20` *(single, hard)*

A posterior is Beta(8, 3). A question asks for the Bayes estimate without naming a loss function. The best answer, and the reason, is:

*Options* `.options[]`:

- **A.** 0.7778, because the mode is the most probable value
- **B.** 0.7273, because the posterior mean is the convention when no loss is stated  ← key
- **C.** Either, because for a Beta posterior the mean and mode coincide
- **D.** Neither, because the question cannot be answered without the loss

*Explanation* `.explanation`: Beta(8, 3) has mean 8/11 = 0.7273 and mode 7/9 = 0.7778, so the option claiming the two coincide is wrong on the arithmetic. The honest position is that 'the Bayes estimator' is undefined until a loss is named — but the convention in every syllabus and examination is squared-error loss, so the posterior mean is the expected answer, and refusing to answer would lose the mark.

---

## Authoring and verification record `provenance`

Reproduced verbatim. It records what changed in each version and how each derivation was checked, including the findings of the two previous review rounds and the reasons some of their recommendations were declined.

> Review pass, October 2026: 3 per-scene quick checks added on theory, worked and explore scenes from a third-party module review, each read for correctness before import; a further set offered for completion and guided scenes was declined, since those scenes already end with the learner writing an answer. The same pass scoped two 'always' claims in the three-Bayesians scenario that the review did not flag: the posterior mean lying between the prior mean and the MLE, and the prior washing out as n grows, both hold for the conjugate families in that scene but not in general. Authored for this platform in October 2026. Every numerical result was computed rather than recalled, and checked independently: the Beta(2,3) + 7/10 example (posterior Beta(9,6), mean 0.6, mode 8/13, prior weight 1/3, weighted decomposition exact); the Normal–Normal case (prior N(100,25), σ²=36, n=9, x̄=112, giving posterior precision 0.29, variance 3.448276, sd 1.856953, mean 110.344828 and a 95% credible interval of (106.705, 113.984)); and the Gamma–Poisson transfer case (Gamma(3,2) with Σx=14, n=7, giving Gamma(17,9), mean 1.888889, mode 1.777778, and an exact median of 1.851984 by bisection on the regularised incomplete gamma, against the approximation (A−1/3)/B = 1.851852). The Gamma family is used in the RATE parameterisation throughout, and the lesson says so, because Indian textbooks use both.

