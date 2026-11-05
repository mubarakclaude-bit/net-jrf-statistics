# lessons/inferencet9 — Neyman-Pearson, MLR, UMP, and when UMP fails  (depth: Apply)
import json, os
OUT = "/home/claude/w1/seed"
L = lambda *p: list(p)

lesson = {
 "id":"inferencet9","moduleId":"inference","topicId":"inference-t9",
 "title":"Neyman–Pearson, Monotone Likelihood Ratio and UMP Tests",
 "breadcrumb":"Statistical Inference → Testing of Hypotheses → The best test there is",
 "engine":"C",
 "engineName":"Testing — fixing one error rate and making the other as small as it can be",
 "estMin":50,"version":"1.0","status":"approved",
 "provenance":"Theory, worked examples and practice authored for this platform against the UGC NET Statistics syllabus. Previous-year questions are stored separately and carry their exam cycle.",
 "objectives":L(
   "State the Neyman–Pearson lemma and use the likelihood ratio to find the most powerful test of one simple hypothesis against another.",
   "Turn 'reject when the ratio is large' into an explicit critical region, and fix the constant from the size condition.",
   "Recognise a monotone likelihood ratio family and quote Karlin–Rubin to get a UMP test for a one-sided alternative.",
   "Say exactly why no UMP test exists for a two-sided alternative, and name what is used instead.",
   "Compute size and power for a given test, and read a power function."),
 "prereq":L(
   {"id":"p1","name":"The likelihood function","why":"Every test in this topic is built from the ratio of two likelihoods. If writing L(θ) is still slow, the MLE topic comes first."},
   {"id":"p2","name":"Distribution of the sample mean","why":"Nearly every critical region here is an inequality on x̄, and the size condition is a normal or chi-square tail probability."},
   {"id":"p3","name":"Type I and Type II errors","why":"The whole subject is the trade-off between them. You need the two definitions cold before scene 3."}),
 "mastery":{"minQ":10,"pass":80,"draw":10,"fmtMin":{"numeric":70,"multi":70},
   "diffMix":{"easy":3,"moderate":5,"hard":2},"noHints":True,"retestDays":7,
   "note":"Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints. Each paper is drawn to the difficulty mix below — 3 easy, 5 moderate, 2 hard — which models a NET-style paper; NTA publishes no official difficulty split."},
 "refs":L(
  {"title":"Hypothesis Testing: the Neyman–Pearson lemma","where":"Lecture 16",
   "site":"Stanford STATS 200 (Autumn 2016)","url":"https://web.stanford.edu/class/archive/stats/stats200/stats200.1172/Lecture16.pdf",
   "type":"Lecture notes","free":True,"checked":"2026-10-12",
   "why":"The lemma stated and proved, then applied to the normal and the Bernoulli. Read it after scene 3, when you want to see why the likelihood ratio is forced on you rather than chosen."},
  {"title":"Uniformly Most Powerful Tests","where":"Lesson 26.1–26.3",
   "site":"Penn State STAT 415","url":"https://online.stat.psu.edu/stat415/lesson/26",
   "type":"Course notes","free":True,"checked":"2026-10-12",
   "why":"The one-sided normal case worked in full, with the power function drawn. The clearest free treatment of why 'uniformly' is the hard word in UMP. CC BY-NC, no login."}),
 "revision":{
  "sheet":L(
    "Simple hypothesis: specifies the distribution completely (H₀: θ = θ₀). Composite: a set of values (H₀: θ ≤ θ₀).",
    "Size α = P(reject H₀ | H₀ true), the Type I error rate you choose. β = P(accept H₀ | H₁ true). Power = 1 − β.",
    "Neyman–Pearson: for simple vs simple, the most powerful size-α test rejects when L(θ₁)/L(θ₀) > k, with k fixed by P(reject | H₀) = α.",
    "Always simplify the ratio into an inequality on a statistic, then find the constant from the size condition.",
    "For discrete data an exact α may need a randomised test: reject with probability γ on the boundary.",
    "MLR in T: for θ₂ > θ₁ the ratio L(θ₂)/L(θ₁) is a non-decreasing function of T.",
    "Karlin–Rubin: with MLR in T, 'reject when T > c' is UMP for H₀: θ ≤ θ₀ against H₁: θ > θ₀.",
    "One-parameter exponential families have MLR in the natural statistic — which is why one-sided UMP tests exist for them.",
    "No UMP test exists for a two-sided alternative in these families: the one-sided tests point opposite ways and neither beats the other everywhere.",
    "What is used instead: UMPU (adding the unbiasedness requirement), or the likelihood ratio test.",
    "Power function β(θ) = P(reject | θ). At θ = θ₀ it equals α; it rises with the gap and with n.",
    "Normal mean, σ known, one-sided: reject when x̄ > μ₀ + z_α·σ/√n. Power at μ₁ is 1 − Φ(z_α − (μ₁−μ₀)√n/σ).",
    "Raising n raises power at fixed α. Raising α raises power too — the two errors trade and cannot both shrink at fixed n."),
  "cards":L(
    ["State the Neyman–Pearson lemma.","For simple H₀ vs simple H₁, the test rejecting when L(θ₁)/L(θ₀) > k, with k chosen so the size is α, is most powerful among all size-α tests."],
    ["Why is the likelihood ratio the right statistic?","Because the lemma proves it: no other size-α test can have greater power. It is forced, not chosen."],
    ["What does MLR mean?","The likelihood ratio for two parameter values is a monotone function of a single statistic T, for every such pair."],
    ["State Karlin–Rubin.","If the family has MLR in T, then rejecting when T > c is UMP for H₀: θ ≤ θ₀ against H₁: θ > θ₀."],
    ["Why does no UMP test exist for a two-sided alternative?","The most powerful test against μ > μ₀ rejects in the upper tail; against μ < μ₀ it rejects in the lower. Neither is most powerful on both sides, so no single test is best uniformly."],
    ["What replaces UMP when it does not exist?","UMPU — restrict to unbiased tests and find the best among those — or fall back on the likelihood ratio test."],
    ["What is a randomised test and when is one needed?","On the boundary, reject with probability γ rather than always or never. Needed for discrete data, where no non-randomised region has size exactly α."],
    ["Define the power function.","β(θ) = P(reject H₀ | θ), as a function of the true parameter. It equals α at θ₀ and rises as θ moves into the alternative."],
    ["One-sided normal test, σ known: the critical region?","Reject when x̄ > μ₀ + z_α σ/√n."],
    ["How do α, n and power move together?","At fixed n, lowering α lowers power. At fixed α, raising n raises power. Only n buys both."]),
  "tricks":L(
    {"hook":"Fix one error, minimise the other","why":"You cannot make α and β small together at fixed n. Neyman–Pearson fixes α and does the best possible on β."},
    {"hook":"Ratio big ⇒ reject","why":"L(θ₁)/L(θ₀) > k. Large ratio means the data look much more like H₁ than H₀."},
    {"hook":"Simplify, then size it","why":"Turn the ratio into an inequality on a statistic FIRST; only then use P(reject | H₀) = α to pin the constant."},
    {"hook":"MLR ⇒ one-sided UMP, and only one-sided","why":"Karlin–Rubin gives a UMP test for a one-sided alternative. Two-sided kills it, because the two tails disagree."}),
  "shortcuts":L(
    "One-parameter exponential family ⇒ MLR in the natural statistic ⇒ a one-sided UMP test exists. That chain answers most UMP questions in one line.",
    "Normal mean, σ known: reject when x̄ > μ₀ + 1.645σ/√n at α = 0.05 one-sided; 1.96 for two-sided.",
    "The critical value never involves the alternative — only μ₀, σ, n and α. The alternative only affects POWER.",
    "If a question says 'two-sided' and asks for a UMP test, the answer is that none exists."),
  "remember":L(
    "A UMP test for a two-sided alternative does not exist in the standard one-parameter families. Saying so IS the answer.",
    "Size is what you set under H₀; power is what you get under H₁. Never quote one for the other."),
  "traps":L(
    "Putting the alternative into the critical value. The cut-off depends on H₀, n and α only.",
    "Forgetting the randomisation on the boundary for discrete data, then claiming size exactly α.",
    "Saying a UMP test exists two-sided because the family is nice. MLR buys one-sided only.",
    "Confusing 'most powerful' (simple vs simple) with 'uniformly most powerful' (over a whole composite alternative)."),
  },
 "traps":L(
   "The critical value never contains μ₁.",
   "MLR gives one-sided UMP only.",
   "Discrete data may need randomisation to hit size α exactly.",
   "Power is computed under H₁, size under H₀."),
}

S=[]
def scene(**kw):
    kw.setdefault("id","s%d"%(len(S)+1)); S.append(kw); return kw

scene(kind="intuition", title="Two ways to be wrong, and only one of them is yours to choose", mins=5,
 objective="See why testing is an asymmetric trade rather than a search for truth.",
 body=L(
  "A test can fail in two ways. It can reject a hypothesis that was true, or it can fail to reject one that was false. Call the first error α and the second β, and notice immediately that you cannot drive both to zero: a test that never rejects has α = 0 and useless β, and a test that always rejects has the reverse.",
  "The Neyman–Pearson answer is to stop pretending the two are symmetric. Fix α at a level you are prepared to live with — conventionally 0.05 or 0.01 — and then, among all tests of that size, take the one with the smallest β. That is the entire programme, and it is why the subject is about POWER rather than about truth.",
  "The asymmetry is deliberate and it reflects where the burden of proof sits. H₀ is the status quo: the drug does nothing, the process is in control, the coin is fair. Rejecting it is a claim, and α is how often you are willing to make that claim wrongly. β is the price you pay for that caution.",
  "What the lemma then adds is startling. For the simplest case — one completely specified hypothesis against another — it does not merely suggest a good test. It proves that the test based on the likelihood ratio is the best possible, and that any other test of the same size has power no greater. You are not choosing a statistic; you are being told which one to use.",
  "Everything after that is an attempt to extend the result. When the alternative is a whole range of values rather than a single one, 'best' has to hold for every one of them at once — uniformly — and that is a far stronger demand. Sometimes it can be met. Often it cannot, and knowing which is which is most of what this topic examines."),
 aside={"h":"Why the words matter",
        "body":"SIMPLE hypothesis: the distribution is fully specified, as in H₀: μ = 5. COMPOSITE: a set of distributions, as in H₀: μ ≤ 5. Neyman–Pearson is a theorem about simple versus simple. Every later result is machinery for getting a composite problem back to that case."},
 scenario={
  "teaser":"A radar has milliseconds to decide whether a return is an aircraft or noise.",
  "title":"How a radar decides",
  "body":L(
   "A radar transmits a pulse and listens. What comes back is mostly thermal noise, with — sometimes — a faint reflection buried in it. The receiver has to decide, continuously and in real time, between two hypotheses: H₀, noise only, and H₁, noise plus a target echo.",
   "Both errors have names and costs. Declaring a target when there is none is a false alarm: the system tracks a ghost, and operators lose confidence. Missing a real return is a missed detection, with obvious consequences. The two cannot be minimised together, so the engineering convention is to fix the false-alarm rate — this is literally called the constant false alarm rate, CFAR — and then maximise the probability of detection subject to it.",
   "That is Neyman–Pearson, implemented in silicon. Fix α, maximise power. And the detector that does it is the likelihood ratio: the receiver forms the ratio of the likelihood of the observed waveform under 'signal present' to that under 'noise only', and compares it with a threshold set by the required false-alarm rate.",
   "The design consequences follow the mathematics exactly. The threshold is computed from the noise distribution alone — the H₀ side — which is why it does not depend on how strong the target is. Target strength affects only the detection probability, which is the power of the test. And the way to improve detection without accepting more false alarms is to integrate more pulses: the equivalent of raising n."),
  "q":"An operator complains of too many false alarms and asks for the threshold to be raised. What happens to the two error rates, and what would be the better fix?",
  "answer":"Raising the threshold lowers α, so false alarms fall — but it moves the cut-off away from the alternative too, so the detection probability falls with it. The two cannot both improve at a fixed amount of data; that is exactly the trade the lemma formalises. The better fix is to integrate more pulses, or to improve the signal-to-noise ratio. Both increase the separation between the two distributions, which raises power at the SAME false-alarm rate — the only thing that buys an improvement in both errors at once.",
  "link":"The same structure runs medical screening: sensitivity is power, one minus specificity is α, and arguing about where to set a diagnostic cut-off is arguing about where on this trade-off to sit."},
 ask={"label":"Ask Claude why the asymmetry is defensible",
      "prompt":"A UGC NET Statistics (JRF) candidate is starting hypothesis testing. In under 150 words, plain text, explain why the Neyman–Pearson framework treats the two error types asymmetrically — fixing α and minimising β — rather than, say, minimising their sum. Mention what that asymmetry assumes about H₀, and one situation where the assumption is uncomfortable. Do not restate the definitions of α and β.",
      "tier":"default"})

scene(kind="explore", title="Watch α and power trade against each other", mins=7,
 objective="See the two error rates as areas, and find out what actually moves power.",
 viz={"type":"np-power","n":16,"d":1.0,"alpha":0.05,"sd":4},
 body=L(
  "Two curves: the sampling distribution of x̄ under H₀ on the left, and under H₁ shifted right by the true gap μ₁ − μ₀. The vertical line is the cut-off c. Reject when x̄ lands to its right.",
  "The red area is α — the part of the H₀ curve that falls in the rejection region, which is exactly how often you reject a true null. The amber area is β, the part of the H₁ curve that falls short of the cut-off and so gets missed. Power is everything else under the H₁ curve.",
  "Now experiment, and watch what happens to the two areas. Raise α: the line slides left, the red area grows and the amber shrinks. Lower it: the reverse. At a fixed sample size the two errors are joined at the hip — you are moving one cut-off, and it cannot favour both sides.",
  "Then raise n and watch something different happen. Both curves narrow, because the standard error σ/√n falls. The cut-off moves in, the red area stays exactly where you set it, and the amber area collapses. Sample size is the only control that improves one error without worsening the other.",
  "Finally set the gap to zero. The curves lie on top of each other and power drops to α itself. A test can never do worse than its own size, and when there is nothing to detect, rejecting at rate α is all it does. That is the floor the whole subject is measured against."))

scene(kind="theory", title="The lemma, and how to actually use it", mins=9,
 objective="State it precisely, then turn it into a critical region you can write down.",
 flow={
  "title":"From two hypotheses to a critical region",
  "alt":"Flow chart for applying the Neyman–Pearson lemma",
  "nodes":[
   {"id":"a","r":0,"c":1,"label":"Simple H₀: θ = θ₀ against simple H₁: θ = θ₁","kind":"start"},
   {"id":"b","r":1,"c":1,"label":"Form the ratio Λ = L(θ₁)/L(θ₀)","kind":"step"},
   {"id":"c","r":2,"c":1,"label":"Simplify: Λ > k becomes an inequality on a statistic T","kind":"step"},
   {"id":"d","r":3,"c":1,"label":"Is the data distribution continuous?","kind":"decision"},
   {"id":"e","r":4,"c":0,"label":"Randomise on the boundary to hit size α exactly","kind":"note"},
   {"id":"f","r":4,"c":2,"label":"Solve P(T > c | H₀) = α for c","kind":"step"},
   {"id":"g","r":5,"c":1,"label":"That region is the MOST POWERFUL size-α test","kind":"end"},
   {"id":"h","r":6,"c":1,"label":"Does c turn out free of θ₁?","kind":"decision"},
   {"id":"i","r":7,"c":1,"label":"Then the same test is UMP against the whole one-sided alternative","kind":"end"}],
  "edges":[
   {"from":"a","to":"b"},{"from":"b","to":"c"},{"from":"c","to":"d"},
   {"from":"d","to":"e","label":"no"},{"from":"d","to":"f","label":"yes"},
   {"from":"e","to":"g"},{"from":"f","to":"g"},{"from":"g","to":"h"},
   {"from":"h","to":"i","label":"yes"}],
  "note":"The last diamond is the bridge from Neyman–Pearson to UMP. If the critical region does not depend on which θ₁ you used, the one test is simultaneously most powerful against all of them — which is what 'uniformly' means."},
 blocks=L(
  {"t":"def","h":"Size, power and the power function",
   "body":"The size of a test is α = P(reject H₀ | H₀ true). Its power at a particular alternative θ is β(θ) = P(reject H₀ | θ), and the power FUNCTION is that probability read as a function of θ. At θ = θ₀ the power function equals the size."},
  {"t":"formula","h":"The Neyman–Pearson lemma",
   "body":"To test simple H₀: θ = θ₀ against simple H₁: θ = θ₁, the test that rejects when\n       Λ(x) = L(θ₁ | x) / L(θ₀ | x)  >  k,\nwith k chosen so that P(Λ > k | θ₀) = α, is MOST POWERFUL among all tests of size α."},
  {"t":"step","h":"How to use it, in the order that works",
   "body":"1. Write both likelihoods and form the ratio.\n2. Cancel everything that does not involve the data.\n3. Rearrange Λ > k into an inequality on a single statistic — usually x̄ or Σxᵢ.\n4. Fix the constant from the SIZE condition, under H₀.\n5. State the region, then compute power under H₁ if asked."},
  {"t":"trap","h":"The direction of the inequality",
   "body":"When you rearrange, dividing or multiplying by a negative quantity flips the inequality. For a one-sided test with θ₁ > θ₀ you should end up rejecting for LARGE values of the natural statistic; if you end up with 'small', re-check the algebra — or check that θ₁ < θ₀, in which case 'small' is correct."},
  {"t":"assume","h":"Randomised tests, and why discrete data need them",
   "body":"For a discrete statistic the achievable sizes are a finite list — for a Binomial(10, 0.5) you can get 0.0107 or 0.0547 but nothing in between. To obtain size exactly α, the test rejects outright above the boundary, rejects with probability γ AT the boundary, and accepts below. The lemma is stated for these randomised tests, which is why it holds in complete generality."},
  {"t":"note","h":"What the lemma does not do",
   "body":"It compares tests of the SAME size. It says nothing about whether α = 0.05 is a sensible choice, and it does not apply directly when either hypothesis is composite. Everything in the second half of this lesson exists to handle that second limitation."}))

scene(kind="worked", title="Worked in full — the normal mean", mins=7,
 objective="Run the lemma end to end and get a critical region with a number in it.",
 problem="X₁,…,X₂₅ are iid N(μ, σ²) with σ = 10 known. Test H₀: μ = 50 against H₁: μ = 55 at α = 0.05. Find the most powerful test, and its power.",
 steps=L(
  {"say":"Write the likelihood ratio, keeping only what involves the data.",
   "math":"Λ = exp{ −Σ(xᵢ−55)²/(2σ²) } / exp{ −Σ(xᵢ−50)²/(2σ²) }\n  = exp{ [Σ(xᵢ−50)² − Σ(xᵢ−55)²] / (2σ²) }",
   "why":"The normalising constants are identical under both hypotheses and cancel. Only the exponent carries information."},
  {"say":"Expand the difference of the two sums. The quadratic terms cancel.",
   "math":"Σ(xᵢ−50)² − Σ(xᵢ−55)² = 10Σxᵢ − 25n(50+55)/… = 2(55−50)Σxᵢ − n(55² − 50²)",
   "why":"Σxᵢ² appears in both and disappears. What survives is linear in Σxᵢ — which is why the test ends up being about x̄."},
  {"say":"So Λ is an increasing function of Σxᵢ. Therefore Λ > k is the same event as x̄ > c.",
   "math":"Λ > k   ⇔   Σxᵢ > k′   ⇔   x̄ > c",
   "why":"This is the step that matters. You never need the value of k: you only need to know which statistic the ratio is monotone in, and in which direction."},
  {"say":"Fix c from the size condition — computed under H₀, not H₁.",
   "math":"P(X̄ > c | μ = 50) = 0.05 ,  X̄ ~ N(50, σ²/n) = N(50, 100/25) = N(50, 4)\nc = 50 + 1.645(2) = 53.29",
   "why":"σ/√n = 10/5 = 2. The alternative μ = 55 plays no part here at all — it told us the direction and nothing more."},
  {"say":"State the test.",
   "math":"Reject H₀ when x̄ > 53.29. This is the most powerful size-0.05 test.",
   "why":"By the lemma, no other test of size 0.05 has greater power against μ = 55."},
  {"say":"Now compute the power, under H₁.",
   "math":"Power = P(X̄ > 53.29 | μ = 55) = P(Z > (53.29 − 55)/2) = P(Z > −0.855) = 0.804",
   "why":"Standardise using the H₁ mean and the same standard error. About 80% — the test will detect a shift of this size four times in five."}),
 after="Notice what the alternative did and did not do. It fixed the DIRECTION of the critical region — reject for large x̄ — and it determined the power. It did not appear in the critical value. That is the observation the next-but-one scene turns into the whole theory of UMP tests.")

scene(kind="recall", title="Pause and recall", mins=2,
 objective="Retrieve before reading on — this is where the retention comes from.",
 intro="Answer each in your head before revealing. Correcting a wrong retrieval beats re-reading a right answer.",
 items=L(
  {"q":"State the Neyman–Pearson lemma.","a":"For simple H₀ against simple H₁, rejecting when L(θ₁)/L(θ₀) > k, with k set so the size is α, is most powerful among all size-α tests."},
  {"q":"Which hypothesis is the critical value computed under?","a":"H₀. The size condition is P(reject | H₀) = α; the alternative affects only the direction and the power."},
  {"q":"What is the power function, and what is its value at θ₀?","a":"β(θ) = P(reject | θ). At θ = θ₀ it equals the size α."},
  {"q":"Why do discrete problems sometimes need a randomised test?","a":"Because the achievable sizes form a finite set, so no ordinary critical region has size exactly α. Rejecting with probability γ on the boundary closes the gap."}))

scene(kind="completion", title="Your turn, with the scaffolding removed — the exponential", mins=8,
 objective="Run the lemma yourself on a family where the algebra goes the other way.",
 problem="X₁,…,Xₙ are iid Exponential with mean θ, f(x) = (1/θ)e^(−x/θ). Test H₀: θ = θ₀ against H₁: θ = θ₁ with θ₁ > θ₀, at level α. Find the form of the most powerful test.",
 steps=L(
  {"say":"Write the likelihood for a sample of size n.",
   "math":"L(θ) = θ^(−n) exp(−Σxᵢ/θ)",
   "why":"The exponential is a one-parameter family and the sample total Σxᵢ is already visible — a good sign that the test will be about it."},
  {"say":"Form the ratio and simplify.",
   "blank":{"prompt":"Write Λ = L(θ₁)/L(θ₀), simplified.",
            "answer":"(θ₀/θ₁)^n exp{Σxᵢ(1/θ₀ − 1/θ₁)}",
            "accept":["(θ₀/θ₁)^n exp{Σxᵢ(1/θ₀ − 1/θ₁)}","(θ0/θ1)^n exp(Sx(1/θ0-1/θ1))",
                      "(θ₀/θ₁)^n e^{Σx(1/θ₀−1/θ₁)}","(theta0/theta1)^n exp(sum x (1/theta0 - 1/theta1))",
                      "(θ₀/θ₁)^n exp(Σxᵢ(1/θ₀ − 1/θ₁))"],
            "hint":"θ₁^(−n)/θ₀^(−n) = (θ₀/θ₁)^n. The exponents combine as −Σx/θ₁ + Σx/θ₀ = Σx(1/θ₀ − 1/θ₁)."},
   "why":"The leading constant does not involve the data, so it will be absorbed into k. Everything that matters is in the exponent."},
  {"say":"Since θ₁ > θ₀, the coefficient (1/θ₀ − 1/θ₁) is positive, so Λ increases with Σxᵢ. Say what the critical region looks like.",
   "blank":{"prompt":"Complete: reject H₀ when Σxᵢ is …",
            "answer":"large",
            "accept":["large","big","greater than c","> c","larger","large (Σx > c)","high"],
            "hint":"A positive coefficient in the exponent means Λ and Σxᵢ move together, so a large ratio is the same event as a large total."},
   "why":"A larger mean makes a larger total more plausible — the direction agrees with intuition, which is always worth a moment's check."},
  {"say":"Identify the null distribution you need to fix the constant.",
   "blank":{"prompt":"Under H₀, what is the distribution of ΣXᵢ?",
            "answer":"Gamma(n, θ₀)",
            "accept":["Gamma(n, θ₀)","gamma(n,theta0)","Gamma(n,θ0)","Gamma with shape n and scale θ₀",
                      "gamma(n, scale θ₀)","2ΣX/θ₀ ~ chi-square with 2n df","chi-square 2n"],
            "hint":"A sum of n independent exponentials with mean θ₀ is gamma with shape n and scale θ₀. Equivalently 2ΣXᵢ/θ₀ follows a chi-square distribution on 2n degrees of freedom, which is the form the tables are in."},
   "why":"The chi-square form is the useful one in an exam: c is read from a chi-square table rather than computed."},
  {"say":"Put the test together.",
   "math":"Reject H₀ when Σxᵢ > c, with c fixed by P(ΣXᵢ > c | θ₀) = α,\ni.e. 2c/θ₀ = χ²(2n) upper-α point",
   "why":"And note the constant does not involve θ₁ at all."}),
 after="Because c came out free of θ₁, the same test is most powerful against EVERY θ₁ greater than θ₀ — not just the one you started with. That is the definition of a uniformly most powerful test, and it fell out of the algebra rather than being imposed. The next scene explains when you can count on that happening.")

scene(kind="theory", title="MLR, Karlin–Rubin, and the wall that two-sided alternatives hit", mins=10,
 objective="Get the general condition for a one-sided UMP test, and the exact reason two-sided fails.",
 blocks=L(
  {"t":"def","h":"Monotone likelihood ratio",
   "body":"A family {f(x;θ)} has monotone likelihood ratio in the statistic T if, for every pair θ₂ > θ₁, the ratio f(x;θ₂)/f(x;θ₁) is a non-decreasing function of T(x). The ratio may depend on the data only through T, and it must move the same way for every such pair."},
  {"t":"formula","h":"Karlin–Rubin theorem",
   "body":"If the family has MLR in T, then for testing\n     H₀: θ ≤ θ₀   against   H₁: θ > θ₀,\nthe test that rejects when T > c, with c fixed by P(T > c | θ₀) = α, is UNIFORMLY MOST POWERFUL at level α."},
  {"t":"note","h":"Where MLR comes from in practice",
   "body":"Every one-parameter exponential family with a strictly increasing natural parameter has MLR in its natural statistic. That covers the binomial in p, the Poisson in λ, the normal in μ with σ known, and the exponential in its mean. So in the exam the chain is: recognise the exponential family, name the natural statistic, quote Karlin–Rubin, write the region."},
  {"t":"formula","h":"The power function of the one-sided normal test",
   "body":"For N(μ, σ²) with σ known, rejecting when x̄ > μ₀ + z_α σ/√n:\n     β(μ) = 1 − Φ( z_α − (μ − μ₀)√n / σ )\nβ(μ₀) = α, and β increases in both (μ − μ₀) and n."},
  {"t":"trap","h":"Why there is no UMP test for a two-sided alternative",
   "body":"Test H₀: μ = μ₀ against H₁: μ ≠ μ₀. Against a particular μ₁ > μ₀ the most powerful test rejects in the UPPER tail; against a particular μ₁ < μ₀ it rejects in the LOWER tail. A single test cannot be both. Any test that is best against the upper alternatives is beaten on the lower ones, so no test is most powerful uniformly over the whole alternative — and the question 'find the UMP test for H₁: μ ≠ μ₀' has the answer 'none exists'."},
  {"t":"def","h":"What is used instead",
   "body":"UNBIASED test: one whose power never falls below its size, β(θ) ≥ α for every θ in the alternative. Restricting attention to unbiased tests and finding the best among them gives the UMPU test, and for the two-sided normal mean that is the familiar symmetric two-tailed test. The other general-purpose answer is the likelihood ratio test, which is not optimal in general but is always available."},
  {"t":"note","h":"A second way UMP fails",
   "body":"Even one-sided, a UMP test can fail to exist when the family lacks MLR — the Cauchy location family is the standard example, and there the critical region genuinely depends on which alternative you aim at. MLR is what rules that out."}))

scene(kind="explore", title="Why one cut-off cannot serve both sides", mins=7,
 objective="See the two-sided failure as a picture rather than as an assertion.",
 viz={"type":"np-power","n":25,"d":2.0,"alpha":0.05,"sd":10},
 body=L(
  "Keep the same display, and this time think of the gap slider as moving the alternative around the null rather than fixing it.",
  "With the gap positive, the upper-tail test shown here has good power — the amber missed-detection area is small. Now slide the gap to zero and then imagine it negative. The alternative curve moves to the LEFT of the null, entirely into the acceptance region. This test's power against a downward shift is not merely poor; it is below α, because the alternative curve has almost nothing to the right of the cut-off.",
  "That is the two-sided problem in one observation. A test that is most powerful against upward shifts is actively worse than useless against downward ones. The mirror-image test has the mirror-image defect. No single rejection region can be best against both, which is precisely why no UMP test exists for H₁: μ ≠ μ₀.",
  "A test whose power dips below its own size, as this one does for negative gaps, is called BIASED — you are more likely to reject when the null is true than when that particular alternative is. Ruling those out is what the unbiasedness restriction does, and the symmetric two-tailed test is the best of what remains. That is the UMPU test.",
  "One more thing worth confirming on the slider: at a fixed gap, raising n raises power while α stays put, but it never rescues the direction. Sample size fixes precision, not a critical region pointed the wrong way."))

scene(kind="guided", title="Now without the steps — a one-sided Bernoulli test", mins=8,
 objective="Apply Karlin–Rubin to a discrete family and meet the randomisation issue for real.",
 problem="X₁,…,X₂₀ are iid Bernoulli(p). Test H₀: p ≤ 0.3 against H₁: p > 0.3 at level α = 0.05. Find the UMP test, give its critical region, and state its exact size. You may use that for T ~ Binomial(20, 0.3): P(T ≥ 10) = 0.0480 and P(T ≥ 9) = 0.1133.",
 hints=L(
  "Direction — the Bernoulli is a one-parameter exponential family. Identify the natural statistic and check which way the likelihood ratio moves as p increases; that tells you MLR and the direction of the region in one step.",
  "Method — quote Karlin–Rubin rather than redoing Neyman–Pearson. It gives you the form 'reject when T > c' immediately, and your only remaining job is to choose c from the size condition at the BOUNDARY value p = 0.3.",
  "Next step — the size condition cannot be met exactly here, because T is discrete. Look at the two tail probabilities you were given, pick the critical region whose size does not exceed 0.05, and then say what would be needed to achieve 0.05 exactly."),
 solution=L(
  {"say":"Write the family in exponential form to confirm MLR.",
   "math":"f(x;p) = p^x(1−p)^(1−x) = (1−p)·exp{ x·log(p/(1−p)) }\nT = ΣXᵢ, natural parameter log(p/(1−p)), strictly increasing in p"},
  {"say":"Increasing natural parameter ⇒ MLR in T. Apply Karlin–Rubin.",
   "math":"The UMP level-α test for H₀: p ≤ 0.3 vs H₁: p > 0.3 rejects when T > c"},
  {"say":"Fix c at the boundary of the null, p = 0.3, where the size is largest.",
   "math":"T ~ Binomial(20, 0.3).  Need P(T ≥ c+1 | p = 0.3) ≤ 0.05"},
  {"say":"Read the two given probabilities and choose.",
   "math":"P(T ≥ 10) = 0.0480 ≤ 0.05  ✓     P(T ≥ 9) = 0.1133 > 0.05  ✗\nSo reject when T ≥ 10"},
  {"say":"State the exact size.",
   "math":"size = P(T ≥ 10 | p = 0.3) = 0.0480, not 0.0500"},
  {"say":"Say what exact size 0.05 would require.",
   "math":"Reject when T ≥ 10; when T = 9, reject with probability\nγ = (0.05 − 0.0480)/(0.1133 − 0.0480) = 0.0020/0.0653 = 0.031"}),
 answer="The Bernoulli is a one-parameter exponential family with increasing natural parameter, so it has MLR in T = ΣXᵢ and Karlin–Rubin applies: the UMP level-0.05 test rejects when T ≥ 10. Its exact size is 0.0480. To obtain size exactly 0.05 the test must be randomised — reject outright when T ≥ 10, and when T = 9 reject with probability γ ≈ 0.031.",
 check="Three things an examiner looks for. The size is evaluated at the BOUNDARY p = 0.3, not somewhere inside the null — a composite null takes its size from its worst case. The achieved size 0.0480 is below 0.05 and that is correct for a non-randomised test; claiming 0.05 exactly without randomising is the error. And the word UMP is earned here by citing MLR plus Karlin–Rubin, not by appealing to Neyman–Pearson, which only covers simple against simple.")

scene(kind="trapcheck", title="Six statements — verdict on each before you look", mins=6,
 objective="Practise the per-statement discipline the real multi-statement items demand.",
 intro="Give every statement a true or false verdict first. In the exam these six would be one question scored all or nothing, so a verdict you skipped is a mark you gambled.",
 items=L(
  {"claim":"The Neyman–Pearson lemma applies to a simple null against a simple alternative.","tf":True,
   "why":"True, and that restriction is the point. Extending it to composite alternatives is what MLR and Karlin–Rubin are for."},
  {"claim":"The critical value of the most powerful test depends on the value specified by the alternative.","tf":False,
   "why":"False. The constant is fixed by the size condition computed under H₀. The alternative determines the DIRECTION of the region and the power, nothing else."},
  {"claim":"A UMP test exists for H₀: μ = μ₀ against H₁: μ ≠ μ₀ in the normal family with σ known.","tf":False,
   "why":"False — the standard counterexample. The best test against upper alternatives rejects in the upper tail and the best against lower ones in the lower tail; no single region is best against both. The usual answer is the UMPU two-tailed test."},
  {"claim":"If a family has monotone likelihood ratio in T, a UMP test exists for a one-sided alternative.","tf":True,
   "why":"True — that is Karlin–Rubin, and it is the main tool for getting from a simple-versus-simple lemma to a composite alternative."},
  {"claim":"Raising the significance level α increases the power of a test.","tf":True,
   "why":"True. A larger α moves the cut-off into the alternative, so power rises — at the cost of more false rejections. It is a trade, not a free gain."},
  {"claim":"For discrete data a non-randomised test can always achieve size exactly α.","tf":False,
   "why":"False. The achievable sizes form a finite set; for Binomial(20, 0.3) you can have 0.0480 or 0.1133 but nothing between. Exact size α needs randomisation on the boundary."}))

scene(kind="guided", title="Transfer — show that no UMP test exists", mins=9,
 objective="Produce the standard non-existence argument, which is an exam answer in its own right.",
 problem="X₁,…,Xₙ are iid N(μ, σ²) with σ² known. Show that no uniformly most powerful level-α test exists for H₀: μ = μ₀ against H₁: μ ≠ μ₀. State what is used instead and why it is the natural replacement.",
 hints=L(
  "Direction — a non-existence proof needs a contradiction. Suppose a UMP test did exist, and compare it with the two one-sided tests on their own home ground.",
  "Method — use Neyman–Pearson twice. For a fixed μ₁ > μ₀, identify the unique most powerful size-α test. Then do the same for a fixed μ₂ < μ₀. Notice the two regions are different, and that each is UNIQUE at its own alternative.",
  "Next step — a UMP test would have to be at least as powerful as each of them at their own alternative. Uniqueness then forces it to equal both regions at once, which is impossible. Then say which extra condition rescues the situation."),
 solution=L(
  {"say":"Fix an alternative above the null and apply the lemma.",
   "math":"For μ₁ > μ₀ the unique MP size-α test rejects when x̄ > μ₀ + z_α σ/√n.  Call this region R₊"},
  {"say":"Now fix an alternative below the null and apply the lemma again.",
   "math":"For μ₂ < μ₀ the unique MP size-α test rejects when x̄ < μ₀ − z_α σ/√n.  Call this region R₋"},
  {"say":"Suppose a UMP level-α test with region R existed. By definition it is at least as powerful as any other size-α test at EVERY alternative.",
   "math":"power_R(μ₁) ≥ power_{R₊}(μ₁)  and  power_R(μ₂) ≥ power_{R₋}(μ₂)"},
  {"say":"But R₊ is the unique most powerful test at μ₁, so matching its power forces R = R₊. The same argument at μ₂ forces R = R₋.",
   "math":"R = R₊  and  R = R₋ ,  yet  R₊ ∩ R₋ = ∅"},
  {"say":"Two disjoint non-empty regions cannot be equal. The assumption fails.",
   "math":"No UMP level-α test exists for the two-sided alternative. ∎"},
  {"say":"Identify the replacement and why it is natural.",
   "math":"R₊ is BIASED: its power at μ₂ < μ₀ is below α. Requiring β(μ) ≥ α for all μ ≠ μ₀ excludes both one-sided tests, and the best remaining test — the UMPU test — is the symmetric two-tailed region |x̄ − μ₀| > z_(α/2) σ/√n."}),
 answer="Neyman–Pearson gives a unique most powerful test at each simple alternative: the upper-tail region for μ₁ > μ₀ and the lower-tail region for μ₂ < μ₀. A UMP test would have to coincide with both, and they are disjoint, so none exists. Restricting to unbiased tests removes the two one-sided regions, and the best of what remains is the two-tailed test |x̄ − μ₀| > z_(α/2)σ/√n — the UMPU test, and the one actually used.",
 check="The structure of this argument is worth more than the result, because it is the template for every non-existence question in this topic: find two alternatives whose optimal tests differ, invoke uniqueness, derive the contradiction. Note also where the word 'unbiased' earns its keep — it is not a decorative condition but exactly the one that eliminates the two offending candidates.")

scene(kind="summary", title="What you should now be able to do unaided", mins=3,
 objective="Close the loop before the test.",
 body=L(
  "Write the likelihood ratio for a simple-versus-simple problem, simplify it to an inequality on a statistic, and fix the constant from the size condition under H₀.",
  "Keep the alternative out of the critical value, and use it only for the direction of the region and for power.",
  "Recognise a one-parameter exponential family, name its natural statistic, and quote MLR plus Karlin–Rubin to write a one-sided UMP test in one line.",
  "Compute a power function, know that β(θ₀) = α, and say how power responds to the gap, to n and to α.",
  "Say immediately that no UMP test exists for a two-sided alternative, give the disjoint-regions reason, and name UMPU and the likelihood ratio test as the replacements.",
  "Handle a discrete problem honestly: pick the region whose size does not exceed α, report the exact size, and give the randomisation probability if exact α is demanded.",
  "The mastery test is ten unseen questions across all of this. Hints are off. The pass is 80% overall with 70% floors on the numerical and multi-statement items."))

scene(kind="quiz", title="Mastery test", mins=12,
 objective="Demonstrate it independently, on unseen questions.",
 setId="inference_t9_mastery")

lesson["scenes"]=S
with open(os.path.join(OUT,"lesson_t9.json"),"w") as f:
    json.dump(lesson,f,ensure_ascii=False,indent=1)
print("scenes:",len(S),"->"," ".join(x["kind"] for x in S))
print("bytes:",os.path.getsize(os.path.join(OUT,"lesson_t9.json")))
