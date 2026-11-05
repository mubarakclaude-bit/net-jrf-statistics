# Lesson 4.1 — Sufficiency, Factorisation and Minimal Sufficiency

Complete authored content of one lesson from a UGC-NET Statistics (Code 107) preparation application, extracted from the application's own content files.

| | |
|---|---|
| Content version | 4.3 |
| Scenes | 17 |
| Core scenes | 16 |
| Optional JRF-extension scenes | 1 |
| Estimated learner time | 104 minutes |
| Mastery pool | 20 items |
| Position in the app | Statistical Inference → Data Reduction → Sufficiency |
| Engine | Estimation and inference — where the parameter touches the data, and what may be discarded |
| Pool label | Sufficiency — mastery test (unseen) |
| Unit | IV — Statistical Inference |
| Audience | JRF-target candidates, many returning after several years away |

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

**Shown to the learner before they begin** `howto`

You do not have to understand every formula the first time you meet it. Each section carries one idea, and most of them end with a question — try it before you open the answer, because the attempt is what makes it stick. If a formula feels opaque, the example just above it is where to go back to. One section is marked an optional JRF extension; the topic is complete without it, and it will still be here when you want it.

**Learning objectives** `objectives[]`

1. Prove an instance of sufficiency on a coin, from counting and cancellation alone.

2. Read a joint density as a likelihood, and say why θ-free factors may be discarded.

3. Apply the Fisher–Neyman factorisation theorem, naming both of its conditions.

4. Give the sufficient statistic for the Bernoulli, Poisson, exponential, normal and Uniform families.

5. Establish minimal sufficiency by the ratio criterion, and let the criterion produce the statistic.

6. Recognise which of the three standard phrasings a question is using, and do the matching work.

7. Say which transformations preserve sufficiency, and what is and is not unique.

8. Relate sufficiency to completeness, to Rao–Blackwell and to the MLE, and state what does not follow.

**Assumed prior knowledge** `prereq[]`

- `prereq[0]` **iid samples, and what a parameter is** — Independence is the only reason you may multiply probabilities, and θ is the knob every question is about.
- `prereq[1]` **Multiplying probabilities, and counting arrangements** — The opening proof is p^t(1−p)^(n−t) divided by C(n,t)·p^t(1−p)^(n−t). Nothing harder is needed to start.
- `prereq[2]` **Densities of the standard families, including supports** — The Uniform case hides the parameter in an indicator, and candidates who skip the support condition miss it entirely. The lesson restates each density as it is used.
- `prereq[3]` **Order statistics, and what 'a function of' means** — Minimality is defined by 'is a function of every other sufficient statistic', and the order statistics are the reduction that always exists.

**Misconceptions the lesson is built to pre-empt** `traps[]`

- For Uniform(0, θ) the sufficient statistic is the maximum, not Σxᵢ.

- With σ² unknown the normal needs (Σxᵢ, Σxᵢ²); only with σ² known does Σxᵢ suffice.

- A minimal sufficient statistic is not unique; the partition it induces is.

- Only one-to-one functions of a sufficient statistic are guaranteed sufficient.

- A complete sufficient statistic is minimal sufficient, but minimal sufficiency does not imply completeness.

- The dimension of a minimal sufficient statistic can exceed the dimension of the parameter — Uniform(θ, θ+1).

- The Cauchy location family reduces no further than the order statistics.

- Sufficiency is relative to the model: changing what is known changes the statistic, with the data unchanged.

- A sufficient statistic need not be an estimator of θ, and need not be unbiased or low-variance.

**Assessment policy** `mastery`

- 10 items drawn per attempt from a pool of 20, mix 3 easy, 5 moderate, 2 hard
- pass mark 80%, no hints during the test, retest after 7 days
- `mastery.note`: Platform settings, not an NTA rule. Ten drawn from a pool of twenty at 3 easy / 5 moderate / 2 hard; a retake draws again, holding the mix and pulling back items previously got wrong.

**Sources** `refs[]`

- `refs[0]` **Definition of Sufficiency, and the Factorization Theorem** — Penn State online notes, STAT 415, Lesson 24.1 and 24.2 (University course notes, free). The cleanest statement of both definitions at exactly this level, with the Bernoulli conditional-distribution argument worked out in 24.1 and three factorisations — Poisson, normal, exponential — in 24.2. Start here if scene 6 moved too quickly.
- `refs[1]` **Mathematical Statistics 18.655 — lecture notes** — MIT OpenCourseWare, Session 6 Sufficiency; Sessions 7-8 Exponential Families I and II (Graduate lecture notes (PDF), free). The measure-theoretic treatment, and the proof that the minimal sufficient statistic is the likelihood up to proportionality. Beyond what NET asks, but it is where the exponential-family explanation in scene 6 comes from.
- `refs[2]` **Statistical Inference** — NPTEL / SWAYAM — IIT Delhi, Prof. Niladri Chatterjee, Theory of estimation and testing, taught for an Indian audience (Free video course with assignments, free). Indian, free, and pitched at exactly this syllabus. Useful if you would rather be taught this topic than read it — and a good second pass if the gap has been a long one.
- `refs[3]` **Statistical Inference, 2nd edition** — Casella and Berger, Chapter 6, Principles of Data Reduction — 6.2.1 factorisation, 6.2.2 minimal sufficiency (Textbook). The standard reference for this unit. Section 6.2.2 contains the ratio criterion used in scenes 10 and 12, and Exercise 6.9 is the Uniform(theta, theta+1) case that scene 14 works through.
- `refs[4]` **An Introduction to Probability and Statistics, 3rd edition** — Rohatgi and Saleh, Chapter 8, Sufficiency and completeness (Textbook). The text most Indian MSc courses set, so its notation is the one NET questions tend to follow. Worth comparing with Casella and Berger where the two differ on how minimal sufficiency is introduced.

---

## The lesson, scene by scene

### Scene 1 of 17 — Four small things, and none of them hard

`scenes[0]` · id `s0` · type `foundation` (prerequisite check) · 4 minutes

**Purpose** `scenes[0].objective`

Check the four tools this lesson picks up — all of them arithmetic — so that nothing later arrives unannounced.

**Body** `scenes[0].body[]`

Start here, but do not let this scene stop you. The four questions below are the tools the lesson picks up, not the lesson itself. Mark anything shaky and read the rebuild — that is exactly what the rebuilds are for, and nothing is being scored.

If you have been away from the subject for a few years, expect two or three of these to feel shaky. That is the normal starting position, not a sign you are in the wrong place. The next three scenes assume nothing beyond a coin and arithmetic, and they rebuild the important ideas from the ground up.

Read them in order if you can. Taken together these four ARE the proof that opens the lesson — you will have derived the main idea before you meet its name.

**Check 1** `scenes[0].items[0]`

- *asks:* What does it mean to call X₁, …, Xₙ an iid sample, and what is a parameter?
- *expected answer* `.recall`: iid means independent and identically distributed: the observations do not influence one another, and all of them come from the same distribution. A parameter is an unknown constant that picks out which distribution in a family you have — p for a coin, λ for a Poisson count, (μ, σ²) for a normal.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Two words, and each one buys you something specific. INDEPENDENT means the probability of the whole sample is the product of the individual probabilities — that is the only reason you are ever allowed to multiply. IDENTICALLY DISTRIBUTED means there is one unknown to find rather than n of them: the same p governs every toss.

> A parameter is best pictured as a knob on the machine generating your data. The family — Bernoulli, Poisson, normal — says what kind of machine it is. The parameter says where the knob is set. Statistical inference is the business of guessing the knob from the output.

> Throughout this topic θ (theta) is a stand-in for whichever parameter the family happens to have. When you see θ, read it as 'the unknown' — p, or λ, or the pair (μ, σ²), whichever the question gave you.

**Check 2** `scenes[0].items[1]`

- *asks:* A coin is tossed three times and comes up H, T, H. If the chance of heads is p, what is the probability of exactly that sequence?
- *expected answer* `.recall`: p × (1 − p) × p = p²(1 − p). You multiply because the tosses are independent; each head contributes a factor p and each tail a factor (1 − p).

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> Write it out in order: heads gives p, tails gives (1 − p), heads gives p. Multiply, because the tosses do not influence each other: p · (1 − p) · p = p²(1 − p).

> Now do the same for n tosses that produced t heads and n − t tails. Each head contributes p and each tail contributes (1 − p), so the probability of that particular sequence is p^t (1 − p)^(n − t).

> Look hard at that expression, because it is the whole lesson in one line. It depends on t — how MANY heads — and on nothing else. Where the heads fell does not appear anywhere in it. Two different sequences with the same number of heads have exactly the same probability, whatever p is. You have just derived the main idea of this topic without being told its name.

**Check 3** `scenes[0].items[2]`

- *asks:* What does C(5,3) equal, and what does it count?
- *expected answer* `.recall`: C(5,3) = 10. It counts the number of ways of choosing 3 positions out of 5 — so the number of different five-toss sequences that contain exactly three heads.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> The formula is C(n,t) = n! / (t!(n − t)!). For n = 5 and t = 3: 5! = 120, 3! = 6, 2! = 2, so C(5,3) = 120/(6 × 2) = 10.

> What it counts is more useful than the formula. Fix the number of heads at three and ask which three of the five tosses they were: HHHTT, HHTHT, HHTTH, HTHHT, and so on. There are ten such sequences and no eleventh.

> You will divide by this number in the very next scene, and the division is where the number 1/10 comes from. For ten tosses with seven heads the same count is C(10,7) = 120, and the answer there is 1/120.

**Check 4** `scenes[0].items[3]`

- *asks:* What does it mean to say a quantity 'does not depend on p'?
- *expected answer* `.recall`: That p does not appear in it once the algebra is simplified — so its value is the same whatever the true p happens to be. 1/10 does not depend on p; p²(1 − p) does.

*Rebuild shown if the learner marks this shaky* `.refresh[]`:

> This is the pivot the entire topic turns on, and it is simpler than the phrase makes it sound. A quantity depends on p if changing p changes it. 1/10 is 1/10 whether p is 0.1 or 0.9, so it does not depend on p.

> The interesting case is a quantity that LOOKS like it depends on p until you simplify. Divide p³(1 − p)² by 10 p³(1 − p)² and every p cancels: what is left is 1/10. The p was there in both the top and the bottom, and it went away.

> Why it matters: if a quantity has no p in it, then watching that quantity teaches you nothing about p. Turn that around and you have the definition coming in scene 2 — if, after keeping some summary of the data, what is left over has no p in it, then the left-over part was never telling you anything about p and can be thrown away. Almost every definition in this lesson is a sentence of the form 'something does not depend on the parameter'. Get comfortable with that phrase and the definitions stop being frightening.

**Quick check before moving on** `scenes[0].ask`

- *question:* X₁, X₂, X₃ are three independent tosses of a coin whose chance of heads is p, and the result comes out H, T, H. What is the probability of exactly that sequence?
- *hint on request:* One factor per toss — p for a head, (1 − p) for a tail — multiplied together, because the tosses are independent.

---

### Scene 2 of 17 — Ten tosses, and the one number that replaces them

`scenes[1]` · id `s1` · type `intuition` (intuition) · 6 minutes

**Purpose** `scenes[1].objective`

Prove an instance of sufficiency on a coin, with real numbers and no notation beyond counting.

**Body** `scenes[1].body[]`

Here is the whole topic, done on a coin, before any notation. A coin has an unknown chance p of coming up heads. You toss it ten times and write down what happened:

H  T  H  H  T  H  T  H  H  H

Count them: seven heads, three tails.

Now the question the topic exists to answer. If your aim is to say something about p, do you need that sequence, or would the single number 7 have served just as well?

Intuitively the number ought to be enough. Nothing in the setup says heads prefer to arrive early. But intuition is not an argument, and checking it is the actual content of this topic — so let us check it.

Any particular ten-toss sequence with seven heads has probability p⁷(1 − p)³: seven factors of p, three factors of (1 − p), multiplied together because the tosses are independent. Notice what is NOT in that expression — any mention of WHICH tosses were heads. Every sequence with seven heads has exactly the same probability as every other.

How many such sequences are there? That is the counting question from the last scene: C(10,7) = 120. So the probability of getting seven heads in some order or other is 120 · p⁷(1 − p)³.

Now the step that matters. Suppose someone tells you only the count — seven — and you ask how likely your particular sequence was, given that count. Divide the one by the other: p⁷(1 − p)³ ⁄ [120 · p⁷(1 − p)³] = 1/120. Every p cancels. Whatever p is — 0.1, 0.5, 0.9 — once the total is known to be seven, each of the 120 arrangements is equally likely, with probability 1/120.

Read what that means, slowly, because it is the definition you are about to be given. The arrangement carries no information about p. It is not that the arrangement is uninteresting — it is that once the total is fixed, the distribution of the arrangement has no p in it at all. Someone who knew only the number 7 could manufacture a perfectly plausible sequence by picking one of the 120 at random, and would not need to know p to do it. The arrangement is noise, generated independently of the thing you are trying to learn.

That is what SUFFICIENCY means, and you have just proved an instance of it from arithmetic. The total number of heads is a sufficient statistic for p. Nine of your ten numbers can be thrown away and nothing about p is lost.

The rest of the lesson does two things with that. It gives you a way of finding the number-that-replaces-the-data without computing any conditional probability, because the cancellation above gets unpleasant in bigger families — that is the factorisation theorem. And it asks whether you can go further still, down to something smaller — that is minimal sufficiency.

**Aside — The sentence to carry out of this scene** `scenes[1].aside.body`

A statistic is sufficient when, once you know it, the distribution of everything else has no parameter left in it. You have now proved that once: given the total, each arrangement has probability 1/C(n,t), and the p's are gone.

**Quick check before moving on** `scenes[1].ask`

- *question:* You tossed the coin ten times and got seven heads. A friend tossed the same coin ten times and also got seven heads, but in a different order. Is there any question about p on which the two of you should give different answers?
- *hint on request:* You both have the same total. Ask what the 1/120 computation says about how much the order could possibly be telling either of you.

---

### Scene 3 of 17 — A statistic is not an estimate

`scenes[2]` · id `s1b` · type `theory` (theory) · 4 minutes

**Purpose** `scenes[2].objective`

Separate three words the exam keeps apart — statistic, estimator, estimate — before they can be confused.

**Block 1 — Why this scene is here, this early** `scenes[2].blocks[0]` *(type `def`)*

You have just produced the number 7 from ten tosses, and the natural next thought is 'so my answer for p is 0.7'. That thought is correct arithmetic and the wrong topic. Sufficiency is about which SUMMARY of the data keeps the information. Estimation — what to guess, and how good the guess is — is topic 4.4. Candidates who meet sufficiency through the sentence 'count the heads, so p̂ = 0.7' carry the confusion into the exam hall, so it is worth four minutes now.

**Block 2 — The three words, with the coin as the example** `scenes[2].blocks[1]` *(type `assume`)*

A STATISTIC is any quantity computed from the sample and nothing else: the number of heads (7), the sample proportion (0.7), the maximum, the whole sample. It may not use an unknown parameter. An ESTIMATOR is a statistic you have chosen in order to guess a parameter — the proportion, used for p. An ESTIMATE is the number that estimator returns for the sample in hand: 0.7. So 7 and 0.7 are both statistics; only 0.7 is an estimate of p, and 7 could not be one, because a probability cannot be 7.

**Block 3 — Both can be sufficient, and sufficiency does not care which** `scenes[2].blocks[2]` *(type `step`)*

Σxᵢ = 7 is sufficient for p. So is x̄ = 0.7, because each can be computed from the other once n is fixed. Sufficiency is a property of the information a summary carries, not of whether the summary is on the right scale to be an answer. That is why the sufficient statistic for an exponential sample is Σxᵢ and not n/Σx, even though n/Σx is the thing you would quote as an estimate of the rate.

**Block 4 — What follows, and what does not** `scenes[2].blocks[3]` *(type `trap`)*

A sufficient statistic need not be unbiased, need not have small variance, and need not estimate θ at all. Nothing about sufficiency makes a statistic a good estimator, and nothing about being a good estimator makes a statistic sufficient. The two properties travel together often enough in the standard families that the exam tests whether you know they are separate.

**Quick check before moving on** `scenes[2].ask`

- *question:* Ten tosses give seven heads. Is ΣXᵢ an estimate of p?
- *hint on request:* Write down the value ΣXᵢ takes, and ask whether that number could be a probability.

---

### Scene 4 of 17 — The likelihood — one formula, read backwards

`scenes[3]` · id `s2` · type `theory` (theory) · 5 minutes

**Purpose** `scenes[3].objective`

Read the joint density as a function of the parameter, and meet every symbol the lesson will use, once each.

**Block 1 — Two readings of the same formula** `scenes[3].blocks[0]` *(type `def`)*

You already wrote p^t(1 − p)^(n − t) for the coin. That expression can be read in two directions. Read as a function of the DATA with p fixed, it is a probability: how likely this sequence was. Read as a function of P with the data fixed, it is the likelihood: how well each candidate value of p accounts for what you actually saw. Same algebra, two viewpoints — and the switch between them is the whole of this topic. Sufficiency asks: when the formula is read the second way, which parts of the data does it actually involve?

**Block 2 — Every symbol in this lesson, once each** `scenes[3].blocks[1]` *(type `assume`)*

θ (theta) — the unknown, whichever one the family has: p, or λ, or the pair (μ, σ²). x = (x₁, …, xₙ) — the numbers you observed. f(x | θ) — the joint density or probability of the whole sample, for a given θ. L(θ) — the same expression read as a function of θ. T(x) — a statistic: any number (or pair of numbers) computed from the data. Σxᵢ — add up the observations. ∏ — multiply them. ∝ — 'equal apart from a factor that contains no θ'. I(condition) — an indicator: 1 when the condition holds, 0 when it does not. Nothing else is introduced without being named.

**Block 3 — The coin's joint probability, in symbols, slowly** `scenes[3].blocks[2]` *(type `step`)*

With xᵢ = 1 for heads and 0 for tails, the number of heads is Σxᵢ, and the probability of the observed sequence is f(x | p) = p^Σx (1 − p)^(n − Σx). Check it against the last scene: with n = 10 and Σx = 7 that is p⁷(1 − p)³, which is where you started. The notation has added nothing except the ability to say it for any n.

**Block 4 — Why a factor with no θ in it can be thrown away** `scenes[3].blocks[3]` *(type `def`)*

Compare the likelihood at two candidate values of θ. A factor that contains no θ multiplies the value at BOTH candidates by the same amount, so it cannot change which candidate comes out higher, nor where the curve peaks, nor its shape. It is a scale on the vertical axis and nothing more. That is why ∝ is the working symbol in this topic, and why the first instinct in every problem is to sweep the θ-free factors aside and see what is left holding the data.

**Block 5 — The exam tell** `scenes[3].blocks[4]` *(type `step`)*

Whatever the family, the first move never changes: write the joint density, including its support, then ask where θ touches the data. In an exponent that gives you a sum. In a support indicator it gives you an extreme value. In n separate denominators it gives you nothing. Everything else in this lesson is that one question, applied.

**Quick check before moving on** `scenes[3].ask`

- *question:* A factor of the joint density that contains no θ can be discarded when you are hunting for a sufficient statistic. Why does throwing it away cost nothing?
- *hint on request:* Picture the likelihood curve. Ask what multiplying every point of it by the same number does to the position of its peak.

---

### Scene 5 of 17 — Two different samples, one identical curve

`scenes[4]` · id `s3` · type `explore` (interactive visualisation) · 4 minutes

**Purpose** `scenes[4].objective`

See that two samples sharing a sufficient statistic give the same likelihood curve, and nothing else.

**Body** `scenes[4].body[]`

You proved the coin case by cancelling. Now see the same fact as a picture. The picture needs one new density, and it is the simplest in the syllabus: the exponential, f(x | λ) = λe^(−λx) for x > 0, the standard model for a waiting time, where λ is the rate. For an iid sample of size n you multiply, which gives f(x | λ) = λⁿ e^(−λΣx).

Below is the likelihood of λ for such a sample, with sliders for the sample size n, for the total Σxᵢ, and for the candidate λ. Look at the sliders before you look at the curve, and notice what is missing: there is no slider for the individual observations. There is nowhere to type them in, because the curve does not depend on them.

That is sufficiency as a picture. The sample (1, 2, 9) and the sample (4, 4, 4) both have n = 3 and Σxᵢ = 12. They give the identical curve — same peak, same width, same everything. Any statement about λ you could read off this curve must be the same for both samples, because there is nothing in the picture that distinguishes them.

Now change Σxᵢ from 12 to 24, holding n at 3, and watch the peak slide from λ̂ = n/Σx = 0.25 to 0.125. So the total does carry information — a different total gives a different answer. Σxᵢ is not discarding information about λ; it is discarding everything EXCEPT information about λ.

Finally raise n and the total together — n = 6 with Σx = 24, then n = 12 with Σx = 48 — and the peak stays near 0.25 while the curve narrows. That narrowing is information accumulating as the sample grows, and it belongs to topic 4.6. Here the only point is that n and Σxᵢ between them are enough to draw the entire curve.

And the factorisation is already visible: f(x | λ) = λⁿ e^(−λΣx) is g(T, λ) = λⁿ e^(−λT) with T = Σxᵢ, times h(x) = 1. You have now met the same statistic twice, from two directions — by cancelling a conditional probability, and by splitting a density into two factors.

**Interactive element** `scenes[4].viz` — live plot of type `exp-likelihood`, initial state n=3, sumx=12. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[4].ask`

- *question:* (1, 2, 9) and (4, 4, 4) give the identical likelihood for λ. Does that mean the two samples were equally probable to occur?
- *hint on request:* Separate 'what these data say about λ' from 'how probable this particular dataset was'. Only the first of the two is what sufficiency is about.

---

### Scene 6 of 17 — The coin again, in exam form — all three questions

`scenes[5]` · id `s4` · type `worked` (worked example) · 9 minutes

**Purpose** `scenes[5].objective`

Verify sufficiency by definition, by factorisation, and establish minimality, in one pass.

**Problem put to the learner** `scenes[5].problem`

X₁,…,Xₙ are iid Bernoulli(p). (a) Show T = ΣXᵢ is sufficient directly from the definition. (b) Confirm it by factorisation. (c) Show it is minimal sufficient. (d) Say whether x̄ and (ΣXᵢ, X₁) are sufficient, and whether they are minimal.

**Worked steps** `scenes[5].steps[]`

1. `scenes[5].steps[0]` (a) First by the definition. Write the probability of one particular sequence with t ones. You did this on the coin two scenes ago; here it is for any n.

   ```
   P(X = x) = p^t (1 − p)^(n − t),   where t = Σxᵢ
   ```

   Laid out:

   $$P(X = x) = p^{t} (1 − p)^{n − t},   where t = Σxᵢ$$

   *why* `.why`: Every sequence with the same number of ones has the SAME probability — the arrangement does not appear anywhere in the expression. That one observation is the whole proof, and the rest is bookkeeping.

2. `scenes[5].steps[1]` Write the probability that the statistic takes that value.

   ```
   P(T = t) = C(n, t) p^t (1 − p)^(n − t)
   ```

   Laid out:

   $$P(T = t) = C(n, t) p^{t} (1 − p)^{n − t}$$

   *why* `.why`: There are C(n, t) sequences with t ones and each has the probability above, so the count is the only new factor. For n = 10 and t = 7 that count is 120, which is the number you divided by earlier.

3. `scenes[5].steps[2]` Divide, to get the conditional distribution of the sample given the statistic.

   ```
   P(X = x | T = t) = p^t(1−p)^(n−t) / [C(n,t) p^t(1−p)^(n−t)] = 1/C(n, t)
   ```

   Laid out:

   $$P(X = x | T = t) = \frac{p^{t}(1−p)^{n−t}}{[C(n,t) p^{t}(1−p)^{n−t}]} = \frac{1}{C(n, t)}$$

   *why* `.why`: The p's cancel completely and a bare number is left. For n = 5, t = 3 it is 1/10; for n = 10, t = 7 it is 1/120. There is no p in it for any t, so T is sufficient — by the definition, with nothing assumed.

4. `scenes[5].steps[3]` (b) Now the factorisation route, which is what you would actually write under time pressure. Start from the joint probability.

   ```
   f(x | p) = p^Σx (1 − p)^(n − Σx)
   ```

   Laid out:

   $$f(x | p) = p^{Σx} (1 − p)^{n − Σx}$$

   *why* `.why`: The same expression as in (a), with Σx written where t was.

5. `scenes[5].steps[4]` Split the second factor, so that its exponent stops mixing n with Σx.

   ```
   (1 − p)^(n − Σx) = (1 − p)ⁿ / (1 − p)^Σx
   ```

   Laid out:

   $$(1 − p)^{n − Σx} = \frac{(1 − p)ⁿ}{(1 − p)^{Σx}}$$

   *why* `.why`: This is the only algebraic move in the derivation and it is just the index law a^(b−c) = a^b/a^c. It is also the line most books leave out, which is what makes the next one look like a conjuring trick.

6. `scenes[5].steps[5]` Put it back together and collect the powers of Σx.

   ```
   f(x | p) = p^Σx · (1 − p)ⁿ/(1 − p)^Σx = [p/(1 − p)]^Σx (1 − p)ⁿ · 1
   ```

   Laid out:

   $$f(x | p) = p^{Σx} · \frac{(1 − p)ⁿ}{(1 − p)^{Σx}} = \frac{p}{(1 − p)}^{Σx} (1 − p)ⁿ · 1$$

   *why* `.why`: Set g(T, p) = [p/(1 − p)]^T (1 − p)ⁿ and h(x) = 1. The data enters g only through Σxᵢ, and h contains no p, so both conditions of the theorem hold. Two lines against six — this is why the theorem exists.

7. `scenes[5].steps[6]` (c) For minimality, form the ratio of the joint probabilities at two different samples of the same size.

   ```
   f(x | p)/f(y | p) = p^(Σx−Σy) (1−p)^(Σy−Σx) = [p/(1 − p)]^(Σx − Σy)
   ```

   Laid out:

   $$\frac{f(x | p)}{f(y | p)} = p^{Σx−Σy} (1−p)^{Σy−Σx} = \frac{p}{(1 − p)}^{Σx − Σy}$$

   *why* `.why`: Everything else cancels because both samples have n observations.

8. `scenes[5].steps[7]` Ask when that ratio is free of p.

   ```
   [p/(1−p)]^(Σx−Σy) is constant in p  ⟺  Σx − Σy = 0  ⟺  Σx = Σy
   ```

   Laid out:

   $$\frac{p}{(1−p)}^{Σx−Σy} is constant in p  ⟺  Σx − Σy = 0  ⟺  Σx = Σy$$

   *why* `.why`: The base p/(1 − p) genuinely moves as p runs across (0,1) — from 0 up to infinity — so the only way a power of it can stay constant is for the exponent to be zero. By the criterion in scene 10, T = Σxᵢ is therefore MINIMAL sufficient.

9. `scenes[5].steps[8]` (d) x̄ first.

   ```
   x̄ = (1/n)Σxᵢ is a one-to-one function of Σxᵢ for fixed n
   ```

   Laid out:

   $$x̄ = \frac{1}{n}Σxᵢ is a one-to-one function of Σxᵢ for fixed n$$

   *why* `.why`: One-to-one functions of a sufficient statistic are sufficient, and of a minimal sufficient statistic are minimal sufficient. So x̄ is both. Note that 'minimal' does not mean unique — Σxᵢ and x̄ are different statistics and both are minimal sufficient, because each can be computed from the other.

10. `scenes[5].steps[9]` Now (ΣXᵢ, X₁).

   ```
   sufficient ✓ (it determines ΣXᵢ)   but NOT minimal ✗ (ΣXᵢ is a function of it, not conversely)
   ```

   *why* `.why`: Carrying the first observation alongside the total is harmless but wasteful: it is a finer statistic than it needs to be. Minimality is precisely the demand that no further reduction is possible, and here one is.

**What to take from it** `scenes[5].after`

Three routes, one answer. Carry the factorisation for speed, the conditional-distribution argument for a 'prove from the definition' question, and the ratio in step 7 for minimality. Carry the two numbers too: 1/C(n,t) for the conditional law, and 1/10 for n = 5, t = 3. If only one line of this scene survives to the exam hall, make it step 7 — the ratio is the tool that hands you the answer instead of asking you to guess it.

**Quick check before moving on** `scenes[5].ask`

- *question:* Part (d) found that (ΣXᵢ, X₁) is sufficient but not minimal. In one sentence, what is wrong with it?
- *hint on request:* Ask what you could still throw away from that pair without losing anything about p.

---

### Scene 7 of 17 — The factorisation theorem, and the families it settles

`scenes[6]` · id `s5` · type `theory` (theory) · 8 minutes

**Purpose** `scenes[6].objective`

State sufficiency two ways, apply the theorem to every standard family, and know what is not unique.

**Block 1 — What the theorem buys you** `scenes[6].blocks[0]` *(type `def`)*

You have now verified sufficiency twice for the same statistic: once by computing a conditional probability and cancelling, once by splitting the density into two factors. The second took two lines and the first took six. The factorisation theorem says the short route always works — that splitting the density is not a lucky shortcut for the coin, but an exact test, valid in both directions, for every family you will meet.

**Block 2 — Sufficiency, by definition** `scenes[6].blocks[1]` *(type `def`)*

A statistic T = T(X) is sufficient for θ if the conditional distribution of X given T = t does not depend on θ, for every t. Equivalently: someone who knows only T could simulate the rest of the sample without knowing θ — which is exactly what picking one of the 120 arrangements at random amounts to. The definition is exact but awkward to apply, because it requires the conditional distribution.

**Block 3 — The Fisher–Neyman factorisation theorem** `scenes[6].blocks[2]` *(type `formula`)*

T is sufficient for θ if and only if the joint density factorises as f(x | θ) = g(T(x), θ) · h(x), where h does not involve θ and g involves the data only through T(x). This is the working tool: no conditional distributions, just algebra. Note both requirements — h free of θ AND g touching the data only via T.

**Block 4 — Bernoulli, Poisson, exponential** `scenes[6].blocks[3]` *(type `step`)*

Bernoulli: f = p^Σx(1−p)^(n−Σx) = [p/(1−p)]^Σx (1−p)ⁿ · 1 by the split in the last scene, so T = Σxᵢ with h = 1. Poisson: multiply the individual terms e^(−λ)λ^xᵢ/xᵢ! to get f = e^(−nλ) λ^Σx · 1/∏xᵢ!, so T = Σxᵢ with h = 1/∏xᵢ! — the factorials carry no λ, which is the whole reason they may be set aside. Exponential with rate λ: f = λⁿe^(−λΣx) · 1, so T = Σxᵢ. Three families, one statistic — which is no coincidence, as the exponential-family block below explains.

**Block 5 — Normal, both cases** `scenes[6].blocks[4]` *(type `step`)*

Start by expanding the exponent: Σ(xᵢ − μ)² = Σxᵢ² − 2μΣxᵢ + nμ². With σ² KNOWN: f ∝ exp{−[Σxᵢ² − 2μΣxᵢ + nμ²]/2σ²} = exp{(μΣxᵢ − nμ²/2)/σ²} · exp{−Σxᵢ²/2σ²}(2πσ²)^(−n/2). The second factor contains no μ, so it is a legitimate h, and T = Σxᵢ, equivalently x̄. With BOTH UNKNOWN: σ² now sits inside that second factor, so it is no longer free of the parameter and cannot be h; the exponent needs Σxᵢ and Σxᵢ² separately. Then T = (Σxᵢ, Σxᵢ²), equivalently (x̄, s²).

**Block 6 — Uniform(0, θ), where the parameter hides in an indicator** `scenes[6].blocks[5]` *(type `formula`)*

f(x | θ) = θ^(−n) · I(0 ≤ x₍₁₎) · I(x₍ₙ₎ ≤ θ). The last indicator is the only place the data meets θ, so T = x₍ₙ₎ = max xᵢ, with h = I(x₍₁₎ ≥ 0). This is the family where candidates look for a sum and find none; the rule is to treat the support condition as part of the density, not as a side remark.

**Block 7 — The exponential family, which explains the pattern** `scenes[6].blocks[6]` *(type `def`)*

If f(x | θ) = h(x) c(θ) exp{Σⱼ wⱼ(θ) tⱼ(x)} — where h(x) carries no θ, c(θ) carries no data, the wⱼ are functions of the parameter and the tⱼ are functions of one observation — then (Σᵢt₁(xᵢ), …, Σᵢt_k(xᵢ)) is sufficient for θ. The Bernoulli, Poisson, exponential, normal, gamma and beta families are all of this form, which is why a sum keeps appearing. The Uniform and the Cauchy are not, and that is exactly why they behave differently — one reduces to a maximum and the other does not reduce at all.

**Block 8 — What is not unique, and what always works** `scenes[6].blocks[7]` *(type `trap`)*

Sufficient statistics are not unique. The whole sample X is trivially sufficient. The order statistics are sufficient for any iid sample. Any ONE-TO-ONE function of a sufficient statistic is sufficient — so Σxᵢ, x̄ and 2Σxᵢ + 7 are all sufficient in the Bernoulli case, and a question asking 'which of these is sufficient' may have several correct answers unless it asks for the minimal one. A many-to-one function of a sufficient statistic need NOT be sufficient, which is the trap in the other direction — but note that it need not fail either: the whole sample is sufficient, and Σxᵢ is a many-to-one function of it that is also sufficient. One-to-one is what GUARANTEES sufficiency is preserved; many-to-one has to be checked.

**Block 9 — The exam tell — three phrasings, three different jobs** `scenes[6].blocks[8]` *(type `step`)*

'Find a sufficient statistic' means factorise the density. 'Find the minimal sufficient statistic', or 'the smallest', means form the ratio at two samples. 'Show from the definition' means compute the conditional distribution and show θ cancelling. The three are not interchangeable and the marks are awarded for doing the one that was asked.

**Reference table** `scenes[6].table`

| Family | Sufficient statistic | Where θ meets the data |
|---|---|---|
| Bernoulli(p) | Σxᵢ | the exponent, after splitting (1−p)ⁿ out |
| Poisson(λ) | Σxᵢ | the exponent; the factorials are h(x) |
| Exponential, rate λ | Σxᵢ | the exponent; h(x) = 1 |
| Normal, σ² known | Σxᵢ, equivalently x̄ | the exponent's cross term only |
| Normal, both unknown | (Σxᵢ, Σxᵢ²), equivalently (x̄, s²) | both exponent terms |
| Uniform(0, θ) | max xᵢ | the support indicator I(max ≤ θ) |

*caption* `.caption`: The six to know cold. Learn the third column rather than the second: the question 'where does θ touch the data' reproduces the middle column every time, and it also handles the families that are not in this table.

**Flow diagram** `scenes[6].flow` — From the joint density to the reduction, and what each family gives

- row 1: Joint density f(x | θ) of an iid sample
- row 2: Factorise: f = g(T(x), θ) · h(x), h free of θ
- row 3: Bernoulli · Poisson · exponential → Σxᵢ  |  Normal, σ² known → Σxᵢ  |  Normal, both → (Σxᵢ, Σxᵢ²)  |  Uniform(0,θ) → max xᵢ
- row 4: Cauchy → the order statistics, no reduction  |  Minimal? test f(x|θ)/f(y|θ) free of θ
- arrows: Joint density f(x | θ) of an iid sample → Factorise: f = g(T(x), θ) · h(x), h free of θ; Factorise: f = g(T(x), θ) · h(x), h free of θ → Bernoulli · Poisson · exponential → Σxᵢ; Factorise: f = g(T(x), θ) · h(x), h free of θ → Normal, σ² known → Σxᵢ; Factorise: f = g(T(x), θ) · h(x), h free of θ → Normal, both → (Σxᵢ, Σxᵢ²); Factorise: f = g(T(x), θ) · h(x), h free of θ → Uniform(0,θ) → max xᵢ; Factorise: f = g(T(x), θ) · h(x), h free of θ → Cauchy → the order statistics, no reduction; Bernoulli · Poisson · exponential → Σxᵢ → Minimal? test f(x|θ)/f(y|θ) free of θ; Normal, both → (Σxᵢ, Σxᵢ²) → Minimal? test f(x|θ)/f(y|θ) free of θ; Uniform(0,θ) → max xᵢ → Minimal? test f(x|θ)/f(y|θ) free of θ

**Quick check before moving on** `scenes[6].ask`

- *question:* The theorem has two conditions. If you factorise a density and your h(x) turns out to contain θ, have you shown that your T is sufficient?
- *hint on request:* Read the statement again and check both halves of it, not just the one about g.

---

### Scene 8 of 17 — Change the model and the answer changes

`scenes[7]` · id `s6` · type `intuition` (intuition) · 4 minutes

**Purpose** `scenes[7].objective`

See that sufficiency is a property of the model rather than of the data, which is what the exam tests.

**Body** `scenes[7].body[]`

One idea separates a candidate who has understood this topic from a candidate who has memorised it, and this is it: sufficiency is a property of the MODEL, not of the data.

Take a normal sample and hold the numbers absolutely fixed. If σ² is known, Σxᵢ is sufficient and everything else may be discarded. If σ² is unknown, Σxᵢ is not sufficient any more — you now need Σxᵢ² as well. Not one number in the sample changed. The family of distributions changed, and with it what counts as noise.

So the question 'what is the sufficient statistic for this data' is malformed. Data do not have sufficient statistics; models do. The first line of any answer is the family, not the numbers.

This is also why examiners phrase these questions so carefully. A question that tells you σ² is known is not being chatty — it is handing you half the answer. A question that leaves both parameters unknown is a different question with a different answer, and on the page the two look almost identical.

There is a practical corollary worth a sentence in any written answer. A reduction justified under one model is not justified under another. Summarise a sample by its mean because the variance was assumed known, then discover that the variance is unknown, and your summary has thrown away something you now need.

The scenario below takes one fixed set of ten numbers through three different models and gets three different answers — one number, two numbers, ten numbers. It is worth the five minutes.

**Aside — The exam tell** `scenes[7].aside.body`

Read the model statement twice before you read the question. 'σ² known' and 'both parameters unknown' are two different questions in nearly identical words, and the difference between one component and two is the whole mark.

**Quick check before moving on** `scenes[7].ask`

- *question:* A colleague hands you ten numbers and asks 'what is the sufficient statistic for this data?'. What is wrong with the question, and what do you need to ask them before you can answer?
- *hint on request:* Everything in this scene turns on one word in their question being the wrong word.

**Optional deep-dive, opened on demand — Sufficiency is a property of the model** `scenes[7].scenario`

*teaser on the closed card:* The same ten numbers, three different models, three different sufficient statistics.

> Take one concrete sample of ten numbers and hold it fixed. Nothing about the data will change in what follows; only the family of distributions assumed for it will. Watch what happens to the sufficient statistic.

> Model one: N(μ, 9), with the variance known to be 9. Expand the exponent and the Σxᵢ² term carries no parameter, so it joins h. The minimal sufficient statistic is Σxᵢ — one number. You may discard nine numbers' worth of detail.

> Model two: N(μ, σ²), both unknown. The identical exponent, but now σ² is a parameter and that same Σxᵢ² term has to stay in g. The minimal sufficient statistic becomes (Σxᵢ, Σxᵢ²) — two numbers. One extra unknown has cost you one extra dimension of summary.

> Model three: Cauchy with location μ. Now there is no exponent at all; the parameter sits inside ten separate denominators and the ratio test forces the whole sorted sample to agree. The minimal sufficient statistic is the ten order statistics. No reduction whatsoever.

> One dataset, three answers: one number, two numbers, ten numbers. So the question 'what is the sufficient statistic for this data' is malformed — data do not have sufficient statistics, MODELS do. The exam phrases questions carefully for this reason, and a question that names a family is naming the thing that determines the answer.

> The practical corollary is worth a sentence in any written answer: a reduction justified under one model is not justified under another. If you summarise a sample by its mean because the variance was assumed known, and the variance later turns out to be unknown, the summary has thrown away information you now need.

*closing line:* Data do not have sufficient statistics; models do — which is why the first step is always to write down the family, not to look at the numbers.

---

### Scene 9 of 17 — Pause and recall

`scenes[8]` · id `s7` · type `recall` (retrieval practice) · 3 minutes

**Purpose** `scenes[8].objective`

Retrieve the definition, the theorem and the standard statistics before the harder half.

**Intro** `scenes[8].intro`

Answer aloud, then look. Everything here has appeared in the scenes so far — nothing is from later.

- `scenes[8].items[0]` **Q:** State the definition of a sufficient statistic.  
  **A:** T is sufficient for θ if the conditional distribution of the sample given T = t does not depend on θ, for every t.
- `scenes[8].items[1]` **Q:** For n Bernoulli trials, what is the conditional probability of a particular sequence given that the total is t — and why does it settle sufficiency?  
  **A:** 1/C(n,t). It contains no p at all, so once the total is known the arrangement says nothing about p. For n = 5, t = 3 it is 1/10; for n = 10, t = 7 it is 1/120.
- `scenes[8].items[2]` **Q:** State the Fisher–Neyman factorisation theorem, with both conditions.  
  **A:** T is sufficient if and only if f(x | θ) = g(T(x), θ)·h(x), where h does not involve θ and g involves the data only through T(x).
- `scenes[8].items[3]` **Q:** Give the sufficient statistic for the Bernoulli, Poisson, exponential, and Uniform(0, θ) families.  
  **A:** Σxᵢ for the first three; max xᵢ for Uniform(0, θ).
- `scenes[8].items[4]` **Q:** Give it for the normal family with σ² known, and with both parameters unknown.  
  **A:** Σxᵢ (equivalently x̄) with σ² known; (Σxᵢ, Σxᵢ²), equivalently (x̄, s²), with both unknown.
- `scenes[8].items[5]` **Q:** Which transformations of a sufficient statistic are guaranteed to preserve sufficiency?  
  **A:** The one-to-one ones. A many-to-one function may or may not — Σxᵢ is a many-to-one function of the whole sample and is sufficient, while the parity of Σxᵢ is not.
- `scenes[8].items[6]` **Q:** Is a sufficient statistic an estimator of θ?  
  **A:** No. It is a summary that retains the information; it need not be a guess at θ and often cannot be one — Σxᵢ is sufficient for p but is not an estimate of a probability.
- `scenes[8].items[7]` **Q:** Why can a factor of the density that contains no θ be discarded?  
  **A:** It scales the likelihood by the same amount at every candidate θ, so it changes neither the peak nor the shape of the curve — only the vertical scale.

---

### Scene 10 of 17 — Your turn, with the scaffolding removed — five families

`scenes[9]` · id `s8` · type `completion` (fill in the blanks) · 7 minutes

**Purpose** `scenes[9].objective`

Produce the factorisation and the statistic for each family unaided.

**Problem put to the learner** `scenes[9].problem`

For each family, give the sufficient statistic. The algebra is short; what is tested is spotting where the parameter meets the data.

**Worked steps** `scenes[9].steps[]`

1. `scenes[9].steps[0]` An iid Poisson(λ) sample of size n.

   - *learner is asked:* Sufficient statistic, and the h(x) you set aside?
   - *accepted answer* `.blank.answer`: Σxᵢ, with h(x) = 1/∏xᵢ!
   - *also accepted:* sum of x, h = 1/prod(x_i!); Σx with h=1/Πxi!; Sx, h(x)=1/product of factorials; Σxᵢ and h = 1/∏xᵢ!; sum xi, h = 1/(x1!...xn!)
   - *hint:* The factorials carry no λ, so they are exactly what the theorem lets you discard.

   *why* `.why`: The easiest of the five, and the one that teaches what h(x) is for.

2. `scenes[9].steps[1]` An iid normal sample with mean μ unknown and variance σ² KNOWN.

   - *learner is asked:* Sufficient statistic?
   - *accepted answer* `.blank.answer`: Σxᵢ, equivalently x̄
   - *also accepted:* Σx or xbar; sum of xi (or the sample mean); x̄; Sx, equivalently the sample mean; sample mean
   - *hint:* Expand the exponent and see which sums survive once σ² is a constant.

   *why* `.why`: The exponent contains Σxᵢ² too, but with σ² known that term is free of μ and goes into h.

3. `scenes[9].steps[2]` An iid Uniform(0, θ) sample.

   - *learner is asked:* Sufficient statistic, and where θ meets the data?
   - *accepted answer* `.blank.answer`: max xᵢ, through the indicator I(max xᵢ ≤ θ)
   - *also accepted:* the maximum, via the support indicator; max x, in the indicator; x(n) = max, through I(max <= theta); the sample maximum; the support condition; max xi through the indicator
   - *hint:* There is no sum anywhere. Treat the support condition as part of the density.

   *why* `.why`: The family candidates get wrong, because they go looking for an exponent.

4. `scenes[9].steps[3]` An iid exponential sample with rate λ.

   - *learner is asked:* Sufficient statistic?
   - *accepted answer* `.blank.answer`: Σxᵢ
   - *also accepted:* sum of xi; Σx; Sx; the sample total; sum x_i (or equivalently the mean)
   - *hint:* f = λⁿe^(−λΣx), and h(x) = 1.

   *why* `.why`: Same statistic as the Poisson, from a different-looking density — both are exponential-family members.

5. `scenes[9].steps[4]` An iid normal sample with BOTH μ and σ² unknown.

   - *learner is asked:* Sufficient statistic?
   - *accepted answer* `.blank.answer`: (Σxᵢ, Σxᵢ²), equivalently (x̄, s²)
   - *also accepted:* (Σx, Σx²); (sum xi, sum xi^2); (xbar, s^2); (Σxᵢ, Σxᵢ²) or (x̄, s²); sum of x and sum of x squared
   - *hint:* With σ² now a parameter, the Σxᵢ² term can no longer be hidden in h.

   *why* `.why`: The pair that shows sufficiency depends on the model: the same sample, one more unknown, and a two-dimensional statistic is needed.

**What to take from it** `scenes[9].after`

Note the pattern across the five. Four exponential-family members give sums; the Uniform gives an extreme order statistic; and the normal gives one statistic or two depending on what is known. If the second and fifth blanks came out the same, re-read the exponent — that is the distinction the exam most often tests.

---

### Scene 11 of 17 — Minimal sufficiency — can you go further?

`scenes[10]` · id `s9` · type `theory` (theory) · 7 minutes

**Purpose** `scenes[10].objective`

Apply the ratio criterion, and see where sufficiency is used in the rest of the module.

**Block 1 — The question this answers** `scenes[10].blocks[0]` *(type `def`)*

Sufficiency says you may throw the rest away. It does not say you have thrown away as MUCH as possible. The whole sample is sufficient, trivially — keep everything and you have certainly kept enough. So 'sufficient' is a floor, not a target. The target is minimal sufficiency: the furthest the data can be reduced with nothing about θ lost. In the coin example you already know the answer is Σxᵢ, because step 7 of the worked scene proved it. This scene gives you the method that proof used.

**Block 2 — The Lehmann–Scheffé criterion — the only tool you need** `scenes[10].blocks[1]` *(type `formula`)*

Suppose T satisfies: f(x | θ)/f(y | θ) is free of θ  ⟺  T(x) = T(y), the ratio being taken over the x and y the family gives positive density to. Then T is minimal sufficient. (That support proviso is what makes the Uniform cases work: there the ratio is a ratio of indicators, and the comparison is between the sets of θ each sample permits rather than between two positive numbers.) In practice you form the ratio, simplify, and read off which functions of the data must agree for θ to disappear. Those functions ARE the minimal sufficient statistic — the method hands you the answer rather than requiring you to guess it first, which is why it is worth more to you than the definition.

**Block 3 — Minimal sufficiency, formally** `scenes[10].blocks[2]` *(type `def`)*

T is minimal sufficient if it is sufficient and is a function of every other sufficient statistic. Intuitively it is the furthest the data can be reduced without loss. It is not unique as a statistic — any one-to-one function of it is also minimal sufficient — but the PARTITION of the sample space it induces is unique, which is the precise sense in which there is only one minimal sufficient statistic.

**Block 4 — The criterion applied three times** `scenes[10].blocks[3]` *(type `step`)*

Bernoulli: the ratio is [p/(1−p)]^(Σx−Σy), free of p iff Σx = Σy → T = Σxᵢ. Normal with both unknown: the ratio is exp{−(Σx² − Σy²)/2σ² + μ(Σx − Σy)/σ²}, free of (μ, σ²) iff Σx = Σy AND Σx² = Σy² → T = (Σxᵢ, Σxᵢ²). Uniform(0, θ): the ratio is I(max x ≤ θ)/I(max y ≤ θ), free of θ iff max x = max y → T = max xᵢ. One method, three families, no guessing.

**Block 5 — The likelihood is the minimal sufficient statistic** `scenes[10].blocks[4]` *(type `def`)*

A deeper way to say the same thing, and one worth stating carefully. Wherever the ratio criterion above applies, the minimal sufficient statistic IS the likelihood function, taken up to a multiplicative constant: two samples are equivalent precisely when their likelihood functions are proportional, which is the ratio condition written another way — and it is why the two samples in the picture back in scene 4 gave one curve. Read it as a statement about the families in this syllabus rather than an unconditional identity; it rests on the same support and regularity conditions the criterion does. This is the content of the likelihood principle, and it is why 'what does the likelihood depend on' is always the right first question.

**Block 6 — Where this is used later in the module** `scenes[10].blocks[5]` *(type `formula`)*

Rao–Blackwell (4.3) conditions an unbiased estimator on a sufficient statistic to reduce its variance — so it needs one to exist. Lehmann–Scheffé upgrades that to a UMVUE when the sufficient statistic is also COMPLETE (4.2). The MLE (4.4), when it exists and is unique, is a function of a sufficient statistic, because the likelihood is — and when the maximiser is not unique it is the SET of maximisers that the sufficient statistic determines, so a rule for choosing among them needs its own care. And Basu's theorem concerns the independence of a complete sufficient statistic from an ancillary one. Four later topics, each resting on this one — which is why this topic is worth the time it takes.

**Block 7 — Minimal sufficient is not the same as complete** `scenes[10].blocks[6]` *(type `trap`)*

The two properties are independent and the exam exploits the confusion. Completeness says E_θ[g(T)] = 0 for all θ forces g ≡ 0 (almost surely); minimal sufficiency says no further reduction is possible. A minimal sufficient statistic need not be complete — the standard example being the Uniform(θ, θ+1) family, whose minimal sufficient statistic (min, max) admits a non-trivial function with zero expectation. A complete sufficient statistic, however, IS minimal sufficient.

**Block 8 — Three more statements to keep straight** `scenes[10].blocks[7]` *(type `trap`)*

Sufficiency says nothing about unbiasedness or variance: a sufficient statistic need not be a good estimator, and is often not an estimator of θ at all — Σxᵢ is not an estimate of p. The dimension of a minimal sufficient statistic can EXCEED the dimension of the parameter, as the transfer problem later shows. And sufficiency is relative to the whole parameter: a statistic sufficient for (μ, σ²) jointly need not be sufficient for μ with σ² unknown.

**Block 9 — The exam tell** `scenes[10].blocks[8]` *(type `step`)*

If the question says 'minimal', or 'smallest', or gives you options that are functions of one another, it is a ratio question — form f(x|θ)/f(y|θ) and do not look for the statistic first. If it merely says 'sufficient', factorisation is enough and several options may be right.

**Quick check before moving on** `scenes[10].ask`

- *question:* The whole sample is always sufficient. Why is that not a useful answer to 'find a sufficient statistic for p'?
- *hint on request:* Nothing is wrong with it as a statement. Ask what the point of looking for a sufficient statistic was in the first place.

---

### Scene 12 of 17 — Where the dependence hides in an indicator

`scenes[11]` · id `s10` · type `explore` (interactive visualisation) · 5 minutes

**Purpose** `scenes[11].objective`

See why the Uniform family's sufficient statistic is an extreme value rather than a sum.

**Body** `scenes[11].body[]`

Take a concrete sample before touching the slider: 2.1, 0.7, 3.6, 1.9, drawn from Uniform(0, θ). The largest observation is 3.6. Now ask which values of θ could have produced this sample. Could θ be 3? No — not unlikely, IMPOSSIBLE, because a Uniform(0, 3) never produces 3.6. Could θ be 4, or 10, or 100? Yes, each of them could, with decreasing plausibility as θ grows and the density 1/θ thins out. So the data rule out every θ below 3.6 outright, and the only thing doing the ruling out is the largest observation.

This is the likelihood for Uniform(0, θ), with sliders for n, the observed maximum, and a candidate θ. Look first at the shape: it is exactly zero to the left of the observed maximum and then decreases as θ^(−n) to the right. The cliff is at θ = max xᵢ — at 3.6 for the sample above.

The zero region is the whole story. A θ below the largest observation would have made that observation impossible, so the data rule it out outright — not improbable, impossible. That is the indicator I(max xᵢ ≤ θ) doing its work, and it is the only place the parameter meets the data.

Now notice which slider is absent again: there is none for the individual observations, nor for their sum. Move n from 5 to 12 with the maximum held at 4.2 and the curve gets steeper beyond the cliff, but the cliff does not move. Change the maximum and the cliff moves with it. So the likelihood depends on the data through n and max xᵢ — and n is not data, it is design. The sufficient statistic is the maximum.

This is worth dwelling on because it breaks the pattern that the other four families establish. Σxᵢ is NOT sufficient here: two samples with the same total and different maxima give different likelihoods, so the total cannot be carrying all the information. The exponential family produces sums; the Uniform is not in the exponential family — its support depends on the parameter — and it produces an extreme order statistic instead.

One more thing the picture shows, which belongs to 4.4 but is visible here. The maximum of this curve sits exactly at the cliff edge, where the derivative does not exist. So the MLE of θ is max xᵢ, and it cannot be found by setting a derivative to zero. Families whose support depends on the parameter are where differentiation fails.

**Interactive element** `scenes[11].viz` — live plot of type `unif-likelihood`, initial state n=5, xmax=4.2. Not reproducible in text; the surrounding body is written to stand alone, and whether it succeeds in doing so is worth your comment.

**Quick check before moving on** `scenes[11].ask`

- *question:* Σxᵢ is sufficient for the exponential and the Poisson but not for Uniform(0, θ). What is different about the Uniform that breaks it?
- *hint on request:* Ask where θ appears in each density, and in particular whether the SET of possible x values depends on it.

---

### Scene 13 of 17 — Now without the steps — the normal with both parameters unknown

`scenes[12]` · id `s11` · type `guided` (guided problem) · 8 minutes

**Purpose** `scenes[12].objective`

Derive a two-dimensional minimal sufficient statistic by the ratio criterion.

**Problem put to the learner** `scenes[12].problem`

X₁,…,Xₙ are iid N(μ, σ²) with BOTH parameters unknown. Find a minimal sufficient statistic for (μ, σ²), justifying minimality, and say why the answer differs from the σ²-known case.

**Hint ladder, revealed one at a time** `scenes[12].hints[]`

1. Write the joint density and expand the exponent into separate sums; do not stop at Σ(xᵢ − μ)².
2. Form the ratio f(x | μ, σ²)/f(y | μ, σ²) and ask what must hold for BOTH parameters to disappear.
3. Two parameters give two conditions, and the conditions name the statistic — you do not have to guess it.

**Model solution, hidden until requested** `scenes[12].solution[]`

1. `scenes[12].solution[0]` Write the joint density and expand the exponent.

   ```
   f(x | μ,σ²) = (2πσ²)^(−n/2) exp{−[Σxᵢ² − 2μΣxᵢ + nμ²]/(2σ²)}
   ```

   Laid out:

   $$f(x | μ,σ²) = (2πσ²)^{−\frac{n}{2}} exp{−\frac{[Σxᵢ² − 2μΣxᵢ + nμ²]}{(2σ²)}}$$

2. `scenes[12].solution[1]` Factorise. With σ² now a parameter, the Σxᵢ² term cannot go into h.

   ```
   = (2πσ²)^(−n/2) exp{−nμ²/(2σ²)} · exp{(μΣxᵢ)/σ² − Σxᵢ²/(2σ²)} · 1
   ```

   Laid out:

   $$= (2πσ²)^{−\frac{n}{2}} exp{−\frac{nμ²}{(2σ²)}} · exp{\frac{(μΣxᵢ)}{σ²} − \frac{Σxᵢ²}{(2σ²)}} · 1$$

   *why* `.why`: So g depends on the data through the PAIR (Σxᵢ, Σxᵢ²) and h(x) = 1. The pair is sufficient by factorisation. Minimality still has to be shown.

3. `scenes[12].solution[2]` Form the ratio at two samples of the same size.

   ```
   f(x)/f(y) = exp{ μ(Σx − Σy)/σ² − (Σx² − Σy²)/(2σ²) }
   ```

   Laid out:

   $$\frac{f(x)}{f(y)} = exp{ \frac{μ(Σx − Σy)}{σ²} − \frac{(Σx² − Σy²)}{(2σ²)} }$$

4. `scenes[12].solution[3]` Require it to be free of both parameters. Treat μ first, with σ² fixed.

   ```
   the coefficient of μ is (Σx − Σy)/σ², which must vanish  ⟹  Σx = Σy
   ```

   Laid out:

   $$the coefficient of μ is \frac{(Σx − Σy)}{σ²}, which must vanish  ⟹  Σx = Σy$$

5. `scenes[12].solution[4]` With that imposed, the remaining exponent must also be free of σ².

   ```
   −(Σx² − Σy²)/(2σ²) free of σ²  ⟹  Σx² = Σy²
   ```

   Laid out:

   $$−\frac{(Σx² − Σy²)}{(2σ²)} free of σ²  ⟹  Σx² = Σy²$$

   *why* `.why`: Two parameters, two conditions. Both must hold, and together they say exactly that the pair agrees.

6. `scenes[12].solution[5]` Read off the conclusion.

   ```
   f(x)/f(y) free of (μ,σ²)  ⟺  (Σx, Σx²) = (Σy, Σy²)  ⟹  T = (Σxᵢ, Σxᵢ²) is minimal sufficient
   ```

   Laid out:

   $$\frac{f(x)}{f(y)} free of (μ,σ²)  ⟺  (Σx, Σx²) = (Σy, Σy²)  ⟹  T = (Σxᵢ, Σxᵢ²) is minimal sufficient$$

7. `scenes[12].solution[6]` State the equivalent form and answer the 'why different' part.

   ```
   (x̄, s²) is a one-to-one function of (Σxᵢ, Σxᵢ²) for n ≥ 2, so it is minimal sufficient too
   ```

   *why* `.why`: With σ² known, exp{−Σxᵢ²/(2σ²)} contains no parameter and is a legitimate h, so Σxᵢ alone suffices. Making σ² unknown moves that factor from h into g, and the statistic gains a second component. The sample did not change; the model did.

**Final answer given to the learner** `scenes[12].answer`

T = (Σxᵢ, Σxᵢ²), equivalently (x̄, s²), is minimal sufficient for (μ, σ²). The ratio of densities is free of both parameters exactly when both components agree. It differs from the σ²-known case because the Σxᵢ² term is free of the parameter only when σ² is a known constant, and so can be absorbed into h only then.

**Self-check offered** `scenes[12].check`

Two checks. The number of conditions produced by the ratio should match the number of unknown parameters — two here, and one in the σ²-known case. And (x̄, s²) must be a one-to-one function of your answer; if it is not, the two are not equivalent and one of them is wrong.

---

### Scene 14 of 17 — Six statements — verdict on each before you look

`scenes[13]` · id `s12` · type `trapcheck` (true/false check) · 5 minutes

**Purpose** `scenes[13].objective`

Meet the exact confusions this topic generates.

**Intro** `scenes[13].intro`

Each is either a standard result or a plausible corruption of one.

- `scenes[13].items[0]` **Claim:** T is sufficient for θ if and only if the joint density can be written as g(T(x), θ)·h(x) with h free of θ.  
  **Verdict: TRUE.** The Fisher–Neyman factorisation theorem, and it is an equivalence in both directions. Both conditions matter: h must be free of θ, and g must involve the data only through T.
- `scenes[13].items[1]` **Claim:** For an iid Uniform(0, θ) sample, Σxᵢ is sufficient for θ.  
  **Verdict: FALSE.** The maximum is sufficient, not the sum. θ meets the data only through the indicator I(max xᵢ ≤ θ), and two samples with the same total but different maxima give different likelihoods. The Uniform is not an exponential-family member, which is why no sum appears.
- `scenes[13].items[2]` **Claim:** A minimal sufficient statistic is unique.  
  **Verdict: FALSE.** Any one-to-one function of one is also minimal sufficient — Σxᵢ and x̄ both are. What is unique is the PARTITION of the sample space it induces, and that is the precise form of the statement.
- `scenes[13].items[3]` **Claim:** Every function of a sufficient statistic is sufficient.  
  **Verdict: FALSE.** A one-to-one function is GUARANTEED to stay sufficient; a many-to-one function may or may not, so the claim as stated is false. Be careful not to overcorrect into 'only one-to-one functions are sufficient', which is also false — the whole sample X is sufficient, and Σxᵢ is a many-to-one function of it that is sufficient too. What a many-to-one function risks is collapsing values of T that the likelihood distinguishes: a statistic recording only whether Σxᵢ is even would plainly not do for the Bernoulli.
- `scenes[13].items[4]` **Claim:** For an iid N(μ, σ²) sample with both parameters unknown, (x̄, s²) is minimal sufficient.  
  **Verdict: TRUE.** For n ≥ 2 it is a one-to-one function of (Σxᵢ, Σxᵢ²) — s² divides by n − 1, so a single observation has no s² — and the ratio criterion identifies that pair as minimal sufficient. With σ² KNOWN the answer collapses to x̄ alone, and keeping the two cases apart is the examinable point.
- `scenes[13].items[5]` **Claim:** A minimal sufficient statistic is always complete.  
  **Verdict: FALSE.** The implication runs the other way: a complete sufficient statistic is minimal sufficient, but not conversely. The standard counterexample is the Uniform(θ, θ+1) family, whose minimal sufficient statistic (min, max) is not complete.

---

### Scene 15 of 17 — JRF extension — the two families where reduction behaves oddly

`scenes[14]` · id `s13` · type `guided` (guided problem) · 9 minutes · **optional JRF extension, core path completes without it**

**Purpose** `scenes[14].objective`

Handle a family whose minimal sufficient statistic has higher dimension than the parameter, and one that admits no reduction at all.

**Problem put to the learner** `scenes[14].problem`

X₁,…,Xₙ are iid Uniform(θ, θ+1), where θ ∈ ℝ is the single unknown parameter. Find a minimal sufficient statistic, state its dimension, and comment on what that dimension tells you.

**Hint ladder, revealed one at a time** `scenes[14].hints[]`

1. Write the density including its support condition, and convert the condition on every observation into a condition on two of them.
2. The density takes only the values 0 and 1, so the ratio test becomes a question about when two indicator functions of θ agree.
3. Count the parameters, then count the components of your statistic, and do not assume they must match.

**Model solution, hidden until requested** `scenes[14].solution[]`

1. `scenes[14].solution[0]` Write the joint density with its support condition explicit.

   ```
   f(x | θ) = ∏ I(θ ≤ xᵢ ≤ θ+1) = I(θ ≤ min xᵢ) · I(max xᵢ ≤ θ+1)
   ```

   *why* `.why`: Each observation must lie in the interval, so the binding constraints come from the smallest and largest values only. The density is 1 where the condition holds and 0 elsewhere.

2. `scenes[14].solution[1]` Rearrange into a statement about θ.

   ```
   f(x | θ) = I(max xᵢ − 1 ≤ θ ≤ min xᵢ)
   ```

   *why* `.why`: The data do not make θ more or less likely within that interval — the likelihood is flat on it and zero outside. All the data do is pin down an interval of possible θ.

3. `scenes[14].solution[2]` Apply the ratio criterion. The ratio is free of θ only if the two indicator functions coincide.

   ```
   I(max x − 1 ≤ θ ≤ min x) / I(max y − 1 ≤ θ ≤ min y) free of θ  ⟺  the two intervals are identical
   ```

4. `scenes[14].solution[3]` Two intervals are identical when their endpoints agree.

   ```
   ⟺  min x = min y  AND  max x = max y
   ```

5. `scenes[14].solution[4]` Read off the statistic and its dimension.

   ```
   T = (min xᵢ, max xᵢ) = (x₍₁₎, x₍ₙ₎),   dimension 2,   while dim(θ) = 1
   ```

6. `scenes[14].solution[5]` Comment on what that means.

   ```
   dim(minimal sufficient) > dim(parameter) is permitted and does happen
   ```

   *why* `.why`: There is no theorem forcing the two to match. It is true for full-rank exponential families, which is why the pattern holds for every family in the completion scene — but the Uniform(θ, θ+1) family has a parameter-dependent support, is not an exponential family, and needs two numbers to summarise one parameter.

7. `scenes[14].solution[6]` Add the fact this family is usually quoted for.

   ```
   (min, max) is minimal sufficient but NOT complete
   ```

   *why* `.why`: The reason needs one more step than it is usually given. The range max − min is ancillary: shifting θ shifts both extremes equally, so the range has the same distribution, and therefore the same expectation c, for every θ. Now CENTRE it. Put g(T) = (max − min) − c. Then E_θ[g(T)] = 0 for every θ while g is not identically zero — which is exactly what completeness forbids. An expectation that happens to be free of θ is not by itself a failure of completeness; the centred function is what demonstrates it. This is the standard counterexample to 'minimal sufficient implies complete', and it is the same family that supplies the dimension mismatch.

**Final answer given to the learner** `scenes[14].answer`

T = (min xᵢ, max xᵢ), of dimension 2, for a one-dimensional parameter. The likelihood is I(max xᵢ − 1 ≤ θ ≤ min xᵢ), so the data determine only an interval for θ, and the two endpoints of that interval are what must be retained. The dimension of a minimal sufficient statistic is not bounded by the dimension of the parameter — and this family is also the standard example of a minimal sufficient statistic that is not complete.

**Self-check offered** `scenes[14].check`

The structural check: your statistic must determine the interval of θ values the data permit. If you answered min alone, or max alone, test it — one endpoint leaves the other free, so a sample with the same minimum and a different maximum would give a different likelihood, and the statistic cannot be sufficient.

**Optional deep-dive, opened on demand — The Cauchy that refuses to be reduced** `scenes[14].scenario`

*teaser on the closed card:* One standard family in which no reduction is possible at all — the whole sorted sample is minimal.

> Every example in this lesson so far reduces n numbers to one or two. That success is so uniform that it is easy to conclude reduction always happens. It does not, and the standard counterexample is worth carrying because it shows what the factorisation theorem is really detecting. You are meeting it now rather than earlier because it only makes sense once you have seen the clean cases work.

> Take the Cauchy location family: f(x | θ) = 1/(π[1 + (x − θ)²]). The joint density for an iid sample is the product ∏ 1/(π[1 + (xᵢ − θ)²]). Now try to factorise it as g(T(x), θ)·h(x). The θ appears inside n separate quadratic terms that cannot be combined — there is no expansion that collects the data into a single sum the way the normal exponent does, because the terms are in denominators rather than exponents.

> Apply the ratio test instead. For two samples x and y, the ratio of joint densities is ∏[1 + (yᵢ − θ)²] / ∏[1 + (xᵢ − θ)²]. This is a ratio of two polynomials in θ of degree 2n. It is free of θ only if the two polynomials are identical, which happens only if the two samples give the same roots WITH THE SAME MULTIPLICITIES — that is, only if the two samples are the same multiset, which is to say permutations of each other. So T(x) = T(y) exactly when the sorted samples agree, and the minimal sufficient statistic is the full set of order statistics.

> Read what that costs. For a Cauchy sample of 100 observations, the minimal sufficient statistic is 100 numbers. No data reduction is available; you cannot summarise, and in particular there is no sense in which the sample mean or median carries the information. This is also why the Cauchy mean does not behave: the sample mean of a Cauchy sample has the same Cauchy distribution as a single observation, so averaging buys nothing.

> For the exam, the facts are small and specific. The Cauchy location family has the order statistics as its minimal sufficient statistic. The dimension of a minimal sufficient statistic is not bounded by the dimension of the parameter. And a family outside the exponential family need not admit any reduction at all.

*closing line:* Reduction is a gift of the model, not a right: the factorisation theorem tells you when the gift is on offer, and sometimes the answer is never.

---

### Scene 16 of 17 — What you should now be able to do unaided

`scenes[15]` · id `s14` · type `summary` (summary) · 4 minutes

**Purpose** `scenes[15].objective`

Compress the topic to two theorems, six families and the traps the exam is built on.

**Body** `scenes[15].body[]`

Where it started. For n coin tosses, the probability of any particular sequence with t heads is p^t(1−p)^(n−t), which mentions t and nothing else. Given the total, each arrangement has probability 1/C(n,t) — no p in it. So the total is sufficient and the arrangement is noise. Everything else in the topic generalises that one calculation.

The definitions. T is sufficient for θ if the conditional distribution of the sample given T does not depend on θ. T is minimal sufficient if, in addition, it is a function of every other sufficient statistic — the furthest reduction available.

The two tools. Fisher–Neyman factorisation: T is sufficient ⟺ f(x | θ) = g(T(x), θ)·h(x) with h free of θ and g touching the data only through T. Lehmann–Scheffé for minimality: T is minimal sufficient if f(x | θ)/f(y | θ) is free of θ exactly when T(x) = T(y). The second method hands you the statistic rather than asking you to guess it: form the ratio, and whatever must agree for θ to vanish IS the statistic.

The six families. Bernoulli, Poisson and exponential all give Σxᵢ. Normal with σ² known gives Σxᵢ, equivalently x̄. Normal with both unknown gives (Σxᵢ, Σxᵢ²), equivalently (x̄, s²). Uniform(0, θ) gives max xᵢ, through the support indicator rather than an exponent. Uniform(θ, θ+1) gives (min xᵢ, max xᵢ) — two numbers for one parameter. Cauchy with a location parameter gives the full set of order statistics: no reduction at all.

The explanation behind the pattern. For an exponential family f = h(x)c(θ)exp{Σⱼwⱼ(θ)tⱼ(x)}, the vector of sums (Σt₁(xᵢ), …, Σt_k(xᵢ)) is sufficient — which is why sums keep appearing. The Uniform and Cauchy families are not exponential families, and they are precisely the two that behave differently.

What is and is not unique. Sufficient statistics are not unique: the whole sample and the order statistics are always sufficient, and any one-to-one function of a sufficient statistic is sufficient. Minimal sufficient statistics are not unique either, but the partition they induce is. A MANY-to-one function of a sufficient statistic need not be sufficient.

Recognising the question. 'Find a sufficient statistic' means factorise, and several options may be right. 'Find the minimal sufficient statistic', or 'the smallest', means form the ratio. 'Prove from the definition' means compute the conditional distribution and show θ cancelling. If the stem says σ² is known, expect one component; if it says both are unknown, expect two. If the family is not an exponential family, do not expect a sum.

What sufficiency is not. It is not estimation — a sufficient statistic need not be, and often cannot be, a guess at θ. It says nothing about unbiasedness or variance. And it is not a property of the numbers: the same ten observations give a one-, two- or ten-dimensional minimal sufficient statistic depending on which family you assume.

The relations to the rest of the module. Rao–Blackwell conditions on a sufficient statistic; Lehmann–Scheffé upgrades the result to a UMVUE when that statistic is complete; an MLE that exists and is unique is a function of a sufficient statistic because the likelihood is, and otherwise the sufficient statistic determines the set of maximisers; and Basu's theorem concerns a complete sufficient statistic and an ancillary one. A complete sufficient statistic is minimal sufficient, but minimal sufficiency does NOT imply completeness — Uniform(θ, θ+1) is the counterexample.

The habit. Write the family first, then the joint density including its support, then look for where the parameter touches the data.

**Reference table** `scenes[15].table`

| Family | Minimal sufficient statistic | Note |
|---|---|---|
| Bernoulli(p) | Σxᵢ | exponential family |
| Poisson(λ) | Σxᵢ | exponential family; h = 1/∏xᵢ! |
| Exponential, rate λ | Σxᵢ | exponential family |
| Normal, σ² known | Σxᵢ, equivalently x̄ | one unknown, one component |
| Normal, both unknown | (Σxᵢ, Σxᵢ²), equivalently (x̄, s²) | two unknowns, two components |
| Uniform(0, θ) | max xᵢ | support depends on θ; no sum |
| Uniform(θ, θ+1)  ✦ | (min xᵢ, max xᵢ) | dimension 2 for one parameter; not complete |
| Cauchy, location θ  ✦ | the full set of order statistics | no reduction at all |

*caption* `.caption`: The last two rows, marked ✦, come from the optional JRF-extension scene. The first six are the ones a pass requires.

---

### Scene 17 of 17 — Mastery test

`scenes[16]` · id `s15` · type `quiz` (mastery test) · 12 minutes

**Purpose** `scenes[16].objective`

Ten unseen questions, drawn 3 easy / 5 moderate / 2 hard.

Draws from the pool reproduced below. `scenes[16].setId` = `inference_t1_mastery`

---

## Revision material `revision`

**Revision sheet** `revision.sheet[]` (29 lines)

1. `[0]` Where it starts: any n-toss sequence with t heads has probability p^t(1−p)^(n−t) — t appears, the order does not.
2. `[1]` Given the total t, each arrangement has probability 1/C(n,t): no p in it, so the order is noise. 1/10 for n=5,t=3.
3. `[2]` T sufficient: the conditional distribution of X given T = t does not depend on θ.
4. `[3]` Fisher–Neyman: T sufficient ⟺ f(x|θ) = g(T(x),θ)·h(x), h free of θ, g touching data only via T.
5. `[4]` A factor with no θ scales the likelihood equally at every θ, so it changes neither peak nor shape — hence ∝.
6. `[5]` A statistic is any function of the data. It is NOT an estimator: Σxᵢ is sufficient for p but is no guess at p.
7. `[6]` Index law that makes the Bernoulli factorise: (1−p)^(n−Σx) = (1−p)ⁿ/(1−p)^Σx.
8. `[7]` Bernoulli: f = [p/(1−p)]^Σx (1−p)ⁿ · 1  →  T = Σxᵢ.
9. `[8]` Poisson: f = e^(−nλ)λ^Σx · 1/∏xᵢ!  →  T = Σxᵢ, with h = 1/∏xᵢ!.
10. `[9]` Exponential rate λ: f = λⁿe^(−λΣx) · 1  →  T = Σxᵢ.
11. `[10]` Normal, σ² KNOWN: T = Σxᵢ, equivalently x̄.
12. `[11]` Normal, BOTH unknown: T = (Σxᵢ, Σxᵢ²), equivalently (x̄, s²).
13. `[12]` Uniform(0,θ): f = θ^(−n) I(max ≤ θ)  →  T = max xᵢ. No sum anywhere.
14. `[13]` Uniform(θ,θ+1): likelihood I(max−1 ≤ θ ≤ min)  →  T = (min, max). Dimension 2 for a 1-dim parameter.
15. `[14]` Cauchy location: minimal sufficient statistic is the full set of order statistics — no reduction.
16. `[15]` Exponential family f = h(x)c(θ)exp{Σwⱼ(θ)tⱼ(x)}  →  (Σt₁, …, Σt_k) sufficient. Explains why sums recur.
17. `[16]` Minimal sufficient: sufficient, and a function of every other sufficient statistic.
18. `[17]` Lehmann–Scheffé criterion: f(x|θ)/f(y|θ) free of θ  ⟺  T(x) = T(y).
19. `[18]` Bernoulli ratio [p/(1−p)]^(Σx−Σy) free of p ⟺ Σx = Σy.
20. `[19]` Normal two-parameter ratio free of (μ,σ²) ⟺ Σx = Σy AND Σx² = Σy².
21. `[20]` The order statistics are always sufficient for an iid sample; the whole sample trivially is.
22. `[21]` One-to-one functions of a sufficient statistic are sufficient; many-to-one functions need not be.
23. `[22]` A minimal sufficient statistic is not unique, but the partition it induces is.
24. `[23]` The minimal sufficient statistic is the likelihood up to a constant — the likelihood principle.
25. `[24]` Complete + sufficient ⟹ minimal sufficient. Minimal sufficient does NOT ⟹ complete.
26. `[25]` Uniform(θ,θ+1): (min,max) is minimal sufficient but not complete — the range has θ-free expectation.
27. `[26]` dim(minimal sufficient) can EXCEED dim(θ); equality holds for full-rank exponential families.
28. `[27]` Three phrasings: 'sufficient' → factorise; 'minimal'/'smallest' → ratio; 'from the definition' → conditional law.
29. `[28]` Used later: Rao–Blackwell (4.3) conditions on it; Lehmann–Scheffé needs completeness too (4.2); a unique MLE is a function of it (4.4); Basu's theorem pairs it with an ancillary statistic.

**Flashcards** `revision.cards[]`

| Front | Back |
|---|---|
| Definition of sufficiency | The conditional law of the sample given T has no θ in it |
| The coin result, in one line | Given t heads, each arrangement has probability 1/C(n,t) — no p |
| Fisher–Neyman factorisation | f = g(T(x), θ)·h(x), with h free of θ |
| Why θ-free factors drop out | They scale the likelihood equally at every θ — peak and shape unchanged |
| Statistic vs estimator | A statistic is any function of the data; it need not estimate anything |
| Bernoulli, Poisson, exponential | Σxᵢ in all three |
| Normal with σ² known, and with both unknown | Σxᵢ (or x̄); then (Σxᵢ, Σxᵢ²) (or (x̄, s²)) |
| Uniform(0, θ) | max xᵢ, via the indicator I(max ≤ θ) |
| Uniform(θ, θ+1) | (min, max) — dimension 2 for one parameter, and not complete |
| Cauchy location family | The order statistics: no reduction is possible |
| Criterion for minimal sufficiency | f(x|θ)/f(y|θ) free of θ ⟺ T(x) = T(y) |
| Which functions preserve sufficiency? | One-to-one ones; many-to-one need not |
| Complete and minimal sufficient | Complete sufficient ⟹ minimal sufficient, not conversely |
| Why sums keep appearing | Those families are exponential families; Uniform and Cauchy are not |
| The three phrasings | 'sufficient' factorise · 'minimal' ratio · 'from the definition' conditional law |

**Memory aids** `revision.tricks[]`

- `[0]` **Where does θ touch the data?** — That one question answers every factorisation. In an exponent it gives a sum; in a support indicator it gives an extreme order statistic; in n separate denominators it gives nothing.
- `[1]` **The coin is the whole topic** — p^t(1−p)^(n−t) mentions how many, never which. Everything else generalises that sentence. When a family confuses you, go back to ten tosses and seven heads.
- `[2]` **The ratio hands you the answer** — You do not guess a statistic and then verify it. Form f(x)/f(y), see what must agree for θ to vanish, and that is the minimal sufficient statistic.
- `[3]` **One unknown, one sum; two unknowns, two sums** — Normal with σ² known needs Σxᵢ; with σ² unknown it needs Σxᵢ² as well. The count of conditions from the ratio matches the count of parameters.
- `[4]` **No sum in the Uniform** — Candidates hunt for Σxᵢ out of habit. The support condition is where θ lives, so the answer is an extreme value.
- `[5]` **Complete implies minimal, not the reverse** — One-directional. Uniform(θ, θ+1) is the counterexample to the reverse, and it is the same family that gives dim(T) > dim(θ).
- `[6]` **Models have sufficient statistics; data do not** — The same ten numbers give a one-, two- or ten-dimensional answer under three different families.

**Elimination shortcuts for multiple-choice items** `revision.shortcuts[]`

- `[0]` Write the support as part of the density, always — it is where the Uniform's answer lives.
- `[1]` Any option offering Σxᵢ for Uniform(0, θ) is wrong; any offering the maximum for the exponential is wrong.
- `[2]` Any option calling a minimal sufficient statistic unique, or claiming it must be complete, is wrong.
- `[3]` Any option saying EVERY function of a sufficient statistic is sufficient is wrong; so is any option saying only the one-to-one ones are. One-to-one is what guarantees it.
- `[4]` If a question says σ² is known, expect one component; if unknown, expect two.
- `[5]` If the family is not an exponential family, do not expect a sum.
- `[6]` If an option is an estimate of θ when the question asked for a sufficient statistic, suspect it.

**If nothing else is remembered** `revision.remember[]`

- `[0]` Any sequence with t heads has probability p^t(1−p)^(n−t); given t, each arrangement has probability 1/C(n,t), with no p in it. That is sufficiency, and the rest is generalisation.
- `[1]` Form the ratio f(x|θ)/f(y|θ) and read the minimal sufficient statistic off the conditions for θ to cancel.
- `[2]` State the family before the statistic: sufficiency is relative to a model, not a property of the numbers.

**Errors to avoid** `revision.traps[]`

- `[0]` Giving Σxᵢ as sufficient for Uniform(0, θ) instead of the maximum.
- `[1]` Ignoring the support condition and so missing where the parameter meets the data.
- `[2]` Using Σxᵢ for the normal when σ² is also unknown, where (Σxᵢ, Σxᵢ²) is needed.
- `[3]` Claiming a minimal sufficient statistic is unique rather than its induced partition.
- `[4]` Asserting that every function of a sufficient statistic is sufficient.
- `[5]` Taking minimal sufficiency to imply completeness — the implication runs the other way.
- `[6]` Assuming dim(minimal sufficient) must equal dim(θ); Uniform(θ, θ+1) gives 2 for 1.
- `[7]` Treating a sufficient statistic as an estimator of θ — Σxᵢ is not an estimate of p.
- `[8]` Answering 'minimal' with a factorisation, or 'sufficient' with a ratio — the phrasings ask for different work.
- `[9]` Forgetting that the Cauchy location family admits no reduction below the order statistics.

---

## Mastery pool — all 20 items with answer keys `qsets/mastery`

Ten are drawn per attempt at 3 easy / 5 moderate / 2 hard. Keys are distributed five to each option letter. Please check each item for a second defensible answer as well as for the correctness of its stated key and explanation.

### Q1 — `inf-t1-m-01` *(single, moderate)*

X₁,…,Xₙ are iid Gamma with known shape α and unknown rate β, so f(x;β) = β^α x^(α−1) e^(−βx) / Γ(α) for x > 0. The minimal sufficient statistic for β is:

*Options* `.options[]`:

- **A.** Σxᵢ  ← key
- **B.** ∏xᵢ
- **C.** x₍ₙ₎
- **D.** (Σxᵢ, ∏xᵢ)

*Explanation* `.explanation`: The joint density is β^(nα)/Γ(α)ⁿ · (∏xᵢ)^(α−1) · e^(−βΣxᵢ). The only factor containing β beyond the constant β^(nα) is e^(−βΣxᵢ), so g depends on the data through Σxᵢ alone, and Σxᵢ is minimal sufficient. The product (∏xᵢ)^(α−1) contains no β — α is known — so it belongs in h, which rules out B and the pair in D. Read D carefully, because it is the instructive distractor: (Σxᵢ, ∏xᵢ) IS sufficient, since anything that determines a sufficient statistic is itself sufficient. It is simply not minimal — Σxᵢ is a function of it and not conversely. That is why this stem asks for the MINIMAL statistic: had it asked only for 'a sufficient statistic', both A and D would have been correct answers.

### Q2 — `inf-t1-m-02` *(numeric, moderate)*

A sample of 12 independent Bernoulli(p) trials is recorded as an ordered sequence, and 5 of them are successes. Using T = ΣXᵢ as the statistic, give its value and the number of distinct ordered sequences sharing that value.

*Options* `.options[]`:

- **A.** 5, and 12 sequences share it
- **B.** 5, and 792 sequences share it  ← key
- **C.** 0.4167, and 792 sequences share it
- **D.** 5, and 4096 sequences share it

*Explanation* `.explanation`: T = Σxᵢ = 5. The sequences sharing T = 5 are the arrangements of five successes among twelve trials: C(12,5) = 792. Those 792 are conditionally equally likely given T = 5, with p cancelling out — which makes sufficiency made concrete. Option C reports the sample mean x̄ = 5/12, a one-to-one transformation of T for fixed n = 12 and therefore minimal sufficient in its own right, which is exactly why the stem names T rather than asking for 'the minimal sufficient statistic' — under that looser wording both B and C would be correct. Option D is 2¹², the number of all possible sequences.

*Arithmetic check* `.check`: Two quantities were asked. C(12,5) = 792, not 12 and not 2¹².

### Q3 — `inf-t1-m-03` *(multi, hard)*

X₁,…,Xₙ are iid U(θ, θ+1) with θ ∈ ℝ unknown. Consider the following statements.

*Statements to judge* `.statements[]`:

- **A.** The minimal sufficient statistic is the pair (X₍₁₎, X₍ₙ₎).
- **B.** The minimal sufficient statistic has higher dimension than the parameter.
- **C.** The family is a one-parameter exponential family.
- **D.** The sample range X₍ₙ₎ − X₍₁₎ carries no information about θ on its own.

*Options* `.options[]`:

- **A.** A, B and C only
- **B.** A and C only
- **C.** A, B and D only  ← key
- **D.** B and D only

*Explanation* `.explanation`: A is true: the joint density is 1 on the region where every xᵢ lies in (θ, θ+1), which is the pair of conditions x₍₁₎ > θ and x₍ₙ₎ < θ+1, so both extremes are needed. B is true for the same reason — one parameter, a two-dimensional minimal sufficient statistic. C is false: the support moves with θ, so this is not an exponential family at all. D is true, and is why the range is the natural thing to look at here.

*Verdict on each statement* `.verdicts`:

- **A — true.** The indicator splits into 1{x₍₁₎ > θ} and 1{x₍ₙ₎ < θ+1}; both extremes meet θ.
- **B — true.** Dimension 2 for a one-dimensional θ. Note WHY: the support moves with θ, so this is not an exponential family at all. A curved exponential family also has dim(T) > dim(θ), but for a different reason, and this family is not one — do not let the two explanations merge.
- **C — false.** The support depends on θ, which disqualifies the family from exponential form entirely.
- **D — true.** The range is ancillary: its distribution is free of θ, since shifting θ shifts both extremes equally.

### Q4 — `inf-t1-m-04` *(numeric, moderate)*

A sample of n = 10 from N(μ, σ²) with BOTH parameters unknown gives Σxᵢ = 50 and Σxᵢ² = 270. Taking T = (ΣXᵢ, ΣXᵢ²), give its value and its dimension.

*Options* `.options[]`:

- **A.** 50, dimension 1
- **B.** (5, 2), dimension 2
- **C.** (5, 27), dimension 2
- **D.** (50, 270), dimension 2  ← key

*Explanation* `.explanation`: With both parameters unknown the exponent needs t₁(x) = x and t₂(x) = x², so T = (Σxᵢ, Σxᵢ²) = (50, 270), dimension 2 — matching the two-dimensional parameter (μ, σ²), so the family is full rank and T is also complete. Option C reports the per-observation averages, which are a valid one-to-one transform but not the values asked for.

*Arithmetic check* `.check`: The question asked for the value AND the dimension. Dimension 2 here equals the dimension of the parameter — that is what makes this family full rank, unlike the curved case.

### Q5 — `inf-t1-m-05` *(single, easy)*

Which statement about the factorisation theorem is correct?

*Options* `.options[]`:

- **A.** h(x) may depend on the data in any way but must not contain θ  ← key
- **B.** The theorem applies only when the support is independent of θ
- **C.** h(x) may contain θ provided g does not
- **D.** g must depend on the data through every observation individually

*Explanation* `.explanation`: That is exactly the condition: g carries θ and touches the data only through T, while h is free in the data and must contain no θ. B is false, and is the common misreading: the factorisation theorem applies perfectly well when the support depends on θ, provided the indicator is kept inside g — the Uniform families are the standard case. It is the exponential-FAMILY criterion, not the factorisation theorem, that needs a fixed support. C has the roles of g and h swapped: h is the factor that must be free of θ. D is false because g is required to touch the data only through T, which is the opposite of involving each observation separately.

### Q6 — `inf-t1-m-06` *(numeric, easy)*

A sample of size 4 from U(0, θ) gives the observations 2.1, 0.7, 3.6 and 1.9. Give the value of the minimal sufficient statistic, and the smallest value of θ that the data do not rule out.

*Options* `.options[]`:

- **A.** 8.3, and θ must be at least 8.3
- **B.** 3.6, and θ must be at least 3.6  ← key
- **C.** 3.6, and θ must be at least 8.3
- **D.** 2.075, and θ must be at least 3.6

*Explanation* `.explanation`: T = x₍ₙ₎ = 3.6. The likelihood is θ^(−4) for θ ≥ 3.6 and exactly zero below, because any smaller θ would have made the observation 3.6 impossible. So the data rule out everything under 3.6, and 3.6 itself is the smallest admissible value — and also the MLE. Option A gives Σxᵢ, which is irrelevant for this family.

*Arithmetic check* `.check`: Both parts turn on the maximum. If you computed the sum anywhere in your working, you answered a question about a different family.

### Q7 — `inf-t1-m-07` *(numeric, easy)*

X₁,…,Xₙ are iid with f(x;θ) = (1/θ)e^(−x/θ) for x > 0. A sample of n = 6 gives Σxᵢ = 42 and ∏xᵢ = 10080. Identify which of these the likelihood actually depends on, and give its value.

*Options* `.options[]`:

- **A.** 10080
- **B.** 7
- **C.** 42  ← key
- **D.** (42, 10080)

*Explanation* `.explanation`: Writing the joint density gives θ^(−6) exp(−Σxᵢ/θ), so θ meets the data only through Σxᵢ = 42. The product is a distractor carried over from densities such as θx^(θ−1) where it does matter. Option B is x̄, a correct one-to-one transform but not the value of Σxᵢ that was asked for; option D adds a statistic the likelihood never uses.

*Arithmetic check* `.check`: The question asked for the value of the minimal sufficient statistic, not the estimate of θ. Reporting 7 is right working and the wrong quantity.

### Q8 — `inf-t1-m-08` *(multi, hard)*

Let T be a minimal sufficient statistic for θ in some family.

*Statements to judge* `.statements[]`:

- **A.** T is a function of every other sufficient statistic for θ.
- **B.** T is necessarily complete.
- **C.** T is necessarily ancillary.
- **D.** Any unique MLE of θ must be a function of T.

*Options* `.options[]`:

- **A.** A, B and D only
- **B.** A and B only
- **C.** B and C only
- **D.** A and D only  ← key

*Explanation* `.explanation`: A is true — minimal means it is a function of every sufficient statistic, which is the definition. B is false: minimal sufficiency and completeness are different properties, and curved families such as N(θ,θ²) are minimal sufficient without being complete. C is false — an ancillary statistic has a distribution free of θ, which is the opposite situation. D is true, since maximising g(T;θ) over θ can only produce a function of T.

*Verdict on each statement* `.verdicts`:

- **A — true.** That is the definition of minimality — the coarsest sufficient summary.
- **B — false.** Full-rank exponential families give both; curved families give minimality without completeness.
- **C — false.** Ancillary means the distribution does not involve θ — close to the reverse of sufficient.
- **D — true.** The likelihood is g(T;θ)h(x) and only g involves θ, so the maximiser depends on the data through T.

### Q9 — `inf-t1-m-09` *(numeric, moderate)*

X₁,…,Xₙ are iid with density f(x;θ) = θ²x e^(−θx) for x > 0, θ > 0. Identify the minimal sufficient statistic and the dimension of the natural parameter.

*Options* `.options[]`:

- **A.** Σxᵢ, and the parameter is 1-dimensional  ← key
- **B.** (Σxᵢ, ∏xᵢ), and the parameter is 2-dimensional
- **C.** ∏xᵢ, and the parameter is 1-dimensional
- **D.** (Σxᵢ, Σlog xᵢ), and the parameter is 2-dimensional

*Explanation* `.explanation`: The joint density is θ^(2n)·(∏xᵢ)·exp(−θΣxᵢ). Only one exponential term carries θ, with t(x) = x, so T = Σxᵢ and the natural parameter is one-dimensional — a full-rank one-parameter exponential family, making T minimal sufficient and complete. The factor ∏xᵢ has no θ in it and belongs in h, which is what makes option B wrong.

*Arithmetic check* `.check`: A factor involving the data is not automatically part of the statistic. Test it: does it contain θ? ∏xᵢ does not, so it goes to h.

### Q10 — `inf-t1-m-10` *(order, moderate)*

You are given a density and asked for a minimal sufficient statistic. Arrange these steps in the order they should be carried out.

*Steps to order* `.items[]`:

- A. Write the joint density and group the factors containing θ
- B. Argue minimality, by exponential-family rank or the likelihood ratio
- C. Check whether the support of the density depends on θ
- D. Read T off the grouping and verify h contains no θ

*Options* `.options[]`:

- **A.** C, D, A, B
- **B.** C, A, D, B  ← key
- **C.** A, D, C, B
- **D.** A, C, D, B

*Explanation* `.explanation`: Check the support first — whether it moves with θ decides whether you may use the exponential-family shortcut or must keep an indicator. Then write the joint density, group the θ-terms to read off T, and finally argue minimality. Starting with the algebra and discovering the moving support afterwards wastes the time the first check would have saved.

### Q11 — `inf-t1-m-11` *(single, easy)*

A statistic T is sufficient for θ precisely when:

*Options* `.options[]`:

- **A.** T is an unbiased estimator of θ
- **B.** T has the smallest variance among all estimators of θ
- **C.** the conditional distribution of the sample given T = t does not depend on θ  ← key
- **D.** T is a one-to-one function of the maximum likelihood estimator

*Explanation* `.explanation`: Sufficiency is defined by the conditional distribution: once T is known, the rest of the sample carries no further information about θ. Unbiasedness and minimum variance are properties of estimators, not of sufficiency, and while the MLE is usually a function of a sufficient statistic, that is a consequence rather than the definition.

### Q12 — `inf-t1-m-12` *(numeric, easy)*

X₁,…,X₆ are iid N(μ, 1) with μ unknown and the variance known to be 1. A sample gives Σxᵢ = 18. Name the minimal sufficient statistic and give its value.

*Options* `.options[]`:

- **A.** Σxᵢ² = 18
- **B.** x₍₆₎ = 18
- **C.** (ΣXᵢ, Σxᵢ²) = (18, 18)
- **D.** ΣXᵢ = 18  ← key

*Explanation* `.explanation`: With σ² known the density factorises with θ appearing only through Σxᵢ, so ΣXᵢ (equivalently X̄ = 3) is minimal sufficient and its value is 18. Σxᵢ² would be needed only if σ² were also unknown, and the sample maximum carries no special role for a normal family.

*Arithmetic check* `.check`: One unknown parameter means one coordinate in the sufficient statistic. If your answer is a pair, check whether σ² was actually given.

### Q13 — `inf-t1-m-13` *(numeric, moderate)*

X₁,…,X₄ are iid Gamma with BOTH the shape α and the rate β unknown. The observations are 1, 2, 4 and 8. Give the value of the minimal sufficient statistic.

*Options* `.options[]`:

- **A.** (Σxᵢ, Σ log xᵢ) = (15, 4.159)  ← key
- **B.** Σxᵢ = 15
- **C.** (Σxᵢ, Σxᵢ²) = (15, 85)
- **D.** (x₍₁₎, x₍₄₎) = (1, 8)

*Explanation* `.explanation`: The gamma density is exp{(α−1)log x − βx + α log β − log Γ(α)}, a two-parameter exponential family with natural statistics Σlog Xᵢ and ΣXᵢ. Σxᵢ = 1+2+4+8 = 15 and Σlog xᵢ = log(1·2·4·8) = log 64 = 4.159. Σxᵢ alone would suffice only if α were known.

*Arithmetic check* `.check`: Two unknown parameters, two coordinates. The second one is a sum of LOGS, not of squares — that is the giveaway for the gamma rather than the normal.

### Q14 — `inf-t1-m-14` *(multi, moderate)*

Let T be sufficient for θ in a family with a fixed support.

*Statements to judge* `.statements[]`:

- **A.** Any one-to-one function of T is also sufficient for θ.
- **B.** f(x;θ) = g(T(x);θ)·h(x) for some non-negative g and h.
- **C.** T is necessarily of lower dimension than the sample.
- **D.** The MLE is a function of T whenever the MLE is unique.

*Options* `.options[]`:

- **A.** A and C only
- **B.** A, B and D only  ← key
- **C.** B, C and D only
- **D.** A, B and C only

*Explanation* `.explanation`: A is true — any invertible transformation of a sufficient statistic is sufficient. B is true: that is the factorisation theorem. C is false, and it is the point of minimal sufficiency: the whole sample is always sufficient and is almost never minimal. D is true — the MLE maximises g(T;θ), so it depends on the data only through T.

*Verdict on each statement* `.verdicts`:

- **A — true.** Knowing T and knowing a one-to-one function of T are the same knowledge.
- **B — true.** The factorisation theorem, stated in the direction you use to verify sufficiency.
- **C — false.** The entire sample is sufficient for every family. Reduction is what MINIMAL sufficiency asks for.
- **D — true.** h(x) does not involve θ, so maximising the likelihood maximises g(T;θ).

### Q15 — `inf-t1-m-15` *(numeric, moderate)*

X₁,…,X₄ are iid U(θ, θ+1) with θ ∈ ℝ unknown. The observations are 2.3, 2.9, 2.5 and 3.1. Give the value of the minimal sufficient statistic.

*Options* `.options[]`:

- **A.** x̄ = 2.7
- **B.** x₍₄₎ = 3.1
- **C.** (x₍₁₎, x₍₄₎) = (2.3, 3.1)  ← key
- **D.** Σxᵢ = 10.8

*Explanation* `.explanation`: The likelihood is 1 exactly when θ ≤ x₍₁₎ and x₍₄₎ ≤ θ+1, and 0 otherwise, so it depends on the data only through the smallest and largest observations. The pair (X₍₁₎, X₍₄₎) is minimal sufficient — and note it is two-dimensional for a one-dimensional parameter, which is allowed.

*Arithmetic check* `.check`: The support moves with θ at BOTH ends here, so both extremes matter. For U(0,θ) only the maximum would.

### Q16 — `inf-t1-m-16` *(multi, hard)*

Consider minimal sufficiency and the statistics around it.

*Statements to judge* `.statements[]`:

- **A.** A minimal sufficient statistic is a function of every other sufficient statistic.
- **B.** Every minimal sufficient statistic is complete.
- **C.** An ancillary statistic is one whose distribution determines θ.
- **D.** If f(x;θ)/f(y;θ) is free of θ exactly when T(x) = T(y), then T is minimal sufficient.

*Options* `.options[]`:

- **A.** A, B and C only
- **B.** B and D only
- **C.** A, B and D only
- **D.** A and D only  ← key

*Explanation* `.explanation`: A is true, and is the usual working definition. B is false: a minimal sufficient statistic need not be complete — U(θ, θ+1) has minimal sufficient (X₍₁₎, X₍₄₎), which is not complete because the range has a θ-free distribution. C is false: an ancillary statistic has a distribution free of θ, so it carries no information about θ on its own. D is true — the Lehmann–Scheffé ratio criterion.

*Verdict on each statement* `.verdicts`:

- **A — true.** It achieves the greatest reduction, so every other sufficient statistic determines it.
- **B — false.** U(θ, θ+1) is the standard counterexample: minimal sufficient but not complete.
- **C — false.** Backwards. Ancillary means the distribution does NOT depend on θ.
- **D — true.** The ratio criterion, and the practical way to verify minimality.

### Q17 — `inf-t1-m-17` *(numeric, moderate)*

X₁,…,X₅ are iid N(μ, σ²) with BOTH parameters unknown. A sample gives Σxᵢ = 20 and Σxᵢ² = 90. Taking T = (ΣXᵢ, ΣXᵢ²), give its value — and note that s² below means the unbiased sample variance Σ(xᵢ − x̄)²/(n − 1).

*Options* `.options[]`:

- **A.** (Σxᵢ, Σxᵢ²) = (20, 90)  ← key
- **B.** Σxᵢ = 20
- **C.** (x̄, Σxᵢ²) = (20, 90)
- **D.** (x̄, s²) = (4, 2.0)

*Explanation* `.explanation`: Two unknown parameters give a two-dimensional natural statistic, (ΣXᵢ, ΣXᵢ²) = (20, 90). Option D names a pair that IS minimal sufficient — (x̄, s²) is a one-to-one function of the natural statistic — but its value is wrong: s² = (90 − 20²/5)/(n−1) = 10/4 = 2.5, not 2.0 (2.0 is the divisor-n version). Option C mislabels x̄ as 20 when x̄ = 4.

*Arithmetic check* `.check`: Σxᵢ²/n − x̄² = 18 − 16 = 2 is the divisor-n variance; the unbiased s² multiplies by n/(n−1) = 5/4 to give 2.5.

### Q18 — `inf-t1-m-18` *(single, easy)*

Which statement about sufficient statistics is FALSE?

*Options* `.options[]`:

- **A.** A sufficient statistic can be higher-dimensional than the parameter
- **B.** A sufficient statistic must always reduce the data to a single number  ← key
- **C.** The entire sample (X₁,…,Xₙ) is always sufficient for θ
- **D.** The order statistics are sufficient whenever the observations are iid

*Explanation* `.explanation`: Sufficiency says nothing about dimension. The whole sample is trivially sufficient, the order statistics are sufficient for any iid model, and U(θ, θ+1) has a two-dimensional minimal sufficient statistic for a one-dimensional θ. Only the claim of reduction to a single number is false.

### Q19 — `inf-t1-m-19` *(numeric, hard)*

X₁,…,Xₙ are iid Cauchy with location θ, f(x;θ) = 1/(π(1 + (x−θ)²)). What is the minimal sufficient statistic?

*Options* `.options[]`:

- **A.** the sample median
- **B.** (ΣXᵢ, ΣXᵢ²)
- **C.** the full set of order statistics — no reduction is possible  ← key
- **D.** x̄, the sample mean

*Explanation* `.explanation`: The Cauchy location family is not an exponential family, and the likelihood ratio for two parameter values depends on the individual observations in a way no summary can absorb. The minimal sufficient statistic is the complete set of order statistics: the sample cannot be reduced at all. The sample mean is useless here — the Cauchy has no finite mean and x̄ has the same Cauchy distribution as a single observation.

*Arithmetic check* `.check`: If a family is not an exponential family, do not assume a low-dimensional sufficient statistic exists. The Cauchy is the standard case where none does.

### Q20 — `inf-t1-m-20` *(order, moderate)*

To show a proposed statistic T is sufficient by the factorisation theorem, arrange these steps.

*Steps to order* `.items[]`:

- A. Split the product into a θ-part and a data-only part
- B. Conclude that T is sufficient
- C. Write the joint density, indicators included
- D. Check the data-only factor contains no θ

*Options* `.options[]`:

- **A.** A, C, D, B
- **B.** C, D, A, B
- **C.** A, D, C, B
- **D.** C, A, D, B  ← key

*Explanation* `.explanation`: Write the joint density first — including the indicator functions, because for a moving support those indicators are where the parameter hides. Then split it into a part depending on the data only through T and a part free of θ, confirm the second factor really has no θ in it, and conclude.

---

## Authoring and verification record `provenance`

Reproduced verbatim. It records what changed in each version and how each derivation was checked, including the findings of the two previous review rounds and the reasons some of their recommendations were declined.

> v4.3, October 2026. A third-party review of the whole module found that v4.2's qualification of the MLE claim had been applied in one place and not in two others — the revision sheet and the summary scene both still said the MLE is ALWAYS a function of a sufficient statistic. Correct finding, and the inconsistency was introduced by v4.2 itself; both are now qualified to a unique MLE, with the set-of-maximisers case stated. The same review's rewritten 'how to use this lesson' note was declined: it drops the sentence telling the learner that one section is an optional JRF extension and that the topic completes without it. v4.2, October 2026, applies a third review round, which returned the mastery pool as a file with two targeted stem corrections and everything else unchanged. Both were real: inf-t1-m-02 asked for the value of 'the minimal sufficient statistic' while offering 0.4167 = 5/12 = x̄, which is a one-to-one function of ΣXᵢ for fixed n and so minimal sufficient itself — two defensible keys; and inf-t1-m-17 offered (x̄, s²) = (4, 2.0), where (x̄, s²) IS minimal sufficient and 2.0 is the divisor-n variance, so with s² left undefined the option was defensible. Applying that principle across the whole pool rather than only where the reviewer applied it found the same defect in two items it had not flagged — m-04, whose option (5, 27) is (Σxᵢ/n, Σxᵢ²/n), and m-07, whose option 7 is x̄ = 42/6. The tell in every case is that the explanation confessed it, calling the distractor 'a valid one-to-one transform'; vcheck.js now fails on that confession. Two further errors of my own surfaced while working through the file: m-03's verdict B described the dimension mismatch as 'the same mismatch that defines a curved family', conflating a moving support with a curved exponential family when U(θ, θ+1) is not an exponential family at all; and m-05's explanation attached the support discussion to option D when it belongs to option B. Two lesson statements were scoped on the reviewer's advice: the MLE is a function of a sufficient statistic when it exists and is unique, and otherwise it is the set of maximisers that is determined; and the likelihood-principle equivalence is stated as holding under the same conditions as the ratio criterion rather than unconditionally. The reviewer's accompanying prose document was written against v4.0, so its other recommendations describe fixes v4.1 had already made, the version-label inconsistency among them. v4.1 applied a second-round academic review of v4.0 and corrects three real errors it found. (i) An OVERCLAIM, in the trapcheck reason and in one elimination shortcut, that ONLY one-to-one functions of a sufficient statistic are sufficient. That is false: the whole sample is sufficient and Σxᵢ is a many-to-one function of it that is also sufficient. The verdict on the claim being judged is unchanged — 'every function of a sufficient statistic is sufficient' is still false — but the reason given for it was wrong, and the corrected text now carries the counterexample. One-to-one is what GUARANTEES preservation; many-to-one must be checked. (ii) A MISSING CONDITION: the (x̄, s²) ↔ (Σxᵢ, Σxᵢ²) equivalence requires n ≥ 2, since s² divides by n − 1. (iii) A LOOSE ARGUMENT in the Uniform(θ, θ+1) incompleteness note: an expectation free of θ is not itself a failure of completeness. The range is ancillary with constant expectation c, and it is the CENTRED function g(T) = (max − min) − c, with E_θ[g(T)] = 0 for every θ and g not identically zero, that demonstrates incompleteness. Two statements were also tightened on the review's advice: the Lehmann–Scheffé ratio criterion now carries its support proviso, and the Cauchy root argument is stated over multisets. The same review turned v4.0's own criticism back on this app, correctly: mastery item inf-t1-m-01 asked for 'a sufficient statistic' while offering (Σxᵢ, ∏xᵢ) as a distractor, and that pair IS sufficient, merely not minimal — the very defect v4.0 declined to import from the previous rewrite. Its stem now asks for the minimal statistic and its explanation names the trap explicitly. Points from the review that needed no change, having already been addressed: the mastery policy is labelled a platform setting rather than an NTA rule; prerequisite teaching was moved out of collapsed blocks in v3.0; scene completion is stored separately from mastery performance; and the family table already scrolls rather than overflowing at 390px. v4.0 merged an earlier external pedagogical review of v3.0. Adopted from that review: a 'how to use this lesson' note; statistic / estimator / estimate promoted from a block to its own scene, placed immediately after the coin so the thought 'so p̂ = 0.7' is met where it arises; a family → statistic reference table in the factorisation scene and again in the summary; a quick check on every teaching scene rather than three; concrete numbers (2.1, 0.7, 3.6, 1.9) in the Uniform scene so it reads without the interactive plot; and the Uniform(θ, θ+1) and Cauchy material gathered into a single scene marked an optional JRF extension, so the core path is 16 sections and completes without it. Declined from that review, with reasons: its replacement mastery set of 10 single-answer recall items in place of the 20-item pool across four formats, since JRF turns on the harder discriminating items; the removal of the exponential-family block, which is what explains why sums recur and which 4.2 and 4.9 both depend on; its verbal treatment of the Cauchy ('in general these terms cannot be reduced') in place of the ratio argument; and the loss of the likelihood-principle line and the map of where sufficiency is used later in the module. Two defects in its question set were also not carried over: its Q6 offers (Σxᵢ, Σxᵢ²) as a distractor for a sufficient statistic when σ² is known, but that pair IS sufficient there and merely not minimal, so the item is unsound as worded; and its answer keys run C,B,A,C,D,B,C,C,D,C — five of ten on C, which this app's validator rejects at a 40% cap per letter. v3.0, which this builds on, was itself a RE-SEQUENCING for a learner returning after a long gap. v2.0 was mathematically complete but front-loaded everything hard: it opened with four prerequisite checks a rusty learner cannot answer ('write the joint density of an iid sample'; 'write the densities of five families'), so the first ninety seconds produced four failures — and the two best explanations in the lesson, including the Bernoulli 1/C(n,t) cancellation that is the one concrete proof a beginner needs, were buried inside those checks' collapsed refresh text. The intuition scene asserted that the total carries all the information about p without showing a single number; the Cauchy counterexample sat at scene 2, before any clean case had succeeded; and the general theorem came before the worked Bernoulli case, skipping the index-law step (1−p)^(n−Σx) = (1−p)ⁿ/(1−p)^Σx that makes the factorisation readable. This version changes the order and fills those gaps, preserving almost all of v2.0's prose: the foundation checks are now four a rusty learner can answer and which together constitute the proof to come; scene 2 is the coin done slowly with real numbers and the 1/120 cancellation; scene 3 promotes the buried likelihood passage to a real scene with a block glossing every symbol once; the worked Bernoulli now precedes the general theorem; 'sufficiency is a property of the model' is its own scene; the Cauchy moved to scene 12; an exam-recognition line was added to every teaching scene; and the beginner's conflation of a sufficient statistic with an estimator is now addressed explicitly, because teaching sufficiency as 'count the heads, so p̂ = 0.7' plants exactly that error. Every derivation was written out and checked rather than quoted: the Bernoulli conditional distribution P(X = x | T = t) = 1/C(n,t), which is 1/10 for n = 5, t = 3 and 1/120 for n = 10, t = 7; the Bernoulli ratio [p/(1−p)]^(Σx−Σy), free of p iff Σx = Σy; the normal two-parameter ratio exp{−(Σx²−Σy²)/2σ² + μ(Σx−Σy)/σ²}, free of both parameters iff both sums agree; and the Uniform(θ, θ+1) likelihood I(max − 1 ≤ θ ≤ min), which gives the two-dimensional minimal sufficient statistic (min, max) for a one-dimensional parameter.

