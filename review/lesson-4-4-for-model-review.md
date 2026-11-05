# Lesson 4.4 — Maximum Likelihood Estimation

Complete authored content of one lesson from a UGC-NET Statistics (Code 107) preparation application, extracted from the application's own content files.

| | |
|---|---|
| Content version | 1.3 |
| Scenes | 15 |
| Core scenes | 15 |
| Optional JRF-extension scenes | 0 |
| Estimated learner time | 46 minutes |
| Mastery pool | 20 items |
| Position in the app | Statistical Inference → Point Estimation → MLE |
| Engine | Estimation and inference — likelihood curves, sampling distributions, visible assumptions |
| Pool label | MLE — mastery test (unseen) |
| Unit | IV — Statistical Inference |
| Audience | JRF-target candidates, many returning after several years away |

## Before you start: where this lesson sits

This lesson is at content version **1.3**. The application's current authoring standard is 4.1, and three of its requirements are **known** to be unmet here, so please do not spend effort reporting them — they are scheduled work, not findings:

- no short "how to use this lesson" note on the overview;
- a quick check on only some teaching scenes rather than all of them;
- no family-to-statistic style reference table where one would help.

This lesson is also **46 minutes against a house standard of about 90**, so it is thinner than intended. Comments on what is MISSING in substance are therefore especially useful — but please flag omissions rather than proposing to shorten what is there.

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

1. Build the likelihood of a sample and say why it is a function of θ, not of x.

2. Derive an MLE through the log-likelihood and the score equation, and verify it is a maximum.

3. Recognise when the derivative method fails and the maximum sits on a boundary.

4. Use invariance to get the MLE of a function of θ without redoing the work.

5. Separate 'maximum likelihood' from 'unbiased', and state the properties the MLE does have.

**Assumed prior knowledge** `prereq[]`

- `prereq[0]` **Joint density of an iid sample** — The likelihood is that joint density, read as a function of θ.
- `prereq[1]` **Differentiating logs and products** — Every MLE derivation turns a product into a sum of logs first.
- `prereq[2]` **Sufficiency and the factorisation theorem** — When an MLE exists and is unique it comes out as a function of the sufficient statistic — a free check on your answer. If the maximiser is not unique, the sufficient statistic determines the whole set of maximisers.

**Misconceptions the lesson is built to pre-empt** `traps[]`

- Writing L(θ) and then differentiating with respect to x.

- Maximising L instead of ℓ, and drowning in the product rule.

- Setting the derivative to zero when the support depends on θ.

- Forgetting the second-order check, so a minimum or a stationary point is reported as the MLE.

- Re-deriving from scratch for g(θ) when invariance gives it in one line.

- Assuming the MLE is unbiased, or that it must equal the UMVUE.

- Dividing by n−1 in σ̂² because that is the formula you have written a hundred times.

**Assessment policy** `mastery`

- 10 items drawn per attempt from a pool of 20, mix 3 easy, 5 moderate, 2 hard
- pass mark 80%, no hints during the test, retest after 7 days
- `mastery.note`: Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the difficulty mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split.

**Sources** `refs[]`

- `refs[0]` **Maximum Likelihood Estimation** — Penn State STAT 415 online notes, Lesson 1.2 (Course notes, free). The cleanest written derivation of the Bernoulli and Normal MLEs, step by step. Read it after scene 4 if the algebra still feels fast.
- `refs[1]` **Maximum likelihood estimation — theory, assumptions, properties** — StatLect, Sections: the sample and its likelihood; the score; information matrix; consistency; asymptotic normality (Reference, free). Where to go for the regularity conditions and the asymptotic results stated precisely. This is the source for scene 7, not the intuition scenes.
- `refs[2]` **Statistics for Applications — Maximum Likelihood Estimation** — MIT OpenCourseWare 18.650 (Fall 2016), Lecture slides, sessions 4–5 (Lecture slides, free). Treats the MLE as minimising KL divergence — the view that makes consistency obvious rather than a result to memorise.

---

## The lesson, scene by scene

### Scene 1 of 15 — Before the lesson — four things it will assume

`scenes[0]` · id `s0` · type `foundation` (prerequisite check) · 6 minutes

**Purpose** `scenes[0].objective`

Confirm that writing a likelihood, logging it and differentiating it are automatic before the derivations begin.

**Body** `scenes[0].body[]`

Maximum likelihood is a short topic with a long tail of arithmetic. Everything in it reduces to: write L(θ), take logs, differentiate, set to zero. If any one of those four steps is slow, every derivation in the lesson will feel like three topics at once.

After a two or three year gap it is usually the differentiating that has gone quiet, not the idea. Four checks, five minutes. Mark anything shaky and read the rebuild before you move on.

**Check 1** `scenes[0].items[0]`

- *asks:* For an iid sample, what is the likelihood L(θ), and how does it differ from the joint density?
- *expected answer* `.recall`: L(θ) = ∏ᵢ₌₁ⁿ f(xᵢ;θ). It is exactly the joint density — the same expression, not an approximation of it. The only difference is which symbol you treat as fixed: the density holds θ fixed and varies x, the likelihood holds the observed x fixed and varies θ.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Independence makes the joint density a product; identical distribution makes every factor the same f. So the joint density of the sample is ∏f(xᵢ;θ).

> Now the data have arrived and are numbers. The only unknown left is θ, so read the same expression as a function of θ and call it L(θ). That re-reading is the entire conceptual content of the word 'likelihood'.

> It is not a probability of θ. L(θ) does not integrate to one over θ, and nothing in this course lets you say 'the probability that θ = 3'. It is a comparison: L(3) > L(5) says the observed data were more probable under 3 than under 5.

**Check 2** `scenes[0].items[1]`

- *asks:* Differentiate a log-likelihood. Which two rules do you need?
- *expected answer* `.recall`: log of a product is a sum of logs, so the derivative of the whole is the sum of the derivatives; and d/dθ log g(θ) = g′(θ)/g(θ). Those two turn any product likelihood into a manageable sum.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Work one all the way through. Exponential with rate λ: f(x;λ) = λe^(−λx), so L(λ) = λⁿ e^(−λΣxᵢ).

> Take logs: ℓ(λ) = n log λ − λΣxᵢ. The product became a sum, and the exponential became linear — that is why you log first and always.

> Differentiate: ℓ′(λ) = n/λ − Σxᵢ. Set it to zero: λ̂ = n/Σxᵢ = 1/x̄. Then check it is a maximum: ℓ″(λ) = −n/λ², negative for every λ > 0, so the stationary point is the maximum. Do not skip that check in the exam — some questions are set precisely where it fails.

**Check 3** `scenes[0].items[2]`

- *asks:* Why is maximising log L the same as maximising L?
- *expected answer* `.recall`: log is strictly increasing, so it preserves order: if L(θ₁) > L(θ₂) then log L(θ₁) > log L(θ₂). The maximising θ is therefore identical. The maximum value is not the same, but nobody asked for it.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> A strictly increasing transformation cannot change which input is largest — it only relabels the heights. So the argmax survives, and taking logs is free.

> This is also why the MLE of a function of θ is that function of the MLE when the function is one-to-one: if θ̂ maximises the likelihood in θ, then g(θ̂) maximises it in g(θ). That is the invariance property, and the lesson uses it from the worked examples onwards.

**Check 4** `scenes[0].items[3]`

- *asks:* What does the factorisation theorem say, and why is it a free check on any MLE you compute?
- *expected answer* `.recall`: If f(x;θ) = g(T(x);θ)·h(x) with h free of θ, then T is sufficient for θ. The MLE maximises g(T;θ), since h contributes no θ — so an MLE that exists and is unique is a function of a sufficient statistic — and if the maximiser is not unique, the sufficient statistic still determines the set of maximisers.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Split the joint density into the part that involves θ and the part that does not. Whatever function of the data appears in the θ-part is a sufficient statistic.

> The consequence is a check you can apply in ten seconds. For a Poisson sample the joint density is e^(−nθ)θ^(Σxᵢ)/∏xᵢ!, so Σxᵢ is sufficient — and the MLE must be a function of Σxᵢ. It is: θ̂ = x̄.

> If your derivation ever produces an estimator that depends on the data in some way the sufficient statistic does not capture — the median, say, when the sufficient statistic is Σxᵢ — you have made an algebra slip. Go back rather than trusting it.

---

### Scene 2 of 15 — Which rate makes what you saw most plausible?

`scenes[1]` · id `s1` · type `intuition` (intuition) · 4 minutes

**Purpose** `scenes[1].objective`

See the likelihood as the density read backwards.

**Body** `scenes[1].body[]`

Two bulbs from the same batch failed at 3 hours and at 9 hours. The batch is modelled as exponential with failure rate λ. You do not know λ. You have to name a number.

Try λ = 0.02. Under that rate, failures at 3 and 9 hours would be startlingly early — the model expects a bulb to last about 50 hours. The data you got would be a surprise.

Try λ = 2. Now the model expects failure in about half an hour, and lasting 9 hours would be a freak event. Again the data you got would be a surprise.

Somewhere between those, there is a rate under which the two failures you actually saw are as unsurprising as they can be. That value is the maximum likelihood estimate. The whole method is this one idea, written in algebra.

The formula does not change — it is the same exponential density. What changes is which symbol you treat as fixed. In probability, θ is fixed and x varies. In likelihood, x is fixed at what you observed and θ varies. That inversion is the entire conceptual content of this topic.

**Aside — The sentence that stops the commonest error** `scenes[1].aside.body`

L(θ) is not the probability that θ is correct. It is the probability of your data, computed under θ. It does not integrate to one over θ, and it is not a distribution for θ. That is Bayesian territory and needs a prior.

**Quick check before moving on** `scenes[1].ask`

- *question:* Why can the best estimate not be a fixed number that ignores which sample you got?
- *hint on request:* What are you choosing θ to do? Think about what the criterion is measured against.

**Optional deep-dive, opened on demand — The German tank problem** `scenes[1].scenario`

*teaser on the closed card:* In 1942 the Allies estimated German tank production from the serial numbers on captured gearboxes.

> Allied intelligence needed to know how many tanks Germany was building. Estimates assembled from agent reports and aerial reconnaissance put output in the region of 1,000 to 1,550 a month.

> Statisticians took a different route. Captured and destroyed tanks carried sequentially numbered components — gearboxes, wheels, engines. If serial numbers run 1 to N and the captured ones are effectively a random sample, then N is the upper endpoint of a discrete uniform distribution and the serial numbers are the data.

> The maximum likelihood estimate is immediate, and it is exactly the case where differentiating gets you nowhere: the likelihood is zero for any N below the largest serial observed and decreasing above it, so N̂ is the largest serial number seen. It is also obviously biased — it can never exceed the truth and almost always falls short.

> The correction is the same one U(0,θ) needs. With k observations and maximum m, the minimum-variance unbiased estimate is m + m/k − 1: push the maximum up by roughly one average gap. For a sample of 10 with a largest serial of 1,200 that gives 1,200 + 120 − 1 = 1,319.

> Post-war records settled it. For August 1942 the statistical estimate was 327 tanks a month against a true figure of 342 — about 4% out. The intelligence estimate for the same month was 1,550, roughly four and a half times the truth. June 1941 went the same way: 244 estimated against 271 actual, while intelligence said 1,550. The method was not flawless — June 1940 gave 169 against an actual 122 — but it was wrong by tens where the conventional estimates were wrong by thousands.

> The whole argument is two topics of this syllabus: a boundary MLE from this lesson, and its bias correction from Rao–Blackwell and Lehmann–Scheffé.

*think-it-through question* `.q`: Why is the estimate so much better than the intelligence figure, given that it uses far less information?

*what the statistics says* `.answer`: Because it uses the right information. The sample maximum is sufficient for N: once you know the largest serial number, the others add nothing about N, so a handful of captured tanks carries nearly all the information a much larger sample would. Agent reports, by contrast, carry an unknown and probably non-zero bias that more reports do not remove. A small sample read through the correct model beats a large body of evidence read through the wrong one.

*link line* `.link`: Figures from the documented wartime comparison of statistical and intelligence estimates. The identical estimator is used today to size populations from sequential identifiers — for instance estimating total units produced from serial numbers on a sample of warranty returns.

---

### Scene 3 of 15 — Move the rate and watch the data become plausible

`scenes[2]` · id `s2` · type `explore` (interactive visualisation) · 5 minutes

**Purpose** `scenes[2].objective`

Locate the peak yourself before being shown the formula for it.

**Body** `scenes[2].body[]`

The curve is L(λ) = λⁿ e^(−λΣxᵢ) for an exponential sample — the likelihood of the data you actually hold, at every candidate rate.

Below it is ℓ(λ) = n·log λ − λ·Σxᵢ. Same peak, in the same place, because log is strictly increasing. It is far easier to differentiate.

Start with n = 2 and Σx = 12, which is the two bulbs. Drag λ and find the top by eye. Then raise n and watch what happens to the width of the curve, not just its position.

**Interactive element** `scenes[2].viz` — live plot of type `exp-likelihood`, initial state n=2, sumx=12.0. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[2].ask`

- *question:* Double every observation, so Σx goes from 12 to 24 with n unchanged. Which way does the peak move, and why does that make sense physically?
- *hint on request:* Longer lifetimes mean what about the failure rate?

---

### Scene 4 of 15 — The three lines that do all the work

`scenes[3]` · id `s3` · type `theory` (theory) · 6 minutes

**Purpose** `scenes[3].objective`

Write the standard derivation in its canonical order.

**Block 1 — Likelihood** `scenes[3].blocks[0]` *(type `def`)*

For an iid sample x₁,…,xₙ from f(x; θ), the likelihood is L(θ) = ∏ᵢ f(xᵢ; θ), viewed as a function of θ with the data held fixed.

**Block 2 — Step 1 — take logs** `scenes[3].blocks[1]` *(type `formula`)*

ℓ(θ) = log L(θ) = Σᵢ log f(xᵢ; θ)

**Block 3 — Step 2 — the score equation** `scenes[3].blocks[2]` *(type `formula`)*

∂ℓ/∂θ = 0,   solved for θ

**Block 4 — Step 3 — confirm it is a maximum** `scenes[3].blocks[3]` *(type `formula`)*

∂²ℓ/∂θ² < 0  evaluated at the root

**Block 5 — The condition that decides whether any of this applies** `scenes[3].blocks[4]` *(type `assume`)*

The support of f must not depend on θ. If the set of possible x values moves when θ moves, ℓ has a jump and the derivative never reaches zero at the maximum. Scene 9 shows exactly that happening.

**Block 6 — Why step 3 is not optional** `scenes[3].blocks[5]` *(type `note`)*

∂ℓ/∂θ = 0 finds stationary points. For the standard one-parameter families the root is the maximum and the check is one line, but examiners do set items where the stationary point is a minimum or where the maximum is at an endpoint. Writing the second derivative costs you five seconds.

**Block 7 — The error that costs a mark without feeling like an error** `scenes[3].blocks[6]` *(type `trap`)*

Differentiating with respect to x instead of θ. By the time you have written ℓ(θ) your variable is θ. The xᵢ are now constants.

**Flow diagram** `scenes[3].flow` — Finding an MLE — and knowing when not to differentiate

*alt text* `.alt`: Decision chart for maximum likelihood estimation

- row 1: Write the likelihood L(θ) for the observed sample
- row 2: Does the SUPPORT depend on θ?
- row 3: Do not differentiate — inspect where L is positive  |  Take logs, then solve ∂ℓ/∂θ = 0
- row 4: Maximum sits at a boundary, e.g. θ̂ = x₍ₙ₎  |  Check ∂²ℓ/∂θ² < 0 at the solution
- row 5: θ̂ is the MLE
- row 6: Asked for g(θ)? By invariance the answer is g(θ̂)
- arrows: Write the likelihood L(θ) for the observed sample → Does the SUPPORT depend on θ?; Does the SUPPORT depend on θ? → [yes] Do not differentiate — inspect where L is positive; Does the SUPPORT depend on θ? → [no] Take logs, then solve ∂ℓ/∂θ = 0; Do not differentiate — inspect where L is positive → Maximum sits at a boundary, e.g. θ̂ = x₍ₙ₎; Take logs, then solve ∂ℓ/∂θ = 0 → Check ∂²ℓ/∂θ² < 0 at the solution; Maximum sits at a boundary, e.g. θ̂ = x₍ₙ₎ → θ̂ is the MLE; Check ∂²ℓ/∂θ² < 0 at the solution → [yes] θ̂ is the MLE; θ̂ is the MLE → Asked for g(θ)? By invariance the answer is g(θ̂)

*note shown under the diagram* `.note`: The left branch is where marks are lost. For U(0,θ) the derivative of the log-likelihood is never zero, so setting it to zero finds nothing at all — the maximum is at the edge of the support.

**Quick check before moving on** `scenes[3].ask`

- *question:* When you differentiate the log-likelihood, what must you check before accepting a stationary point as the MLE?
- *hint on request:* Check the parameter space, boundary points, and whether the point is a maximum rather than a minimum.

---

### Scene 5 of 15 — Worked in full — the exponential rate

`scenes[4]` · id `s4` · type `worked` (worked example) · 5 minutes

**Purpose** `scenes[4].objective`

See the canonical derivation with reasoning at every step.

**Problem put to the learner** `scenes[4].problem`

X₁,…,Xₙ are iid Exponential with rate λ, so f(x; λ) = λe^(−λx) for x > 0. Find the MLE of λ.

**Worked steps** `scenes[4].steps[]`

1. `scenes[4].steps[0]` Write the likelihood as the product of densities.

   ```
   L(λ) = ∏ᵢ λe^(−λxᵢ) = λⁿ e^(−λΣxᵢ)
   ```

   Laid out:

   $$L(λ) = ∏ᵢ λe^{−λxᵢ} = λⁿ e^{−λΣxᵢ}$$

   *why* `.why`: The product collapses because each factor carries one λ and the exponents add. Already you can see the likelihood depends on the data only through Σxᵢ — that is the sufficient statistic announcing itself.

2. `scenes[4].steps[1]` Take logs.

   ```
   ℓ(λ) = n·log λ − λ·Σxᵢ
   ```

   *why* `.why`: A sum instead of a product. Nothing is lost: log is strictly increasing, so whatever maximises ℓ maximises L.

3. `scenes[4].steps[2]` Differentiate with respect to λ and set to zero.

   ```
   dℓ/dλ = n/λ − Σxᵢ = 0
   ```

   Laid out:

   $$\frac{dℓ}{dλ} = \frac{n}{λ} − Σxᵢ = 0$$

   *why* `.why`: The xᵢ are constants here. The only variable is λ.

4. `scenes[4].steps[3]` Solve.

   ```
   λ̂ = n / Σxᵢ = 1 / x̄
   ```

   Laid out:

   $$λ̂ = \frac{n}{Σxᵢ} = \frac{1}{x̄}$$

   *why* `.why`: The reciprocal of the sample mean. Sensible: the exponential mean is 1/λ, so estimating the mean by x̄ and inverting gives the same answer — which is invariance, arriving early.

5. `scenes[4].steps[4]` Check it is a maximum.

   ```
   d²ℓ/dλ² = −n/λ² < 0 for all λ > 0
   ```

   Laid out:

   $$\frac{d²ℓ}{dλ²} = −\frac{n}{λ²} < 0 for all λ > 0$$

   *why* `.why`: Negative everywhere, so ℓ is strictly concave and the stationary point is the global maximum. One line, done.

6. `scenes[4].steps[5]` Put the numbers in.

   ```
   n = 2, Σxᵢ = 12  ⟹  λ̂ = 2/12 = 0.167 per hour
   ```

   Laid out:

   $$n = 2, Σxᵢ = 12  ⟹  λ̂ = \frac{2}{12} = 0.167 per hour$$

   *why* `.why`: This is the peak you found by dragging the slider in scene 2. The algebra and the picture agree.

**What to take from it** `scenes[4].after`

Notice what the derivation never needed: any claim that λ̂ is unbiased, or best, or anything else. Maximum likelihood is a recipe for producing an estimator. Whether that estimator is any good is a separate question, and scene 8 shows it is not always.

**Quick check before moving on** `scenes[4].ask`

- *question:* For an exponential sample, how do you distinguish the rate parameterisation from the scale parameterisation when finding the MLE?
- *hint on request:* Write the exact density first; rate and scale are reciprocals and lead to different-looking likelihoods.

---

### Scene 6 of 15 — Pause and recall

`scenes[5]` · id `s5` · type `recall` (retrieval practice) · 2 minutes

**Purpose** `scenes[5].objective`

Retrieve before reading on — this is where the retention comes from.

**Intro** `scenes[5].intro`

Answer each in your head, then reveal. Retrieving an answer wrongly and correcting it beats reading the right answer twice.

- `scenes[5].items[0]` **Q:** In L(θ), which symbol varies and which is held fixed?  
  **A:** θ varies. The data x₁,…,xₙ are fixed at the values you observed.
- `scenes[5].items[1]` **Q:** Why maximise ℓ rather than L?  
  **A:** log turns the product into a sum, and because log is strictly increasing the maximiser is unchanged.
- `scenes[5].items[2]` **Q:** What is the one condition that decides whether the score equation is the right tool at all?  
  **A:** The support of f must not depend on θ.
- `scenes[5].items[3]` **Q:** Write the MLE of the exponential rate from memory.  
  **A:** λ̂ = n/Σxᵢ = 1/x̄.

---

### Scene 7 of 15 — Your turn, with the scaffolding partly removed — Bernoulli

`scenes[6]` · id `s6` · type `completion` (fill in the blanks) · 6 minutes

**Purpose** `scenes[6].objective`

Supply the steps yourself rather than following them.

**Problem put to the learner** `scenes[6].problem`

X₁,…,Xₙ are iid Bernoulli(p), so f(x; p) = p^x (1−p)^(1−x) for x ∈ {0,1}. Let k = Σxᵢ be the number of successes. Find the MLE of p.

**Worked steps** `scenes[6].steps[]`

1. `scenes[6].steps[0]` The likelihood.

   ```
   L(p) = p^k (1−p)^(n−k)
   ```

   Laid out:

   $$L(p) = p^{k} (1−p)^{n−k}$$

   *why* `.why`: Each success contributes p, each failure contributes (1−p).

2. `scenes[6].steps[1]` Take logs.

   - *learner is asked:* Write ℓ(p).
   - *accepted answer* `.blank.answer`: k log p + (n−k) log(1−p)
   - *also accepted:* k log p + (n-k) log(1-p); klogp+(n-k)log(1-p); k ln p + (n-k) ln(1-p)
   - *hint:* log of a product is a sum of logs; log of a power brings the exponent down.

   *why* `.why`: Two terms, one for the successes and one for the failures.

3. `scenes[6].steps[2]` Differentiate with respect to p and set to zero.

   - *learner is asked:* Write dℓ/dp = 0.
   - *accepted answer* `.blank.answer`: k/p − (n−k)/(1−p) = 0
   - *also accepted:* k/p - (n-k)/(1-p) = 0; k/p-(n-k)/(1-p)=0; k/p = (n-k)/(1-p)
   - *hint:* d/dp log(1−p) = −1/(1−p). Mind that minus sign — it is the single commonest slip here.

   *why* `.why`: The chain rule on the second term supplies the minus sign.

4. `scenes[6].steps[3]` Solve for p.

   - *learner is asked:* Write p̂.
   - *accepted answer* `.blank.answer`: k/n
   - *also accepted:* k/n; x̄; xbar; k / n; the sample proportion
   - *hint:* Cross-multiply: k(1−p) = (n−k)p. Expand and the kp terms cancel.

   *why* `.why`: The sample proportion — which is also x̄, so the Bernoulli MLE is the sample mean.

5. `scenes[6].steps[4]` Check.

   ```
   d²ℓ/dp² = −k/p² − (n−k)/(1−p)² < 0
   ```

   Laid out:

   $$\frac{d²ℓ}{dp²} = −\frac{k}{p²} − \frac{(n−k)}{(1−p)²} < 0$$

   *why* `.why`: Negative for every p in (0,1), so the stationary point is the maximum.

**What to take from it** `scenes[6].after`

Two derivations, identical shape: product → log → differentiate → solve → check. The shape is what you are memorising, not the individual answers.

---

### Scene 8 of 15 — The four properties the exam actually tests

`scenes[7]` · id `s7` · type `theory` (theory) · 7 minutes

**Purpose** `scenes[7].objective`

Hold the properties with their conditions attached, because the conditions are what the items test.

**Block 1 — 1. Invariance** `scenes[7].blocks[0]` *(type `def`)*

If θ̂ is the MLE of θ, then g(θ̂) is the MLE of g(θ), for any function g. No regularity conditions, no second derivation. If λ̂ = 1/x̄ then the MLE of the mean 1/λ is x̄, and the MLE of λ² is 1/x̄².

**Block 2 — 2. It is a function of the sufficient statistic** `scenes[7].blocks[1]` *(type `def`)*

The factorisation theorem writes L(θ) = g(T(x); θ)·h(x). Maximising over θ only ever touches g, so the maximiser depends on the data only through T. Use this as a free check: if your answer is not a function of the sufficient statistic, you have made an algebra mistake.

**Block 3 — 3. Consistency and asymptotic normality** `scenes[7].blocks[2]` *(type `def`)*

Under regularity conditions, θ̂ →ᵖ θ, and √n(θ̂ − θ) →ᵈ N(0, 1/I(θ)) — equivalently θ̂ is approximately N(θ, 1/(nI(θ))) for large n. So the MLE attains the Cramér–Rao bound asymptotically, which is the precise sense in which it is 'efficient'.

**Block 4 — Which regularity conditions** `scenes[7].blocks[3]` *(type `assume`)*

The support does not depend on θ; θ is interior to the parameter space; ℓ is twice differentiable; differentiation and integration can be interchanged; the information I(θ) is finite and positive. U(0,θ) violates the first, which is why the usual asymptotics do not apply there.

**Block 5 — 4. It is NOT generally unbiased** `scenes[7].blocks[4]` *(type `trap`)*

This is the property examiners most often test by implication. Maximum likelihood optimises plausibility of the data, not expected value of the estimator. For N(μ,σ²) the MLE σ̂² = Σ(xᵢ−x̄)²/n has E[σ̂²] = (n−1)σ²/n — biased low. For the exponential rate, E[λ̂] = nλ/(n−1) — biased high. Both biases vanish as n grows, which is consistency, not unbiasedness.

**Block 6 — MLE versus UMVUE** `scenes[7].blocks[5]` *(type `note`)*

They coincide often enough to be dangerous. They are different objects: the MLE maximises the likelihood, the UMVUE minimises variance among unbiased estimators. When a question offers both as options, decide which criterion it named.

**Quick check before moving on** `scenes[7].ask`

- *question:* Why does consistency not imply unbiasedness, and why does unbiasedness not imply minimum variance?
- *hint on request:* These are distinct properties: limiting behaviour, expectation at fixed n, and variance comparisons answer different questions.

---

### Scene 9 of 15 — Watch the MLE be biased, then watch the bias die

`scenes[8]` · id `s8` · type `explore` (interactive visualisation) · 5 minutes

**Purpose** `scenes[8].objective`

Turn 'the MLE is not unbiased' from a sentence into something you have seen.

**Body** `scenes[8].body[]`

This is the exact sampling distribution of λ̂ = n/ΣX for an exponential sample — not a simulation. ΣX is Gamma(n, λ), so λ̂ has a known density and the curve is drawn from it.

The solid line is the true λ. The dashed line is E[λ̂] = nλ/(n−1). At n = 2 the estimator is biased by a full 100%: it expects to return twice the truth. At n = 3 it is 50% high. At n = 20, about 5%.

Notice two things moving at once as you raise n: the dashed line slides toward the solid one — that is the bias dying — and the whole distribution narrows — that is the variance dying. Both together are consistency.

Also notice the shape. Even at moderate n the distribution is visibly right-skewed, not the symmetric normal the asymptotic theory promises. 'Asymptotically normal' means eventually, and the exam has asked which sample size makes that approximation reasonable.

**Interactive element** `scenes[8].viz` — live plot of type `mle-sampling`, initial state lam=0.5, n=3. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[8].ask`

- *question:* The bias is nλ/(n−1) − λ = λ/(n−1). An estimator whose bias goes to zero is called asymptotically unbiased. Is every consistent estimator asymptotically unbiased, or are those two different claims?
- *hint on request:* Consistency is about convergence in probability. Bias is about an expectation. Can an expectation be dragged around by a vanishingly rare but enormous value?

---

### Scene 10 of 15 — Where calculus fails — the uniform

`scenes[9]` · id `s9` · type `explore` (interactive visualisation) · 5 minutes

**Purpose** `scenes[9].objective`

Recognise the boundary case on sight, because the derivative will not warn you.

**Body** `scenes[9].body[]`

X₁,…,Xₙ are iid U(0, θ). The density is 1/θ on [0, θ] and zero outside, so the likelihood is L(θ) = θ^(−n), but only for θ ≥ x₍ₙ₎, the largest observation. For any smaller θ at least one observed value would have been impossible, so L(θ) = 0.

That gives the shape on screen: flat zero, a vertical cliff at x₍ₙ₎, then a curve decreasing for the rest of its life.

Set the derivative to zero and you get −n·θ^(−n−1) = 0, which has no solution. The derivative is negative everywhere the likelihood is positive. Nothing is wrong with your algebra — the method simply does not apply, because the support depends on θ.

The maximum is at the cliff edge: θ̂ = x₍ₙ₎, the sample maximum. Read it off the picture, not off a derivative.

This estimator is biased low — it can never exceed the true θ, and almost surely falls short, with E[θ̂] = nθ/(n+1). The unbiased correction is (n+1)/n · x₍ₙ₎, which is not the MLE.

**Interactive element** `scenes[9].viz` — live plot of type `unif-likelihood`, initial state n=5, xmax=4.2. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[9].ask`

- *question:* Drag θ below the cliff. Why is the likelihood exactly zero there rather than merely small?
- *hint on request:* What would θ < x₍ₙ₎ say about the value you actually observed?

**Optional deep-dive, opened on demand — Fitting lifetimes when most units have not failed yet** `scenes[9].scenario`

*teaser on the closed card:* Why reliability software fits a Weibull by likelihood and not by least squares.

> A reliability engineer has 400 units on test. Sixty have failed; the rest are still running when the test is stopped. The problem is not the sixty — it is the 340, each of which says 'longer than this', and a method that ignores them will make the product look far worse than it is.

> Maximum likelihood handles that in one line of bookkeeping. A failure at time t contributes its density f(t;θ); a unit still running at time t contributes its survival probability 1 − F(t;θ). The likelihood is the product of both kinds of term, and nothing else about the method changes. A least-squares fit to a probability plot has no natural way to carry the second kind of term, which is why the standard reliability packages fit by likelihood.

> Then invariance does the second half of the work. The quantity a warranty department actually wants is rarely a parameter: it is B10 life, the time by which 10% of units have failed, or the probability of surviving the warranty period. Each is a function of the fitted parameters, and the MLE of a function is that function of the MLE — so the answer comes straight out of the fit with no new estimation.

> What the method does not give you for free is a sanity check, and the checks are where the marks and the money both are. A shape parameter below 1 says the failure rate is decreasing — infant mortality, a manufacturing problem — while a shape above 1 says wear-out. Reporting a B10 life from a fit whose shape parameter contradicts the physics is the usual way this goes wrong in practice.

*closing line:* Censored data are the ordinary case, not the exception, and the likelihood is the estimator that takes them in its stride.

---

### Scene 11 of 15 — Now without the steps — Poisson

`scenes[10]` · id `s10` · type `guided` (guided problem) · 6 minutes

**Purpose** `scenes[10].objective`

Select the method yourself. The hints are there, and using them is recorded.

**Problem put to the learner** `scenes[10].problem`

X₁,…,Xₙ are iid Poisson(λ), so P(X = x) = e^(−λ) λ^x / x! for x = 0,1,2,…  A sample of n = 8 gives Σxᵢ = 20. Find the MLE of λ, and then the MLE of P(X = 0).

**Hint ladder, revealed one at a time** `scenes[10].hints[]`

1. Direction — before any algebra, ask which quantity you are choosing. You are choosing λ to make Σxᵢ = 20 as plausible as it can be. Write the likelihood as a product over i and see what survives.
2. Method — the support {0,1,2,…} does not depend on λ, so the score equation is the right tool. Take logs: the x! becomes an additive constant that does not involve λ, so it will vanish on differentiation. Do not waste time on it.
3. Next step — ℓ(λ) = −nλ + (Σxᵢ)·log λ − Σ log(xᵢ!). Differentiate with respect to λ, set to zero, and solve. Then for the second part do not start again: use invariance.

**Model solution, hidden until requested** `scenes[10].solution[]`

1. `scenes[10].solution[0]` Likelihood.

   ```
   L(λ) = ∏ e^(−λ) λ^(xᵢ)/xᵢ! = e^(−nλ) λ^(Σxᵢ) / ∏xᵢ!
   ```

   Laid out:

   $$L(λ) = ∏ e^{−λ} \frac{λ^{xᵢ}}{xᵢ!} = \frac{e^{−nλ} λ^{Σxᵢ}}{∏xᵢ!}$$

2. `scenes[10].solution[1]` Log-likelihood, dropping the constant.

   ```
   ℓ(λ) = −nλ + (Σxᵢ) log λ − Σ log(xᵢ!)
   ```

3. `scenes[10].solution[2]` Score equation.

   ```
   dℓ/dλ = −n + (Σxᵢ)/λ = 0
   ```

   Laid out:

   $$\frac{dℓ}{dλ} = −n + \frac{(Σxᵢ)}{λ} = 0$$

4. `scenes[10].solution[3]` Solve.

   ```
   λ̂ = Σxᵢ / n = x̄ = 20/8 = 2.5
   ```

   Laid out:

   $$λ̂ = \frac{Σxᵢ}{n} = x̄ = \frac{20}{8} = 2.5$$

5. `scenes[10].solution[4]` Check.

   ```
   d²ℓ/dλ² = −(Σxᵢ)/λ² < 0  ✓
   ```

   Laid out:

   $$\frac{d²ℓ}{dλ²} = −\frac{(Σxᵢ)}{λ²} < 0  ✓$$

6. `scenes[10].solution[5]` Second part, by invariance.

   ```
   P(X=0) = e^(−λ), so its MLE is e^(−λ̂) = e^(−2.5) = 0.0821
   ```

   Laid out:

   $$P(X=0) = e^{−λ}, so its MLE is e^{−λ̂} = e^{−2.5} = 0.0821$$

**Final answer given to the learner** `scenes[10].answer`

λ̂ = 2.5 and the MLE of P(X=0) is e^(−2.5) ≈ 0.0821

**Self-check offered** `scenes[10].check`

The question asked for two quantities. Reporting only λ̂ = 2.5 is the single likeliest way to lose this mark — it is right working, wrong quantity.

---

### Scene 12 of 15 — Six statements — verdict on each before you look

`scenes[11]` · id `s11` · type `trapcheck` (true/false check) · 5 minutes

**Purpose** `scenes[11].objective`

Practise the per-statement discipline that multi-statement items demand.

**Intro** `scenes[11].intro`

Give every statement a true or false verdict first. Multi-statement items in the real paper are scored on the whole set, so a verdict you skipped is a mark you gambled.

- `scenes[11].items[0]` **Claim:** If θ̂ is the MLE of θ, then θ̂² is the MLE of θ².  
  **Verdict: TRUE.** Invariance, with no conditions attached. This one is true and is often placed among false statements to catch people who distrust it.
- `scenes[11].items[1]` **Claim:** The MLE is always unbiased.  
  **Verdict: FALSE.** False, and the commonest trap in the topic. E[σ̂²] = (n−1)σ²/n for the normal; E[λ̂] = nλ/(n−1) for the exponential rate.
- `scenes[11].items[2]` **Claim:** The MLE always exists and is unique.  
  **Verdict: FALSE.** False. The likelihood can be maximised on a set rather than a point — U(θ−½, θ+½) gives an interval of maximisers — and for some models no maximum exists in the parameter space.
- `scenes[11].items[3]` **Claim:** The MLE is a function of the sufficient statistic.  
  **Verdict: TRUE.** True, straight from the factorisation theorem: maximising over θ touches only the factor that depends on the data through T.
- `scenes[11].items[4]` **Claim:** For U(0,θ), the MLE is obtained by setting dℓ/dθ = 0.  
  **Verdict: FALSE.** False. The support depends on θ, the derivative never vanishes, and the maximum is at the boundary: θ̂ = x₍ₙ₎.
- `scenes[11].items[5]` **Claim:** Under regularity conditions the MLE attains the Cramér–Rao lower bound asymptotically.  
  **Verdict: TRUE.** True — that is exactly the content of √n(θ̂−θ) →ᵈ N(0, 1/I(θ)). Note 'asymptotically': for finite n the MLE need not attain the bound at all.

---

### Scene 13 of 15 — Transfer — a case you have not been shown

`scenes[12]` · id `s12` · type `guided` (guided problem) · 6 minutes

**Purpose** `scenes[12].objective`

Apply the method to a two-parameter model with no worked template in front of you.

**Problem put to the learner** `scenes[12].problem`

X₁,…,Xₙ are iid N(μ, σ²) with BOTH parameters unknown. Find the MLEs of μ and σ².

**Hint ladder, revealed one at a time** `scenes[12].hints[]`

1. Direction — two unknowns means two score equations. Write ℓ(μ, σ²) and take a partial derivative with respect to each, not a total derivative.
2. Method — differentiate with respect to μ first. The σ² terms are constants for that derivative and the answer drops out in one line. Substitute that result before differentiating with respect to σ².
3. Next step — ℓ = −(n/2)log(2π) − (n/2)log σ² − (1/(2σ²))Σ(xᵢ−μ)². Differentiating in σ² is easier if you treat σ² as a single symbol, say v, rather than squaring and unsquaring.

**Model solution, hidden until requested** `scenes[12].solution[]`

1. `scenes[12].solution[0]` Log-likelihood.

   ```
   ℓ(μ, v) = −(n/2)log(2πv) − (1/(2v))·Σ(xᵢ−μ)²,  writing v for σ²
   ```

   Laid out:

   $$ℓ(μ, v) = −\frac{n}{2}log(2πv) − \frac{1}{(2v)}·Σ(xᵢ−μ)²,  writing v for σ²$$

2. `scenes[12].solution[1]` Differentiate in μ.

   ```
   ∂ℓ/∂μ = (1/v)·Σ(xᵢ−μ) = 0  ⟹  μ̂ = x̄
   ```

   Laid out:

   $$\frac{∂ℓ}{∂μ} = \frac{1}{v}·Σ(xᵢ−μ) = 0  ⟹  μ̂ = x̄$$

3. `scenes[12].solution[2]` Substitute and differentiate in v.

   ```
   ∂ℓ/∂v = −n/(2v) + (1/(2v²))·Σ(xᵢ−x̄)² = 0
   ```

   Laid out:

   $$\frac{∂ℓ}{∂v} = −\frac{n}{(2v)} + \frac{1}{(2v²)}·Σ(xᵢ−x̄)² = 0$$

4. `scenes[12].solution[3]` Solve.

   ```
   v̂ = σ̂² = Σ(xᵢ−x̄)² / n
   ```

   Laid out:

   $$v̂ = σ̂² = \frac{Σ(xᵢ−x̄)²}{n}$$

**Final answer given to the learner** `scenes[12].answer`

μ̂ = x̄ and σ̂² = Σ(xᵢ−x̄)²/n

**Self-check offered** `scenes[12].check`

Divided by n, not by n−1. The n−1 version is the unbiased estimator s², and it is not the MLE. E[σ̂²] = (n−1)σ²/n, so the MLE understates the variance — by 10% at n = 10. If you wrote n−1 here, that is the same reflex that produced the degrees-of-freedom errors in your error log, and it is worth a line in it now.

---

### Scene 14 of 15 — What you should now be able to do unaided

`scenes[13]` · id `s13` · type `summary` (summary) · 3 minutes

**Purpose** `scenes[13].objective`

Close the loop before the test.

**Body** `scenes[13].body[]`

Write L(θ) for any standard family, take logs, solve the score equation, and confirm the sign of the second derivative.

Spot a support that depends on θ and go straight to the boundary instead of differentiating.

Produce the MLE of any function of θ in one line by invariance.

State, with its condition attached, each of: consistency, asymptotic normality, the link to sufficiency, and the absence of unbiasedness.

The mastery test is ten questions you have not seen, mixing all of these. Hints are off. The pass is 80% overall with 70% floors on the numerical and multi-statement items.

---

### Scene 15 of 15 — Mastery test

`scenes[14]` · id `s14` · type `quiz` (mastery test) · 12 minutes

**Purpose** `scenes[14].objective`

Demonstrate it independently, on unseen questions.

Draws from the pool reproduced below. `scenes[14].setId` = `inference_t4_mastery`

---

## Revision material `revision`

**Revision sheet** `revision.sheet[]` (10 lines)

1. `[0]` L(θ) = ∏ f(xᵢ; θ). Same formula as the density; the variable is now θ.
2. `[1]` ℓ(θ) = Σ log f(xᵢ; θ). Maximise ℓ, never L.
3. `[2]` Score equation: ∂ℓ/∂θ = 0. Then check ∂²ℓ/∂θ² < 0 at the root.
4. `[3]` Support depends on θ ⟹ the derivative is useless. Look at the boundary.
5. `[4]` Invariance: MLE of g(θ) is g(θ̂). No second derivation.
6. `[5]` A unique MLE is a function of the sufficient statistic; if maximisers are not unique, the statistic determines the set of them.
7. `[6]` Consistent and asymptotically N(θ, 1/(nI(θ))) under regularity — but not generally unbiased.
8. `[7]` Exponential rate: λ̂ = n/Σxᵢ = 1/x̄.   Bernoulli: p̂ = x̄.   Poisson: λ̂ = x̄.
9. `[8]` N(μ,σ²): μ̂ = x̄, σ̂² = Σ(xᵢ−x̄)²/n — divided by n, not n−1.
10. `[9]` U(0,θ): θ̂ = x₍ₙ₎, the sample maximum.

**Flashcards** `revision.cards[]`

| Front | Back |
|---|---|
| Likelihood, in one sentence | The probability of the data you actually observed, computed under each candidate θ. Not a probability of θ. |
| Why take logs? | It turns the product into a sum, and log is strictly increasing so the maximiser is unchanged. |
| When does the score equation fail? | When the support depends on θ — U(0,θ) is the standard case. The maximum is then at a boundary. |
| MLE of θ², given θ̂ | θ̂², by invariance. |
| Is the MLE unbiased? | Not in general. Exponential rate: E[λ̂] = nλ/(n−1). Normal variance: E[σ̂²] = (n−1)σ²/n. |
| Two properties the MLE does have | Consistency, and asymptotic normality with variance 1/(nI(θ)) — under regularity conditions. |
| MLE of σ² for N(μ,σ²), both unknown | Σ(xᵢ−x̄)²/n. Dividing by n−1 gives the unbiased estimator, which is not the MLE. |
| Free check on any MLE you derive | It must be a function of the sufficient statistic. |

**Memory aids** `revision.tricks[]`

- `[0]` **Log, differentiate, check** — Three steps in order. The third — the second-derivative check — is the one most often skipped and most often worth a mark.
- `[1]` **Invariance: substitute, don't re-derive** — MLE of g(θ) is g(θ̂). True for ANY g, one-to-one or not.
- `[2]` **Support moves → look, don't differentiate** — U(0,θ): ℓ′ is never zero. The maximum is at the boundary x₍ₙ₎.
- `[3]` **MLE is not unbiased** — σ̂² divides by n, not n−1. Efficiency is asymptotic; bias at finite n is normal.

**Elimination shortcuts for multiple-choice items** `revision.shortcuts[]`

- `[0]` Bernoulli / Poisson / exponential mean: the MLE is just x̄.
- `[1]` Exponential RATE: λ̂ = n/ΣX, biased upward with E[λ̂] = nλ/(n−1).
- `[2]` N(μ,σ²) both unknown: μ̂ = x̄ and σ̂² = Σ(xᵢ−x̄)²/n — divisor n.
- `[3]` U(0,θ): θ̂ = x₍ₙ₎. U(θ−1/2, θ+1/2): any value in [x₍ₙ₎−1/2, x₍₁₎+1/2] — the MLE is not unique.

**If nothing else is remembered** `revision.remember[]`

- `[0]` An MLE need not be unique, unbiased, or even exist in a closed form.
- `[1]` Under regularity it IS consistent, asymptotically normal and asymptotically efficient — all three are large-sample claims.

**Errors to avoid** `revision.traps[]`


---

## Mastery pool — all 20 items with answer keys `qsets/mastery`

Ten are drawn per attempt at 3 easy / 5 moderate / 2 hard. Keys are distributed five to each option letter. Please check each item for a second defensible answer as well as for the correctness of its stated key and explanation.

### Q1 — `mle-m-01` *(single, moderate)*

X₁,…,Xₙ are iid with density f(x;θ) = θx^(θ−1) on 0 < x < 1, θ > 0. The MLE of θ is:

*Options* `.options[]`:

- **A.** −n / Σ log xᵢ  ← key
- **B.** n / Σ log xᵢ
- **C.** −Σ log xᵢ / n
- **D.** x̄ / (1 − x̄)

*Explanation* `.explanation`: ℓ(θ) = n log θ + (θ−1)Σ log xᵢ. Then dℓ/dθ = n/θ + Σ log xᵢ = 0, so θ̂ = −n/Σ log xᵢ. The minus sign is required and is what makes θ̂ positive, since every log xᵢ < 0 on (0,1). Option B has the wrong sign and would return a negative estimate.

### Q2 — `mle-m-02` *(numeric, moderate)*

A geometric sample (number of trials to the first success, support 1,2,3,…) of size n = 6 has Σxᵢ = 24. Give the MLE of p and the MLE of the expected number of trials.

*Options* `.options[]`:

- **A.** p̂ = 0.25 and the MLE of E[X] is 0.75
- **B.** p̂ = 0.25 and the MLE of E[X] is 4  ← key
- **C.** p̂ = 0.20 and the MLE of E[X] is 5
- **D.** p̂ = 4 and the MLE of E[X] is 0.25

*Explanation* `.explanation`: P(X=x) = (1−p)^(x−1) p, so ℓ(p) = n log p + (Σxᵢ − n) log(1−p). Setting the derivative to zero gives p̂ = n/Σxᵢ = 6/24 = 0.25. E[X] = 1/p, so by invariance its MLE is 1/0.25 = 4, which is x̄.

*Arithmetic check* `.check`: p̂ and 1/p̂ are both plausible-looking answers. Confirm which the question asked for.

### Q3 — `mle-m-03` *(multi, hard)*

X₁,…,Xₙ are iid U(0,θ) and θ̂ = x₍ₙ₎ is the MLE.

*Statements to judge* `.statements[]`:

- **A.** The score equation dℓ/dθ = 0 has no solution for this model.
- **B.** θ̂ understates θ with probability 1.
- **C.** θ̂ is not a function of the sufficient statistic.
- **D.** (n+1)/n · θ̂ is unbiased for θ.

*Options* `.options[]`:

- **A.** A and C only
- **B.** B and C only
- **C.** A, B and D only  ← key
- **D.** A, B and C only

*Explanation* `.explanation`: A is true — the derivative never vanishes, so the usual method does not locate the maximum. B is true: x₍ₙ₎ ≤ θ always, and E[θ̂] = nθ/(n+1) < θ. C is false — x₍ₙ₎ is the complete sufficient statistic and the MLE is a function of it. D is true: scaling by (n+1)/n removes the bias.

*Verdict on each statement* `.verdicts`:

- **A — true.** dℓ/dθ = −n/θ < 0 wherever L > 0. It is never zero.
- **B — true.** The sample maximum cannot exceed θ, and equals it with probability 0.
- **C — false.** x₍ₙ₎ IS the sufficient statistic here, so the MLE is trivially a function of it.
- **D — true.** E[x₍ₙ₎] = nθ/(n+1), so multiplying by (n+1)/n gives θ exactly.

### Q4 — `mle-m-04` *(numeric, moderate)*

A sample of n = 16 from N(μ, σ²) with both unknown gives Σxᵢ = 80 and Σ(xᵢ − x̄)² = 60. Give the MLE of σ², the unbiased estimator s², and say which is larger.

*Options* `.options[]`:

- **A.** σ̂² = 4, s² = 3.75; σ̂² is larger
- **B.** σ̂² = 3.75, s² = 3.75; they are equal
- **C.** σ̂² = 5, s² = 4; σ̂² is larger
- **D.** σ̂² = 3.75, s² = 4; s² is larger  ← key

*Explanation* `.explanation`: The MLE divides by n: σ̂² = 60/16 = 3.75. The unbiased estimator divides by n−1: s² = 60/15 = 4. Since n−1 < n, s² is always the larger of the two, and the MLE is biased low by a factor (n−1)/n = 15/16.

*Arithmetic check* `.check`: Two numbers and a comparison were asked for. The n versus n−1 choice is the whole question — write which denominator you used.

### Q5 — `mle-m-05` *(single, easy)*

If θ̂ is the MLE of θ and the parameter of interest is ψ = e^(−2θ), then the MLE of ψ is:

*Options* `.options[]`:

- **A.** e^(−2θ̂)  ← key
- **B.** −2e^(−2θ̂)
- **C.** E[e^(−2θ̂)]
- **D.** It cannot be obtained without a fresh derivation

*Explanation* `.explanation`: Invariance: the MLE of any function g(θ) is g(θ̂), so ψ̂ = e^(−2θ̂) directly. Option B is the derivative, not the estimator. Option C confuses the MLE with an expectation — and note e^(−2θ̂) is generally a biased estimator of e^(−2θ), which is consistent with the MLE not being unbiased.

### Q6 — `mle-m-06` *(multi, hard)*

Consider the likelihood function L(θ) for a fixed observed sample.

*Statements to judge* `.statements[]`:

- **A.** L(θ) is a probability density function of θ and integrates to 1 over the parameter space.
- **B.** L(θ) is computed from the data actually observed, held fixed.
- **C.** Maximising log L(θ) can give a different maximiser from maximising L(θ).
- **D.** L(θ) depends on the data only through a sufficient statistic, when one exists.

*Options* `.options[]`:

- **A.** A and C only
- **B.** B and D only  ← key
- **C.** A, B and D only
- **D.** B, C and D only

*Explanation* `.explanation`: A is false — L is a function of θ but is not a probability distribution over θ and need not integrate to 1. B is true. C is false: the maximiser is unchanged by taking logs, which is precisely why we do it. D is true, by the factorisation theorem.

*Verdict on each statement* `.verdicts`:

- **A — false.** It is not a distribution for θ. Treating it as one is the single commonest misconception in the topic.
- **B — true.** That is the definition — the data are fixed and θ varies.
- **C — false.** log is strictly increasing, so the maximiser is identical.
- **D — true.** L(θ) = g(T(x);θ)·h(x), and h does not involve θ.

### Q7 — `mle-m-07` *(numeric, moderate)*

X₁,…,Xₙ are iid Exponential(λ). Fisher information for a single observation is I(λ) = 1/λ². For n = 25 and λ̂ = 0.4, the approximate standard error of λ̂ from the asymptotic distribution is:

*Options* `.options[]`:

- **A.** 0.016
- **B.** 0.40
- **C.** 0.08  ← key
- **D.** 0.20

*Explanation* `.explanation`: Asymptotically λ̂ ~ N(λ, 1/(nI(λ))). Here 1/(nI(λ)) = λ²/n, so the SE is λ/√n, estimated as λ̂/√n = 0.4/5 = 0.08.

*Arithmetic check* `.check`: √n = 5, not 25. Taking the root of n is the step most often dropped here.

### Q8 — `mle-m-08` *(single, easy)*

Which of the following is NOT guaranteed for a maximum likelihood estimator, even under the usual regularity conditions?

*Options* `.options[]`:

- **A.** Asymptotic normality
- **B.** Invariance under reparametrisation
- **C.** Consistency
- **D.** Unbiasedness for every finite n  ← key

*Explanation* `.explanation`: Consistency, asymptotic normality and invariance all hold. Unbiasedness does not: the normal variance MLE is biased low and the exponential rate MLE is biased high, at every finite n. Regularity conditions buy asymptotic behaviour, not finite-sample unbiasedness.

### Q9 — `mle-m-09` *(numeric, easy)*

A sample of size n = 3 from U(0,θ) gives observations 1.2, 3.8 and 2.5. The MLE of θ, the MLE of θ², and E[θ̂] are:

*Options* `.options[]`:

- **A.** 3.8,  14.44,  3θ/4  ← key
- **B.** 3.8,  14.44,  4θ/3
- **C.** 2.5,  6.25,  3θ/4
- **D.** 3.8,  7.60,  θ

*Explanation* `.explanation`: θ̂ = x₍ₙ₎ = 3.8, the sample maximum. By invariance the MLE of θ² is 3.8² = 14.44. And E[x₍ₙ₎] = nθ/(n+1) = 3θ/4, which understates θ — the sample maximum can never exceed it.

*Arithmetic check* `.check`: Three quantities asked, and the third is in terms of θ, not a number. Answering only θ̂ = 3.8 is the wrong-quantity error in its purest form.

### Q10 — `mle-m-10` *(order, moderate)*

A question gives a density whose support is 0 < x < θ. Arrange the steps you should take, in order.

*Steps to order* `.items[]`:

- A. Identify the maximum at the boundary θ̂ = x₍ₙ₎
- B. Check whether the support depends on θ
- C. Address any follow-up on bias or on a function of θ
- D. Conclude the score equation does not apply

*Options* `.options[]`:

- **A.** A, B, D, C
- **B.** B, D, A, C  ← key
- **C.** B, A, D, C
- **D.** D, B, A, C

*Explanation* `.explanation`: Check the support first — that single check decides the whole method. Seeing it depends on θ, abandon the derivative, locate the maximum on the boundary at x₍ₙ₎, and only then answer any follow-up about bias or a function of θ. Starting with the derivative wastes the time the check would have saved.

### Q11 — `mle-m-11` *(single, easy)*

The maximum likelihood estimate of θ is the value that:

*Options* `.options[]`:

- **A.** equates the sample mean to the population mean
- **B.** makes the estimator unbiased for θ
- **C.** maximises the likelihood of the observed sample  ← key
- **D.** minimises the mean squared error

*Explanation* `.explanation`: The MLE is defined by maximisation of L(θ) at the observed data, nothing else. Unbiasedness is not required and frequently fails; minimum MSE is a different criterion altogether; and equating moments is the method of moments.

### Q12 — `mle-m-12` *(numeric, moderate)*

X₁,…,X₈ are iid Poisson(λ) with Σxᵢ = 24. Give the MLE of λ and the MLE of P(X = 0) = e^(−λ).

*Options* `.options[]`:

- **A.** λ̂ = 24, and e^(−24)
- **B.** λ̂ = 3, and ((n−1)/n)^T ≈ 0.0424
- **C.** λ̂ = 3, and 1 − e^(−3) ≈ 0.950
- **D.** λ̂ = 3, and e^(−3) ≈ 0.0498  ← key

*Explanation* `.explanation`: λ̂ = x̄ = 24/8 = 3. By invariance, the MLE of any function g(λ) is g(λ̂), so the MLE of e^(−λ) is e^(−3) = 0.0498. Option B is the UMVUE of e^(−λ), a different estimator answering a different question — it is unbiased, while the MLE is not.

*Arithmetic check* `.check`: Invariance means you substitute, you do not re-derive. If the question had asked for the UMVUE the answer would be ((n−1)/n)^T instead.

### Q13 — `mle-m-13` *(multi, hard)*

Consider maximum likelihood estimation in general.

*Statements to judge* `.statements[]`:

- **A.** If θ̂ is the MLE of θ, then g(θ̂) is the MLE of g(θ).
- **B.** Maximum likelihood estimators are unbiased.
- **C.** Under regularity the MLE is asymptotically efficient.
- **D.** The MLE need not be found by setting a derivative to zero.

*Options* `.options[]`:

- **A.** A, C and D only  ← key
- **B.** B, C and D only
- **C.** A, B and C only
- **D.** A and B only

*Explanation* `.explanation`: A is true — this is invariance, and it holds for any function. B is false: MLEs are frequently biased, σ̂² for the normal being the standard case. C is true: under regularity the MLE is consistent and asymptotically normal with variance 1/(nI(θ)). D is true — for U(0,θ) the likelihood is maximised at the boundary x₍ₙ₎, where the derivative is never zero.

*Verdict on each statement* `.verdicts`:

- **A — true.** The invariance property, valid for any function g, one-to-one or not.
- **B — false.** σ̂² = Σ(xᵢ−x̄)²/n has expectation (n−1)σ²/n. Biased.
- **C — true.** √n(θ̂−θ) → N(0, 1/I(θ)), so it attains the bound in the limit.
- **D — true.** A boundary maximum, as for U(0,θ), is found by inspecting the likelihood, not differentiating it.

### Q14 — `mle-m-14` *(numeric, moderate)*

X₁,…,X₁₀ are iid Bernoulli(p) with Σxᵢ = 3. Give the MLE of p and the MLE of the odds p/(1−p).

*Options* `.options[]`:

- **A.** p̂ = 0.3, odds = 0.3
- **B.** p̂ = 0.3, odds = 3/7 ≈ 0.4286  ← key
- **C.** p̂ = 3, odds = 3/7
- **D.** p̂ = 0.3, odds = 7/3 ≈ 2.333

*Explanation* `.explanation`: p̂ = x̄ = 3/10 = 0.3. By invariance the MLE of p/(1−p) is p̂/(1−p̂) = 0.3/0.7 = 3/7 ≈ 0.4286. Option D inverts the ratio, giving the odds against rather than the odds for.

*Arithmetic check* `.check`: With p̂ below 0.5 the odds must come out below 1. An answer above 1 has the ratio upside down.

### Q15 — `mle-m-15` *(single, moderate)*

For X₁,…,Xₙ iid U(0,θ), why is the MLE found without differentiating?

*Options* `.options[]`:

- **A.** The parameter is not identifiable
- **B.** The likelihood is not a function of θ
- **C.** The likelihood is θ^(−n) on θ ≥ x₍ₙ₎ and 0 below it, so it is maximised at the left endpoint of its support  ← key
- **D.** The derivative of the log-likelihood has no solution anywhere

*Explanation* `.explanation`: L(θ) = θ^(−n)·I(θ ≥ x₍ₙ₎) is strictly decreasing wherever it is positive, so the maximum sits at the smallest admissible θ, namely x₍ₙ₎. The derivative is −nθ^(−n−1), never zero, which is why setting it to zero finds nothing: the maximum is at a boundary, not at a stationary point.

### Q16 — `mle-m-16` *(numeric, hard)*

X₁,…,X₂₀ are iid N(μ, σ²) with both unknown. The sample gives Σxᵢ = 60 and Σ(xᵢ − x̄)² = 76. Give the MLE of σ² and the unbiased estimator s², and say which is larger.

*Options* `.options[]`:

- **A.** σ̂² = 3.8 and s² = 3.8, they coincide
- **B.** σ̂² = 76 and s² = 4.0
- **C.** σ̂² = 4.0 and s² = 3.8, so σ̂² is larger
- **D.** σ̂² = 3.8 and s² = 4.0, so s² is larger  ← key

*Explanation* `.explanation`: The MLE divides by n: σ̂² = 76/20 = 3.8. The unbiased estimator divides by n−1: s² = 76/19 = 4.0. Since n−1 < n the unbiased version is always the larger of the two, and the gap closes as n grows — which is the MLE's bias, E[σ̂²] = (n−1)σ²/n, written as a number.

*Arithmetic check* `.check`: s² > σ̂² always, for any sample. If your two numbers come out the other way round, the divisors have been swapped.

### Q17 — `mle-m-17` *(multi, moderate)*

X₁,…,Xₙ are iid Exponential with mean θ.

*Statements to judge* `.statements[]`:

- **A.** The MLE of θ is x̄.
- **B.** The MLE of θ is unbiased.
- **C.** The MLE of the rate λ = 1/θ is also unbiased.
- **D.** The MLE of θ attains the Cramér–Rao bound.

*Options* `.options[]`:

- **A.** A, B and D only  ← key
- **B.** A and C only
- **C.** B and C only
- **D.** A, B and C only

*Explanation* `.explanation`: A is true — the likelihood equation gives θ̂ = x̄. B is true, and here the MLE happens to be unbiased, since E[X̄] = θ. C is false: the MLE of the RATE λ = 1/θ is 1/x̄ by invariance, and that one IS biased, with E[1/X̄] = nλ/(n−1). D is true: Var(X̄) = θ²/n, which equals the Cramér–Rao bound for θ.

*Verdict on each statement* `.verdicts`:

- **A — true.** ℓ = −n log θ − Σx/θ, and setting ℓ′ = 0 gives θ̂ = x̄.
- **B — true.** E[X̄] = θ exactly, at every n.
- **C — false.** Invariance preserves the MLE, not unbiasedness: E[n/ΣX] = nλ/(n−1) > λ.
- **D — true.** I(θ) = 1/θ², so the floor is θ²/n = Var(X̄). Attained.

### Q18 — `mle-m-18` *(numeric, easy)*

A sample of size n = 5 from U(0,θ) gives the observations 2.4, 0.9, 3.7, 1.1 and 3.2. Give the MLE of θ.

*Options* `.options[]`:

- **A.** 2.26
- **B.** 3.7  ← key
- **C.** 4.52
- **D.** 1.85

*Explanation* `.explanation`: The MLE for U(0,θ) is the sample maximum, so θ̂ = 3.7. Option A is x̄ = 11.3/5 = 2.26, option C is the moment estimator 2x̄ = 4.52, and option D is half the maximum. Note any answer below 3.7 is impossible, since a 3.7 was observed.

*Arithmetic check* `.check`: Compare any candidate against the largest observation. Below it, the likelihood is exactly zero.

### Q19 — `mle-m-19` *(single, easy)*

Which is NOT a general property of maximum likelihood estimators?

*Options* `.options[]`:

- **A.** invariance under reparameterisation
- **B.** consistency under regularity conditions
- **C.** unbiasedness at every sample size  ← key
- **D.** asymptotic normality under regularity conditions

*Explanation* `.explanation`: Invariance holds always; consistency and asymptotic normality hold under the usual regularity conditions. Unbiasedness is the one that is not general — σ̂² for the normal and the exponential rate estimator are both biased at every finite n.

### Q20 — `mle-m-20` *(order, moderate)*

To find an MLE for a family whose support does not involve θ, arrange these steps.

*Steps to order* `.items[]`:

- A. Differentiate and solve ℓ′(θ) = 0
- B. Apply invariance if a function of θ was asked for
- C. Write the log-likelihood ℓ(θ)
- D. Verify the second-order condition for a maximum

*Options* `.options[]`:

- **A.** A, C, D, B
- **B.** C, D, A, B
- **C.** A, D, C, B
- **D.** C, A, D, B  ← key

*Explanation* `.explanation`: Write the log-likelihood first, then differentiate and solve the likelihood equation, then confirm the stationary point is a maximum rather than a minimum or inflection, and only then apply invariance if the question asked for a function of θ. Checking the second-order condition is the step most often skipped and most often worth a mark.

---

## Authoring and verification record `provenance`

Reproduced verbatim. It records what changed in each version and how each derivation was checked, including the findings of the two previous review rounds and the reasons some of their recommendations were declined.

> Review pass, October 2026: 3 per-scene quick checks added on theory, worked and explore scenes from a third-party module review, each read for correctness before import; a further set offered for completion and guided scenes was declined, since those scenes already end with the learner writing an answer. The review also found the MLE described as ALWAYS a function of the sufficient statistic in the prerequisite and the revision sheet; applying that finding across the lesson turned up a third copy in a prerequisite-check recall, which the review had not flagged. All three now qualify the claim to an MLE that exists and is unique, and state that otherwise the sufficient statistic determines the set of maximisers. Theory and worked examples authored for this platform; previous-year questions marked separately and carry their exam cycle.

