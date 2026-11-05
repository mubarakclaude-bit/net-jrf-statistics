# Authors the pilot lesson: Maximum Likelihood Estimation.
# Output: lesson_mle.json, qset_mle_practice.json, qset_mle_mastery.json
import json, os
OUT = "/home/claude/w1/seed"

L = lambda *p: list(p)

lesson = {
 "id": "mle",
 "moduleId": "inference",
 "topicId": "inference-t4",
 "title": "Maximum Likelihood Estimation",
 "breadcrumb": "Statistical Inference → Point Estimation → MLE",
 "engine": "B",
 "engineName": "Estimation and inference — likelihood curves, sampling distributions, visible assumptions",
 "estMin": 40,
 "version": "1.0",
 "status": "approved",
 "provenance": "Theory and worked examples authored for this platform; previous-year questions marked separately and carry their exam cycle.",
 "objectives": L(
   "Build the likelihood of a sample and say why it is a function of θ, not of x.",
   "Derive an MLE through the log-likelihood and the score equation, and verify it is a maximum.",
   "Recognise when the derivative method fails and the maximum sits on a boundary.",
   "Use invariance to get the MLE of a function of θ without redoing the work.",
   "Separate 'maximum likelihood' from 'unbiased', and state the properties the MLE does have."),
 "prereq": L(
   {"id":"p1","name":"Joint density of an iid sample","why":"The likelihood is that joint density, read as a function of θ."},
   {"id":"p2","name":"Differentiating logs and products","why":"Every MLE derivation turns a product into a sum of logs first."},
   {"id":"p3","name":"Sufficiency and the factorisation theorem","why":"The MLE always comes out as a function of the sufficient statistic — that is a free check on your answer."}),
 "mastery": {"minQ":10,"pass":80,"fmtMin":{"numeric":70,"multi":70},"noHints":True,"retestDays":7,
   "note":"Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints."},
 "refs": L(
  {"title":"Maximum Likelihood Estimation","where":"Lesson 1.2","site":"Penn State STAT 415 online notes",
   "url":"https://online.stat.psu.edu/stat415/lesson/1/1.2","type":"Course notes","free":True,"checked":"2026-10-12",
   "why":"The cleanest written derivation of the Bernoulli and Normal MLEs, step by step. Read it after scene 4 if the algebra still feels fast."},
  {"title":"Maximum likelihood estimation — theory, assumptions, properties","where":"Sections: the sample and its likelihood; the score; information matrix; consistency; asymptotic normality",
   "site":"StatLect","url":"https://www.statlect.com/fundamentals-of-statistics/maximum-likelihood","type":"Reference","free":True,"checked":"2026-10-12",
   "why":"Where to go for the regularity conditions and the asymptotic results stated precisely. This is the source for scene 7, not the intuition scenes."},
  {"title":"Statistics for Applications — Maximum Likelihood Estimation","where":"Lecture slides, sessions 4–5",
   "site":"MIT OpenCourseWare 18.650 (Fall 2016)","url":"https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/pages/lecture-slides/",
   "type":"Lecture slides","free":True,"checked":"2026-10-12",
   "why":"Treats the MLE as minimising KL divergence — the view that makes consistency obvious rather than a result to memorise."}),
 "revision": {
  "sheet": L(
    "L(θ) = ∏ f(xᵢ; θ). Same formula as the density; the variable is now θ.",
    "ℓ(θ) = Σ log f(xᵢ; θ). Maximise ℓ, never L.",
    "Score equation: ∂ℓ/∂θ = 0. Then check ∂²ℓ/∂θ² < 0 at the root.",
    "Support depends on θ ⟹ the derivative is useless. Look at the boundary.",
    "Invariance: MLE of g(θ) is g(θ̂). No second derivation.",
    "The MLE is always a function of the sufficient statistic.",
    "Consistent and asymptotically N(θ, 1/(nI(θ))) under regularity — but not generally unbiased.",
    "Exponential rate: λ̂ = n/Σxᵢ = 1/x̄.   Bernoulli: p̂ = x̄.   Poisson: λ̂ = x̄.",
    "N(μ,σ²): μ̂ = x̄, σ̂² = Σ(xᵢ−x̄)²/n — divided by n, not n−1.",
    "U(0,θ): θ̂ = x₍ₙ₎, the sample maximum."),
  "cards": L(
    ["Likelihood, in one sentence","The probability of the data you actually observed, computed under each candidate θ. Not a probability of θ."],
    ["Why take logs?","It turns the product into a sum, and log is strictly increasing so the maximiser is unchanged."],
    ["When does the score equation fail?","When the support depends on θ — U(0,θ) is the standard case. The maximum is then at a boundary."],
    ["MLE of θ², given θ̂","θ̂², by invariance."],
    ["Is the MLE unbiased?","Not in general. Exponential rate: E[λ̂] = nλ/(n−1). Normal variance: E[σ̂²] = (n−1)σ²/n."],
    ["Two properties the MLE does have","Consistency, and asymptotic normality with variance 1/(nI(θ)) — under regularity conditions."],
    ["MLE of σ² for N(μ,σ²), both unknown","Σ(xᵢ−x̄)²/n. Dividing by n−1 gives the unbiased estimator, which is not the MLE."],
    ["Free check on any MLE you derive","It must be a function of the sufficient statistic."])},
 "traps": L(
  "Writing L(θ) and then differentiating with respect to x.",
  "Maximising L instead of ℓ, and drowning in the product rule.",
  "Setting the derivative to zero when the support depends on θ.",
  "Forgetting the second-order check, so a minimum or a stationary point is reported as the MLE.",
  "Re-deriving from scratch for g(θ) when invariance gives it in one line.",
  "Assuming the MLE is unbiased, or that it must equal the UMVUE.",
  "Dividing by n−1 in σ̂² because that is the formula you have written a hundred times."),
}

S = []
def scene(**kw):
    kw.setdefault("id", "s%d" % (len(S)+1))
    S.append(kw); return kw

scene(kind="intuition", title="Which rate makes what you saw most plausible?", mins=4,
 objective="See the likelihood as the density read backwards.",
 body=L(
  "Two bulbs from the same batch failed at 3 hours and at 9 hours. The batch is modelled as exponential with failure rate λ. You do not know λ. You have to name a number.",
  "Try λ = 0.02. Under that rate, failures at 3 and 9 hours would be startlingly early — the model expects a bulb to last about 50 hours. The data you got would be a surprise.",
  "Try λ = 2. Now the model expects failure in about half an hour, and lasting 9 hours would be a freak event. Again the data you got would be a surprise.",
  "Somewhere between those, there is a rate under which the two failures you actually saw are as unsurprising as they can be. That value is the maximum likelihood estimate. The whole method is this one idea, written in algebra.",
  "The formula does not change — it is the same exponential density. What changes is which symbol you treat as fixed. In probability, θ is fixed and x varies. In likelihood, x is fixed at what you observed and θ varies. That inversion is the entire conceptual content of this topic."),
 aside={"h":"The sentence that stops the commonest error",
        "body":"L(θ) is not the probability that θ is correct. It is the probability of your data, computed under θ. It does not integrate to one over θ, and it is not a distribution for θ. That is Bayesian territory and needs a prior."},
 ask={"q":"Why can the best estimate not be a fixed number that ignores which sample you got?",
      "nudge":"What are you choosing θ to do? Think about what the criterion is measured against."})

scene(kind="explore", title="Move the rate and watch the data become plausible", mins=5,
 objective="Locate the peak yourself before being shown the formula for it.",
 viz={"type":"exp-likelihood","n":2,"sumx":12.0},
 body=L(
  "The curve is L(λ) = λⁿ e^(−λΣxᵢ) for an exponential sample — the likelihood of the data you actually hold, at every candidate rate.",
  "Below it is ℓ(λ) = n·log λ − λ·Σxᵢ. Same peak, in the same place, because log is strictly increasing. It is far easier to differentiate.",
  "Start with n = 2 and Σx = 12, which is the two bulbs. Drag λ and find the top by eye. Then raise n and watch what happens to the width of the curve, not just its position."),
 ask={"q":"Double every observation, so Σx goes from 12 to 24 with n unchanged. Which way does the peak move, and why does that make sense physically?",
      "nudge":"Longer lifetimes mean what about the failure rate?"})

scene(kind="theory", title="The three lines that do all the work", mins=6,
 objective="Write the standard derivation in its canonical order.",
 blocks=L(
  {"t":"def","h":"Likelihood","body":"For an iid sample x₁,…,xₙ from f(x; θ), the likelihood is L(θ) = ∏ᵢ f(xᵢ; θ), viewed as a function of θ with the data held fixed."},
  {"t":"formula","h":"Step 1 — take logs","body":"ℓ(θ) = log L(θ) = Σᵢ log f(xᵢ; θ)"},
  {"t":"formula","h":"Step 2 — the score equation","body":"∂ℓ/∂θ = 0,   solved for θ"},
  {"t":"formula","h":"Step 3 — confirm it is a maximum","body":"∂²ℓ/∂θ² < 0  evaluated at the root"},
  {"t":"assume","h":"The condition that decides whether any of this applies","body":"The support of f must not depend on θ. If the set of possible x values moves when θ moves, ℓ has a jump and the derivative never reaches zero at the maximum. Scene 9 shows exactly that happening."},
  {"t":"note","h":"Why step 3 is not optional","body":"∂ℓ/∂θ = 0 finds stationary points. For the standard one-parameter families the root is the maximum and the check is one line, but examiners do set items where the stationary point is a minimum or where the maximum is at an endpoint. Writing the second derivative costs you five seconds."},
  {"t":"trap","h":"The error that costs a mark without feeling like an error","body":"Differentiating with respect to x instead of θ. By the time you have written ℓ(θ) your variable is θ. The xᵢ are now constants."}))

scene(kind="worked", title="Worked in full — the exponential rate", mins=5,
 objective="See the canonical derivation with reasoning at every step.",
 problem="X₁,…,Xₙ are iid Exponential with rate λ, so f(x; λ) = λe^(−λx) for x > 0. Find the MLE of λ.",
 steps=L(
  {"say":"Write the likelihood as the product of densities.","math":"L(λ) = ∏ᵢ λe^(−λxᵢ) = λⁿ e^(−λΣxᵢ)",
   "why":"The product collapses because each factor carries one λ and the exponents add. Already you can see the likelihood depends on the data only through Σxᵢ — that is the sufficient statistic announcing itself."},
  {"say":"Take logs.","math":"ℓ(λ) = n·log λ − λ·Σxᵢ",
   "why":"A sum instead of a product. Nothing is lost: log is strictly increasing, so whatever maximises ℓ maximises L."},
  {"say":"Differentiate with respect to λ and set to zero.","math":"dℓ/dλ = n/λ − Σxᵢ = 0",
   "why":"The xᵢ are constants here. The only variable is λ."},
  {"say":"Solve.","math":"λ̂ = n / Σxᵢ = 1 / x̄",
   "why":"The reciprocal of the sample mean. Sensible: the exponential mean is 1/λ, so estimating the mean by x̄ and inverting gives the same answer — which is invariance, arriving early."},
  {"say":"Check it is a maximum.","math":"d²ℓ/dλ² = −n/λ² < 0 for all λ > 0",
   "why":"Negative everywhere, so ℓ is strictly concave and the stationary point is the global maximum. One line, done."},
  {"say":"Put the numbers in.","math":"n = 2, Σxᵢ = 12  ⟹  λ̂ = 2/12 = 0.167 per hour",
   "why":"This is the peak you found by dragging the slider in scene 2. The algebra and the picture agree."}),
 after="Notice what the derivation never needed: any claim that λ̂ is unbiased, or best, or anything else. Maximum likelihood is a recipe for producing an estimator. Whether that estimator is any good is a separate question, and scene 8 shows it is not always.")

scene(kind="recall", title="Pause and recall", mins=2,
 objective="Retrieve before reading on — this is where the retention comes from.",
 intro="Answer each in your head, then reveal. Retrieving an answer wrongly and correcting it beats reading the right answer twice.",
 items=L(
  {"q":"In L(θ), which symbol varies and which is held fixed?","a":"θ varies. The data x₁,…,xₙ are fixed at the values you observed."},
  {"q":"Why maximise ℓ rather than L?","a":"log turns the product into a sum, and because log is strictly increasing the maximiser is unchanged."},
  {"q":"What is the one condition that decides whether the score equation is the right tool at all?","a":"The support of f must not depend on θ."},
  {"q":"Write the MLE of the exponential rate from memory.","a":"λ̂ = n/Σxᵢ = 1/x̄."}))

scene(kind="completion", title="Your turn, with the scaffolding partly removed — Bernoulli", mins=6,
 objective="Supply the steps yourself rather than following them.",
 problem="X₁,…,Xₙ are iid Bernoulli(p), so f(x; p) = p^x (1−p)^(1−x) for x ∈ {0,1}. Let k = Σxᵢ be the number of successes. Find the MLE of p.",
 steps=L(
  {"say":"The likelihood.","math":"L(p) = p^k (1−p)^(n−k)","why":"Each success contributes p, each failure contributes (1−p)."},
  {"say":"Take logs.","blank":{"prompt":"Write ℓ(p).","answer":"k log p + (n−k) log(1−p)",
    "accept":["k log p + (n-k) log(1-p)","klogp+(n-k)log(1-p)","k ln p + (n-k) ln(1-p)"],
    "hint":"log of a product is a sum of logs; log of a power brings the exponent down."},
   "why":"Two terms, one for the successes and one for the failures."},
  {"say":"Differentiate with respect to p and set to zero.","blank":{"prompt":"Write dℓ/dp = 0.","answer":"k/p − (n−k)/(1−p) = 0",
    "accept":["k/p - (n-k)/(1-p) = 0","k/p-(n-k)/(1-p)=0","k/p = (n-k)/(1-p)"],
    "hint":"d/dp log(1−p) = −1/(1−p). Mind that minus sign — it is the single commonest slip here."},
   "why":"The chain rule on the second term supplies the minus sign."},
  {"say":"Solve for p.","blank":{"prompt":"Write p̂.","answer":"k/n","accept":["k/n","x̄","xbar","k / n","the sample proportion"],
    "hint":"Cross-multiply: k(1−p) = (n−k)p. Expand and the kp terms cancel."},
   "why":"The sample proportion — which is also x̄, so the Bernoulli MLE is the sample mean."},
  {"say":"Check.","math":"d²ℓ/dp² = −k/p² − (n−k)/(1−p)² < 0","why":"Negative for every p in (0,1), so the stationary point is the maximum."}),
 after="Two derivations, identical shape: product → log → differentiate → solve → check. The shape is what you are memorising, not the individual answers.")

scene(kind="theory", title="The four properties the exam actually tests", mins=7,
 objective="Hold the properties with their conditions attached, because the conditions are what the items test.",
 blocks=L(
  {"t":"def","h":"1. Invariance","body":"If θ̂ is the MLE of θ, then g(θ̂) is the MLE of g(θ), for any function g. No regularity conditions, no second derivation. If λ̂ = 1/x̄ then the MLE of the mean 1/λ is x̄, and the MLE of λ² is 1/x̄²."},
  {"t":"def","h":"2. It is a function of the sufficient statistic","body":"The factorisation theorem writes L(θ) = g(T(x); θ)·h(x). Maximising over θ only ever touches g, so the maximiser depends on the data only through T. Use this as a free check: if your answer is not a function of the sufficient statistic, you have made an algebra mistake."},
  {"t":"def","h":"3. Consistency and asymptotic normality","body":"Under regularity conditions, θ̂ →ᵖ θ, and √n(θ̂ − θ) →ᵈ N(0, 1/I(θ)) — equivalently θ̂ is approximately N(θ, 1/(nI(θ))) for large n. So the MLE attains the Cramér–Rao bound asymptotically, which is the precise sense in which it is 'efficient'."},
  {"t":"assume","h":"Which regularity conditions","body":"The support does not depend on θ; θ is interior to the parameter space; ℓ is twice differentiable; differentiation and integration can be interchanged; the information I(θ) is finite and positive. U(0,θ) violates the first, which is why the usual asymptotics do not apply there."},
  {"t":"trap","h":"4. It is NOT generally unbiased","body":"This is the property examiners most often test by implication. Maximum likelihood optimises plausibility of the data, not expected value of the estimator. For N(μ,σ²) the MLE σ̂² = Σ(xᵢ−x̄)²/n has E[σ̂²] = (n−1)σ²/n — biased low. For the exponential rate, E[λ̂] = nλ/(n−1) — biased high. Both biases vanish as n grows, which is consistency, not unbiasedness."},
  {"t":"note","h":"MLE versus UMVUE","body":"They coincide often enough to be dangerous. They are different objects: the MLE maximises the likelihood, the UMVUE minimises variance among unbiased estimators. When a question offers both as options, decide which criterion it named."}))

scene(kind="explore", title="Watch the MLE be biased, then watch the bias die", mins=5,
 objective="Turn 'the MLE is not unbiased' from a sentence into something you have seen.",
 viz={"type":"mle-sampling","lam":0.5,"n":3},
 body=L(
  "This is the exact sampling distribution of λ̂ = n/ΣX for an exponential sample — not a simulation. ΣX is Gamma(n, λ), so λ̂ has a known density and the curve is drawn from it.",
  "The solid line is the true λ. The dashed line is E[λ̂] = nλ/(n−1). At n = 2 the estimator is biased by a full 100%: it expects to return twice the truth. At n = 3 it is 50% high. At n = 20, about 5%.",
  "Notice two things moving at once as you raise n: the dashed line slides toward the solid one — that is the bias dying — and the whole distribution narrows — that is the variance dying. Both together are consistency.",
  "Also notice the shape. Even at moderate n the distribution is visibly right-skewed, not the symmetric normal the asymptotic theory promises. 'Asymptotically normal' means eventually, and the exam has asked which sample size makes that approximation reasonable."),
 ask={"q":"The bias is nλ/(n−1) − λ = λ/(n−1). An estimator whose bias goes to zero is called asymptotically unbiased. Is every consistent estimator asymptotically unbiased, or are those two different claims?",
      "nudge":"Consistency is about convergence in probability. Bias is about an expectation. Can an expectation be dragged around by a vanishingly rare but enormous value?"})

scene(kind="explore", title="Where calculus fails — the uniform", mins=5,
 objective="Recognise the boundary case on sight, because the derivative will not warn you.",
 viz={"type":"unif-likelihood","n":5,"xmax":4.2},
 body=L(
  "X₁,…,Xₙ are iid U(0, θ). The density is 1/θ on [0, θ] and zero outside, so the likelihood is L(θ) = θ^(−n), but only for θ ≥ x₍ₙ₎, the largest observation. For any smaller θ at least one observed value would have been impossible, so L(θ) = 0.",
  "That gives the shape on screen: flat zero, a vertical cliff at x₍ₙ₎, then a curve decreasing for the rest of its life.",
  "Set the derivative to zero and you get −n·θ^(−n−1) = 0, which has no solution. The derivative is negative everywhere the likelihood is positive. Nothing is wrong with your algebra — the method simply does not apply, because the support depends on θ.",
  "The maximum is at the cliff edge: θ̂ = x₍ₙ₎, the sample maximum. Read it off the picture, not off a derivative.",
  "This estimator is biased low — it can never exceed the true θ, and almost surely falls short, with E[θ̂] = nθ/(n+1). The unbiased correction is (n+1)/n · x₍ₙ₎, which is not the MLE."),
 ask={"q":"Drag θ below the cliff. Why is the likelihood exactly zero there rather than merely small?",
      "nudge":"What would θ < x₍ₙ₎ say about the value you actually observed?"})

scene(kind="guided", title="Now without the steps — Poisson", mins=6,
 objective="Select the method yourself. The hints are there, and using them is recorded.",
 problem="X₁,…,Xₙ are iid Poisson(λ), so P(X = x) = e^(−λ) λ^x / x! for x = 0,1,2,…  A sample of n = 8 gives Σxᵢ = 20. Find the MLE of λ, and then the MLE of P(X = 0).",
 hints=L(
  "Direction — before any algebra, ask which quantity you are choosing. You are choosing λ to make Σxᵢ = 20 as plausible as it can be. Write the likelihood as a product over i and see what survives.",
  "Method — the support {0,1,2,…} does not depend on λ, so the score equation is the right tool. Take logs: the x! becomes an additive constant that does not involve λ, so it will vanish on differentiation. Do not waste time on it.",
  "Next step — ℓ(λ) = −nλ + (Σxᵢ)·log λ − Σ log(xᵢ!). Differentiate with respect to λ, set to zero, and solve. Then for the second part do not start again: use invariance."),
 solution=L(
  {"say":"Likelihood.","math":"L(λ) = ∏ e^(−λ) λ^(xᵢ)/xᵢ! = e^(−nλ) λ^(Σxᵢ) / ∏xᵢ!"},
  {"say":"Log-likelihood, dropping the constant.","math":"ℓ(λ) = −nλ + (Σxᵢ) log λ − Σ log(xᵢ!)"},
  {"say":"Score equation.","math":"dℓ/dλ = −n + (Σxᵢ)/λ = 0"},
  {"say":"Solve.","math":"λ̂ = Σxᵢ / n = x̄ = 20/8 = 2.5"},
  {"say":"Check.","math":"d²ℓ/dλ² = −(Σxᵢ)/λ² < 0  ✓"},
  {"say":"Second part, by invariance.","math":"P(X=0) = e^(−λ), so its MLE is e^(−λ̂) = e^(−2.5) = 0.0821"}),
 answer="λ̂ = 2.5 and the MLE of P(X=0) is e^(−2.5) ≈ 0.0821",
 check="The question asked for two quantities. Reporting only λ̂ = 2.5 is the single likeliest way to lose this mark — it is right working, wrong quantity.")

scene(kind="trapcheck", title="Six statements — verdict on each before you look", mins=5,
 objective="Practise the per-statement discipline that multi-statement items demand.",
 intro="Give every statement a true or false verdict first. Multi-statement items in the real paper are scored on the whole set, so a verdict you skipped is a mark you gambled.",
 items=L(
  {"claim":"If θ̂ is the MLE of θ, then θ̂² is the MLE of θ².","tf":True,
   "why":"Invariance, with no conditions attached. This one is true and is often placed among false statements to catch people who distrust it."},
  {"claim":"The MLE is always unbiased.","tf":False,
   "why":"False, and the commonest trap in the topic. E[σ̂²] = (n−1)σ²/n for the normal; E[λ̂] = nλ/(n−1) for the exponential rate."},
  {"claim":"The MLE always exists and is unique.","tf":False,
   "why":"False. The likelihood can be maximised on a set rather than a point — U(θ−½, θ+½) gives an interval of maximisers — and for some models no maximum exists in the parameter space."},
  {"claim":"The MLE is a function of the sufficient statistic.","tf":True,
   "why":"True, straight from the factorisation theorem: maximising over θ touches only the factor that depends on the data through T."},
  {"claim":"For U(0,θ), the MLE is obtained by setting dℓ/dθ = 0.","tf":False,
   "why":"False. The support depends on θ, the derivative never vanishes, and the maximum is at the boundary: θ̂ = x₍ₙ₎."},
  {"claim":"Under regularity conditions the MLE attains the Cramér–Rao lower bound asymptotically.","tf":True,
   "why":"True — that is exactly the content of √n(θ̂−θ) →ᵈ N(0, 1/I(θ)). Note 'asymptotically': for finite n the MLE need not attain the bound at all."}))

scene(kind="guided", title="Transfer — a case you have not been shown", mins=6,
 objective="Apply the method to a two-parameter model with no worked template in front of you.",
 problem="X₁,…,Xₙ are iid N(μ, σ²) with BOTH parameters unknown. Find the MLEs of μ and σ².",
 hints=L(
  "Direction — two unknowns means two score equations. Write ℓ(μ, σ²) and take a partial derivative with respect to each, not a total derivative.",
  "Method — differentiate with respect to μ first. The σ² terms are constants for that derivative and the answer drops out in one line. Substitute that result before differentiating with respect to σ².",
  "Next step — ℓ = −(n/2)log(2π) − (n/2)log σ² − (1/(2σ²))Σ(xᵢ−μ)². Differentiating in σ² is easier if you treat σ² as a single symbol, say v, rather than squaring and unsquaring."),
 solution=L(
  {"say":"Log-likelihood.","math":"ℓ(μ, v) = −(n/2)log(2πv) − (1/(2v))·Σ(xᵢ−μ)²,  writing v for σ²"},
  {"say":"Differentiate in μ.","math":"∂ℓ/∂μ = (1/v)·Σ(xᵢ−μ) = 0  ⟹  μ̂ = x̄"},
  {"say":"Substitute and differentiate in v.","math":"∂ℓ/∂v = −n/(2v) + (1/(2v²))·Σ(xᵢ−x̄)² = 0"},
  {"say":"Solve.","math":"v̂ = σ̂² = Σ(xᵢ−x̄)² / n"}),
 answer="μ̂ = x̄ and σ̂² = Σ(xᵢ−x̄)²/n",
 check="Divided by n, not by n−1. The n−1 version is the unbiased estimator s², and it is not the MLE. E[σ̂²] = (n−1)σ²/n, so the MLE understates the variance — by 10% at n = 10. If you wrote n−1 here, that is the same reflex that produced the degrees-of-freedom errors in your error log, and it is worth a line in it now.")

scene(kind="summary", title="What you should now be able to do unaided", mins=3,
 objective="Close the loop before the test.",
 body=L(
  "Write L(θ) for any standard family, take logs, solve the score equation, and confirm the sign of the second derivative.",
  "Spot a support that depends on θ and go straight to the boundary instead of differentiating.",
  "Produce the MLE of any function of θ in one line by invariance.",
  "State, with its condition attached, each of: consistency, asymptotic normality, the link to sufficiency, and the absence of unbiasedness.",
  "The mastery test is ten questions you have not seen, mixing all of these. Hints are off. The pass is 80% overall with 70% floors on the numerical and multi-statement items."))

scene(kind="quiz", title="Mastery test", mins=12,
 objective="Demonstrate it independently, on unseen questions.",
 setId="inference_t4_mastery")

lesson["scenes"] = S

# ---------------- practice bank (scene-linked, browsable) ----------------
def q(i, fmt, stem, options, ans, expl, **kw):
    d = {"id": "mle-p-%02d" % i, "format": fmt, "topic": "inference-t4", "stem": stem,
         "options": options, "answer": ans, "explanation": expl}
    d.update(kw); return d

practice = [
 q(1,"single","The likelihood function L(θ) for a fixed observed sample is best described as:",
   ["A probability distribution over θ that integrates to 1",
    "The probability of the observed data, computed as a function of θ",
    "The posterior density of θ given the data",
    "The joint density of the sample, as a function of x"],
   "B","It is the joint density read as a function of θ with the data held fixed. It does not integrate to 1 over θ and is not a distribution for θ — treating it as one is the Bayesian posterior, which also needs a prior."),
 q(2,"numeric","A sample of n = 10 from Bernoulli(p) gives Σxᵢ = 7. Find the MLE of p, and then the MLE of the odds p/(1−p).",
   [],"p̂ = 0.7; odds MLE = 0.7/0.3 = 2.333",
   "p̂ = k/n = 7/10 = 0.7. The odds are a function of p, so invariance gives the MLE directly: 0.7/0.3 = 7/3 ≈ 2.333. No second derivation is needed.",
   check="The question asked for two things. Check you reported the odds and not just p̂."),
 q(3,"single","For X₁,…,Xₙ iid U(0,θ), the MLE of θ is:",
   ["x̄", "2x̄", "x₍ₙ₎, the sample maximum", "(n+1)/n · x₍ₙ₎"],
   "C","The support depends on θ, so the derivative never vanishes. L(θ) = θ^(−n) for θ ≥ x₍ₙ₎ and 0 below, so the maximum sits at the boundary θ̂ = x₍ₙ₎. Option D is the unbiased correction, not the MLE. Option B is the method-of-moments estimator."),
 q(4,"numeric","X₁,…,X₅ iid Exponential(λ) with Σxᵢ = 20. Give the MLE of λ and the MLE of the mean lifetime.",
   [],"λ̂ = 0.25; mean lifetime MLE = 4",
   "λ̂ = n/Σxᵢ = 5/20 = 0.25. The mean is 1/λ, so by invariance its MLE is 1/0.25 = 4 — which is just x̄.",
   check="Rate and mean are reciprocals. Reporting 4 when the question asked for λ is the classic wrong-quantity slip here."),
 q(5,"multi","X₁,…,Xₙ are iid N(μ, σ²) with both unknown. Consider the following statements.",
   ["A and C only","A and B only","B and D only","A, C and D only"],"A",
   "A is true: μ̂ = x̄. B is false: the MLE divides by n, so σ̂² = Σ(xᵢ−x̄)²/n. C is true: E[σ̂²] = (n−1)σ²/n < σ². D is false — the bias vanishes as n → ∞, so it is asymptotically unbiased.",
   statements=["The MLE of μ is x̄.",
               "The MLE of σ² is Σ(xᵢ−x̄)²/(n−1).",
               "The MLE of σ² is biased downward for every finite n.",
               "The bias of the MLE of σ² persists as n → ∞."],
   verdicts={"A":{"tf":True,"why":"∂ℓ/∂μ = 0 gives μ̂ = x̄ immediately, whatever σ² is."},
             "B":{"tf":False,"why":"That is s², the unbiased estimator. The MLE divides by n."},
             "C":{"tf":True,"why":"E[σ̂²] = (n−1)σ²/n, which is strictly below σ² for every finite n."},
             "D":{"tf":False,"why":"(n−1)/n → 1, so the bias dies. Asymptotically unbiased, and consistent."}}),
 q(6,"single","Which condition, if violated, makes the score equation dℓ/dθ = 0 the wrong tool for finding an MLE?",
   ["The sample must be iid","The support of the density must not depend on θ",
    "The parameter must be scalar","The density must be continuous"],
   "B","A support that moves with θ puts a discontinuity in L at the boundary, and the maximum sits on it where the derivative is not zero. U(0,θ) is the standard example. The other three are neither necessary nor the operative condition."),
 q(7,"numeric","A Poisson sample of size n = 12 has Σxᵢ = 36. Give the MLE of λ and the MLE of P(X = 0).",
   [],"λ̂ = 3; MLE of P(X=0) = e^(−3) ≈ 0.0498",
   "λ̂ = x̄ = 36/12 = 3. P(X=0) = e^(−λ) is a function of λ, so by invariance its MLE is e^(−3) ≈ 0.0498.",
   check="e^(−3), not 3. Confirm which of the two the question asked for before you write the final line."),
 q(8,"multi","Consider the maximum likelihood estimator θ̂ under the usual regularity conditions.",
   ["A, B and D only","A and C only","B, C and D only","All four"],"A",
   "A is true (invariance holds with no conditions). B is true (factorisation). C is false — the MLE is not generally unbiased, let alone UMVUE. D is true — that is asymptotic efficiency.",
   statements=["g(θ̂) is the MLE of g(θ) for any function g.",
               "θ̂ is a function of the sufficient statistic.",
               "θ̂ is the UMVUE of θ.",
               "θ̂ is asymptotically normal with variance 1/(nI(θ))."],
   verdicts={"A":{"tf":True,"why":"Invariance, unconditional."},
             "B":{"tf":True,"why":"L factorises through T, so the maximiser depends on the data only through T."},
             "C":{"tf":False,"why":"Different criteria. The MLE is often biased, and the UMVUE minimises variance among unbiased estimators."},
             "D":{"tf":True,"why":"√n(θ̂−θ) →ᵈ N(0, 1/I(θ)) under regularity — the CRLB attained in the limit."}}),
 q(9,"numeric","For an exponential sample with n = 4, the MLE of the rate is λ̂ = n/Σxᵢ. Its exact expectation is E[λ̂] = nλ/(n−1). By what percentage does it overstate λ on average at n = 4, and what is that property called?",
   [],"33.3% high; it is biased but asymptotically unbiased (and consistent)",
   "E[λ̂] = 4λ/3 = 1.333λ, so a 33.3% overstatement on average. The bias is λ/(n−1), which tends to zero: asymptotically unbiased, and combined with vanishing variance, consistent. It is not unbiased at any finite n.",
   check="A percentage and a name were both asked for. One without the other is half an answer."),
 q(10,"single","The MLE of θ for a sample from U(0,θ) is x₍ₙ₎, with E[x₍ₙ₎] = nθ/(n+1). Which statement is correct?",
   ["θ̂ is unbiased","θ̂ overstates θ on average","θ̂ understates θ on average and is consistent",
    "θ̂ is the UMVUE of θ"],
   "C","nθ/(n+1) < θ, so it understates. It must: the sample maximum can never exceed the true θ. The bias θ/(n+1) → 0 and the variance → 0, so the estimator is consistent. The UMVUE here is (n+1)/n · x₍ₙ₎."),
 q(11,"match","Match each model in List I with its maximum likelihood estimator in List II.",
   ["A-3, B-1, C-4, D-2","A-1, B-3, C-2, D-4","A-3, B-4, C-1, D-2","A-2, B-1, C-4, D-3"],"A",
   "Exponential rate inverts the mean: n/Σxᵢ. Bernoulli gives the sample proportion x̄. U(0,θ) is the boundary case x₍ₙ₎. The normal variance with μ unknown divides by n.",
   pairs=[["A. Exponential(λ), estimate λ","1. x̄"],
          ["B. Bernoulli(p), estimate p","2. Σ(xᵢ−x̄)²/n"],
          ["C. U(0,θ), estimate θ","3. n/Σxᵢ"],
          ["D. N(μ,σ²) both unknown, estimate σ²","4. x₍ₙ₎"]]),
 q(12,"order","Arrange the steps of a standard MLE derivation in the order they should be carried out.",
   ["C, A, D, B","A, C, D, B","C, D, A, B","A, D, C, B"],"A",
   "Write the likelihood as a product, take logs to turn it into a sum, solve the score equation, then confirm the second derivative is negative. The second-order check comes last and is the step most often skipped.",
   items=["A. Take logarithms to obtain ℓ(θ)",
          "B. Verify ∂²ℓ/∂θ² < 0 at the root",
          "C. Write L(θ) as a product of densities",
          "D. Solve ∂ℓ/∂θ = 0"]),
]

# ---------------- mastery bank (unseen, excluded from browsing and mocks) ----------------
def m(i, fmt, stem, options, ans, expl, **kw):
    d = {"id": "mle-m-%02d" % i, "format": fmt, "topic": "inference-t4", "stem": stem,
         "options": options, "answer": ans, "explanation": expl}
    d.update(kw); return d

mastery = [
 m(1,"single","X₁,…,Xₙ are iid with density f(x;θ) = θx^(θ−1) on 0 < x < 1, θ > 0. The MLE of θ is:",
   ["−n / Σ log xᵢ","n / Σ log xᵢ","−Σ log xᵢ / n","x̄ / (1 − x̄)"],
   "A","ℓ(θ) = n log θ + (θ−1)Σ log xᵢ. Then dℓ/dθ = n/θ + Σ log xᵢ = 0, so θ̂ = −n/Σ log xᵢ. The minus sign is required and is what makes θ̂ positive, since every log xᵢ < 0 on (0,1). Option B has the wrong sign and would return a negative estimate."),
 m(2,"numeric","A geometric sample (number of trials to the first success, support 1,2,3,…) of size n = 6 has Σxᵢ = 24. Give the MLE of p and the MLE of the expected number of trials.",
   ["p̂ = 0.25 and the MLE of E[X] is 4","p̂ = 4 and the MLE of E[X] is 0.25",
    "p̂ = 0.25 and the MLE of E[X] is 0.75","p̂ = 0.20 and the MLE of E[X] is 5"],"A",
   "P(X=x) = (1−p)^(x−1) p, so ℓ(p) = n log p + (Σxᵢ − n) log(1−p). Setting the derivative to zero gives p̂ = n/Σxᵢ = 6/24 = 0.25. E[X] = 1/p, so by invariance its MLE is 1/0.25 = 4, which is x̄.",
   check="p̂ and 1/p̂ are both plausible-looking answers. Confirm which the question asked for."),
 m(3,"multi","X₁,…,Xₙ are iid U(0,θ) and θ̂ = x₍ₙ₎ is the MLE.",
   ["A, B and D only","A and C only","B and C only","A, B and C only"],"A",
   "A is true — the derivative never vanishes, so the usual method does not locate the maximum. B is true: x₍ₙ₎ ≤ θ always, and E[θ̂] = nθ/(n+1) < θ. C is false — x₍ₙ₎ is the complete sufficient statistic and the MLE is a function of it. D is true: scaling by (n+1)/n removes the bias.",
   statements=["The score equation dℓ/dθ = 0 has no solution for this model.",
               "θ̂ understates θ with probability 1.",
               "θ̂ is not a function of the sufficient statistic.",
               "(n+1)/n · θ̂ is unbiased for θ."],
   verdicts={"A":{"tf":True,"why":"dℓ/dθ = −n/θ < 0 wherever L > 0. It is never zero."},
             "B":{"tf":True,"why":"The sample maximum cannot exceed θ, and equals it with probability 0."},
             "C":{"tf":False,"why":"x₍ₙ₎ IS the sufficient statistic here, so the MLE is trivially a function of it."},
             "D":{"tf":True,"why":"E[x₍ₙ₎] = nθ/(n+1), so multiplying by (n+1)/n gives θ exactly."}}),
 m(4,"numeric","A sample of n = 16 from N(μ, σ²) with both unknown gives Σxᵢ = 80 and Σ(xᵢ − x̄)² = 60. Give the MLE of σ², the unbiased estimator s², and say which is larger.",
   ["σ̂² = 3.75, s² = 4; s² is larger","σ̂² = 4, s² = 3.75; σ̂² is larger",
    "σ̂² = 3.75, s² = 3.75; they are equal","σ̂² = 5, s² = 4; σ̂² is larger"],"A",
   "The MLE divides by n: σ̂² = 60/16 = 3.75. The unbiased estimator divides by n−1: s² = 60/15 = 4. Since n−1 < n, s² is always the larger of the two, and the MLE is biased low by a factor (n−1)/n = 15/16.",
   check="Two numbers and a comparison were asked for. The n versus n−1 choice is the whole question — write which denominator you used."),
 m(5,"single","If θ̂ is the MLE of θ and the parameter of interest is ψ = e^(−2θ), then the MLE of ψ is:",
   ["e^(−2θ̂)","−2e^(−2θ̂)","E[e^(−2θ̂)]","It cannot be obtained without a fresh derivation"],
   "A","Invariance: the MLE of any function g(θ) is g(θ̂), so ψ̂ = e^(−2θ̂) directly. Option B is the derivative, not the estimator. Option C confuses the MLE with an expectation — and note e^(−2θ̂) is generally a biased estimator of e^(−2θ), which is consistent with the MLE not being unbiased."),
 m(6,"multi","Consider the likelihood function L(θ) for a fixed observed sample.",
   ["B and D only","A and C only","A, B and D only","B, C and D only"],"A",
   "A is false — L is a function of θ but is not a probability distribution over θ and need not integrate to 1. B is true. C is false: the maximiser is unchanged by taking logs, which is precisely why we do it. D is true, by the factorisation theorem.",
   statements=["L(θ) is a probability density function of θ and integrates to 1 over the parameter space.",
               "L(θ) is computed from the data actually observed, held fixed.",
               "Maximising log L(θ) can give a different maximiser from maximising L(θ).",
               "L(θ) depends on the data only through a sufficient statistic, when one exists."],
   verdicts={"A":{"tf":False,"why":"It is not a distribution for θ. Treating it as one is the single commonest misconception in the topic."},
             "B":{"tf":True,"why":"That is the definition — the data are fixed and θ varies."},
             "C":{"tf":False,"why":"log is strictly increasing, so the maximiser is identical."},
             "D":{"tf":True,"why":"L(θ) = g(T(x);θ)·h(x), and h does not involve θ."}}),
 m(7,"numeric","X₁,…,Xₙ are iid Exponential(λ). Fisher information for a single observation is I(λ) = 1/λ². For n = 25 and λ̂ = 0.4, the approximate standard error of λ̂ from the asymptotic distribution is:",
   ["0.08","0.016","0.40","0.20"],"A",
   "Asymptotically λ̂ ~ N(λ, 1/(nI(λ))). Here 1/(nI(λ)) = λ²/n, so the SE is λ/√n, estimated as λ̂/√n = 0.4/5 = 0.08.",
   check="√n = 5, not 25. Taking the root of n is the step most often dropped here."),
 m(8,"single","Which of the following is NOT guaranteed for a maximum likelihood estimator, even under the usual regularity conditions?",
   ["Consistency","Asymptotic normality","Unbiasedness for every finite n","Invariance under reparametrisation"],
   "C","Consistency, asymptotic normality and invariance all hold. Unbiasedness does not: the normal variance MLE is biased low and the exponential rate MLE is biased high, at every finite n. Regularity conditions buy asymptotic behaviour, not finite-sample unbiasedness."),
 m(9,"numeric","A sample of size n = 3 from U(0,θ) gives observations 1.2, 3.8 and 2.5. The MLE of θ, the MLE of θ², and E[θ̂] are:",
   ["3.8,  14.44,  3θ/4","3.8,  14.44,  4θ/3","2.5,  6.25,  3θ/4","3.8,  7.60,  θ"],"A",
   "θ̂ = x₍ₙ₎ = 3.8, the sample maximum. By invariance the MLE of θ² is 3.8² = 14.44. And E[x₍ₙ₎] = nθ/(n+1) = 3θ/4, which understates θ — the sample maximum can never exceed it.",
   check="Three quantities asked, and the third is in terms of θ, not a number. Answering only θ̂ = 3.8 is the wrong-quantity error in its purest form."),
 m(10,"order","A question gives a density whose support is 0 < x < θ. Arrange the steps you should take, in order.",
   ["B, D, A, C","A, B, D, C","B, A, D, C","D, B, A, C"],"A",
   "Check the support first — that single check decides the whole method. Seeing it depends on θ, abandon the derivative, locate the maximum on the boundary at x₍ₙ₎, and only then answer any follow-up about bias or a function of θ. Starting with the derivative wastes the time the check would have saved.",
   items=["A. Identify the maximum at the boundary θ̂ = x₍ₙ₎",
          "B. Check whether the support depends on θ",
          "C. Address any follow-up on bias or on a function of θ",
          "D. Conclude the score equation does not apply"]),
]

for d, name, label, src in [
    (practice, "inference_t4_practice", "MLE — linked practice", "variant"),
    (mastery, "inference_t4_mastery", "MLE — mastery test (unseen)", "mastery")]:
    body = {"moduleId":"inference","source":src,"label":label,"topicId":"inference-t4",
            "count":len(d),"items":d}
    with open(os.path.join(OUT, name + ".json"), "w") as f:
        json.dump(body, f, ensure_ascii=False, indent=1)
    print(name, len(d), "items")

with open(os.path.join(OUT, "lesson_mle.json"), "w") as f:
    json.dump(lesson, f, ensure_ascii=False, indent=1)

print("lesson scenes:", len(S), "->", ", ".join(x["kind"] for x in S))
print("bytes:", os.path.getsize(os.path.join(OUT, "lesson_mle.json")))
