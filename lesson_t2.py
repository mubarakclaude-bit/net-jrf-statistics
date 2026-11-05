# lessons/inferencet2 — Completeness, exponential families, ancillarity, Basu
# plus qsets/inference_t2_mastery
import json, os
OUT = "/home/claude/w1/seed"
L = lambda *p: list(p)

lesson = {
 "id":"inferencet2","moduleId":"inference","topicId":"inference-t2",
 "title":"Completeness, Exponential Families, Ancillarity and Basu",
 "breadcrumb":"Statistical Inference → Data Reduction → Completeness",
 "engine":"B",
 "engineName":"Estimation and inference — likelihood families, and what makes one rich enough to pin an estimator down",
 "estMin":45,"version":"1.0","status":"approved",
 "provenance":"Theory, worked examples and practice authored for this platform against the UGC NET Statistics syllabus. Previous-year questions are stored separately and carry their exam cycle.",
 "objectives":L(
   "State completeness as a property of a family of distributions, and say why it is not a property of a statistic on its own.",
   "Prove a statistic complete by the standard route: set E[g(T)] = 0, and use uniqueness of a power series, a polynomial or an integral.",
   "Read completeness off the exponential-family form, and recognise a curved family where that argument fails.",
   "Identify an ancillary statistic and apply Basu's theorem to get independence without touching a joint density.",
   "Disprove completeness by constructing a non-trivial unbiased estimator of zero.",
   "Keep sufficient, minimal, complete and ancillary apart — the exam tests the boundaries, not the definitions."),
 "prereq":L(
   {"id":"p1","name":"Sufficiency and the factorisation theorem","why":"Completeness is always asked about a sufficient statistic. If finding T is still slow, do the sufficiency topic first."},
   {"id":"p2","name":"Expectation of a function of a statistic","why":"Every completeness proof starts by writing E[g(T)] out as a sum or an integral."},
   {"id":"p3","name":"Power series and polynomial identities","why":"The proofs all end the same way: a series that vanishes on an interval has every coefficient zero. That step is the whole argument."}),
 "mastery":{"minQ":10,"pass":80,"fmtMin":{"numeric":70,"multi":70},"noHints":True,"retestDays":7,
   "note":"Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints."},
 "refs":L(
  {"title":"The Exponential Criterion","where":"Lesson 24.3","site":"Penn State STAT 415 online notes",
   "url":"https://online.stat.psu.edu/stat415/lesson/24/24.3","type":"Course notes","free":True,"checked":"2026-10-12",
   "why":"Puts Bernoulli, Poisson, Normal, Exponential and Geometric into exponential form one at a time. Read it alongside scene 7 if rearranging a density into h(x)c(θ)exp(Σw t) is the step that slows you down."},
  {"title":"Mathematical Statistics — Exponential Families I and II","where":"Lecture notes 7 and 8",
   "site":"MIT OpenCourseWare 18.655 (Spring 2016)","url":"https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/pages/lecture-notes/",
   "type":"Lecture notes","free":True,"checked":"2026-10-12",
   "why":"The natural parameter space and the full-rank condition stated properly. This is the source for the completeness criterion in scene 7, and for why curved families fall outside it."},
  {"title":"Mathematical Statistics — Unbiased Estimation and Risk Inequalities","where":"Lecture note 13",
   "site":"MIT OpenCourseWare 18.655 (Spring 2016)","url":"https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/pages/lecture-notes/",
   "type":"Lecture notes","free":True,"checked":"2026-10-12",
   "why":"Where completeness earns its keep: Rao–Blackwell and Lehmann–Scheffé. Reach for it after scene 1, when you want to see the payoff before doing the proofs."}),
 "revision":{
  "sheet":L(
    "T is complete if E_θ[g(T)] = 0 for every θ forces g(T) = 0 with probability 1.",
    "Completeness is a property of the FAMILY {f_T(t;θ) : θ ∈ Θ}, never of T by itself.",
    "In words: the only unbiased estimator of zero that is a function of T is zero itself.",
    "That uniqueness is what makes Lehmann–Scheffé give ONE best unbiased estimator.",
    "Proof route: write E[g(T)] = 0, then use uniqueness — power series (Poisson), polynomial (Binomial), differentiate under the integral (Uniform).",
    "Full-rank k-parameter exponential family ⟹ (Σt₁, …, Σt_k) is complete AND minimal sufficient.",
    "Full rank means the natural parameter space contains an open k-dimensional rectangle.",
    "Curved family (dim T > dim θ, e.g. N(θ,θ²)) ⟹ minimal sufficient but NOT complete.",
    "Ancillary: the distribution of A does not depend on θ at all.",
    "Basu: T complete sufficient, A ancillary ⟹ T and A are independent, for every θ.",
    "Complete sufficient ⟹ minimal sufficient (Bahadur). The converse is false.",
    "To DISPROVE completeness, build one non-zero g with E[g(T)] = 0 for all θ — an ancillary function of T minus its mean does it."),
  "cards":L(
    ["Completeness in one sentence","If a function of T averages to zero under every θ in the family, that function must be zero."],
    ["Whose property is completeness?","The family's, not the statistic's. The same T can be complete under one family and not under another."],
    ["Why we want it","It makes the unbiased estimator built on T unique, which is what turns Rao–Blackwell into Lehmann–Scheffé."],
    ["Standard proof ending","A power series or polynomial that vanishes on an interval has every coefficient zero."],
    ["Exponential-family criterion","Full rank — the natural parameter space holds an open k-dimensional rectangle — gives completeness and minimal sufficiency together."],
    ["Ancillary statistic","One whose distribution is free of θ. For U(0,θ), X₍₁₎/X₍ₙ₎ is ancillary because θ cancels."],
    ["Basu's theorem","Complete sufficient T is independent of every ancillary A — no joint density needed."],
    ["How to disprove completeness","Find a non-trivial g(T) with mean zero for all θ. For U(θ,θ+1), the range minus (n−1)/(n+1) does it."])},
 "traps":L(
   "Calling a statistic complete without naming the family it is complete for.",
   "Assuming minimal sufficient implies complete — curved families are the counterexample.",
   "Applying the exponential-family criterion to a family whose support moves with θ.",
   "Forgetting that the natural parameter space must contain an open rectangle, not just two or three points.",
   "Using Basu without checking that T is complete as well as sufficient.",
   "Treating 'ancillary' as 'useless' — an ancillary statistic is exactly what Basu needs, and it can still matter when you condition.",
   "Proving E[g(T)] = 0 for one θ and concluding completeness. It must hold for every θ in Θ."),
}

S=[]
def scene(**kw):
    kw.setdefault("id","s%d"%(len(S)+1)); S.append(kw); return kw

scene(kind="intuition", title="A family too rich to hide anything in", mins=5,
 objective="Meet completeness as a statement about a whole family of distributions.",
 body=L(
  "Suppose you have a sufficient statistic T, and someone hands you a function g and claims that E[g(T)] = 0. If they mean under one particular θ, that is easy — plenty of non-zero functions average to zero somewhere.",
  "Now make the claim far harder. Insist that E_θ[g(T)] = 0 for EVERY θ in the family. One function, one equation, but the equation has to hold simultaneously across the whole parameter space.",
  "For a rich enough family, that is impossible unless g was zero all along. The distributions of T move around so much as θ varies that no fixed non-zero function can keep averaging to zero against all of them. A family with that property is called complete.",
  "This is why the property belongs to the family and not to T. The same statistic can be complete under one model and fail under another, because what changed was the collection of distributions, not the function of the data.",
  "The payoff is uniqueness. Rao–Blackwell says conditioning an unbiased estimator on a sufficient statistic cannot make it worse. Completeness says there is only one unbiased function of T to land on — so the improvement has a single destination. That is Lehmann–Scheffé, and it is the reason this definition is in the syllabus at all."),
 aside={"h":"The phrasing that makes the definition click",
   "body":"Read E_θ[g(T)] = 0 ∀θ ⟹ g ≡ 0 as: the only unbiased estimator of zero that depends on the data through T is the trivial one. If a second one existed, you could add it to any unbiased estimator and get a different unbiased estimator — and uniqueness would be gone."},
 ask={"q":"Why does 'the only unbiased estimator of zero is zero' force the unbiased estimator built on T to be unique?",
      "nudge":"Suppose two different unbiased estimators of θ were both functions of T. What is the expectation of their difference?"})

scene(kind="explore", title="A family of likelihoods that sweeps the whole line", mins=5,
 objective="See the richness that completeness is really asking for.",
 viz={"type":"exp-likelihood","n":4,"sumx":16.0},
 body=L(
  "This is the exponential sample again: L(λ) = λⁿ e^(−λΣxᵢ). The data reach it only through n and Σxᵢ, so Σxᵢ is sufficient — that much is the previous topic.",
  "Completeness asks something extra, and it is about the curve rather than the data. Drag λ and notice that the family of densities of T = ΣXᵢ really does move: T is Gamma(n, λ), and as λ runs over all of (0, ∞) the natural parameter −λ sweeps an entire open interval.",
  "That sweep is the condition. A one-parameter exponential family whose natural parameter covers an open interval is full rank, and its sufficient statistic is complete. Nothing non-trivial can average to zero against all of those distributions at once.",
  "Contrast it with a family where λ were allowed only two values. Sufficiency would be unchanged — the likelihood still sees only Σxᵢ — but two equations cannot pin a whole function down, and completeness would fail. Same statistic, different family, different answer."),
 ask={"q":"Sufficiency and completeness are both being claimed for Σxᵢ here. Which of the two would survive if λ were restricted to {1, 2}, and which would not?",
      "nudge":"Does restricting θ change how the data enter the likelihood? Does it change how many equations E[g(T)] = 0 has to satisfy?"})

scene(kind="theory", title="The definition, and the one proof technique", mins=7,
 objective="Hold the definition precisely, and learn the single argument that closes every proof.",
 blocks=L(
  {"t":"def","h":"Completeness","body":"A family of distributions {f_T(t; θ) : θ ∈ Θ} is complete if, for every measurable g, E_θ[g(T)] = 0 for all θ ∈ Θ implies P_θ(g(T) = 0) = 1 for all θ ∈ Θ. Loosely, 'T is complete' always means its family is."},
  {"t":"note","h":"Bounded completeness","body":"The same condition restricted to bounded g. It is weaker, and it is all Basu's theorem actually needs. Exam questions use full completeness; be aware the distinction exists."},
  {"t":"step","h":"The proof route, every time","body":"1. Write E_θ[g(T)] = 0 explicitly as a sum or integral over t.   2. Strip off every factor that does not involve t.   3. Recognise what is left as a power series, a polynomial, or an integral that must vanish for all θ.   4. Invoke uniqueness: a series vanishing on an interval has all coefficients zero; an integral vanishing for all upper limits has a zero integrand.   5. Conclude g(t) = 0 at every t the statistic can take."},
  {"t":"formula","h":"The three endings you will actually use",
   "body":"Poisson  →  Σ_t a_t λ^t ≡ 0 on an interval ⟹ every a_t = 0\nBinomial →  Σ_t a_t r^t ≡ 0 on an interval ⟹ every a_t = 0  (after r = p/(1−p))\nUniform  →  ∫₀^θ g(x)x^(n−1) dx ≡ 0 for all θ ⟹ differentiate in θ ⟹ g ≡ 0"},
  {"t":"assume","h":"For all θ, not for some θ","body":"The quantifier is the whole content. E[g(T)] = 0 at a single θ says almost nothing. Questions are written so that a candidate who drops the quantifier reaches a confident wrong answer."},
  {"t":"trap","h":"Completeness does not follow from sufficiency","body":"Nor from minimal sufficiency. They are separate properties and the exam exploits the gap: a curved exponential family has a minimal sufficient statistic that is not complete. The implication runs the other way — complete and sufficient implies minimal sufficient (Bahadur's theorem) — and the converse is false."}))

scene(kind="worked", title="Worked in full — Σxᵢ is complete for the Poisson", mins=6,
 objective="See the five steps executed once, with the uniqueness argument spelled out.",
 problem="X₁,…,Xₙ are iid Poisson(λ), λ > 0. Show that T = ΣXᵢ is a complete sufficient statistic for λ.",
 steps=L(
  {"say":"Identify the distribution of T.","math":"T = ΣXᵢ ~ Poisson(nλ),   P(T = t) = e^(−nλ) (nλ)^t / t!,  t = 0,1,2,…",
   "why":"Sums of independent Poissons are Poisson with the parameters added. Completeness is a statement about the family of distributions of T, so you need that family written down before anything else."},
  {"say":"Write the condition out in full.","math":"E_λ[g(T)] = Σ_{t≥0} g(t) · e^(−nλ) (nλ)^t / t! = 0   for every λ > 0",
   "why":"Nothing clever — just the definition of expectation for a discrete statistic. The quantifier 'for every λ > 0' is doing all the work and must be carried through."},
  {"say":"Strip the factor that does not involve t.","math":"e^(−nλ) > 0, so divide it out:   Σ_{t≥0} [ g(t) nᵗ / t! ] λ^t = 0   for every λ > 0",
   "why":"Dividing by a strictly positive quantity cannot change whether the rest is zero. What remains is a power series in λ with coefficients a_t = g(t)nᵗ/t!."},
  {"say":"Apply uniqueness of power series.","math":"A power series vanishing on an open interval has every coefficient zero:   g(t) nᵗ / t! = 0  for every t",
   "why":"This is the step the whole proof exists for. It is only available because the identity holds for a continuum of λ — one value, or even a hundred, would not do it."},
  {"say":"Conclude.","math":"nᵗ > 0 and t! > 0, so g(t) = 0 for every t = 0,1,2,…   Hence T is complete.",
   "why":"g vanishes at every point T can take, which is exactly P(g(T) = 0) = 1. Sufficiency came from factorisation in the previous topic, so T is complete AND sufficient."}),
 after="Look back at where the family's richness entered: step 4, and nowhere else. Steps 1 to 3 are bookkeeping. If you ever find a proof of completeness that never uses 'for all θ', you have made an error.")

scene(kind="recall", title="Pause and recall", mins=2,
 objective="Retrieve before reading on — this is where the retention comes from.",
 intro="Answer each in your head before revealing. Correcting a wrong retrieval beats re-reading a right answer.",
 items=L(
  {"q":"State completeness.","a":"E_θ[g(T)] = 0 for every θ in Θ implies g(T) = 0 with probability 1."},
  {"q":"Is completeness a property of T, or of something else?","a":"Of the family of distributions of T. The same statistic can be complete under one family and not under another."},
  {"q":"Which step of a completeness proof actually uses 'for all θ'?","a":"The uniqueness step — a power series or polynomial vanishing on an interval has every coefficient zero."},
  {"q":"Complete sufficient implies minimal sufficient. Does the converse hold?","a":"No. A curved exponential family such as N(θ,θ²) has a minimal sufficient statistic that is not complete."}))

scene(kind="completion", title="Your turn, with the scaffolding removed — the Bernoulli", mins=8,
 objective="Run the same argument where the ending is a polynomial rather than a power series.",
 problem="X₁,…,Xₙ are iid Bernoulli(p), 0 < p < 1. Show that T = ΣXᵢ is complete.",
 steps=L(
  {"say":"Identify the distribution of T and write the condition.",
   "math":"T ~ Binomial(n, p):   E_p[g(T)] = Σ_{t=0}^{n} g(t) C(n,t) p^t (1−p)^(n−t) = 0   for every p ∈ (0,1)",
   "why":"A finite sum this time, not an infinite series — which is why the ending will be a polynomial identity rather than a power series one."},
  {"say":"Divide through by (1−p)^n, which is strictly positive on (0,1).",
   "blank":{"prompt":"Write what the sum becomes. Use r for p/(1−p).",
     "answer":"Σ g(t) C(n,t) r^t = 0",
     "accept":["Σ g(t) C(n,t) r^t = 0","sum g(t) C(n,t) r^t = 0","Σ_{t=0}^n g(t)C(n,t)r^t=0",
               "Σ g(t) nCt r^t = 0","sum_{t=0}^{n} g(t) C(n,t) r^t = 0","Σg(t)C(n,t)r^t=0"],
     "hint":"p^t(1−p)^(n−t) ÷ (1−p)^n = p^t(1−p)^(−t) = (p/(1−p))^t. Everything else is unchanged."},
   "why":"The substitution turns a two-variable mess into a clean polynomial in a single variable r."},
  {"say":"Note the range of r.","math":"As p runs over (0,1), r = p/(1−p) runs over all of (0, ∞)",
   "why":"This is the quantifier arriving in its new clothes. The identity now holds on an open interval of r, which is exactly what the uniqueness argument needs."},
  {"say":"Apply uniqueness of polynomials.",
   "blank":{"prompt":"What must be true of every coefficient?",
     "answer":"g(t) C(n,t) = 0 for every t",
     "accept":["g(t) C(n,t) = 0 for every t","g(t)C(n,t)=0","every coefficient is zero","g(t) C(n,t) = 0",
               "all coefficients are zero","g(t)*C(n,t)=0 for all t"],
     "hint":"A polynomial of degree n that vanishes at infinitely many points is the zero polynomial — so every coefficient vanishes."},
   "why":"A non-zero polynomial of degree n has at most n roots. Vanishing on a whole interval leaves only the zero polynomial."},
  {"say":"Conclude.",
   "blank":{"prompt":"What does that give for g?",
     "answer":"g(t) = 0 for t = 0,1,…,n",
     "accept":["g(t) = 0 for t = 0,1,…,n","g(t)=0 for all t","g(t) = 0","g is identically zero",
               "g(t)=0 for t=0..n","g ≡ 0"],
     "hint":"C(n,t) is never zero for t between 0 and n, so the other factor must be."},
   "why":"g vanishes at every value T can take, so T is complete. Sufficiency came from factorisation, so T is complete and sufficient — and Lehmann–Scheffé now applies."}),
 after="Poisson ended in a power series, Bernoulli in a polynomial. Same five steps, different uniqueness theorem at the end. When you meet a new family, the only question is which uniqueness result closes it.")

scene(kind="theory", title="Exponential families, ancillarity, and Basu", mins=9,
 objective="Get completeness without proving it, and get independence without a joint density.",
 blocks=L(
  {"t":"def","h":"k-parameter exponential family",
   "body":"f(x; θ) = h(x) · c(θ) · exp( Σ_{j=1}^{k} w_j(θ) t_j(x) ). The vector (w₁(θ),…,w_k(θ)) is the natural parameter, and the set of values it takes as θ ranges over Θ is the natural parameter space."},
  {"t":"formula","h":"The criterion that saves the proof",
   "body":"If the natural parameter space contains an open k-dimensional rectangle, the family is FULL RANK, and\nT = ( Σᵢ t₁(xᵢ), …, Σᵢ t_k(xᵢ) )  is complete AND minimal sufficient."},
  {"t":"assume","h":"What full rank is really asking","body":"That the natural parameter genuinely moves in k independent directions. Two isolated values are not an interval; a curve inside a plane is not a rectangle. This is the condition candidates skip, and it is the condition the curved-family questions turn on."},
  {"t":"trap","h":"Curved families","body":"If dim(T) > dim(θ) the natural parameter traces a lower-dimensional curve and the family is not full rank. N(θ, θ²) has T = (ΣXᵢ, ΣXᵢ²) with w₁ = −1/(2θ²), w₂ = 1/θ satisfying w₁ = −w₂²/2 — a curve in the plane, not a rectangle. T stays minimal sufficient and is NOT complete, so Lehmann–Scheffé gives you nothing there."},
  {"t":"def","h":"Ancillary statistic","body":"A statistic A whose distribution does not depend on θ at all. For a location family, the differences Xᵢ − X̄ are ancillary; for a scale family such as U(0,θ), the ratio X₍₁₎/X₍ₙ₎ is ancillary, because θ cancels."},
  {"t":"formula","h":"Basu's theorem","body":"If T is a complete sufficient statistic for θ and A is ancillary, then T and A are independent — for every θ."},
  {"t":"note","h":"Why Basu is worth memorising","body":"It proves independence without anyone computing a joint density. The textbook proof that X̄ and S² are independent for a normal sample is a page of algebra or an orthogonal-transformation argument; Basu does it in three lines. In an exam that is the difference between finishing the question and not."},
  {"t":"trap","h":"Both conditions, every time","body":"Sufficient alone will not do, and complete alone will not do. If a question offers a sufficient statistic that is not complete — a curved family, or U(θ,θ+1) — Basu does not apply and any independence you claim is unjustified."}))

scene(kind="explore", title="Where completeness is proved by hand, and Basu pays off", mins=6,
 objective="Watch one family give you completeness, ancillarity and independence together.",
 viz={"type":"unif-likelihood","n":5,"xmax":4.2},
 body=L(
  "X₁,…,Xₙ are iid U(0, θ). The likelihood is the cliff on screen: θ^(−n) above the sample maximum, zero below. X₍ₙ₎ is sufficient — that was the previous topic — and here it is also complete.",
  "The proof is the third ending from scene 3. X₍ₙ₎ has density n x^(n−1)/θⁿ on (0, θ), so E[g(X₍ₙ₎)] = 0 for all θ becomes ∫₀^θ g(x) x^(n−1) dx = 0 for all θ. Differentiate both sides with respect to θ and you get g(θ)θ^(n−1) = 0 for every θ > 0, so g ≡ 0. The whole argument is one differentiation.",
  "Now look for something ancillary. Take the ratio X₍₁₎/X₍ₙ₎. Scaling every observation by a constant leaves it unchanged, and changing θ is exactly such a scaling — so its distribution cannot involve θ. It is ancillary.",
  "Basu now hands you a fact for free: X₍ₙ₎ and X₍₁₎/X₍ₙ₎ are independent. No joint density, no Jacobian. That is the whole point of the theorem.",
  "Drag the maximum and watch the likelihood move with it while the ratio sits quietly outside the picture, unaffected by θ. Complete sufficient on one side, ancillary on the other, independent by Basu."),
 ask={"q":"X₍₁₎ on its own is NOT ancillary for U(0,θ), but X₍₁₎/X₍ₙ₎ is. What does the division actually remove?",
      "nudge":"Write X₍₁₎ as θ times a U(0,1) order statistic. Which factor survives the ratio?"})

scene(kind="guided", title="Now without the steps — independence in the normal sample", mins=8,
 objective="Choose Basu yourself, and check both of its conditions before you use it.",
 problem="X₁,…,Xₙ are iid N(μ, σ²) with σ² KNOWN. Prove that X̄ and S² = Σ(Xᵢ − X̄)²/(n−1) are independent.",
 hints=L(
  "Direction — you are being asked for independence, and you have been given a theorem this week that delivers independence. Before reaching for it, write down what it needs: one complete sufficient statistic, and one ancillary statistic. Decide which of X̄ and S² is which.",
  "Method — Basu. X̄ is complete sufficient for μ here, because with σ² known the family is a full-rank one-parameter exponential family. So the work is all on the other side: show that the distribution of S² does not involve μ.",
  "Next step — write Xᵢ − X̄ = (Xᵢ − μ) − (X̄ − μ) and look at what S² becomes. The variables Yᵢ = Xᵢ − μ are N(0, σ²), with no μ in them anywhere."),
 solution=L(
  {"say":"Check the first condition.","math":"σ² known ⟹ f(x;μ) = h(x)c(μ)exp( (μ/σ²)·Σxᵢ ), a full-rank one-parameter exponential family, so X̄ is complete sufficient for μ."},
  {"say":"Rewrite the deviations.","math":"Xᵢ − X̄ = (Xᵢ − μ) − (X̄ − μ) = Yᵢ − Ȳ,   where Yᵢ = Xᵢ − μ ~ N(0, σ²)"},
  {"say":"Check the second condition.","math":"S² = Σ(Yᵢ − Ȳ)²/(n−1), and the distribution of the Yᵢ does not involve μ ⟹ S² is ancillary for μ."},
  {"say":"Apply Basu.","math":"X̄ complete sufficient, S² ancillary ⟹ X̄ ⟂ S², for every μ."}),
 answer="X̄ is complete sufficient for μ, S² is ancillary for μ, so Basu's theorem gives their independence immediately.",
 check="Two conditions were needed and both had to be verified — stating Basu without showing S² is ancillary answers half the question. Note also what the argument assumed: σ² known. The result is true with σ² unknown as well, but Basu alone does not get you there, because then X̄ is no longer sufficient on its own.")

scene(kind="trapcheck", title="Six statements — verdict on each before you look", mins=6,
 objective="Practise the per-statement discipline the real multi-statement items demand.",
 intro="Give every statement a true or false verdict first. In the exam these six would be one question scored all or nothing, so a verdict you skipped is a mark you gambled.",
 items=L(
  {"claim":"Completeness is a property of the statistic T alone, independent of the family of distributions.","tf":False,
   "why":"False, and the misconception the whole topic rests on. Completeness is a property of the family {f_T(t;θ)}. Restrict Θ enough and the same T stops being complete."},
  {"claim":"If T is complete and sufficient, then T is minimal sufficient.","tf":True,
   "why":"True — this is Bahadur's theorem, assuming a minimal sufficient statistic exists. Candidates often believe the converse instead, which is false."},
  {"claim":"Every minimal sufficient statistic is complete.","tf":False,
   "why":"False. N(θ, θ²) has minimal sufficient (ΣXᵢ, ΣXᵢ²), which is not complete because the family is curved."},
  {"claim":"The distribution of an ancillary statistic does not depend on θ.","tf":True,
   "why":"True — that is the definition. Note it says the distribution, not that the statistic is useless: an ancillary statistic is precisely what Basu's theorem needs."},
  {"claim":"Basu's theorem requires only that T be sufficient and A be ancillary.","tf":False,
   "why":"False — T must be COMPLETE and sufficient. Drop completeness and the conclusion fails; U(θ,θ+1) is the standard case where sufficiency holds, completeness does not, and no independence follows."},
  {"claim":"In a full-rank k-parameter exponential family, the natural sufficient statistic is complete.","tf":True,
   "why":"True, and it is the shortcut worth memorising: full rank means the natural parameter space contains an open k-dimensional rectangle, and then T is complete and minimal sufficient together."}))

scene(kind="guided", title="Transfer — show that a statistic is NOT complete", mins=8,
 objective="Run the argument backwards: construct a counterexample instead of proving a theorem.",
 problem="X₁,…,Xₙ are iid U(θ, θ+1) with θ ∈ ℝ unknown. The minimal sufficient statistic is T = (X₍₁₎, X₍ₙ₎). Show that T is NOT complete.",
 hints=L(
  "Direction — to disprove completeness you do not argue, you exhibit. You need one specific function g, not identically zero, with E_θ[g(T)] = 0 for every θ. Start by asking which functions of T have an expectation that does not move when θ moves.",
  "Method — a function of T whose distribution is free of θ is ancillary, and its mean is therefore some constant c. Subtract the constant and you have your g. So look for an ancillary function of (X₍₁₎, X₍ₙ₎) in this location family.",
  "Next step — the range R = X₍ₙ₎ − X₍₁₎ is unchanged when every observation shifts by the same amount, and changing θ is exactly such a shift. Find E[R], then write down g."),
 solution=L(
  {"say":"Find an ancillary function of T.","math":"R = X₍ₙ₎ − X₍₁₎. Shifting all Xᵢ by a constant leaves R unchanged, and the family is a location family, so the distribution of R does not involve θ."},
  {"say":"Compute its mean.","math":"Write Xᵢ = θ + Uᵢ with Uᵢ iid U(0,1). Then R = U₍ₙ₎ − U₍₁₎, and E[U₍ₙ₎] = n/(n+1), E[U₍₁₎] = 1/(n+1), so E[R] = (n−1)/(n+1)."},
  {"say":"Build the counterexample.","math":"g(T) = (X₍ₙ₎ − X₍₁₎) − (n−1)/(n+1)"},
  {"say":"Verify both halves.","math":"E_θ[g(T)] = E[R] − (n−1)/(n+1) = 0 for EVERY θ, yet g(T) is not identically zero — R is a genuine random variable with positive variance."},
  {"say":"Conclude.","math":"A non-zero function of T has mean zero for every θ, so T is not complete. Basu's theorem therefore does not apply to this family."}),
 answer="g(T) = (X₍ₙ₎ − X₍₁₎) − (n−1)/(n+1) is a non-trivial unbiased estimator of zero, so T = (X₍₁₎, X₍ₙ₎) is not complete.",
 check="Two things had to be shown, and a half answer scores nothing: that E[g(T)] = 0 for all θ, AND that g is not identically zero. Candidates routinely produce the function and forget to say why it is non-trivial — which is the half that makes it a counterexample.")

scene(kind="summary", title="What you should now be able to do unaided", mins=3,
 objective="Close the loop before the test.",
 body=L(
  "State completeness with its quantifier intact, and say whose property it is.",
  "Prove completeness for a standard family by setting E[g(T)] = 0 and finishing with the right uniqueness result — power series, polynomial, or differentiation under the integral.",
  "Put a density into exponential form, check whether the natural parameter space holds an open rectangle, and take completeness for free when it does.",
  "Spot a curved family by comparing dim(T) with dim(θ), and refuse to claim completeness there.",
  "Identify an ancillary statistic, check both of Basu's conditions, and use it to get independence in three lines.",
  "Disprove completeness by building an ancillary function of T and subtracting its mean.",
  "The mastery test is ten unseen questions across all of this. Hints are off. The pass is 80% overall with 70% floors on the numerical and multi-statement items."))

scene(kind="quiz", title="Mastery test", mins=12,
 objective="Demonstrate it independently, on unseen questions.",
 setId="inference_t2_mastery")

lesson["scenes"]=S

def m(i,fmt,stem,options,ans,expl,**kw):
    d={"id":"inf-t2-m-%02d"%i,"format":fmt,"topic":"inference-t2","stem":stem,
       "options":options,"answer":ans,"explanation":expl}
    d.update(kw); return d

mastery=[
 m(1,"single","A family of distributions of T is complete when:",
   ["E_θ[g(T)] = 0 for every θ implies g(T) = 0 with probability 1",
    "E_θ[g(T)] = 0 for some θ implies g(T) = 0 with probability 1",
    "Var_θ(T) does not depend on θ",
    "The distribution of T does not depend on θ"],
   "A","That is the definition, and the quantifier 'for every θ' is the whole content — option B weakens it to a single θ, which says almost nothing. Option D describes an ancillary statistic, which is close to the opposite situation. Option C is unrelated to completeness."),
 m(2,"numeric","X₁,…,X₅ are iid U(0,θ). The sample maximum is x₍₅₎ = 3.5. Given E[X₍ₙ₎] = nθ/(n+1), give the UMVUE of θ and its value here.",
   ["(6/5)·x₍₅₎ = 4.2","x₍₅₎ = 3.5","(5/6)·x₍₅₎ = 2.917","2x̄, which cannot be found from x₍₅₎ alone"],
   "A","X₍ₙ₎ is complete sufficient, and E[X₍ₙ₎] = 5θ/6, so (6/5)X₍ₙ₎ is unbiased. Being an unbiased function of a complete sufficient statistic, Lehmann–Scheffé makes it the UMVUE: (6/5)(3.5) = 4.2. Option B is the MLE, which is biased low; option C scales the wrong way and makes the bias worse.",
   check="The multiplier is (n+1)/n = 6/5, not n/(n+1). A UMVUE for θ must come out larger than the sample maximum, never smaller."),
 m(3,"multi","Consider Basu's theorem and its conditions.",
   ["A, C and D only","A and B only","B and C only","A, B and D only"],"A",
   "A is true — that is the statement of the theorem. B is false: completeness is required as well as sufficiency, and dropping it breaks the conclusion. C is true, and is the standard application. D is true — bounded completeness suffices, which is why some texts state it that way.",
   statements=["If T is complete sufficient and A is ancillary, then T and A are independent for every θ.",
               "Sufficiency of T alone is enough for the conclusion.",
               "For an iid normal sample with σ² known, Basu gives the independence of X̄ and S².",
               "Bounded completeness of T is enough for the theorem to hold."],
   verdicts={"A":{"tf":True,"why":"The theorem exactly as stated."},
             "B":{"tf":False,"why":"Completeness is essential. U(θ,θ+1) is sufficient without being complete, and no independence follows."},
             "C":{"tf":True,"why":"X̄ is complete sufficient for μ, S² is ancillary for μ, so they are independent."},
             "D":{"tf":True,"why":"Basu's proof only needs the condition for bounded g, so bounded completeness suffices."}}),
 m(4,"numeric","X₁,…,X₄ are iid U(θ, θ+1). The range is R = X₍₄₎ − X₍₁₎. Give E[R], and say what it shows about the minimal sufficient statistic (X₍₁₎, X₍₄₎).",
   ["E[R] = 3/5, and it shows the statistic is not complete",
    "E[R] = 3/5, and it shows the statistic is not sufficient",
    "E[R] = 1/5, and it shows the statistic is not complete",
    "E[R] = 4/5, and it shows the statistic is ancillary"],
   "A","Writing Xᵢ = θ + Uᵢ with Uᵢ iid U(0,1), R = U₍₄₎ − U₍₁₎ with E[R] = (n−1)/(n+1) = 3/5. Since R is ancillary, g(T) = R − 3/5 is a non-zero function with mean 0 for every θ, so T is not complete. It remains perfectly sufficient — option B confuses the two properties.",
   check="Two parts: the number and what it demonstrates. (n−1)/(n+1) with n = 4 is 3/5, not 1/5 — that would be E[U₍₁₎]."),
 m(5,"single","For which family is the minimal sufficient statistic NOT complete?",
   ["N(θ, θ²) with θ > 0","Poisson(λ) with λ > 0","Bernoulli(p) with 0 < p < 1",
    "Exponential with rate λ > 0"],
   "A","N(θ,θ²) is a curved exponential family: the minimal sufficient statistic (ΣXᵢ, ΣXᵢ²) is two-dimensional while θ is one-dimensional, so the natural parameter traces a curve rather than filling an open rectangle. Full rank fails and completeness goes with it. The other three are full-rank one-parameter families whose sufficient statistic is complete."),
 m(6,"numeric","X₁,…,X₄ are iid Bernoulli(p) and Σxᵢ = 3. The UMVUE of p² is T(T−1)/(n(n−1)). Give its value, and say why it is the UMVUE.",
   ["0.5, because it is an unbiased function of a complete sufficient statistic",
    "0.5625, because it is the square of the MLE",
    "0.75, because it is the sample proportion",
    "0.5, because it has the smallest variance among all estimators"],
   "A","T(T−1)/(n(n−1)) = 3·2/(4·3) = 0.5. It is unbiased because E[T(T−1)] = n(n−1)p², and T is complete sufficient, so Lehmann–Scheffé makes the unbiased function of T the UMVUE. Option B is p̂² = 0.5625, which is biased. Option D overstates the claim — UMVUE means smallest variance among UNBIASED estimators only.",
   check="The question asked for the value and the reason. 0.5 with the wrong reason is still a wrong answer in a two-part item."),
 m(7,"multi","Let T be sufficient for θ in some family.",
   ["B and D only","A and B only","A, B and C only","C and D only"],"A",
   "A is false — sufficiency does not give completeness; the implication runs the other way. B is true, by Bahadur's theorem. C is false: ancillarity means the distribution is free of θ, which is close to the opposite of sufficiency. D is true, and is exactly how completeness is disproved.",
   statements=["If T is sufficient then T is complete.",
               "If T is complete and sufficient then T is minimal sufficient.",
               "A sufficient statistic is always ancillary.",
               "Exhibiting one non-zero g with E_θ[g(T)] = 0 for all θ disproves completeness."],
   verdicts={"A":{"tf":False,"why":"No. The whole sample is sufficient and is almost never complete."},
             "B":{"tf":True,"why":"Bahadur's theorem, assuming a minimal sufficient statistic exists."},
             "C":{"tf":False,"why":"Ancillary means the distribution does not involve θ — nearly the reverse of carrying all the information about θ."},
             "D":{"tf":True,"why":"Completeness is a universal claim, so a single counterexample destroys it."}}),
 m(8,"numeric","X₁,…,Xₙ are iid with f(x;θ) = θ e^(−θx), x > 0. Put the family in exponential form and give the dimension of the natural parameter space together with the complete sufficient statistic.",
   ["Dimension 1, and T = Σxᵢ","Dimension 2, and T = (Σxᵢ, Σxᵢ²)",
    "Dimension 1, and T = x₍ₙ₎","Dimension 2, and T = (Σxᵢ, n)"],
   "A","f = θ·exp(−θx) = h(x)c(θ)exp(w(θ)t(x)) with h = 1, c(θ) = θ, w(θ) = −θ and t(x) = x. One natural parameter, and as θ runs over (0,∞) the value −θ covers an open interval, so the family is full rank. T = Σxᵢ is therefore complete and minimal sufficient.",
   check="One parameter means a one-dimensional T. If you wrote a pair, check how many distinct t-functions the exponent actually needed."),
 m(9,"numeric","X₁,…,Xₙ are iid Poisson(λ). You must show T = ΣXᵢ is complete. After writing E_λ[g(T)] = 0 and dividing out e^(−nλ), what remains and what closes the argument?",
   ["A power series in λ that vanishes on an interval, so every coefficient is zero",
    "A polynomial in λ of degree n, so it has at most n roots",
    "An integral over (0,λ), so differentiating in λ gives g ≡ 0",
    "A moment generating function, so uniqueness of MGFs gives g ≡ 0"],
   "A","Dividing by e^(−nλ) leaves Σ_t [g(t)nᵗ/t!] λ^t = 0 for every λ > 0 — a power series in λ identically zero on an open interval, so every coefficient vanishes and g(t) = 0 for all t. Option B is the Binomial ending, option C the Uniform ending; both are right arguments applied to the wrong family.",
   check="The sum over t is infinite for a Poisson, so it is a power series and not a polynomial. Identify the support before choosing which uniqueness result to cite."),
 m(10,"order","To prove a statistic complete, arrange these steps in the order they are carried out.",
   ["C, A, D, B","A, C, D, B","C, D, A, B","D, C, A, B"],"A",
   "Write the distribution of T first — completeness is a statement about that family, so nothing can start without it. Then write E[g(T)] = 0 in full, strip the factors free of t, and close with the uniqueness result. Reaching for a uniqueness theorem before you know whether the sum is finite or infinite is how candidates pick the wrong one.",
   items=["A. Write E_θ[g(T)] = 0 explicitly as a sum or integral",
          "B. Apply the uniqueness result and conclude g ≡ 0",
          "C. Identify the distribution of T and its support",
          "D. Divide out every factor that does not involve t"]),
]

body={"moduleId":"inference","source":"mastery","topicId":"inference-t2",
      "label":"Completeness and Basu — mastery test (unseen)","count":len(mastery),"items":mastery}
with open(os.path.join(OUT,"inference_t2_mastery.json"),"w") as f:
    json.dump(body,f,ensure_ascii=False,indent=1)
with open(os.path.join(OUT,"lesson_t2.json"),"w") as f:
    json.dump(lesson,f,ensure_ascii=False,indent=1)
fm={}
for i in mastery: fm[i["format"]]=fm.get(i["format"],0)+1
print("scenes:",len(S),"->"," ".join(x["kind"] for x in S))
print("mastery:",len(mastery),fm)
print("bytes:",os.path.getsize(os.path.join(OUT,"lesson_t2.json")))
