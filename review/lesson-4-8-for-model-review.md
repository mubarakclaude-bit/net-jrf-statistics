# Lesson 4.8 — Decision Theory: Loss, Risk, Admissibility and Minimax

Complete authored content of one lesson from a UGC-NET Statistics (Code 107) preparation application, extracted from the application's own content files.

| | |
|---|---|
| Content version | 1.1 |
| Scenes | 14 |
| Core scenes | 14 |
| Optional JRF-extension scenes | 0 |
| Estimated learner time | 93 minutes |
| Mastery pool | 20 items |
| Position in the app | Statistical Inference → Decision theory → Loss, risk, admissibility, minimax |
| Engine | Estimation and inference — risk as a curve, and the two ways of collapsing it to a number |
| Pool label | Decision Theory: Loss, Risk, Admissibility and Minimax — mastery test (unseen) |
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

1. Define loss, decision rule, risk and Bayes risk, and say which are functions of θ and which are numbers.

2. Decide whether one rule dominates another, and hence whether a rule is admissible.

3. Define the minimax criterion and compute a minimax value by flattening a risk curve.

4. Apply the three relations between Bayes, minimax and admissible rules, and state what does not follow.

5. Derive the minimax estimator of a binomial proportion and identify the least favourable prior.

6. Translate a testing problem into decision-theoretic language and say why Neyman–Pearson is not minimax.

**Assumed prior knowledge** `prereq[]`

- `prereq[0]` **Loss functions, decision rules and expectation over the sample** — Risk is an expectation over the data with θ fixed, and keeping that straight is most of the topic.
- `prereq[1]` **The bias-variance decomposition of mean squared error** — Under squared-error loss, risk = variance + bias², and that identity does all the arithmetic here.
- `prereq[2]` **Mean and variance of a binomial count and proportion** — The worked example and the guided problem are both binomial, and p(1−p)/n is the curve everything is compared against.
- `prereq[3]` **Bayes estimators as posterior summaries** — Minimax rules are found by choosing a prior that flattens the risk, so the posterior-mean formula is the candidate family.

**Misconceptions the lesson is built to pre-empt** `traps[]`

- Risk is a function of θ; Bayes risk and the minimax value are the numbers derived from it.

- Admissible does not imply minimax, and minimax does not imply admissible without uniqueness.

- A Bayes rule is minimax only if its risk is constant — and constant risk alone is not sufficient either.

- A rule that ignores the data entirely is admissible, which is what makes admissibility weak.

- The MLE of a normal mean vector is inadmissible for dimension three or more, by James–Stein.

- Neyman–Pearson constrains the size and maximises power; it does not minimise the maximum error probability.

- Under squared-error loss, risk includes the squared bias, so a biased rule's variance is not its risk.

- For weighted absolute loss the Bayes rule is a quantile, not the median, and it moves away from the costlier error.

**Assessment policy** `mastery`

- 10 items drawn per attempt from a pool of 20, mix 3 easy, 5 moderate, 2 hard
- pass mark 80%, no hints during the test, retest after 7 days
- `mastery.note`: Platform settings, not an NTA rule. Ten drawn from a pool of twenty at 3 easy / 5 moderate / 2 hard; a retake draws again, holding the mix and pulling back items previously got wrong.

**Sources** `refs[]`

- `refs[0]` **Elementary Decision Theory** — University of Washington STAT 581, Yen-Chi Chen, Loss, risk, Bayes risk, admissibility, minimax and least favourable priors (Graduate lecture notes, free). Covers every definition in this lesson in the same order, including the least favourable prior, which most undergraduate texts leave out. The closest free match to scenes 4 and 10.
- `refs[1]` **Mathematical Statistics 18.655 — lecture notes** — MIT OpenCourseWare, Session 4, The Decision Theoretic Framework (Graduate lecture notes (PDF), free). Sets up the decision problem formally and proves the relation this lesson leans on: a Bayes rule with constant risk is minimax.
- `refs[2]` **Theory of Point Estimation, 2nd edition** — Lehmann and Casella, Chapter 1 (decision theory) and Chapter 5 (minimax estimation) (Textbook). The standard source for admissibility and minimaxity. Chapter 5 derives the binomial minimax estimator (x + sqrt(n)/2)/(n + sqrt(n)) that scene 5 builds from scratch, and proves it is minimax.
- `refs[3]` **Statistical Inference, 2nd edition** — Casella and Berger, Section 7.3.4, Loss function optimality (Textbook). The gentler account, at the level NET asks. Read this first if the Lehmann and Casella treatment is heavier than you need.
- `refs[4]` **Testing Statistical Hypotheses, 3rd edition** — Lehmann and Romano, Chapter 1, The general decision problem (Textbook). Where the translation of testing into decision-theoretic language in scene 9 comes from, and why Neyman-Pearson constrains one error rather than minimising the maximum.

---

## The lesson, scene by scene

### Scene 1 of 14 — Before the lesson — four things it will assume

`scenes[0]` · id `s0` · type `foundation` (prerequisite check) · 5 minutes

**Purpose** `scenes[0].objective`

Have loss, expectation over the sample, and the bias-variance split ready, so risk is a quantity you can compute rather than a definition to recite.

**Body** `scenes[0].body[]`

Decision theory is the frame the rest of Unit IV sits inside. Estimation, testing and interval construction are all decisions; loss and risk are the language that lets them be compared. The syllabus sets this topic at State, so the examinable content is definitions and relations rather than hard derivations — but the definitions are only usable if you can compute a risk, and that is what these four checks are for.

If they are solid, the whole topic is four definitions and three relations between them.

**Check 1** `scenes[0].items[0]`

- *asks:* What is a loss function, a decision rule, and the risk of a decision rule?
- *expected answer* `.recall`: A loss function L(θ, a) is the penalty for taking action a when the truth is θ. A decision rule δ(x) maps each possible sample to an action. The risk is the expected loss over the sampling distribution, R(θ, δ) = E_θ[L(θ, δ(X))] — a function of θ, not a number.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Keep the three apart. The loss is a penalty for one θ and one action; it involves no randomness. The rule is what you will do for each possible dataset; it involves no θ. The risk averages the loss over the data for a FIXED θ, which is why it is a function of θ and why two rules can be compared only by comparing two curves.

> That last point is the whole difficulty of the topic. If risk were a single number, the best rule would be the one with the smallest number. Because it is a curve, two rules can cross, and then neither is better — which is what admissibility is about.

> Note what is averaged over. Risk averages over the SAMPLE with θ held fixed; Bayes risk goes one step further and averages over θ as well, using a prior. Those are two different operations and the exam separates them.

**Check 2** `scenes[0].items[1]`

- *asks:* Under squared-error loss, what does the risk of an estimator equal?
- *expected answer* `.recall`: The mean squared error, which decomposes as R(θ, θ̂) = Var_θ(θ̂) + [bias_θ(θ̂)]². With L(θ, a) = (θ − a)², risk and MSE are the same object.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Write it out: E[(θ̂ − θ)²] = E[(θ̂ − E θ̂ + E θ̂ − θ)²]. The cross term vanishes because E[θ̂ − Eθ̂] = 0, leaving the variance plus the squared bias.

> This is the identity that makes the whole topic computable. Every risk in this lesson is obtained by writing down a variance and a bias and adding the square of the second to the first — no integration required.

> It also explains why biased estimators are not automatically worse. A rule that accepts some bias to buy a large variance reduction can have lower risk, and the shrinkage estimators in this lesson are exactly that trade made deliberately.

**Check 3** `scenes[0].items[2]`

- *asks:* What are the mean and variance of a binomial count, and of the sample proportion?
- *expected answer* `.recall`: For X ~ Bin(n, p): E[X] = np and Var(X) = np(1 − p). For the proportion p̂ = X/n: E[p̂] = p, so it is unbiased, and Var(p̂) = p(1 − p)/n.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Because p̂ is unbiased, its squared-error risk is just its variance, p(1 − p)/n. That is a curve in p: zero at the two ends and largest at p = 0.5, where it equals 1/(4n).

> That shape is the key to the main example in this lesson. The MLE's risk is excellent when p is near 0 or 1 and at its worst in the middle, so a rule with a flat risk curve can beat it in the middle while losing at the ends.

> Keep 1/(4n) in mind as a number. For n = 9 the MLE's worst-case risk is 1/36 = 0.0278, and the lesson will produce a rule whose risk is 1/64 = 0.0156 everywhere.

**Check 4** `scenes[0].items[3]`

- *asks:* What is the Bayes estimator under squared-error loss, from the previous topic?
- *expected answer* `.recall`: The posterior mean. With a Beta(α, β) prior and x successes in n trials, that is (α + x)/(α + β + n); with the symmetric prior Beta(a, a) it is (x + a)/(n + 2a).

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> This topic and the last are two views of the same machinery. In 4.7 the prior was the point and the loss was the afterthought; here the loss is the point and the prior becomes a device.

> The connection worth carrying in advance: a Bayes rule is one that minimises Bayes risk for a stated prior. It turns out that a Bayes rule whose ordinary risk happens to be CONSTANT in θ is minimax, and that is how minimax rules are actually found.

> So the formula (x + a)/(n + 2a) is about to be used not as a Bayesian answer but as a family of candidate rules, with a chosen to flatten the risk curve.

---

### Scene 2 of 14 — Two curves that cross

`scenes[1]` · id `s1` · type `intuition` (intuition) · 5 minutes

**Purpose** `scenes[1].objective`

See why 'which estimator is better' is usually the wrong question, and what the two standard repairs are.

**Body** `scenes[1].body[]`

Everything awkward about this topic comes from one fact: risk is a function of the unknown parameter, and two rules' risk curves generally cross.

Suppose one rule has risk 0.02 everywhere and another has risk that is 0.01 near the ends of the parameter range and 0.03 in the middle. Which is better? The honest answer is that the question is malformed. The second is better if θ is near an end and worse if it is in the middle, and you do not know which it is — that is the whole point of having to estimate it.

There are only two serious ways out, and the syllabus names both. The first is to give up on a total ordering and ask only the weaker question: is there a rule that is at least as good as this one everywhere, and strictly better somewhere? If so, this rule is INADMISSIBLE and should be discarded; nothing is lost by dropping it. If not, it is ADMISSIBLE, and admissibility is a very low bar — it certifies only that the rule is not uniformly beatable, not that it is good. The constant rule 'always answer 7' is admissible, because nothing beats it when θ happens to be 7.

The second way out is to impose an ordering by force, by judging each rule on its worst case. The MINIMAX rule is the one whose highest risk over all θ is lowest. That turns curves into numbers and always produces an answer, at the cost of being governed entirely by the least favourable parameter value — a pessimist's criterion.

The third option, which is what Bayesians do, is to average the risk over a prior instead of taking its maximum. That also turns a curve into a number, and the number depends on the prior. The striking fact, and the one this lesson builds to, is that these two repairs meet: the minimax rule is usually a Bayes rule for a particular prior, the one that makes the problem hardest.

**Aside — The sentence to carry into the exam** `scenes[1].aside.body`

Admissible means not uniformly beatable — a weak certificate. Minimax means the best worst case. Bayes means the best average against a prior. The three are different questions, and a rule can satisfy one and not another.

**Quick check before moving on** `scenes[1].ask`

- *question:* The rule 'ignore the data and always answer 0.5' is admissible under squared-error loss. Does that tell you anything good about it?
- *hint on request:* Ask what would have to be true of a competing rule for it to beat this one everywhere, including at θ = 0.5.

---

### Scene 3 of 14 — Watch two risk curves cross

`scenes[2]` · id `s2` · type `explore` (interactive visualisation) · 6 minutes

**Purpose** `scenes[2].objective`

Read admissibility and the minimax value straight off the picture.

**Body** `scenes[2].body[]`

Three risk curves for estimating a normal mean: the sample mean in pink, a constant guess in teal, and a shrinkage rule between them in ochre. The horizontal axis is θ, the vertical axis is squared-error risk.

Start with the sample mean alone by setting the shrinkage weight to 1. Its risk is a flat line at σ²/n = 1.0 — flat because x̄ is unbiased, so its risk is a variance that does not depend on θ. That flatness is what makes it minimax: its worst case equals its everywhere-case, and no rule can do better in the worst case.

Now drag the weight to 0. The rule ignores the data and always answers m. Its risk is the parabola (θ − m)²: exactly zero when θ happens to equal m, and growing without limit as θ moves away. This is the cleanest possible demonstration that no rule dominates another everywhere — at θ = m this absurd rule beats every estimator ever devised, which is precisely why admissibility is a weak criterion.

Set the weight to 0.5 and look at where the ochre curve crosses the pink line. To the left and right of the crossings the sample mean is better; between them the shrinkage rule is. Neither dominates, so BOTH are admissible. But read the two worst cases off the readout: the sample mean's is 1.0, the shrinkage rule's is larger. So the sample mean is minimax and the shrinkage rule is not — admissible and minimax are different questions, and this frame is the difference.

Finally move the target m away from zero and watch the whole ochre curve slide with it. The shrinkage rule's advantage is purchased near wherever you aim it, and paid for everywhere else.

**Interactive element** `scenes[2].viz` — live plot of type `risk-curves`, initial state n=9, sd=3, m=0, w=0.5. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[2].ask`

- *question:* At weight 0.5 the shrinkage rule's risk at θ = m is 0.25, a quarter of the sample mean's. Why is that not an argument for using it?
- *hint on request:* Ask what you would need to know in order to collect that advantage, and whether you know it.

---

### Scene 4 of 14 — The four definitions and the three relations

`scenes[3]` · id `s3` · type `theory` (theory) · 9 minutes

**Purpose** `scenes[3].objective`

State every definition in the topic precisely, and the relations the exam asks you to apply.

**Block 1 — The decision problem** `scenes[3].blocks[0]` *(type `def`)*

A parameter space Θ, an action space A, a loss function L : Θ × A → [0, ∞), and a family of distributions {f(x | θ)}. A decision rule δ maps each sample x to an action δ(x) ∈ A. For estimation A = Θ and δ is an estimator; for testing A = {accept, reject} and δ is a test. A randomised rule chooses among actions by a probability distribution, which matters because randomised rules are sometimes needed to attain a stated size and sometimes needed for a minimax solution to exist.

**Block 2 — Risk, and Bayes risk** `scenes[3].blocks[1]` *(type `formula`)*

Risk: R(θ, δ) = E_θ[L(θ, δ(X))] = ∫ L(θ, δ(x)) f(x | θ) dx. A function of θ. Bayes risk, against a prior π: r(π, δ) = ∫ R(θ, δ) π(θ) dθ = E_π[R(θ, δ)]. A single number. The distinction is the one most worth getting right: risk integrates over the DATA, Bayes risk integrates over the data and then over the PARAMETER.

**Block 3 — Domination and admissibility** `scenes[3].blocks[2]` *(type `def`)*

δ₁ dominates δ₂ if R(θ, δ₁) ≤ R(θ, δ₂) for every θ, with strict inequality for at least one θ. δ₂ is then inadmissible. A rule is admissible if no rule dominates it. Admissibility is a NEGATIVE property — it says nothing beats you everywhere — and it is weak: a constant rule is admissible, and inadmissible rules can still be perfectly reasonable in practice.

**Block 4 — Minimax** `scenes[3].blocks[3]` *(type `formula`)*

δ* is minimax if sup_θ R(θ, δ*) = inf_δ sup_θ R(θ, δ). The minimax value is that common quantity. The criterion is complete — it always ranks two rules — and it is pessimistic, because the ranking is decided entirely by each rule's worst parameter value.

**Block 5 — Bayes rules** `scenes[3].blocks[4]` *(type `def`)*

δ_π is a Bayes rule with respect to π if it minimises r(π, δ). Under squared-error loss it is the posterior mean; under absolute-error loss the posterior median; under 0–1 loss the posterior mode. The practical route to a Bayes rule is therefore always the same: find the posterior, then take the summary the loss names.

**Block 6 — The three relations the exam asks for** `scenes[3].blocks[5]` *(type `formula`)*

(1) A Bayes rule with CONSTANT risk is minimax. (2) A unique Bayes rule is admissible. (3) If a minimax rule is unique, it is admissible. The first is the one that does work: it converts the hard problem of minimising a supremum into the easy problem of choosing a prior that flattens the risk curve. The prior that does so is called the LEAST FAVOURABLE prior, because it makes the problem as hard as possible.

**Block 7 — Why relation (1) is true, in one paragraph** `scenes[3].blocks[6]` *(type `step`)*

Let δ_π be Bayes for π with risk constant at c. For any rule δ, its worst-case risk is at least its average risk against π, which is at least the Bayes risk of δ_π, which equals c because the risk is constant. So sup_θ R(θ, δ) ≥ c = sup_θ R(θ, δ_π) for every δ, which is the definition of δ_π being minimax. The whole argument is 'a maximum is at least an average', used once.

**Block 8 — What is NOT true** `scenes[3].blocks[7]` *(type `trap`)*

Minimax does not imply admissible, and admissible does not imply minimax — the explore scene showed both failures in one picture. An unbiased estimator need not be admissible; the sample variance with divisor n − 1 is the standard counterexample under squared-error loss. And the MLE is not generally admissible: in estimating a normal mean vector in three or more dimensions, the James–Stein shrinkage estimator dominates it everywhere, which is the most famous inadmissibility result in statistics.

**Quick check before moving on** `scenes[3].ask`

- *question:* How do loss, risk, admissibility and minimaxity differ?
- *hint on request:* Loss is for a realised action and parameter; risk averages loss under sampling; admissibility rules out uniformly better procedures; minimaxity minimises worst-case risk.

---

### Scene 5 of 14 — Worked in full — the minimax estimator of a binomial p

`scenes[4]` · id `s4` · type `worked` (worked example) · 8 minutes

**Purpose** `scenes[4].objective`

Build a minimax rule from scratch by flattening a risk curve, and verify it.

**Problem put to the learner** `scenes[4].problem`

X ~ Bin(9, p) and the loss is squared error. (a) Find the risk of the MLE p̂ = X/9 and its worst case. (b) Within the family δ_a(x) = (x + a)/(9 + 2a), find the value of a making the risk constant in p. (c) State the minimax value, and (d) decide whether either rule dominates the other.

**Worked steps** `scenes[4].steps[]`

1. `scenes[4].steps[0]` (a) The MLE is unbiased, so its risk is its variance.

   ```
   R(p, p̂) = Var(X/9) = 9p(1−p)/81 = p(1−p)/9
   ```

   Laid out:

   $$R(p, p̂) = Var\frac{X}{9} = \frac{9p(1−p)}{81} = \frac{p(1−p)}{9}$$

   *why* `.why`: A curve, not a number: zero at p = 0 and p = 1, maximal at p = 0.5. Unbiasedness is what removes the bias term and leaves a pure variance.

2. `scenes[4].steps[1]` Its worst case is at the middle.

   ```
   sup_p p(1−p)/9 = (1/4)/9 = 1/36 = 0.027778  at p = 0.5
   ```

   Laid out:

   $$sup_p \frac{p(1−p)}{9} = \frac{\frac{1}{4}}{9} = \frac{1}{36} = 0.027778  at p = 0.5$$

   *why* `.why`: This is the number any competitor has to beat in the worst case. Note 1/(4n) is the general form.

3. `scenes[4].steps[2]` (b) Write the bias and variance of δ_a, with N = 9 + 2a.

   ```
   E[δ_a] = (9p + a)/N,  bias = (9p + a)/N − p = (a − 2ap)/N;   Var(δ_a) = 9p(1−p)/N²
   ```

   Laid out:

   $$E[δ_a] = \frac{(9p + a)}{N},  bias = \frac{(9p + a)}{N} − p = \frac{(a − 2ap)}{N};   Var(δ_a) = \frac{9p(1−p)}{N²}$$

   *why* `.why`: The bias is linear in p and the variance quadratic, so the risk is a quadratic in p. Making it constant means killing the coefficients of p and p².

4. `scenes[4].steps[3]` Add variance and squared bias, and collect in p.

   ```
   R = [9p − 9p² + a² − 4a²p + 4a²p²]/N² = [a² + (9 − 4a²)p + (4a² − 9)p²]/N²
   ```

   Laid out:

   $$R = \frac{[9p − 9p² + a² − 4a²p + 4a²p²]}{N²} = \frac{[a² + (9 − 4a²)p + (4a² − 9)p²]}{N²}$$

   *why* `.why`: The p and p² coefficients are 9 − 4a² and −(9 − 4a²): negatives of each other. So a single condition kills both at once, which is why this family works.

5. `scenes[4].steps[4]` Set the coefficient to zero and solve for a.

   ```
   9 − 4a² = 0  ⟹  a = 3/2 = √9/2,  i.e.  a = √n/2
   ```

   Laid out:

   $$9 − 4a² = 0  ⟹  a = \frac{3}{2} = \frac{√9}{2},  i.e.  a = \frac{√n}{2}$$

   *why* `.why`: The general answer is a = √n/2, so the minimax estimator of a binomial proportion is (x + √n/2)/(n + √n). For n = 9 that is (x + 1.5)/12.

6. `scenes[4].steps[5]` (c) Evaluate the constant.

   ```
   R = a²/N² = (1.5)²/12² = 2.25/144 = 0.015625 = 1/64;   general form 1/(4(1 + √n)²)
   ```

   Laid out:

   $$R = \frac{a²}{N²} = \frac{(1.5)²}{12²} = 2.\frac{25}{144} = 0.015625 = \frac{1}{64};   general form \frac{1}{(4(1 + √n)²)}$$

   *why* `.why`: Check the general form: 1/(4(1+3)²) = 1/64 ✓. And 0.015625 < 0.027778, so this rule's worst case beats the MLE's by a wide margin. Because the risk is constant AND the rule is Bayes for Beta(1.5, 1.5) — the posterior mean (x + a)/(n + 2a) — relation (1) applies and the rule is minimax.

7. `scenes[4].steps[6]` (d) Compare the two curves to settle domination.

   ```
   p(1−p)/9 = 1/64  ⟹  p² − p + 9/64 = 0  ⟹  p = (1 ± √0.4375)/2 = 0.1693, 0.8307
   ```

   Laid out:

   $$\frac{p(1−p)}{9} = \frac{1}{64}  ⟹  p² − p + \frac{9}{64} = 0  ⟹  p = \frac{(1 ± √0.4375)}{2} = 0.1693, 0.8307$$

   *why* `.why`: Below 0.1693 and above 0.8307 the MLE has the smaller risk; between them the minimax rule does. The curves cross, so neither dominates and both are admissible. At p = 0.1 the MLE's risk is 0.0100 against 0.0156 — the minimax rule is genuinely worse there, and that is the price of insuring against the worst case.

8. `scenes[4].steps[7]` State the least favourable prior, which is the by-product.

   ```
   Beta(√n/2, √n/2) = Beta(1.5, 1.5)
   ```

   Laid out:

   $$Beta(\frac{√n}{2}, \frac{√n}{2}) = Beta(1.5, 1.5)$$

   *why* `.why`: This prior makes the problem hardest, in the sense that the best achievable Bayes risk against it equals the minimax value. It is also the bridge back to 4.7: the minimax rule here IS a posterior mean, with the prior chosen by a flatness condition rather than by belief.

**What to take from it** `scenes[4].after`

Four numbers to carry: MLE worst case 1/36 = 0.0278, minimax value 1/64 = 0.0156, the estimator (x + √n/2)/(n + √n), and the least favourable prior Beta(√n/2, √n/2). And one method: to find a minimax rule, take a conjugate family of Bayes rules and choose the prior parameter that flattens the risk.

**Quick check before moving on** `scenes[4].ask`

- *question:* To establish that an estimator is minimax in a finite decision problem, what risks must you compare?
- *hint on request:* Find its maximum risk over the parameter space and show no competing estimator can achieve a smaller maximum risk.

---

### Scene 6 of 14 — Pause and recall

`scenes[5]` · id `s5` · type `recall` (retrieval practice) · 3 minutes

**Purpose** `scenes[5].objective`

Retrieve the definitions and relations before the harder material.

**Intro** `scenes[5].intro`

Answer aloud, then look. Everything here was in the last two scenes.

- `scenes[5].items[0]` **Q:** Define the risk of a decision rule, and say what it is a function of.  
  **A:** R(θ, δ) = E_θ[L(θ, δ(X))] — the expected loss over the sampling distribution, for a fixed θ. It is a function of θ, which is why two rules can cross.
- `scenes[5].items[1]` **Q:** Define Bayes risk, and say how it differs from risk.  
  **A:** r(π, δ) = ∫ R(θ, δ) π(θ) dθ. Risk averages over the data with θ fixed; Bayes risk averages that over θ too, using a prior, so it is a single number.
- `scenes[5].items[2]` **Q:** What does it mean for a rule to be inadmissible?  
  **A:** Some other rule has risk no larger at every θ and strictly smaller at some θ. A rule is admissible if no such rule exists.
- `scenes[5].items[3]` **Q:** Define the minimax rule.  
  **A:** The rule minimising sup_θ R(θ, δ) — the best worst case. The common value of inf_δ sup_θ R is the minimax value.
- `scenes[5].items[4]` **Q:** State the relation that is actually used to find minimax rules.  
  **A:** A Bayes rule with constant risk is minimax, and the prior that achieves it is the least favourable prior.
- `scenes[5].items[5]` **Q:** Give the minimax estimator of a binomial p under squared-error loss, and its risk.  
  **A:** (x + √n/2)/(n + √n), with constant risk 1/(4(1 + √n)²). For n = 9 that is (x + 1.5)/12 and 1/64.

---

### Scene 7 of 14 — Your turn, with the scaffolding removed — five judgements

`scenes[6]` · id `s6` · type `completion` (fill in the blanks) · 7 minutes

**Purpose** `scenes[6].objective`

Apply each definition to a case you have not been shown.

**Problem put to the learner** `scenes[6].problem`

Fill in each blank. The arithmetic is small; what is tested is which definition applies.

**Worked steps** `scenes[6].steps[]`

1. `scenes[6].steps[0]` Estimating a normal mean with known σ², the rule δ(x) = x̄ has risk σ²/n at every θ.

   - *learner is asked:* Is it minimax, and why in one clause?
   - *accepted answer* `.blank.answer`: yes, because its risk is constant
   - *also accepted:* yes - constant risk; minimax, constant risk; yes, constant risk so worst case = risk everywhere; yes because the risk does not depend on theta
   - *hint:* Its worst case equals its everywhere-case, and no rule can do better in the worst case.

   *why* `.why`: The flat-risk argument is the one relation in this topic that does real work.

2. `scenes[6].steps[1]` The rule 'ignore the data and always answer 3' has risk (θ − 3)², which is 0 at θ = 3.

   - *learner is asked:* Is it admissible, and is it minimax?
   - *accepted answer* `.blank.answer`: admissible but not minimax
   - *also accepted:* admissible, not minimax; yes admissible; no not minimax; it is admissible but its worst case is unbounded so not minimax; admissible but not minimax (unbounded worst case)
   - *hint:* Nothing can beat it at θ = 3, but its supremum of risk is infinite.

   *why* `.why`: This single example shows admissibility is weak and that admissible does not imply minimax.

3. `scenes[6].steps[2]` For a Bin(16, p) problem under squared-error loss.

   - *learner is asked:* The minimax estimator and its risk?
   - *accepted answer* `.blank.answer`: (x + 2)/20, risk 1/100 = 0.01
   - *also accepted:* (x+2)/20 and 0.01; (x + 2)/20, 1/100; (x+2)/20, risk 0.01; estimator (x+2)/20 risk 1/(4(1+4)^2)=0.01
   - *hint:* a = √n/2 and the risk is 1/(4(1 + √n)²), with √16 = 4.

   *why* `.why`: Substituting into the general form is the fastest marks in the topic; n = 16 is chosen to make √n an integer.

4. `scenes[6].steps[3]` A rule is the unique Bayes rule for some proper prior.

   - *learner is asked:* What does that establish about it?
   - *accepted answer* `.blank.answer`: it is admissible
   - *also accepted:* admissible; that it is admissible; it must be admissible; admissibility (a unique Bayes rule is admissible)
   - *hint:* One of the three relations in scene 4, and it needs the uniqueness.

   *why* `.why`: The relation runs this way only: a unique Bayes rule is admissible, not the converse.

5. `scenes[6].steps[4]` Estimating a normal mean VECTOR in three or more dimensions, the MLE is the vector of sample means.

   - *learner is asked:* What is known about its admissibility, and by which result?
   - *accepted answer* `.blank.answer`: it is inadmissible, by the James-Stein estimator
   - *also accepted:* inadmissible - James-Stein; inadmissible, James-Stein shrinkage dominates it; not admissible (James-Stein); inadmissible by James Stein
   - *hint:* A shrinkage estimator dominates it everywhere once the dimension is at least 3.

   *why* `.why`: The most famous inadmissibility result in statistics, and the standard counterexample to 'the MLE is always sensible'.

**What to take from it** `scenes[6].after`

Note what the second blank does to intuition: a rule that ignores the data entirely is admissible. Admissibility certifies only that a rule is not uniformly beatable, and that is a very low bar.

---

### Scene 8 of 14 — Testing as a decision problem, and the loose ends

`scenes[7]` · id `s7` · type `theory` (theory) · 7 minutes

**Purpose** `scenes[7].objective`

Carry the testing translation and the remaining vocabulary the syllabus names.

**Block 1 — Testing in decision language** `scenes[7].blocks[0]` *(type `def`)*

Take A = {0, 1}, with 1 meaning reject H₀, and the 0–1 loss L(θ, a) = 0 for a correct decision and 1 for an error. Then the risk is the probability of error: R(θ, δ) = P_θ(type I error) for θ ∈ H₀ and P_θ(type II error) for θ ∈ H₁. The whole Neyman–Pearson apparatus is one risk function, cut in two by which hypothesis θ belongs to.

**Block 2 — Why Neyman–Pearson is not a minimax criterion** `scenes[7].blocks[1]` *(type `formula`)*

Neyman–Pearson does not minimise the maximum of the two error probabilities. It CONSTRAINS one — size at most α — and minimises the other. That asymmetric treatment is a choice, justified by the two errors having different consequences, and it is why the framework needs a null hypothesis at all. A minimax test would instead equalise the two errors, which it does by choosing α to make them equal.

**Block 3 — Unbiasedness and invariance as restrictions** `scenes[7].blocks[2]` *(type `def`)*

Both are ways of shrinking the class of rules until a best one exists. Restrict to unbiased tests and a uniformly most powerful unbiased, or UMPU, test can exist where no UMP test does; restrict to invariant rules and a UMP invariant test can exist. The logic is the same as restricting to unbiased estimators before looking for a minimum-variance one: you cannot optimise over everything, so you optimise over a class and then defend the class.

**Block 4 — Complete class, and essentially complete class** `scenes[7].blocks[3]` *(type `def`)*

A class C of rules is complete if every rule outside it is dominated by some rule in C — so nothing is lost by restricting attention to C. The central result of the subject is that, under mild conditions, the Bayes rules form a complete class: every admissible rule is a Bayes rule or a limit of Bayes rules. That is why Bayesian machinery turns up in the search for minimax and admissible rules even when nobody involved holds a prior belief.

**Block 5 — Randomised rules, and why they are needed** `scenes[7].blocks[4]` *(type `step`)*

A randomised rule picks an action by a coin toss whose bias may depend on the data. Two places they are unavoidable: attaining an exact size α with a discrete test statistic, where no non-randomised critical region has the right probability; and guaranteeing that a minimax rule exists, since the set of risk points need not be closed without them. Under a convex loss such as squared error, randomisation never helps for estimation — a result that follows from Jensen's inequality.

**Block 6 — Five statements that look right and are not** `scenes[7].blocks[5]` *(type `trap`)*

Admissible does not imply minimax; minimax does not imply admissible. A Bayes rule need not be minimax unless its risk is constant. The MLE is not generally admissible. An unbiased estimator need not be admissible. And the minimax value is not the smallest risk achievable at any θ — it is the smallest achievable WORST CASE, which is a different and much larger number.

**Flow diagram** `scenes[7].flow` — One risk curve, two ways of collapsing it, three relations between the answers

- row 1: Θ, actions A, loss L(θ,a), rule δ(x)
- row 2: Risk R(θ,δ) = E_θ[L(θ,δ(X))] — a function of θ
- row 3: Take the supremum over θ  |  Average over a prior π
- row 4: Minimax rule  |  Bayes rule
- row 5: Constant risk + Bayes ⟹ minimax · unique Bayes ⟹ admissible
- arrows: Θ, actions A, loss L(θ,a), rule δ(x) → Risk R(θ,δ) = E_θ[L(θ,δ(X))] — a function of θ; Risk R(θ,δ) = E_θ[L(θ,δ(X))] — a function of θ → Take the supremum over θ; Risk R(θ,δ) = E_θ[L(θ,δ(X))] — a function of θ → Average over a prior π; Take the supremum over θ → Minimax rule; Average over a prior π → Bayes rule; Bayes rule → Constant risk + Bayes ⟹ minimax · unique Bayes ⟹ admissible; Minimax rule → Constant risk + Bayes ⟹ minimax · unique Bayes ⟹ admissible

**Quick check before moving on** `scenes[7].ask`

- *question:* How does a hypothesis test fit into decision theory?
- *hint on request:* The action is reject or do not reject; the loss assigns costs to Type I and Type II errors, and risk is the resulting error probability weighted by loss.

**Optional deep-dive, opened on demand — What insuring against the worst case actually costs** `scenes[7].scenario`

*teaser on the closed card:* The minimax rule's worst case is 44% better. At p = 0.1 it is 56% worse. Both figures are the same rule.

> Minimax is usually presented as the cautious choice, and caution sounds free. It is not, and the binomial example prices it exactly. Take n = 9 and compare the MLE's risk p(1−p)/9 against the minimax rule's constant 1/64 = 0.015625.

> At p = 0.5, where the MLE is at its worst, the MLE's risk is 1/36 = 0.027778 and the minimax rule's is 0.015625 — the minimax rule is 43.8% better. That is the advantage it was built for. Now move to p = 0.1: the MLE's risk is 0.010000 and the minimax rule's is still 0.015625, so the minimax rule is 56.2% WORSE. At p = 0.05 it is worse by a factor of nearly three — 0.015625 against 0.005278.

> The two curves cross at p = 0.1693 and p = 0.8307, which are the exact roots of p(1−p)/9 = 1/64. So the minimax rule wins on roughly the middle two-thirds of the parameter range and loses on the outer third, sometimes heavily. Whether that is a good trade depends entirely on where p actually is, which is the one thing you do not know.

> This is why minimax is a criterion and not a conclusion. It answers a specific question — what should I do if I must guard against the least favourable parameter value — and it answers it optimally. It does not answer 'what is the best estimator', because that question has no answer once the risk curves cross. An exam question asking you to 'compare' two estimators is asking for this structure: where each wins, where the curves cross, which has the better worst case, and whether either dominates.

> The practical reading, worth a sentence in any answer: if you have genuine reason to think p is extreme, the MLE is better and you should say so. Minimax is insurance, and insurance is worth buying only when the risk you are insuring against is real.

*closing line:* Minimax buys a better worst case and pays for it everywhere else; the price here is exact and computable.

---

### Scene 9 of 14 — The least favourable prior, seen as a flatness condition

`scenes[8]` · id `s8` · type `explore` (interactive visualisation) · 6 minutes

**Purpose** `scenes[8].objective`

Watch a risk curve flatten as a prior parameter is tuned, which is how minimax rules are found.

**Body** `scenes[8].body[]`

This frame opens with the shrinkage weight at 1, so the only curve that matters is the flat pink line at σ²/n = 1.0 — the sample mean. Hold that picture: FLAT IS THE GOAL. A rule with flat risk has nothing to fear from an adversary choosing θ, because every θ costs the same.

Now drop the weight slightly, to 0.95. The curve tilts: slightly better near the target, slightly worse away from it, and its supremum over the frame rises above 1.0. Every departure from flatness hands the adversary a parameter value to exploit, and the readout's worst-case line records the damage.

That is the whole logic of the worked example, in a different problem. There, the family of candidate rules was δ_a(x) = (x + a)/(n + 2a) — the posterior means of the Beta(a, a) priors — and the risk was a quadratic in p with the p and p² coefficients equal to 9 − 4a² and its negative. One value of a, namely √n/2, killed both and left a constant. The prior that did it, Beta(√n/2, √n/2), is the least favourable prior.

So 'least favourable' is not a statement about belief. It names the prior against which the best achievable Bayes risk is largest — the hardest problem in the family — and the striking fact is that solving that one hardest problem solves the minimax problem too. Note the direction of the argument: you do not verify minimaxity by checking every rule. You produce one rule, show its risk is constant, show it is Bayes for some prior, and the relation does the rest.

One caution the picture makes obvious. Flat risk is sufficient for minimaxity only alongside being a Bayes rule. A rule can have constant risk and be poor — 'always answer the first observation' has constant risk σ², flat as anything, and is dominated by x̄ for every n > 1.

**Interactive element** `scenes[8].viz` — live plot of type `risk-curves`, initial state n=9, sd=3, m=0, w=1. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[8].ask`

- *question:* 'Always report x₁' has constant risk σ², which is flat. Why does that not make it minimax?
- *hint on request:* The relation has two conditions, and this rule satisfies only one of them. Which?

---

### Scene 10 of 14 — Now without the steps — settle admissibility and minimaxity

`scenes[9]` · id `s9` · type `guided` (guided problem) · 8 minutes

**Purpose** `scenes[9].objective`

Compare two rules completely: domination, admissibility, and which is minimax.

**Problem put to the learner** `scenes[9].problem`

X ~ Bin(16, p), squared-error loss. Consider δ₁(x) = x/16 and δ₂(x) = (x + 2)/20. (a) Write both risk functions. (b) Does either dominate the other? (c) Which is minimax, and what is the minimax value? (d) Are both admissible?

**Hint ladder, revealed one at a time** `scenes[9].hints[]`

1. δ₁ is unbiased, so its risk is a variance. For δ₂, note that 2 = √16/2, so it is the minimax rule and its risk should come out constant.
2. Set the two risks equal and solve the resulting quadratic in p to find where the curves cross.
3. Domination requires one curve to be below the other at EVERY p. A single crossing settles the question.

**Model solution, hidden until requested** `scenes[9].solution[]`

1. `scenes[9].solution[0]` (a) δ₁ is unbiased, so its risk is Var(X/16).

   ```
   R(p, δ₁) = 16p(1−p)/256 = p(1−p)/16
   ```

   Laid out:

   $$R(p, δ₁) = \frac{16p(1−p)}{256} = \frac{p(1−p)}{16}$$

2. `scenes[9].solution[1]` δ₂ is δ_a with a = 2 = √16/2, so it is the minimax rule and its risk is the constant from the general form.

   ```
   R(p, δ₂) = 1/(4(1 + √16)²) = 1/(4 × 25) = 1/100 = 0.01
   ```

   Laid out:

   $$R(p, δ₂) = \frac{1}{(4(1 + √16)²)} = \frac{1}{(4 × 25)} = \frac{1}{100} = 0.01$$

3. `scenes[9].solution[2]` (b) Set them equal to locate the crossings.

   ```
   p(1−p)/16 = 1/100  ⟹  p² − p + 0.16 = 0  ⟹  p = (1 ± √0.36)/2 = (1 ± 0.6)/2 = 0.2, 0.8
   ```

   Laid out:

   $$\frac{p(1−p)}{16} = \frac{1}{100}  ⟹  p² − p + 0.16 = 0  ⟹  p = \frac{(1 ± √0.36)}{2} = \frac{(1 ± 0.6)}{2} = 0.2, 0.8$$

4. `scenes[9].solution[3]` Read off which is lower where.

   ```
   p < 0.2 or p > 0.8 → δ₁ lower;   0.2 < p < 0.8 → δ₂ lower
   ```

   *why* `.why`: For instance at p = 0.1, R(δ₁) = 0.09/16 = 0.005625 against 0.01; at p = 0.5, R(δ₁) = 0.25/16 = 0.015625 against 0.01.

5. `scenes[9].solution[4]` So neither dominates.

   ```
   the curves cross at p = 0.2 and p = 0.8 ⟹ no domination either way
   ```

6. `scenes[9].solution[5]` (c) Compare the worst cases.

   ```
   sup R(δ₁) = 1/64 = 0.015625 at p = 0.5;   sup R(δ₂) = 0.01  ⟹  δ₂ is minimax, value 0.01
   ```

   Laid out:

   $$sup R(δ₁) = \frac{1}{64} = 0.015625 at p = 0.5;   sup R(δ₂) = 0.01  ⟹  δ₂ is minimax, value 0.01$$

7. `scenes[9].solution[6]` (d) Admissibility follows from (b).

   ```
   neither is dominated ⟹ both admissible
   ```

**Final answer given to the learner** `scenes[9].answer`

R(p, δ₁) = p(1−p)/16 and R(p, δ₂) = 0.01. The curves cross at p = 0.2 and 0.8, so neither dominates and both are admissible. δ₂ is minimax with minimax value 0.01, against δ₁'s worst case of 1/64 = 0.015625.

**Self-check offered** `scenes[9].check`

Three checks. The crossing points must be symmetric about 0.5, because R(δ₁) is, and 0.2 and 0.8 are. The minimax value must be below the other rule's worst case — 0.01 < 0.015625 ✓. And δ₂'s risk must be genuinely constant; if yours depends on p, the coefficient-killing condition a = √n/2 was not used.

**Optional deep-dive, opened on demand — Minimax as a game against nature** `scenes[9].scenario`

*teaser on the closed card:* Why a prior nobody believes in is the key to a criterion that mentions no prior at all.

> The minimax criterion makes no reference to a prior, and yet the only practical way to find a minimax rule runs through one. That looks like a trick. It is not; it is the structure of a two-person game, and seeing it that way makes the relation in scene 4 obvious rather than magical.

> Set the problem up as a game. You choose a decision rule δ. An adversary — call it nature — chooses the parameter θ. The payoff nature collects from you is the risk R(θ, δ). You want to minimise it; nature wants to maximise it. You move first, in the sense that nature may choose θ knowing your rule, which is exactly what 'worst case' means: your loss is sup_θ R(θ, δ), and you pick δ to make that as small as possible.

> Now allow nature a mixed strategy — a probability distribution over θ rather than a single value. A distribution over the parameter is a prior, and nature's expected payoff against it is the Bayes risk r(π, δ). Nature's best mixed strategy is the one that maximises the best Bayes risk you can achieve against it, and that distribution is precisely what the LEAST FAVOURABLE prior is: nature's optimal play.

> At the equilibrium of such a game, the two orders of play agree — the minimum of the maxima equals the maximum of the minima. Your equilibrium strategy is the Bayes rule against nature's optimal prior, and nature is indifferent between every θ it has put mass on, which is to say your risk is CONSTANT across them. That indifference is the flat risk curve. It is not a lucky coincidence that flat risk certifies minimaxity; it is what equilibrium looks like from your side of the board.

> Two things follow that are worth carrying. First, the least favourable prior is a device, not a belief — in the binomial problem it came out as Beta(√n/2, √n/2), which nobody would assert as a description of the world. Second, this is why Bayes rules form a complete class: the equilibrium strategies of the game are Bayes rules, so anything that is not one (or a limit of them) is beatable, which is what inadmissible means.

*closing line:* Minimax is the equilibrium of a game against nature; the least favourable prior is nature's optimal play, and flat risk is the indifference that marks the equilibrium.

---

### Scene 11 of 14 — Six statements — verdict on each before you look

`scenes[10]` · id `s10` · type `trapcheck` (true/false check) · 6 minutes

**Purpose** `scenes[10].objective`

Meet the exact implications this topic invites you to assert and that do not hold.

**Intro** `scenes[10].intro`

Each is either a standard result or an implication running the wrong way.

- `scenes[10].items[0]` **Claim:** A Bayes rule whose risk is constant in θ is minimax.  
  **Verdict: TRUE.** The argument is one line: any rule's worst-case risk is at least its average risk against the prior, which is at least the Bayes risk, which equals the constant. This is the relation that makes minimax problems solvable.
- `scenes[10].items[1]` **Claim:** Every minimax rule is admissible.  
  **Verdict: FALSE.** Not in general. Minimaxity is about the worst case only, and a rule can have the best worst case while being dominated elsewhere. A UNIQUE minimax rule is admissible, and that qualifier is the whole content of the statement.
- `scenes[10].items[2]` **Claim:** The risk of a decision rule is a single number summarising its quality.  
  **Verdict: FALSE.** Risk is a FUNCTION of θ. Bayes risk is the single number, obtained by averaging risk over a prior, and the minimax value is another, obtained by taking its supremum. Collapsing risk to a number is what the whole topic is about.
- `scenes[10].items[3]` **Claim:** Under squared-error loss the risk of an estimator equals its variance plus the square of its bias.  
  **Verdict: TRUE.** The MSE decomposition, with the cross term vanishing. It is how every risk in this topic is actually computed, and it is why a biased rule can have lower risk than an unbiased one.
- `scenes[10].items[4]` **Claim:** The maximum likelihood estimator is always admissible.  
  **Verdict: FALSE.** For a normal mean vector in three or more dimensions the James–Stein shrinkage estimator dominates it at every parameter value — the most famous inadmissibility result in statistics. The MLE has many virtues; admissibility is not reliably among them.
- `scenes[10].items[5]` **Claim:** The rule that ignores the data and always reports a fixed constant is inadmissible.  
  **Verdict: FALSE.** It is admissible. At the parameter value equal to that constant its risk is zero, so no rule can have risk no larger everywhere and strictly smaller somewhere. This is the standard demonstration that admissibility is a weak criterion.

---

### Scene 12 of 14 — Transfer — a loss that is not squared error

`scenes[11]` · id `s11` · type `guided` (guided problem) · 7 minutes

**Purpose** `scenes[11].objective`

Build a Bayes rule and judge a rule's admissibility when the loss is asymmetric.

**Problem put to the learner** `scenes[11].problem`

A component's lifetime parameter θ is estimated, and under-estimating is twice as costly as over-estimating: L(θ, a) = 2(θ − a) if a < θ, and (a − θ) if a ≥ θ. The posterior for θ has been computed. (a) What posterior summary is the Bayes rule here? (b) If a competing rule has risk equal to that of the Bayes rule at every θ, what can be said about admissibility? (c) Why does this loss make the squared-error answer wrong?

**Hint ladder, revealed one at a time** `scenes[11].hints[]`

1. This is a weighted absolute-error loss. Recall that plain absolute-error loss gives the median, and ask what weighting the two sides does to that result.
2. For weighted absolute loss with weights k₁ below and k₂ above, the Bayes rule is a QUANTILE of the posterior, not the median.
3. For (b), apply the definition of domination literally — it requires a strict inequality somewhere.

**Model solution, hidden until requested** `scenes[11].solution[]`

1. `scenes[11].solution[0]` (a) Identify the loss. It is absolute error with unequal weights, 2 for under-estimation and 1 for over-estimation.

   ```
   L = k₁(θ − a) for a < θ with k₁ = 2;  k₂(a − θ) for a ≥ θ with k₂ = 1
   ```

2. `scenes[11].solution[1]` The Bayes rule for weighted absolute loss is the k₁/(k₁ + k₂) quantile of the posterior.

   ```
   quantile at 2/(2 + 1) = 2/3  ⟹  the posterior 66.7th percentile
   ```

   Laid out:

   $$quantile at \frac{2}{(2 + 1)} = \frac{2}{3}  ⟹  the posterior 66.7th percentile$$

3. `scenes[11].solution[2]` Sanity-check the direction and the special case.

   ```
   k₁ = k₂ ⟹ quantile 1/2 = the median ✓;  k₁ > k₂ ⟹ quantile above the median
   ```

   Laid out:

   $$k₁ = k₂ ⟹ quantile \frac{1}{2} = the median ✓;  k₁ > k₂ ⟹ quantile above the median$$

   *why* `.why`: Under-estimating costs more, so the rule deliberately aims high. If your answer had moved below the median, the weights were applied the wrong way round.

4. `scenes[11].solution[3]` (b) Apply the definition of domination.

   ```
   equal risk at every θ ⟹ no strict inequality anywhere ⟹ neither dominates the other
   ```

   *why* `.why`: Domination needs risk no larger everywhere AND strictly smaller somewhere. Equal risks fail the second condition, so the two rules are risk-equivalent and the admissibility of one says nothing about the other beyond that neither beats it.

5. `scenes[11].solution[4]` (c) Say why squared error gives the wrong answer here.

   ```
   squared error is symmetric: L(θ, θ+c) = L(θ, θ−c). This loss has L(θ, θ−c) = 2c and L(θ, θ+c) = c
   ```

   *why* `.why`: A symmetric loss cannot express 'under-estimating is worse', so its Bayes rule — the posterior mean — sits in the wrong place. The loss function, not the posterior, is what encodes the asymmetry of consequences.

**Final answer given to the learner** `scenes[11].answer`

(a) The 2/3 quantile of the posterior — weighted absolute loss with weights k₁ below and k₂ above gives the k₁/(k₁+k₂) quantile, which reduces to the median when the weights are equal. (b) Neither dominates: equal risk everywhere fails the strict-inequality requirement. (c) Squared-error loss is symmetric and so cannot represent the asymmetry, and its Bayes rule, the posterior mean, is therefore aimed at the wrong point.

**Self-check offered** `scenes[11].check`

The structural check that catches the commonest error: when under-estimation is the costlier mistake, the estimate must move UP from the median, not down. If your quantile came out at 1/3, the weights were transposed.

---

### Scene 13 of 14 — What you should now be able to do unaided

`scenes[12]` · id `s12` · type `summary` (summary) · 4 minutes

**Purpose** `scenes[12].objective`

Compress the topic to four definitions, three relations and one method.

**Body** `scenes[12].body[]`

The definitions. A decision rule δ maps data to actions. Its risk R(θ, δ) = E_θ[L(θ, δ(X))] is a FUNCTION of θ. Bayes risk r(π, δ) = ∫ R(θ, δ) π(θ) dθ is a NUMBER. δ₁ dominates δ₂ if its risk is no larger everywhere and strictly smaller somewhere; a rule nothing dominates is admissible. A minimax rule minimises sup_θ R(θ, δ).

The relations. A Bayes rule with constant risk is minimax, and the prior achieving it is the least favourable prior. A unique Bayes rule is admissible. A unique minimax rule is admissible. Nothing else holds: admissible does not imply minimax, minimax does not imply admissible, and a Bayes rule is not minimax unless its risk is constant.

The computation. Under squared-error loss, risk = variance + bias². That identity does all the arithmetic in this topic. For an unbiased rule the risk is just the variance, so the MLE of a binomial p has risk p(1−p)/n with worst case 1/(4n).

The method, and the one result to carry. To find a minimax rule, take a conjugate family of Bayes rules and pick the prior parameter that flattens the risk. For Bin(n, p) under squared error this gives the minimax estimator (x + √n/2)/(n + √n), with constant risk 1/(4(1 + √n)²) and least favourable prior Beta(√n/2, √n/2). For n = 9: estimator (x + 1.5)/12, risk 1/64 = 0.0156, against the MLE's worst case of 1/36 = 0.0278 — and the two risk curves cross at p = 0.1693 and 0.8307, so neither dominates and both are admissible.

The losses and their Bayes rules. Squared error → posterior mean. Absolute error → posterior median. 0–1 loss → posterior mode. Weighted absolute error with weights k₁ below and k₂ above → the k₁/(k₁+k₂) posterior quantile.

The translations. Testing is a decision problem with 0–1 loss, where risk is the probability of error — type I on H₀ and type II on H₁. Neyman–Pearson constrains one error and minimises the other rather than minimising the maximum, which is why it is not a minimax criterion. Unbiasedness and invariance are restrictions imposed so that a best rule exists within a class. Bayes rules form a complete class, which is why they appear in every search for admissible and minimax rules.

The counterexamples worth keeping. A constant rule is admissible — so admissibility is weak. The MLE for a normal mean vector in dimension three or more is inadmissible, by James–Stein. And 'always report x₁' has perfectly constant risk and is still dominated by x̄, because constant risk alone is not enough: the rule has to be Bayes as well.

---

### Scene 14 of 14 — Mastery test

`scenes[13]` · id `s13` · type `quiz` (mastery test) · 12 minutes

**Purpose** `scenes[13].objective`

Ten unseen questions, drawn 3 easy / 5 moderate / 2 hard.

Draws from the pool reproduced below. `scenes[13].setId` = `inference_t8_mastery`

---

## Revision material `revision`

**Revision sheet** `revision.sheet[]` (22 lines)

1. `[0]` Risk R(θ,δ) = E_θ[L(θ,δ(X))] — a FUNCTION of θ. Bayes risk r(π,δ) = ∫R(θ,δ)π(θ)dθ — a NUMBER.
2. `[1]` Squared-error loss: risk = MSE = variance + bias². For an unbiased rule, risk = variance.
3. `[2]` δ₁ dominates δ₂: risk no larger at every θ, strictly smaller at some θ. Undominated = admissible.
4. `[3]` Minimax rule: minimises sup_θ R(θ,δ). Minimax value = inf_δ sup_θ R(θ,δ).
5. `[4]` Bayes rule: minimises Bayes risk. Squared error → posterior mean; absolute → median; 0–1 → mode.
6. `[5]` Weighted absolute loss, k₁ below and k₂ above → the k₁/(k₁+k₂) posterior quantile.
7. `[6]` RELATION 1: a Bayes rule with CONSTANT risk is minimax; its prior is the least favourable prior.
8. `[7]` RELATION 2: a UNIQUE Bayes rule is admissible.
9. `[8]` RELATION 3: a UNIQUE minimax rule is admissible.
10. `[9]` NOT true: admissible ⇒ minimax; minimax ⇒ admissible; Bayes ⇒ minimax without constant risk.
11. `[10]` MLE of binomial p: risk p(1−p)/n, worst case 1/(4n) at p = 0.5.
12. `[11]` Minimax estimator of binomial p: (x + √n/2)/(n + √n), constant risk 1/(4(1+√n)²).
13. `[12]` Least favourable prior for that problem: Beta(√n/2, √n/2).
14. `[13]` n = 9: estimator (x+1.5)/12, risk 1/64 = 0.0156; MLE worst case 1/36 = 0.0278; curves cross at 0.1693, 0.8307.
15. `[14]` n = 16: estimator (x+2)/20, risk 1/100 = 0.01; MLE worst case 1/64; curves cross at 0.2 and 0.8.
16. `[15]` x̄ for a normal mean has constant risk σ²/n and is minimax.
17. `[16]` A constant rule 'always answer c' is ADMISSIBLE (risk 0 at θ = c) but not minimax.
18. `[17]` The MLE of a normal mean vector is INADMISSIBLE for dimension ≥ 3 — James–Stein.
19. `[18]` Testing as a decision problem: 0–1 loss, risk = P(type I) on H₀ and P(type II) on H₁.
20. `[19]` Neyman–Pearson constrains size and maximises power; it does not minimise the maximum error, so it is not minimax.
21. `[20]` Bayes rules form a complete class: every admissible rule is a Bayes rule or a limit of them.
22. `[21]` Randomisation is needed for exact size with discrete statistics; it never helps estimation under convex loss.

**Flashcards** `revision.cards[]`

| Front | Back |
|---|---|
| Risk versus Bayes risk | Risk is a function of θ; Bayes risk averages it over a prior to one number |
| Squared-error risk of an estimator | Variance + bias² |
| δ₁ dominates δ₂ means | Risk no larger everywhere, strictly smaller somewhere |
| Admissible means | Nothing dominates it — a weak certificate, not a recommendation |
| Minimax rule | Minimises the worst-case risk, sup_θ R(θ,δ) |
| The relation that finds minimax rules | A Bayes rule with constant risk is minimax |
| Least favourable prior | The prior whose best achievable Bayes risk equals the minimax value |
| Minimax estimator of a binomial p | (x + √n/2)/(n + √n), risk 1/(4(1+√n)²) |
| MLE of binomial p: risk and worst case | p(1−p)/n, worst case 1/(4n) at p = 0.5 |
| Is a constant rule admissible? | Yes — its risk is zero at one θ, so nothing beats it everywhere |
| Famous inadmissibility result | James–Stein dominates the MLE for a normal mean vector, dimension ≥ 3 |
| Weighted absolute loss, k₁ under and k₂ over | The k₁/(k₁+k₂) posterior quantile |

**Memory aids** `revision.tricks[]`

- `[0]` **Risk is a curve; Bayes risk and the minimax value are numbers** — Every confusion in the topic comes from treating risk as a number. Two curves cross, which is why admissibility exists as a concept at all.
- `[1]` **Flat risk plus Bayes equals minimax** — Both conditions are needed. Flat alone is not enough — 'always report x₁' is flat and dominated.
- `[2]` **Admissible is a low bar** — A rule that ignores the data is admissible. It certifies only that nothing beats you everywhere.
- `[3]` **Root n over two** — a = √n/2 in (x + a)/(n + 2a) is the flattening choice, giving risk 1/(4(1+√n)²) and prior Beta(√n/2, √n/2). Three results from one number.
- `[4]` **Neyman-Pearson constrains, minimax equalises** — NP caps one error and minimises the other; a minimax test makes the two errors equal. That is why NP is not a minimax criterion.

**Elimination shortcuts for multiple-choice items** `revision.shortcuts[]`

- `[0]` For an unbiased rule, risk is just the variance — no bias term to compute.
- `[1]` Check any claimed minimax risk for constancy: if it still depends on θ, the flattening condition was not used.
- `[2]` Any option asserting that minimax implies admissible, or the reverse, without a uniqueness qualifier is wrong.
- `[3]` Any option calling a constant rule inadmissible is wrong.
- `[4]` Any option calling the MLE always admissible is wrong — James–Stein, dimension ≥ 3.
- `[5]` If a loss is asymmetric, the Bayes rule moves AWAY from the costlier error, not towards it.

**If nothing else is remembered** `revision.remember[]`

- `[0]` To settle domination, find where the two risk curves cross; one crossing is enough to rule it out both ways.
- `[1]` To find a minimax rule, flatten the risk inside a conjugate family of Bayes rules.

**Errors to avoid** `revision.traps[]`

- `[0]` Treating risk as a single number rather than a function of θ.
- `[1]` Asserting minimax ⇒ admissible, or admissible ⇒ minimax, without the uniqueness condition.
- `[2]` Calling a Bayes rule minimax when its risk is not constant.
- `[3]` Calling the data-ignoring constant rule inadmissible.
- `[4]` Claiming the MLE is always admissible, or forgetting the dimension ≥ 3 condition on James–Stein.
- `[5]` Confusing the minimax value with the smallest risk attainable at some θ.
- `[6]` Forgetting the bias term when a rule is biased, and so reporting a variance as a risk.
- `[7]` Applying asymmetric weights the wrong way round and moving the estimate towards the costlier error.
- `[8]` Assuming an unbiased estimator must be admissible.

---

## Mastery pool — all 20 items with answer keys `qsets/mastery`

Ten are drawn per attempt at 3 easy / 5 moderate / 2 hard. Keys are distributed five to each option letter. Please check each item for a second defensible answer as well as for the correctness of its stated key and explanation.

### Q1 — `inference-t8-m-01` *(single, easy)*

The risk of a decision rule δ is:

*Options* `.options[]`:

- **A.** A single number summarising its quality
- **B.** The loss incurred at the observed sample
- **C.** The expected loss averaged over a prior for θ
- **D.** The expected loss over the sampling distribution, as a function of θ  ← key

*Explanation* `.explanation`: R(θ, δ) = E_θ[L(θ, δ(X))] — an expectation over the DATA with θ held fixed, so it is a function of θ. The averaged-over-a-prior option describes Bayes risk, which is a single number, and the loss at the observed sample is the loss itself, before any expectation is taken at all.

### Q2 — `inference-t8-m-02` *(single, easy)*

A decision rule δ₂ is inadmissible if:

*Options* `.options[]`:

- **A.** Some rule has risk no larger at every θ and strictly smaller at some θ  ← key
- **B.** Its risk is not constant in θ
- **C.** It is not a Bayes rule for any prior
- **D.** Its worst-case risk exceeds that of some other rule

*Explanation* `.explanation`: That is the definition of being dominated. Non-constant risk is irrelevant to admissibility, and having a larger worst case than another rule only means you are not minimax — a rule can lose on the worst case and still be admissible, because the other rule may be worse elsewhere.

### Q3 — `inference-t8-m-03` *(single, easy)*

Under squared-error loss, the risk of an estimator equals:

*Options* `.options[]`:

- **A.** Its variance
- **B.** Its squared bias
- **C.** Its variance plus its squared bias  ← key
- **D.** Its variance minus its squared bias

*Explanation* `.explanation`: Risk under squared error is the mean squared error, which decomposes as variance + bias². It reduces to the variance alone only when the estimator is unbiased — which is why the risk of the sample proportion is just p(1−p)/n.

### Q4 — `inference-t8-m-04` *(single, easy)*

A minimax decision rule is one that minimises:

*Options* `.options[]`:

- **A.** The average risk over a prior
- **B.** The risk at the true parameter value
- **C.** The variance of the estimator
- **D.** The maximum risk over all θ  ← key

*Explanation* `.explanation`: Minimax minimises sup_θ R(θ, δ) — the worst case. Minimising the average risk over a prior gives the Bayes rule, and 'the risk at the true parameter value' is not a usable criterion, since the true value is unknown — that impossibility is the reason the two collapses of the risk curve exist at all.

### Q5 — `inference-t8-m-05` *(numeric, easy)*

For X ~ Bin(n, p), the worst-case risk of the maximum likelihood estimator p̂ = X/n under squared-error loss is:

*Options* `.options[]`:

- **A.** 1/(2n)
- **B.** 1/(4n)  ← key
- **C.** 1/n
- **D.** 1/(4n²)

*Explanation* `.explanation`: p̂ is unbiased, so its risk is Var(p̂) = p(1−p)/n, which is largest at p = 0.5 where p(1−p) = 1/4. The worst case is therefore 1/(4n) — for n = 9 that is 1/36 = 0.0278.

*Arithmetic check* `.check`: Maximise p(1−p) first: it peaks at 1/4 when p = 0.5. Then divide by n.

### Q6 — `inference-t8-m-06` *(single, easy)*

Which relation is used in practice to establish that a rule is minimax?

*Options* `.options[]`:

- **A.** A Bayes rule with constant risk is minimax  ← key
- **B.** Every admissible rule is minimax
- **C.** Every minimax rule is a Bayes rule for the uniform prior
- **D.** An unbiased rule with minimum variance is minimax

*Explanation* `.explanation`: This is the relation that does the work: it converts minimising a supremum into choosing a prior that flattens the risk curve. Admissibility does not imply minimaxity, the least favourable prior is generally not uniform, and minimum-variance unbiasedness is a separate criterion entirely.

### Q7 — `inference-t8-m-07` *(numeric, moderate)*

For X ~ Bin(16, p) under squared-error loss, the minimax estimator of p and its risk are:

*Options* `.options[]`:

- **A.** (x + 2)/20 and 0.0100  ← key
- **B.** (x + 4)/24 and 0.0156
- **C.** (x + 2)/18 and 0.0100
- **D.** (x + 2)/20 and 0.0156

*Explanation* `.explanation`: With a = √n/2 = 2, the estimator is (x + a)/(n + 2a) = (x + 2)/20 and the constant risk is 1/(4(1 + √n)²) = 1/(4 × 25) = 0.0100. The value 0.0156 is 1/64, which is the MLE's worst case for n = 16, and (x + 2)/18 has the wrong denominator — it must be n + 2a, not n + a.

*Arithmetic check* `.check`: Denominator n + 2a = 16 + 4 = 20, and 1/(4(1+4)²) = 1/100. Both must be right for the option to be.

### Q8 — `inference-t8-m-08` *(single, moderate)*

The rule 'ignore the data and always report the constant c' under squared-error loss is:

*Options* `.options[]`:

- **A.** Inadmissible, because it uses no data
- **B.** Minimax, because its risk is constant
- **C.** Admissible, because its risk is zero at θ = c  ← key
- **D.** Neither admissible nor minimax, because its risk is unbounded

*Explanation* `.explanation`: Its risk is (θ − c)², which is zero at θ = c, so no rule can have risk no larger everywhere and strictly smaller somewhere — it is admissible. Its risk is not constant and is unbounded, so it is certainly not minimax. This is the standard demonstration that admissibility is a weak criterion.

### Q9 — `inference-t8-m-09` *(multi, moderate)*

Consider the following statements about the relations between Bayes, minimax and admissible rules.

*Statements to judge* `.statements[]`:

- **A.** A unique Bayes rule is admissible.
- **B.** Every minimax rule is admissible.
- **C.** Every Bayes rule is minimax.
- **D.** A Bayes rule whose risk is constant in θ is minimax.

*Options* `.options[]`:

- **A.** A and B only
- **B.** A, B and C only
- **C.** A and D only  ← key
- **D.** A, B, C and D

*Explanation* `.explanation`: A and D hold. B is false without a uniqueness qualifier — a minimax rule need not be admissible, though a UNIQUE one is. C is false too: a Bayes rule is minimax only if its risk is constant, which most Bayes rules are not.

*Verdict on each statement* `.verdicts`:

- **A — true.** The uniqueness is essential; without it the implication can fail.
- **B — false.** Minimaxity concerns the worst case only; a unique minimax rule is admissible, but not every one.
- **C — false.** Only if its risk is constant. Most Bayes rules have risk that varies with θ.
- **D — true.** A maximum is at least an average, applied once — and the prior is then the least favourable prior.

### Q10 — `inference-t8-m-10` *(numeric, moderate)*

For X ~ Bin(9, p), the risk of the MLE and that of the minimax estimator are equal at:

*Options* `.options[]`:

- **A.** p = 0.25 and 0.75
- **B.** p = 0.1693 and 0.8307  ← key
- **C.** p = 0.2 and 0.8
- **D.** p = 0.5 only

*Explanation* `.explanation`: Set p(1−p)/9 = 1/64, giving p² − p + 9/64 = 0 and p = (1 ± √0.4375)/2 = 0.1693 and 0.8307. The pair 0.2 and 0.8 is the answer for n = 16, where the equation is p² − p + 0.16 = 0 — a genuine result for the wrong sample size.

*Arithmetic check* `.check`: The two roots must be symmetric about 0.5, since p(1−p) is. And at p = 0.5 the MLE's risk is 0.0278 against 0.0156, so they are certainly not equal there.

### Q11 — `inference-t8-m-11` *(single, moderate)*

For a normal mean with known variance σ², the estimator x̄ has risk σ²/n at every θ. It follows that x̄ is:

*Options* `.options[]`:

- **A.** Inadmissible, since shrinkage estimators exist
- **B.** Minimax only if the prior is normal
- **C.** Not minimax, because its risk does not depend on θ
- **D.** Minimax, because its risk is constant  ← key

*Explanation* `.explanation`: Constant risk means the worst case equals the everywhere-case, and no rule can better it in the worst case — so x̄ is minimax. Shrinkage estimators beat it near their target and lose elsewhere, so they do not dominate it in one dimension, and the option denying minimaxity inverts the argument: constant risk is what makes a rule minimax, not what disqualifies it.

### Q12 — `inference-t8-m-12` *(match, moderate)*

Match the criterion in List I with its definition in List II.

*Pairs to match* `.pairs[]`:

| Left | Right |
|---|---|
| A. Risk | I. Minimises the maximum risk over θ |
| B. Bayes risk | II. Not dominated by any other rule |
| C. Minimax rule | III. Expected loss over the data, for a fixed θ |
| D. Admissible rule | IV. Risk averaged over a prior for θ |

*Options* `.options[]`:

- **A.** A-III, B-IV, C-I, D-II  ← key
- **B.** A-I, B-III, C-IV, D-II
- **C.** A-III, B-I, C-II, D-IV
- **D.** A-IV, B-III, C-I, D-II

*Explanation* `.explanation`: Risk is the expected loss over the data for fixed θ; Bayes risk averages that over a prior; a minimax rule minimises the maximum risk; an admissible rule is one that nothing dominates. Each wrong option moves at least two pairs, so the mapping must be checked rather than inferred from one entry.

*Arithmetic check* `.check`: Separate the two that are quantities (risk, Bayes risk) from the two that are properties of a rule (minimax, admissible), and the mapping halves.

### Q13 — `inference-t8-m-13` *(numeric, moderate)*

For X ~ Bin(4, p) under squared-error loss, the minimax value is:

*Options* `.options[]`:

- **A.** 0.0625
- **B.** 0.0278  ← key
- **C.** 0.1250
- **D.** 0.0156

*Explanation* `.explanation`: The minimax value is 1/(4(1 + √n)²) = 1/(4 × 9) = 1/36 = 0.0278. The value 0.0625 is 1/16, which is the MLE's worst case 1/(4n) for n = 4 — a correct quantity for the wrong question, and the distractor most candidates pick.

*Arithmetic check* `.check`: The minimax value must be strictly below the MLE's worst case of 1/(4n) = 0.0625, so 0.0625 cannot be the answer and 0.1250 is larger still.

### Q14 — `inference-t8-m-14` *(single, moderate)*

In decision-theoretic language, a test of hypotheses uses the action space {0, 1} and 0–1 loss. Its risk at a particular θ is:

*Options* `.options[]`:

- **A.** The power of the test
- **B.** The size of the test
- **C.** The probability of an error at that θ  ← key
- **D.** The expected sample size

*Explanation* `.explanation`: With 0–1 loss the expected loss is the probability of taking the wrong action: the probability of a type I error for θ in H₀, and of a type II error for θ in H₁. Size is the supremum of the first over H₀ and power is one minus the second, so both are features of that risk function rather than the risk itself.

### Q15 — `inference-t8-m-15` *(multi, moderate)*

Consider the following statements about admissibility.

*Statements to judge* `.statements[]`:

- **A.** A rule that ignores the data entirely can be admissible.
- **B.** The maximum likelihood estimator is admissible in every problem.
- **C.** An unbiased estimator need not be admissible.
- **D.** Admissibility does not imply minimaxity.

*Options* `.options[]`:

- **A.** A and B only
- **B.** B and C only
- **C.** A, C and D only  ← key
- **D.** A, B and D only

*Explanation* `.explanation`: A, C and D hold. B is false: the maximum likelihood estimator of a normal mean VECTOR is inadmissible once the dimension is three or more, which is the most famous inadmissibility result in the subject.

*Verdict on each statement* `.verdicts`:

- **A — true.** Its risk is zero at one parameter value, so nothing can dominate it.
- **B — false.** For a normal mean vector in dimension three or more, a shrinkage estimator dominates it everywhere.
- **C — true.** Unbiasedness is a constraint, not a guarantee of undominatedness.
- **D — true.** A constant rule is admissible and its worst-case risk is unbounded.

### Q16 — `inference-t8-m-16` *(single, moderate)*

The least favourable prior in a minimax problem is best described as:

*Options* `.options[]`:

- **A.** The prior against which the best achievable Bayes risk is largest  ← key
- **B.** The prior that a cautious statistician would actually believe
- **C.** The uniform prior over the parameter space
- **D.** The prior that minimises the Bayes risk of the minimax rule

*Explanation* `.explanation`: It names the hardest problem in the family — the prior maximising the minimum achievable Bayes risk — and solving that one problem solves the minimax problem. It is a device rather than a belief, and it is generally not uniform: for the binomial problem it is Beta(√n/2, √n/2).

### Q17 — `inference-t8-m-17` *(numeric, hard)*

Under the loss L(θ, a) = 3(θ − a) for a < θ and (a − θ) for a ≥ θ, the Bayes rule is:

*Options* `.options[]`:

- **A.** The posterior median
- **B.** The posterior mean
- **C.** The 0.25 quantile of the posterior
- **D.** The 0.75 quantile of the posterior  ← key

*Explanation* `.explanation`: This is weighted absolute-error loss with k₁ = 3 for under-estimation and k₂ = 1 for over-estimation, and the Bayes rule is the k₁/(k₁ + k₂) quantile — here 3/4. Under-estimating is the costlier error, so the estimate must move ABOVE the median; the 0.25 quantile is the answer with the weights transposed, which is the error the options are built around.

*Arithmetic check* `.check`: Equal weights must give the median, and 1/(1+1) = 1/2 ✓. Then check the direction: costlier under-estimation pushes the estimate up.

### Q18 — `inference-t8-m-18` *(single, hard)*

A rule has perfectly constant risk σ² for every θ, and is not minimax. Which explanation is correct?

*Options* `.options[]`:

- **A.** Constant risk is sufficient for minimaxity, so the premise is impossible
- **B.** Constant risk is only sufficient alongside the rule being a Bayes rule, and this one is not  ← key
- **C.** The risk must be constant AND small for the rule to be minimax
- **D.** Minimaxity requires the risk to be constant and the loss to be bounded

*Explanation* `.explanation`: The relation has two conditions: a BAYES rule with constant risk is minimax. 'Always report x₁' has constant risk σ², is flat as anything, and is dominated by x̄ for every n > 1 — so flatness alone proves nothing. The third option is not a theorem, because 'small' is not a defined condition, and boundedness of the loss is not required.

### Q19 — `inference-t8-m-19` *(numeric, hard)*

For X ~ Bin(25, p), by what factor does the MLE's worst-case risk exceed the minimax value?

*Options* `.options[]`:

- **A.** 1.20
- **B.** 1.44  ← key
- **C.** 1.78
- **D.** 2.25

*Explanation* `.explanation`: The MLE's worst case is 1/(4n) = 1/100 = 0.0100 and the minimax value is 1/(4(1 + √n)²) = 1/(4 × 36) = 1/144 = 0.006944. The ratio is 144/100 = 1.44. In general the factor is (1 + √n)²/n, which equals 1.78 for n = 9 and approaches 1 as n grows — the minimax rule's advantage is a small-sample phenomenon.

*Arithmetic check* `.check`: The general factor is (1+√n)²/n = (1 + 1/√n)². For n = 25 that is (1 + 0.2)² = 1.44.

### Q20 — `inference-t8-m-20` *(single, hard)*

Two rules have identical risk at every value of θ. Which conclusion is correct?

*Options* `.options[]`:

- **A.** Each dominates the other, so both are inadmissible
- **B.** They must be the same rule
- **C.** Both must be minimax
- **D.** Neither dominates the other, so the admissibility of one says nothing about the other  ← key

*Explanation* `.explanation`: Domination requires risk no larger everywhere AND strictly smaller somewhere; identical risk fails the second condition in both directions, so neither dominates. They need not be the same rule — two different rules can be risk-equivalent — and whether either is minimax depends on whether that common risk has the smallest achievable supremum, which identical risk alone does not establish.

---

## Authoring and verification record `provenance`

Reproduced verbatim. It records what changed in each version and how each derivation was checked, including the findings of the two previous review rounds and the reasons some of their recommendations were declined.

> Review pass, October 2026: 3 per-scene quick checks added on theory, worked and explore scenes from a third-party module review, each read for correctness before import; a further set offered for completion and guided scenes was declined, since those scenes already end with the learner writing an answer. Authored for this platform in October 2026. The central worked example was computed from the binomial sum rather than quoted: for n = 9, the rule (x + 1.5)/12 has risk E[(d − p)²] equal to 0.015625 at p = 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 and 0.9 — constant in p, and matching the closed form 1/(4(1 + √n)²) = 1/64. The MLE's risk p(1−p)/9 has worst case 1/36 = 0.027778 at p = 0.5, and the two curves cross where p(1−p)/9 = 1/64, giving p = (1 ± √0.4375)/2 = 0.169281 and 0.830719, both verified to eight decimal places. The identification of (x + √n/2)/(n + √n) as the Bayes rule under Beta(√n/2, √n/2) follows from the Beta(a,a) posterior mean (x + a)/(n + 2a) with a = √n/2, and is what ties this topic to 4.7. The n = 16 case in scenes 7 and 10 was derived the same way: risk 1/100, crossings at p = 0.2 and 0.8.

