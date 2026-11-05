#!/usr/bin/env python3
# Insert a "foundation" scene at the front of every lesson.
# Audience: someone returning to NET preparation after a two to three year gap.
# Each item is a prerequisite the lesson will lean on, with a one-line recall
# answer and a short rebuild for anyone who marks it shaky.
import json, io, os, sys

SEED = "seed"

def P(*xs): return list(xs)

FOUND = {}

FOUND["lesson_t1.json"] = dict(
  title="Before the lesson — four things it will assume",
  mins=6,
  objective="Check the handful of second-year tools this topic rests on, and rebuild any that have gone quiet.",
  body=P(
    "Most people come back to NET preparation after a break of two or three years. Nothing in this lesson is hard, but it does assume four small things are automatic. If they are not, the lesson reads as if it is skipping steps — and it is not; those steps happened in your second year.",
    "So spend five minutes here first. For each item, answer it in your head, then say honestly whether you knew it. \"Shaky\" is not a confession, it is an instruction to the page: it opens a short rebuild in place, and you carry on."
  ),
  items=[
    dict(
      ask="Write down the joint density of an iid sample x₁,…,xₙ drawn from f(x;θ).",
      recall="∏ᵢ₌₁ⁿ f(xᵢ;θ) — the same function f evaluated at each observation, all multiplied together. Independence is what makes it a product; identically distributed is what makes every factor the same f.",
      refresh=P(
        "Two facts, joined. For independent variables the joint density factorises: f(x₁,…,xₙ) = f₁(x₁)·f₂(x₂)⋯fₙ(xₙ). For identically distributed variables every one of those marginals is the same function. Put them together and you get ∏f(xᵢ;θ).",
        "Once the data are fixed and you let θ vary instead, that same expression is called the likelihood L(θ). Nothing changes on the page; only which symbol you regard as the unknown.",
        "Do one now. Poisson(θ): f(x;θ) = e^(−θ)θˣ/x!. The product is ∏ e^(−θ)θ^(xᵢ)/xᵢ! = e^(−nθ) θ^(Σxᵢ) / ∏xᵢ!. Notice how the n exponentials collected into one e^(−nθ) and the powers of θ collected into θ^(Σxᵢ). Collecting like that is the whole mechanical skill this lesson needs."
      )),
    dict(
      ask="What does a conditional distribution of the sample given T = t mean?",
      recall="P(A|B) = P(A∩B)/P(B). The conditional distribution of the data given T = t is the distribution over exactly those data sets that would have produced that t, each one's probability divided by P(T=t) so the pieces add to one.",
      refresh=P(
        "Take three Bernoulli(p) tosses and T = Σxᵢ. Ask for the conditional distribution given T = 2. Only three sequences qualify: HHT, HTH, THH, each with probability p²(1−p). And P(T=2) = 3p²(1−p).",
        "So each sequence has conditional probability p²(1−p) / 3p²(1−p) = 1/3. The p cancelled. That is not a coincidence of this example — it is the definition of sufficiency arriving early, and the lesson's third section will say it formally.",
        "You will almost never have to compute one of these in the exam. You do have to know what the definition is claiming, because the claim is where the intuition lives."
      )),
    dict(
      ask="Rewrite (∏xᵢ)^θ and ∏xᵢ^(θ−1) using exp and a single sum.",
      recall="(∏xᵢ)^θ = exp(θ Σ log xᵢ) and ∏xᵢ^(θ−1) = exp((θ−1) Σ log xᵢ). A product raised to a power becomes an exponential of a sum, because log turns products into sums.",
      refresh=P(
        "Two moves. First, a = e^(log a) for any a > 0. Second, log of a product is the sum of the logs. So (∏xᵢ)^θ = e^(θ·log∏xᵢ) = e^(θ Σ log xᵢ).",
        "This is the single manipulation that unlocks half the questions in the topic, because it drags the data into one sum sitting next to θ. Example: for the density f(x;θ) = θx^(θ−1) on (0,1), the joint density is θⁿ ∏xᵢ^(θ−1) = θⁿ exp((θ−1) Σ log xᵢ). Written that way, Σ log xᵢ is visibly the only thing about the data that θ ever touches — so that is the sufficient statistic, read off without a single integral.",
        "Practise the move in the other direction too: exp(θ Σ log xᵢ) back to (∏xᵢ)^θ. Exam options are often written in whichever of the two forms is less familiar."
      )),
    dict(
      ask="What does an indicator 1{0 < x < θ} do inside a density, and what is ∏ᵢ 1{0 < xᵢ < θ}?",
      recall="An indicator equals 1 when its condition holds and 0 otherwise. A product of indicators is 1 only if every condition holds, so ∏1{0 < xᵢ < θ} = 1{x₍₁₎ > 0}·1{x₍ₙ₎ < θ} — the smallest and largest observation are all that survive.",
      refresh=P(
        "An indicator is a switch written as a number, so that a density defined piecewise can be written in one line. For U(0,θ): f(x;θ) = (1/θ)·1{0 < x < θ}, which is 1/θ on the interval and 0 outside it.",
        "Multiply n of those together: θ^(−n) ∏1{0 < xᵢ < θ}. The product of the n switches is on only when every xᵢ clears both bounds, and 'every xᵢ is below θ' is the same statement as 'the largest xᵢ is below θ'. So the joint density is θ^(−n) 1{x₍ₙ₎ < θ} 1{x₍₁₎ > 0}.",
        "This matters more than it looks. A candidate who writes θ^(−n) and drops the indicator concludes that the data say nothing about θ at all. The indicator is where θ meets the data, and the largest observation is the sufficient statistic because of it. Any time the range of a density depends on θ, the indicator is the load-bearing part of the expression."
      ))]
)

FOUND["lesson_mle.json"] = dict(
  title="Before the lesson — four things it will assume",
  mins=6,
  objective="Confirm that writing a likelihood, logging it and differentiating it are automatic before the derivations begin.",
  body=P(
    "Maximum likelihood is a short topic with a long tail of arithmetic. Everything in it reduces to: write L(θ), take logs, differentiate, set to zero. If any one of those four steps is slow, every derivation in the lesson will feel like three topics at once.",
    "After a two or three year gap it is usually the differentiating that has gone quiet, not the idea. Four checks, five minutes. Mark anything shaky and read the rebuild before you move on."
  ),
  items=[
    dict(
      ask="For an iid sample, what is the likelihood L(θ), and how does it differ from the joint density?",
      recall="L(θ) = ∏ᵢ₌₁ⁿ f(xᵢ;θ). It is exactly the joint density — the same expression, not an approximation of it. The only difference is which symbol you treat as fixed: the density holds θ fixed and varies x, the likelihood holds the observed x fixed and varies θ.",
      refresh=P(
        "Independence makes the joint density a product; identical distribution makes every factor the same f. So the joint density of the sample is ∏f(xᵢ;θ).",
        "Now the data have arrived and are numbers. The only unknown left is θ, so read the same expression as a function of θ and call it L(θ). That re-reading is the entire conceptual content of the word 'likelihood'.",
        "It is not a probability of θ. L(θ) does not integrate to one over θ, and nothing in this course lets you say 'the probability that θ = 3'. It is a comparison: L(3) > L(5) says the observed data were more probable under 3 than under 5."
      )),
    dict(
      ask="Differentiate a log-likelihood. Which two rules do you need?",
      recall="log of a product is a sum of logs, so the derivative of the whole is the sum of the derivatives; and d/dθ log g(θ) = g′(θ)/g(θ). Those two turn any product likelihood into a manageable sum.",
      refresh=P(
        "Work one all the way through. Exponential with rate λ: f(x;λ) = λe^(−λx), so L(λ) = λⁿ e^(−λΣxᵢ).",
        "Take logs: ℓ(λ) = n log λ − λΣxᵢ. The product became a sum, and the exponential became linear — that is why you log first and always.",
        "Differentiate: ℓ′(λ) = n/λ − Σxᵢ. Set it to zero: λ̂ = n/Σxᵢ = 1/x̄. Then check it is a maximum: ℓ″(λ) = −n/λ², negative for every λ > 0, so the stationary point is the maximum. Do not skip that check in the exam — some questions are set precisely where it fails."
      )),
    dict(
      ask="Why is maximising log L the same as maximising L?",
      recall="log is strictly increasing, so it preserves order: if L(θ₁) > L(θ₂) then log L(θ₁) > log L(θ₂). The maximising θ is therefore identical. The maximum value is not the same, but nobody asked for it.",
      refresh=P(
        "A strictly increasing transformation cannot change which input is largest — it only relabels the heights. So the argmax survives, and taking logs is free.",
        "This is also why the MLE of a function of θ is that function of the MLE when the function is one-to-one: if θ̂ maximises the likelihood in θ, then g(θ̂) maximises it in g(θ). That is the invariance property, and the lesson uses it from the worked examples onwards."
      )),
    dict(
      ask="What does the factorisation theorem say, and why is it a free check on any MLE you compute?",
      recall="If f(x;θ) = g(T(x);θ)·h(x) with h free of θ, then T is sufficient for θ. The MLE maximises g(T;θ), since h contributes no θ — so the MLE is always a function of a sufficient statistic.",
      refresh=P(
        "Split the joint density into the part that involves θ and the part that does not. Whatever function of the data appears in the θ-part is a sufficient statistic.",
        "The consequence is a check you can apply in ten seconds. For a Poisson sample the joint density is e^(−nθ)θ^(Σxᵢ)/∏xᵢ!, so Σxᵢ is sufficient — and the MLE must be a function of Σxᵢ. It is: θ̂ = x̄.",
        "If your derivation ever produces an estimator that depends on the data in some way the sufficient statistic does not capture — the median, say, when the sufficient statistic is Σxᵢ — you have made an algebra slip. Go back rather than trusting it."
      ))]
)

FOUND["lesson_t2.json"] = dict(
  title="Before the lesson — four things it will assume",
  mins=6,
  objective="Check the three pieces of machinery every completeness argument is built from, before the first proof.",
  body=P(
    "Completeness is the one idea in this module that looks like pure algebra, and that is exactly what it is: you write E[g(T)] = 0 for every θ and then argue that g must have been zero all along. The argument is short. It is also unforgiving if the algebra underneath is rusty.",
    "Three of these four checks are the algebra. The first is the topic that comes before this one — if it is shaky, finish sufficiency first; this lesson will assume you can produce T without thinking."
  ),
  items=[
    dict(
      ask="What does the factorisation theorem say, and why is completeness always asked about a sufficient statistic?",
      recall="If f(x;θ) = g(T(x);θ)h(x) with h free of θ, then T is sufficient. Completeness is a property of the distribution family of T, and it is useful only because of Lehmann–Scheffé — which needs T to be both complete and sufficient.",
      refresh=P(
        "Sufficiency says nothing was lost. Completeness says nothing is wasted: the family of distributions of T is rich enough that no non-trivial function of T can average to zero at every θ.",
        "Alone, completeness is a curiosity. Paired with sufficiency it gives uniqueness — one and only one unbiased function of T — and that is what makes an estimator provably best. So every exam question about completeness is really a question about the pair.",
        "If writing down T is still slow, do the sufficiency topic first. Everything here starts after that step."
      )),
    dict(
      ask="Write E[g(T)] out as an expression, for a discrete T and for a continuous T.",
      recall="Discrete: Σ_t g(t)P(T=t), summed over the support. Continuous: ∫ g(t)f_T(t)dt over the support. Every completeness argument begins by writing one of these and ends by asking what 'this is 0 for all θ' forces on g.",
      refresh=P(
        "Expectation of a function of a random variable does not need the distribution of that function. You weight g(t) by the probability of t and add up: that is the law of the unconscious statistician, and it is why no change of variable is needed.",
        "Write the binomial case out in full, because the lesson's first proof is exactly this: E[g(T)] = Σ_(t=0)^n g(t)·C(n,t)p^t(1−p)^(n−t).",
        "And the continuous template, for a one-parameter exponential-family T: E[g(T)] = ∫ g(t)·c(θ)h(t)e^(θt)dt. Setting that to zero for all θ is a statement about a transform of g, which is why these proofs end in a uniqueness argument rather than algebra."
      )),
    dict(
      ask="A power series Σaₖzᵏ equals zero for every z in an interval. What follows about the coefficients?",
      recall="Every aₖ is zero. A power series that is not identically zero has isolated roots — at most countably many — so it cannot vanish on a whole interval.",
      refresh=P(
        "This is the step that finishes almost every completeness proof, so it is worth having a picture of. A nonzero polynomial of degree m has at most m roots; a nonzero power series behaves the same way locally. Vanishing everywhere on an interval is therefore only possible if there was nothing there to begin with.",
        "See it used. For binomial completeness, set E[g(T)] = 0 and divide through by (1−p)ⁿ, which is never zero for p in (0,1). With z = p/(1−p), which sweeps all of (0,∞) as p sweeps (0,1), you are left with Σ_(t=0)^n g(t)C(n,t)zᵗ = 0 for every z > 0.",
        "That is a polynomial in z vanishing on an interval, so every coefficient g(t)C(n,t) is zero, and since C(n,t) > 0, g(t) = 0 for t = 0,…,n. Completeness proved. Notice that the family had to contain enough values of p for z to sweep an interval — the same proof fails if p can only be 1/3 or 1/2."
      )),
    dict(
      ask="What is the support of a distribution, and why is the conclusion 'g(T) = 0 with probability one' rather than 'g is the zero function'?",
      recall="The support is the set of values T actually takes with positive probability. Completeness forces g to vanish there and says nothing about g anywhere else, so the honest conclusion is P(g(T)=0) = 1 for every θ.",
      refresh=P(
        "For a binomial T the support is {0,1,…,n}: the argument pins down n+1 numbers. g(17.5) is simply never consulted, because T never takes that value.",
        "This is not pedantry — it is how a question gets set. 'T is complete, g(T) has expectation zero, therefore g ≡ 0' is a false option; the true one says 'almost surely' or 'with probability one'. Read the options for that phrase.",
        "It also explains why the unbiased function of a complete sufficient statistic is unique only up to sets of probability zero: two estimators that differ nowhere that matters are counted as the same estimator."
      ))]
)

FOUND["lesson_t3.json"] = dict(
  title="Before the lesson — four things it will assume",
  mins=6,
  objective="Rebuild conditional expectation and the variance decomposition, which together are the whole proof of Rao–Blackwell.",
  body=P(
    "Rao–Blackwell has a reputation for being deep. It is one line of algebra you already know: a variance splits into two non-negative pieces, so throwing one away can only help. The theorem is that observation, applied to E[δ|T].",
    "What makes it feel hard after a gap is conditional expectation — specifically, remembering that E[δ|T] is a random variable and not a number. Three checks on that, one on the topic before this."
  ),
  items=[
    dict(
      ask="What does the factorisation theorem say, and why must Rao–Blackwell condition on a sufficient statistic specifically?",
      recall="If f(x;θ) = g(T(x);θ)h(x) with h free of θ, then T is sufficient. Conditioning on a sufficient T leaves no θ in the conditional distribution, so E[δ|T] is computable from the data alone. Condition on a non-sufficient statistic and the answer still contains θ — it is not an estimator at all.",
      refresh=P(
        "Sufficiency is doing real work here, not decoration. E[δ|T=t] is an average over the conditional distribution of the data given T=t. If that conditional distribution depends on θ, so does the average, and you cannot compute it without knowing the very thing you are estimating.",
        "That is the one-sentence reason the theorem is stated for sufficient statistics: sufficiency is exactly the condition that makes the conditional average usable."
      )),
    dict(
      ask="Is E[δ|T] a number or a random variable? And what is E[X₁ | ΣXᵢ = t] for an iid sample?",
      recall="A random variable — a function of T. E[δ|T=t] is a number, for each fixed t; E[δ|T] is the whole function, and it has a variance of its own. By symmetry E[X₁|ΣXᵢ=t] = t/n, since the n observations are exchangeable and their conditional means must sum to t.",
      refresh=P(
        "Keep the two notations apart and most of the confusion goes. E[δ|T=t] means 'average δ over all data sets with T=t' — a number depending on t. E[δ|T] means 'that number, as a function of the random T' — a random variable.",
        "The symmetry argument is worth having at your fingertips because it appears in exam questions as a one-step answer. If X₁,…,Xₙ are iid and you are told ΣXᵢ = t, no observation is distinguishable from any other, so all n conditional means are equal; they add to t; so each is t/n. No distribution was needed.",
        "The same move, less obviously: E[X₁X₂|ΣXᵢ=t] is the same for every pair, which turns a hard conditional expectation into counting pairs."
      )),
    dict(
      ask="State the decomposition of Var(δ) in terms of a statistic T.",
      recall="Var(δ) = E[Var(δ|T)] + Var(E[δ|T]). Both terms are non-negative, so Var(E[δ|T]) ≤ Var(δ). That single inequality is Rao–Blackwell.",
      refresh=P(
        "Read it as bookkeeping. The total variability of δ is the variability left inside each level of T, averaged across levels, plus the variability of the level averages themselves. Nothing is created or lost.",
        "Rao–Blackwell keeps the second term and discards the first. Since E[Var(δ|T)] ≥ 0 always, the replacement estimator E[δ|T] has variance no larger — and strictly smaller unless Var(δ|T) = 0, which means δ was already a function of T.",
        "The companion fact is the tower property: E[E[δ|T]] = E[δ]. It is what guarantees the new estimator is still unbiased, so you have paid nothing for the variance reduction. Have both lines ready before section 3."
      )),
    dict(
      ask="What does 'unbiased' mean precisely, and what does 'uniformly minimum variance' add to it?",
      recall="Unbiased: E[T] = θ for every θ in the parameter space, not just for one convenient value. UMVUE adds that among all unbiased estimators, this one has the smallest variance at every θ simultaneously — no trading good performance at one θ for bad at another.",
      refresh=P(
        "The 'for every θ' in unbiasedness is where marks are lost. An estimator that happens to be right on average when θ = 2 is not unbiased.",
        "The word 'uniformly' carries the same weight. It is easy to find an estimator with tiny variance at one point — the constant 7 has variance zero and is superb if θ really is 7. Requiring unbiasedness rules out that cheat, and requiring minimum variance uniformly rules out the subtler versions of it.",
        "This is why Lehmann–Scheffé is worth so much: it hands you a single estimator that wins at every θ at once, which is a far stronger statement than winning on average."
      ))]
)

FOUND["lesson_t5.json"] = dict(
  title="Before the lesson — four things it will assume",
  mins=6,
  objective="Get the moments of the standard families and the moment/variance identity back to automatic, since every equation in this topic starts there.",
  body=P(
    "The method of moments is the easiest estimation method to state and the easiest to fumble. Stating it takes one line: set the sample moments equal to the population moments and solve. Fumbling it takes one forgotten formula — the variance of a uniform, say, or the rate-versus-scale convention for the gamma.",
    "So this check is mostly recall of standard results. That is deliberate: in the exam these are not derived, they are remembered, and a two year gap is exactly long enough to lose them."
  ),
  items=[
    dict(
      ask="Define the r-th population moment and the r-th sample moment, and state what the method of moments does with them.",
      recall="μ_r′ = E[Xʳ] and m_r′ = (1/n)Σxᵢʳ. For k unknown parameters, set m_r′ = μ_r′(θ) for r = 1,…,k and solve the k equations.",
      refresh=P(
        "The population moment is a property of the model and so is a function of θ: for an exponential with rate λ, μ₁′ = 1/λ. The sample moment is a number computed from the data and knows nothing about θ.",
        "The method just equates them and solves. One unknown, one equation: 1/λ = x̄ gives λ̃ = 1/x̄. Two unknowns, two equations — which is where the second moment comes in and where the arithmetic starts to bite.",
        "A word on notation, since exam papers use both. The prime marks a raw moment, about zero. Moments about the mean are written without it: μ₂ = Var(X). Mixing the two is the commonest source of a wrong sign in this topic."
      )),
    dict(
      ask="From memory: E[X] and Var(X) for the exponential, U(a,b), gamma and normal.",
      recall="Exponential with rate λ: 1/λ and 1/λ². U(a,b): (a+b)/2 and (b−a)²/12. Gamma with shape α and rate β: α/β and α/β². Normal(μ,σ²): μ and σ².",
      refresh=P(
        "Carry these four as a block, because the moment equations begin with them and there is no time to derive them in the exam.",
        "Exponential(λ): mean 1/λ, variance 1/λ². The exponential is a gamma with shape 1, which is the quickest way to recover it if you blank.",
        "U(a,b): mean is the midpoint (a+b)/2; variance is (b−a)²/12. The 12 is the one number people lose. Sanity check: U(0,1) has variance 1/12 ≈ 0.083, which is right for a spread of one unit.",
        "Gamma: with shape α and rate β, mean α/β and variance α/β². If the book uses scale θ = 1/β instead, the mean is αθ and the variance αθ². Read which convention a question is using before you write anything — the two differ by a reciprocal and the options will include both answers."
      )),
    dict(
      ask="How do E[X²], Var(X) and E[X] relate, and why does the second moment equation nearly always use that identity?",
      recall="E[X²] = Var(X) + (E[X])². The second sample moment (1/n)Σxᵢ² estimates E[X²], not the variance — so you convert the model's variance into a second moment before equating.",
      refresh=P(
        "Var(X) = E[X²] − (E[X])² rearranged. Nothing more, but it is used in every two-parameter moment problem.",
        "See why. For N(μ,σ²), the two moment equations are μ = x̄ and E[X²] = σ² + μ² = (1/n)Σxᵢ². Substituting the first into the second gives σ̃² = (1/n)Σxᵢ² − x̄² = (1/n)Σ(xᵢ−x̄)².",
        "Note what came out: the divisor is n, not n−1. The method of moments estimator of a variance is the biased one, and the lesson returns to that — the method makes no promise of unbiasedness, only of consistency."
      )),
    dict(
      ask="What does least squares minimise, and what are the normal equations for fitting a straight line?",
      recall="It minimises Σ(yᵢ − a − bxᵢ)². Setting the two partial derivatives to zero gives b̂ = Σ(xᵢ−x̄)(yᵢ−ȳ)/Σ(xᵢ−x̄)² and â = ȳ − b̂x̄.",
      refresh=P(
        "You differentiate the sum of squared vertical deviations with respect to a and then b, set both to zero, and solve. The two resulting equations are called the normal equations.",
        "Both formulas carry a reading worth keeping. b̂ is a ratio of the sample covariance of x and y to the variance of x. And â = ȳ − b̂x̄ says the fitted line passes through (x̄, ȳ) whatever the slope — a free check on any numerical answer.",
        "The lesson compares all three methods on the same footing, so you need this one in the same form as the other two: an estimating criterion, differentiated, set to zero."
      ))]
)

FOUND["lesson_t6.json"] = dict(
  title="Before the lesson — four things it will assume",
  mins=6,
  objective="Confirm the score, the two forms of Fisher information and the variance of a mean, before the bound is derived.",
  body=P(
    "The Cramér–Rao bound is a formula with four places to go wrong, and three of them are in the groundwork rather than the idea. You need the log-likelihood and its derivatives at speed, you need to know that information adds across an iid sample, and you need Var(X̄) = σ²/n on reflex because that is what almost every attainment check compares against.",
    "Four checks. If the first one is shaky, the maximum likelihood topic is the better place to be for half an hour — this lesson is built directly on it."
  ),
  items=[
    dict(
      ask="Write the log-likelihood and the score for an iid sample, and say what E[score] is.",
      recall="ℓ(θ) = Σᵢ log f(xᵢ;θ) and the score is U(θ) = ∂ℓ/∂θ = Σᵢ ∂log f(xᵢ;θ)/∂θ. Under the regularity conditions E[U(θ)] = 0 for every θ, and Var(U(θ)) = Iₙ(θ).",
      refresh=P(
        "The log turns the product likelihood into a sum, so the score is a sum of n independent terms — which is where every 'information adds' result comes from.",
        "E[U] = 0 is not an accident of a particular family; it follows from differentiating ∫f(x;θ)dx = 1 under the integral sign. That interchange is precisely what the regularity conditions license, and it is why the bound fails for U(0,θ), where the range of the density depends on θ.",
        "Do one. Exponential rate λ: log f = log λ − λx, so U(λ) = Σ(1/λ − xᵢ) = n/λ − Σxᵢ. Check: E[U] = n/λ − n·(1/λ) = 0, as promised."
      )),
    dict(
      ask="Give the two expressions for Fisher information from a single observation, and relate Iₙ(θ) to I(θ).",
      recall="I(θ) = E[(∂log f/∂θ)²] = −E[∂²log f/∂θ²] — the two are equal under the regularity conditions. For an iid sample Iₙ(θ) = n·I(θ): information adds.",
      refresh=P(
        "Use whichever is less work. The second-derivative form is usually easier because differentiating twice often kills the data entirely and leaves no expectation to take.",
        "Exponential rate λ again: log f = log λ − λx, so ∂²/∂λ² = −1/λ², which is already constant. Then I(λ) = −E[−1/λ²] = 1/λ², and Iₙ(λ) = n/λ².",
        "Additivity is worth a sentence of its own, because questions exploit it. The score is a sum of independent terms, so its variance is the sum of their variances, and each term contributes the same I(θ). Twice the data, twice the information, half the bound."
      )),
    dict(
      ask="What is Var(X̄) in terms of Var(X), and why does it appear in nearly every attainment check?",
      recall="Var(X̄) = σ²/n. For many standard families the bound for estimating the mean works out to exactly σ²/n, so the check 'is the bound attained?' becomes 'does my estimator's variance equal σ²/n?'",
      refresh=P(
        "Var(ΣXᵢ) = nσ² by independence, and dividing a random variable by n divides its variance by n², so Var(X̄) = nσ²/n² = σ²/n.",
        "That is why X̄ keeps turning out to be efficient. For a Poisson(θ) sample, Iₙ(θ) = n/θ so the bound is θ/n; and Var(X̄) = θ/n since the Poisson variance is θ. The bound is attained exactly, and X̄ is the UMVUE for θ.",
        "Keep the n straight. The bound 1/Iₙ(θ) uses the information in the whole sample; comparing it against Var(X) rather than Var(X̄) is the slip that makes an efficient estimator look n times too bad."
      )),
    dict(
      ask="If the target is τ(θ) rather than θ itself, what changes in the bound?",
      recall="The numerator becomes the square of the derivative: Var(T) ≥ [τ′(θ)]²/Iₙ(θ) for any T unbiased for τ(θ). Forgetting to square τ′ is the single most common slip in this topic.",
      refresh=P(
        "The plain bound Var(T) ≥ 1/Iₙ(θ) is the special case τ(θ) = θ, where τ′ = 1 and the numerator is invisible. As soon as the target is a function of θ, the numerator reappears.",
        "Example. Estimating τ(θ) = θ² from a Poisson sample: τ′ = 2θ, Iₙ = n/θ, so the bound is (2θ)²·θ/n = 4θ³/n. Dropping the square would give 2θ²/n — a different order in θ, and an option on the paper.",
        "The derivative is with respect to θ, evaluated at the true θ, and it is squared because variance is on a squared scale. If a question gives you τ in words — 'the probability of no events', e^(−θ) for a Poisson — write τ down explicitly and differentiate it before touching the bound."
      ))]
)

FOUND["lesson_t9.json"] = dict(
  title="Before the lesson — four things it will assume",
  mins=6,
  objective="Reinstate the two error definitions and the normal tail calculation, which every critical region in this topic ends with.",
  body=P(
    "Testing is where notation defeats people. The ideas are small — compare two likelihoods, reject when the ratio is large — but every question ends in a tail probability, and every option differs from its neighbours by an α, a β or a square root of n.",
    "Four checks: one on likelihoods, one on the two error types, one on the distribution of X̄, one on turning a ratio into an inequality. None takes more than a minute if it is there."
  ),
  items=[
    dict(
      ask="Write L(θ) for an iid sample, and the likelihood ratio for testing a simple H₀: θ = θ₀ against a simple H₁: θ = θ₁.",
      recall="L(θ) = ∏f(xᵢ;θ). The ratio is Λ(x) = L(θ₁)/L(θ₀) — the likelihood under the alternative over the likelihood under the null. Neyman–Pearson rejects H₀ when Λ is large.",
      refresh=P(
        "Both likelihoods are the same product, evaluated at two different values of θ. Nothing new is being introduced; you are comparing two heights of one curve.",
        "Conventions differ and this costs marks. Many books write the ratio the other way up, L(θ₀)/L(θ₁), and reject for small values. Either is correct; mixing them inside one question is not. Decide which way up you write it, and read each exam option for which way it is written.",
        "Do one. Exponential rate λ, testing λ₀ against λ₁ > λ₀: Λ = (λ₁/λ₀)ⁿ e^(−(λ₁−λ₀)Σxᵢ). Since λ₁ − λ₀ > 0, Λ is decreasing in Σxᵢ, so 'Λ large' is the same event as 'Σxᵢ small'. That translation is the whole technique."
      )),
    dict(
      ask="Define a Type I and a Type II error, and say which probability is α and which is β.",
      recall="Type I: rejecting H₀ when H₀ is true; its probability is α, the size or level. Type II: failing to reject H₀ when H₁ is true; its probability is β, and the power is 1 − β.",
      refresh=P(
        "Fix them by what is true, not by what you did. The label names the state of the world you got wrong: Type I happens only when H₀ is true, Type II only when it is false.",
        "α = P(reject H₀ | H₀ true) and β = P(accept H₀ | H₁ true). Power = 1 − β = P(reject H₀ | H₁ true) is the quantity Neyman–Pearson maximises, with α held fixed as a constraint.",
        "The trade-off is the subject of the whole topic. Shrinking the rejection region lowers α and raises β; the only way to improve both at once is more data. Any exam option claiming a test lowers both at fixed n is wrong on principle."
      )),
    dict(
      ask="For an iid N(μ,σ²) sample, what is the distribution of X̄, and how do you turn P(X̄ > c) into a standard normal probability?",
      recall="X̄ ~ N(μ, σ²/n). Then P(X̄ > c) = P(Z > (c−μ)/(σ/√n)) = 1 − Φ((c−μ)√n/σ), where Z is standard normal.",
      refresh=P(
        "A sum of independent normals is normal, so X̄ is normal; its mean is μ and its variance σ²/n. The √n in the denominator of the standardisation comes from that variance and is the most frequently dropped symbol in the whole paper.",
        "Standardise by subtracting the mean and dividing by the standard deviation — σ/√n here, not σ. So Z = (X̄−μ)√n/σ.",
        "The two numbers to carry: Φ(1.645) = 0.95 and Φ(1.96) = 0.975. A one-sided size-0.05 test puts the critical value at μ₀ + 1.645σ/√n; a two-sided one at μ₀ ± 1.96σ/√n. The lesson's power calculations standardise twice — once under H₀ to find c, once under H₁ to find the power at that c."
      )),
    dict(
      ask="If the likelihood ratio Λ is an increasing function of Σxᵢ, what does the rejection region {Λ > k} become?",
      recall="{Σxᵢ > c}, where c is chosen so that P(Σxᵢ > c | θ₀) = α. A monotone ratio lets you replace an inequality on Λ by an inequality on the single statistic, and that is the only reason the test is computable.",
      refresh=P(
        "If g is strictly increasing then g(t) > k and t > g^(−1)(k) describe the same set of t. So an inequality in Λ becomes an inequality in the statistic, and you never have to find k itself — you find c directly from the size condition.",
        "Watch the direction. If Λ is decreasing in the statistic, as in the exponential example above, {Λ > k} becomes {Σxᵢ < c} and the size condition is a lower tail. Getting this backwards produces a test of size 1 − α, which is always one of the options.",
        "Monotonicity is also exactly the condition the lesson later names MLR, and it is what upgrades a test for two simple hypotheses into a UMP test against a one-sided alternative. So this small algebraic step is carrying more weight than it looks."
      ))]
)

def main():
    changed = []
    for fn, found in FOUND.items():
        path = os.path.join(SEED, fn)
        d = json.load(io.open(path, encoding="utf-8"))
        scenes = d["scenes"]
        # idempotent: replace an existing foundation scene rather than stacking
        scenes = [s for s in scenes if s.get("kind") != "foundation"]
        sc = dict(kind="foundation", id="s0",
                  title=found["title"], mins=found["mins"],
                  objective=found["objective"],
                  body=found["body"], items=found["items"])
        d["scenes"] = [sc] + scenes
        d["estMin"] = d.get("estMin", 40) + found["mins"]
        try:
            maj, mnr = d.get("version", "1.0").split(".")
            d["version"] = "%s.%d" % (maj, int(mnr) + 1)
        except Exception:
            pass
        json.dump(d, io.open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        changed.append((fn, d["topicId"], len(d["scenes"]), len(found["items"])))
    for c in changed:
        print("%-20s %-14s %2d scenes  %d checks" % c)

if __name__ == "__main__":
    main()
