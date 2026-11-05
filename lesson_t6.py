# lessons/inferencet6 — Cramer-Rao bound and Fisher information  (depth: Apply)
import json, os
OUT = "/home/claude/w1/seed"
L = lambda *p: list(p)

lesson = {
 "id":"inferencet6","moduleId":"inference","topicId":"inference-t6",
 "title":"The Cramér–Rao Bound and Fisher Information",
 "breadcrumb":"Statistical Inference → Point Estimation → How good can an estimator be",
 "engine":"B",
 "engineName":"Estimation and inference — curvature of the log-likelihood, and the variance floor it sets",
 "estMin":45,"version":"1.0","status":"approved",
 "provenance":"Theory, worked examples and practice authored for this platform against the UGC NET Statistics syllabus. Previous-year questions are stored separately and carry their exam cycle.",
 "objectives":L(
   "Compute Fisher information by either formula, E[(∂ℓ/∂θ)²] or −E[∂²ℓ/∂θ²], and scale it to a sample as nI₁(θ).",
   "Write the Cramér–Rao bound for an unbiased estimator of θ, and for a function g(θ) with [g′(θ)]² on top.",
   "Check the regularity conditions before quoting the bound, and name the family where they fail.",
   "Decide whether a given estimator attains the bound, using the linear-score condition rather than guesswork.",
   "Compute efficiency and relative efficiency, and state what the bound says about the MLE as n grows."),
 "prereq":L(
   {"id":"p1","name":"Log-likelihood and the score","why":"Everything here is built on ℓ(θ) and its first two derivatives. If writing ℓ is still slow, do the MLE topic first."},
   {"id":"p2","name":"Variance of a sample mean","why":"Nearly every attainment check ends by comparing a bound with Var(X̄) = Var(X)/n."},
   {"id":"p3","name":"Rao–Blackwell and Lehmann–Scheffé","why":"The bound and the UMVUE answer different questions. Scene 8 shows a case where the best unbiased estimator still does not reach the floor."}),
 "mastery":{"minQ":10,"pass":80,"fmtMin":{"numeric":70,"multi":70},"noHints":True,"retestDays":7,
   "note":"Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints."},
 "refs":L(
  {"title":"Fisher information and the Cramér–Rao bound","where":"Lecture 15",
   "site":"Stanford STATS 200 (Autumn 2016)","url":"https://web.stanford.edu/class/archive/stats/stats200/stats200.1172/Lecture15.pdf",
   "type":"Lecture notes","free":True,"checked":"2026-10-12",
   "why":"The definition, the theorem with a proof, efficiency, and the MLE's asymptotic normality in eight pages, with Gamma examples. Read it after scene 7. One gap to know about: it refers to 'certain regularity conditions' without listing them — scene 3 here spells them out, so the two complement each other."},
  {"title":"Mathematical Statistics — Unbiased Estimation and Risk Inequalities","where":"Lecture note 13",
   "site":"MIT OpenCourseWare 18.655 (Spring 2016)","url":"https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/pages/lecture-notes/",
   "type":"Lecture notes","free":True,"checked":"2026-10-12",
   "why":"Places the bound inside the risk framework alongside Rao–Blackwell, which is where it belongs. Useful at scene 8, when you want to see why a UMVUE can sit strictly above the floor."}),
 "revision":{
  "sheet":L(
    "Score: U(θ) = ∂ℓ/∂θ.  Under regularity, E[U] = 0.",
    "Fisher information: I(θ) = Var(U) = E[U²] = −E[∂²ℓ/∂θ²]. The second form is usually the easy one.",
    "For an iid sample: Iₙ(θ) = n·I₁(θ). Information adds.",
    "Cramér–Rao, unbiased T for θ:   Var(T) ≥ 1 / (n I(θ)).",
    "For a function:   Var(T) ≥ [g′(θ)]² / (n I(θ))  when T is unbiased for g(θ).",
    "Biased T with bias b(θ):   Var(T) ≥ (1 + b′(θ))² / (n I(θ)).",
    "Attainment: the bound is reached exactly when ∂ℓ/∂θ = A(θ)·[T − g(θ)] — the score is LINEAR in T.",
    "Efficiency e(T) = CRLB / Var(T). Efficient means e = 1.",
    "Bernoulli: I(p) = 1/(p(1−p)), CRLB = p(1−p)/n, attained by x̄.",
    "Poisson: I(λ) = 1/λ, CRLB = λ/n, attained by x̄.",
    "Normal, σ² known: I(μ) = 1/σ², CRLB = σ²/n, attained by x̄.",
    "Exponential: I = 1/θ² in BOTH parameterisations, but the bound is attained for the mean θ and NOT for the rate λ.",
    "Regularity fails when the support depends on θ. For U(0,θ) the UMVUE has variance θ²/(n(n+2)) — order n⁻², faster than any 1/n floor.",
    "The MLE is asymptotically efficient: Var(θ̂) → 1/(nI(θ))."),
  "cards":L(
    ["Fisher information, in words","How sharply the log-likelihood curves at its peak, averaged over samples. Sharp peak, high information, low attainable variance."],
    ["Two formulas for I(θ)","E[(∂ℓ/∂θ)²] and −E[∂²ℓ/∂θ²]. Equal under regularity; the second derivative is usually less work."],
    ["Information for n observations","Iₙ(θ) = n·I₁(θ). Independent observations contribute information additively."],
    ["Cramér–Rao for a function of θ","Var(T) ≥ [g′(θ)]²/(nI(θ)) when T is unbiased for g(θ). Forgetting to square g′ is the standard slip."],
    ["When is the bound attained?","Exactly when the score factorises as A(θ)[T − g(θ)]. If the score is not linear in T, no unbiased estimator reaches the floor."],
    ["Where the bound does not apply","When the support depends on θ. U(0,θ) is the standard case, and its UMVUE beats any 1/n bound."],
    ["Efficiency","e(T) = CRLB/Var(T), between 0 and 1. e = 1 means efficient; the MLE achieves it only in the limit."],
    ["Same family, different answer","For the exponential, x̄ attains the bound for the mean 1/λ but nothing attains it for the rate λ. Parameterisation matters."])},
 "traps":L(
   "Quoting the bound for a family whose support moves with θ.",
   "Forgetting the [g′(θ)]² numerator when the target is a function of θ rather than θ itself.",
   "Using the bound on a biased estimator without the (1 + b′(θ))² numerator.",
   "Writing I₁(θ) where the question wants nI₁(θ), or the reverse.",
   "Assuming a UMVUE must attain the bound — it need not.",
   "Confusing observed information −∂²ℓ/∂θ² at θ̂ with expected information −E[∂²ℓ/∂θ²].",
   "Treating 'the MLE is efficient' as a finite-sample statement. It is asymptotic."),
}

S=[]
def scene(**kw):
    kw.setdefault("id","s%d"%(len(S)+1)); S.append(kw); return kw

scene(kind="intuition", title="How sharp is the peak?", mins=5,
 objective="See information as curvature before meeting any formula.",
 body=L(
  "Two experiments, same estimate. In the first, the log-likelihood rises to a sharp spike at θ̂ and falls away steeply on both sides. In the second it has a long flat ridge, and values a fair distance from θ̂ are almost as plausible.",
  "Which experiment has told you more about θ? Obviously the first. In the second, the data barely discriminate between neighbouring parameter values, so any estimate you form will move around a lot from sample to sample.",
  "That is the whole idea, and Fisher information is the number that measures it: the curvature of the log-likelihood at the top, averaged over the samples you might have drawn. Steep curvature means high information. High information means a low floor on how much any estimator must vary.",
  "The Cramér–Rao bound turns that into an inequality you can compute with. It says no unbiased estimator of θ can have variance below 1/(nI(θ)). Not 'no estimator anyone has found' — no estimator that exists, under the stated conditions.",
  "Two things follow that the exam likes. If you find an unbiased estimator whose variance equals the bound, you are finished: it is the best unbiased estimator and you need no further argument. And if the bound tells you something impossible, that is a signal the conditions were violated, not that you have discovered a better estimator."),
 aside={"h":"Why the second derivative and not the first",
   "body":"At the maximum the first derivative is zero by construction — it carries no information about sharpness. The second derivative is the first quantity that measures how fast the likelihood falls away, which is exactly what 'the data pin θ down' means."},
 ask={"q":"Why does a flatter log-likelihood near its maximum mean a less precise estimator?",
      "nudge":"If the curve is nearly flat, how different could the data have been before the peak moved appreciably?"})

scene(kind="explore", title="Watch the peak sharpen as the sample grows", mins=6,
 objective="Connect sample size, curvature and the variance floor in one picture.",
 viz={"type":"exp-likelihood","n":3,"sumx":12.0},
 body=L(
  "This is the exponential likelihood. Leave Σxᵢ roughly proportional to n — for instance n = 3 with Σx = 12, then n = 6 with Σx = 24 — so the peak stays near the same λ̂, and watch what happens to its WIDTH.",
  "At n = 3 the curve is a broad hill: a wide band of rates makes the data nearly as plausible. At n = 12 it is a narrow spike. Nothing about the estimate changed; what changed is how firmly the data exclude neighbouring values.",
  "That narrowing is information accumulating. For the exponential rate, I₁(λ) = 1/λ², so a sample of n carries Iₙ(λ) = n/λ², and the Cramér–Rao floor for an unbiased estimator of λ is λ²/n. Double n and the floor halves.",
  "Information adds because the observations are independent: each one contributes its own curvature to the total. That additivity is why nearly every bound you will compute in an exam has an n in the denominator and nothing more complicated."),
 ask={"q":"The floor for estimating λ is λ²/n, so it shrinks like 1/n. What does that say about the standard error, and about how many observations you need to halve it?",
      "nudge":"Standard error is the square root of variance. If variance falls like 1/n, what does its square root do?"})

scene(kind="theory", title="Score, information, and the conditions that make it work", mins=8,
 objective="Get both formulas for I(θ) and know exactly when they are allowed.",
 blocks=L(
  {"t":"def","h":"Score function","body":"U(θ) = ∂ℓ(θ)/∂θ, the derivative of the log-likelihood. Under regularity it has mean zero: E_θ[U(θ)] = 0. Setting U = 0 is how you found the MLE, so the score is already familiar."},
  {"t":"formula","h":"Fisher information — two equal forms",
   "body":"I(θ) = Var( U(θ) ) = E[ (∂ℓ/∂θ)² ]  =  − E[ ∂²ℓ/∂θ² ]"},
  {"t":"note","h":"Which form to use","body":"Almost always the second. Differentiating twice and taking an expectation is shorter than squaring a score and expanding it. The two agree only under regularity — the equality is itself a consequence of being allowed to swap differentiation and integration."},
  {"t":"formula","h":"Information adds","body":"For an iid sample of size n:   Iₙ(θ) = n · I₁(θ).\nCompute the information in ONE observation, then multiply."},
  {"t":"assume","h":"The regularity conditions","body":"The support of f does not depend on θ; θ is interior to the parameter space; ℓ is twice differentiable in θ; differentiation under the integral sign is valid; and 0 < I(θ) < ∞. Every result below assumes all of these."},
  {"t":"trap","h":"Observed versus expected information","body":"−∂²ℓ/∂θ² evaluated at θ̂ is the OBSERVED information: a number computed from your data. I(θ) = −E[∂²ℓ/∂θ²] is the EXPECTED information: an average over all samples, and a function of θ. The Cramér–Rao bound uses the expected one. Software often reports the observed one, and questions exploit the difference."},
  {"t":"note","h":"A sanity check worth doing","body":"I(θ) must be strictly positive. If your calculation gives zero or something negative, you have dropped a sign or differentiated the wrong variable — go back rather than carry it forward."}))

scene(kind="worked", title="Worked in full — the Bernoulli", mins=6,
 objective="Compute I(p), write the bound, and settle attainment in one pass.",
 problem="X₁,…,Xₙ are iid Bernoulli(p). Find I(p), the Cramér–Rao bound for unbiased estimators of p, and decide whether x̄ attains it.",
 steps=L(
  {"say":"Log-likelihood for one observation.","math":"ℓ(p) = x log p + (1 − x) log(1 − p)",
   "why":"Work with a single observation and multiply by n at the end. It is less algebra and it is what Iₙ = nI₁ is for."},
  {"say":"Score.","math":"U(p) = ∂ℓ/∂p = x/p − (1 − x)/(1 − p)",
   "why":"Note the minus sign from the chain rule on log(1−p). It is the commonest slip in this calculation."},
  {"say":"Second derivative.","math":"∂²ℓ/∂p² = − x/p² − (1 − x)/(1 − p)²",
   "why":"Both terms are negative for any x, which is the concavity you expect at a maximum."},
  {"say":"Take minus the expectation, using E[X] = p.",
   "math":"I(p) = p/p² + (1 − p)/(1 − p)² = 1/p + 1/(1 − p) = 1/( p(1 − p) )",
   "why":"The two fractions combine over a common denominator. Notice the result is largest near p = 0 or 1 and smallest at p = 0.5 — extreme probabilities are easier to pin down."},
  {"say":"Scale to the sample and write the bound.","math":"Iₙ(p) = n/( p(1−p) ),   CRLB = 1/Iₙ(p) = p(1 − p)/n",
   "why":"The bound is the reciprocal of the total information. Every unbiased estimator of p must have variance at least this."},
  {"say":"Check attainment.","math":"Var(x̄) = Var(X)/n = p(1 − p)/n  =  CRLB   ✓",
   "why":"Equality, so x̄ is efficient and no unbiased estimator of p can do better. This also re-derives, in one line, that x̄ is the UMVUE — without Rao–Blackwell or Lehmann–Scheffé."}),
 after="Three questions answered by one calculation: how much information the data carry, what floor that sets, and whether the obvious estimator reaches it. When a question asks only for the bound, compute the attainment check anyway — it is two lines and it is often the next part.")

scene(kind="recall", title="Pause and recall", mins=2,
 objective="Retrieve before reading on — this is where the retention comes from.",
 intro="Answer each in your head before revealing. Correcting a wrong retrieval beats re-reading a right answer.",
 items=L(
  {"q":"Write both formulas for Fisher information.","a":"I(θ) = E[(∂ℓ/∂θ)²] = −E[∂²ℓ/∂θ²]."},
  {"q":"How does information scale with sample size?","a":"Iₙ(θ) = n·I₁(θ) — it adds across independent observations."},
  {"q":"State the Cramér–Rao bound for an unbiased estimator of θ.","a":"Var(T) ≥ 1/(n I(θ))."},
  {"q":"Name the condition that most often fails, and one family where it does.","a":"The support must not depend on θ. U(0,θ) violates it."}))

scene(kind="completion", title="Your turn, with the scaffolding removed — the Poisson", mins=7,
 objective="Run the same four steps yourself on a discrete family.",
 problem="X₁,…,Xₙ are iid Poisson(λ). Find I(λ), the Cramér–Rao bound for unbiased estimators of λ, and decide whether x̄ attains it.",
 steps=L(
  {"say":"Log-likelihood for one observation, dropping the constant.",
   "math":"ℓ(λ) = −λ + x log λ − log(x!)",
   "why":"The log(x!) term has no λ in it, so it will vanish on the first derivative. Write it once and forget it."},
  {"say":"Differentiate twice.",
   "blank":{"prompt":"Write ∂²ℓ/∂λ².",
     "answer":"−x/λ²",
     "accept":["−x/λ²","-x/lambda^2","-x/λ^2","−x/λ^2","-x/λ²"],
     "hint":"First derivative is −1 + x/λ. Differentiate again: the constant disappears and x/λ = xλ^(−1) brings down a factor."},
   "why":"Negative for every x > 0, as concavity at a maximum requires."},
  {"say":"Take minus the expectation, using E[X] = λ.",
   "blank":{"prompt":"Write I(λ).",
     "answer":"1/λ",
     "accept":["1/λ","1/lambda","1/λ ","λ^(-1)","1 / λ"],
     "hint":"−E[−X/λ²] = E[X]/λ². Now substitute E[X] = λ and cancel."},
   "why":"Information falls as λ grows, so the floor λ/n rises: a larger mean is harder to pin down in ABSOLUTE terms. Relative to λ itself it is easier — the standard error √(λ/n) divided by λ is 1/√(nλ), which shrinks. Keep the two straight; questions ask for one and offer the other."},
  {"say":"Write the bound for a sample of size n.",
   "blank":{"prompt":"Write the Cramér–Rao bound for unbiased estimators of λ.",
     "answer":"λ/n",
     "accept":["λ/n","lambda/n","λ / n"],
     "hint":"Iₙ = n·I₁, and the bound is its reciprocal."},
   "why":"The familiar 1/n rate, with the parameter itself in the numerator."},
  {"say":"Check attainment.","math":"Var(x̄) = Var(X)/n = λ/n = CRLB   ✓  so x̄ is efficient",
   "why":"The Poisson variance equals its mean, which is exactly what makes the equality come out. x̄ is the UMVUE of λ and attains the floor."}),
 after="Bernoulli and Poisson both came out efficient, which can give the impression that the obvious estimator always attains the bound. Scene 8 breaks that impression on purpose.")

scene(kind="theory", title="The bound itself — functions, bias, attainment, efficiency", mins=9,
 objective="Handle the three variants the exam actually sets, and know when the floor is reachable.",
 blocks=L(
  {"t":"formula","h":"Cramér–Rao, the standard form","body":"T unbiased for θ:    Var_θ(T)  ≥  1 / ( n I(θ) )"},
  {"t":"formula","h":"For a function of θ","body":"T unbiased for g(θ):    Var_θ(T)  ≥  [ g′(θ) ]² / ( n I(θ) )\nThe derivative is SQUARED. Dropping that square is the single commonest error in this topic."},
  {"t":"formula","h":"For a biased estimator","body":"If E[T] = θ + b(θ):    Var_θ(T)  ≥  ( 1 + b′(θ) )² / ( n I(θ) )\nSetting b ≡ 0 recovers the standard form, so this is the general statement."},
  {"t":"def","h":"Efficiency","body":"e(T) = CRLB / Var(T), a number in (0, 1]. T is efficient when e(T) = 1. Relative efficiency of T₁ to T₂ is Var(T₂)/Var(T₁)."},
  {"t":"formula","h":"When is the bound attainable at all?",
   "body":"Equality holds for an unbiased T of g(θ) if and only if the score factorises as\n   ∂ℓ/∂θ  =  A(θ) · [ T − g(θ) ]\nfor some function A not involving the data. In words: the score must be LINEAR in T."},
  {"t":"note","h":"How to use that condition","body":"Write the score, and try to collect it into a constant-in-data multiple of (something − something). If it refuses to factorise that way, no unbiased estimator attains the bound and the floor is unreachable — which is a complete answer to 'does an efficient estimator exist?'."},
  {"t":"trap","h":"Where the bound does not apply at all",
   "body":"If the support depends on θ, regularity fails and the inequality is simply not available. For U(0,θ) the UMVUE (n+1)/n·X₍ₙ₎ has variance θ²/(n(n+2)), which is of order n⁻² — faster than any 1/n floor could allow. Quoting a Cramér–Rao bound there produces a contradiction, and the contradiction is the evidence that the conditions were violated."},
  {"t":"note","h":"What it says about the MLE","body":"Under regularity, √n(θ̂ − θ) → N(0, 1/I(θ)), so the MLE's variance approaches 1/(nI(θ)) — the bound — as n grows. The MLE is asymptotically efficient. At finite n it may be biased and may sit above the floor, as the next scene shows."}))

scene(kind="explore", title="A case where nothing reaches the floor", mins=7,
 objective="See that the bound is a floor, not a promise — and that the parameterisation decides.",
 viz={"type":"mle-sampling","lam":0.5,"n":10},
 body=L(
  "Exponential again, and here I(λ) = 1/λ², so the floor for an unbiased estimator of the RATE is λ²/n. With λ = 0.5 and n = 10 that is 0.25/10 = 0.025.",
  "From the previous topic, the UMVUE of λ is (n−1)/ΣX, and its variance works out to λ²/(n−2) = 0.25/8 = 0.03125. That is comfortably above the floor of 0.025. The best unbiased estimator that exists does not attain the bound.",
  "Why not? Apply the attainment test. The score is ∂ℓ/∂λ = n/λ − Σxᵢ = −n( x̄ − 1/λ ). It IS linear — but in x̄, and against the target 1/λ, not λ. So an unbiased estimator of 1/λ attains the bound, and no unbiased estimator of λ does.",
  "Check that claim directly. Write θ = 1/λ for the mean. Then I(θ) = 1/θ² as well, the floor is θ²/n, and Var(X̄) = θ²/n exactly. Attained.",
  "The same family, the same data, the same information — and the bound is reachable for the mean but not for the rate. Attainability is a property of the parameterisation, not only of the model. Raise n on the slider and watch the MLE's spread fall toward the floor it never quite sits on."),
 ask={"q":"The MLE is called efficient, yet here it sits above the floor at every finite n. In what sense is the claim true?",
      "nudge":"Look at what happens to the ratio of its variance to the bound as n grows, rather than at the gap itself."})

scene(kind="guided", title="Now without the steps — the normal mean", mins=7,
 objective="Run the whole calculation unaided on the family that appears most often.",
 problem="X₁,…,Xₙ are iid N(μ, σ²) with σ² KNOWN. Find I(μ), write the Cramér–Rao bound for unbiased estimators of μ, and determine whether x̄ is efficient.",
 hints=L(
  "Direction — start with the log-density of a single observation and drop every term that has no μ in it. Those terms contribute nothing to any derivative with respect to μ, so carrying them is wasted writing.",
  "Method — use I(μ) = −E[∂²ℓ/∂μ²]. Differentiate twice with respect to μ. Something convenient happens: the second derivative has no x in it at all, so the expectation step is trivial.",
  "Next step — once you have I(μ), the bound is 1/(nI(μ)). Compare it with Var(X̄), which you already know for a normal sample."),
 solution=L(
  {"say":"Log-density, keeping only μ terms.","math":"ℓ(μ) = −(x − μ)² / (2σ²) + constant"},
  {"say":"First derivative — the score.","math":"∂ℓ/∂μ = (x − μ) / σ²"},
  {"say":"Second derivative.","math":"∂²ℓ/∂μ² = −1/σ²,   free of x"},
  {"say":"Fisher information.","math":"I(μ) = −E[ −1/σ² ] = 1/σ²,   so Iₙ(μ) = n/σ²"},
  {"say":"The bound.","math":"CRLB = 1/Iₙ(μ) = σ²/n"},
  {"say":"Attainment.","math":"Var(X̄) = σ²/n = CRLB  ✓  x̄ is efficient, with e(x̄) = 1"}),
 answer="I(μ) = 1/σ², the bound is σ²/n, and x̄ attains it exactly — so x̄ is efficient and is the UMVUE of μ.",
 check="Three things were asked and the third is the one candidates drop: say explicitly that the bound is ATTAINED and that x̄ is therefore efficient. Note also that the second derivative contained no x, so the expectation step was free — a useful signal that you have differentiated correctly for a normal mean.")

scene(kind="trapcheck", title="Six statements — verdict on each before you look", mins=6,
 objective="Practise the per-statement discipline the real multi-statement items demand.",
 intro="Give every statement a true or false verdict first. In the exam these six would be one question scored all or nothing, so a verdict you skipped is a mark you gambled.",
 items=L(
  {"claim":"The Cramér–Rao bound applies to every estimator, biased or not, in every family.","tf":False,
   "why":"False twice over. The standard form is for unbiased estimators; a biased one needs the (1 + b′(θ))² numerator. And the whole result requires the regularity conditions, which fail when the support depends on θ."},
  {"claim":"If an unbiased estimator attains the bound, it is the UMVUE.","tf":True,
   "why":"True, and it is the quickest route to a UMVUE when it works. Nothing unbiased can be below the floor, so an estimator sitting on it cannot be beaten."},
  {"claim":"Every UMVUE attains the Cramér–Rao bound.","tf":False,
   "why":"False — the converse does not hold. For the exponential rate, the UMVUE (n−1)/ΣX has variance λ²/(n−2), strictly above the floor λ²/n."},
  {"claim":"For an iid sample, Iₙ(θ) = n·I₁(θ).","tf":True,
   "why":"True. Information is additive over independent observations, which is why the bound carries a 1/n."},
  {"claim":"For X₁,…,Xₙ iid U(0,θ), the Cramér–Rao bound gives a valid floor for unbiased estimators of θ.","tf":False,
   "why":"False. The support depends on θ, regularity fails, and the bound does not apply. The UMVUE's variance is θ²/(n(n+2)), of order n⁻², which no 1/n floor could permit."},
  {"claim":"Under regularity, −E[∂²ℓ/∂θ²] equals E[(∂ℓ/∂θ)²].","tf":True,
   "why":"True — that equality is the information identity, and it is itself a consequence of being allowed to differentiate under the integral sign."}))

scene(kind="guided", title="Transfer — a bound for a function of the parameter", mins=9,
 objective="Apply the [g′(θ)]² form to a target you met two topics ago.",
 problem="X₁,…,Xₙ are iid Poisson(λ). In the Rao–Blackwell topic the UMVUE of g(λ) = e^(−λ) came out as ((n−1)/n)^T with T = ΣXᵢ. Find the Cramér–Rao bound for unbiased estimators of e^(−λ), and say whether that UMVUE attains it.",
 hints=L(
  "Direction — the target is not λ, so the standard 1/(nI) form is the wrong one. Identify g(λ), differentiate it, and remember what happens to that derivative in the formula.",
  "Method — use Var(T) ≥ [g′(λ)]²/(n I(λ)). You already found I(λ) for the Poisson in scene 6, so only g′ is new work.",
  "Next step — for the comparison you need the variance of ((n−1)/n)^T. Use the fact that for T ~ Poisson(nλ) and any constant a, E[a^T] = e^(nλ(a−1)). Apply it once with a and once with a² to get the variance."),
 solution=L(
  {"say":"Identify g and differentiate.","math":"g(λ) = e^(−λ),   g′(λ) = −e^(−λ),   [g′(λ)]² = e^(−2λ)"},
  {"say":"Information for the Poisson.","math":"I(λ) = 1/λ,  so  n I(λ) = n/λ"},
  {"say":"The bound.","math":"CRLB = e^(−2λ) / (n/λ) = λ e^(−2λ) / n"},
  {"say":"Variance of the UMVUE, writing a = (n−1)/n.",
   "math":"E[a^T] = e^(nλ(a−1)) = e^(−λ)  ✓ unbiased.\nE[a^(2T)] = e^(nλ(a²−1)) = e^(−2λ + λ/n),   since a² − 1 = (1 − 2n)/n²"},
  {"say":"Subtract.","math":"Var = e^(−2λ + λ/n) − e^(−2λ) = e^(−2λ) ( e^(λ/n) − 1 )"},
  {"say":"Compare.","math":"e^(λ/n) − 1 = λ/n + λ²/(2n²) + …  >  λ/n,\nso Var > λe^(−2λ)/n = CRLB, strictly, at every finite n — but the ratio → 1 as n → ∞."}),
 answer="CRLB = λe^(−2λ)/n. The UMVUE has variance e^(−2λ)(e^(λ/n) − 1), which is strictly greater than the bound for every finite n, though the two agree in the limit.",
 check="Two traps sat in this one. The numerator is [g′(λ)]² = e^(−2λ), not g′ itself and not 1 — if your bound had no e^(−2λ) in it you used the wrong form. And the conclusion is that the bound is NOT attained, which is a perfectly good answer: being the best unbiased estimator and sitting on the Cramér–Rao floor are different achievements.")

scene(kind="summary", title="What you should now be able to do unaided", mins=3,
 objective="Close the loop before the test.",
 body=L(
  "Compute I(θ) for any standard family by differentiating the log-density twice and taking minus the expectation.",
  "Scale it with Iₙ = nI₁ and write the bound as its reciprocal.",
  "Switch to the [g′(θ)]² numerator the moment the target is a function of θ, and to (1+b′(θ))² when the estimator is biased.",
  "Check the regularity conditions first, and refuse to quote a bound when the support moves with θ.",
  "Settle attainment by testing whether the score is linear in the estimator, rather than by hoping.",
  "Compute efficiency as CRLB/Var, and state the MLE's efficiency as an asymptotic claim, not a finite-sample one.",
  "The mastery test is ten unseen questions across all of this. Hints are off. The pass is 80% overall with 70% floors on the numerical and multi-statement items."))

scene(kind="quiz", title="Mastery test", mins=12,
 objective="Demonstrate it independently, on unseen questions.",
 setId="inference_t6_mastery")

lesson["scenes"]=S

def m(i,fmt,stem,options,ans,expl,**kw):
    d={"id":"inf-t6-m-%02d"%i,"format":fmt,"topic":"inference-t6","stem":stem,
       "options":options,"answer":ans,"explanation":expl}
    d.update(kw); return d

mastery=[
 m(1,"single","Fisher information for a single observation may be computed as:",
   ["−E[∂²ℓ/∂θ²], which equals E[(∂ℓ/∂θ)²] under regularity",
    "E[∂²ℓ/∂θ²], which equals Var(∂ℓ/∂θ) always",
    "−∂²ℓ/∂θ² evaluated at θ̂",
    "E[∂ℓ/∂θ], which is non-zero under regularity"],
   "A","Both forms in A are standard and agree under regularity. B has the wrong sign and drops the condition. C is the OBSERVED information — a number from one dataset, not the expected information the bound uses. D is wrong on the fact: the score has expectation zero under regularity, which is why its variance is the useful quantity."),
 m(2,"numeric","X₁,…,X₂₅ are iid Bernoulli(p) with p = 0.4. Give the Cramér–Rao bound for unbiased estimators of p, and say whether x̄ attains it.",
   ["0.0096, and x̄ attains it","0.0096, and x̄ does not attain it",
    "0.24, and x̄ attains it","0.24, and x̄ does not attain it"],
   "A","I(p) = 1/(p(1−p)), so the bound is p(1−p)/n = (0.4)(0.6)/25 = 0.24/25 = 0.0096. And Var(x̄) = p(1−p)/n is exactly that, so x̄ is efficient. Option C forgets to divide by n.",
   check="Two parts: the number and the attainment verdict. 0.24 is p(1−p) before dividing by n — check the n is in there."),
 m(3,"multi","Consider the Cramér–Rao bound and its conditions.",
   ["A, B and D only","A and C only","B and C only","A, C and D only"],"A",
   "A is true — the squared derivative is the correct numerator for a function of θ. B is true, and is the general form that reduces to the standard one when b ≡ 0. C is false: the converse fails, as the exponential rate shows. D is true, and is why U(0,θ) is excluded.",
   statements=["For T unbiased for g(θ), the bound is [g′(θ)]²/(nI(θ)).",
               "For a biased T with bias b(θ), the bound is (1+b′(θ))²/(nI(θ)).",
               "Every UMVUE attains the Cramér–Rao bound.",
               "The bound requires the support of the density to be free of θ."],
   verdicts={"A":{"tf":True,"why":"The derivative is squared; forgetting the square is the commonest error in the topic."},
             "B":{"tf":True,"why":"The general form. Setting b ≡ 0 recovers the standard statement."},
             "C":{"tf":False,"why":"The exponential rate's UMVUE has variance λ²/(n−2), strictly above the floor λ²/n."},
             "D":{"tf":True,"why":"A moving support breaks differentiation under the integral, and with it the whole derivation."}}),
 m(4,"numeric","X₁,…,X₁₆ are iid Poisson(λ) with λ = 4. Give Iₙ(λ) and the Cramér–Rao bound for unbiased estimators of λ.",
   ["Iₙ = 4, bound = 0.25","Iₙ = 0.25, bound = 4",
    "Iₙ = 64, bound = 0.015625","Iₙ = 4, bound = 4"],
   "A","I₁(λ) = 1/λ = 0.25, so Iₙ = n/λ = 16/4 = 4, and the bound is its reciprocal, 1/4 = 0.25. Note Var(x̄) = λ/n = 0.25 too, so x̄ attains it. Option C uses I₁ = λ rather than 1/λ.",
   check="The bound is the RECIPROCAL of the total information. If your two numbers are not reciprocals of each other, one of them is wrong."),
 m(5,"single","For which family does the Cramér–Rao bound fail to apply?",
   ["U(0,θ), because the support depends on θ","Poisson(λ), because the data are discrete",
    "Bernoulli(p), because p is bounded","N(μ,σ²) with σ² known, because there are two parameters"],
   "A","Regularity requires the support to be free of the parameter, and for U(0,θ) it is not — so differentiation under the integral fails and the bound is unavailable. Discreteness is no obstacle (B is wrong; Poisson and Bernoulli are both standard applications), a bounded parameter space is fine provided θ is interior, and in D σ² is known so there is only one unknown parameter."),
 m(6,"numeric","X₁,…,X₃₆ are iid N(μ, σ²) with σ² = 9 known. Give Iₙ(μ) and the Cramér–Rao bound for unbiased estimators of μ.",
   ["Iₙ = 4, bound = 0.25","Iₙ = 0.25, bound = 4",
    "Iₙ = 324, bound = 0.00309","Iₙ = 4, bound = 9"],
   "A","I₁(μ) = 1/σ² = 1/9, so Iₙ = n/σ² = 36/9 = 4 and the bound is 1/4 = 0.25. That equals Var(X̄) = σ²/n = 9/36 = 0.25, so x̄ is efficient. Option C multiplies by σ² instead of dividing.",
   check="σ² = 9 is the variance, not the standard deviation. I₁ = 1/σ² = 1/9, not 1/3."),
 m(7,"multi","Let T be an unbiased estimator of θ in a regular family.",
   ["B and C only","A and B only","A, B and C only","C and D only"],"A",
   "A is false — the MLE's efficiency is an asymptotic statement; at finite n it may be biased and above the floor. B is true, and is the standard shortcut to a UMVUE. C is true, and is the exact attainment criterion. D is false: efficiency is CRLB/Var, which cannot exceed 1.",
   statements=["The MLE attains the Cramér–Rao bound exactly for every sample size.",
               "If Var(T) equals the bound, then T is the UMVUE of θ.",
               "The bound is attained if and only if the score can be written as A(θ)[T − θ].",
               "Efficiency e(T) = CRLB/Var(T) can exceed 1 for a very good estimator."],
   verdicts={"A":{"tf":False,"why":"Asymptotic only. Var(θ̂) → 1/(nI(θ)); at finite n it generally sits above."},
             "B":{"tf":True,"why":"Nothing unbiased can be below the floor, so an estimator on it cannot be beaten."},
             "C":{"tf":True,"why":"The linear-score condition is exactly the equality case of the Cauchy–Schwarz step."},
             "D":{"tf":False,"why":"Var(T) ≥ CRLB, so the ratio is at most 1. A value above 1 means an arithmetic error."}}),
 m(8,"numeric","X₁,…,X₁₀ are iid Exponential with rate λ = 2. The UMVUE of λ is (n−1)/ΣX, with variance λ²/(n−2). Give the Cramér–Rao bound and the efficiency of the UMVUE.",
   ["Bound = 0.4, efficiency = 0.8","Bound = 0.5, efficiency = 0.8",
    "Bound = 0.4, efficiency = 1.0","Bound = 0.5, efficiency = 1.25"],
   "A","I(λ) = 1/λ², so the bound is λ²/n = 4/10 = 0.4. The UMVUE's variance is λ²/(n−2) = 4/8 = 0.5. Efficiency is CRLB/Var = 0.4/0.5 = 0.8. The best unbiased estimator is only 80% efficient here, which is the point: a UMVUE need not sit on the floor.",
   check="Efficiency is bound ÷ variance, so it must come out at or below 1. Option D's 1.25 is the ratio taken upside down."),
 m(9,"numeric","X₁,…,Xₙ are iid Exponential with mean θ, so f(x) = (1/θ)e^(−x/θ). Given I(θ) = 1/θ², give the Cramér–Rao bound for unbiased estimators of θ and say whether x̄ attains it.",
   ["θ²/n, and x̄ attains it exactly","θ²/n, and x̄ does not attain it",
    "1/(nθ²), and x̄ attains it exactly","θ/n, and x̄ does not attain it"],
   "A","The bound is 1/(nI(θ)) = θ²/n. For this family Var(X) = θ², so Var(X̄) = θ²/n, equal to the bound — x̄ is efficient. Contrast this with the RATE parameterisation of the same family, where nothing unbiased attains the floor: attainability depends on which parameter you are estimating.",
   check="The bound is the reciprocal of nI(θ), so with I = 1/θ² it is θ²/n and not 1/(nθ²). Writing the reciprocal the wrong way round is the slip option C is built from."),
 m(10,"order","To find the Cramér–Rao bound for an unbiased estimator of g(θ), arrange these steps in order.",
   ["C, A, D, B","A, C, D, B","C, D, A, B","A, D, C, B"],"A",
   "Check regularity first — if the support depends on θ there is no bound to compute and everything after is wasted. Then get I₁(θ) from the second derivative, scale to nI₁ and divide [g′(θ)]² by it, and finally compare with the candidate estimator's variance to settle attainment.",
   items=["A. Compute I₁(θ) = −E[∂²ℓ/∂θ²]",
          "B. Compare with Var(T) to decide whether the bound is attained",
          "C. Check that the support does not depend on θ",
          "D. Form [g′(θ)]² / (n I₁(θ))"]),
]

body={"moduleId":"inference","source":"mastery","topicId":"inference-t6",
      "label":"Cramér–Rao and Fisher information — mastery test (unseen)","count":len(mastery),"items":mastery}
with open(os.path.join(OUT,"inference_t6_mastery.json"),"w") as f:
    json.dump(body,f,ensure_ascii=False,indent=1)
with open(os.path.join(OUT,"lesson_t6.json"),"w") as f:
    json.dump(lesson,f,ensure_ascii=False,indent=1)
fm={}
for i in mastery: fm[i["format"]]=fm.get(i["format"],0)+1
print("scenes:",len(S),"->"," ".join(x["kind"] for x in S))
print("mastery:",len(mastery),fm)
print("bytes:",os.path.getsize(os.path.join(OUT,"lesson_t6.json")))
