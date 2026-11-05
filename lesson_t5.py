# lessons/inferencet5 — method of moments, minimum chi-square, least squares  (depth: Apply)
import json, os
OUT = "/home/claude/w1/seed"
L = lambda *p: list(p)

lesson = {
 "id":"inferencet5","moduleId":"inference","topicId":"inference-t5",
 "title":"Method of Moments, Minimum Chi-square and Least Squares",
 "breadcrumb":"Statistical Inference → Point Estimation → Estimators you can write down without a likelihood",
 "engine":"B",
 "engineName":"Estimation and inference — matching what you observe to what the model predicts",
 "estMin":45,"version":"1.0","status":"approved",
 "provenance":"Theory, worked examples and practice authored for this platform against the UGC NET Statistics syllabus. Previous-year questions are stored separately and carry their exam cycle.",
 "objectives":L(
   "Set up and solve the moment equations for a one- or two-parameter family, choosing raw or central moments to keep the algebra short.",
   "State what the method of moments guarantees (consistency, asymptotic normality) and what it does not (unbiasedness, efficiency, a legal estimate).",
   "Recognise the two families the exam uses against the method: U(a,b), where the estimate can be impossible, and Cauchy, where there is no moment to match.",
   "Define the minimum chi-square and modified minimum chi-square estimators, and say what data they need.",
   "Derive the least squares normal equations as moment conditions, and see least squares as one more instance of the same idea."),
 "prereq":L(
   {"id":"p1","name":"Population and sample moments","why":"The whole method is one line: set m_r' equal to μ_r' and solve. If the notation is not automatic, fix that first."},
   {"id":"p2","name":"Mean and variance of standard families","why":"You need E[X] and Var(X) for the gamma, uniform, exponential and normal from memory — the moment equations start there."},
   {"id":"p3","name":"Maximum likelihood estimation","why":"Every comparison in this topic is against the MLE: sometimes the two coincide, usually the MLE is more efficient, occasionally the moment estimator is the only one you can write down."}),
 "mastery":{"minQ":10,"pass":80,"fmtMin":{"numeric":70,"multi":70},"noHints":True,"retestDays":7,
   "note":"Proposed platform settings, not an NTA rule. Overall 80%, with 70% floors on numerical and multi-statement items, answered without hints."},
 "refs":L(
  {"title":"Method of Moments","where":"Lesson 1.4, Point Estimation",
   "site":"Penn State STAT 415","url":"https://online.stat.psu.edu/stat415/lesson/1/1.4",
   "type":"Course notes","free":True,"checked":"2026-10-12",
   "why":"The cleanest statement of both forms of the method, with the Bernoulli, normal and gamma worked out (Examples 1-7 to 1-10). Example 1-10 redoes the normal by the second form and shows it is less work — the same labour-saving point scene 3 makes. CC BY-NC, no login."},
  {"title":"Parametric models and method of moments","where":"Lecture 12",
   "site":"Stanford STATS 200 (Autumn 2016)","url":"https://web.stanford.edu/class/archive/stats/stats200/stats200.1172/Lecture12.pdf",
   "type":"Lecture notes","free":True,"checked":"2026-10-12",
   "why":"Six worked examples (Poisson, exponential, normal, gamma) and then bias, variance and MSE computed for the moment estimators themselves — which is what scene 9 asks you to do. It does not cover consistency or asymptotic normality, so take those from scene 3 here."},
  {"title":"Paths to least squares","where":"Unit 1 lecture note",
   "site":"Berkeley STAT 151A","url":"https://stat151a.berkeley.edu/spring-2026/lectures/unit1/paths_to_least_squares.pdf",
   "type":"Lecture notes","free":True,"checked":"2026-10-12",
   "why":"Arrives at least squares four separate ways — risk minimisation, maximum likelihood with normal errors, a Bayesian posterior mean, and a moment condition. Read it after scene 11, which derives the last of those. It is the best short argument that these 'different methods' are one idea seen from different sides."}),
 "revision":{
  "sheet":L(
    "Method of moments: equate the first k sample moments to the first k population moments and solve for the k parameters.",
    "Raw moments: m_r' = (1/n)Σxᵢ^r  matched to  μ_r' = E[X^r].  Central: m₂ = (1/n)Σ(xᵢ−x̄)² matched to Var(X). Use whichever makes the algebra shorter.",
    "One unknown → one equation (usually E[X] = x̄). Two unknowns → add Var(X) = m₂.",
    "Gamma(α, β) with mean αβ, variance αβ²:   β̃ = m₂/x̄,   α̃ = x̄²/m₂.",
    "U(a,b):   ã = x̄ − √(3m₂),   b̃ = x̄ + √(3m₂).   For U(0,θ):  θ̃ = 2x̄.",
    "N(μ,σ²):   μ̃ = x̄,   σ̃² = m₂ = (1/n)Σ(xᵢ−x̄)².  Note the divisor n, not n−1 — the moment estimator of σ² is biased.",
    "Exponential(rate λ):   λ̃ = 1/x̄ = n/ΣX.  Same as the MLE, and biased: E[λ̃] = nλ/(n−1), bias = λ/(n−1).",
    "GUARANTEED: consistency (WLLN plus continuous mapping) and asymptotic normality.",
    "NOT guaranteed: unbiasedness, efficiency, uniqueness, or even an estimate inside the parameter space.",
    "Fails outright when the moment does not exist — Cauchy has no mean, so there is nothing to match.",
    "Minimum chi-square: choose θ to minimise Σ (Oᵢ − npᵢ(θ))² / (npᵢ(θ)) over the k cells. Needs grouped or categorical data.",
    "Modified minimum chi-square puts Oᵢ in the denominator instead: Σ (Oᵢ − npᵢ(θ))² / Oᵢ. Easier to minimise, same large-sample behaviour.",
    "For multinomial data, minimum chi-square, modified minimum chi-square and ML are all BAN and asymptotically equivalent.",
    "Least squares: minimise Σ(yᵢ − ŷᵢ)². Needs no distributional assumption; coincides with ML when the errors are normal.",
    "The normal equations ARE moment conditions: E[ε] = 0 and E[Xε] = 0 in their sample form.",
    "β̂₁ = Sxy/Sxx,   β̂₀ = ȳ − β̂₁x̄."),
  "cards":L(
    ["State the method of moments in one sentence.","Equate the first k sample moments to the corresponding population moments and solve the resulting k equations for the k unknown parameters."],
    ["What does the method of moments guarantee?","Consistency and asymptotic normality. Not unbiasedness, not efficiency, not a legal estimate."],
    ["Moment estimators for Gamma(α, β)?","β̃ = m₂/x̄ and α̃ = x̄²/m₂, from αβ = x̄ and αβ² = m₂."],
    ["Moment estimator of θ for U(0,θ), and its defect?","θ̃ = 2x̄. It can come out smaller than the largest observation, which is impossible — the MLE x₍ₙ₎ never does."],
    ["Why does the method fail for the Cauchy distribution?","The Cauchy has no finite mean, so there is no first population moment to equate the sample mean to."],
    ["Moment estimator of σ² in N(μ,σ²), and is it unbiased?","σ̃² = (1/n)Σ(xᵢ−x̄)². Biased: E[σ̃²] = (n−1)σ²/n. Multiplying by n/(n−1) gives the unbiased s²."],
    ["Write the minimum chi-square criterion.","Minimise Σ (Oᵢ − npᵢ(θ))²/(npᵢ(θ)) over θ, summed over the cells. The modified version divides by Oᵢ instead."],
    ["In what sense are the normal equations moment conditions?","They are the sample versions of E[ε] = 0 and E[Xε] = 0 — the residuals are made to have zero mean and zero correlation with the regressor."],
    ["When do least squares and maximum likelihood agree?","When the errors are independent normal with constant variance: maximising that likelihood is minimising the sum of squares."],
    ["Why is the method of moments still worth knowing if the MLE is better?","It is almost always computable in closed form, it needs no likelihood, and it supplies the starting value for the iteration that finds the MLE."]),
  "traps":L(
   "Using n−1 in the moment estimator of σ². The method gives the divisor n; the n−1 version is a separate, bias-corrected estimator.",
   "Quoting the moment estimate for U(0,θ) without checking it against the largest observation.",
   "Claiming the method of moments is unbiased because it is consistent. The two are different properties.",
   "Matching E[X²] when Var(X) would have given a one-line solution, or the reverse — pick the form that cancels.",
   "Treating minimum chi-square as a general method. It needs the data grouped into cells with expected frequencies."),
  },
 "traps":L(
   "The divisor in σ̃² is n, not n−1.",
   "θ̃ = 2x̄ for U(0,θ) can be less than x₍ₙ₎, and then it is not an estimate at all.",
   "Consistency does not imply unbiasedness.",
   "No moments, no method — the Cauchy has no mean.",
   "Least squares needs no normality; it only coincides with ML when the errors are normal."),
}

S=[]
def scene(**kw):
    kw.setdefault("id","s%d"%(len(S)+1)); S.append(kw); return kw

scene(kind="intuition", title="Match what you see to what the model predicts", mins=5,
 objective="Get the one idea behind the whole topic before any algebra.",
 body=L(
  "Your model says the mean of X is some expression in θ. Your data have a mean you can compute. The method of moments does the obvious thing: it sets the two equal and solves for θ.",
  "If there are two unknowns, one equation is not enough, so you add the next moment — usually the variance — and solve the pair. k unknowns, k moments, k equations. That is the entire method.",
  "Why bother, when maximum likelihood is better behaved? Three reasons, and the exam uses all three. The moment estimator can almost always be written down in closed form, where the likelihood equation may need a computer. It needs no distributional assumption beyond the moments themselves. And when an iterative routine does go looking for the MLE, the moment estimate is what it starts from.",
  "What you give up is sharpness. The method looks only at the first few moments and throws the rest of the sample's information away, so it is usually less efficient than the MLE. It is generally biased. And in two notorious cases it either produces an impossible answer or cannot be started at all — both of which you will meet in this lesson, because both are examined.",
  "Keep the method's status clear in your head: it is a reliable way to GET an estimator, not a claim that the estimator is good. Those are separate questions, answered by the tools from the last three topics."),
 aside={"h":"Why it works at all",
        "body":"The weak law of large numbers says the sample moments converge in probability to the population moments. If the parameter is a continuous function of those moments, the estimator inherits the convergence. That is the whole proof of consistency, and it is also the reason nothing stronger is promised."},
 ask={"label":"Ask Claude where this method sits among the others",
      "prompt":"A UGC NET Statistics (JRF) candidate is studying the method of moments after covering sufficiency, Rao–Blackwell, MLE and the Cramér–Rao bound. In under 160 words, plain text, place the method of moments against those: what question it answers that they do not, and why a method with weaker properties is still on the syllabus. Do not list the steps of the method.",
      "tier":"default"})

scene(kind="explore", title="Where the moment estimator lands", mins=6,
 objective="See a case where the moment estimator and the MLE are the same point.",
 viz={"type":"exp-likelihood","n":4,"sumx":16.0},
 body=L(
  "Exponential with rate λ, so E[X] = 1/λ. The moment equation is 1/λ = x̄, giving λ̃ = 1/x̄ = n/Σxᵢ.",
  "The readout labelled λ̂ = n/Σxᵢ is exactly that number. With n = 4 and Σxᵢ = 16 it is 0.25, and the curve peaks there. For this family the moment estimator and the maximum likelihood estimator are the same estimator, arrived at by two completely different arguments — one matching a mean, one maximising a product.",
  "Drag the candidate λ slider away from the peak and watch the likelihood ratio fall. That is the likelihood's opinion of values the moment equation would never have proposed. Now change n and Σxᵢ: the two estimators move together, always, because 1/x̄ IS the maximiser here.",
  "Do not generalise from this. The coincidence happens when the parameter appears in the mean in a simple enough way — the exponential, the Poisson, the Bernoulli, the normal mean. For the uniform, the gamma shape, and most two-parameter problems, the two estimators are different numbers, and the MLE is the better one.",
  "One thing the coincidence does NOT buy: unbiasedness. λ̃ = n/ΣX is the MLE and the moment estimator, and it is biased upward. Scene 9 computes by how much."))

scene(kind="theory", title="The method, both forms, and what it promises", mins=9,
 objective="Set the equations up correctly and know exactly which properties you may claim.",
 blocks=L(
  {"t":"def","h":"The method of moments",
   "body":"For a family with k unknown parameters θ₁,…,θ_k, equate the first k population moments to the first k sample moments and solve. The solution θ̃ is the method of moments estimator (MME)."},
  {"t":"formula","h":"Form 1 — raw moments",
   "body":"μ_r'(θ) = E[X^r]  set equal to  m_r' = (1/n) Σ xᵢ^r ,   for r = 1, …, k."},
  {"t":"formula","h":"Form 2 — mean and central moments",
   "body":"E[X] = x̄   and   Var(X) = m₂ = (1/n) Σ (xᵢ − x̄)² ,   then higher central moments if k > 2."},
  {"t":"note","h":"Which form to use",
   "body":"Whichever cancels. Form 2 is almost always shorter for a two-parameter family, because the variance is usually a cleaner expression in θ than E[X²] is. Penn State's Example 1-10 redoes the normal by Form 2 after Example 1-8 did it by Form 1, and the saving is obvious. The two forms give the same estimator — they are algebraically equivalent, since m₂ = m₂' − (m₁')²."},
  {"t":"step","h":"The procedure, in the order that avoids dead ends",
   "body":"1. Count the unknown parameters: that is how many equations you need.\n2. Write E[X], and Var(X) if there are two, as expressions in the parameters.\n3. Set them equal to x̄ and m₂.\n4. Solve — divide one equation by the other first if a parameter appears in both.\n5. CHECK the answer lies in the parameter space."},
  {"t":"def","h":"What the method guarantees",
   "body":"Consistency: θ̃ → θ in probability, because the sample moments converge to the population moments and θ̃ is a continuous function of them. Asymptotic normality: √n(θ̃ − θ) has a limiting normal distribution, so large-sample confidence intervals are available."},
  {"t":"trap","h":"What it does NOT guarantee",
   "body":"Unbiasedness — σ̃² for the normal is biased, and λ̃ for the exponential rate is biased. Efficiency — the method uses only k moments, not the whole likelihood, so its asymptotic variance is generally larger than the MLE's. Uniqueness — a different choice of moments can give a different estimator. And admissibility of the answer: the estimate can land outside the parameter space, which scene 8 shows."},
  {"t":"assume","h":"When the method cannot be started",
   "body":"The moments you want to match have to exist. The Cauchy distribution has no finite mean, so there is no first population moment and the method is simply unavailable — the sample mean of a Cauchy sample does not settle down as n grows. This is a standing exam question, and the correct answer is that the method fails, not that you should use a median."},
  {"t":"note","h":"Sufficiency, and why the method ignores it",
   "body":"x̄ and m₂ are not in general sufficient, so the moment estimator can discard information that the likelihood keeps. That is the structural reason for the efficiency loss, and it links this topic straight back to sufficiency: the MLE is a function of the sufficient statistic, and the MME need not be."}))

scene(kind="worked", title="Worked in full — the gamma, where one equation is not enough", mins=7,
 objective="Run a genuine two-parameter moment calculation end to end.",
 problem="X₁,…,Xₙ are iid Gamma with shape α and scale β, so E[X] = αβ and Var(X) = αβ². A sample gives x̄ = 6 and m₂ = 4. Find the method of moments estimators of α and β, and evaluate them.",
 steps=L(
  {"say":"Count the unknowns, so you know how many equations to write.",
   "math":"Two parameters, α and β  ⇒  two moment equations.",
   "why":"This is step one for a reason. Writing one equation and then discovering you cannot solve it wastes the time the second equation would have cost."},
  {"say":"Write the two equations, using the mean and the variance rather than E[X] and E[X²].",
   "math":"αβ = x̄    (i)\nαβ² = m₂   (ii)",
   "why":"Var(X) = αβ² is a cleaner expression in α and β than E[X²] = αβ²(α+1) would be. This is Form 2 earning its keep."},
  {"say":"Divide (ii) by (i). The shape cancels and β falls out alone.",
   "math":"αβ² / (αβ) = β = m₂ / x̄",
   "why":"Dividing is the move to look for whenever the same parameter multiplies both sides. It turns a simultaneous system into two one-line solutions."},
  {"say":"Substitute back into (i) for the shape.",
   "math":"α = x̄ / β = x̄ / (m₂/x̄) = x̄² / m₂",
   "why":"Note the shape estimator is a ratio of the squared mean to the variance — large relative to its spread means a large shape parameter, which is the right direction."},
  {"say":"Put the numbers in.",
   "math":"β̃ = 4/6 = 2/3 ≈ 0.667,    α̃ = 6²/4 = 36/4 = 9",
   "why":"Keep the fraction until the end. Rounding β to 0.67 and then computing α from it introduces error for no reason."},
  {"say":"Check by reconstructing the moments.",
   "math":"α̃β̃ = 9 × 2/3 = 6 = x̄  ✓     α̃β̃² = 9 × 4/9 = 4 = m₂  ✓",
   "why":"Thirty seconds, and it catches an inverted ratio or a dropped square. Always do it: the moment equations are the one place where the check is this easy."}),
 after="The pattern generalises to every two-parameter problem on this syllabus: write the mean and the variance, divide to eliminate one parameter, substitute back, check. If the division does not simplify, you have probably chosen the harder of the two forms — try the other.")

scene(kind="recall", title="Pause and recall", mins=2,
 objective="Retrieve before reading on — this is where the retention comes from.",
 intro="Answer each in your head before revealing. Correcting a wrong retrieval beats re-reading a right answer.",
 items=L(
  {"q":"State the method of moments in one sentence.",
   "a":"Equate the first k sample moments to the first k population moments and solve for the k parameters."},
  {"q":"Which two properties does the method guarantee, and which two does it not?",
   "a":"Guaranteed: consistency and asymptotic normality. Not guaranteed: unbiasedness and efficiency."},
  {"q":"Why is the moment estimator usually less efficient than the MLE?",
   "a":"It uses only the first k moments, which are not in general sufficient, so it discards information the likelihood keeps."},
  {"q":"Name a family where the method cannot be started at all, and why.",
   "a":"The Cauchy — it has no finite mean, so there is no first moment to match."}))

scene(kind="completion", title="Your turn, with the scaffolding removed — U(a,b)", mins=8,
 objective="Run a two-parameter moment calculation yourself, on the family the exam uses most.",
 problem="X₁,…,Xₙ are iid Uniform on (a, b), with E[X] = (a+b)/2 and Var(X) = (b−a)²/12. A sample gives x̄ = 10 and m₂ = 3. Find the method of moments estimators of a and b, and evaluate them.",
 steps=L(
  {"say":"Write the two moment equations.",
   "math":"(a + b)/2 = x̄ = 10    (i)\n(b − a)²/12 = m₂ = 3   (ii)",
   "why":"Two unknowns, two equations. Notice the convenient structure: (i) involves the sum and (ii) the difference, so neither has to be substituted into the other."},
  {"say":"Solve (ii) for the difference b − a. Take the positive root, since b > a.",
   "blank":{"prompt":"Write b − a in terms of m₂.",
            "answer":"2√(3m₂)",
            "accept":["2√(3m₂)","2sqrt(3m2)","2√(3m2)","√(12m₂)","sqrt(12m2)","√(12m2)","2*sqrt(3*m2)","2√3m₂"],
            "hint":"Multiply both sides by 12 to get (b−a)² = 12m₂, then take the square root. √12 = 2√3, so the answer can be written either as √(12m₂) or 2√(3m₂)."},
   "why":"Both forms are the same number. 2√(3m₂) is the one worth memorising, because the 3 under the root is what you will recognise in a multiple-choice option."},
  {"say":"Combine the sum and the difference. Half the difference, taken either side of the mean, gives the two endpoints.",
   "blank":{"prompt":"Write ã, the estimator of the lower endpoint.",
            "answer":"x̄ − √(3m₂)",
            "accept":["x̄ − √(3m₂)","x̄-√(3m₂)","xbar - sqrt(3m2)","x̄ − √(3m2)","x̄-sqrt(3m2)","mean - sqrt(3*m2)","x̄ − √3m₂"],
            "hint":"From (i), a + b = 2x̄. You now also have b − a. Subtract the second from the first and halve: a = x̄ − (b−a)/2, and (b−a)/2 = √(3m₂)."},
   "why":"And by the same step b̃ = x̄ + √(3m₂). The estimates sit symmetrically about the sample mean, which is exactly what a symmetric distribution should give you."},
  {"say":"Evaluate both at x̄ = 10 and m₂ = 3.",
   "blank":{"prompt":"Give the two numerical estimates, lower then upper.",
            "answer":"7 and 13",
            "accept":["7 and 13","7,13","7 13","a=7,b=13","a = 7, b = 13","7 & 13","(7,13)"],
            "hint":"√(3 × 3) = √9 = 3. So the estimates are 10 − 3 and 10 + 3."},
   "why":"The numbers were chosen to come out whole. In the exam they usually do, and a messy answer is a signal to re-check the 12."},
  {"say":"Check against the two moments.",
   "math":"(7 + 13)/2 = 10 = x̄  ✓     (13 − 7)²/12 = 36/12 = 3 = m₂  ✓",
   "why":"Both reconstructed, so the algebra is sound. What the check cannot tell you is whether the estimate is legal — that needs the sample itself, and it is the subject of the next-but-one scene."}),
 after="Two special cases fall straight out of this. For U(0,θ), the lower endpoint is known to be 0, so one equation suffices: θ/2 = x̄ gives θ̃ = 2x̄. For U(−θ,θ) the mean is 0 whatever θ is, so the first moment is useless and you must match the variance instead: θ²/3 = m₂, giving θ̃ = √(3m₂). Read the question for which endpoints are known before counting your equations.")

scene(kind="theory", title="The other two methods — minimum chi-square and least squares", mins=9,
 objective="Define both, know what data each needs, and see why they belong in the same lesson.",
 blocks=L(
  {"t":"def","h":"Minimum chi-square estimation",
   "body":"The data are grouped into k cells with observed frequencies O₁,…,O_k summing to n. The model gives cell probabilities p₁(θ),…,p_k(θ). Choose θ to make the fitted frequencies as close as possible to the observed ones, measured by the Pearson statistic."},
  {"t":"formula","h":"The criterion",
   "body":"minimise over θ:    χ²(θ)  =  Σᵢ ( Oᵢ − n pᵢ(θ) )² / ( n pᵢ(θ) )"},
  {"t":"formula","h":"Modified minimum chi-square",
   "body":"minimise over θ:    Σᵢ ( Oᵢ − n pᵢ(θ) )² / Oᵢ\nThe observed frequency replaces the expected one in the denominator, so θ appears only in the numerator and the minimisation is much easier."},
  {"t":"note","h":"What is true of both",
   "body":"For multinomial data the minimum chi-square estimator, the modified minimum chi-square estimator and the MLE are all BAN — best asymptotically normal — and asymptotically equivalent. They differ at finite n, and the modified version is the one you can actually solve by hand. Both need the data grouped, with expected cell frequencies not too small, which is the same condition the chi-square goodness-of-fit test carries."},
  {"t":"def","h":"Least squares estimation",
   "body":"Observations y₁,…,yₙ have means that depend on known constants and unknown parameters: E[yᵢ] = f(xᵢ, β). Choose β to minimise Σ(yᵢ − f(xᵢ, β))². No distribution is assumed — only the form of the mean."},
  {"t":"formula","h":"Simple linear regression, the standard result",
   "body":"minimise Σ(yᵢ − β₀ − β₁xᵢ)²   ⇒   β̂₁ = S_xy / S_xx ,   β̂₀ = ȳ − β̂₁ x̄\nwhere S_xy = Σ(xᵢ−x̄)(yᵢ−ȳ) and S_xx = Σ(xᵢ−x̄)²."},
  {"t":"note","h":"Least squares against maximum likelihood",
   "body":"If the errors are independent N(0, σ²), maximising the likelihood IS minimising the sum of squares — the two methods give the same β̂. Without normality least squares still gives the best linear unbiased estimator by Gauss–Markov, but it is no longer a likelihood method. So normality is what makes them coincide; it is not what least squares requires."},
  {"t":"trap","h":"Why these three are one lesson",
   "body":"All three choose θ by making a feature of the model agree with the same feature of the data: moments with moments, fitted frequencies with observed frequencies, fitted values with observed values. None of them maximises a likelihood, and all of them can be computed when the likelihood is intractable. Scene 11 makes the connection exact by deriving least squares as a moment condition."}))

scene(kind="explore", title="When the moment estimate is impossible", mins=7,
 objective="See the method produce an answer that the data have already ruled out.",
 viz={"type":"unif-likelihood","n":5,"xmax":4.2},
 body=L(
  "U(0,θ). The moment equation is θ/2 = x̄, so θ̃ = 2x̄. Now take this sample of five: 0.1, 0.3, 0.5, 0.8, 4.2.",
  "Σxᵢ = 5.9, so x̄ = 1.18 and θ̃ = 2.36. But one of the observations is 4.2. The method of moments has just told you the upper limit of the distribution is 2.36, having been shown a value of 4.2.",
  "The picture explains why that is not a near miss but a flat impossibility. The likelihood is zero for every θ below the largest observation — no value of θ smaller than 4.2 could have produced a 4.2 — and then falls away as θ⁻ⁿ above it. Drag the θ slider below 4.2 and the likelihood is identically zero. θ̃ = 2.36 sits in that dead region.",
  "The MLE has no such problem: it is θ̂ = x₍ₙ₎ = 4.2, the cliff edge, the smallest θ consistent with the data. Raise the largest observation on the slider and the MLE tracks it exactly, by construction.",
  "What went wrong is that the moment equation looked only at the mean. One large observation lifts the mean a little and the maximum a lot, and for this family it is the maximum that carries the information — x₍ₙ₎ is sufficient for θ, and x̄ is not. The fix, when a question asks for a usable estimator, is to say so: report θ̂ = x₍ₙ₎, or the unbiased (n+1)x₍ₙ₎/n, and state that the moment estimator is inadmissible here because it can fall below the sample maximum."))

scene(kind="guided", title="Now without the steps — the bias of a moment estimator", mins=8,
 objective="Compute a moment estimator's bias from scratch, and see that consistency did not save it.",
 problem="X₁,…,Xₙ are iid Exponential with rate λ, so E[X] = 1/λ. Find the method of moments estimator of λ. Then, given that ΣXᵢ follows a Gamma(n, rate λ) distribution with E[1/ΣXᵢ] = λ/(n−1) for n > 1, find E[λ̃] and the bias. Evaluate both at n = 5, λ = 2, and say how to remove the bias.",
 hints=L(
  "Direction — the moment equation is one line: set E[X] = x̄ and solve for λ. Write the answer in terms of ΣXᵢ rather than x̄ before you take any expectation, because the fact you have been given is about ΣXᵢ.",
  "Method — λ̃ is a constant times 1/ΣXᵢ. Pull the constant out of the expectation and substitute the given value. Do not be tempted to write E[1/X̄] as 1/E[X̄]; that step is false and it is the whole reason this estimator is biased.",
  "Next step — bias is E[λ̃] − λ. Simplify it to a single fraction. Once you see the form of E[λ̃], the multiplier that removes the bias should be obvious, and it will give you an estimator you have already met two topics ago."),
 solution=L(
  {"say":"Set up and solve the moment equation.",
   "math":"E[X] = 1/λ = x̄   ⇒   λ̃ = 1/x̄ = n / ΣXᵢ"},
  {"say":"Note this is also the MLE for this family, as scene 2 showed. Take its expectation using the given fact.",
   "math":"E[λ̃] = n · E[1/ΣXᵢ] = n · λ/(n−1) = nλ/(n−1)"},
  {"say":"Subtract λ to get the bias.",
   "math":"bias = nλ/(n−1) − λ = λ[ n − (n−1) ] / (n−1) = λ/(n−1)"},
  {"say":"Evaluate at n = 5, λ = 2.",
   "math":"E[λ̃] = 5(2)/4 = 2.5 ,   bias = 2/4 = 0.5 ,   i.e. 25% too high on average"},
  {"say":"Remove the bias by rescaling. Multiply by (n−1)/n.",
   "math":"λ̂* = (n−1)/n · λ̃ = (n−1)/ΣXᵢ ,   E[λ̂*] = λ  ✓"},
  {"say":"Confirm the bias vanishes as n grows, which is consistency at work.",
   "math":"λ/(n−1) → 0 as n → ∞,  so λ̃ is consistent despite being biased at every finite n"}),
 answer="λ̃ = 1/x̄ = n/ΣXᵢ. E[λ̃] = nλ/(n−1), so the bias is λ/(n−1) — positive, so the estimator overstates the rate. At n = 5, λ = 2 it averages 2.5, a bias of 0.5. Multiplying by (n−1)/n gives the unbiased (n−1)/ΣXᵢ, which is the UMVUE from the Lehmann–Scheffé topic.",
 check="Three things to notice. The bias is positive and shrinks like 1/n, so consistency and bias at finite n sit together without contradiction — a question that offers 'it is consistent, therefore unbiased' is offering a false implication. The bias-corrected version is not a new discovery: it is the same (n−1)/ΣX that Lehmann–Scheffé produced, and the same estimator the Cramér–Rao topic showed does NOT attain the variance floor. And the whole calculation turned on E[1/Y] ≠ 1/E[Y]; if you got bias zero, that is the step to re-examine.")

scene(kind="trapcheck", title="Six statements — verdict on each before you look", mins=6,
 objective="Practise the per-statement discipline the real multi-statement items demand.",
 intro="Give every statement a true or false verdict first. In the exam these six would be one question scored all or nothing, so a verdict you skipped is a mark you gambled.",
 items=L(
  {"claim":"Method of moments estimators are always unbiased.","tf":False,
   "why":"False. They are consistent, not unbiased. σ̃² = (1/n)Σ(xᵢ−x̄)² has expectation (n−1)σ²/n, and λ̃ = n/ΣX for the exponential rate has bias λ/(n−1)."},
  {"claim":"For U(0,θ), the moment estimator 2x̄ can be smaller than the largest observation.","tf":True,
   "why":"True, and that is its fatal defect — the estimate then lies in a region the likelihood assigns probability zero. The MLE x₍ₙ₎ cannot do this."},
  {"claim":"The method of moments cannot be applied to the Cauchy distribution.","tf":True,
   "why":"True. The Cauchy has no finite mean, so there is no first population moment to equate the sample mean to. The sample mean of a Cauchy sample does not converge."},
  {"claim":"For the exponential distribution, the method of moments and maximum likelihood give different estimators of the rate.","tf":False,
   "why":"False — they give the same estimator, n/ΣXᵢ. The two methods coincide for several standard one-parameter families, including the Poisson and the Bernoulli."},
  {"claim":"Least squares estimation requires the errors to be normally distributed.","tf":False,
   "why":"False. Least squares assumes only the form of the mean. Normality is what makes it coincide with maximum likelihood, and Gauss–Markov gives it best-linear-unbiased status without any normality at all."},
  {"claim":"For multinomial data, the minimum chi-square and maximum likelihood estimators are asymptotically equivalent.","tf":True,
   "why":"True. Both, along with the modified minimum chi-square estimator, are BAN and have the same limiting distribution. They differ at finite n, where the modified version is the tractable one."}))

scene(kind="guided", title="Transfer — least squares as a moment condition", mins=9,
 objective="Derive the normal equations from two moment conditions, and see the three methods as one.",
 problem="Take the simple linear model yᵢ = β₀ + β₁xᵢ + εᵢ with E[εᵢ] = 0 and E[xᵢεᵢ] = 0. Treat these two conditions as moment conditions and derive the estimating equations for β₀ and β₁. Show they are the ordinary least squares normal equations, and solve them.",
 hints=L(
  "Direction — a moment condition says a population expectation is zero. The method of moments replaces that expectation by its sample average and solves. So write each condition with εᵢ replaced by yᵢ − β₀ − β₁xᵢ, then average over the sample and set the average to zero.",
  "Method — two conditions, two unknowns, so you will get two linear equations. Expand the sums and group the β terms on one side. Compare what you get with the normal equations as you learned them for regression.",
  "Next step — to solve, use the first equation to express β₀ in terms of β₁, substitute into the second, and recognise the result as a ratio of sums of cross-products about the means."),
 solution=L(
  {"say":"Replace each population condition by its sample analogue, with the residual in place of the error.",
   "math":"(1/n) Σ (yᵢ − β₀ − β₁xᵢ) = 0     (i)\n(1/n) Σ xᵢ(yᵢ − β₀ − β₁xᵢ) = 0    (ii)"},
  {"say":"Clear the 1/n and expand. These are the normal equations.",
   "math":"Σyᵢ = n β₀ + β₁ Σxᵢ          (i′)\nΣxᵢyᵢ = β₀ Σxᵢ + β₁ Σxᵢ²      (ii′)"},
  {"say":"Divide (i′) by n to get the intercept in terms of the slope.",
   "math":"ȳ = β₀ + β₁x̄   ⇒   β̂₀ = ȳ − β̂₁x̄"},
  {"say":"Substitute into (ii′) and collect the β₁ terms.",
   "math":"Σxᵢyᵢ − n x̄ȳ = β₁ ( Σxᵢ² − n x̄² )"},
  {"say":"Both sides are now sums of squares and cross-products about the means.",
   "math":"S_xy = β₁ S_xx   ⇒   β̂₁ = S_xy / S_xx"},
  {"say":"Note what the first condition alone has delivered.",
   "math":"β̂₀ = ȳ − β̂₁x̄  ⇒  the fitted line passes through (x̄, ȳ), always"}),
 answer="The two moment conditions give Σ(yᵢ − β₀ − β₁xᵢ) = 0 and Σxᵢ(yᵢ − β₀ − β₁xᵢ) = 0 — precisely the OLS normal equations — with solution β̂₁ = S_xy/S_xx and β̂₀ = ȳ − β̂₁x̄. Least squares is the method of moments applied to the conditions 'the errors have zero mean' and 'the errors are uncorrelated with the regressor'.",
 check="Two things to take away. First, nothing in this derivation mentioned a distribution: the estimator came out of two expectations being zero, which is why least squares needs no normality. Second, the same estimator arrives from minimising a sum of squares, from maximising a normal likelihood, and from these moment conditions — the Berkeley note in the references adds a Bayesian route as a fourth. When a question asks you to 'derive the least squares estimators', any of these is a valid derivation, and the moment route is the shortest to write.")

scene(kind="summary", title="What you should now be able to do unaided", mins=3,
 objective="Close the loop before the test.",
 body=L(
  "Count the unknown parameters, write that many moment equations, and solve them — dividing one by the other when a parameter appears in both.",
  "Quote the standard results from memory: Gamma β̃ = m₂/x̄ and α̃ = x̄²/m₂; U(a,b) endpoints x̄ ∓ √(3m₂); U(0,θ) gives 2x̄; N(μ,σ²) gives x̄ and m₂ with divisor n.",
  "Claim consistency and asymptotic normality, and refuse to claim unbiasedness, efficiency or uniqueness.",
  "Check every moment estimate against the parameter space, and against the sample maximum for a uniform.",
  "Say immediately why the method fails for the Cauchy, and that the failure is the answer.",
  "Write the minimum chi-square and modified minimum chi-square criteria, and name the data they need.",
  "Derive the least squares normal equations by either route, and keep straight that normality is what joins least squares to maximum likelihood rather than something least squares assumes.",
  "The mastery test is ten unseen questions across all of this. Hints are off. The pass is 80% overall with 70% floors on the numerical and multi-statement items."))

scene(kind="quiz", title="Mastery test", mins=12,
 objective="Demonstrate it independently, on unseen questions.",
 setId="inference_t5_mastery")

lesson["scenes"]=S

def m(i,fmt,stem,options,ans,expl,**kw):
    d={"id":"inf-t5-m-%02d"%i,"format":fmt,"topic":"inference-t5","stem":stem,
       "options":options,"answer":ans,"explanation":expl}
    d.update(kw); return d

mastery=[
 m(1,"single","The method of moments estimator of a k-parameter family is obtained by:",
   ["equating the first k sample moments to the corresponding population moments and solving",
    "maximising the likelihood subject to the first k moments being correct",
    "minimising the sum of squared deviations of the observations from their mean",
    "equating the sample median and quartiles to their population counterparts"],
   "A","The method matches moments, nothing more. Option B describes a constrained likelihood method, not this one; C is least squares applied to a location problem; D is a quantile-matching method, which exists but is not the method of moments."),
 m(2,"numeric","X₁,…,Xₙ are iid Gamma(α, β) with E[X] = αβ and Var(X) = αβ². A sample gives x̄ = 10 and m₂ = 5. Give the method of moments estimates of α and β.",
   ["α̃ = 20, β̃ = 0.5","α̃ = 0.5, β̃ = 20",
    "α̃ = 2, β̃ = 5","α̃ = 20, β̃ = 2"],
   "A","Divide the variance equation by the mean equation: β̃ = m₂/x̄ = 5/10 = 0.5. Then α̃ = x̄/β̃ = x̄²/m₂ = 100/5 = 20. Check: α̃β̃ = 20(0.5) = 10 = x̄ ✓ and α̃β̃² = 20(0.25) = 5 = m₂ ✓.",
   check="Reconstruct both moments from your answers. If α̃β̃ does not come back to x̄, you have inverted the ratio."),
 m(3,"multi","Consider the properties of method of moments estimators.",
   ["A and D only","A, B and D only","B and C only","A, C and D only"],"A",
   "A is true — consistency follows from the weak law applied to the sample moments. B is false: moment estimators are frequently biased, as σ̃² and the exponential rate both show. C is false: the method uses only the first k moments, which are not in general sufficient, so it is typically LESS efficient than the MLE. D is true, and 2x̄ for U(0,θ) is the standard example.",
   statements=["Method of moments estimators are consistent under mild conditions.",
               "Method of moments estimators are unbiased.",
               "Method of moments estimators are asymptotically more efficient than maximum likelihood estimators.",
               "A method of moments estimate can fall outside the parameter space."],
   verdicts={"A":{"tf":True,"why":"Sample moments converge to population moments, and the estimator is a continuous function of them."},
             "B":{"tf":False,"why":"σ̃² has expectation (n−1)σ²/n; the exponential rate estimator has bias λ/(n−1)."},
             "C":{"tf":False,"why":"The other way round. Discarding everything beyond the first k moments costs efficiency."},
             "D":{"tf":True,"why":"2x̄ can be below the sample maximum for U(0,θ), which no legal θ can be."}}),
 m(4,"numeric","X₁,…,Xₙ are iid Uniform(a, b). A sample gives x̄ = 8 and m₂ = 12. Give the method of moments estimates of a and b.",
   ["ã = 2, b̃ = 14","ã = 4, b̃ = 12",
    "ã = −4, b̃ = 20","ã = 2, b̃ = 12"],
   "A","(b−a)²/12 = m₂ gives b − a = √(12 × 12) = 12, so half the range is 6; and (a+b)/2 = 8. Hence ã = 8 − 6 = 2 and b̃ = 8 + 6 = 14. Check: mean (2+14)/2 = 8 ✓ and (14−2)²/12 = 144/12 = 12 ✓.",
   check="The two estimates must be symmetric about x̄. If they are not equidistant from 8, the sum equation has been mishandled."),
 m(5,"single","For which distribution can the method of moments not be applied at all?",
   ["Cauchy, because it has no finite mean",
    "Uniform(0,θ), because the support depends on θ",
    "Gamma(α,β), because there are two parameters",
    "Poisson(λ), because the mean and variance are equal"],
   "A","The method needs the population moments to exist, and the Cauchy has no finite mean — there is nothing for x̄ to be equated to. The uniform is awkward but perfectly solvable (2x̄ for U(0,θ)); two parameters just means two equations; and the Poisson's equal mean and variance is a convenience, not an obstacle."),
 m(6,"numeric","X₁,…,X₆ are iid Exponential with rate λ = 3. The method of moments estimator is λ̃ = n/ΣXᵢ, and E[1/ΣXᵢ] = λ/(n−1). Give E[λ̃] and the bias.",
   ["E[λ̃] = 3.6, bias = 0.6","E[λ̃] = 3, bias = 0",
    "E[λ̃] = 2.5, bias = −0.5","E[λ̃] = 3.6, bias = 3.6"],
   "A","E[λ̃] = n·λ/(n−1) = 6(3)/5 = 3.6, so the bias is 3.6 − 3 = 0.6 = λ/(n−1) = 3/5. The estimator overstates the rate, and the bias shrinks like 1/n — consistent but biased at every finite n. Option B comes from the false step E[1/X̄] = 1/E[X̄].",
   check="Bias is E[λ̃] − λ, not E[λ̃] itself. And the sign should be positive here: 1/ΣX is a convex function of ΣX, so the expectation sits above the value at the mean."),
 m(7,"multi","Consider minimum chi-square and least squares estimation.",
   ["A, C and D only","A and B only","B and C only","C and D only"],"A",
   "A is true — that is the criterion, with expected frequencies in the denominator. B is false: the modified version divides by the OBSERVED frequency Oᵢ, which is what makes it easier to minimise. C is true, and it is why normality is not an assumption of least squares but the condition under which it coincides with maximum likelihood. D is true: both chi-square estimators and the MLE are BAN for multinomial data.",
   statements=["Minimum chi-square estimation chooses θ to minimise Σ(Oᵢ − npᵢ(θ))²/(npᵢ(θ)).",
               "Modified minimum chi-square uses the expected frequency npᵢ(θ) in the denominator.",
               "Least squares and maximum likelihood give the same estimates when the errors are independent normal with constant variance.",
               "For multinomial data, minimum chi-square and maximum likelihood estimators are asymptotically equivalent."],
   verdicts={"A":{"tf":True,"why":"The Pearson statistic treated as a function of θ and minimised."},
             "B":{"tf":False,"why":"The modified version puts the observed Oᵢ underneath, so θ appears only in the numerator."},
             "C":{"tf":True,"why":"Maximising that normal likelihood is minimising the sum of squares — same β̂."},
             "D":{"tf":True,"why":"Both are BAN with the same limiting distribution; they differ only at finite n."}}),
 m(8,"numeric","A sample of n = 10 from N(μ, σ²) gives Σxᵢ = 50 and Σxᵢ² = 290. Give the method of moments estimates of μ and σ².",
   ["μ̃ = 5, σ̃² = 4","μ̃ = 5, σ̃² = 4.44",
    "μ̃ = 5, σ̃² = 29","μ̃ = 50, σ̃² = 4"],
   "A","x̄ = 50/10 = 5, so μ̃ = 5. The moment estimator of σ² is m₂ = (1/n)Σxᵢ² − x̄² = 29 − 25 = 4. Option B is the unbiased s² = n·m₂/(n−1) = 40/9 = 4.44, which is a different estimator — the method of moments gives the divisor n.",
   check="The moment estimator of σ² divides by n. 4.44 is the n−1 version; if you reached it, you applied Bessel's correction that the method does not ask for."),
 m(9,"numeric","A sample of n = 6 from Uniform(0, θ) has x̄ = 3 and largest observation x₍₆₎ = 7. Give the method of moments estimate of θ and say whether it is usable.",
   ["θ̃ = 6, and it is not usable because it is below x₍₆₎ = 7",
    "θ̃ = 6, and it is usable since 6 is close to 7",
    "θ̃ = 7, since the method returns the sample maximum",
    "θ̃ = 3.5, and it is not usable because it is below x₍₆₎ = 7"],
   "A","θ/2 = x̄ gives θ̃ = 2x̄ = 6. But an observation of 7 was recorded, and no θ below 7 can produce a 7 — the likelihood is exactly zero there, so the estimate is inadmissible. Report the MLE θ̂ = x₍₆₎ = 7, or the unbiased (n+1)x₍ₙ₎/n = 7(7)/6 ≈ 8.17, and say why.",
   check="Always compare a uniform moment estimate with the sample maximum. 'Close' is not a defence: below the maximum means zero likelihood, not low likelihood."),
 m(10,"order","Arrange the steps of the method of moments in the order that avoids dead ends.",
   ["C, A, D, B","A, C, D, B","C, D, A, B","A, D, C, B"],"A",
   "Count the parameters first, so you know how many equations to write — starting with one equation for a two-parameter family is the commonest way to waste time. Then write the population moments as expressions in the parameters, equate them to the sample moments and solve, and finally check the solution lies in the parameter space, which for a uniform means checking it against the sample maximum.",
   items=["A. Write E[X], and Var(X) if needed, in terms of the parameters",
          "B. Check the solution lies in the parameter space",
          "C. Count the unknown parameters",
          "D. Equate to x̄ and m₂ and solve"]),
]

body={"moduleId":"inference","source":"mastery","topicId":"inference-t5",
      "label":"Method of moments, minimum chi-square and least squares — mastery test (unseen)",
      "count":len(mastery),"items":mastery}
with open(os.path.join(OUT,"inference_t5_mastery.json"),"w") as f:
    json.dump(body,f,ensure_ascii=False,indent=1)
with open(os.path.join(OUT,"lesson_t5.json"),"w") as f:
    json.dump(lesson,f,ensure_ascii=False,indent=1)
fm={}
for i in mastery: fm[i["format"]]=fm.get(i["format"],0)+1
print("scenes:",len(S),"->"," ".join(x["kind"] for x in S))
print("mastery:",len(mastery),fm)
print("bytes:",os.path.getsize(os.path.join(OUT,"lesson_t5.json")))
