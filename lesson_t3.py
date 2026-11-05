# lessons/inferencet3 — Rao-Blackwell and Lehmann-Scheffe
# plus qsets/inference_t3_mastery
import json, os
OUT = "/home/claude/w1/seed"
L = lambda *p: list(p)

lesson = {
 "id":"inferencet3","moduleId":"inference","topicId":"inference-t3",
 "title":"Rao–Blackwell and Lehmann–Scheffé",
 "breadcrumb":"Statistical Inference → Point Estimation → Best unbiased estimation",
 "engine":"B",
 "engineName":"Estimation and inference — sampling distributions, and the variance you remove by conditioning",
 "estMin":45,"version":"1.0","status":"approved",
 "provenance":"Theory, worked examples and practice authored for this platform against the UGC NET Statistics syllabus. Previous-year questions are stored separately and carry their exam cycle.",
 "objectives":L(
   "State Rao–Blackwell and say why the statistic conditioned on must be sufficient.",
   "Compute E[δ(X) | T = t] in the standard cases, using the conditional distribution of the sample given its total.",
   "State Lehmann–Scheffé and explain exactly which word turns 'an improvement' into 'the unique best'.",
   "Produce a UMVUE by either route — Rao–Blackwellise a crude unbiased estimator, or find an unbiased function of a complete sufficient statistic directly.",
   "Say when a UMVUE fails to exist, and when it exists but is absurd.",
   "Separate the UMVUE from the MLE, and know which of the two survives a change of parameter."),
 "prereq":L(
   {"id":"p1","name":"Sufficiency and the factorisation theorem","why":"Rao–Blackwell conditions on a sufficient statistic. If T is wrong, E[δ|T] still involves θ and is not an estimator at all."},
   {"id":"p2","name":"Completeness","why":"It is the single word that upgrades Rao–Blackwell's 'no worse' into Lehmann–Scheffé's 'uniquely best'. Scene 7 leans on it entirely."},
   {"id":"p3","name":"Conditional expectation and the variance decomposition","why":"Var(δ) = E[Var(δ|T)] + Var(E[δ|T]) is the whole proof of Rao–Blackwell. Know it before scene 3."}),
 "mastery":{"minQ":10,"pass":80,"fmtMin":{"numeric":70,"multi":70},"noHints":True,"retestDays":7,
   "note":"Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints."},
 "refs":L(
  {"title":"Mathematical Statistics — Unbiased Estimation and Risk Inequalities","where":"Lecture note 13",
   "site":"MIT OpenCourseWare 18.655 (Spring 2016)","url":"https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/pages/lecture-notes/",
   "type":"Lecture notes","free":True,"checked":"2026-10-12",
   "why":"The graduate statement of both theorems with the risk framework around them. Reach for it after scene 7, when you want to see why the conclusion is about convex loss and not only variance."},
  {"title":"Properties of a Sufficient Statistic — Completeness and Uniqueness","where":"Prof. Michael Levine, 16 April 2015",
   "site":"Purdue STAT 517","url":"https://www.stat.purdue.edu/~mlevins/docs/stat517/Lecture15_STAT517.pdf",
   "type":"Lecture slides","free":True,"checked":"2026-10-12",
   "why":"Works the same examples this lesson uses — Bernoulli by conditioning, the exponential MVUE, the uniform (n+1)/n·X₍ₙ₎, and N(μ, a²μ²) as a sufficient-but-not-complete case. Read it after scene 6. One caution: the final slide labels the MVUE of a Poisson probability as 'the MVUE of λ', which is a slip — the target there is the probability, not the parameter."}),
 "revision":{
  "sheet":L(
    "Rao–Blackwell: δ unbiased for g(θ), T sufficient ⟹ η(T) = E[δ|T] is unbiased and Var(η) ≤ Var(δ).",
    "The proof is one line: Var(δ) = E[Var(δ|T)] + Var(E[δ|T]) ≥ Var(η(T)).",
    "T must be SUFFICIENT, or E[δ|T] still contains θ and is not a statistic.",
    "The inequality is ≤, not <. It is an equality exactly when δ was already a function of T.",
    "Lehmann–Scheffé: T complete sufficient and η(T) unbiased ⟹ η(T) is THE UMVUE, unique almost surely.",
    "Completeness is what gives uniqueness: two unbiased functions of T differ by an unbiased estimator of zero.",
    "Two routes to a UMVUE: Rao–Blackwellise any crude unbiased δ, or solve E[h(T)] = g(θ) for h directly.",
    "Poisson, g = e^(−λ):  UMVUE = ((n−1)/n)^T.   Bernoulli, g = p²:  UMVUE = T(T−1)/(n(n−1)).",
    "Exponential rate λ:  MLE = n/Σxᵢ (biased),  UMVUE = (n−1)/Σxᵢ.",
    "U(0,θ):  UMVUE of θ = (n+1)/n · x₍ₙ₎.   UMVUE of θ² = (n+2)/n · x₍ₙ₎².",
    "N(μ,σ²), σ² known:  UMVUE of μ² = x̄² − σ²/n. It can come out negative — UMVUEs are not obliged to be sensible.",
    "A UMVUE is not invariant: the UMVUE of g(θ) is not g(UMVUE of θ). The MLE is invariant; this is the difference.",
    "No complete sufficient statistic (curved family) ⟹ Lehmann–Scheffé says nothing.",
    "Unbiased does not mean smaller MSE. For σ², the MLE beats s² on mean squared error."),
  "cards":L(
    ["Rao–Blackwell, in one sentence","Conditioning an unbiased estimator on a sufficient statistic keeps it unbiased and cannot increase its variance."],
    ["Why T must be sufficient","Otherwise the conditional distribution still depends on θ, so E[δ|T] is not computable from data alone."],
    ["The one-line proof","Var(δ) = E[Var(δ|T)] + Var(E[δ|T]). The first term is ≥ 0, so Var(E[δ|T]) ≤ Var(δ)."],
    ["When does Rao–Blackwell change nothing?","When δ is already a function of T. Then E[δ|T] = δ and the variance is unchanged."],
    ["What completeness adds","Uniqueness. Without it you get an improvement; with it you get THE best, and every starting point lands on the same answer."],
    ["Two routes to a UMVUE","Rao–Blackwellise any unbiased estimator, or solve E[h(T)] = g(θ) directly for h."],
    ["Is the UMVUE invariant?","No. The UMVUE of θ² is (n+2)/n·x₍ₙ₎², not the square of (n+1)/n·x₍ₙ₎. Only the MLE has invariance."],
    ["Can a UMVUE be absurd?","Yes. For a single Poisson observation the UMVUE of e^(−2λ) is (−1)^X — it alternates ±1 while estimating a number in (0,1)."])},
 "traps":L(
   "Conditioning on a statistic that is not sufficient, and producing an 'estimator' that still contains θ.",
   "Reading Rao–Blackwell as a strict improvement. It is ≤, with equality when δ was already a function of T.",
   "Claiming uniqueness from Rao–Blackwell alone. Uniqueness needs completeness.",
   "Applying Lehmann–Scheffé in a curved family, where no complete sufficient statistic exists.",
   "Squaring the UMVUE of θ and calling it the UMVUE of θ². That is MLE invariance, and UMVUEs do not have it.",
   "Assuming the UMVUE must beat the MLE on mean squared error. For the normal variance it does not.",
   "Forgetting to subtract the bias term: x̄² estimates μ² + σ²/n, not μ²."),
}

S=[]
def scene(**kw):
    kw.setdefault("id","s%d"%(len(S)+1)); S.append(kw); return kw

scene(kind="intuition", title="A terrible estimator, and what to do with it", mins=5,
 objective="See conditioning as the act of throwing away noise while keeping the signal.",
 body=L(
  "You have n observations from a Poisson(λ) and you want to estimate e^(−λ), the probability that a count comes out zero.",
  "Here is an estimator that works: look only at the FIRST observation and score 1 if it was zero, 0 otherwise. Call it δ = 1{X₁ = 0}. Its expectation is exactly P(X₁ = 0) = e^(−λ), so it is unbiased. Correct, and useless — it ignores n−1 observations and can only ever return 0 or 1 while estimating a number strictly between them.",
  "Now ask a different question. Suppose someone tells you the total ΣXᵢ = 7, but not how the sevens were distributed. What is your best guess at δ? That is a conditional expectation: E[δ | ΣXᵢ = 7]. Answering it uses all n observations, because the total did.",
  "Rao–Blackwell says that quantity is still unbiased, and its variance cannot be larger. You have improved the estimator by doing nothing but averaging away the part of the data that was irrelevant.",
  "One condition makes this legal, and it is the reason the previous two topics exist. The conditioning statistic has to be SUFFICIENT. If it were not, the conditional distribution would still depend on λ, and E[δ | T] would contain the unknown you were trying to estimate — not an estimator at all."),
 aside={"h":"What is actually being removed",
   "body":"Var(δ) = E[Var(δ|T)] + Var(E[δ|T]). The first term is the variability of δ among samples that share the same T — pure noise, since those samples are indistinguishable as far as θ is concerned. Conditioning deletes that term. Nothing about θ is lost, because T is sufficient."},
 ask={"q":"Why must T be sufficient for E[δ(X) | T] to be usable as an estimator at all?",
      "nudge":"Write down what you would need to know to compute the conditional expectation by hand. Is any of it unknown?"})

scene(kind="explore", title="The estimator you already know, and the one that is unbiased", mins=6,
 objective="See the bias Rao–Blackwell and Lehmann–Scheffé are there to remove.",
 viz={"type":"mle-sampling","lam":0.5,"n":4},
 body=L(
  "This is the exact sampling distribution of the exponential MLE, λ̂ = n/ΣX. The solid line is the true λ; the dashed line is E[λ̂] = nλ/(n−1), sitting stubbornly to the right of it.",
  "That gap is not a sampling accident — it is there at every n. The MLE systematically overstates the rate.",
  "Now ΣX is a complete sufficient statistic for λ, and E[1/ΣX] = λ/(n−1). So (n−1)/ΣX has expectation exactly λ. It is an unbiased function of a complete sufficient statistic, which by Lehmann–Scheffé makes it the UMVUE.",
  "Notice what it is: (n−1)/ΣX = ((n−1)/n) · λ̂. The best unbiased estimator is the MLE shrunk by a factor of (n−1)/n — precisely the factor that removes the gap on screen.",
  "Raise n and watch the two lines converge. The correction gets smaller because the MLE's bias does, which is why the distinction stops mattering asymptotically and matters a great deal at the sample sizes exam questions use."),
 ask={"q":"s² is unbiased for σ² and the MLE Σ(xᵢ−x̄)²/n is not. Which of the two has the smaller mean squared error?",
      "nudge":"MSE = variance + bias². Dividing by a larger number shrinks an estimator — what does shrinking do to each of those two terms?"})

scene(kind="theory", title="Rao–Blackwell, and the one line that proves it", mins=7,
 objective="Hold the theorem with its condition attached, and be able to prove it from the variance decomposition.",
 blocks=L(
  {"t":"def","h":"The construction","body":"Let δ(X) be any unbiased estimator of g(θ), and let T be sufficient for θ. Define η(T) = E[ δ(X) | T ]. Because T is sufficient, that conditional expectation does not involve θ, so η is a genuine statistic."},
  {"t":"formula","h":"Rao–Blackwell theorem","body":"E_θ[η(T)] = g(θ)   for every θ,   and   Var_θ(η(T)) ≤ Var_θ(δ(X))   for every θ."},
  {"t":"step","h":"Unbiasedness — the tower property","body":"E[η(T)] = E[ E[δ|T] ] = E[δ] = g(θ). One line, no conditions beyond δ being unbiased."},
  {"t":"step","h":"The variance half — one decomposition","body":"Var(δ) = E[ Var(δ | T) ] + Var( E[δ | T] ) = E[ Var(δ|T) ] + Var(η(T)).\nThe first term is an expectation of a variance, so it is ≥ 0. Therefore Var(η) ≤ Var(δ)."},
  {"t":"assume","h":"Sufficiency is not decoration","body":"Drop it and E[δ|T] depends on θ. You would be writing down a function of the unknown parameter and calling it an estimate. Every exam question that offers a non-sufficient statistic to condition on is testing exactly this."},
  {"t":"trap","h":"It is ≤, not <","body":"Equality holds precisely when Var(δ|T) = 0, which means δ was already a function of T. Rao–Blackwellising an estimator that already depends only on T changes nothing. Candidates lose marks asserting a strict improvement."},
  {"t":"note","h":"What it does NOT give you","body":"A best estimator. Start from a different unbiased δ and you may land somewhere else. Rao–Blackwell improves; it does not identify. The next theorem fixes that, and it needs completeness to do it."}))

scene(kind="worked", title="Worked in full — the Poisson zero probability", mins=7,
 objective="Carry out one conditional expectation end to end, and see where the sufficiency gets used.",
 problem="X₁,…,Xₙ are iid Poisson(λ). Find the UMVUE of g(λ) = e^(−λ) = P(X = 0).",
 steps=L(
  {"say":"Start from any unbiased estimator, however crude.","math":"δ = 1{X₁ = 0},   E[δ] = P(X₁ = 0) = e^(−λ)  ✓",
   "why":"It does not have to be good. It has to be unbiased. The whole method is a machine for turning something unbiased into something unbiased and best."},
  {"say":"Name the complete sufficient statistic.","math":"T = ΣXᵢ ~ Poisson(nλ), complete and sufficient",
   "why":"Sufficiency makes the conditioning legal; completeness will make the answer unique. Both were established in the previous two topics."},
  {"say":"Identify the conditional distribution of X₁ given T.","math":"Given ΣXᵢ = t, (X₁,…,Xₙ) ~ Multinomial(t, 1/n, …, 1/n),  so  X₁ | T = t ~ Binomial(t, 1/n)",
   "why":"This is the step that does the work. Note there is no λ in it anywhere — that is sufficiency showing up in practice, not as an abstraction."},
  {"say":"Compute the conditional expectation.","math":"η(t) = E[ 1{X₁=0} | T = t ] = P(X₁ = 0 | T = t) = (1 − 1/n)^t = ((n−1)/n)^t",
   "why":"The expectation of an indicator is the probability of the event. A Binomial(t, 1/n) is zero with probability (1−1/n)^t."},
  {"say":"Conclude.","math":"UMVUE of e^(−λ)  =  ((n−1)/n)^T,  where T = ΣXᵢ",
   "why":"It is unbiased by the tower property, and it is a function of a complete sufficient statistic, so Lehmann–Scheffé makes it the unique best unbiased estimator."},
  {"say":"Sanity-check the shape.","math":"n = 10, T = 7  ⟹  (0.9)⁷ = 0.478,  which lies in (0,1) as a probability must",
   "why":"Compare with the estimator you started from, which would have returned 0 or 1. Same unbiasedness, enormously less variance."}),
 after="Look back at step 3. Everything turned on knowing the conditional distribution of the sample given its total, and that distribution was free of λ. That is the only place sufficiency was used, and without it the calculation could not have been done at all.")

scene(kind="recall", title="Pause and recall", mins=2,
 objective="Retrieve before reading on — this is where the retention comes from.",
 intro="Answer each in your head before revealing. Correcting a wrong retrieval beats re-reading a right answer.",
 items=L(
  {"q":"State Rao–Blackwell.","a":"If δ is unbiased for g(θ) and T is sufficient, then η(T) = E[δ|T] is unbiased and has variance no larger than δ's."},
  {"q":"Which identity proves the variance half?","a":"Var(δ) = E[Var(δ|T)] + Var(E[δ|T]). The first term is non-negative."},
  {"q":"When does Rao–Blackwell leave the estimator unchanged?","a":"When δ is already a function of T, so Var(δ|T) = 0."},
  {"q":"What does Rao–Blackwell NOT give you, and what supplies it?","a":"Uniqueness — a single best estimator. Completeness supplies it, through Lehmann–Scheffé."}))

scene(kind="completion", title="Your turn, with the scaffolding removed — estimating p²", mins=8,
 objective="Run a conditional expectation yourself, with a hypergeometric count instead of a binomial one.",
 problem="X₁,…,Xₙ are iid Bernoulli(p). Find the UMVUE of g(p) = p². Take T = ΣXᵢ, which is complete and sufficient.",
 steps=L(
  {"say":"Find a crude unbiased estimator to start from.",
   "blank":{"prompt":"Write an unbiased estimator of p² using two observations.",
     "answer":"X₁X₂",
     "accept":["X₁X₂","X1X2","X_1 X_2","x1x2","X₁·X₂","X1*X2","the product of two observations"],
     "hint":"X₁ and X₂ are independent, each with mean p. What is the expectation of their product?"},
   "why":"E[X₁X₂] = E[X₁]E[X₂] = p². Crude — it uses two observations and returns only 0 or 1 — but unbiased, which is all the method needs."},
  {"say":"Recognise what the conditional expectation is asking for.",
   "math":"E[X₁X₂ | T = t] = P(X₁ = 1 and X₂ = 1 | ΣXᵢ = t)",
   "why":"The product of two indicators is itself the indicator of both events happening, so its conditional expectation is a conditional probability."},
  {"say":"Count the arrangements.",
   "blank":{"prompt":"Write that probability as a ratio of binomial coefficients.",
     "answer":"C(n−2, t−2) / C(n, t)",
     "accept":["C(n−2, t−2) / C(n, t)","C(n-2,t-2)/C(n,t)","(n-2 choose t-2)/(n choose t)",
               "C(n-2, t-2)/C(n, t)","nCt form: C(n-2,t-2)/C(n,t)"],
     "hint":"Given t ones among n positions, every arrangement is equally likely. Fix ones in positions 1 and 2 — how many ways are left to place the rest?"},
   "why":"Conditional on the total, the pattern of ones is uniform over all C(n,t) arrangements. Fixing two of them leaves C(n−2,t−2)."},
  {"say":"Simplify.",
   "blank":{"prompt":"Simplify that ratio.",
     "answer":"t(t−1) / (n(n−1))",
     "accept":["t(t−1) / (n(n−1))","t(t-1)/(n(n-1))","T(T-1)/(n(n-1))","t(t-1)/n(n-1)"],
     "hint":"Write both coefficients as factorials and cancel. Almost everything goes; two factors survive on top and two below."},
   "why":"The factorials collapse to t(t−1)/(n(n−1)) — a clean function of T alone, as it had to be."},
  {"say":"Conclude.","math":"UMVUE of p²  =  T(T−1) / (n(n−1)),  T = ΣXᵢ",
   "why":"Unbiased and a function of a complete sufficient statistic, so Lehmann–Scheffé applies. Note it is NOT p̂² = (T/n)², which is biased upward — the UMVUE is the version with the (T−1) and the (n−1)."}),
 after="Both worked examples had the same shape: pick anything unbiased, condition on the total, and let the conditional distribution of the sample given its total do the work. Only the counting changed — binomial for the Poisson, hypergeometric here.")

scene(kind="theory", title="Lehmann–Scheffé, and when a UMVUE misbehaves", mins=9,
 objective="See exactly which word upgrades an improvement into the unique best, and learn the limits.",
 blocks=L(
  {"t":"formula","h":"Lehmann–Scheffé theorem",
   "body":"If T is a COMPLETE sufficient statistic and η(T) is unbiased for g(θ),\nthen η(T) is the UMVUE of g(θ), and it is unique with probability 1."},
  {"t":"step","h":"Why completeness gives uniqueness",
   "body":"Suppose η₁(T) and η₂(T) are both unbiased for g(θ). Then E[η₁(T) − η₂(T)] = 0 for every θ. So η₁ − η₂ is an unbiased estimator of zero that is a function of T — and completeness says the only such function is zero. Hence η₁ = η₂ almost surely."},
  {"t":"note","h":"Both routes land in the same place","body":"Route A: take any unbiased δ and compute E[δ|T]. Route B: solve E[h(T)] = g(θ) for h directly. Completeness guarantees they give the same answer, so use whichever is less algebra. Route B is usually faster when you can guess the form of h."},
  {"t":"trap","h":"A UMVUE can be absurd",
   "body":"Take a SINGLE Poisson observation, n = 1, and estimate e^(−2λ). Solving E[h(X)] = e^(−2λ) gives h(x) = (−1)^x. So the unique best unbiased estimator alternates between +1 and −1 while estimating a number strictly inside (0,1). It is the UMVUE, and it is nonsense. Unbiasedness is a constraint, not a virtue, and this example is the standard way examiners make that point."},
  {"t":"trap","h":"UMVUEs are not invariant",
   "body":"The MLE of g(θ) is g(θ̂) — that is invariance, and it holds always. The UMVUE has no such property. For U(0,θ) the UMVUE of θ is (n+1)/n·X₍ₙ₎, but the UMVUE of θ² is (n+2)/n·X₍ₙ₎², which is NOT the square of the first. Scene 11 makes you derive both."},
  {"t":"assume","h":"No complete sufficient statistic, no theorem",
   "body":"In a curved family such as N(θ,θ²), the minimal sufficient statistic is not complete, so Lehmann–Scheffé is silent. A UMVUE may still exist, but you would need a different argument to find it — and an exam will not expect you to."},
  {"t":"note","h":"Unbiased is not the same as accurate",
   "body":"For N(μ,σ²), s² = Σ(xᵢ−x̄)²/(n−1) is the UMVUE of σ², yet the MLE Σ(xᵢ−x̄)²/n has smaller mean squared error, and Σ(xᵢ−x̄)²/(n+1) is better still. UMVUE means smallest variance among UNBIASED estimators only. Drop the unbiasedness requirement and you can usually do better."}))

scene(kind="explore", title="Where the complete sufficient statistic is an order statistic", mins=6,
 objective="Apply Lehmann–Scheffé by the direct route, with no conditioning at all.",
 viz={"type":"unif-likelihood","n":6,"xmax":4.2},
 body=L(
  "X₁,…,Xₙ are iid U(0, θ). The likelihood is the cliff on screen, and X₍ₙ₎ is complete and sufficient — both established in the previous two topics.",
  "Here Route B is far easier than conditioning. Write the density of the maximum: f(x) = n x^(n−1)/θⁿ on (0, θ). Then E[X₍ₙ₎] = ∫₀^θ x · n x^(n−1)/θⁿ dx = nθ/(n+1).",
  "So X₍ₙ₎ understates θ by the factor n/(n+1), and multiplying it back gives an unbiased estimator: (n+1)/n · X₍ₙ₎. It is an unbiased function of a complete sufficient statistic, so Lehmann–Scheffé makes it the UMVUE. No conditional expectation was needed anywhere.",
  "Drag the maximum and watch the whole likelihood follow it. Everything the data say about θ is in that one number — which is why an estimator built on it can be best.",
  "Compare with the MLE, which is X₍ₙ₎ itself. It can never exceed θ, so it is biased low at every n. The UMVUE is the same statistic with the bias scaled out, exactly as in the exponential case in scene 2."),
 ask={"q":"The MLE here is X₍ₙ₎ and the UMVUE is (n+1)/n·X₍ₙ₎. Both are functions of the same statistic. Why is only one of them unbiased?",
      "nudge":"The maximum of n draws from (0,θ) sits below θ with probability 1. What does that force its expectation to be?"})

scene(kind="guided", title="Now without the steps — the UMVUE of μ²", mins=8,
 objective="Choose the direct route yourself, and remember the correction term.",
 problem="X₁,…,Xₙ are iid N(μ, σ²) with σ² KNOWN. Find the UMVUE of μ².",
 hints=L(
  "Direction — first name the complete sufficient statistic for μ when σ² is known. Then write down the obvious candidate for estimating μ² and ask whether it is actually unbiased, rather than assuming it.",
  "Method — Route B. You want h with E[h(X̄)] = μ². Start from E[X̄²] and use the identity E[Y²] = Var(Y) + (E[Y])². The gap you find is the correction you must subtract.",
  "Next step — X̄ ~ N(μ, σ²/n), so Var(X̄) = σ²/n. Put that into the identity and read off what has to come off X̄²."),
 solution=L(
  {"say":"Complete sufficient statistic.","math":"σ² known ⟹ the family is a full-rank one-parameter exponential family, so X̄ is complete and sufficient for μ."},
  {"say":"Test the obvious candidate.","math":"E[X̄²] = Var(X̄) + (E[X̄])² = σ²/n + μ²  ≠ μ²"},
  {"say":"Correct the bias.","math":"E[ X̄² − σ²/n ] = μ²   ✓"},
  {"say":"Apply Lehmann–Scheffé.","math":"X̄² − σ²/n is an unbiased function of a complete sufficient statistic ⟹ it is the UMVUE of μ²."}),
 answer="The UMVUE of μ² is X̄² − σ²/n.",
 check="Two things to verify before you move on. First, the correction term is σ²/n, not σ² — the variance of the MEAN, not of one observation. Second, this estimator can come out negative when x̄² < σ²/n, even though μ² cannot be. That is not an error in your working; it is a genuine wart of unbiased estimation, and a question may ask you to comment on it.")

scene(kind="trapcheck", title="Six statements — verdict on each before you look", mins=6,
 objective="Practise the per-statement discipline the real multi-statement items demand.",
 intro="Give every statement a true or false verdict first. In the exam these six would be one question scored all or nothing, so a verdict you skipped is a mark you gambled.",
 items=L(
  {"claim":"Rao–Blackwell requires the conditioning statistic to be sufficient.","tf":True,
   "why":"True, and it is the condition that makes the result a statistic at all. Without sufficiency, E[δ|T] still contains θ."},
  {"claim":"Rao–Blackwellising an unbiased estimator can increase its variance.","tf":False,
   "why":"False. Var(δ) = E[Var(δ|T)] + Var(η), and the first term is non-negative, so Var(η) ≤ Var(δ) always."},
  {"claim":"Rao–Blackwell applied to a sufficient but not complete statistic still produces an improvement.","tf":True,
   "why":"True — the variance inequality needs only sufficiency. What you lose without completeness is uniqueness: different starting estimators may give different answers, none of them identifiable as best."},
  {"claim":"Lehmann–Scheffé requires the statistic to be complete as well as sufficient.","tf":True,
   "why":"True. Completeness is exactly what forces two unbiased functions of T to coincide, which is where uniqueness comes from."},
  {"claim":"A UMVUE, when it exists, is always a sensible estimator of the quantity concerned.","tf":False,
   "why":"False. For a single Poisson observation the UMVUE of e^(−2λ) is (−1)^X, which alternates ±1 while estimating a number in (0,1). Unbiasedness is a constraint, not a guarantee of good behaviour."},
  {"claim":"If η is the UMVUE of θ, then η² is the UMVUE of θ².","tf":False,
   "why":"False. That is invariance, which the MLE has and the UMVUE does not. For U(0,θ) the UMVUE of θ² is (n+2)/n·X₍ₙ₎², not the square of (n+1)/n·X₍ₙ₎."}))

scene(kind="guided", title="Transfer — the UMVUE of θ², and why it is not the square", mins=9,
 objective="Derive a second UMVUE in the same family, and see invariance fail in front of you.",
 problem="X₁,…,Xₙ are iid U(0, θ). Scene 8 gave the UMVUE of θ as (n+1)/n · X₍ₙ₎. Now find the UMVUE of θ², and compare it with the square of that estimator.",
 hints=L(
  "Direction — do not square anything yet. Go back to the definition: you need a function of the complete sufficient statistic whose expectation is exactly θ². The natural candidate is a multiple of X₍ₙ₎².",
  "Method — Route B again. Compute E[X₍ₙ₎²] from the density of the maximum, then scale it so the expectation lands on θ² exactly.",
  "Next step — the density of X₍ₙ₎ is n x^(n−1)/θⁿ on (0, θ). Integrate x² against it; the integral is elementary and the θ's mostly cancel."),
 solution=L(
  {"say":"Expectation of the squared maximum.","math":"E[X₍ₙ₎²] = ∫₀^θ x² · n x^(n−1)/θⁿ dx = (n/θⁿ) · [x^(n+2)/(n+2)]₀^θ = n θ² / (n+2)"},
  {"say":"Scale it to be unbiased.","math":"E[ (n+2)/n · X₍ₙ₎² ] = θ²   ✓"},
  {"say":"Apply Lehmann–Scheffé.","math":"UMVUE of θ²  =  (n+2)/n · X₍ₙ₎²"},
  {"say":"Now square the UMVUE of θ and compare.","math":"[ (n+1)/n · X₍ₙ₎ ]² = (n+1)²/n² · X₍ₙ₎²   versus   (n+2)/n · X₍ₙ₎² = n(n+2)/n² · X₍ₙ₎²"},
  {"say":"They differ.","math":"(n+1)² = n² + 2n + 1   and   n(n+2) = n² + 2n.   The squared estimator is larger by X₍ₙ₎²/n², so it is biased upward for θ²."}),
 answer="The UMVUE of θ² is (n+2)/n · X₍ₙ₎². Squaring the UMVUE of θ gives (n+1)²/n² · X₍ₙ₎², which overstates θ² by X₍ₙ₎²/n² on average and is therefore not the UMVUE.",
 check="The comparison was part of the question, not a flourish — answering with the formula alone leaves marks on the table. And notice what this kills: the habit, built up in the MLE topic, of transforming an estimator and keeping the label. The MLE is invariant; the UMVUE is not. If a question asks for the UMVUE of a function of θ, you must derive it from scratch.")

scene(kind="summary", title="What you should now be able to do unaided", mins=3,
 objective="Close the loop before the test.",
 body=L(
  "Write down any unbiased estimator, however crude, and improve it by conditioning on a sufficient statistic.",
  "Prove Rao–Blackwell from the variance decomposition in one line, and say when the inequality is an equality.",
  "Compute E[δ|T] in the standard cases by identifying the conditional distribution of the sample given its total.",
  "State Lehmann–Scheffé and explain that completeness, not sufficiency, is what delivers uniqueness.",
  "Reach for the direct route — solve E[h(T)] = g(θ) — whenever guessing the form of h is easier than conditioning.",
  "Refuse to square a UMVUE and call the result a UMVUE, and refuse to assume a UMVUE beats the MLE on mean squared error.",
  "The mastery test is ten unseen questions across all of this. Hints are off. The pass is 80% overall with 70% floors on the numerical and multi-statement items."))

scene(kind="quiz", title="Mastery test", mins=12,
 objective="Demonstrate it independently, on unseen questions.",
 setId="inference_t3_mastery")

lesson["scenes"]=S

def m(i,fmt,stem,options,ans,expl,**kw):
    d={"id":"inf-t3-m-%02d"%i,"format":fmt,"topic":"inference-t3","stem":stem,
       "options":options,"answer":ans,"explanation":expl}
    d.update(kw); return d

mastery=[
 m(1,"single","Rao–Blackwell guarantees that η(T) = E[δ(X) | T] satisfies:",
   ["η is unbiased and Var(η) ≤ Var(δ), provided T is sufficient",
    "η is unbiased and Var(η) < Var(δ), for any statistic T",
    "η has smaller mean squared error than δ, provided T is complete",
    "η is the UMVUE, provided T is sufficient"],
   "A","Unbiasedness comes from the tower property; the variance inequality from Var(δ) = E[Var(δ|T)] + Var(η). Option B overstates it twice: the inequality is not strict, and T must be sufficient or η is not even a statistic. Option D skips completeness, without which there is no uniqueness and so no UMVUE claim."),
 m(2,"numeric","X₁,…,X₅ are iid Poisson(λ) with ΣXᵢ = 3. The UMVUE of e^(−λ) is ((n−1)/n)^T. Give its value.",
   ["0.512","0.549","0.216","0.600"],
   "A","((n−1)/n)^T = (4/5)³ = 0.512. Option B is e^(−0.6), the plug-in estimate e^(−λ̂) with λ̂ = x̄ = 0.6 — a perfectly reasonable estimator but a biased one, and not the UMVUE. Option C is (3/5)³ and option D is x̄ itself.",
   check="The base is (n−1)/n = 4/5, not x̄ and not T/n. Confirm which of n and T goes in the exponent before you compute."),
 m(3,"multi","Consider Lehmann–Scheffé and the UMVUEs it produces.",
   ["A, C and D only","A and B only","B and C only","A, B and D only"],"A",
   "A is true — that is the statement. B is false: completeness is required, and without it the theorem is silent. C is true, and is the standard pathology. D is true — the UMVUE is not invariant, unlike the MLE.",
   statements=["If T is complete sufficient and η(T) is unbiased for g(θ), then η(T) is the unique UMVUE.",
               "Sufficiency of T alone is enough for the uniqueness conclusion.",
               "A UMVUE can take values outside the range of the quantity it estimates.",
               "The UMVUE of g(θ) need not equal g applied to the UMVUE of θ."],
   verdicts={"A":{"tf":True,"why":"The theorem exactly as stated, with uniqueness holding almost surely."},
             "B":{"tf":False,"why":"Without completeness you get Rao–Blackwell's improvement but no uniqueness."},
             "C":{"tf":True,"why":"X̄² − σ²/n can be negative while μ² cannot; (−1)^X estimates a number in (0,1)."},
             "D":{"tf":True,"why":"UMVUEs are not invariant. For U(0,θ), the UMVUE of θ² is (n+2)/n·X₍ₙ₎², not the square of the UMVUE of θ."}}),
 m(4,"numeric","X₁,…,X₆ are iid Bernoulli(p) with ΣXᵢ = 4. The UMVUE of p² is T(T−1)/(n(n−1)). Give its value, and say how it compares with p̂².",
   ["0.400, which is smaller than p̂² = 0.444","0.444, which equals p̂²",
    "0.400, which is larger than p̂² = 0.333","0.267, which is smaller than p̂² = 0.444"],
   "A","T(T−1)/(n(n−1)) = 4·3/(6·5) = 12/30 = 0.400, while p̂² = (4/6)² = 0.444. The plug-in estimator is biased upward for p², and the UMVUE sits below it — which is the correction the (T−1) and (n−1) supply.",
   check="Two parts: the value and the comparison. If you computed only 0.4, confirm p̂² before choosing, because three options carry that same number."),
 m(5,"single","For which situation does Lehmann–Scheffé fail to deliver a UMVUE?",
   ["N(θ, θ²) with θ > 0, where the minimal sufficient statistic is not complete",
    "Poisson(λ), where T = ΣXᵢ is complete sufficient",
    "U(0, θ), where X₍ₙ₎ is complete sufficient",
    "Bernoulli(p), where T = ΣXᵢ is complete sufficient"],
   "A","N(θ,θ²) is a curved exponential family: (ΣXᵢ, ΣXᵢ²) is minimal sufficient but not complete, so the theorem has nothing to act on. A UMVUE may still exist, but Lehmann–Scheffé cannot identify it. The other three are full-rank families whose sufficient statistic is complete."),
 m(6,"numeric","X₁,…,X₈ are iid U(0,θ) with sample maximum x₍₈₎ = 6. Give the UMVUE of θ and the MLE of θ.",
   ["UMVUE = 6.75, MLE = 6","UMVUE = 6, MLE = 6.75",
    "UMVUE = 5.33, MLE = 6","UMVUE = 6.75, MLE = 6.75"],
   "A","The UMVUE is (n+1)/n · x₍ₙ₎ = (9/8)(6) = 6.75; the MLE is x₍ₙ₎ = 6 itself. The UMVUE must exceed the sample maximum, because the maximum can never exceed θ and so understates it. Option C scales the wrong way, making the bias worse.",
   check="The multiplier is (n+1)/n = 9/8, greater than 1. Any answer below the sample maximum is wrong on sight."),
 m(7,"multi","Let δ be an unbiased estimator of g(θ) and let T be a statistic.",
   ["B and C only","A and B only","A, B and C only","C and D only"],"A",
   "A is false — equality holds whenever δ is already a function of T, so the improvement need not be strict. B is true, by the tower property. C is true, and is the point of requiring sufficiency. D is false: unbiasedness restricts the comparison to unbiased estimators, and a biased estimator can have smaller MSE.",
   statements=["Rao–Blackwellising always strictly reduces the variance.",
               "E[E[δ|T]] = g(θ) whenever δ is unbiased.",
               "If T is not sufficient, E[δ|T] may depend on θ and so may not be a statistic.",
               "A UMVUE has the smallest mean squared error among all estimators."],
   verdicts={"A":{"tf":False,"why":"It is ≤. Equality when Var(δ|T) = 0, i.e. δ already depends on the data only through T."},
             "B":{"tf":True,"why":"The tower property, needing nothing beyond δ being unbiased."},
             "C":{"tf":True,"why":"Sufficiency is exactly what frees the conditional distribution of θ."},
             "D":{"tf":False,"why":"Smallest variance among UNBIASED estimators only. The MLE of σ² beats s² on MSE."}}),
 m(8,"numeric","X₁,…,X₆ are iid Exponential with rate λ and Σxᵢ = 24. Give the MLE of λ and the UMVUE of λ.",
   ["MLE = 0.250, UMVUE = 0.2083","MLE = 0.2083, UMVUE = 0.250",
    "MLE = 0.250, UMVUE = 0.250","MLE = 4.000, UMVUE = 4.800"],
   "A","The MLE is n/Σxᵢ = 6/24 = 0.250. Since E[1/ΣX] = λ/(n−1), the unbiased version is (n−1)/Σxᵢ = 5/24 = 0.2083, and ΣX is complete sufficient so Lehmann–Scheffé makes it the UMVUE. Option B swaps them; option D gives the mean 1/λ rather than the rate.",
   check="The UMVUE is the MLE shrunk by (n−1)/n, so it must be the SMALLER of the two. If your UMVUE came out larger, you scaled the wrong way."),
 m(9,"numeric","X₁,…,X₁₀ are iid N(μ, σ²) with σ² = 5 known, and x̄ = 4. Give the UMVUE of μ².",
   ["15.5","16.0","11.0","16.5"],
   "A","X̄ is complete sufficient for μ. E[X̄²] = Var(X̄) + μ² = σ²/n + μ², so the UMVUE is x̄² − σ²/n = 16 − 5/10 = 15.5. Option B is x̄² itself, which overstates μ² by σ²/n. Option C subtracts σ² rather than σ²/n.",
   check="The correction is the variance of the MEAN, σ²/n = 0.5, not σ² = 5. Subtracting the wrong one is the commonest slip in this item."),
 m(10,"order","To find a UMVUE by Rao–Blackwellisation, arrange these steps in the order they are carried out.",
   ["C, A, D, B","A, C, D, B","C, D, A, B","D, C, A, B"],"A",
   "Identify the complete sufficient statistic first — it determines whether the method applies at all and what you will condition on. Then find any unbiased estimator, compute the conditional expectation, and finally invoke Lehmann–Scheffé. Starting by hunting for an unbiased estimator wastes effort if no complete sufficient statistic exists.",
   items=["A. Find any unbiased estimator δ of g(θ), however crude",
          "B. Invoke Lehmann–Scheffé to declare the result the UMVUE",
          "C. Identify a complete sufficient statistic T",
          "D. Compute η(T) = E[δ | T] using the conditional distribution given T"]),
]

body={"moduleId":"inference","source":"mastery","topicId":"inference-t3",
      "label":"Rao–Blackwell and Lehmann–Scheffé — mastery test (unseen)","count":len(mastery),"items":mastery}
with open(os.path.join(OUT,"inference_t3_mastery.json"),"w") as f:
    json.dump(body,f,ensure_ascii=False,indent=1)
with open(os.path.join(OUT,"lesson_t3.json"),"w") as f:
    json.dump(lesson,f,ensure_ascii=False,indent=1)
fm={}
for i in mastery: fm[i["format"]]=fm.get(i["format"],0)+1
print("scenes:",len(S),"->"," ".join(x["kind"] for x in S))
print("mastery:",len(mastery),fm)
print("bytes:",os.path.getsize(os.path.join(OUT,"lesson_t3.json")))
