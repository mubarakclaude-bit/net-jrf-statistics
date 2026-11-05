# Lesson 4.5 — Method of Moments, Minimum Chi-square and Least Squares

Complete authored content of one lesson from a UGC-NET Statistics (Code 107) preparation application, extracted from the application's own content files.

| | |
|---|---|
| Content version | 1.3 |
| Scenes | 14 |
| Core scenes | 14 |
| Optional JRF-extension scenes | 0 |
| Estimated learner time | 51 minutes |
| Mastery pool | 20 items |
| Position in the app | Statistical Inference → Point Estimation → Estimators you can write down without a likelihood |
| Engine | Estimation and inference — matching what you observe to what the model predicts |
| Pool label | Method of moments, minimum chi-square and least squares — mastery test (unseen) |
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

1. Set up and solve the moment equations for a one- or two-parameter family, choosing raw or central moments to keep the algebra short.

2. State what the method of moments guarantees (consistency, asymptotic normality) and what it does not (unbiasedness, efficiency, a legal estimate).

3. Recognise the two families the exam uses against the method: U(a,b), where the estimate can be impossible, and Cauchy, where there is no moment to match.

4. Define the minimum chi-square and modified minimum chi-square estimators, and say what data they need.

5. Derive the least squares normal equations as moment conditions, and see least squares as one more instance of the same idea.

**Assumed prior knowledge** `prereq[]`

- `prereq[0]` **Population and sample moments** — The whole method is one line: set m_r' equal to μ_r' and solve. If the notation is not automatic, fix that first.
- `prereq[1]` **Mean and variance of standard families** — You need E[X] and Var(X) for the gamma, uniform, exponential and normal from memory — the moment equations start there.
- `prereq[2]` **Maximum likelihood estimation** — Every comparison in this topic is against the MLE: sometimes the two coincide, usually the MLE is more efficient, occasionally the moment estimator is the only one you can write down.

**Misconceptions the lesson is built to pre-empt** `traps[]`

- The divisor in σ̃² is n, not n−1.

- θ̃ = 2x̄ for U(0,θ) can be less than x₍ₙ₎, and then it is not an estimate at all.

- Consistency does not imply unbiasedness.

- No moments, no method — the Cauchy has no mean.

- Least squares needs no normality; it only coincides with ML when the errors are normal.

**Assessment policy** `mastery`

- 10 items drawn per attempt from a pool of 20, mix 3 easy, 5 moderate, 2 hard
- pass mark 80%, no hints during the test, retest after 7 days
- `mastery.note`: Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the difficulty mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split.

**Sources** `refs[]`

- `refs[0]` **Method of Moments** — Penn State STAT 415, Lesson 1.4, Point Estimation (Course notes, free). The cleanest statement of both forms of the method, with the Bernoulli, normal and gamma worked out (Examples 1-7 to 1-10). Example 1-10 redoes the normal by the second form and shows it is less work — the same labour-saving point scene 3 makes. CC BY-NC, no login.
- `refs[1]` **Parametric models and method of moments** — Stanford STATS 200 (Autumn 2016), Lecture 12 (Lecture notes, free). Six worked examples (Poisson, exponential, normal, gamma) and then bias, variance and MSE computed for the moment estimators themselves — which is what scene 9 asks you to do. It does not cover consistency or asymptotic normality, so take those from scene 3 here.
- `refs[2]` **Paths to least squares** — Berkeley STAT 151A, Unit 1 lecture note (Lecture notes, free). Arrives at least squares four separate ways — risk minimisation, maximum likelihood with normal errors, a Bayesian posterior mean, and a moment condition. Read it after scene 11, which derives the last of those. It is the best short argument that these 'different methods' are one idea seen from different sides.

---

## The lesson, scene by scene

### Scene 1 of 14 — Before the lesson — four things it will assume

`scenes[0]` · id `s0` · type `foundation` (prerequisite check) · 6 minutes

**Purpose** `scenes[0].objective`

Get the moments of the standard families and the moment/variance identity back to automatic, since every equation in this topic starts there.

**Body** `scenes[0].body[]`

The method of moments is the easiest estimation method to state and the easiest to fumble. Stating it takes one line: set the sample moments equal to the population moments and solve. Fumbling it takes one forgotten formula — the variance of a uniform, say, or the rate-versus-scale convention for the gamma.

So this check is mostly recall of standard results. That is deliberate: in the exam these are not derived, they are remembered, and a two year gap is exactly long enough to lose them.

**Check 1** `scenes[0].items[0]`

- *asks:* Define the r-th population moment and the r-th sample moment, and state what the method of moments does with them.
- *expected answer* `.recall`: μ_r′ = E[Xʳ] and m_r′ = (1/n)Σxᵢʳ. For k unknown parameters, set m_r′ = μ_r′(θ) for r = 1,…,k and solve the k equations.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> The population moment is a property of the model and so is a function of θ: for an exponential with rate λ, μ₁′ = 1/λ. The sample moment is a number computed from the data and knows nothing about θ.

> The method just equates them and solves. One unknown, one equation: 1/λ = x̄ gives λ̃ = 1/x̄. Two unknowns, two equations — which is where the second moment comes in and where the arithmetic starts to bite.

> A word on notation, since exam papers use both. The prime marks a raw moment, about zero. Moments about the mean are written without it: μ₂ = Var(X). Mixing the two is the commonest source of a wrong sign in this topic.

**Check 2** `scenes[0].items[1]`

- *asks:* From memory: E[X] and Var(X) for the exponential, U(a,b), gamma and normal.
- *expected answer* `.recall`: Exponential with rate λ: 1/λ and 1/λ². U(a,b): (a+b)/2 and (b−a)²/12. Gamma with shape α and rate β: α/β and α/β². Normal(μ,σ²): μ and σ².

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Carry these four as a block, because the moment equations begin with them and there is no time to derive them in the exam.

> Exponential(λ): mean 1/λ, variance 1/λ². The exponential is a gamma with shape 1, which is the quickest way to recover it if you blank.

> U(a,b): mean is the midpoint (a+b)/2; variance is (b−a)²/12. The 12 is the one number people lose. Sanity check: U(0,1) has variance 1/12 ≈ 0.083, which is right for a spread of one unit.

> Gamma: with shape α and rate β, mean α/β and variance α/β². If the book uses scale θ = 1/β instead, the mean is αθ and the variance αθ². Read which convention a question is using before you write anything — the two differ by a reciprocal and the options will include both answers.

**Check 3** `scenes[0].items[2]`

- *asks:* How do E[X²], Var(X) and E[X] relate, and why does the second moment equation nearly always use that identity?
- *expected answer* `.recall`: E[X²] = Var(X) + (E[X])². The second sample moment (1/n)Σxᵢ² estimates E[X²], not the variance — so you convert the model's variance into a second moment before equating.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Var(X) = E[X²] − (E[X])² rearranged. Nothing more, but it is used in every two-parameter moment problem.

> See why. For N(μ,σ²), the two moment equations are μ = x̄ and E[X²] = σ² + μ² = (1/n)Σxᵢ². Substituting the first into the second gives σ̃² = (1/n)Σxᵢ² − x̄² = (1/n)Σ(xᵢ−x̄)².

> Note what came out: the divisor is n, not n−1. The method of moments estimator of a variance is the biased one, and the lesson returns to that — the method makes no promise of unbiasedness, only of consistency.

**Check 4** `scenes[0].items[3]`

- *asks:* What does least squares minimise, and what are the normal equations for fitting a straight line?
- *expected answer* `.recall`: It minimises Σ(yᵢ − a − bxᵢ)². Setting the two partial derivatives to zero gives b̂ = Σ(xᵢ−x̄)(yᵢ−ȳ)/Σ(xᵢ−x̄)² and â = ȳ − b̂x̄.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> You differentiate the sum of squared vertical deviations with respect to a and then b, set both to zero, and solve. The two resulting equations are called the normal equations.

> Both formulas carry a reading worth keeping. b̂ is a ratio of the sample covariance of x and y to the variance of x. And â = ȳ − b̂x̄ says the fitted line passes through (x̄, ȳ) whatever the slope — a free check on any numerical answer.

> The lesson compares all three methods on the same footing, so you need this one in the same form as the other two: an estimating criterion, differentiated, set to zero.

---

### Scene 2 of 14 — Match what you see to what the model predicts

`scenes[1]` · id `s1` · type `intuition` (intuition) · 5 minutes

**Purpose** `scenes[1].objective`

Get the one idea behind the whole topic before any algebra.

**Body** `scenes[1].body[]`

Your model says the mean of X is some expression in θ. Your data have a mean you can compute. The method of moments does the obvious thing: it sets the two equal and solves for θ.

If there are two unknowns, one equation is not enough, so you add the next moment — usually the variance — and solve the pair. k unknowns, k moments, k equations. That is the entire method.

Why bother, when maximum likelihood is better behaved? Three reasons, and the exam uses all three. The moment estimator can almost always be written down in closed form, where the likelihood equation may need a computer. It needs no distributional assumption beyond the moments themselves. And when an iterative routine does go looking for the MLE, the moment estimate is what it starts from.

What you give up is sharpness. The method looks only at the first few moments and throws the rest of the sample's information away, so it is usually less efficient than the MLE. It is generally biased. And in two notorious cases it either produces an impossible answer or cannot be started at all — both of which you will meet in this lesson, because both are examined.

Keep the method's status clear in your head: it is a reliable way to GET an estimator, not a claim that the estimator is good. Those are separate questions, answered by the tools from the last three topics.

**Aside — Why it works at all** `scenes[1].aside.body`

The weak law of large numbers says the sample moments converge in probability to the population moments. If the parameter is a continuous function of those moments, the estimator inherits the convergence. That is the whole proof of consistency, and it is also the reason nothing stronger is promised.

**Suggested question to put to the assistant** `scenes[1].ask` *(legacy shape: a pre-written prompt, not a self-test question — this scene has no quick check)*

- *button label* `.label`: Ask Claude where this method sits among the others
- *prompt* `.prompt`: A UGC NET Statistics (JRF) candidate is studying the method of moments after covering sufficiency, Rao–Blackwell, MLE and the Cramér–Rao bound. In under 160 words, plain text, place the method of moments against those: what question it answers that they do not, and why a method with weaker properties is still on the syllabus. Do not list the steps of the method.
- *model tier requested* `.tier`: default *(configuration, not content)*

**Optional deep-dive, opened on demand — Sizing a spillway from 40 years of annual peak flows** `scenes[1].scenario`

*teaser on the closed card:* Every flood defence in the country is sized by a method-of-moments fit.

> A dam spillway has to pass the 100-year flood. The hydrologist has one number per year — the annual peak discharge — and perhaps forty of them. From that, a design flow with an exceedance probability of 0.01 must be produced, and defended at a public inquiry.

> The standard practice is to fit a two-parameter distribution to the annual maxima, commonly a gamma or a Gumbel, and read the quantile off the fitted curve. The fitting is done by the method of moments: set the mean of the distribution equal to the sample mean, the variance equal to the sample variance, and solve.

> Why not maximum likelihood, which is more efficient? Three reasons, all of them the ones this lesson gives. The moment estimates are closed-form, so they can be computed and audited on a spreadsheet by a reviewer who is not a statistician. They require no iteration that might fail to converge on a short record. And national design guidance has to be reproducible — two engineers with the same data must get the same answer, which an iterative optimiser does not guarantee.

> The cost is efficiency. With forty observations the moment estimate of the shape parameter is noticeably noisier than the MLE, and the 100-year quantile inherits that noise. Practitioners handle this by reporting confidence bands around the design flow rather than pretending the point estimate is exact.

> There is also a trap this lesson has already shown you. If the sample variance is large relative to the squared mean, the gamma shape estimate α̃ = x̄²/m₂ comes out below 1 — a legal value, but one implying an infinite density at zero flow. If it comes out negative, which a short skewed record can produce for other distributions, the estimate is outside the parameter space and must be reported as such rather than quietly truncated.

*think-it-through question* `.q`: A record gives x̄ = 400 m³/s and m₂ = 160,000. What are the gamma moment estimates, and what do they say?

*what the statistics says* `.answer`: β̃ = m₂/x̄ = 160000/400 = 400 and α̃ = x̄²/m₂ = 160000/160000 = 1. A shape of exactly 1 is the exponential distribution, so the record is consistent with exponentially distributed annual peaks of mean 400 — which is the classic signature of a variance equal to the squared mean. That is a meaningful finding rather than a failure: it tells the hydrologist the data carry no evidence of the extra shape flexibility the gamma offers, and that the simpler one-parameter model would do.

*link line* `.link`: The same moment fit is used for wind-speed distributions in turbine siting and for particle-size distributions in process engineering — anywhere a closed-form, auditable fit matters more than the last few percent of efficiency.

---

### Scene 3 of 14 — Where the moment estimator lands

`scenes[2]` · id `s2` · type `explore` (interactive visualisation) · 6 minutes

**Purpose** `scenes[2].objective`

See a case where the moment estimator and the MLE are the same point.

**Body** `scenes[2].body[]`

Exponential with rate λ, so E[X] = 1/λ. The moment equation is 1/λ = x̄, giving λ̃ = 1/x̄ = n/Σxᵢ.

The readout labelled λ̂ = n/Σxᵢ is exactly that number. With n = 4 and Σxᵢ = 16 it is 0.25, and the curve peaks there. For this family the moment estimator and the maximum likelihood estimator are the same estimator, arrived at by two completely different arguments — one matching a mean, one maximising a product.

Drag the candidate λ slider away from the peak and watch the likelihood ratio fall. That is the likelihood's opinion of values the moment equation would never have proposed. Now change n and Σxᵢ: the two estimators move together, always, because 1/x̄ IS the maximiser here.

Do not generalise from this. The coincidence happens when the parameter appears in the mean in a simple enough way — the exponential, the Poisson, the Bernoulli, the normal mean. For the uniform, the gamma shape, and most two-parameter problems, the two estimators are different numbers, and the MLE is the better one.

One thing the coincidence does NOT buy: unbiasedness. λ̃ = n/ΣX is the MLE and the moment estimator, and it is biased upward. Scene 9 computes by how much.

**Interactive element** `scenes[2].viz` — live plot of type `exp-likelihood`, initial state n=4, sumx=16.0. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[2].ask`

- *question:* Why does matching the first population moment to the first sample moment produce a method-of-moments estimator?
- *hint on request:* The sample moment is used as an estimate of the corresponding population moment, yielding an equation in the unknown parameter.

---

### Scene 4 of 14 — The method, both forms, and what it promises

`scenes[3]` · id `s3` · type `theory` (theory) · 9 minutes

**Purpose** `scenes[3].objective`

Set the equations up correctly and know exactly which properties you may claim.

**Block 1 — The method of moments** `scenes[3].blocks[0]` *(type `def`)*

For a family with k unknown parameters θ₁,…,θ_k, equate the first k population moments to the first k sample moments and solve. The solution θ̃ is the method of moments estimator (MME).

**Block 2 — Form 1 — raw moments** `scenes[3].blocks[1]` *(type `formula`)*

μ_r'(θ) = E[X^r]  set equal to  m_r' = (1/n) Σ xᵢ^r ,   for r = 1, …, k.

**Block 3 — Form 2 — mean and central moments** `scenes[3].blocks[2]` *(type `formula`)*

E[X] = x̄   and   Var(X) = m₂ = (1/n) Σ (xᵢ − x̄)² ,   then higher central moments if k > 2.

**Block 4 — Which form to use** `scenes[3].blocks[3]` *(type `note`)*

Whichever cancels. Form 2 is almost always shorter for a two-parameter family, because the variance is usually a cleaner expression in θ than E[X²] is. Penn State's Example 1-10 redoes the normal by Form 2 after Example 1-8 did it by Form 1, and the saving is obvious. The two forms give the same estimator — they are algebraically equivalent, since m₂ = m₂' − (m₁')².

**Block 5 — The procedure, in the order that avoids dead ends** `scenes[3].blocks[4]` *(type `step`)*

1. Count the unknown parameters: that is how many equations you need.
2. Write E[X], and Var(X) if there are two, as expressions in the parameters.
3. Set them equal to x̄ and m₂.
4. Solve — divide one equation by the other first if a parameter appears in both.
5. CHECK the answer lies in the parameter space.

**Block 6 — What the method guarantees** `scenes[3].blocks[5]` *(type `def`)*

Consistency: θ̃ → θ in probability, because the sample moments converge to the population moments and θ̃ is a continuous function of them. Asymptotic normality: √n(θ̃ − θ) has a limiting normal distribution, so large-sample confidence intervals are available.

**Block 7 — What it does NOT guarantee** `scenes[3].blocks[6]` *(type `trap`)*

Unbiasedness — σ̃² for the normal is biased, and λ̃ for the exponential rate is biased. Efficiency — the method uses only k moments, not the whole likelihood, so its asymptotic variance is generally larger than the MLE's. Uniqueness — a different choice of moments can give a different estimator. And admissibility of the answer: the estimate can land outside the parameter space, which scene 8 shows.

**Block 8 — When the method cannot be started** `scenes[3].blocks[7]` *(type `assume`)*

The moments you want to match have to exist. The Cauchy distribution has no finite mean, so there is no first population moment and the method is simply unavailable — the sample mean of a Cauchy sample does not settle down as n grows. This is a standing exam question, and the correct answer is that the method fails, not that you should use a median.

**Block 9 — Sufficiency, and why the method ignores it** `scenes[3].blocks[8]` *(type `note`)*

x̄ and m₂ are not in general sufficient, so the moment estimator can discard information that the likelihood keeps. That is the structural reason for the efficiency loss, and it links this topic straight back to sufficiency: the MLE is a function of the sufficient statistic, and the MME need not be.

**Flow diagram** `scenes[3].flow` — The method of moments, with the check that most answers omit

*alt text* `.alt`: Decision chart for method of moments estimation

- row 1: Count the unknown parameters: k
- row 2: Do the first k population moments exist?
- row 3: No moments, no method — e.g. the Cauchy  |  Write E[X], and Var(X) if k = 2, in the parameters
- row 4: Set equal to x̄ and m₂; divide one by the other to eliminate
- row 5: Does the solution lie INSIDE the parameter space?
- row 6: Report the moment estimate  |  Inadmissible — say so and give the MLE instead
- arrows: Count the unknown parameters: k → Do the first k population moments exist?; Do the first k population moments exist? → [no] No moments, no method — e.g. the Cauchy; Do the first k population moments exist? → [yes] Write E[X], and Var(X) if k = 2, in the parameters; Write E[X], and Var(X) if k = 2, in the parameters → Set equal to x̄ and m₂; divide one by the other to eliminate; Set equal to x̄ and m₂; divide one by the other to eliminate → Does the solution lie INSIDE the parameter space?; Does the solution lie INSIDE the parameter space? → [yes] Report the moment estimate; Does the solution lie INSIDE the parameter space? → [no] Inadmissible — say so and give the MLE instead

*note shown under the diagram* `.note`: The last diamond is the one that is skipped. For U(0,θ) the estimate 2x̄ can land below the largest observation, where the likelihood is exactly zero — and that is the examinable point, not a mistake to hide.

**Quick check before moving on** `scenes[3].ask`

- *question:* When the number of unknown parameters exceeds the number of moment equations, what must you do before claiming a unique method-of-moments estimate?
- *hint on request:* Choose additional moments or another identification strategy; the original equations may not determine a unique solution.

---

### Scene 5 of 14 — Worked in full — the gamma, where one equation is not enough

`scenes[4]` · id `s4` · type `worked` (worked example) · 7 minutes

**Purpose** `scenes[4].objective`

Run a genuine two-parameter moment calculation end to end.

**Problem put to the learner** `scenes[4].problem`

X₁,…,Xₙ are iid Gamma with shape α and scale β, so E[X] = αβ and Var(X) = αβ². A sample gives x̄ = 6 and m₂ = 4. Find the method of moments estimators of α and β, and evaluate them.

**Worked steps** `scenes[4].steps[]`

1. `scenes[4].steps[0]` Count the unknowns, so you know how many equations to write.

   ```
   Two parameters, α and β  ⇒  two moment equations.
   ```

   *why* `.why`: This is step one for a reason. Writing one equation and then discovering you cannot solve it wastes the time the second equation would have cost.

2. `scenes[4].steps[1]` Write the two equations, using the mean and the variance rather than E[X] and E[X²].

   ```
   αβ = x̄    (i)
αβ² = m₂   (ii)
   ```

   *why* `.why`: Var(X) = αβ² is a cleaner expression in α and β than E[X²] = αβ²(α+1) would be. This is Form 2 earning its keep.

3. `scenes[4].steps[2]` Divide (ii) by (i). The shape cancels and β falls out alone.

   ```
   αβ² / (αβ) = β = m₂ / x̄
   ```

   Laid out:

   $$\frac{αβ²}{(αβ)} = β = \frac{m₂}{x̄}$$

   *why* `.why`: Dividing is the move to look for whenever the same parameter multiplies both sides. It turns a simultaneous system into two one-line solutions.

4. `scenes[4].steps[3]` Substitute back into (i) for the shape.

   ```
   α = x̄ / β = x̄ / (m₂/x̄) = x̄² / m₂
   ```

   Laid out:

   $$α = \frac{x̄}{β} = \frac{x̄}{\frac{m₂}{x̄}} = \frac{x̄²}{m₂}$$

   *why* `.why`: Note the shape estimator is a ratio of the squared mean to the variance — large relative to its spread means a large shape parameter, which is the right direction.

5. `scenes[4].steps[4]` Put the numbers in.

   ```
   β̃ = 4/6 = 2/3 ≈ 0.667,    α̃ = 6²/4 = 36/4 = 9
   ```

   Laid out:

   $$β̃ = \frac{4}{6} = \frac{2}{3} ≈ 0.667,    α̃ = \frac{6²}{4} = \frac{36}{4} = 9$$

   *why* `.why`: Keep the fraction until the end. Rounding β to 0.67 and then computing α from it introduces error for no reason.

6. `scenes[4].steps[5]` Check by reconstructing the moments.

   ```
   α̃β̃ = 9 × 2/3 = 6 = x̄  ✓     α̃β̃² = 9 × 4/9 = 4 = m₂  ✓
   ```

   Laid out:

   $$α̃β̃ = 9 × \frac{2}{3} = 6 = x̄  ✓     α̃β̃² = 9 × \frac{4}{9} = 4 = m₂  ✓$$

   *why* `.why`: Thirty seconds, and it catches an inverted ratio or a dropped square. Always do it: the moment equations are the one place where the check is this easy.

**What to take from it** `scenes[4].after`

The pattern generalises to every two-parameter problem on this syllabus: write the mean and the variance, divide to eliminate one parameter, substitute back, check. If the division does not simplify, you have probably chosen the harder of the two forms — try the other.

**Quick check before moving on** `scenes[4].ask`

- *question:* In the Gamma example, why are two equations needed and how do you check the resulting parameter estimates?
- *hint on request:* There are two unknown parameters; solve the two moment equations and check both estimates lie in the parameter space.

---

### Scene 6 of 14 — Pause and recall

`scenes[5]` · id `s5` · type `recall` (retrieval practice) · 2 minutes

**Purpose** `scenes[5].objective`

Retrieve before reading on — this is where the retention comes from.

**Intro** `scenes[5].intro`

Answer each in your head before revealing. Correcting a wrong retrieval beats re-reading a right answer.

- `scenes[5].items[0]` **Q:** State the method of moments in one sentence.  
  **A:** Equate the first k sample moments to the first k population moments and solve for the k parameters.
- `scenes[5].items[1]` **Q:** Which two properties does the method guarantee, and which two does it not?  
  **A:** Guaranteed: consistency and asymptotic normality. Not guaranteed: unbiasedness and efficiency.
- `scenes[5].items[2]` **Q:** Why is the moment estimator usually less efficient than the MLE?  
  **A:** It uses only the first k moments, which are not in general sufficient, so it discards information the likelihood keeps.
- `scenes[5].items[3]` **Q:** Name a family where the method cannot be started at all, and why.  
  **A:** The Cauchy — it has no finite mean, so there is no first moment to match.

---

### Scene 7 of 14 — Your turn, with the scaffolding removed — U(a,b)

`scenes[6]` · id `s6` · type `completion` (fill in the blanks) · 8 minutes

**Purpose** `scenes[6].objective`

Run a two-parameter moment calculation yourself, on the family the exam uses most.

**Problem put to the learner** `scenes[6].problem`

X₁,…,Xₙ are iid Uniform on (a, b), with E[X] = (a+b)/2 and Var(X) = (b−a)²/12. A sample gives x̄ = 10 and m₂ = 3. Find the method of moments estimators of a and b, and evaluate them.

**Worked steps** `scenes[6].steps[]`

1. `scenes[6].steps[0]` Write the two moment equations.

   ```
   (a + b)/2 = x̄ = 10    (i)
(b − a)²/12 = m₂ = 3   (ii)
   ```

   Laid out:

   $$\frac{(a + b)}{2} = x̄ = 10    (i)
\frac{(b − a)²}{12} = m₂ = 3   (ii)$$

   *why* `.why`: Two unknowns, two equations. Notice the convenient structure: (i) involves the sum and (ii) the difference, so neither has to be substituted into the other.

2. `scenes[6].steps[1]` Solve (ii) for the difference b − a. Take the positive root, since b > a.

   - *learner is asked:* Write b − a in terms of m₂.
   - *accepted answer* `.blank.answer`: 2√(3m₂)
   - *also accepted:* 2√(3m₂); 2sqrt(3m2); 2√(3m2); √(12m₂); sqrt(12m2); √(12m2); 2*sqrt(3*m2); 2√3m₂
   - *hint:* Multiply both sides by 12 to get (b−a)² = 12m₂, then take the square root. √12 = 2√3, so the answer can be written either as √(12m₂) or 2√(3m₂).

   *why* `.why`: Both forms are the same number. 2√(3m₂) is the one worth memorising, because the 3 under the root is what you will recognise in a multiple-choice option.

3. `scenes[6].steps[2]` Combine the sum and the difference. Half the difference, taken either side of the mean, gives the two endpoints.

   - *learner is asked:* Write ã, the estimator of the lower endpoint.
   - *accepted answer* `.blank.answer`: x̄ − √(3m₂)
   - *also accepted:* x̄ − √(3m₂); x̄-√(3m₂); xbar - sqrt(3m2); x̄ − √(3m2); x̄-sqrt(3m2); mean - sqrt(3*m2); x̄ − √3m₂
   - *hint:* From (i), a + b = 2x̄. You now also have b − a. Subtract the second from the first and halve: a = x̄ − (b−a)/2, and (b−a)/2 = √(3m₂).

   *why* `.why`: And by the same step b̃ = x̄ + √(3m₂). The estimates sit symmetrically about the sample mean, which is exactly what a symmetric distribution should give you.

4. `scenes[6].steps[3]` Evaluate both at x̄ = 10 and m₂ = 3.

   - *learner is asked:* Give the two numerical estimates, lower then upper.
   - *accepted answer* `.blank.answer`: 7 and 13
   - *also accepted:* 7 and 13; 7,13; 7 13; a=7,b=13; a = 7, b = 13; 7 & 13; (7,13)
   - *hint:* √(3 × 3) = √9 = 3. So the estimates are 10 − 3 and 10 + 3.

   *why* `.why`: The numbers were chosen to come out whole. In the exam they usually do, and a messy answer is a signal to re-check the 12.

5. `scenes[6].steps[4]` Check against the two moments.

   ```
   (7 + 13)/2 = 10 = x̄  ✓     (13 − 7)²/12 = 36/12 = 3 = m₂  ✓
   ```

   Laid out:

   $$\frac{(7 + 13)}{2} = 10 = x̄  ✓     \frac{(13 − 7)²}{12} = \frac{36}{12} = 3 = m₂  ✓$$

   *why* `.why`: Both reconstructed, so the algebra is sound. What the check cannot tell you is whether the estimate is legal — that needs the sample itself, and it is the subject of the next-but-one scene.

**What to take from it** `scenes[6].after`

Two special cases fall straight out of this. For U(0,θ), the lower endpoint is known to be 0, so one equation suffices: θ/2 = x̄ gives θ̃ = 2x̄. For U(−θ,θ) the mean is 0 whatever θ is, so the first moment is useless and you must match the variance instead: θ²/3 = m₂, giving θ̃ = √(3m₂). Read the question for which endpoints are known before counting your equations.

---

### Scene 8 of 14 — The other two methods — minimum chi-square and least squares

`scenes[7]` · id `s7` · type `theory` (theory) · 9 minutes

**Purpose** `scenes[7].objective`

Define both, know what data each needs, and see why they belong in the same lesson.

**Block 1 — Minimum chi-square estimation** `scenes[7].blocks[0]` *(type `def`)*

The data are grouped into k cells with observed frequencies O₁,…,O_k summing to n. The model gives cell probabilities p₁(θ),…,p_k(θ). Choose θ to make the fitted frequencies as close as possible to the observed ones, measured by the Pearson statistic.

**Block 2 — The criterion** `scenes[7].blocks[1]` *(type `formula`)*

minimise over θ:    χ²(θ)  =  Σᵢ ( Oᵢ − n pᵢ(θ) )² / ( n pᵢ(θ) )

**Block 3 — Modified minimum chi-square** `scenes[7].blocks[2]` *(type `formula`)*

minimise over θ:    Σᵢ ( Oᵢ − n pᵢ(θ) )² / Oᵢ
The observed frequency replaces the expected one in the denominator, so θ appears only in the numerator and the minimisation is much easier.

**Block 4 — What is true of both** `scenes[7].blocks[3]` *(type `note`)*

For multinomial data the minimum chi-square estimator, the modified minimum chi-square estimator and the MLE are all BAN — best asymptotically normal — and asymptotically equivalent. They differ at finite n, and the modified version is the one you can actually solve by hand. Both need the data grouped, with expected cell frequencies not too small, which is the same condition the chi-square goodness-of-fit test carries.

**Block 5 — Least squares estimation** `scenes[7].blocks[4]` *(type `def`)*

Observations y₁,…,yₙ have means that depend on known constants and unknown parameters: E[yᵢ] = f(xᵢ, β). Choose β to minimise Σ(yᵢ − f(xᵢ, β))². No distribution is assumed — only the form of the mean.

**Block 6 — Simple linear regression, the standard result** `scenes[7].blocks[5]` *(type `formula`)*

minimise Σ(yᵢ − β₀ − β₁xᵢ)²   ⇒   β̂₁ = S_xy / S_xx ,   β̂₀ = ȳ − β̂₁ x̄
where S_xy = Σ(xᵢ−x̄)(yᵢ−ȳ) and S_xx = Σ(xᵢ−x̄)².

**Block 7 — Least squares against maximum likelihood** `scenes[7].blocks[6]` *(type `note`)*

If the errors are independent N(0, σ²), maximising the likelihood IS minimising the sum of squares — the two methods give the same β̂. Without normality least squares still gives the best linear unbiased estimator by Gauss–Markov, but it is no longer a likelihood method. So normality is what makes them coincide; it is not what least squares requires.

**Block 8 — Why these three are one lesson** `scenes[7].blocks[7]` *(type `trap`)*

All three choose θ by making a feature of the model agree with the same feature of the data: moments with moments, fitted frequencies with observed frequencies, fitted values with observed values. None of them maximises a likelihood, and all of them can be computed when the likelihood is intractable. Scene 11 makes the connection exact by deriving least squares as a moment condition.

**Quick check before moving on** `scenes[7].ask`

- *question:* What is being minimised in minimum chi-square and least squares, and how does that differ from matching moments directly?
- *hint on request:* Minimum chi-square weights discrepancies between observed and expected cell proportions; least squares minimises a sum of squared residuals.

---

### Scene 9 of 14 — When the moment estimate is impossible

`scenes[8]` · id `s8` · type `explore` (interactive visualisation) · 7 minutes

**Purpose** `scenes[8].objective`

See the method produce an answer that the data have already ruled out.

**Body** `scenes[8].body[]`

U(0,θ). The moment equation is θ/2 = x̄, so θ̃ = 2x̄. Now take this sample of five: 0.1, 0.3, 0.5, 0.8, 4.2.

Σxᵢ = 5.9, so x̄ = 1.18 and θ̃ = 2.36. But one of the observations is 4.2. The method of moments has just told you the upper limit of the distribution is 2.36, having been shown a value of 4.2.

The picture explains why that is not a near miss but a flat impossibility. The likelihood is zero for every θ below the largest observation — no value of θ smaller than 4.2 could have produced a 4.2 — and then falls away as θ⁻ⁿ above it. Drag the θ slider below 4.2 and the likelihood is identically zero. θ̃ = 2.36 sits in that dead region.

The MLE has no such problem: it is θ̂ = x₍ₙ₎ = 4.2, the cliff edge, the smallest θ consistent with the data. Raise the largest observation on the slider and the MLE tracks it exactly, by construction.

What went wrong is that the moment equation looked only at the mean. One large observation lifts the mean a little and the maximum a lot, and for this family it is the maximum that carries the information — x₍ₙ₎ is sufficient for θ, and x̄ is not. The fix, when a question asks for a usable estimator, is to say so: report θ̂ = x₍ₙ₎, or the unbiased (n+1)x₍ₙ₎/n, and state that the moment estimator is inadmissible here because it can fall below the sample maximum.

**Interactive element** `scenes[8].viz` — live plot of type `unif-likelihood`, initial state n=5, xmax=4.2. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[8].ask`

- *question:* What should you do if a method-of-moments solution falls outside the parameter space?
- *hint on request:* Recognise that the algebraic solution is not an admissible estimate; do not silently treat it as valid.

**Optional deep-dive, opened on demand — The starting value problem, and who solves it** `scenes[8].scenario`

*teaser on the closed card:* Why an actuary fits claim sizes by moments first and by likelihood second.

> An actuary models claim sizes on a motor portfolio as gamma with unknown shape and rate. The likelihood for the gamma shape has no closed-form maximum — it involves the digamma function — so the fit is numerical, and a numerical maximiser has to start somewhere.

> The method of moments gives the starting point in one line. Set the first two sample moments equal to their population values and solve: the shape comes out as x̄² divided by the sample variance, and the rate as x̄ divided by the sample variance. No iteration, no derivative, no software beyond a calculator.

> Those values are usually close enough that the likelihood maximiser converges in a few steps, and far enough from the boundary that it does not wander off into a region where the shape goes negative. Starting a gamma fit from an arbitrary value is how you get a maximiser that fails to converge, or converges to something a long way from the data.

> The division of labour is the point. Moment estimates are consistent, instantaneous and usually less efficient than the MLE; the MLE is efficient but needs a sensible place to begin. The textbook treats them as rival methods; practice treats them as the first and second step of one procedure.

*closing line:* Consistency gets you into the right neighbourhood; the likelihood finds the right house once you are there.

---

### Scene 10 of 14 — Now without the steps — the bias of a moment estimator

`scenes[9]` · id `s9` · type `guided` (guided problem) · 8 minutes

**Purpose** `scenes[9].objective`

Compute a moment estimator's bias from scratch, and see that consistency did not save it.

**Problem put to the learner** `scenes[9].problem`

X₁,…,Xₙ are iid Exponential with rate λ, so E[X] = 1/λ. Find the method of moments estimator of λ. Then, given that ΣXᵢ follows a Gamma(n, rate λ) distribution with E[1/ΣXᵢ] = λ/(n−1) for n > 1, find E[λ̃] and the bias. Evaluate both at n = 5, λ = 2, and say how to remove the bias.

**Hint ladder, revealed one at a time** `scenes[9].hints[]`

1. Direction — the moment equation is one line: set E[X] = x̄ and solve for λ. Write the answer in terms of ΣXᵢ rather than x̄ before you take any expectation, because the fact you have been given is about ΣXᵢ.
2. Method — λ̃ is a constant times 1/ΣXᵢ. Pull the constant out of the expectation and substitute the given value. Do not be tempted to write E[1/X̄] as 1/E[X̄]; that step is false and it is the whole reason this estimator is biased.
3. Next step — bias is E[λ̃] − λ. Simplify it to a single fraction. Once you see the form of E[λ̃], the multiplier that removes the bias should be obvious, and it will give you an estimator you have already met two topics ago.

**Model solution, hidden until requested** `scenes[9].solution[]`

1. `scenes[9].solution[0]` Set up and solve the moment equation.

   ```
   E[X] = 1/λ = x̄   ⇒   λ̃ = 1/x̄ = n / ΣXᵢ
   ```

   Laid out:

   $$E[X] = \frac{1}{λ} = x̄   ⇒   λ̃ = \frac{1}{x̄} = \frac{n}{ΣXᵢ}$$

2. `scenes[9].solution[1]` Note this is also the MLE for this family, as scene 2 showed. Take its expectation using the given fact.

   ```
   E[λ̃] = n · E[1/ΣXᵢ] = n · λ/(n−1) = nλ/(n−1)
   ```

   Laid out:

   $$E[λ̃] = n · E\frac{1}{ΣXᵢ} = n · \frac{λ}{(n−1)} = \frac{nλ}{(n−1)}$$

3. `scenes[9].solution[2]` Subtract λ to get the bias.

   ```
   bias = nλ/(n−1) − λ = λ[ n − (n−1) ] / (n−1) = λ/(n−1)
   ```

   Laid out:

   $$bias = \frac{nλ}{(n−1)} − λ = \frac{λ[ n − (n−1) ]}{(n−1)} = \frac{λ}{(n−1)}$$

4. `scenes[9].solution[3]` Evaluate at n = 5, λ = 2.

   ```
   E[λ̃] = 5(2)/4 = 2.5 ,   bias = 2/4 = 0.5 ,   i.e. 25% too high on average
   ```

   Laid out:

   $$E[λ̃] = \frac{5(2)}{4} = 2.5 ,   bias = \frac{2}{4} = 0.5 ,   i.e. 25% too high on average$$

5. `scenes[9].solution[4]` Remove the bias by rescaling. Multiply by (n−1)/n.

   ```
   λ̂* = (n−1)/n · λ̃ = (n−1)/ΣXᵢ ,   E[λ̂*] = λ  ✓
   ```

   Laid out:

   $$λ̂* = \frac{(n−1)}{n} · λ̃ = \frac{(n−1)}{ΣXᵢ} ,   E[λ̂*] = λ  ✓$$

6. `scenes[9].solution[5]` Confirm the bias vanishes as n grows, which is consistency at work.

   ```
   λ/(n−1) → 0 as n → ∞,  so λ̃ is consistent despite being biased at every finite n
   ```

   Laid out:

   $$\frac{λ}{(n−1)} → 0 as n → ∞,  so λ̃ is consistent despite being biased at every finite n$$

**Final answer given to the learner** `scenes[9].answer`

λ̃ = 1/x̄ = n/ΣXᵢ. E[λ̃] = nλ/(n−1), so the bias is λ/(n−1) — positive, so the estimator overstates the rate. At n = 5, λ = 2 it averages 2.5, a bias of 0.5. Multiplying by (n−1)/n gives the unbiased (n−1)/ΣXᵢ, which is the UMVUE from the Lehmann–Scheffé topic.

**Self-check offered** `scenes[9].check`

Three things to notice. The bias is positive and shrinks like 1/n, so consistency and bias at finite n sit together without contradiction — a question that offers 'it is consistent, therefore unbiased' is offering a false implication. The bias-corrected version is not a new discovery: it is the same (n−1)/ΣX that Lehmann–Scheffé produced, and the same estimator the Cramér–Rao topic showed does NOT attain the variance floor. And the whole calculation turned on E[1/Y] ≠ 1/E[Y]; if you got bias zero, that is the step to re-examine.

---

### Scene 11 of 14 — Six statements — verdict on each before you look

`scenes[10]` · id `s10` · type `trapcheck` (true/false check) · 6 minutes

**Purpose** `scenes[10].objective`

Practise the per-statement discipline the real multi-statement items demand.

**Intro** `scenes[10].intro`

Give every statement a true or false verdict first. In the exam these six would be one question scored all or nothing, so a verdict you skipped is a mark you gambled.

- `scenes[10].items[0]` **Claim:** Method of moments estimators are always unbiased.  
  **Verdict: FALSE.** False. They are consistent, not unbiased. σ̃² = (1/n)Σ(xᵢ−x̄)² has expectation (n−1)σ²/n, and λ̃ = n/ΣX for the exponential rate has bias λ/(n−1).
- `scenes[10].items[1]` **Claim:** For U(0,θ), the moment estimator 2x̄ can be smaller than the largest observation.  
  **Verdict: TRUE.** True, and that is its fatal defect — the estimate then lies in a region the likelihood assigns probability zero. The MLE x₍ₙ₎ cannot do this.
- `scenes[10].items[2]` **Claim:** The method of moments cannot be applied to the Cauchy distribution.  
  **Verdict: TRUE.** True. The Cauchy has no finite mean, so there is no first population moment to equate the sample mean to. The sample mean of a Cauchy sample does not converge.
- `scenes[10].items[3]` **Claim:** For the exponential distribution, the method of moments and maximum likelihood give different estimators of the rate.  
  **Verdict: FALSE.** False — they give the same estimator, n/ΣXᵢ. The two methods coincide for several standard one-parameter families, including the Poisson and the Bernoulli.
- `scenes[10].items[4]` **Claim:** Least squares estimation requires the errors to be normally distributed.  
  **Verdict: FALSE.** False. Least squares assumes only the form of the mean. Normality is what makes it coincide with maximum likelihood, and Gauss–Markov gives it best-linear-unbiased status without any normality at all.
- `scenes[10].items[5]` **Claim:** For multinomial data, the minimum chi-square and maximum likelihood estimators are asymptotically equivalent.  
  **Verdict: TRUE.** True. Both, along with the modified minimum chi-square estimator, are BAN and have the same limiting distribution. They differ at finite n, where the modified version is the tractable one.

---

### Scene 12 of 14 — Transfer — least squares as a moment condition

`scenes[11]` · id `s11` · type `guided` (guided problem) · 9 minutes

**Purpose** `scenes[11].objective`

Derive the normal equations from two moment conditions, and see the three methods as one.

**Problem put to the learner** `scenes[11].problem`

Take the simple linear model yᵢ = β₀ + β₁xᵢ + εᵢ with E[εᵢ] = 0 and E[xᵢεᵢ] = 0. Treat these two conditions as moment conditions and derive the estimating equations for β₀ and β₁. Show they are the ordinary least squares normal equations, and solve them.

**Hint ladder, revealed one at a time** `scenes[11].hints[]`

1. Direction — a moment condition says a population expectation is zero. The method of moments replaces that expectation by its sample average and solves. So write each condition with εᵢ replaced by yᵢ − β₀ − β₁xᵢ, then average over the sample and set the average to zero.
2. Method — two conditions, two unknowns, so you will get two linear equations. Expand the sums and group the β terms on one side. Compare what you get with the normal equations as you learned them for regression.
3. Next step — to solve, use the first equation to express β₀ in terms of β₁, substitute into the second, and recognise the result as a ratio of sums of cross-products about the means.

**Model solution, hidden until requested** `scenes[11].solution[]`

1. `scenes[11].solution[0]` Replace each population condition by its sample analogue, with the residual in place of the error.

   ```
   (1/n) Σ (yᵢ − β₀ − β₁xᵢ) = 0     (i)
(1/n) Σ xᵢ(yᵢ − β₀ − β₁xᵢ) = 0    (ii)
   ```

   Laid out:

   $$\frac{1}{n} Σ (yᵢ − β₀ − β₁xᵢ) = 0     (i)
\frac{1}{n} Σ xᵢ(yᵢ − β₀ − β₁xᵢ) = 0    (ii)$$

2. `scenes[11].solution[1]` Clear the 1/n and expand. These are the normal equations.

   ```
   Σyᵢ = n β₀ + β₁ Σxᵢ          (i′)
Σxᵢyᵢ = β₀ Σxᵢ + β₁ Σxᵢ²      (ii′)
   ```

3. `scenes[11].solution[2]` Divide (i′) by n to get the intercept in terms of the slope.

   ```
   ȳ = β₀ + β₁x̄   ⇒   β̂₀ = ȳ − β̂₁x̄
   ```

4. `scenes[11].solution[3]` Substitute into (ii′) and collect the β₁ terms.

   ```
   Σxᵢyᵢ − n x̄ȳ = β₁ ( Σxᵢ² − n x̄² )
   ```

5. `scenes[11].solution[4]` Both sides are now sums of squares and cross-products about the means.

   ```
   S_xy = β₁ S_xx   ⇒   β̂₁ = S_xy / S_xx
   ```

   Laid out:

   $$S_xy = β₁ S_xx   ⇒   β̂₁ = \frac{S_xy}{S_xx}$$

6. `scenes[11].solution[5]` Note what the first condition alone has delivered.

   ```
   β̂₀ = ȳ − β̂₁x̄  ⇒  the fitted line passes through (x̄, ȳ), always
   ```

**Final answer given to the learner** `scenes[11].answer`

The two moment conditions give Σ(yᵢ − β₀ − β₁xᵢ) = 0 and Σxᵢ(yᵢ − β₀ − β₁xᵢ) = 0 — precisely the OLS normal equations — with solution β̂₁ = S_xy/S_xx and β̂₀ = ȳ − β̂₁x̄. Least squares is the method of moments applied to the conditions 'the errors have zero mean' and 'the errors are uncorrelated with the regressor'.

**Self-check offered** `scenes[11].check`

Two things to take away. First, nothing in this derivation mentioned a distribution: the estimator came out of two expectations being zero, which is why least squares needs no normality. Second, the same estimator arrives from minimising a sum of squares, from maximising a normal likelihood, and from these moment conditions — the Berkeley note in the references adds a Bayesian route as a fourth. When a question asks you to 'derive the least squares estimators', any of these is a valid derivation, and the moment route is the shortest to write.

---

### Scene 13 of 14 — What you should now be able to do unaided

`scenes[12]` · id `s12` · type `summary` (summary) · 3 minutes

**Purpose** `scenes[12].objective`

Close the loop before the test.

**Body** `scenes[12].body[]`

Count the unknown parameters, write that many moment equations, and solve them — dividing one by the other when a parameter appears in both.

Quote the standard results from memory: Gamma β̃ = m₂/x̄ and α̃ = x̄²/m₂; U(a,b) endpoints x̄ ∓ √(3m₂); U(0,θ) gives 2x̄; N(μ,σ²) gives x̄ and m₂ with divisor n.

Claim consistency and asymptotic normality, and refuse to claim unbiasedness, efficiency or uniqueness.

Check every moment estimate against the parameter space, and against the sample maximum for a uniform.

Say immediately why the method fails for the Cauchy, and that the failure is the answer.

Write the minimum chi-square and modified minimum chi-square criteria, and name the data they need.

Derive the least squares normal equations by either route, and keep straight that normality is what joins least squares to maximum likelihood rather than something least squares assumes.

The mastery test is ten unseen questions across all of this. Hints are off. The pass is 80% overall with 70% floors on the numerical and multi-statement items.

---

### Scene 14 of 14 — Mastery test

`scenes[13]` · id `s13` · type `quiz` (mastery test) · 12 minutes

**Purpose** `scenes[13].objective`

Demonstrate it independently, on unseen questions.

Draws from the pool reproduced below. `scenes[13].setId` = `inference_t5_mastery`

---

## Revision material `revision`

**Revision sheet** `revision.sheet[]` (16 lines)

1. `[0]` Method of moments: equate the first k sample moments to the first k population moments and solve for the k parameters.
2. `[1]` Raw moments: m_r' = (1/n)Σxᵢ^r  matched to  μ_r' = E[X^r].  Central: m₂ = (1/n)Σ(xᵢ−x̄)² matched to Var(X). Use whichever makes the algebra shorter.
3. `[2]` One unknown → one equation (usually E[X] = x̄). Two unknowns → add Var(X) = m₂.
4. `[3]` Gamma(α, β) with mean αβ, variance αβ²:   β̃ = m₂/x̄,   α̃ = x̄²/m₂.
5. `[4]` U(a,b):   ã = x̄ − √(3m₂),   b̃ = x̄ + √(3m₂).   For U(0,θ):  θ̃ = 2x̄.
6. `[5]` N(μ,σ²):   μ̃ = x̄,   σ̃² = m₂ = (1/n)Σ(xᵢ−x̄)².  Note the divisor n, not n−1 — the moment estimator of σ² is biased.
7. `[6]` Exponential(rate λ):   λ̃ = 1/x̄ = n/ΣX.  Same as the MLE, and biased: E[λ̃] = nλ/(n−1), bias = λ/(n−1).
8. `[7]` GUARANTEED: consistency (WLLN plus continuous mapping) and asymptotic normality.
9. `[8]` NOT guaranteed: unbiasedness, efficiency, uniqueness, or even an estimate inside the parameter space.
10. `[9]` Fails outright when the moment does not exist — Cauchy has no mean, so there is nothing to match.
11. `[10]` Minimum chi-square: choose θ to minimise Σ (Oᵢ − npᵢ(θ))² / (npᵢ(θ)) over the k cells. Needs grouped or categorical data.
12. `[11]` Modified minimum chi-square puts Oᵢ in the denominator instead: Σ (Oᵢ − npᵢ(θ))² / Oᵢ. Easier to minimise, same large-sample behaviour.
13. `[12]` For multinomial data, minimum chi-square, modified minimum chi-square and ML are all BAN and asymptotically equivalent.
14. `[13]` Least squares: minimise Σ(yᵢ − ŷᵢ)². Needs no distributional assumption; coincides with ML when the errors are normal.
15. `[14]` The normal equations ARE moment conditions: E[ε] = 0 and E[Xε] = 0 in their sample form.
16. `[15]` β̂₁ = Sxy/Sxx,   β̂₀ = ȳ − β̂₁x̄.

**Flashcards** `revision.cards[]`

| Front | Back |
|---|---|
| State the method of moments in one sentence. | Equate the first k sample moments to the corresponding population moments and solve the resulting k equations for the k unknown parameters. |
| What does the method of moments guarantee? | Consistency and asymptotic normality. Not unbiasedness, not efficiency, not a legal estimate. |
| Moment estimators for Gamma(α, β)? | β̃ = m₂/x̄ and α̃ = x̄²/m₂, from αβ = x̄ and αβ² = m₂. |
| Moment estimator of θ for U(0,θ), and its defect? | θ̃ = 2x̄. It can come out smaller than the largest observation, which is impossible — the MLE x₍ₙ₎ never does. |
| Why does the method fail for the Cauchy distribution? | The Cauchy has no finite mean, so there is no first population moment to equate the sample mean to. |
| Moment estimator of σ² in N(μ,σ²), and is it unbiased? | σ̃² = (1/n)Σ(xᵢ−x̄)². Biased: E[σ̃²] = (n−1)σ²/n. Multiplying by n/(n−1) gives the unbiased s². |
| Write the minimum chi-square criterion. | Minimise Σ (Oᵢ − npᵢ(θ))²/(npᵢ(θ)) over θ, summed over the cells. The modified version divides by Oᵢ instead. |
| In what sense are the normal equations moment conditions? | They are the sample versions of E[ε] = 0 and E[Xε] = 0 — the residuals are made to have zero mean and zero correlation with the regressor. |
| When do least squares and maximum likelihood agree? | When the errors are independent normal with constant variance: maximising that likelihood is minimising the sum of squares. |
| Why is the method of moments still worth knowing if the MLE is better? | It is almost always computable in closed form, it needs no likelihood, and it supplies the starting value for the iteration that finds the MLE. |

**Memory aids** `revision.tricks[]`

- `[0]` **k unknowns, k moments** — Count the parameters first. Starting with one equation for a two-parameter family is the commonest way to waste time.
- `[1]` **Divide to kill a parameter** — Var ÷ mean cancels the shape in the gamma and leaves the scale alone. Look for it whenever a parameter multiplies both.
- `[2]` **Divisor n, not n−1** — The moment estimator of σ² is Σ(xᵢ−x̄)²/n. The n−1 version is a separate, bias-corrected estimator.
- `[3]` **No mean, no method** — The Cauchy has no finite first moment, so there is nothing to equate x̄ to. The method fails, and that failure IS the answer.

**Elimination shortcuts for multiple-choice items** `revision.shortcuts[]`

- `[0]` Gamma(α,β): β̃ = m₂/x̄ and α̃ = x̄²/m₂.
- `[1]` U(a,b): ã = x̄ − √(3m₂), b̃ = x̄ + √(3m₂). U(0,θ): θ̃ = 2x̄. U(−θ,θ): θ̃ = √(3m₂).
- `[2]` When the first moment carries no parameter — as for U(−θ,θ) — skip it and match the variance.
- `[3]` Least squares is the method of moments applied to E[ε] = 0 and E[Xε] = 0.

**If nothing else is remembered** `revision.remember[]`

- `[0]` Guaranteed: consistency and asymptotic normality. NOT guaranteed: unbiasedness, efficiency, uniqueness, or a legal estimate.
- `[1]` Always check the answer against the parameter space — and against the sample maximum for a uniform.

**Errors to avoid** `revision.traps[]`

- `[0]` Using n−1 in the moment estimator of σ². The method gives the divisor n; the n−1 version is a separate, bias-corrected estimator.
- `[1]` Quoting the moment estimate for U(0,θ) without checking it against the largest observation.
- `[2]` Claiming the method of moments is unbiased because it is consistent. The two are different properties.
- `[3]` Matching E[X²] when Var(X) would have given a one-line solution, or the reverse — pick the form that cancels.
- `[4]` Treating minimum chi-square as a general method. It needs the data grouped into cells with expected frequencies.

---

## Mastery pool — all 20 items with answer keys `qsets/mastery`

Ten are drawn per attempt at 3 easy / 5 moderate / 2 hard. Keys are distributed five to each option letter. Please check each item for a second defensible answer as well as for the correctness of its stated key and explanation.

### Q1 — `inf-t5-m-01` *(single, easy)*

The method of moments estimator of a k-parameter family is obtained by:

*Options* `.options[]`:

- **A.** equating the first k sample moments to the corresponding population moments and solving  ← key
- **B.** minimising the sum of squared deviations of the observations from their mean
- **C.** maximising the likelihood subject to the first k moments being correct
- **D.** equating the sample median and quartiles to their population counterparts

*Explanation* `.explanation`: The method matches moments, nothing more. Option C describes a constrained likelihood method, not this one; C is least squares applied to a location problem; D is a quantile-matching method, which exists but is not the method of moments.

### Q2 — `inf-t5-m-02` *(numeric, moderate)*

X₁,…,Xₙ are iid Gamma(α, β) with E[X] = αβ and Var(X) = αβ². A sample gives x̄ = 10 and m₂ = 5. Give the method of moments estimates of α and β.

*Options* `.options[]`:

- **A.** α̃ = 0.5, β̃ = 20
- **B.** α̃ = 20, β̃ = 0.5  ← key
- **C.** α̃ = 20, β̃ = 2
- **D.** α̃ = 2, β̃ = 5

*Explanation* `.explanation`: Divide the variance equation by the mean equation: β̃ = m₂/x̄ = 5/10 = 0.5. Then α̃ = x̄/β̃ = x̄²/m₂ = 100/5 = 20. Check: α̃β̃ = 20(0.5) = 10 = x̄ ✓ and α̃β̃² = 20(0.25) = 5 = m₂ ✓.

*Arithmetic check* `.check`: Reconstruct both moments from your answers. If α̃β̃ does not come back to x̄, you have inverted the ratio.

### Q3 — `inf-t5-m-03` *(multi, hard)*

Consider the properties of method of moments estimators.

*Statements to judge* `.statements[]`:

- **A.** Method of moments estimators are consistent under mild conditions.
- **B.** Method of moments estimators are unbiased.
- **C.** Method of moments estimators are asymptotically more efficient than maximum likelihood estimators.
- **D.** A method of moments estimate can fall outside the parameter space.

*Options* `.options[]`:

- **A.** B and C only
- **B.** A, B and D only
- **C.** A and D only  ← key
- **D.** A, C and D only

*Explanation* `.explanation`: A is true — consistency follows from the weak law applied to the sample moments. B is false: moment estimators are frequently biased, as σ̃² and the exponential rate both show. C is false: the method uses only the first k moments, which are not in general sufficient, so it is typically LESS efficient than the MLE. D is true, and 2x̄ for U(0,θ) is the standard example.

*Verdict on each statement* `.verdicts`:

- **A — true.** Sample moments converge to population moments, and the estimator is a continuous function of them.
- **B — false.** σ̃² has expectation (n−1)σ²/n; the exponential rate estimator has bias λ/(n−1).
- **C — false.** The other way round. Discarding everything beyond the first k moments costs efficiency.
- **D — true.** 2x̄ can be below the sample maximum for U(0,θ), which no legal θ can be.

### Q4 — `inf-t5-m-04` *(numeric, moderate)*

X₁,…,Xₙ are iid Uniform(a, b). A sample gives x̄ = 8 and m₂ = 12. Give the method of moments estimates of a and b.

*Options* `.options[]`:

- **A.** ã = 4, b̃ = 12
- **B.** ã = 2, b̃ = 12
- **C.** ã = −4, b̃ = 20
- **D.** ã = 2, b̃ = 14  ← key

*Explanation* `.explanation`: (b−a)²/12 = m₂ gives b − a = √(12 × 12) = 12, so half the range is 6; and (a+b)/2 = 8. Hence ã = 8 − 6 = 2 and b̃ = 8 + 6 = 14. Check: mean (2+14)/2 = 8 ✓ and (14−2)²/12 = 144/12 = 12 ✓.

*Arithmetic check* `.check`: The two estimates must be symmetric about x̄. If they are not equidistant from 8, the sum equation has been mishandled.

### Q5 — `inf-t5-m-05` *(single, easy)*

For which distribution can the method of moments not be applied at all?

*Options* `.options[]`:

- **A.** Cauchy, because it has no finite mean  ← key
- **B.** Poisson(λ), because the mean and variance are equal
- **C.** Gamma(α,β), because there are two parameters
- **D.** Uniform(0,θ), because the support depends on θ

*Explanation* `.explanation`: The method needs the population moments to exist, and the Cauchy has no finite mean — there is nothing for x̄ to be equated to. The uniform is awkward but perfectly solvable (2x̄ for U(0,θ)); two parameters just means two equations; and the Poisson's equal mean and variance is a convenience, not an obstacle.

### Q6 — `inf-t5-m-06` *(numeric, moderate)*

X₁,…,X₆ are iid Exponential with rate λ = 3. The method of moments estimator is λ̃ = n/ΣXᵢ, and E[1/ΣXᵢ] = λ/(n−1). Give E[λ̃] and the bias.

*Options* `.options[]`:

- **A.** E[λ̃] = 2.5, bias = −0.5
- **B.** E[λ̃] = 3.6, bias = 0.6  ← key
- **C.** E[λ̃] = 3.6, bias = 3.6
- **D.** E[λ̃] = 3, bias = 0

*Explanation* `.explanation`: E[λ̃] = n·λ/(n−1) = 6(3)/5 = 3.6, so the bias is 3.6 − 3 = 0.6 = λ/(n−1) = 3/5. The estimator overstates the rate, and the bias shrinks like 1/n — consistent but biased at every finite n. Option D comes from the false step E[1/X̄] = 1/E[X̄].

*Arithmetic check* `.check`: Bias is E[λ̃] − λ, not E[λ̃] itself. And the sign should be positive here: 1/ΣX is a convex function of ΣX, so the expectation sits above the value at the mean.

### Q7 — `inf-t5-m-07` *(multi, hard)*

Consider minimum chi-square and least squares estimation.

*Statements to judge* `.statements[]`:

- **A.** Minimum chi-square estimation chooses θ to minimise Σ(Oᵢ − npᵢ(θ))²/(npᵢ(θ)).
- **B.** Modified minimum chi-square uses the expected frequency npᵢ(θ) in the denominator.
- **C.** Least squares and maximum likelihood give the same estimates when the errors are independent normal with constant variance.
- **D.** For multinomial data, minimum chi-square and maximum likelihood estimators are asymptotically equivalent.

*Options* `.options[]`:

- **A.** C and D only
- **B.** B and C only
- **C.** A, C and D only  ← key
- **D.** A and B only

*Explanation* `.explanation`: A is true — that is the criterion, with expected frequencies in the denominator. B is false: the modified version divides by the OBSERVED frequency Oᵢ, which is what makes it easier to minimise. C is true, and it is why normality is not an assumption of least squares but the condition under which it coincides with maximum likelihood. D is true: both chi-square estimators and the MLE are BAN for multinomial data.

*Verdict on each statement* `.verdicts`:

- **A — true.** The Pearson statistic treated as a function of θ and minimised.
- **B — false.** The modified version puts the observed Oᵢ underneath, so θ appears only in the numerator.
- **C — true.** Maximising that normal likelihood is minimising the sum of squares — same β̂.
- **D — true.** Both are BAN with the same limiting distribution; they differ only at finite n.

### Q8 — `inf-t5-m-08` *(numeric, moderate)*

A sample of n = 10 from N(μ, σ²) gives Σxᵢ = 50 and Σxᵢ² = 290. Give the method of moments estimates of μ and σ².

*Options* `.options[]`:

- **A.** μ̃ = 5, σ̃² = 4.44
- **B.** μ̃ = 5, σ̃² = 29
- **C.** μ̃ = 50, σ̃² = 4
- **D.** μ̃ = 5, σ̃² = 4  ← key

*Explanation* `.explanation`: x̄ = 50/10 = 5, so μ̃ = 5. The moment estimator of σ² is m₂ = (1/n)Σxᵢ² − x̄² = 29 − 25 = 4. Option A is the unbiased s² = n·m₂/(n−1) = 40/9 = 4.44, which is a different estimator — the method of moments gives the divisor n.

*Arithmetic check* `.check`: The moment estimator of σ² divides by n. 4.44 is the n−1 version; if you reached it, you applied Bessel's correction that the method does not ask for.

### Q9 — `inf-t5-m-09` *(numeric, hard)*

A sample of n = 6 from Uniform(0, θ) has x̄ = 3 and largest observation x₍₆₎ = 7. Give the method of moments estimate of θ and say whether it is usable.

*Options* `.options[]`:

- **A.** θ̃ = 6, and it is not usable because it is below x₍₆₎ = 7  ← key
- **B.** θ̃ = 3.5, and it is not usable because it is below x₍₆₎ = 7
- **C.** θ̃ = 7, since the method returns the sample maximum
- **D.** θ̃ = 6, and it is usable since 6 is close to 7

*Explanation* `.explanation`: θ/2 = x̄ gives θ̃ = 2x̄ = 6. But an observation of 7 was recorded, and no θ below 7 can produce a 7 — the likelihood is exactly zero there, so the estimate is inadmissible. Report the MLE θ̂ = x₍₆₎ = 7, or the unbiased (n+1)x₍ₙ₎/n = 7(7)/6 ≈ 8.17, and say why.

*Arithmetic check* `.check`: Always compare a uniform moment estimate with the sample maximum. 'Close' is not a defence: below the maximum means zero likelihood, not low likelihood.

### Q10 — `inf-t5-m-10` *(order, easy)*

Arrange the steps of the method of moments in the order that avoids dead ends.

*Steps to order* `.items[]`:

- A. Write E[X], and Var(X) if needed, in terms of the parameters
- B. Check the solution lies in the parameter space
- C. Count the unknown parameters
- D. Equate to x̄ and m₂ and solve

*Options* `.options[]`:

- **A.** A, D, C, B
- **B.** C, A, D, B  ← key
- **C.** A, C, D, B
- **D.** C, D, A, B

*Explanation* `.explanation`: Count the parameters first, so you know how many equations to write — starting with one equation for a two-parameter family is the commonest way to waste time. Then write the population moments as expressions in the parameters, equate them to the sample moments and solve, and finally check the solution lies in the parameter space, which for a uniform means checking it against the sample maximum.

### Q11 — `inf-t5-m-11` *(single, easy)*

The method of moments requires that:

*Options* `.options[]`:

- **A.** the likelihood function be differentiable
- **B.** the support of the density be free of the parameter
- **C.** the population moments being matched exist and are finite  ← key
- **D.** the sample size exceed the number of parameters by at least ten

*Explanation* `.explanation`: The method matches moments, so the moments have to exist — this is exactly why it cannot be applied to the Cauchy. Differentiability of the likelihood is a maximum likelihood concern, a moving support troubles the Cramér–Rao bound rather than this method, and there is no sample-size rule of that kind.

### Q12 — `inf-t5-m-12` *(numeric, moderate)*

X₁,…,Xₙ are iid Exponential with mean θ. A sample of n = 12 gives Σxᵢ = 60. Give the method of moments estimate of θ, and say whether it is unbiased.

*Options* `.options[]`:

- **A.** θ̃ = 5, and it is biased upward
- **B.** θ̃ = 0.2, and it is unbiased
- **C.** θ̃ = 12/60 = 0.2, and it is biased
- **D.** θ̃ = 5, and it is unbiased  ← key

*Explanation* `.explanation`: E[X] = θ, so the moment equation is θ = x̄ = 60/12 = 5. Since E[X̄] = θ exactly, this estimator is unbiased at every n. Note the contrast with the RATE parameterisation of the same family, where λ̃ = 1/x̄ is biased: unbiasedness is a property of the estimator, not of the family.

*Arithmetic check* `.check`: The target here is the MEAN, so the moment equation is solved directly and no reciprocal is taken. 0.2 is the rate, not the mean.

### Q13 — `inf-t5-m-13` *(multi, hard)*

Consider how the method of moments compares with maximum likelihood.

*Statements to judge* `.statements[]`:

- **A.** The moment estimator is usually available in closed form where the MLE is not.
- **B.** For some standard families the two methods give the same estimator.
- **C.** The moment estimator has smaller asymptotic variance than the MLE.
- **D.** The moment estimate is commonly used as the starting value for an iterative search for the MLE.

*Options* `.options[]`:

- **A.** A, B and D only  ← key
- **B.** A and C only
- **C.** B and C only
- **D.** A, B and C only

*Explanation* `.explanation`: A is true — this is the usual reason to reach for it. B is true: for the exponential, Poisson, Bernoulli and the normal mean the two methods give the same estimator. C is false: the moment estimator is generally LESS efficient, because it uses only the first k moments rather than the whole likelihood. D is true, and it is the standard practical use of the method today.

*Verdict on each statement* `.verdicts`:

- **A — true.** Solving moment equations is algebra; solving the likelihood equation may need a computer.
- **B — true.** The exponential rate, the Poisson mean and the Bernoulli p all coincide.
- **C — false.** Backwards. Discarding everything past the kth moment costs efficiency.
- **D — true.** Cheap to compute and close enough to start a Newton iteration from.

### Q14 — `inf-t5-m-14` *(numeric, moderate)*

X₁,…,Xₙ are iid Uniform(−θ, θ) with θ > 0. A sample gives x̄ = 0.2 and m₂ = 12. Give the method of moments estimate of θ.

*Options* `.options[]`:

- **A.** θ̃ = 12
- **B.** θ̃ = 6  ← key
- **C.** θ̃ = 3.46
- **D.** θ̃ = 0.4

*Explanation* `.explanation`: E[X] = 0 whatever θ is, so the first moment equation is useless and you must match the variance instead: Var(X) = (2θ)²/12 = θ²/3 = m₂, giving θ̃ = √(3m₂) = √36 = 6. Option D is 2x̄, which would be the answer for U(0,θ) and is meaningless here.

*Arithmetic check* `.check`: When the first moment carries no parameter, skip it and go to the second. Reading the question for which endpoints are known is the whole task.

### Q15 — `inf-t5-m-15` *(single, moderate)*

For U(0,θ), the moment estimator 2x̄ can fall below the sample maximum. The correct response in an exam is to:

*Options* `.options[]`:

- **A.** round the estimate up to the sample maximum and present it as the moment estimate
- **B.** discard the largest observation and recompute
- **C.** report that the estimate is inadmissible and give the MLE x₍ₙ₎ instead, with the reason  ← key
- **D.** report 2x̄ anyway, since the method was applied correctly

*Explanation* `.explanation`: The method was applied correctly and still produced something impossible, which is itself the examinable point: the moment estimate can land outside the parameter space. Saying so, and offering x₍ₙ₎ or the unbiased (n+1)x₍ₙ₎/n, is the complete answer. Rounding or discarding data would be inventing a different estimator and hiding the defect.

### Q16 — `inf-t5-m-16` *(numeric, hard)*

X₁,…,Xₙ are iid Gamma(α, β) with E[X] = αβ and Var(X) = αβ². A sample gives x̄ = 4 and m₂ = 16. Give the method of moments estimates, and comment on α̃.

*Options* `.options[]`:

- **A.** α̃ = 1, β̃ = 16
- **B.** α̃ = 4, β̃ = 1 — a shape of 4 with unit scale
- **C.** α̃ = 16, β̃ = 0.25
- **D.** α̃ = 1, β̃ = 4 — the estimate says the data look exponential  ← key

*Explanation* `.explanation`: β̃ = m₂/x̄ = 16/4 = 4 and α̃ = x̄²/m₂ = 16/16 = 1. A gamma with shape 1 is exactly the exponential distribution, so the moment estimates are telling you the sample is consistent with an exponential of mean 4 — which is also what a variance equal to the squared mean indicates, since that is the exponential's signature.

*Arithmetic check* `.check`: Shape 1 is not a failure of the method; it is a meaningful answer. The clue was m₂ = x̄², which is Var = mean² — the exponential.

### Q17 — `inf-t5-m-17` *(multi, moderate)*

Consider least squares estimation.

*Statements to judge* `.statements[]`:

- **A.** Least squares requires no distributional assumption about the errors.
- **B.** Under the Gauss–Markov conditions, least squares gives the best linear unbiased estimator.
- **C.** Least squares always coincides with maximum likelihood.
- **D.** The fitted regression line always passes through (x̄, ȳ).

*Options* `.options[]`:

- **A.** A, B and D only  ← key
- **B.** A and C only
- **C.** B and C only
- **D.** A, B and C only

*Explanation* `.explanation`: A is true — least squares assumes only the form of the mean. B is true, and is the Gauss–Markov theorem. C is false: least squares and maximum likelihood coincide only under normal errors; without normality least squares is still BLUE but is not a likelihood method. D is true, and it follows from the first normal equation.

*Verdict on each statement* `.verdicts`:

- **A — true.** Only E[yᵢ] = β₀ + β₁xᵢ is assumed; the error distribution is left open.
- **B — true.** Gauss–Markov: BLUE under zero-mean, constant-variance, uncorrelated errors.
- **C — false.** Only when the errors are independent normal with constant variance.
- **D — true.** β̂₀ = ȳ − β̂₁x̄ rearranges to ȳ = β̂₀ + β̂₁x̄.

### Q18 — `inf-t5-m-18` *(numeric, moderate)*

A simple linear regression on n = 5 points gives S_xx = 20, S_xy = 30, x̄ = 4 and ȳ = 10. Give the least squares estimates of the slope and intercept.

*Options* `.options[]`:

- **A.** β̂₁ = 0.667, β̂₀ = 7.33
- **B.** β̂₁ = 1.5, β̂₀ = 4  ← key
- **C.** β̂₁ = 1.5, β̂₀ = 16
- **D.** β̂₁ = 1.5, β̂₀ = 10

*Explanation* `.explanation`: β̂₁ = S_xy/S_xx = 30/20 = 1.5, then β̂₀ = ȳ − β̂₁x̄ = 10 − 1.5(4) = 10 − 6 = 4. Option A inverts the ratio to S_xx/S_xy, and option C adds rather than subtracts in the intercept formula.

*Arithmetic check* `.check`: Substitute back: at x = x̄ = 4 the line gives 4 + 1.5(4) = 10 = ȳ ✓. The line must pass through the point of means.

### Q19 — `inf-t5-m-19` *(single, easy)*

Modified minimum chi-square estimation differs from minimum chi-square in that it:

*Options* `.options[]`:

- **A.** requires the data to be ungrouped
- **B.** maximises the likelihood instead of minimising a distance
- **C.** uses the observed frequency Oᵢ in the denominator rather than the expected npᵢ(θ)  ← key
- **D.** minimises the absolute deviations instead of the squared ones

*Explanation* `.explanation`: Putting Oᵢ underneath removes θ from the denominator, so the quantity to minimise is far simpler — the parameter appears only in the numerator. The two versions, and the MLE, are all BAN for multinomial data and asymptotically equivalent; they differ only at finite n, where the modified version is the one you can solve by hand.

### Q20 — `inf-t5-m-20` *(order, easy)*

To estimate two parameters by the method of moments, arrange these steps.

*Steps to order* `.items[]`:

- A. Express E[X] and Var(X) in terms of the parameters
- B. Check the solution lies in the parameter space
- C. Count the unknown parameters
- D. Equate to x̄ and m₂ and solve

*Options* `.options[]`:

- **A.** A, C, D, B
- **B.** C, D, A, B
- **C.** A, D, C, B
- **D.** C, A, D, B  ← key

*Explanation* `.explanation`: Count the parameters first so you write the right number of equations. Then express the mean and the variance in terms of them, set those equal to x̄ and m₂ and solve — dividing one equation by the other when a parameter appears in both — and finally check the answer lies inside the parameter space.

---

## Authoring and verification record `provenance`

Reproduced verbatim. It records what changed in each version and how each derivation was checked, including the findings of the two previous review rounds and the reasons some of their recommendations were declined.

> Review pass, October 2026: 5 per-scene quick checks added on theory, worked and explore scenes from a third-party module review, each read for correctness before import; a further set offered for completion and guided scenes was declined, since those scenes already end with the learner writing an answer. Theory, worked examples and practice authored for this platform against the UGC NET Statistics syllabus. Previous-year questions are stored separately and carry their exam cycle.

