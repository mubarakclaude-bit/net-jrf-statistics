# Lesson 4.6 — The Cramér–Rao Bound and Fisher Information

Complete authored content of one lesson from a UGC-NET Statistics (Code 107) preparation application, extracted from the application's own content files.

| | |
|---|---|
| Content version | 1.3 |
| Scenes | 14 |
| Core scenes | 14 |
| Optional JRF-extension scenes | 0 |
| Estimated learner time | 51 minutes |
| Mastery pool | 20 items |
| Position in the app | Statistical Inference → Point Estimation → How good can an estimator be |
| Engine | Estimation and inference — curvature of the log-likelihood, and the variance floor it sets |
| Pool label | Cramér–Rao and Fisher information — mastery test (unseen) |
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

1. Compute Fisher information by either formula, E[(∂ℓ/∂θ)²] or −E[∂²ℓ/∂θ²], and scale it to a sample as nI₁(θ).

2. Write the Cramér–Rao bound for an unbiased estimator of θ, and for a function g(θ) with [g′(θ)]² on top.

3. Check the regularity conditions before quoting the bound, and name the family where they fail.

4. Decide whether a given estimator attains the bound, using the linear-score condition rather than guesswork.

5. Compute efficiency and relative efficiency, and state what the bound says about the MLE as n grows.

**Assumed prior knowledge** `prereq[]`

- `prereq[0]` **Log-likelihood and the score** — Everything here is built on ℓ(θ) and its first two derivatives. If writing ℓ is still slow, do the MLE topic first.
- `prereq[1]` **Variance of a sample mean** — Nearly every attainment check ends by comparing a bound with Var(X̄) = Var(X)/n.
- `prereq[2]` **Rao–Blackwell and Lehmann–Scheffé** — The bound and the UMVUE answer different questions. Scene 8 shows a case where the best unbiased estimator still does not reach the floor.

**Misconceptions the lesson is built to pre-empt** `traps[]`

- Quoting the bound for a family whose support moves with θ.

- Forgetting the [g′(θ)]² numerator when the target is a function of θ rather than θ itself.

- Using the bound on a biased estimator without the (1 + b′(θ))² numerator.

- Writing I₁(θ) where the question wants nI₁(θ), or the reverse.

- Assuming a UMVUE must attain the bound — it need not.

- Confusing observed information −∂²ℓ/∂θ² at θ̂ with expected information −E[∂²ℓ/∂θ²].

- Treating 'the MLE is efficient' as a finite-sample statement. It is asymptotic.

**Assessment policy** `mastery`

- 10 items drawn per attempt from a pool of 20, mix 3 easy, 5 moderate, 2 hard
- pass mark 80%, no hints during the test, retest after 7 days
- `mastery.note`: Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the difficulty mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split.

**Sources** `refs[]`

- `refs[0]` **Fisher information and the Cramér–Rao bound** — Stanford STATS 200 (Autumn 2016), Lecture 15 (Lecture notes, free). The definition, the theorem with a proof, efficiency, and the MLE's asymptotic normality in eight pages, with Gamma examples. Read it after scene 7. One gap to know about: it refers to 'certain regularity conditions' without listing them — scene 3 here spells them out, so the two complement each other.
- `refs[1]` **Mathematical Statistics — Unbiased Estimation and Risk Inequalities** — MIT OpenCourseWare 18.655 (Spring 2016), Lecture note 13 (Lecture notes, free). Places the bound inside the risk framework alongside Rao–Blackwell, which is where it belongs. Useful at scene 8, when you want to see why a UMVUE can sit strictly above the floor.

---

## The lesson, scene by scene

### Scene 1 of 14 — Before the lesson — four things it will assume

`scenes[0]` · id `s0` · type `foundation` (prerequisite check) · 6 minutes

**Purpose** `scenes[0].objective`

Confirm the score, the two forms of Fisher information and the variance of a mean, before the bound is derived.

**Body** `scenes[0].body[]`

The Cramér–Rao bound is a formula with four places to go wrong, and three of them are in the groundwork rather than the idea. You need the log-likelihood and its derivatives at speed, you need to know that information adds across an iid sample, and you need Var(X̄) = σ²/n on reflex because that is what almost every attainment check compares against.

Four checks. If the first one is shaky, the maximum likelihood topic is the better place to be for half an hour — this lesson is built directly on it.

**Check 1** `scenes[0].items[0]`

- *asks:* Write the log-likelihood and the score for an iid sample, and say what E[score] is.
- *expected answer* `.recall`: ℓ(θ) = Σᵢ log f(xᵢ;θ) and the score is U(θ) = ∂ℓ/∂θ = Σᵢ ∂log f(xᵢ;θ)/∂θ. Under the regularity conditions E[U(θ)] = 0 for every θ, and Var(U(θ)) = Iₙ(θ).

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> The log turns the product likelihood into a sum, so the score is a sum of n independent terms — which is where every 'information adds' result comes from.

> E[U] = 0 is not an accident of a particular family; it follows from differentiating ∫f(x;θ)dx = 1 under the integral sign. That interchange is precisely what the regularity conditions license, and it is why the bound fails for U(0,θ), where the range of the density depends on θ.

> Do one. Exponential rate λ: log f = log λ − λx, so U(λ) = Σ(1/λ − xᵢ) = n/λ − Σxᵢ. Check: E[U] = n/λ − n·(1/λ) = 0, as promised.

**Check 2** `scenes[0].items[1]`

- *asks:* Give the two expressions for Fisher information from a single observation, and relate Iₙ(θ) to I(θ).
- *expected answer* `.recall`: I(θ) = E[(∂log f/∂θ)²] = −E[∂²log f/∂θ²] — the two are equal under the regularity conditions. For an iid sample Iₙ(θ) = n·I(θ): information adds.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Use whichever is less work. The second-derivative form is usually easier because differentiating twice often kills the data entirely and leaves no expectation to take.

> Exponential rate λ again: log f = log λ − λx, so ∂²/∂λ² = −1/λ², which is already constant. Then I(λ) = −E[−1/λ²] = 1/λ², and Iₙ(λ) = n/λ².

> Additivity is worth a sentence of its own, because questions exploit it. The score is a sum of independent terms, so its variance is the sum of their variances, and each term contributes the same I(θ). Twice the data, twice the information, half the bound.

**Check 3** `scenes[0].items[2]`

- *asks:* What is Var(X̄) in terms of Var(X), and why does it appear in nearly every attainment check?
- *expected answer* `.recall`: Var(X̄) = σ²/n. For many standard families the bound for estimating the mean works out to exactly σ²/n, so the check 'is the bound attained?' becomes 'does my estimator's variance equal σ²/n?'

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Var(ΣXᵢ) = nσ² by independence, and dividing a random variable by n divides its variance by n², so Var(X̄) = nσ²/n² = σ²/n.

> That is why X̄ keeps turning out to be efficient. For a Poisson(θ) sample, Iₙ(θ) = n/θ so the bound is θ/n; and Var(X̄) = θ/n since the Poisson variance is θ. The bound is attained exactly, and X̄ is the UMVUE for θ.

> Keep the n straight. The bound 1/Iₙ(θ) uses the information in the whole sample; comparing it against Var(X) rather than Var(X̄) is the slip that makes an efficient estimator look n times too bad.

**Check 4** `scenes[0].items[3]`

- *asks:* If the target is τ(θ) rather than θ itself, what changes in the bound?
- *expected answer* `.recall`: The numerator becomes the square of the derivative: Var(T) ≥ [τ′(θ)]²/Iₙ(θ) for any T unbiased for τ(θ). Forgetting to square τ′ is the single most common slip in this topic.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> The plain bound Var(T) ≥ 1/Iₙ(θ) is the special case τ(θ) = θ, where τ′ = 1 and the numerator is invisible. As soon as the target is a function of θ, the numerator reappears.

> Example. Estimating τ(θ) = θ² from a Poisson sample: τ′ = 2θ, Iₙ = n/θ, so the bound is (2θ)²·θ/n = 4θ³/n. Dropping the square would give 2θ²/n — a different order in θ, and an option on the paper.

> The derivative is with respect to θ, evaluated at the true θ, and it is squared because variance is on a squared scale. If a question gives you τ in words — 'the probability of no events', e^(−θ) for a Poisson — write τ down explicitly and differentiate it before touching the bound.

---

### Scene 2 of 14 — How sharp is the peak?

`scenes[1]` · id `s1` · type `intuition` (intuition) · 5 minutes

**Purpose** `scenes[1].objective`

See information as curvature before meeting any formula.

**Body** `scenes[1].body[]`

Two experiments, same estimate. In the first, the log-likelihood rises to a sharp spike at θ̂ and falls away steeply on both sides. In the second it has a long flat ridge, and values a fair distance from θ̂ are almost as plausible.

Which experiment has told you more about θ? Obviously the first. In the second, the data barely discriminate between neighbouring parameter values, so any estimate you form will move around a lot from sample to sample.

That is the whole idea, and Fisher information is the number that measures it: the curvature of the log-likelihood at the top, averaged over the samples you might have drawn. Steep curvature means high information. High information means a low floor on how much any estimator must vary.

The Cramér–Rao bound turns that into an inequality you can compute with. It says no unbiased estimator of θ can have variance below 1/(nI(θ)). Not 'no estimator anyone has found' — no estimator that exists, under the stated conditions.

Two things follow that the exam likes. If you find an unbiased estimator whose variance equals the bound, you are finished: it is the best unbiased estimator and you need no further argument. And if the bound tells you something impossible, that is a signal the conditions were violated, not that you have discovered a better estimator.

**Aside — Why the second derivative and not the first** `scenes[1].aside.body`

At the maximum the first derivative is zero by construction — it carries no information about sharpness. The second derivative is the first quantity that measures how fast the likelihood falls away, which is exactly what 'the data pin θ down' means.

**Quick check before moving on** `scenes[1].ask`

- *question:* Why does a flatter log-likelihood near its maximum mean a less precise estimator?
- *hint on request:* If the curve is nearly flat, how different could the data have been before the peak moved appreciably?

**Optional deep-dive, opened on demand — Specifying a sensor before it exists** `scenes[1].scenario`

*teaser on the closed card:* How many measurements does a sensor need? The Cramér–Rao bound answers before anything is built.

> An engineering team is specifying a vibration monitor for rotating equipment. The requirement is to estimate a shaft's rotational frequency to within a stated tolerance. The questions on the table are how long to sample, at what rate, and whether a cheaper sensor with more noise can be rescued by simply taking more samples.

> None of these can be answered by trying estimation algorithms, because the answer must not depend on which algorithm is eventually written. What is needed is a floor: the best precision ANY unbiased estimator could achieve from data of that quality. That floor is 1/(n I(θ)), and computing it needs only the measurement model — no data and no code.

> This is routine practice in signal processing. The Cramér–Rao bound on a time-of-arrival estimate sets the theoretical ranging accuracy of a radar or a satellite navigation signal, and it is computed at the system-design stage to decide bandwidth and power. If the bound says the required accuracy is unreachable with the proposed signal, no amount of clever processing will rescue it, and the specification has to change.

> Two consequences shape the engineering. First, information adds: Iₙ = n I₁, so the floor on the variance falls like 1/n and the standard error like 1/√n. Halving the error costs four times the samples — which is why 'just sample more' runs into diminishing returns, and why a quieter sensor usually beats a longer record.

> Second, a design can be judged before it is built. If a candidate algorithm's variance sits close to the bound it is efficient and there is nothing left to gain from better processing; if it sits far above, the money is better spent on the algorithm than on the hardware. Efficiency, computed as bound ÷ achieved variance, is the number that decides where the next pound goes.

*think-it-through question* `.q`: The team doubles the sampling rate, doubling n. By what factor does the achievable standard error improve, and what would the same money buy if spent on halving the sensor noise instead?

*what the statistics says* `.answer`: Doubling n halves the variance floor, so the standard error falls by a factor of √2 — about 29%. Halving the noise standard deviation, in a Gaussian measurement model where I(θ) ∝ 1/σ², quadruples the information and halves the standard error — a 50% improvement. Noise reduction beats sampling because information enters linearly in n but as 1/σ² in the noise. That comparison is exactly what the bound is for: it is a design calculation, not a data analysis.

*link line* `.link`: The same reasoning sets the sample-size calculation in a clinical trial: the information per subject fixes how many subjects are needed for a given precision, before a single patient is enrolled.

---

### Scene 3 of 14 — Watch the peak sharpen as the sample grows

`scenes[2]` · id `s2` · type `explore` (interactive visualisation) · 6 minutes

**Purpose** `scenes[2].objective`

Connect sample size, curvature and the variance floor in one picture.

**Body** `scenes[2].body[]`

This is the exponential likelihood. Leave Σxᵢ roughly proportional to n — for instance n = 3 with Σx = 12, then n = 6 with Σx = 24 — so the peak stays near the same λ̂, and watch what happens to its WIDTH.

At n = 3 the curve is a broad hill: a wide band of rates makes the data nearly as plausible. At n = 12 it is a narrow spike. Nothing about the estimate changed; what changed is how firmly the data exclude neighbouring values.

That narrowing is information accumulating. For the exponential rate, I₁(λ) = 1/λ², so a sample of n carries Iₙ(λ) = n/λ², and the Cramér–Rao floor for an unbiased estimator of λ is λ²/n. Double n and the floor halves.

Information adds because the observations are independent: each one contributes its own curvature to the total. That additivity is why nearly every bound you will compute in an exam has an n in the denominator and nothing more complicated.

**Interactive element** `scenes[2].viz` — live plot of type `exp-likelihood`, initial state n=3, sumx=12.0. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[2].ask`

- *question:* The floor for estimating λ is λ²/n, so it shrinks like 1/n. What does that say about the standard error, and about how many observations you need to halve it?
- *hint on request:* Standard error is the square root of variance. If variance falls like 1/n, what does its square root do?

---

### Scene 4 of 14 — Score, information, and the conditions that make it work

`scenes[3]` · id `s3` · type `theory` (theory) · 8 minutes

**Purpose** `scenes[3].objective`

Get both formulas for I(θ) and know exactly when they are allowed.

**Block 1 — Score function** `scenes[3].blocks[0]` *(type `def`)*

U(θ) = ∂ℓ(θ)/∂θ, the derivative of the log-likelihood. Under regularity it has mean zero: E_θ[U(θ)] = 0. Setting U = 0 is how you found the MLE, so the score is already familiar.

**Block 2 — Fisher information — two equal forms** `scenes[3].blocks[1]` *(type `formula`)*

I(θ) = Var( U(θ) ) = E[ (∂ℓ/∂θ)² ]  =  − E[ ∂²ℓ/∂θ² ]

**Block 3 — Which form to use** `scenes[3].blocks[2]` *(type `note`)*

Almost always the second. Differentiating twice and taking an expectation is shorter than squaring a score and expanding it. The two agree only under regularity — the equality is itself a consequence of being allowed to swap differentiation and integration.

**Block 4 — Information adds** `scenes[3].blocks[3]` *(type `formula`)*

For an iid sample of size n:   Iₙ(θ) = n · I₁(θ).
Compute the information in ONE observation, then multiply.

**Block 5 — The regularity conditions** `scenes[3].blocks[4]` *(type `assume`)*

The support of f does not depend on θ; θ is interior to the parameter space; ℓ is twice differentiable in θ; differentiation under the integral sign is valid; and 0 < I(θ) < ∞. Every result below assumes all of these.

**Block 6 — Observed versus expected information** `scenes[3].blocks[5]` *(type `trap`)*

−∂²ℓ/∂θ² evaluated at θ̂ is the OBSERVED information: a number computed from your data. I(θ) = −E[∂²ℓ/∂θ²] is the EXPECTED information: an average over all samples, and a function of θ. The Cramér–Rao bound uses the expected one. Software often reports the observed one, and questions exploit the difference.

**Block 7 — A sanity check worth doing** `scenes[3].blocks[6]` *(type `note`)*

I(θ) must be strictly positive. If your calculation gives zero or something negative, you have dropped a sign or differentiated the wrong variable — go back rather than carry it forward.

**Flow diagram** `scenes[3].flow` — Is this estimator efficient? The order that avoids wasted work

*alt text* `.alt`: Decision chart for the Cramér–Rao bound

- row 1: An unbiased estimator T of g(θ)
- row 2: Does the support depend on θ?
- row 3: Regularity fails — there is NO bound to quote  |  Compute I(θ) = −E[∂²ℓ/∂θ²], then scale: Iₙ = n I₁
- row 4: Is the target θ itself?
- row 5: Bound = 1/(n I(θ))  |  Bound = [g′(θ)]²/(n I(θ))
- row 6: Compare with Var(T): efficiency = bound ÷ Var(T)
- arrows: An unbiased estimator T of g(θ) → Does the support depend on θ?; Does the support depend on θ? → [yes] Regularity fails — there is NO bound to quote; Does the support depend on θ? → [no] Compute I(θ) = −E[∂²ℓ/∂θ²], then scale: Iₙ = n I₁; Compute I(θ) = −E[∂²ℓ/∂θ²], then scale: Iₙ = n I₁ → Is the target θ itself?; Is the target θ itself? → [yes] Bound = 1/(n I(θ)); Is the target θ itself? → [no] Bound = [g′(θ)]²/(n I(θ)); Bound = 1/(n I(θ)) → Compare with Var(T): efficiency = bound ÷ Var(T); Bound = [g′(θ)]²/(n I(θ)) → Compare with Var(T): efficiency = bound ÷ Var(T)

*note shown under the diagram* `.note`: Check regularity FIRST. Computing an information number for U(0,θ) and then quoting a bound produces a contradiction, and the contradiction is evidence the conditions were violated — not a discovery.

**Quick check before moving on** `scenes[3].ask`

- *question:* What regularity assumptions are used when differentiating under the integral sign to show the score has expectation zero?
- *hint on request:* The support and differentiability/integrability conditions must justify exchanging differentiation and integration; parameter-dependent support can break the usual argument.

---

### Scene 5 of 14 — Worked in full — the Bernoulli

`scenes[4]` · id `s4` · type `worked` (worked example) · 6 minutes

**Purpose** `scenes[4].objective`

Compute I(p), write the bound, and settle attainment in one pass.

**Problem put to the learner** `scenes[4].problem`

X₁,…,Xₙ are iid Bernoulli(p). Find I(p), the Cramér–Rao bound for unbiased estimators of p, and decide whether x̄ attains it.

**Worked steps** `scenes[4].steps[]`

1. `scenes[4].steps[0]` Log-likelihood for one observation.

   ```
   ℓ(p) = x log p + (1 − x) log(1 − p)
   ```

   *why* `.why`: Work with a single observation and multiply by n at the end. It is less algebra and it is what Iₙ = nI₁ is for.

2. `scenes[4].steps[1]` Score.

   ```
   U(p) = ∂ℓ/∂p = x/p − (1 − x)/(1 − p)
   ```

   Laid out:

   $$U(p) = \frac{∂ℓ}{∂p} = \frac{x}{p} − \frac{(1 − x)}{(1 − p)}$$

   *why* `.why`: Note the minus sign from the chain rule on log(1−p). It is the commonest slip in this calculation.

3. `scenes[4].steps[2]` Second derivative.

   ```
   ∂²ℓ/∂p² = − x/p² − (1 − x)/(1 − p)²
   ```

   Laid out:

   $$\frac{∂²ℓ}{∂p²} = − \frac{x}{p²} − \frac{(1 − x)}{(1 − p)²}$$

   *why* `.why`: Both terms are negative for any x, which is the concavity you expect at a maximum.

4. `scenes[4].steps[3]` Take minus the expectation, using E[X] = p.

   ```
   I(p) = p/p² + (1 − p)/(1 − p)² = 1/p + 1/(1 − p) = 1/( p(1 − p) )
   ```

   Laid out:

   $$I(p) = \frac{p}{p²} + \frac{(1 − p)}{(1 − p)²} = \frac{1}{p} + \frac{1}{(1 − p)} = \frac{1}{( p(1 − p) )}$$

   *why* `.why`: The two fractions combine over a common denominator. Notice the result is largest near p = 0 or 1 and smallest at p = 0.5 — extreme probabilities are easier to pin down.

5. `scenes[4].steps[4]` Scale to the sample and write the bound.

   ```
   Iₙ(p) = n/( p(1−p) ),   CRLB = 1/Iₙ(p) = p(1 − p)/n
   ```

   Laid out:

   $$Iₙ(p) = \frac{n}{( p(1−p) )},   CRLB = \frac{1}{Iₙ(p)} = \frac{p(1 − p)}{n}$$

   *why* `.why`: The bound is the reciprocal of the total information. Every unbiased estimator of p must have variance at least this.

6. `scenes[4].steps[5]` Check attainment.

   ```
   Var(x̄) = Var(X)/n = p(1 − p)/n  =  CRLB   ✓
   ```

   Laid out:

   $$Var(x̄) = \frac{Var(X)}{n} = \frac{p(1 − p)}{n}  =  CRLB   ✓$$

   *why* `.why`: Equality, so x̄ is efficient and no unbiased estimator of p can do better. This also re-derives, in one line, that x̄ is the UMVUE — without Rao–Blackwell or Lehmann–Scheffé.

**What to take from it** `scenes[4].after`

Three questions answered by one calculation: how much information the data carry, what floor that sets, and whether the obvious estimator reaches it. When a question asks only for the bound, compute the attainment check anyway — it is two lines and it is often the next part.

**Quick check before moving on** `scenes[4].ask`

- *question:* For a Bernoulli sample, how do you derive Fisher information from the score rather than memorising the formula?
- *hint on request:* Differentiate the log-likelihood, square the score, and take its expectation (or use the negative expected second derivative when justified).

---

### Scene 6 of 14 — Pause and recall

`scenes[5]` · id `s5` · type `recall` (retrieval practice) · 2 minutes

**Purpose** `scenes[5].objective`

Retrieve before reading on — this is where the retention comes from.

**Intro** `scenes[5].intro`

Answer each in your head before revealing. Correcting a wrong retrieval beats re-reading a right answer.

- `scenes[5].items[0]` **Q:** Write both formulas for Fisher information.  
  **A:** I(θ) = E[(∂ℓ/∂θ)²] = −E[∂²ℓ/∂θ²].
- `scenes[5].items[1]` **Q:** How does information scale with sample size?  
  **A:** Iₙ(θ) = n·I₁(θ) — it adds across independent observations.
- `scenes[5].items[2]` **Q:** State the Cramér–Rao bound for an unbiased estimator of θ.  
  **A:** Var(T) ≥ 1/(n I(θ)).
- `scenes[5].items[3]` **Q:** Name the condition that most often fails, and one family where it does.  
  **A:** The support must not depend on θ. U(0,θ) violates it.

---

### Scene 7 of 14 — Your turn, with the scaffolding removed — the Poisson

`scenes[6]` · id `s6` · type `completion` (fill in the blanks) · 7 minutes

**Purpose** `scenes[6].objective`

Run the same four steps yourself on a discrete family.

**Problem put to the learner** `scenes[6].problem`

X₁,…,Xₙ are iid Poisson(λ). Find I(λ), the Cramér–Rao bound for unbiased estimators of λ, and decide whether x̄ attains it.

**Worked steps** `scenes[6].steps[]`

1. `scenes[6].steps[0]` Log-likelihood for one observation, dropping the constant.

   ```
   ℓ(λ) = −λ + x log λ − log(x!)
   ```

   *why* `.why`: The log(x!) term has no λ in it, so it will vanish on the first derivative. Write it once and forget it.

2. `scenes[6].steps[1]` Differentiate twice.

   - *learner is asked:* Write ∂²ℓ/∂λ².
   - *accepted answer* `.blank.answer`: −x/λ²
   - *also accepted:* −x/λ²; -x/lambda^2; -x/λ^2; −x/λ^2; -x/λ²
   - *hint:* First derivative is −1 + x/λ. Differentiate again: the constant disappears and x/λ = xλ^(−1) brings down a factor.

   *why* `.why`: Negative for every x > 0, as concavity at a maximum requires.

3. `scenes[6].steps[2]` Take minus the expectation, using E[X] = λ.

   - *learner is asked:* Write I(λ).
   - *accepted answer* `.blank.answer`: 1/λ
   - *also accepted:* 1/λ; 1/lambda; 1/λ ; λ^(-1); 1 / λ
   - *hint:* −E[−X/λ²] = E[X]/λ². Now substitute E[X] = λ and cancel.

   *why* `.why`: Information falls as λ grows, so the floor λ/n rises: a larger mean is harder to pin down in ABSOLUTE terms. Relative to λ itself it is easier — the standard error √(λ/n) divided by λ is 1/√(nλ), which shrinks. Keep the two straight; questions ask for one and offer the other.

4. `scenes[6].steps[3]` Write the bound for a sample of size n.

   - *learner is asked:* Write the Cramér–Rao bound for unbiased estimators of λ.
   - *accepted answer* `.blank.answer`: λ/n
   - *also accepted:* λ/n; lambda/n; λ / n
   - *hint:* Iₙ = n·I₁, and the bound is its reciprocal.

   *why* `.why`: The familiar 1/n rate, with the parameter itself in the numerator.

5. `scenes[6].steps[4]` Check attainment.

   ```
   Var(x̄) = Var(X)/n = λ/n = CRLB   ✓  so x̄ is efficient
   ```

   Laid out:

   $$Var(x̄) = \frac{Var(X)}{n} = \frac{λ}{n} = CRLB   ✓  so x̄ is efficient$$

   *why* `.why`: The Poisson variance equals its mean, which is exactly what makes the equality come out. x̄ is the UMVUE of λ and attains the floor.

**What to take from it** `scenes[6].after`

Bernoulli and Poisson both came out efficient, which can give the impression that the obvious estimator always attains the bound. Scene 8 breaks that impression on purpose.

---

### Scene 8 of 14 — The bound itself — functions, bias, attainment, efficiency

`scenes[7]` · id `s7` · type `theory` (theory) · 9 minutes

**Purpose** `scenes[7].objective`

Handle the three variants the exam actually sets, and know when the floor is reachable.

**Block 1 — Cramér–Rao, the standard form** `scenes[7].blocks[0]` *(type `formula`)*

T unbiased for θ:    Var_θ(T)  ≥  1 / ( n I(θ) )

**Block 2 — For a function of θ** `scenes[7].blocks[1]` *(type `formula`)*

T unbiased for g(θ):    Var_θ(T)  ≥  [ g′(θ) ]² / ( n I(θ) )
The derivative is SQUARED. Dropping that square is the single commonest error in this topic.

**Block 3 — For a biased estimator** `scenes[7].blocks[2]` *(type `formula`)*

If E[T] = θ + b(θ):    Var_θ(T)  ≥  ( 1 + b′(θ) )² / ( n I(θ) )
Setting b ≡ 0 recovers the standard form, so this is the general statement.

**Block 4 — Efficiency** `scenes[7].blocks[3]` *(type `def`)*

e(T) = CRLB / Var(T), a number in (0, 1]. T is efficient when e(T) = 1. Relative efficiency of T₁ to T₂ is Var(T₂)/Var(T₁).

**Block 5 — When is the bound attainable at all?** `scenes[7].blocks[4]` *(type `formula`)*

Equality holds for an unbiased T of g(θ) if and only if the score factorises as
   ∂ℓ/∂θ  =  A(θ) · [ T − g(θ) ]
for some function A not involving the data. In words: the score must be LINEAR in T.

**Block 6 — How to use that condition** `scenes[7].blocks[5]` *(type `note`)*

Write the score, and try to collect it into a constant-in-data multiple of (something − something). If it refuses to factorise that way, no unbiased estimator attains the bound and the floor is unreachable — which is a complete answer to 'does an efficient estimator exist?'.

**Block 7 — Where the bound does not apply at all** `scenes[7].blocks[6]` *(type `trap`)*

If the support depends on θ, regularity fails and the inequality is simply not available. For U(0,θ) the UMVUE (n+1)/n·X₍ₙ₎ has variance θ²/(n(n+2)), which is of order n⁻² — faster than any 1/n floor could allow. Quoting a Cramér–Rao bound there produces a contradiction, and the contradiction is the evidence that the conditions were violated.

**Block 8 — What it says about the MLE** `scenes[7].blocks[7]` *(type `note`)*

Under regularity, √n(θ̂ − θ) → N(0, 1/I(θ)), so the MLE's variance approaches 1/(nI(θ)) — the bound — as n grows. The MLE is asymptotically efficient. At finite n it may be biased and may sit above the floor, as the next scene shows.

**Quick check before moving on** `scenes[7].ask`

- *question:* What are the conditions for the Cramér–Rao inequality, and what does equality tell you?
- *hint on request:* The estimator must be unbiased with finite variance and the regularity conditions must hold; equality indicates the score is proportional to the centered estimator under the relevant conditions.

---

### Scene 9 of 14 — A case where nothing reaches the floor

`scenes[8]` · id `s8` · type `explore` (interactive visualisation) · 7 minutes

**Purpose** `scenes[8].objective`

See that the bound is a floor, not a promise — and that the parameterisation decides.

**Body** `scenes[8].body[]`

Exponential again, and here I(λ) = 1/λ², so the floor for an unbiased estimator of the RATE is λ²/n. With λ = 0.5 and n = 10 that is 0.25/10 = 0.025.

From the previous topic, the UMVUE of λ is (n−1)/ΣX, and its variance works out to λ²/(n−2) = 0.25/8 = 0.03125. That is comfortably above the floor of 0.025. The best unbiased estimator that exists does not attain the bound.

Why not? Apply the attainment test. The score is ∂ℓ/∂λ = n/λ − Σxᵢ = −n( x̄ − 1/λ ). It IS linear — but in x̄, and against the target 1/λ, not λ. So an unbiased estimator of 1/λ attains the bound, and no unbiased estimator of λ does.

Check that claim directly. Write θ = 1/λ for the mean. Then I(θ) = 1/θ² as well, the floor is θ²/n, and Var(X̄) = θ²/n exactly. Attained.

The same family, the same data, the same information — and the bound is reachable for the mean but not for the rate. Attainability is a property of the parameterisation, not only of the model. Raise n on the slider and watch the MLE's spread fall toward the floor it never quite sits on.

**Interactive element** `scenes[8].viz` — live plot of type `mle-sampling`, initial state lam=0.5, n=10. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[8].ask`

- *question:* The MLE is called efficient, yet here it sits above the floor at every finite n. In what sense is the claim true?
- *hint on request:* Look at what happens to the ratio of its variance to the bound as n grows, rather than at the gap itself.

---

### Scene 10 of 14 — Now without the steps — the normal mean

`scenes[9]` · id `s9` · type `guided` (guided problem) · 7 minutes

**Purpose** `scenes[9].objective`

Run the whole calculation unaided on the family that appears most often.

**Problem put to the learner** `scenes[9].problem`

X₁,…,Xₙ are iid N(μ, σ²) with σ² KNOWN. Find I(μ), write the Cramér–Rao bound for unbiased estimators of μ, and determine whether x̄ is efficient.

**Hint ladder, revealed one at a time** `scenes[9].hints[]`

1. Direction — start with the log-density of a single observation and drop every term that has no μ in it. Those terms contribute nothing to any derivative with respect to μ, so carrying them is wasted writing.
2. Method — use I(μ) = −E[∂²ℓ/∂μ²]. Differentiate twice with respect to μ. Something convenient happens: the second derivative has no x in it at all, so the expectation step is trivial.
3. Next step — once you have I(μ), the bound is 1/(nI(μ)). Compare it with Var(X̄), which you already know for a normal sample.

**Model solution, hidden until requested** `scenes[9].solution[]`

1. `scenes[9].solution[0]` Log-density, keeping only μ terms.

   ```
   ℓ(μ) = −(x − μ)² / (2σ²) + constant
   ```

   Laid out:

   $$ℓ(μ) = \frac{−(x − μ)²}{(2σ²) + constant}$$

2. `scenes[9].solution[1]` First derivative — the score.

   ```
   ∂ℓ/∂μ = (x − μ) / σ²
   ```

   Laid out:

   $$\frac{∂ℓ}{∂μ} = \frac{(x − μ)}{σ²}$$

3. `scenes[9].solution[2]` Second derivative.

   ```
   ∂²ℓ/∂μ² = −1/σ²,   free of x
   ```

   Laid out:

   $$\frac{∂²ℓ}{∂μ²} = −\frac{1}{σ²},   free of x$$

4. `scenes[9].solution[3]` Fisher information.

   ```
   I(μ) = −E[ −1/σ² ] = 1/σ²,   so Iₙ(μ) = n/σ²
   ```

   Laid out:

   $$I(μ) = −E[ −\frac{1}{σ²} ] = \frac{1}{σ²},   so Iₙ(μ) = \frac{n}{σ²}$$

5. `scenes[9].solution[4]` The bound.

   ```
   CRLB = 1/Iₙ(μ) = σ²/n
   ```

   Laid out:

   $$CRLB = \frac{1}{Iₙ(μ)} = \frac{σ²}{n}$$

6. `scenes[9].solution[5]` Attainment.

   ```
   Var(X̄) = σ²/n = CRLB  ✓  x̄ is efficient, with e(x̄) = 1
   ```

   Laid out:

   $$Var(X̄) = \frac{σ²}{n} = CRLB  ✓  x̄ is efficient, with e(x̄) = 1$$

**Final answer given to the learner** `scenes[9].answer`

I(μ) = 1/σ², the bound is σ²/n, and x̄ attains it exactly — so x̄ is efficient and is the UMVUE of μ.

**Self-check offered** `scenes[9].check`

Three things were asked and the third is the one candidates drop: say explicitly that the bound is ATTAINED and that x̄ is therefore efficient. Note also that the second derivative contained no x, so the expectation step was free — a useful signal that you have differentiated correctly for a normal mean.

**Optional deep-dive, opened on demand — Dilution of precision is a Fisher information calculation** `scenes[9].scenario`

*teaser on the closed card:* Why a satellite receiver quotes a position accuracy before it has taken a reading.

> A satellite navigation receiver reports a position and, alongside it, a figure for how good that position can be. The figure is available before the fix is computed — it depends on which satellites are visible and where they sit in the sky, not on the measurements themselves.

> That is the Cramér–Rao bound doing its work. The ranging error on each satellite signal enters the likelihood through the geometry of the satellite directions, and the Fisher information for position is built from those directions. Inverting it gives the smallest variance any unbiased position estimate can have, and the square root of the relevant diagonal entry is what the receiver displays.

> The geometry dominates. Satellites spread widely across the sky give an information matrix that is well conditioned and a tight bound; satellites bunched together give a nearly singular one, and the bound blows up in the direction the geometry cannot resolve. This is why accuracy is poor in an urban canyon even when every signal is strong: the bound is set by where the satellites are, not by how clean the signals look.

> The practical consequence is the one the bound is for. A receiver can tell you in advance that no processing will achieve the accuracy you want with the satellites currently in view, so the choice is to wait for the constellation to move or to add another source. That is a planning decision made from the bound alone, before any estimator exists.

*closing line:* The bound is a statement about the experiment, not the estimator — which is why it can be computed before any data arrive.

---

### Scene 11 of 14 — Six statements — verdict on each before you look

`scenes[10]` · id `s10` · type `trapcheck` (true/false check) · 6 minutes

**Purpose** `scenes[10].objective`

Practise the per-statement discipline the real multi-statement items demand.

**Intro** `scenes[10].intro`

Give every statement a true or false verdict first. In the exam these six would be one question scored all or nothing, so a verdict you skipped is a mark you gambled.

- `scenes[10].items[0]` **Claim:** The Cramér–Rao bound applies to every estimator, biased or not, in every family.  
  **Verdict: FALSE.** False twice over. The standard form is for unbiased estimators; a biased one needs the (1 + b′(θ))² numerator. And the whole result requires the regularity conditions, which fail when the support depends on θ.
- `scenes[10].items[1]` **Claim:** If an unbiased estimator attains the bound, it is the UMVUE.  
  **Verdict: TRUE.** True, and it is the quickest route to a UMVUE when it works. Nothing unbiased can be below the floor, so an estimator sitting on it cannot be beaten.
- `scenes[10].items[2]` **Claim:** Every UMVUE attains the Cramér–Rao bound.  
  **Verdict: FALSE.** False — the converse does not hold. For the exponential rate, the UMVUE (n−1)/ΣX has variance λ²/(n−2), strictly above the floor λ²/n.
- `scenes[10].items[3]` **Claim:** For an iid sample, Iₙ(θ) = n·I₁(θ).  
  **Verdict: TRUE.** True. Information is additive over independent observations, which is why the bound carries a 1/n.
- `scenes[10].items[4]` **Claim:** For X₁,…,Xₙ iid U(0,θ), the Cramér–Rao bound gives a valid floor for unbiased estimators of θ.  
  **Verdict: FALSE.** False. The support depends on θ, regularity fails, and the bound does not apply. The UMVUE's variance is θ²/(n(n+2)), of order n⁻², which no 1/n floor could permit.
- `scenes[10].items[5]` **Claim:** Under regularity, −E[∂²ℓ/∂θ²] equals E[(∂ℓ/∂θ)²].  
  **Verdict: TRUE.** True — that equality is the information identity, and it is itself a consequence of being allowed to differentiate under the integral sign.

---

### Scene 12 of 14 — Transfer — a bound for a function of the parameter

`scenes[11]` · id `s11` · type `guided` (guided problem) · 9 minutes

**Purpose** `scenes[11].objective`

Apply the [g′(θ)]² form to a target you met two topics ago.

**Problem put to the learner** `scenes[11].problem`

X₁,…,Xₙ are iid Poisson(λ). In the Rao–Blackwell topic the UMVUE of g(λ) = e^(−λ) came out as ((n−1)/n)^T with T = ΣXᵢ. Find the Cramér–Rao bound for unbiased estimators of e^(−λ), and say whether that UMVUE attains it.

**Hint ladder, revealed one at a time** `scenes[11].hints[]`

1. Direction — the target is not λ, so the standard 1/(nI) form is the wrong one. Identify g(λ), differentiate it, and remember what happens to that derivative in the formula.
2. Method — use Var(T) ≥ [g′(λ)]²/(n I(λ)). You already found I(λ) for the Poisson in scene 6, so only g′ is new work.
3. Next step — for the comparison you need the variance of ((n−1)/n)^T. Use the fact that for T ~ Poisson(nλ) and any constant a, E[a^T] = e^(nλ(a−1)). Apply it once with a and once with a² to get the variance.

**Model solution, hidden until requested** `scenes[11].solution[]`

1. `scenes[11].solution[0]` Identify g and differentiate.

   ```
   g(λ) = e^(−λ),   g′(λ) = −e^(−λ),   [g′(λ)]² = e^(−2λ)
   ```

   Laid out:

   $$g(λ) = e^{−λ},   g′(λ) = −e^{−λ},   [g′(λ)]² = e^{−2λ}$$

2. `scenes[11].solution[1]` Information for the Poisson.

   ```
   I(λ) = 1/λ,  so  n I(λ) = n/λ
   ```

   Laid out:

   $$I(λ) = \frac{1}{λ},  so  n I(λ) = \frac{n}{λ}$$

3. `scenes[11].solution[2]` The bound.

   ```
   CRLB = e^(−2λ) / (n/λ) = λ e^(−2λ) / n
   ```

   Laid out:

   $$CRLB = \frac{e^{−2λ}}{\frac{n}{λ}} = \frac{λ e^{−2λ}}{n}$$

4. `scenes[11].solution[3]` Variance of the UMVUE, writing a = (n−1)/n.

   ```
   E[a^T] = e^(nλ(a−1)) = e^(−λ)  ✓ unbiased.
E[a^(2T)] = e^(nλ(a²−1)) = e^(−2λ + λ/n),   since a² − 1 = (1 − 2n)/n²
   ```

   Laid out:

   $$E[a^{T}] = e^{nλ(a−1)} = e^{−λ}  ✓ unbiased.
E[a^{2T}] = e^{nλ(a²−1)} = e^{−2λ + \frac{λ}{n}},   since a² − 1 = \frac{(1 − 2n)}{n²}$$

5. `scenes[11].solution[4]` Subtract.

   ```
   Var = e^(−2λ + λ/n) − e^(−2λ) = e^(−2λ) ( e^(λ/n) − 1 )
   ```

   Laid out:

   $$Var = e^{−2λ + \frac{λ}{n}} − e^{−2λ} = e^{−2λ} ( e^{\frac{λ}{n}} − 1 )$$

6. `scenes[11].solution[5]` Compare.

   ```
   e^(λ/n) − 1 = λ/n + λ²/(2n²) + …  >  λ/n,
so Var > λe^(−2λ)/n = CRLB, strictly, at every finite n — but the ratio → 1 as n → ∞.
   ```

   Laid out:

   $$e^{\frac{λ}{n}} − 1 = \frac{λ}{n} + \frac{λ²}{(2n²)} + …  >  \frac{λ}{n},
so Var > \frac{λe^{−2λ}}{n} = CRLB, strictly, at every finite n — but the ratio → 1 as n → ∞.$$

**Final answer given to the learner** `scenes[11].answer`

CRLB = λe^(−2λ)/n. The UMVUE has variance e^(−2λ)(e^(λ/n) − 1), which is strictly greater than the bound for every finite n, though the two agree in the limit.

**Self-check offered** `scenes[11].check`

Two traps sat in this one. The numerator is [g′(λ)]² = e^(−2λ), not g′ itself and not 1 — if your bound had no e^(−2λ) in it you used the wrong form. And the conclusion is that the bound is NOT attained, which is a perfectly good answer: being the best unbiased estimator and sitting on the Cramér–Rao floor are different achievements.

---

### Scene 13 of 14 — What you should now be able to do unaided

`scenes[12]` · id `s12` · type `summary` (summary) · 3 minutes

**Purpose** `scenes[12].objective`

Close the loop before the test.

**Body** `scenes[12].body[]`

Compute I(θ) for any standard family by differentiating the log-density twice and taking minus the expectation.

Scale it with Iₙ = nI₁ and write the bound as its reciprocal.

Switch to the [g′(θ)]² numerator the moment the target is a function of θ, and to (1+b′(θ))² when the estimator is biased.

Check the regularity conditions first, and refuse to quote a bound when the support moves with θ.

Settle attainment by testing whether the score is linear in the estimator, rather than by hoping.

Compute efficiency as CRLB/Var, and state the MLE's efficiency as an asymptotic claim, not a finite-sample one.

The mastery test is ten unseen questions across all of this. Hints are off. The pass is 80% overall with 70% floors on the numerical and multi-statement items.

---

### Scene 14 of 14 — Mastery test

`scenes[13]` · id `s13` · type `quiz` (mastery test) · 12 minutes

**Purpose** `scenes[13].objective`

Demonstrate it independently, on unseen questions.

Draws from the pool reproduced below. `scenes[13].setId` = `inference_t6_mastery`

---

## Revision material `revision`

**Revision sheet** `revision.sheet[]` (14 lines)

1. `[0]` Score: U(θ) = ∂ℓ/∂θ.  Under regularity, E[U] = 0.
2. `[1]` Fisher information: I(θ) = Var(U) = E[U²] = −E[∂²ℓ/∂θ²]. The second form is usually the easy one.
3. `[2]` For an iid sample: Iₙ(θ) = n·I₁(θ). Information adds.
4. `[3]` Cramér–Rao, unbiased T for θ:   Var(T) ≥ 1 / (n I(θ)).
5. `[4]` For a function:   Var(T) ≥ [g′(θ)]² / (n I(θ))  when T is unbiased for g(θ).
6. `[5]` Biased T with bias b(θ):   Var(T) ≥ (1 + b′(θ))² / (n I(θ)).
7. `[6]` Attainment: the bound is reached exactly when ∂ℓ/∂θ = A(θ)·[T − g(θ)] — the score is LINEAR in T.
8. `[7]` Efficiency e(T) = CRLB / Var(T). Efficient means e = 1.
9. `[8]` Bernoulli: I(p) = 1/(p(1−p)), CRLB = p(1−p)/n, attained by x̄.
10. `[9]` Poisson: I(λ) = 1/λ, CRLB = λ/n, attained by x̄.
11. `[10]` Normal, σ² known: I(μ) = 1/σ², CRLB = σ²/n, attained by x̄.
12. `[11]` Exponential: I = 1/θ² in BOTH parameterisations, but the bound is attained for the mean θ and NOT for the rate λ.
13. `[12]` Regularity fails when the support depends on θ. For U(0,θ) the UMVUE has variance θ²/(n(n+2)) — order n⁻², faster than any 1/n floor.
14. `[13]` The MLE is asymptotically efficient: Var(θ̂) → 1/(nI(θ)).

**Flashcards** `revision.cards[]`

| Front | Back |
|---|---|
| Fisher information, in words | How sharply the log-likelihood curves at its peak, averaged over samples. Sharp peak, high information, low attainable variance. |
| Two formulas for I(θ) | E[(∂ℓ/∂θ)²] and −E[∂²ℓ/∂θ²]. Equal under regularity; the second derivative is usually less work. |
| Information for n observations | Iₙ(θ) = n·I₁(θ). Independent observations contribute information additively. |
| Cramér–Rao for a function of θ | Var(T) ≥ [g′(θ)]²/(nI(θ)) when T is unbiased for g(θ). Forgetting to square g′ is the standard slip. |
| When is the bound attained? | Exactly when the score factorises as A(θ)[T − g(θ)]. If the score is not linear in T, no unbiased estimator reaches the floor. |
| Where the bound does not apply | When the support depends on θ. U(0,θ) is the standard case, and its UMVUE beats any 1/n bound. |
| Efficiency | e(T) = CRLB/Var(T), between 0 and 1. e = 1 means efficient; the MLE achieves it only in the limit. |
| Same family, different answer | For the exponential, x̄ attains the bound for the mean 1/λ but nothing attains it for the rate λ. Parameterisation matters. |

**Memory aids** `revision.tricks[]`

- `[0]` **Information is curvature** — I(θ) measures how sharply the log-likelihood peaks. Sharp peak → much information → low floor.
- `[1]` **Square the derivative** — For g(θ) the numerator is [g′(θ)]². Dropping the square is the single commonest error in the topic.
- `[2]` **Expected, not observed** — The bound uses −E[∂²ℓ/∂θ²], an average over samples. −∂²ℓ/∂θ² at θ̂ is the observed information — a different number.
- `[3]` **Score linear in T ⇔ bound attained** — ∂ℓ/∂θ = A(θ)[T − g(θ)] is exactly when equality holds. If it refuses to factorise, no unbiased estimator reaches the floor.

**Elimination shortcuts for multiple-choice items** `revision.shortcuts[]`

- `[0]` Bernoulli I(p) = 1/(p(1−p)); Poisson I(λ) = 1/λ; Normal mean I(μ) = 1/σ²; exponential rate I(λ) = 1/λ².
- `[1]` The bound and the total information are reciprocals — if your two numbers do not multiply to 1, one is wrong.
- `[2]` Efficiency = bound ÷ Var(T), so it can never exceed 1. Above 1 means the ratio is upside down.
- `[3]` Biased estimator? The numerator becomes (1 + b′(θ))².

**If nothing else is remembered** `revision.remember[]`

- `[0]` The bound applies to UNBIASED estimators in REGULAR families. Both words matter.
- `[1]` A UMVUE need not attain it — best unbiased and efficient are different achievements.

**Errors to avoid** `revision.traps[]`


---

## Mastery pool — all 20 items with answer keys `qsets/mastery`

Ten are drawn per attempt at 3 easy / 5 moderate / 2 hard. Keys are distributed five to each option letter. Please check each item for a second defensible answer as well as for the correctness of its stated key and explanation.

### Q1 — `inf-t6-m-01` *(single, easy)*

Fisher information for a single observation may be computed as:

*Options* `.options[]`:

- **A.** −E[∂²ℓ/∂θ²], which equals E[(∂ℓ/∂θ)²] under regularity  ← key
- **B.** E[∂ℓ/∂θ], which is non-zero under regularity
- **C.** E[∂²ℓ/∂θ²], which equals Var(∂ℓ/∂θ) always
- **D.** −∂²ℓ/∂θ² evaluated at θ̂

*Explanation* `.explanation`: Both forms in A are standard and agree under regularity. B has the wrong sign and drops the condition. C is the OBSERVED information — a number from one dataset, not the expected information the bound uses. D is wrong on the fact: the score has expectation zero under regularity, which is why its variance is the useful quantity.

### Q2 — `inf-t6-m-02` *(numeric, moderate)*

X₁,…,X₂₅ are iid Bernoulli(p) with p = 0.4. Give the Cramér–Rao bound for unbiased estimators of p, and say whether x̄ attains it.

*Options* `.options[]`:

- **A.** 0.0096, and x̄ does not attain it
- **B.** 0.0096, and x̄ attains it  ← key
- **C.** 0.24, and x̄ attains it
- **D.** 0.24, and x̄ does not attain it

*Explanation* `.explanation`: I(p) = 1/(p(1−p)), so the bound is p(1−p)/n = (0.4)(0.6)/25 = 0.24/25 = 0.0096. And Var(x̄) = p(1−p)/n is exactly that, so x̄ is efficient. Option C forgets to divide by n.

*Arithmetic check* `.check`: Two parts: the number and the attainment verdict. 0.24 is p(1−p) before dividing by n — check the n is in there.

### Q3 — `inf-t6-m-03` *(multi, hard)*

Consider the Cramér–Rao bound and its conditions.

*Statements to judge* `.statements[]`:

- **A.** For T unbiased for g(θ), the bound is [g′(θ)]²/(nI(θ)).
- **B.** For a biased T with bias b(θ), the bound is (1+b′(θ))²/(nI(θ)).
- **C.** Every UMVUE attains the Cramér–Rao bound.
- **D.** The bound requires the support of the density to be free of θ.

*Options* `.options[]`:

- **A.** A and C only
- **B.** B and C only
- **C.** A, B and D only  ← key
- **D.** A, C and D only

*Explanation* `.explanation`: A is true — the squared derivative is the correct numerator for a function of θ. B is true, and is the general form that reduces to the standard one when b ≡ 0. C is false: the converse fails, as the exponential rate shows. D is true, and is why U(0,θ) is excluded.

*Verdict on each statement* `.verdicts`:

- **A — true.** The derivative is squared; forgetting the square is the commonest error in the topic.
- **B — true.** The general form. Setting b ≡ 0 recovers the standard statement.
- **C — false.** The exponential rate's UMVUE has variance λ²/(n−2), strictly above the floor λ²/n.
- **D — true.** A moving support breaks differentiation under the integral, and with it the whole derivation.

### Q4 — `inf-t6-m-04` *(numeric, moderate)*

X₁,…,X₁₆ are iid Poisson(λ) with λ = 4. Give Iₙ(λ) and the Cramér–Rao bound for unbiased estimators of λ.

*Options* `.options[]`:

- **A.** Iₙ = 0.25, bound = 4
- **B.** Iₙ = 64, bound = 0.015625
- **C.** Iₙ = 4, bound = 4
- **D.** Iₙ = 4, bound = 0.25  ← key

*Explanation* `.explanation`: I₁(λ) = 1/λ = 0.25, so Iₙ = n/λ = 16/4 = 4, and the bound is its reciprocal, 1/4 = 0.25. Note Var(x̄) = λ/n = 0.25 too, so x̄ attains it. Option B uses I₁ = λ rather than 1/λ.

*Arithmetic check* `.check`: The bound is the RECIPROCAL of the total information. If your two numbers are not reciprocals of each other, one of them is wrong.

### Q5 — `inf-t6-m-05` *(single, easy)*

For which family does the Cramér–Rao bound fail to apply?

*Options* `.options[]`:

- **A.** U(0,θ), because the support depends on θ  ← key
- **B.** N(μ,σ²) with σ² known, because there are two parameters
- **C.** Poisson(λ), because the data are discrete
- **D.** Bernoulli(p), because p is bounded

*Explanation* `.explanation`: Regularity requires the support to be free of the parameter, and for U(0,θ) it is not — so differentiation under the integral fails and the bound is unavailable. Discreteness is no obstacle (B is wrong; Poisson and Bernoulli are both standard applications), a bounded parameter space is fine provided θ is interior, and in D σ² is known so there is only one unknown parameter.

### Q6 — `inf-t6-m-06` *(numeric, moderate)*

X₁,…,X₃₆ are iid N(μ, σ²) with σ² = 9 known. Give Iₙ(μ) and the Cramér–Rao bound for unbiased estimators of μ.

*Options* `.options[]`:

- **A.** Iₙ = 0.25, bound = 4
- **B.** Iₙ = 4, bound = 0.25  ← key
- **C.** Iₙ = 324, bound = 0.00309
- **D.** Iₙ = 4, bound = 9

*Explanation* `.explanation`: I₁(μ) = 1/σ² = 1/9, so Iₙ = n/σ² = 36/9 = 4 and the bound is 1/4 = 0.25. That equals Var(X̄) = σ²/n = 9/36 = 0.25, so x̄ is efficient. Option C multiplies by σ² instead of dividing.

*Arithmetic check* `.check`: σ² = 9 is the variance, not the standard deviation. I₁ = 1/σ² = 1/9, not 1/3.

### Q7 — `inf-t6-m-07` *(multi, hard)*

Let T be an unbiased estimator of θ in a regular family.

*Statements to judge* `.statements[]`:

- **A.** The MLE attains the Cramér–Rao bound exactly for every sample size.
- **B.** If Var(T) equals the bound, then T is the UMVUE of θ.
- **C.** The bound is attained if and only if the score can be written as A(θ)[T − θ].
- **D.** Efficiency e(T) = CRLB/Var(T) can exceed 1 for a very good estimator.

*Options* `.options[]`:

- **A.** A and B only
- **B.** A, B and C only
- **C.** B and C only  ← key
- **D.** C and D only

*Explanation* `.explanation`: A is false — the MLE's efficiency is an asymptotic statement; at finite n it may be biased and above the floor. B is true, and is the standard shortcut to a UMVUE. C is true, and is the exact attainment criterion. D is false: efficiency is CRLB/Var, which cannot exceed 1.

*Verdict on each statement* `.verdicts`:

- **A — false.** Asymptotic only. Var(θ̂) → 1/(nI(θ)); at finite n it generally sits above.
- **B — true.** Nothing unbiased can be below the floor, so an estimator on it cannot be beaten.
- **C — true.** The linear-score condition is exactly the equality case of the Cauchy–Schwarz step.
- **D — false.** Var(T) ≥ CRLB, so the ratio is at most 1. A value above 1 means an arithmetic error.

### Q8 — `inf-t6-m-08` *(numeric, hard)*

X₁,…,X₁₀ are iid Exponential with rate λ = 2. The UMVUE of λ is (n−1)/ΣX, with variance λ²/(n−2). Give the Cramér–Rao bound and the efficiency of the UMVUE.

*Options* `.options[]`:

- **A.** Bound = 0.5, efficiency = 0.8
- **B.** Bound = 0.4, efficiency = 1.0
- **C.** Bound = 0.5, efficiency = 1.25
- **D.** Bound = 0.4, efficiency = 0.8  ← key

*Explanation* `.explanation`: I(λ) = 1/λ², so the bound is λ²/n = 4/10 = 0.4. The UMVUE's variance is λ²/(n−2) = 4/8 = 0.5. Efficiency is CRLB/Var = 0.4/0.5 = 0.8. The best unbiased estimator is only 80% efficient here, which is the point: a UMVUE need not sit on the floor.

*Arithmetic check* `.check`: Efficiency is bound ÷ variance, so it must come out at or below 1. Option C's 1.25 is the ratio taken upside down.

### Q9 — `inf-t6-m-09` *(numeric, moderate)*

X₁,…,Xₙ are iid Exponential with mean θ, so f(x) = (1/θ)e^(−x/θ). Given I(θ) = 1/θ², give the Cramér–Rao bound for unbiased estimators of θ and say whether x̄ attains it.

*Options* `.options[]`:

- **A.** θ²/n, and x̄ attains it exactly  ← key
- **B.** 1/(nθ²), and x̄ attains it exactly
- **C.** θ/n, and x̄ does not attain it
- **D.** θ²/n, and x̄ does not attain it

*Explanation* `.explanation`: The bound is 1/(nI(θ)) = θ²/n. For this family Var(X) = θ², so Var(X̄) = θ²/n, equal to the bound — x̄ is efficient. Contrast this with the RATE parameterisation of the same family, where nothing unbiased attains the floor: attainability depends on which parameter you are estimating.

*Arithmetic check* `.check`: The bound is the reciprocal of nI(θ), so with I = 1/θ² it is θ²/n and not 1/(nθ²). Writing the reciprocal the wrong way round is the slip option B is built from.

### Q10 — `inf-t6-m-10` *(order, easy)*

To find the Cramér–Rao bound for an unbiased estimator of g(θ), arrange these steps in order.

*Steps to order* `.items[]`:

- A. Compute I₁(θ) = −E[∂²ℓ/∂θ²]
- B. Compare with Var(T) to decide whether the bound is attained
- C. Check that the support does not depend on θ
- D. Form [g′(θ)]² / (n I₁(θ))

*Options* `.options[]`:

- **A.** A, C, D, B
- **B.** C, A, D, B  ← key
- **C.** C, D, A, B
- **D.** A, D, C, B

*Explanation* `.explanation`: Check regularity first — if the support depends on θ there is no bound to compute and everything after is wasted. Then get I₁(θ) from the second derivative, scale to nI₁ and divide [g′(θ)]² by it, and finally compare with the candidate estimator's variance to settle attainment.

### Q11 — `inf-t6-m-11` *(single, easy)*

The Cramér–Rao bound gives a lower bound on:

*Options* `.options[]`:

- **A.** the bias of any estimator of θ
- **B.** the variance of the maximum likelihood estimator only
- **C.** the variance of any unbiased estimator of θ, under regularity conditions  ← key
- **D.** the mean squared error of every estimator, biased or not

*Explanation* `.explanation`: The standard form is a floor on the variance of UNBIASED estimators, and it needs the regularity conditions. A biased estimator has a different bound, with (1+b′(θ))² on top, and its variance can sit below the unbiased floor — which is why the inequality says nothing about every estimator at once.

### Q12 — `inf-t6-m-12` *(numeric, moderate)*

X₁,…,X₅₀ are iid Bernoulli(p) with p = 0.5. Give Iₙ(p) and the Cramér–Rao bound for unbiased estimators of p.

*Options* `.options[]`:

- **A.** Iₙ = 200, bound = 0.25
- **B.** Iₙ = 0.005, bound = 200
- **C.** Iₙ = 12.5, bound = 0.08
- **D.** Iₙ = 200, bound = 0.005  ← key

*Explanation* `.explanation`: I₁(p) = 1/(p(1−p)) = 1/0.25 = 4, so Iₙ = 50(4) = 200 and the bound is 1/200 = 0.005. Check it against Var(x̄) = p(1−p)/n = 0.25/50 = 0.005 — equal, so x̄ is efficient here.

*Arithmetic check* `.check`: The bound and the total information are reciprocals. If the two numbers do not multiply to 1, one of them is wrong.

### Q13 — `inf-t6-m-13` *(multi, hard)*

Consider Fisher information.

*Statements to judge* `.statements[]`:

- **A.** Iₙ(θ) = n I₁(θ) for an iid sample.
- **B.** I(θ) = E[(∂ℓ/∂θ)²] equals −E[∂²ℓ/∂θ²] under regularity.
- **C.** I(θ) is computed by evaluating the second derivative at the MLE.
- **D.** I(θ) must be strictly positive.

*Options* `.options[]`:

- **A.** A, B and D only  ← key
- **B.** A and C only
- **C.** B and C only
- **D.** A, B and C only

*Explanation* `.explanation`: A is true — information adds over independent observations. B is true, and is the identity that makes the second form usable. C is false: I(θ) = −E[∂²ℓ/∂θ²] is the EXPECTED information, a function of θ; evaluating −∂²ℓ/∂θ² at θ̂ gives the OBSERVED information, a number from one dataset. D is true — a zero or negative information signals an algebra error, since I(θ) = Var(score) ≥ 0 and the conditions require it strictly positive.

*Verdict on each statement* `.verdicts`:

- **A — true.** Independence makes the information in the sample the sum of the individual contributions.
- **B — true.** The information identity, itself a consequence of differentiating under the integral.
- **C — false.** That is the OBSERVED information. The bound uses the expected version.
- **D — true.** It is a variance, and the regularity conditions require 0 < I(θ) < ∞.

### Q14 — `inf-t6-m-14` *(numeric, moderate)*

X₁,…,X₉ are iid N(μ, σ²) with σ² = 36 known. An unbiased estimator T of μ has Var(T) = 8. Give the Cramér–Rao bound and the efficiency of T.

*Options* `.options[]`:

- **A.** bound = 4, efficiency = 2
- **B.** bound = 4, efficiency = 0.5  ← key
- **C.** bound = 8, efficiency = 1
- **D.** bound = 0.25, efficiency = 0.03

*Explanation* `.explanation`: I₁(μ) = 1/σ² = 1/36, so Iₙ = 9/36 = 0.25 and the bound is 1/0.25 = 4, which is also σ²/n = 36/9 = 4. Efficiency is CRLB/Var(T) = 4/8 = 0.5, so T carries half the information X̄ does. Option A takes the ratio upside down.

*Arithmetic check* `.check`: Efficiency is bound ÷ variance and can never exceed 1. Any answer above 1 means the ratio was inverted.

### Q15 — `inf-t6-m-15` *(single, moderate)*

An unbiased estimator T of θ is found with Var(T) strictly below 1/(nI(θ)). What has gone wrong?

*Options* `.options[]`:

- **A.** Nothing — T is simply a very good estimator
- **B.** T must be biased after all
- **C.** Either the regularity conditions fail, or there is an arithmetic error — no unbiased estimator can beat the bound where it applies  ← key
- **D.** The Fisher information was computed for the wrong sample size

*Explanation* `.explanation`: Where the conditions hold, the inequality is a theorem: nothing unbiased can sit below the floor. A result below it is evidence that a condition was violated — most often a support that moves with θ — or that the arithmetic is wrong. U(0,θ) is the standard case where quoting the bound produces exactly this contradiction.

### Q16 — `inf-t6-m-16` *(numeric, hard)*

X₁,…,Xₙ are iid Bernoulli(p). Find the Cramér–Rao bound for unbiased estimators of the variance g(p) = p(1−p), and evaluate it at p = 0.4, n = 25.

*Options* `.options[]`:

- **A.** p(1−p)/n = 0.0096
- **B.** (1−2p)²/n = 0.0016
- **C.** (1−2p)p(1−p)/n = 0.00192
- **D.** (1−2p)²p(1−p)/n = 0.000384  ← key

*Explanation* `.explanation`: g′(p) = 1 − 2p, so [g′(p)]² = (1−2p)². With I(p) = 1/(p(1−p)) the bound is [g′(p)]²/(nI(p)) = (1−2p)²p(1−p)/n. At p = 0.4: (0.2)² = 0.04 and p(1−p) = 0.24, so the bound is 0.04 × 0.24/25 = 0.0096/25 = 0.000384. Option A is the bound for p itself rather than for p(1−p); option C drops the square on the derivative.

*Arithmetic check* `.check`: The derivative is SQUARED and the bound is a quotient, not a product. Note also that at p = 0.5 the bound is zero, because g′(0.5) = 0 — the variance is at its maximum there and locally flat.

### Q17 — `inf-t6-m-17` *(multi, moderate)*

Consider efficiency and attainment of the bound.

*Statements to judge* `.statements[]`:

- **A.** e(T) = CRLB/Var(T), and T is efficient when e(T) = 1.
- **B.** Every maximum likelihood estimator is efficient at every sample size.
- **C.** The bound is attained exactly when the score factorises as A(θ)[T − g(θ)].
- **D.** A UMVUE can have variance strictly above the Cramér–Rao bound.

*Options* `.options[]`:

- **A.** A, C and D only  ← key
- **B.** B and C only
- **C.** A, B and C only
- **D.** A and B only

*Explanation* `.explanation`: A is true — efficiency is the ratio of the floor to the achieved variance. B is false: the MLE's efficiency is an asymptotic statement, and at finite n the MLE may be biased and sit above the floor. C is true, and is the exact attainment criterion. D is true — for the exponential rate the UMVUE has variance λ²/(n−2) against a floor of λ²/n.

*Verdict on each statement* `.verdicts`:

- **A — true.** The definition, and the ratio is at most 1.
- **B — false.** Asymptotic only. At finite n the MLE is often biased and above the floor.
- **C — true.** The equality case of the Cauchy–Schwarz step — the score must be linear in T.
- **D — true.** λ²/(n−2) > λ²/n. Best unbiased and efficient are different achievements.

### Q18 — `inf-t6-m-18` *(numeric, moderate)*

X₁,…,X₄₀ are iid Exponential with mean θ = 5. Give the Cramér–Rao bound for unbiased estimators of θ, and the efficiency of x̄.

*Options* `.options[]`:

- **A.** bound = 5, efficiency = 1
- **B.** bound = 0.625, efficiency = 1  ← key
- **C.** bound = 0.625, efficiency = 0.8
- **D.** bound = 0.125, efficiency = 1

*Explanation* `.explanation`: For the mean parameterisation I(θ) = 1/θ², so the bound is θ²/n = 25/40 = 0.625. Var(X̄) = θ²/n = 0.625 as well, so x̄ attains it and its efficiency is exactly 1. The rate parameterisation of the same family behaves differently — there nothing unbiased attains the floor.

*Arithmetic check* `.check`: Attainment depends on which parameter you are estimating, not on the family. For the exponential MEAN it is attained; for the RATE it is not.

### Q19 — `inf-t6-m-19` *(single, easy)*

Which quantity does the Cramér–Rao bound use?

*Options* `.options[]`:

- **A.** the observed information, −∂²ℓ/∂θ² at θ̂
- **B.** the score evaluated at the MLE
- **C.** the expected Fisher information, −E[∂²ℓ/∂θ²]  ← key
- **D.** the second derivative of the likelihood, not the log-likelihood

*Explanation* `.explanation`: The bound is stated with the expected information, an average over all the samples that might have been drawn and a function of θ. The observed information is a single number computed from the data in hand; software often reports it, and questions exploit the difference.

### Q20 — `inf-t6-m-20` *(order, moderate)*

To decide whether an unbiased estimator T of θ is efficient, arrange these steps.

*Steps to order* `.items[]`:

- A. Compute I(θ) and form the bound 1/(nI(θ))
- B. Take the ratio CRLB/Var(T)
- C. Compute Var(T)
- D. Check the regularity conditions hold

*Options* `.options[]`:

- **A.** D, C, A, B
- **B.** A, C, D, B
- **C.** A, D, C, B
- **D.** D, A, C, B  ← key

*Explanation* `.explanation`: Check regularity first — if the support depends on θ there is no bound to compare against and the question is void. Then compute I(θ) and the bound 1/(nI(θ)), then Var(T), and finally take the ratio to get the efficiency.

---

## Authoring and verification record `provenance`

Reproduced verbatim. It records what changed in each version and how each derivation was checked, including the findings of the two previous review rounds and the reasons some of their recommendations were declined.

> Review pass, October 2026: 3 per-scene quick checks added on theory, worked and explore scenes from a third-party module review, each read for correctness before import; a further set offered for completion and guided scenes was declined, since those scenes already end with the learner writing an answer. Theory, worked examples and practice authored for this platform against the UGC NET Statistics syllabus. Previous-year questions are stored separately and carry their exam cycle.

